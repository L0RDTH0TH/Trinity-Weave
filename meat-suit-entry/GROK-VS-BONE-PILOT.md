# Grok vs bone pilot (meat suit)

| | Grok | Meat suit / bone pilot |
|--|------|-------------------------|
| Access | **Cannot** use private vault. Uses **Trinity-Weave** | Full vault + Cursor |
| **`main`** | **Trinity = the system** (mint law, pack walk queue) | Publishes via `weave_public_sync` |
| **`project/<id>`** | **Project being served** (PMG, Roadmap, grounding) | Publishes via `project_bridge_sync` / push |
| Mint | Operate in system (`main`); serve project branch | Applies rows; emit pack; sync both |
| Custom instructions | Paste [Grok-Second-Brain-Custom-Instructions.md](https://github.com/L0RDTH0TH/Trinity-Weave/blob/main/Docs/Grok-Second-Brain-Custom-Instructions.md) (two-pass mint) | Maintains that file + `weave_public_sync` |

Grok cannot read the vault. Stale system pack on `main` = publish with `weave_public_sync` — not “mint is main-only / project branch forbidden.”
