"""Run touch.behavior_signals pytest/unittest proofs for Trinity external leg (Wave 2.5e)."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .trinity_card import contract_proof_paths, get_touch, touch_behavior_signals


@dataclass(frozen=True)
class BehaviorProofResult:
    test_name: str
    ok: bool
    target: str | None = None
    detail: str = ""

    def to_dict(self) -> dict[str, str | bool | None]:
        return {
            "test_name": self.test_name,
            "ok": self.ok,
            "target": self.target,
            "detail": self.detail,
        }


def _module_dotted(vault_root: Path, py_path: Path) -> str:
    scripts = (vault_root / "scripts").resolve()
    rel = py_path.resolve().relative_to(scripts)
    return ".".join(rel.with_suffix("").parts)


def _proof_search_paths(vault_root: Path, card: dict[str, Any]) -> list[Path]:
    touch = get_touch(card)
    seen: set[str] = set()
    out: list[Path] = []
    for raw in list(contract_proof_paths(card)) + list(touch.get("primary_paths") or []):
        rel = str(raw).strip()
        if not rel or rel in seen:
            continue
        seen.add(rel)
        p = vault_root / rel
        if p.is_file() and p.suffix == ".py":
            out.append(p)
        elif p.is_dir():
            out.extend(sorted(p.glob("test_*.py")))
            out.extend(sorted(p.glob("**/test_*.py")))
        else:
            parent = p.parent
            tests_dir = vault_root / "scripts/eat_queue_core/tests"
            if tests_dir.is_dir():
                out.append(tests_dir)
    if not out:
        tests_dir = vault_root / "scripts/eat_queue_core/tests"
        if tests_dir.is_dir():
            out.append(tests_dir)
    else:
        tests_dir = vault_root / "scripts/eat_queue_core/tests"
        if tests_dir.is_dir() and tests_dir not in out:
            out.append(tests_dir)
    return out


def find_test_file_for_signal(
    vault_root: Path, card: dict[str, Any], test_name: str
) -> Path | None:
    """Return the proof file containing ``def test_name`` if any."""
    if not test_name.startswith("test_"):
        return None
    for base in _proof_search_paths(vault_root, card):
        if base.is_file():
            files = [base]
        else:
            files = sorted(base.glob("test_*.py"))
        for py_path in files:
            try:
                text = py_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if re.search(rf"^\s*def {re.escape(test_name)}\s*\(", text, re.MULTILINE):
                return py_path
    return None


def _is_pytest_style(py_path: Path) -> bool:
    try:
        head = py_path.read_text(encoding="utf-8", errors="replace")[:12000]
    except OSError:
        return False
    return (
        "import pytest" in head
        or "@pytest.fixture" in head
        or "@pytest.mark" in head
    )


def find_unittest_target(vault_root: Path, card: dict[str, Any], test_name: str) -> str | None:
    """Resolve ``eat_queue_core.tests....TestClass.test_name`` for a behavior_signal."""
    if not test_name.startswith("test_"):
        return None
    for base in _proof_search_paths(vault_root, card):
        if base.is_file():
            files = [base]
        else:
            files = sorted(base.glob("test_*.py"))
        for py_path in files:
            try:
                lines = py_path.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            current_class: str | None = None
            found = False
            for line in lines:
                cls_m = re.match(r"^class\s+(\w+)\s*\(", line)
                if cls_m:
                    current_class = cls_m.group(1)
                    continue
                if re.match(rf"^\s*def {re.escape(test_name)}\s*\(", line):
                    found = True
                    break
            if not found:
                continue
            mod = _module_dotted(vault_root, py_path)
            if current_class:
                return f"{mod}.{current_class}.{test_name}"
            return f"{mod}.{test_name}"
    return None


def _run_subprocess_proof(
    cmd: list[str],
    *,
    vault_root: Path,
    test_name: str,
    target: str,
    timeout_seconds: float,
) -> BehaviorProofResult:
    env = os.environ.copy()
    env["PYTHONPATH"] = str((vault_root / "scripts").resolve())
    env.setdefault("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "1")
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(vault_root.resolve()),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return BehaviorProofResult(
            test_name=test_name,
            ok=False,
            target=target,
            detail=f"timeout after {timeout_seconds}s",
        )
    except OSError as e:
        return BehaviorProofResult(
            test_name=test_name,
            ok=False,
            target=target,
            detail=str(e),
        )
    if proc.returncode == 0:
        return BehaviorProofResult(test_name=test_name, ok=True, target=target)
    err = (proc.stderr or proc.stdout or "").strip()
    if len(err) > 400:
        err = err[:397] + "..."
    return BehaviorProofResult(
        test_name=test_name,
        ok=False,
        target=target,
        detail=err or f"exit {proc.returncode}",
    )


def run_behavior_proof(
    vault_root: Path,
    card: dict[str, Any],
    test_name: str,
    *,
    timeout_seconds: float = 120.0,
) -> BehaviorProofResult:
    py_file = find_test_file_for_signal(vault_root, card, test_name)
    if py_file and _is_pytest_style(py_file):
        rel = py_file.resolve().relative_to(vault_root.resolve()).as_posix()
        target = f"pytest:{rel}::{test_name}"
        return _run_subprocess_proof(
            [
                sys.executable,
                "-m",
                "pytest",
                str(py_file),
                "-k",
                test_name,
                "-q",
                "--tb=short",
                "--no-header",
            ],
            vault_root=vault_root,
            test_name=test_name,
            target=target,
            timeout_seconds=timeout_seconds,
        )

    target = find_unittest_target(vault_root, card, test_name)
    if not target:
        return BehaviorProofResult(
            test_name=test_name,
            ok=False,
            target=None,
            detail="behavior_signal test not found under contract.proof / primary_paths",
        )
    return _run_subprocess_proof(
        [sys.executable, "-m", "unittest", target],
        vault_root=vault_root,
        test_name=test_name,
        target=target,
        timeout_seconds=timeout_seconds,
    )


def run_card_behavior_proofs(
    vault_root: Path,
    card: dict[str, Any],
    *,
    timeout_seconds: float = 120.0,
) -> list[BehaviorProofResult]:
    results: list[BehaviorProofResult] = []
    for name in touch_behavior_signals(card):
        if not name.startswith("test_"):
            continue
        results.append(
            run_behavior_proof(
                vault_root,
                card,
                name,
                timeout_seconds=timeout_seconds,
            )
        )
    return results
