"""Export checkout session state for safe branch switch + crash heal."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def session_path(vault_root: Path) -> Path:
    return vault_root / ".technical/grok-bridge/export-session.json"


def read_session(vault_root: Path) -> dict[str, Any] | None:
    path = session_path(vault_root)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except (OSError, ValueError):
        return None


def write_session(vault_root: Path, payload: dict[str, Any]) -> None:
    path = session_path(vault_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def clear_session(vault_root: Path) -> None:
    path = session_path(vault_root)
    if path.is_file():
        try:
            path.unlink()
        except OSError:
            pass
