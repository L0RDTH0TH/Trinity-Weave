"""Structural honesty check for factory harness steps."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class FactoryLittleValResult:
    little_val_ok: bool
    anti_pattern_violations: list[str] = field(default_factory=list)
    run_id: str = ""
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "little_val_ok": self.little_val_ok,
            "anti_pattern_violations": list(self.anti_pattern_violations),
            "run_id": self.run_id,
            "detail": self.detail,
        }


def check_integrate_receipt(receipt: dict[str, Any]) -> FactoryLittleValResult:
    violations: list[str] = []
    if not receipt.get("manifest_row_id"):
        violations.append("missing_receipt:manifest_row_id")
    if not receipt.get("game_repo_path"):
        violations.append("missing_receipt:game_repo_path")
    if receipt.get("status") != "integrated":
        violations.append("integrate_status_not_green")
    ok = len(violations) == 0
    return FactoryLittleValResult(
        little_val_ok=ok,
        anti_pattern_violations=violations,
        run_id=str(receipt.get("run_id", "")),
        detail="integrate receipt check",
    )


def check_spine_socket(game_repo: Path, wrap_policy: str) -> FactoryLittleValResult:
    violations: list[str] = []
    if wrap_policy == "ICameraRig":
        iface = game_repo / "Core" / "ICameraRig.cs"
        if not iface.is_file():
            violations.append("missing_spine_socket:ICameraRig")
        main_cs = game_repo / "Main.cs"
        if main_cs.is_file():
            text = main_cs.read_text(encoding="utf-8", errors="replace")
            if "DMCameraRig" in text and "ICameraRig" not in text:
                violations.append("unwelded_vendor:DMCameraRig_in_Main_without_ICameraRig")
    ok = len(violations) == 0
    return FactoryLittleValResult(
        little_val_ok=ok,
        anti_pattern_violations=violations,
        detail=f"spine socket check for {wrap_policy}",
    )


def merge_results(*results: FactoryLittleValResult) -> FactoryLittleValResult:
    violations: list[str] = []
    run_id = ""
    for r in results:
        violations.extend(r.anti_pattern_violations)
        if r.run_id:
            run_id = r.run_id
    ok = len(violations) == 0
    return FactoryLittleValResult(
        little_val_ok=ok,
        anti_pattern_violations=violations,
        run_id=run_id,
        detail="merged factory little_val",
    )
