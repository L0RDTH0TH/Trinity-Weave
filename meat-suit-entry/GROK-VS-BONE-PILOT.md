# Grok vs bone pilot (meat suit)

| | Grok | Meat suit / bone pilot |
|--|------|-------------------------|
| Sees | Committed Trinity-Weave **`main`** via GitHub connector (login only — **no branch config**) | Full vault + Cursor |
| Mint | Card `weave/component-proposals/catalog_mint.yaml` + pack `Docs/catalog-mint/<project_id>/` | Applies rows in vault; `catalog_mint_pack_emit` republishes pack |
| Custom instructions | Paste short body from `Docs/Grok-Second-Brain-Custom-Instructions.md` | Maintains that file |

## Connector honesty

Grok Connectors → GitHub = OAuth. There is **no UI** to “also attach `project/<id>`.”  
Project branches still exist for Cursor/export hygiene. **Mint dialogue for Grok is card + pack on `main`.**

Do not instruct yourself to switch branches in Grok Chat.
