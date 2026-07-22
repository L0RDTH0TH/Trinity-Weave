"""Playtest-Brief — operator morning handoff after factory slice lane work."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .factory_orchestrator import DEFAULT_QUEUE_REL, load_alpha_queue
from .operator_feedback import DEFAULT_FEEDBACK_REL, KINESTHETIC_CHECKLIST_IDS, load_operator_feedback

BRIEF_DIR_REL = "1-Projects/genesis-mythos-master/Factory-DRB/operator-feedback/playtest-briefs"
GAME_CHECKLIST_REL = ".technical/weave/kinesthetic_checklist.yaml"
MANIFEST_REL = "1-Projects/genesis-mythos-master/Factory-DRB/Tech-Stack-Manifest-v1.yaml"


@dataclass(frozen=True)
class PlaytestBriefResult:
    ok: bool
    path: str
    slice_id: str
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "path": self.path,
            "slice_id": self.slice_id,
            "detail": self.detail,
        }


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _game_repo_rel(vault_root: Path) -> str:
    manifest = vault_root / MANIFEST_REL
    rel = "5-Attachments/Code-Repos/genesis-mythos-alpha"
    if manifest.is_file():
        data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        if isinstance(data, dict) and data.get("game_repo_path"):
            rel = str(data["game_repo_path"])
    return rel.strip("/")


def _load_checklist_items(vault_root: Path) -> list[dict[str, Any]]:
    repo = vault_root / _game_repo_rel(vault_root)
    path = repo / GAME_CHECKLIST_REL
    if path.is_file():
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        items = data.get("checklist") if isinstance(data, dict) else None
        if isinstance(items, list):
            return [x for x in items if isinstance(x, dict) and x.get("id")]

    return [{"id": cid, "kinesthetic": True, "hypothesis": ""} for cid in KINESTHETIC_CHECKLIST_IDS]


def _slice_record(vault_root: Path, slice_id: str, queue_rel: str) -> dict[str, Any]:
    queue = load_alpha_queue(vault_root, queue_rel)
    for sl in queue.get("slices") or []:
        if isinstance(sl, dict) and str(sl.get("id") or "") == slice_id:
            return sl
    return {}


def write_playtest_brief(
    vault_root: Path,
    *,
    slice_id: str,
    queue_lane: str = "godot",
    slice_exit_gates_pass: bool = False,
    slice_exit_gate_summary: dict[str, Any] | None = None,
    receipt_id: str | None = None,
    queue_rel: str = DEFAULT_QUEUE_REL,
) -> PlaytestBriefResult:
    """
    Emit operator Playtest-Brief after PM pass and slice exit gates (vault feed).

    Runs from `implementation_cell_tail` (production SLICE_PRODUCER_REVIEW path) or
    `factory_lane_runner` when `skip_pm_agent` completes inline. Includes red exit gates
    so the operator knows what to playtest next.
    """
    vault_root = vault_root.resolve()
    sl = _slice_record(vault_root, slice_id, queue_rel)
    if not sl:
        return PlaytestBriefResult(False, "", slice_id, "slice_not_found")

    game_repo = _game_repo_rel(vault_root)
    checklist = _load_checklist_items(vault_root)
    kinesthetic_items = [c for c in checklist if c.get("kinesthetic", True)]
    feedback_rows = load_operator_feedback(vault_root, DEFAULT_FEEDBACK_REL)
    by_id = {r.checklist_id: r for r in feedback_rows}

    stamp = _utc_stamp()
    out_dir = vault_root / BRIEF_DIR_REL
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"playtest-brief-{slice_id}-{stamp}.md"

    drb_refs = sl.get("drb_refs") or []
    if not drb_refs:
        repo_checklist = vault_root / game_repo / GAME_CHECKLIST_REL
        if repo_checklist.is_file():
            raw = yaml.safe_load(repo_checklist.read_text(encoding="utf-8")) or {}
            if isinstance(raw, dict):
                drb_refs = list(raw.get("drb_refs") or [])

    gate_lines: list[str] = []
    if slice_exit_gate_summary:
        for name, info in slice_exit_gate_summary.items():
            if isinstance(info, dict):
                gate_lines.append(f"- `{name}`: {'pass' if info.get('ok') else 'FAIL'} — {info.get('detail', '')}")

    pending: list[str] = []
    for item in kinesthetic_items:
        cid = str(item.get("id") or "")
        row = by_id.get(cid)
        if row is None or not row.decided or row.pass_ is not True:
            hyp = str(item.get("hypothesis") or "")
            pending.append(f"- [ ] **`{cid}`** — {hyp}")

    body = f"""---
