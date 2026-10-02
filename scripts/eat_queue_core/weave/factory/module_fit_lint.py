"""module_fit_pass lint — host touch budget + Core zone discipline.

Budget measures **changed/diff lines** (honest delta), not whole-file sums.
host_touch_budget is a shell-era accounting seat — it cannot alone block-or-pass
Prefer product seats (prefer_authorship_pass dominates disposition).
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .factory_little_val import FactoryLittleValResult
from .lane_charters import load_lane_charter
from .prefer_authorship_contract import slice_requires_prefer_authorship

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
    budget_exceeded: bool = False
    budget_is_advisory_only: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "detail": self.detail,
            "core_touch_lines": self.core_touch_lines,
            "budget_exceeded": self.budget_exceeded,
            "budget_is_advisory_only": self.budget_is_advisory_only,
            "violations": list(self.little_val.anti_pattern_violations),
        }


def _charter_raw(vault_root: Path, lane_id: str) -> dict[str, Any]:
    ch = load_lane_charter(vault_root, lane_id)
    if ch is None:
        return {}
    raw = yaml.safe_load(ch.path.read_text(encoding="utf-8")) or {}
    return raw if isinstance(raw, dict) else {}


def count_file_diff_lines(game_repo: Path, rel: str) -> int:
    """Honest delta: git numstat insert+delete, or full line count for untracked new files."""
    fp = game_repo / rel
    if not fp.is_file():
        return 0
    repo = game_repo.resolve()
    if (repo / ".git").is_dir():
        try:
            r = subprocess.run(
                ["git", "diff", "--numstat", "HEAD", "--", rel],
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if r.returncode == 0 and r.stdout.strip():
                # numstat: inserted\tdeleted\tpath
                parts = r.stdout.strip().splitlines()[0].split("\t")
                if len(parts) >= 2:
                    ins = int(parts[0]) if parts[0].isdigit() else 0
                    dele = int(parts[1]) if parts[1].isdigit() else 0
                    return ins + dele
            # Untracked / new file
            r2 = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard", "--", rel],
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=15,
            )
            if r2.returncode == 0 and r2.stdout.strip():
                return sum(1 for _ in fp.open(encoding="utf-8", errors="replace"))
            # Tracked but unchanged vs HEAD → 0 diff lines (honest)
            r3 = subprocess.run(
                ["git", "ls-files", "--", rel],
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=15,
            )
            if r3.returncode == 0 and r3.stdout.strip():
                return 0
        except (subprocess.TimeoutExpired, OSError, ValueError):
            pass
    # No git — fall back to file length only for explicitly listed changed paths
    # (caller already scoped the change set). Still prefer not to invent huge budgets.
    return sum(1 for _ in fp.open(encoding="utf-8", errors="replace"))


def count_core_touches(game_repo: Path, changed_paths: tuple[str, ...]) -> int:
    """Sum **diff** lines under Core/ for the change set (not whole-file sums)."""
    total = 0
    for rel in changed_paths:
        if not rel.startswith("Core/"):
            continue
        total += count_file_diff_lines(game_repo, rel)
    return total


# Backward-compatible alias — old name counted whole files; now diffs.
count_core_touch_lines = count_core_touches


def run_module_fit_pass(
    vault_root: Path,
    *,
    lane_id: str,
    game_repo_rel: str,
    changed_paths: tuple[str, ...] | None = None,
    job: dict[str, Any] | None = None,
) -> ModuleFitResult:
    vault_root = vault_root.resolve()
    violations: list[str] = []
    fields = _charter_raw(vault_root, lane_id)
    job = job if isinstance(job, dict) else {}
    # Prefer overlay / PQ may raise budget for thin Prefer welds that touch Core/WorldGen.
    budget = int(
        job.get("host_touch_budget")
        or fields.get("host_touch_budget")
        or fields.get("max_core_touch_lines_per_slice")
        or 500
    )
    waive_shell = bool(job.get("waive_shell_era_seats"))
    prefer_product = slice_requires_prefer_authorship(str(job.get("slice_id") or ""), job)
    # When Prefer product seats apply, budget alone is advisory — never sole pass/fail.
    budget_advisory = prefer_product or bool(job.get("prefer_proof") or job.get("thin_prefer"))
    repo = vault_root / game_repo_rel.strip("/")

    if changed_paths is None:
        # Fail-closed without a change set: do not count the whole Core tree as this slice.
        changed_paths = ()

    touches = count_core_touches(repo, changed_paths)
    budget_exceeded = touches > budget
    if budget_exceeded:
        if waive_shell or budget_advisory:
            # Shell-era accounting seat — Prefer overlays may waive / treat advisory.
            # Never let budget alone block-or-pass Prefer product seats.
            pass
        else:
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
    if budget_exceeded and budget_advisory and ok:
        detail = f"module_fit_pass_ok;budget_advisory_exceeded:{touches}>{budget}"
    return ModuleFitResult(
        ok,
        lv,
        detail,
        core_touch_lines=touches,
        budget_exceeded=budget_exceeded,
        budget_is_advisory_only=budget_advisory,
    )
