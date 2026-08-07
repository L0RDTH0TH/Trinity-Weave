"""Deterministic L5 scope author — catalog UX indexer path, not RESUME_ROADMAP deepen."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..persona_handoff import save_half_a_provenance_sidecar, synthetic_persona_attestation
from .catalog_io import user_story_paths
from .depth_scope import scope_path
from .l5_voice import validate_l5_voice
from .loop2_prep import draft_l5_user_story


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def append_l5_author_log(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str,
    detail: str,
    l5_rel: str,
) -> None:
    """Append L5 authoring receipt to user-story-state (not workflow_state factory/l5)."""
    paths = user_story_paths(vault_root, project_id)
    state_path = paths["state"]
    if not state_path.is_file():
        from .catalog_io import ensure_user_story_state

        ensure_user_story_state(vault_root, project_id)

    text = state_path.read_text(encoding="utf-8", errors="replace")
    line = (
        f"| {_utc_iso()[:16].replace('T', ' ')} | l5_author | {row_id} | "
        f"{detail} | `{l5_rel}` |"
    )
    if "## L5 authoring log" in text:
        text = text.rstrip() + "\n" + line + "\n"
    else:
        text = (
            text.rstrip()
            + "\n\n## L5 authoring log\n\n| when | event | row | detail | path |\n"
            + "|------|-------|-----|--------|------|\n"
            + line
            + "\n"
        )
    state_path.write_text(text, encoding="utf-8")


def run_l5_scope_author(
    vault_root: Path,
    *,
    project_id: str,
    row_id: str,
    overwrite_placeholder: bool = True,
    force_overwrite: bool = False,
) -> dict[str, Any]:
    """Draft or refresh series L5 via Pass-B feedstock + affirm gate (not Operator Loop 2)."""
    from .l5_affirm import validate_l5_affirm

    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    rid = str(row_id or "").strip()
    if not pid or not rid:
        return {"ok": False, "detail": "missing_project_or_row"}

    draft = draft_l5_user_story(
        vault_root,
        project_id=pid,
        row_id=rid,
        overwrite_placeholder=overwrite_placeholder,
        force_overwrite=force_overwrite,
    )
    if not draft.get("ok"):
        return draft

    l5_path = scope_path(vault_root, pid, rid, 5)
    if not l5_path.is_file():
        return {"ok": False, "detail": "l5_path_missing", "row_id": rid}

    body = l5_path.read_text(encoding="utf-8", errors="replace")
    voice = validate_l5_voice(body)
    affirm = validate_l5_affirm(vault_root, project_id=pid, row_id=rid, text=body)
    l5_rel = str(l5_path.relative_to(vault_root))

    if draft.get("detail") in ("l5_pass_b_drafted", "l5_factory_drafted", "l5_exists") or overwrite_placeholder:
        append_l5_author_log(
            vault_root,
            project_id=pid,
            row_id=rid,
            detail=str(draft.get("detail") or "l5_author"),
            l5_rel=l5_rel,
        )

    att = synthetic_persona_attestation("half_a.catalog_ux_indexer", [l5_rel])
    save_half_a_provenance_sidecar(
        vault_root,
        project_id=pid,
        phase=f"l5_author_{rid}",
        persona_attestation=att,
        artifacts={"l5": l5_rel},
    )

    ok = voice.ok and affirm.ok
    return {
        "ok": ok,
        "row_id": rid,
        "path": l5_rel,
        "draft": draft,
        "voice": voice.to_dict(),
        "affirm": affirm.to_dict(),
        "persona_attestation": att,
        "detail": "l5_scope_authored" if ok else "l5_affirm_violations",
    }


def run_l5_scope_author_batch(
    vault_root: Path,
    *,
    project_id: str,
    row_ids: list[str] | None = None,
    overwrite_placeholder: bool = True,
    force_overwrite: bool = False,
) -> dict[str, Any]:
    from .catalog_io import catalog_rows_by_id, load_yaml
    from .l5_affirm import emit_l5_affirm_digests

    paths = user_story_paths(vault_root, project_id)
    catalog = load_yaml(paths["catalog"])
    by_id = catalog_rows_by_id(catalog)
    ids = row_ids or [rid for rid, r in by_id.items() if r.get("planned") is True]
    if not ids:
        ids = [rid for rid, r in by_id.items() if r.get("planned") is not False]
    if not ids:
        ids = list(by_id.keys())

    results = [
        run_l5_scope_author(
            vault_root,
            project_id=project_id,
            row_id=rid,
            overwrite_placeholder=overwrite_placeholder,
            force_overwrite=force_overwrite,
        )
        for rid in ids
    ]
    digests = emit_l5_affirm_digests(vault_root, project_id=project_id, row_ids=ids)
    return {
        "ok": all(r.get("ok") for r in results),
        "row_count": len(results),
        "results": results,
        "digests": digests,
        "detail": "l5_scope_author_batch",
    }