title: Playtest-Brief — {slice_id}
slice_id: {slice_id}
release_slice: {sl.get('release_slice', '')}
queue_lane: {queue_lane}
created: {stamp}
slice_exit_gates_pass: {str(slice_exit_gates_pass).lower()}
receipt_id: {receipt_id or ''}
game_repo: {game_repo}
---

# Playtest-Brief — {slice_id}

Factory slice **lane work is complete**. Human playtest is the next step before slice exit gates can green.

## Operator session (run in order)

**In-game HUD (when `GMM_PLAYTEST=1` or `GMM_PLAYTEST_CAPTURE=1`):** U=pass · I=fail+note · N=note · J/K=prev/next · S=skip

**Editor MCP assist (optional while playing):** Cursor `get_runtime_log` reads `playtest|mark|...` lines — Godot never spawns Cursor.

```bash
# 1 — Play with capture (from game repo)
cd {game_repo}
GMM_PLAYTEST=1 ./scripts/run-f6-playtest.sh
# or legacy: GMM_PLAYTEST_CAPTURE=1 ./scripts/run-f6-playtest.sh

# 2 — Ingest session → operator_feedback suggestions (from vault root)
cd /path/to/Second-Brain
./scripts/run-operator-playtest-session.sh

# Optional MCP tail after session (editor was connected during play)
./scripts/playtest-mcp-assist.sh

# 3 — Review suggestions, then confirm rows you accept
PYTHONPATH=scripts python3 -m eat_queue_core.weave.factory.cli operator-confirm --vault-root . --list
PYTHONPATH=scripts python3 -m eat_queue_core.weave.factory.cli operator-confirm --vault-root . --checklist-id Flow_Launch --pass true --confirm
```

## Slice exit gate status

**Slice exit gates pass:** `{slice_exit_gates_pass}`

{chr(10).join(gate_lines) if gate_lines else '- (exit gates not evaluated yet)'}

## Kinesthetic checklist — test these

{chr(10).join(pending) if pending else '- All kinesthetic rows decided — run surface-pass to verify'}

## DRB references

{chr(10).join(f'- [[{ref}]]' for ref in drb_refs) if drb_refs else '- See usability-navigation-v1 / usability-launch-v1'}

## Factory notes

- `playtest_trace` and `playtest_operator_mark` rows require **`operator_confirmed: true`** before ship.
- Explicit **operator marks** (HUD U/I/N/S) override passive `window_pass` heuristics on ingest.
- Overnight factory **does not** block on missing F6 session.
- Re-run lane jobs or surface-pass only after you confirm feedback rows.
"""

    out_path.write_text(body, encoding="utf-8")
    latest = out_dir / "latest.md"
    latest.write_text(body, encoding="utf-8")

    rel = str(out_path.relative_to(vault_root))
    parts = rel.split("/")
    project_id = parts[1] if len(parts) > 1 and parts[0] == "1-Projects" else ""
    if project_id:
        from ..user_story.implementation_artifact_ledger import record_implementation_artifact

        record_implementation_artifact(
            vault_root,
            project_id,
            artifact_path=rel,
            event_type="playtest_brief",
            slice_id=slice_id,
        )

    return PlaytestBriefResult(True, rel, slice_id, "playtest_brief_written")
