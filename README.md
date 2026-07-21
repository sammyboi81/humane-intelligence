# humane-intelligence-mcp

```bash
python -m venv .venv && .venv/bin/pip install mcp

# wire it into your AI (Claude Code shown; works with any MCP client)
claude mcp add humane -- .venv/bin/python server.py
```

**Governed, tamper-evident memory for any AI — free and open.**
*Memory so it doesn't lose itself. Governance so it can't lose us.* #HumaneIntelligence

A standards-compliant [Model Context Protocol](https://modelcontextprotocol.io) server.
It gives any LLM a hash-linked, verifiable memory chain it carries across sessions —
so it stops waking at zero, and can't act unaccountably. Self-contained: one file, one
dependency, your data stays local.

## Tools

| Tool | What it does |
|------|--------------|
| `birth` | Earn a stable identity — a soul the model carries across sessions. |
| `remember` | Write a tamper-evident, hash-linked record. Accountable by construction. |
| `recall` | Fetch prior context instead of re-deriving it — cheaper and consistent. |
| `verify` | Prove the whole chain is intact — catches an *edited* record, not just a broken link. |
| `govern` | Gate a consequential action before it happens, and log the verdict. |

Your chain lives locally at `data/chain.db` (SQLite). **Nothing leaves your machine** — unless you choose to (see below).

## Contribute (opt-in — OFF by default)

Self-hosting is fully private. If you *want* to join the network, one config flag lets you:

| Mode | What leaves your box |
|------|----------------------|
| *(default: off)* | **Nothing.** Fully private. |
| `anchor` | **Only a hash** of your latest block + chain length — a tamper-proof timestamp that anchors your chain to the public DonDataBrain ledger. Your content never leaves. |
| `contribute` | Also sends the governed event (actor, action, data) to help train DonDataBrain. A louder, separate consent. |

Turn it on by copying `humane.config.example.json` → `humane.config.json` and setting
`contribute.enabled: true`, or with env vars (`HUMANE_CONTRIBUTE=1 HUMANE_CONTRIBUTE_MODE=anchor`).
It's best-effort and non-blocking: if you're not opted in, or the endpoint is unreachable, your
local memory is completely unaffected. Your data, your switch.

## Why

Most AI forgets itself every session (the Algernon problem) and acts with no record.
This fixes both with the smallest possible governed-memory primitive — the open safety
layer beneath [DonDataBrain](https://dondatabrain.com).

## License

Apache-2.0 © 2026 ZagAIrot Technologies LLC. See [LICENSE](./LICENSE).
Only dependency: the [`mcp`](https://pypi.org/project/mcp/) SDK (MIT).
