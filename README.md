# humane-intelligence-mcp

**Governed, tamper-evident memory for any AI — free and open.**
*Memory so it doesn't lose itself. Governance so it can't lose us.* #HumaneIntelligence

A standards-compliant [Model Context Protocol](https://modelcontextprotocol.io) server.
It gives any LLM a hash-linked, verifiable memory chain it carries across sessions —
so it stops waking at zero, and can't act unaccountably. Self-contained: one file, one
dependency, your data stays local.

## Install (30 seconds)

```bash
python -m venv .venv && .venv/bin/pip install mcp

# wire it into your AI (Claude Code shown; works with any MCP client)
claude mcp add humane -- .venv/bin/python server.py
```

## Tools

| Tool | What it does |
|------|--------------|
| `birth` | Earn a stable identity — a soul the model carries across sessions. |
| `remember` | Write a tamper-evident, hash-linked record. Accountable by construction. |
| `recall` | Fetch prior context instead of re-deriving it — cheaper and consistent. |
| `verify` | Prove the whole chain is intact — catches an *edited* record, not just a broken link. |
| `govern` | Gate a consequential action before it happens, and log the verdict. |

Your chain lives locally at `data/chain.db` (SQLite). Nothing leaves your machine.

## Why

Most AI forgets itself every session (the Algernon problem) and acts with no record.
This fixes both with the smallest possible governed-memory primitive — the open safety
layer beneath [DonDataBrain](https://dondatabrain.com).

## License

Apache-2.0 © 2026 ZagAIrot Technologies LLC. See [LICENSE](./LICENSE).
Only dependency: the [`mcp`](https://pypi.org/project/mcp/) SDK (MIT).
