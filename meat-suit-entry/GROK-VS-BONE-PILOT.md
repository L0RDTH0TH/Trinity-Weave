# Grok vs bone pilot (meat suit)

| | Grok | Meat suit / bone pilot |
|--|------|-------------------------|
| Sees | Committed Trinity-Weave **`main`** via GitHub connector (login only — **no branch config**) | Full vault + Cursor |
| Mint | `Docs/gmm-catalog-mint/` on `main` | Applies rows in vault, republishes pack |
| Custom instructions | Paste short body from `Docs/Grok-Second-Brain-Custom-Instructions.md` | Maintains that file |

## Connector honesty

Grok Connectors → GitHub = OAuth. There is **no UI** to “also attach `project/genesis-mythos-master`.”  
Project branches still exist for Cursor/export hygiene. **Mint dialogue for Grok is mirrored onto `main`** under `Docs/gmm-catalog-mint/`.

Do not instruct yourself to switch branches in Grok Chat.
