"""Lightweight code-quality checks for weave paths (CQ L40–47, Wave 2+)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


MAX_FUNC_LINES = 80
MAX_FILE_LOC = 420


@dataclass(frozen=True)
class CodeQualityResult:
    ok: bool
    violations: tuple[str, ...]


def scan_weave_module(path: Path) -> CodeQualityResult:
    """Static scan one Python file under weave/ or lane_snapshot."""
    if not path.is_file():
        return CodeQualityResult(True, ())
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    violations: list[str] = []
    if len(lines) > MAX_FILE_LOC:
        violations.append(f"loc_cap:{path.name}:{len(lines)}>{MAX_FILE_LOC}")
    if 'eval(' in text or 'exec(' in text:
        violations.append(f"forbidden_pattern:eval_exec:{path.name}")
    if not text.strip().startswith('"""') and not text.strip().startswith("#"):
        violations.append(f"docstring_missing:{path.name}")
    return CodeQualityResult(len(violations) == 0, tuple(violations))


def friction_score(violation_count: int, module_count: int) -> float:
    if module_count <= 0:
        return 0.0
    return round(100.0 * violation_count / module_count, 2)
