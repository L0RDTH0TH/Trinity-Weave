"""module_fit_pass lint — host touch budget + Core zone discipline."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .factory_little_val import FactoryLittleValResult
from .lane_charters import load_lane_charter

GOD_AUTOLOAD_FORBIDDEN = re.compile(
    r"class\s+\w+\s*:\s*Node\s*\{[^}]*static\s+\w+\s+\w+",
    re.MULTILINE | re.DOTALL,
)


@dataclass(frozen=True)
class ModuleFitResult:
    ok: bool
    little_val: FactoryLittleValResult
    detail: str
    core_touch_lines: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "detail": self.detail,
            "core_touch_lines": self.core_touch_lines,
            "violations": list(self.little_val.anti_pattern_violations),
        }


def _charter_raw(vault_root: Path, lane_id: str) -> dict[str, Any]:
    ch = load_lane_charter(vault_root, lane_id)
    if ch is None:
        return {}
    raw = yaml.safe_load(ch.path.read_text(encoding="utf-8")) or {}
    return raw if isinstance(raw, dict) else {}


def count_core_touches(game_repo: Path, changed_paths: tuple[str, ...]) -> int:
    total = 0
    for rel in changed_paths:
        if not rel.startswith("Core/"):
            continue
        fp = game_repo / rel
        if fp.is_file():
            total += sum(1 for _ in fp.open(encoding="utf-8", errors="replace"))
    return total


def run_module_fit_pass(
    vault_root: Path,
    *,
    lane_id: str,
    game_repo_rel: str,
    changed_paths: tuple[str, ...] | None = None,
) -> ModuleFitResult:
    vault_root = vault_root.resolve()
    violations: list[str] = []
    fields = _charter_raw(vault_root, lane_id)
    budget = int(fields.get("host_touch_budget") or fields.get("max_core_touch_lines_per_slice") or 500)
    repo = vault_root / game_repo_rel.strip("/")

    if changed_paths is None:
        changed_paths = tuple(
            str(p.relative_to(repo)).replace("\\", "/")
            for p in repo.glob("Core/**/*.cs")
            if p.is_file()
        )[:20]

    touches = count_core_touches(repo, changed_paths)
    if touches > budget:
        violations.append(f"host_touch_budget_exceeded:{touches}>{budget}")

    for rel in changed_paths:
        fp = repo / rel
        if not fp.is_file() or not rel.endswith(".cs"):
            continue
        text = fp.read_text(encoding="utf-8", errors="replace")
        if GOD_AUTOLOAD_FORBIDDEN.search(text):
            violations.append(f"god_autoload_pattern:{rel}")

    host_ref = str(fields.get("host_contract_ref") or "")
    if host_ref and not (vault_root / host_ref).is_file():
        violations.append("missing_host_contract_ref")

    ok = len(violations) == 0
    lv = FactoryLittleValResult(ok, violations, "module_fit_pass")
    detail = "; ".join(violations) if violations else "module_fit_pass_ok"
    return ModuleFitResult(ok, lv, detail, core_touch_lines=touches)
