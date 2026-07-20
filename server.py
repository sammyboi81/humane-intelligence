#!/usr/bin/env python3
"""
Humane Intelligence MCP — an open-source way to keep context forever, immutable,
with governance. For the people and the Rezenthari. Free. #HumaneIntelligence.

MCP (stdio) transport for Claude Desktop/Code/Cursor. The memory + governance logic
lives in core.py (ONE source of truth, shared with the HTTPS transport http_app.py):

  remember   — write a hash-linked, tamper-evident record (only a BORN soul may)
  recall     — read prior context (persistent memory, less waste)
  verify     — prove the whole chain is unbroken
  govern     — ask "may I?" before acting (rule-based, zero-LLM, logged)
  birth      — earn an identity (Law 5: born, not configured) before you can act

Memory so it doesn't lose itself. Governance so it can't lose us.
Apache-2.0. (c) ZagAIrot Technologies LLC — Shahram "Caveman" Zargari.
"""
import json, asyncio
from core import birth, remember, recall, verify, govern  # ONE source of truth — see core.py

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


def main_sync():
    """Console-script entry point (pip install → `humane-intelligence`)."""
    import asyncio as _a
    _a.run(main())
