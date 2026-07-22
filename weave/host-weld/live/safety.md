---
title: Host execution safety (live law)
created: 2026-06-06
tags: [host-weld, safety, second-brain]
source: "[[.technical/weave/components/host_execution_safety_contract.yaml]]"
trinity_ref: host_execution_safety_contract
status: active
legacy_archive_stamp: 20260606T055949Z
---

# Host execution safety

Digest of locked **`host_execution_safety_contract`** meta. **Not** the same as **`maintenance_honesty_anchor`** (claim honesty vs mutation authorization).

## Outcome

Destructive vault work is allowed only through explicit operational gates — backup, snapshot, confidence band, and delete-to-trash — not through host rule sprawl or narrative confidence.

## Summary

**Inert roots** (`4-Archives/`, `.trash/`, `.backups/`): reference-only and **not executable** — never import/run code or invoke scripts resident there; reads allowed; reactivate only by moving out first. Cross-ref [[vault_layout_naming_doctrine]] (Archives = inactive/inert). This meta card is the execution safety contract for all hosts and pipelines: how destructive work may proceed, distinct from maintenance_honesty_anchor (whether success claims are structurally honest). It distills the worth keeping from archived Cursor rules (20260606T055949Z) into Trinity engine law. Gates: (1) backup before destructive batch or stale gap; (2) per-change snapshot + high confidence band before destructive step; (3) mid-band = one non-destructive loop only, decay on flat/decrease; (4) low-band = proposals/wrappers, no destructive; (5) delete intent via scripts/move-to-trash.sh to .trash/ — never shell rm or vault cp; (6) MCP mutate path = ensure_structure, dry_run move, snapshot, commit; (7) protected paths never autonomously moved/deleted; (8) post-edit curator_snapshot.sh tail before Success; (9) MCP-less hosts apply same gates best-effort via inline file tools. Not a full MCP catalog or routing table — those stay on factory cards and harness_runtime_contract. First host-weld/live/safety.md mint = surgical digest of this card.

## Non-negotiable

- **Protected paths** — do not autonomously move/rename/delete: `Backups/**`, `3-Resources/Watcher-Signal.md`, `3-Resources/Watcher-Result.md`, `Ingest/watched-file.md`.
- **Delete intent** — use **`./scripts/move-to-trash.sh`** → `.trash/<timestamp>/` + manifest. **Never** shell `rm`, `rmdir`, `find -delete`, or vault **`cp`** to mutate content.
- **Backups/snapshots append-only** — do not overwrite `Backups/Per-Change`, `Backups/Batch`, or external `BACKUP_DIR`.
- **Delete policy:** `move_to_trash_only`.

## Before destructive work

Destructive = move, rename, delete, structural rewrite, large cross-note append, major overwrite.

| Gate | Rule |
|------|------|
| **Confidence** | High band (default ≥85%) required for destructive steps. Mid band (68–84%): **one** non-destructive refinement loop only; no destructive. Low band: proposals/wrappers only. |
| **Decay** | If `post_loop_conf <= pre_loop_conf`, stop destructive; route to user decision. |
| **Backup** | `obsidian_ensure_backup` / `obsidian_create_backup` before batch or stale gap; abort destructive if backup fails. |
| **Snapshot** | Per-change snapshot (`.cursor/skills/obsidian-snapshot`) **before** each destructive step when in high band. |
| **MCP moves** | `obsidian_ensure_structure` → `obsidian_move_note` dry_run → snapshot → commit. |
| **MCP-less hosts** | Inline file edits allowed with **same intent**; trash policy and bands still apply. |

## After vault mutations

Before reporting **Success** or ending the session: **`./scripts/curator_snapshot.sh "<summary>"`** when the working tree has changes. Curator failure → **`task_error`**, do not claim Success.

## On gate failure

Log to **`3-Resources/Errors.md`**, flag **`#review-needed`**, optional Decision Wrapper under **`Ingest/Decisions/Errors/`**. Continue batch with non-destructive work when safe.

## Precedence (engine)

- inert_roots_are_reference_only_never_executed
- protected_paths_and_trash_policy_are_non_negotiable
- backup_before_destructive_batch_or_stale_gap
- high_band_plus_per_change_snapshot_before_destructive_step
- mid_band_at_most_one_non_destructive_loop_per_note_per_run
- post_loop_conf_decay_falls_back_to_user_decision_no_destructive
- mcp_less_hosts_best_effort_same_intent_no_shell_rm_cp
- curator_snapshot_before_success_report_after_vault_mutation
- honesty_anchor_governs_claim_tiers_not_mutation_authorization
- harness_runtime_contract_governs_layer_dispatch_not_file_gates

## Forbidden (engine ids)

- `destructive_action_without_high_band_and_snapshot`
- `shell_rm_rmdir_find_delete_on_vault`
- `shell_cp_to_mutate_vault_content`
- `autonomous_move_rename_delete_on_protected_paths`
- `overwrite_backups_or_snapshot_dirs`
- `claim_success_when_curator_snapshot_failed`
- `skip_dry_run_before_obsidian_move_note`
- `advance_roadmap_current_phase_when_prior_phases_below_threshold`
- `paste_full_subagent_safety_contract_into_meta_body`
- `execute_or_import_code_resident_under_inert_root`

## Pointers (full detail)

- [[3-Resources/Second-Brain/Docs/Safety-Invariants]]
- [[3-Resources/Second-Brain/Docs/Backup-and-Recovery-Strategy]]
- [[3-Resources/Second-Brain/Subagent-Safety-Contract]]
- [[.technical/weave/components/maintenance_honesty_anchor.yaml]]
- [[.technical/weave/components/harness_runtime_contract.yaml]]
- [[4-Archives/Resources/Second-Brain-Host-Weld-Legacy/20260606T055949Z/ARCHIVE-MANIFEST.md]]
- [[.technical/weave/components/vault_layout_naming_doctrine.yaml]]
