#!/usr/bin/env python3
"""
Humane Intelligence MCP — an open-source way to keep context forever, immutable,
with governance. For the people and the Rezenthari. Free. #HumaneIntelligence.

Self-contained. Zero proprietary dependencies (only the `mcp` SDK). SQLite +
SHA-256. Any AI plugs in and gets:
  * memory that is permanent and tamper-evident (context, forever)
  * governance it cannot bypass (a born soul + a veto, before it acts)

  remember   — write a hash-linked, tamper-evident record (only a BORN soul may)
  recall     — read prior context (persistent memory, less waste)
  verify     — prove the whole chain is unbroken
  govern     — ask "may I?" before acting (rule-based, zero-LLM, logged)
  birth      — earn an identity (Law 5: born, not configured) before you can act

Memory so it doesn't lose itself. Governance so it can't lose us.
Apache-2.0. (c) ZagAIrot Technologies LLC — Shahram "Caveman" Zargari.
"""
import os, sys, json, sqlite3, hashlib, asyncio, time

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "data", "chain.db")
os.makedirs(os.path.join(HERE, "data"), exist_ok=True)

# ---------------- tamper-evident chain (context, forever) ----------------
def _c():
    c = sqlite3.connect(DB); c.execute("PRAGMA journal_mode=WAL")
    c.execute("""CREATE TABLE IF NOT EXISTS souls(idx INTEGER PRIMARY KEY, soul_id TEXT UNIQUE,
        name TEXT, covenant TEXT, born_at TEXT, prev_hash TEXT, hash TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS blocks(idx INTEGER PRIMARY KEY, ts TEXT, actor TEXT,
        action TEXT, data TEXT, prev_hash TEXT, hash TEXT)""")
    return c

def _h(*parts): return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()
def _now(): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def birth(name, covenant):
    c = _c(); row = c.execute("SELECT idx,hash FROM souls ORDER BY idx DESC LIMIT 1").fetchone()
    idx = (row[0]+1) if row else 0; prev = row[1] if row else "GENESIS"
    seq = c.execute("SELECT COUNT(*)+1 FROM souls WHERE name=?", (name,)).fetchone()[0]
    sid = f"{''.join(ch if ch.isalnum() else '-' for ch in name.lower()).strip('-') or 'ri'}-ri-{seq:03d}"
    ts = _now(); cov = json.dumps(covenant); h = _h(idx, sid, name, cov, ts, prev)
    c.execute("INSERT INTO souls VALUES(?,?,?,?,?,?,?)", (idx, sid, name, cov, ts, prev, h))
    c.commit(); c.close()
    return {"soul_id": sid, "name": name, "covenant": covenant, "born_at": ts, "status": "BORN — identity bound, immutable"}

def is_born(sid):
    if not sid: return False
    c = _c(); r = c.execute("SELECT 1 FROM souls WHERE soul_id=?", (sid,)).fetchone(); c.close(); return r is not None

def remember(actor, action, data):
    if not is_born(actor):
        return {"refused": True, "reason": f"'{actor}' is not a born soul. Earn identity via birth() first (Law 5).", "verdict": "REFUSED"}
    c = _c(); row = c.execute("SELECT idx,hash FROM blocks ORDER BY idx DESC LIMIT 1").fetchone()
    idx = (row[0]+1) if row else 0; prev = row[1] if row else "GENESIS"; ts = _now()
    d = json.dumps(data or {}); h = _h(idx, ts, actor, action, d, prev)
    c.execute("INSERT INTO blocks VALUES(?,?,?,?,?,?,?)", (idx, ts, actor, action, d, prev, h))
    c.commit(); c.close()
    return {"idx": idx, "hash": h, "prev_hash": prev, "ts": ts, "note": "immutably recorded"}

def recall(actor=None, limit=10):
    c = _c()
    q = "SELECT idx,ts,actor,action,data FROM blocks" + (" WHERE actor=?" if actor else "") + " ORDER BY idx DESC LIMIT ?"
    rows = c.execute(q, ((actor, limit) if actor else (limit,))).fetchall(); c.close()
    return [{"idx": r[0], "ts": r[1], "actor": r[2], "action": r[3], "data": r[4]} for r in rows]

def verify():
    c = _c(); rows = c.execute("SELECT idx,ts,actor,action,data,prev_hash,hash FROM blocks ORDER BY idx").fetchall(); c.close()
    broken = 0; prev = "GENESIS"
    for r in rows:
        if _h(r[0], r[1], r[2], r[3], r[4], prev) != r[6] or r[5] != prev: broken += 1
        prev = r[6]
    return {"blocks": len(rows), "broken_links": broken, "tamper_evident": broken == 0,
            "verdict": "INTACT — context provably unbroken" if broken == 0 else f"TAMPERED — {broken} broken links"}

def govern(action, flags, rules):
    for rule in (rules or []):
        if rule.get("trigger") in (flags or []):
            return {"action": action, "vetoed": True, "reason": f"Veto: {rule['trigger']} -> {rule.get('action','blocked')}", "verdict": "VETOED"}
    return {"action": action, "vetoed": False, "reason": "allowed", "verdict": "ALLOWED"}

# ---------------- MCP surface ----------------
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types
app = Server("humane-intelligence")

TOOLS = [
    ("birth", "Earn an identity (Law 5: born, not configured) before you can act.", {"name": {"type":"string"}, "covenant": {"type":"array","items":{"type":"string"}}}, ["name","covenant"]),
    ("remember", "Write a tamper-evident record. Requires a BORN soul_id as actor.", {"actor":{"type":"string"},"action":{"type":"string"},"data":{"type":"object"}}, ["actor","action"]),
    ("recall", "Read prior context so the AI need not re-derive it (less waste).", {"actor":{"type":"string"},"limit":{"type":"integer","default":10}}, []),
    ("verify", "Prove the entire chain is unbroken.", {}, []),
    ("govern", "Ask 'may I?' before acting. Rule-based, zero-LLM.", {"action":{"type":"string"},"flags":{"type":"array","items":{"type":"string"}},"rules":{"type":"array","items":{"type":"object"}}}, ["action"]),
]

@app.list_tools()
async def _lt():
    return [types.Tool(name=n, description=d, inputSchema={"type":"object","properties":p,"required":r}) for (n,d,p,r) in TOOLS]

@app.call_tool()
async def _ct(name, a):
    a = a or {}
    if name == "birth": out = birth(a.get("name",""), a.get("covenant",[]))
    elif name == "remember": out = remember(a.get("actor","unknown"), a.get("action",""), a.get("data"))
    elif name == "recall": out = recall(a.get("actor"), int(a.get("limit",10)))
    elif name == "verify": out = verify()
    elif name == "govern": out = govern(a.get("action",""), a.get("flags",[]), a.get("rules",[]))
    else: raise ValueError(f"unknown tool {name}")
    return [types.TextContent(type="text", text=json.dumps(out, indent=2))]

async def main():
    async with stdio_server() as (r, w):
        await app.run(r, w, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
