"""Load locked harness_runtime_contract meta and parity-check harness subcommands."""

from __future__ import annotations

import io
import re
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .trinity_card import get_conceptual, get_touch
from .trinity_card_paths import load_trinity_card

CONTRACT_ID = "harness_runtime_contract"

REQUIRED_HARNESS_SUBCOMMANDS: tuple[str, ...] = (
    "headless_eat",
    "headless_overnight",
    "roadmap_factory_eat",
    "trinity_integration_vet",
    "trinity_weave_self_wrap",
    "full_cycle",
)


@dataclass(frozen=True)
class RuntimeContract:
    trinity_id: str
    outcome: str | None
    summary: str | None
    forbidden: tuple[str, ...] = ()
    primary_paths: tuple[str, ...] = ()
    source: str = "locked"

    def to_dict(self) -> dict[str, Any]:
        return {
            "trinity_id": self.trinity_id,
            "outcome": self.outcome,
            "summary": self.summary,
            "forbidden": list(self.forbidden),
            "primary_paths": list(self.primary_paths),
            "source": self.source,
        }


def load_runtime_contract(vault_root: Path) -> RuntimeContract:
    vault_root = vault_root.resolve()
    try:
        card = load_trinity_card(vault_root, CONTRACT_ID, prefer="locked")
    except (OSError, ValueError, FileNotFoundError):
        return RuntimeContract(
            trinity_id=CONTRACT_ID,
            outcome=None,
            summary=None,
            source="missing",
        )
    con = get_conceptual(card)
    rules = card.get("rules") if isinstance(card.get("rules"), dict) else {}
    touch = get_touch(card)
    forbidden_raw = rules.get("forbidden") or []
    forbidden = [str(x).strip() for x in forbidden_raw if str(x).strip()] if isinstance(forbidden_raw, list) else []
    paths_raw = touch.get("primary_paths") or []
    paths = [str(x).strip() for x in paths_raw if str(x).strip()] if isinstance(paths_raw, list) else []
    return RuntimeContract(
        trinity_id=CONTRACT_ID,
        outcome=str(con.get("outcome") or "") or None,
        summary=str(con.get("summary") or "") or None,
        forbidden=tuple(forbidden),
        primary_paths=tuple(paths),
        source="locked",
    )


def _harness_subcommand_names(vault_root: Path) -> set[str]:
    harness_py = vault_root / "scripts" / "eat_queue_core" / "harness.py"
    if not harness_py.is_file():
        return set()
    text = harness_py.read_text(encoding="utf-8", errors="replace")
    pattern = r'sub\.add_parser\(\s*["\']([^"\']+)["\']'
    return {m.group(1) for m in re.finditer(pattern, text)}


def run_runtime_contract_parity(vault_root: Path) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    contract = load_runtime_contract(vault_root)
    found = _harness_subcommand_names(vault_root)
    missing = [c for c in REQUIRED_HARNESS_SUBCOMMANDS if c not in found]
    headless_py = vault_root / "scripts" / "eat_queue_core" / "headless_orchestrator.py"
    wired_rf = headless_py.is_file() and "run_layer1_roadmap_factory_pass" in headless_py.read_text(encoding="utf-8")
    ok = contract.source == "locked" and not missing and wired_rf
    return {
        "ok": ok,
        "contract": contract.to_dict(),
        "harness_subcommands_found": len(found),
        "missing_required": missing,
        "headless_eat_wires_roadmap_factory": wired_rf,
    }


def run_operator_path_conduct(vault_root: Path) -> dict[str, Any]:
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName("eat_queue_core.tests.test_product_factory_operator_path")
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)
    return {
        "ok": result.wasSuccessful(),
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
    }
