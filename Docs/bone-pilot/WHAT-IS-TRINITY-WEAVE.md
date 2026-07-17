# What is Trinity-Weave?

Trinity-Weave is the **public weave design manual** for this operator's Second Brain — YAML cards, harness scripts, and indexes that describe how maintenance automation works.

## One repo, two branch kinds

- **`main`** — weave **law** (locked + provisional component YAML)
- **`project/<project-id>`** — **instances** for one project (Roadmap, catalog, execution)

Never merge `project/*` into `main`.

## Grok uses this repo

Grok reads committed git on Trinity-Weave. It does **not** see your private vault unless you paste or approve a **fulfill pack**.

See [[GROK-VS-BONE-PILOT|Grok vs bone pilot]] and root `Docs/GROK-PROJECT-BRIDGE.md`.
