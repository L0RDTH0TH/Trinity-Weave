"""Rung 1 — auto-stamp conceptual immutability when factory feed gate passes."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .catalog_io import parse_state_frontmatter, user_story_paths
from .conceptual_track_ready import _read_note, iter_conceptual_roadmap_notes


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp_note_frozen(path: Path, *, frozen_at: str) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 4)
    if end < 0:
        return False
    fm = yaml.safe_load(text[4:end]) or {}
    if not isinstance(fm, dict):
        return False
    if fm.get("frozen") is True:
        return False
    fm["frozen"] = True
    fm.setdefault("roadmap_track", "conceptual")
    fm["conceptual_frozen_at"] = frozen_at
    body = text[end + 4 :].lstrip("\n")
    new_fm = yaml.dump(fm, sort_keys=False, allow_unicode=True).strip()
    path.write_text(f"---\n{new_fm}\n---\n\n{body}", encoding="utf-8")
    return True


def _update_roadmap_state_freeze(vault_root: Path, project_id: str, ts: str) -> bool:
    path = vault_root / "1-Projects" / project_id / "Roadmap" / "roadmap-state.md"
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 4)
    if end < 0:
        return False
    fm = yaml.safe_load(text[4:end]) or {}
    if not isinstance(fm, dict):
        return False
    changed = False
    if not fm.get("conceptual_frozen_at"):
        fm["conceptual_frozen_at"] = ts
        changed = True
    if str(fm.get("roadmap_track") or "conceptual").lower() != "execution":
        if fm.get("roadmap_track") != "conceptual":
            fm["roadmap_track"] = "conceptual"
            changed = True
    if not changed:
        return False
    body = text[end + 4 :].lstrip("\n")
    new_fm = yaml.dump(fm, sort_keys=False, allow_unicode=True).strip()
    path.write_text(f"---\n{new_fm}\n---\n\n{body}", encoding="utf-8")
    return True


def _update_user_story_mint_status(vault_root: Path, project_id: str, ts: str) -> bool:
    paths = user_story_paths(vault_root, project_id)
    path = paths["state"]
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 4)
    if end < 0:
        return False
    fm = yaml.safe_load(text[4:end]) or {}
    if not isinstance(fm, dict):
        return False
    if fm.get("mint_status") == "conceptual_frozen":
        return False
    fm["mint_status"] = "conceptual_frozen"
    fm["conceptual_frozen_at"] = ts
    fm.pop("conceptual_gate_policy", None)
    body = text[end + 4 :].lstrip("\n")
    new_fm = yaml.dump(fm, sort_keys=False, allow_unicode=True).strip()
    path.write_text(f"---\n{new_fm}\n---\n\n{body}", encoding="utf-8")
    return True


def stamp_factory_conceptual_freeze(
    vault_root: Path,
    project_id: str,
    *,
    gate_signature: str = "",
) -> dict[str, Any]:
    """
    Idempotent rung-1 freeze: user-story mint_status + conceptual note frozen stamps.

    Does not thaw; operator unfreeze_conceptual only.
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    ts = _utc_iso()
    notes_stamped = 0
    for path, fm, _body in iter_conceptual_roadmap_notes(vault_root, pid):
        if fm.get("frozen") is True:
            continue
        if _stamp_note_frozen(path, frozen_at=ts):
            notes_stamped += 1

    state_updated = _update_roadmap_state_freeze(vault_root, pid, ts)
    us_updated = _update_user_story_mint_status(vault_root, pid, ts)

    return {
        "ok": True,
        "project_id": pid,
        "conceptual_frozen_at": ts,
        "gate_signature": gate_signature,
        "notes_stamped": notes_stamped,
        "roadmap_state_updated": state_updated,
        "user_story_state_updated": us_updated,
        "idempotent_skip": notes_stamped == 0 and not state_updated and not us_updated,
    }
