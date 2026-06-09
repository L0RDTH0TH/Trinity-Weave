"""Load `gitforge` and `parallel_execution` from Second-Brain-Config.md fenced YAML blocks."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

_YAML_FENCE = re.compile(r"```yaml\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)


def merge_yaml_blocks_from_config(config_path: Path) -> dict[str, Any]:
    """Parse all ```yaml ... ``` blocks and merge top-level keys (later wins)."""
    if not config_path.is_file():
        return {}
    text = config_path.read_text(encoding="utf-8", errors="replace")
    merged: dict[str, Any] = {}
    for m in _YAML_FENCE.finditer(text):
        block = m.group(1).strip()
        if not block:
            continue
        try:
            import yaml  # type: ignore[import-untyped]

            data = yaml.safe_load(block)
        except ImportError:
            raise RuntimeError("PyYAML required for gitforge harness (pip install pyyaml)") from None
        if isinstance(data, dict):
            for k, v in data.items():
                merged[k] = v
    return merged


def get_gitforge_config(merged: dict[str, Any]) -> dict[str, Any]:
    raw = merged.get("gitforge")
    return raw if isinstance(raw, dict) else {}


def get_parallel_execution_config(merged: dict[str, Any]) -> dict[str, Any]:
    raw = merged.get("parallel_execution")
    return raw if isinstance(raw, dict) else {}


def lock_timeout_seconds(pe: dict[str, Any], gf: dict[str, Any]) -> int:
    inner = pe.get("gitforge") if isinstance(pe.get("gitforge"), dict) else {}
    v = inner.get("lock_timeout_seconds")
    if isinstance(v, int) and v > 0:
        return v
    v2 = gf.get("lock_timeout_seconds")
    if isinstance(v2, int) and v2 > 0:
        return v2
    return 30
