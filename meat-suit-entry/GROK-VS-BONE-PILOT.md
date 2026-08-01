# Grok vs bone pilot (meat suit)

| | Grok | Meat suit / bone pilot |
|--|------|-------------------------|
| Access | **Cannot** use private vault. Uses **Trinity-Weave** | Full vault + Cursor |
| **`main`** | **Trinity = the system** (mint law, pack walk queue) | Publishes via `weave_public_sync` |
| **`project/<id>`** | **Project being served** (PMG, Roadmap, grounding) | Publishes via `project_bridge_sync` / push |
| Mint | Operate in system (`main`); serve project branch | Applies rows; emit pack; sync both |
| Custom instructions | Paste from GitHub: [Docs/Grok-Second-Brain-Custom-Instructions.md](https://github.com/L0RDTH0TH/Trinity-Weave/blob/main/Docs/Grok-Second-Brain-Custom-Instructions.md) (also linked from [`GROK-START-HERE.md`](https://github.com/L0RDTH0TH/Trinity-Weave/blob/main/GROK-START-HERE.md)) | Maintains vault copy → `weave_public_sync` |

**Two-pass mint:** series walk → Trinity publish gate → children validate (Cursor drafts). See custom instructions + pack `MINT-PACK.md` Walk Order.

Grok cannot read the vault. Stale system pack on `main` = publish with `weave_public_sync` — not “mint is main-only / project branch forbidden.”
