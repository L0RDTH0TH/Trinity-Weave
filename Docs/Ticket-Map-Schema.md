---
title: Ticket Map Schema
created: 2026-10-17
status: active
para-type: Resource
schema_version: 1
audience: factory_agents_operators
---

# Ticket Map Schema (vault-wide)

Binding until the next schema bump. Any Prefer / factory ticket map in the vault **must** conform. This is **not** project-specific — Genesis World-Builder is one consumer.

Picker + Gate A share this shape via `scripts/eat_queue_core/weave/factory/ticket_map_schema.py`.

## Map note frontmatter (required)

```yaml
ticket_map: true
map_id: <stable-slug>
title: <human title>
project-id: <owning-project-or-system>
map_status: active   # active | deferred | complete
created: YYYY-MM-DD
updated: YYYY-MM-DD  # bump on any ticket stamp / pointer change
# optional navigation aids:
active_recovery: <ticket_map_id>
active_recovery_slice: <slice_id>
```

| `map_status` | Picker |
|--------------|--------|
| `active` | Listed |
| `complete` | Listed (browse; tickets usually `f5_good`) |
| `deferred` | **Hidden** |

## Discovery

Markdown with `ticket_map: true` under `1-Projects/**` and `3-Resources/**`. Filename `*Ticket-Map*.md` is optional hint only.

## Ticket rows (canonical)

```markdown
| Ticket | Status | Product job | Notes |
|--------|--------|-------------|-------|
| `SOME-id` | `open` | Player-visible job… | Prefer / proofs |
```

| `ticket_status` | Meaning |
|-----------------|--------|
| `open` | Not F5-closed; Prefer-linked rows are **candidates** — launchable only after Gate B₁ |
| `f5_good` | F5 trail (primary greyed list — Prefer-linked history stays visible) |
| `deferred` | Parked / nursery; Prefer-linked only with `--all-tickets` |
| `superseded` | Hidden (unless `--all-tickets`) |

Legacy 3-column rows (`Ticket | job | notes`) still parse; status is inferred from Notes when Status column absent. **New writes must include Status.**

## Launchable = open + Gate B₁ (binding)

**Prefer + Gate A + B₁ = ticket** for FACTORY WELD launch purposes.

| Condition | Picker |
|-----------|--------|
| Map Status `open` **and** `slice-briefs/<slice_id>.prefer-result.json` has `map_fidelity_hostile_ok: true` | **Launchable** |
| Map Status `open` but prefer-result missing or `map_fidelity_hostile_ok` not exactly `true` | **Draft / B₁ pending** — omitted from default list; with `--all-tickets` shown disabled (`B₁ pending`) |
| Map Status `f5_good` Prefer-linked | Grey trail (browse only) |

Fail closed: missing prefer-result or any non-`true` stamp → not launchable.

Stamp path: Gate B₁ (`VALIDATE prefer_map_fidelity`) writes `map_fidelity_hostile_ok: true` into the prefer-result JSON next to the armed packet.

## Picker = map ∩ Prefer (binding)

**Prefer (`.armed.yaml` with `ticket_map_id`) joined to the map is the live row.** It is a **draft** until Gate B₁; only then is it a factory **ticket** for launch. The map is concordance (id, job, Status, order) + trail.

`scripts/factory_weld_launch_clip.py`:

1. Operator picks a **map** → scoped to that note’s `project-id`.
2. Scan `1-Projects/<project-id>/**/slice-briefs/*.armed.yaml`.
3. Join to map when either:
   - armed `ticket_map_id` matches a map row, or
   - map Notes/job wiki-links a slice that has `*.armed.yaml` (legacy Prefer without the field).
4. Load Gate B₁ from `<slice_id>.prefer-result.json` (`prefer_b1_ok`); default list **omits** open rows that fail B₁.
5. List in map order; `active_recovery` ★ first among launchable.
6. **`f5_good` Prefer-linked rows are the primary grey trail** (browse, not launch).
7. Multiple Prefer slices (r1/r2/…) on the **same** `ticket_map_id` → **multiple list rows** when each is B₁-ready (or under `--all-tickets`); launch still resolves that one id + chosen `slice_id`.
8. Naked map rows with no Prefer do **not** appear.

Labels are **id-first**, then `· slice_id ·` short prose.

## Stamp law (agents)

- Operator F5 pass on a ticket → set that row’s Status to `f5_good`; bump map `updated`.
- Defer a ticket → `deferred`; bump `updated`.
- Supersede → `superseded`.
- Map done → `map_status: complete` (map stays in picker).
- Map defer → `map_status: deferred` (map hidden).

## Prefer join

Under `1-Projects/<project-id>/Factory-DRB/slice-briefs/` (or any `slice-briefs` under that project), match `ticket_map_id` / `slice_id`. Ambiguous matches without slice hint: newest armed mtime; warn.

## Cross-links

- [[Prefer-Map-Fidelity-Automation-Plan]] · Gate A uses this parse
- Factory CLI: `scripts/factory_weld_launch_clip.py`
