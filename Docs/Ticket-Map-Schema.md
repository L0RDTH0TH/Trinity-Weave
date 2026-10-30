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

## Active map socket (harness)

Gate A / `load_ticket_map_rows` resolve the map from the project — **not** a hardcoded product filename:

1. `1-Projects/<project-id>/Factory-DRB/factory-project.yaml` → `ticket_map_runtime.map_note` or `map_id`
2. Else sole active discovered map for that project
3. Else the active map that contains `ticket_map_id`

Harness: `resolve_active_ticket_map_rel` in `ticket_map_schema.py`.

## Ticket rows (canonical)

```markdown
| Ticket | Status | Product job | Notes | Observe |
|--------|--------|-------------|-------|---------|
| `SOME-id` | `open` | Capability this row adds… | Prefer / proofs | `person` |
```

| `Observe` | Meaning |
|-----------|---------|
| `person` | Someone does the act and can tell it happened. Prefer `proof_shape: moment`. |
| `record` | A file or return value is the whole claim. Prefer `proof_shape: contract`. |

`Observe` is human-authored. Ticketment / status stamp / Prefer emit **must not** rewrite it. Missing cell → Gate A fail closed.

| `ticket_status` | Meaning |
|-----------------|--------|
| `open` | Not F5-closed; Prefer-linked rows are **candidates** — launchable only after Gate B₁ |
| `f5_good` | F5 trail (primary greyed list — Prefer-linked history stays visible) |
| `deferred` | Parked / nursery; Prefer-linked only with `--all-tickets` |
| `superseded` | Hidden (unless `--all-tickets`) |

Legacy 3-column rows (`Ticket | job | notes`) still parse; status is inferred from Notes when Status column absent. **New writes must include Status.**

## Launchable = open + Gate A forms_ok + Gate B₁ (binding)

**Prefer + Gate A (`forms_ok`) + B₁ = ticket** for FACTORY WELD launch purposes.

| Condition | Picker |
|-----------|--------|
| Map Status `open` **and** Gate A `forms_ok` **and** prefer-result has Trinity-stored `map_fidelity_hostile` with `source: cursor_senior_b1`, `trinity_stamped: true`, `ok: true` | **Launchable** |
| Prefer `incomplete_missing_observer` (empty checks + named `missing_observer`) | **Incomplete** — not launchable; do not call B₁; factory `armed_slice_id` stays null |
| Map Status `open` but prefer-result missing, disk-shaped JSON without Trinity stamp, `harness_b1`, or bare author ok | **Draft / B₁ pending** — omitted from default list; with `--all-tickets` shown disabled (`B₁ pending`) |
| Map Status `f5_good` Prefer-linked | Grey trail (browse only) |

Fail closed: incomplete Prefer, missing prefer-result, or any non-`true` stamp → not launchable. `armed_slice_id` only after stored B₁ `ok: true` on a `forms_ok` Prefer.

Stamp path: factory-order only — `harness prefer_senior_gate --gate b1 --factory-order --armed …` (Trinity invokes senior, stamps source, stores from stdout). No chat `--write-b1`. Ticketment must not call the store. Incomplete packets never enter senior.

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
6. **`f5_good` Prefer-linked rows are the primary grey trail** (browse, not launch). One Prefer per ticket (latest F5/close). Trail order = **steps taken, newest first** (`operator_f5_at` / `completed_at` / `closed_at`), not map tip→tail grouping.
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
