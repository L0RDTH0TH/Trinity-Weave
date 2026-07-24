"""Reset factory User-Story artifacts for fresh_greenfield overnight runs."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .catalog_io import user_story_paths


def reset_greenfield_factory_artifacts(vault_root: Path, project_id: str) -> dict[str, Any]:
    """
    Clear loop-2 factory surface so a greenfield packet cannot inherit stale conductor state.

    Does not remove ROADMAP/ tree or PMG — only User-Story + operator-feedback stubs.
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        return {"ok": False, "detail": "no_project_id"}

    paths = user_story_paths(vault_root, pid)
    removed: list[str] = []

    for key in ("catalog", "budget", "state"):
        p = paths.get(key)
        if p and p.is_file():
            p.unlink()
            removed.append(str(p.relative_to(vault_root)))

    backlog = paths["catalog"].parent / "MINT-BACKLOG.yaml"
    if backlog.is_file():
        backlog.unlink()
        removed.append(str(backlog.relative_to(vault_root)))

    scopes = paths.get("scopes_dir")
    if scopes and scopes.is_dir():
        shutil.rmtree(scopes)
        removed.append(str(scopes.relative_to(vault_root)))

    feedback = (
        vault_root
        / "1-Projects"
        / pid
        / "Factory-DRB"
        / "operator-feedback"
        / "user-story-operator-feedback.yaml"
    )
    if feedback.is_file():
        feedback.unlink()
        removed.append(str(feedback.relative_to(vault_root)))

    return {"ok": True, "detail": "greenfield_factory_reset", "removed": removed}
