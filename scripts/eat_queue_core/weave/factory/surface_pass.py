"""Surface seat — usability_pass (Tier B human gate). Not interpretation_pass."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .factory_drb_paths import drb_artifact_path, resolve_project_id
from .factory_little_val import FactoryLittleValResult
from .kinesthetic_probes import run_and_sync_probes, run_kinesthetic_probes
from .lane_charters import validate_six_lane_charters
from .operator_feedback import (
    DEFAULT_FEEDBACK_REL,
    KINESTHETIC_CHECKLIST_IDS,
    validate_kinesthetic_feedback,
)
from .product_kinesthetic_honesty import run_product_kinesthetic_honesty

USABILITY_NAV_DRG = "usability_nav"
USABILITY_LAUNCH_DRG = "usability_launch"
GATE_PRECEDENCE_DRG = "gate_precedence"
MANIFEST_KEY = "tech_stack_manifest"
CLOSED_ALPHA_KEY = "closed_alpha_release"


def _surface_drb_paths(vault_root: Path, project_id: str | None = None) -> dict[str, Path]:
    pid = resolve_project_id(vault_root, project_id)
    return {
        "nav": drb_artifact_path(vault_root, USABILITY_NAV_DRG, project_id=pid),
        "launch": drb_artifact_path(vault_root, USABILITY_LAUNCH_DRG, project_id=pid),
        "gate": drb_artifact_path(vault_root, GATE_PRECEDENCE_DRG, project_id=pid),
        "manifest": drb_artifact_path(vault_root, MANIFEST_KEY, project_id=pid),
        "closed_alpha": drb_artifact_path(vault_root, CLOSED_ALPHA_KEY, project_id=pid),
    }

# Re-export for callers — canonical list lives in operator_feedback.


@dataclass(frozen=True)
class SurfacePassResult:
    ok: bool
    little_val: FactoryLittleValResult
    detail: str
    checklist_coverage: dict[str, bool]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "detail": self.detail,
            "violations": list(self.little_val.anti_pattern_violations),
            "checklist_coverage": dict(self.checklist_coverage),
        }


def _read_manifest_flags(vault_root: Path, project_id: str | None = None) -> dict[str, Any]:
    paths = _surface_drb_paths(vault_root, project_id)
    path = paths["manifest"]
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def _extract_checklist_ids_from_drb(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    text = path.read_text(encoding="utf-8")
    m = re.search(r"```yaml\s+(.*?)```", text, re.DOTALL)
    if not m:
        return {cid for cid in KINESTHETIC_CHECKLIST_IDS if f"id: {cid}" in text or f"| `{cid}`" in text}
    block = yaml.safe_load(m.group(1))
    items: list[Any] = []
    if isinstance(block, dict) and isinstance(block.get("checklist"), list):
        items = block["checklist"]
    elif isinstance(block, list):
        items = block
    return {str(item["id"]) for item in items if isinstance(item, dict) and "id" in item}


def _violations_from_live_probes(
    vault_root: Path,
    *,
    run_smokes: bool = False,
    project_id: str | None = None,
    checklist_ids: tuple[str, ...] | None = None,
) -> list[str]:
    """Stage 2 (factory lane) — automatic structural/smoke probes only; ignores operator pass:false."""
    probes = run_kinesthetic_probes(
        vault_root,
        run_smokes=run_smokes,
        project_id=project_id,
        checklist_ids=checklist_ids,
    )
    out: list[str] = []
    for probe in probes:
        if probe.pass_:
            continue
        if probe.kinesthetic:
            out.append(f"kinesthetic_structural_fail:{probe.checklist_id}")
        else:
            out.append(f"checklist_structural_fail:{probe.checklist_id}")
    return out


def run_surface_pass(
    vault_root: Path,
    *,
    project_id: str | None = None,
    run_probes: bool = True,
    run_smokes: bool = False,
    gate_mode: str = "full",
    checklist_ids: tuple[str, ...] | None = None,
) -> SurfacePassResult:
    """
    Surface seat / usability_pass — Tier B human gate.

    gate_mode:
    - ``full`` (stage 3 / slice exit / CLI): operator kinesthetic rows must pass proof tiers.
    - ``lane_seat`` (stage 2 factory run): live structural probes only — never operator pass:false.
    """
    violations: list[str] = []
    lane_seat = str(gate_mode or "full").strip().lower() == "lane_seat"
    feedback_v: list[str] = []

    paths = _surface_drb_paths(vault_root, project_id)

    for key, path in (("nav", paths["nav"]), ("launch", paths["launch"]), ("gate", paths["gate"])):
        if not path.is_file():
            violations.append(f"missing_surface_drb:{path.relative_to(vault_root)}")

    violations.extend(validate_six_lane_charters(vault_root))

    nav_ids = _extract_checklist_ids_from_drb(paths["nav"])
    launch_ids = _extract_checklist_ids_from_drb(paths["launch"])
    declared = nav_ids | launch_ids
    if lane_seat and checklist_ids:
        coverage = {cid: cid in declared for cid in checklist_ids}
        for cid in checklist_ids:
            if cid not in declared:
                violations.append(f"checklist_id_not_in_drb:{cid}")
    elif not lane_seat:
        coverage = {cid: cid in declared for cid in KINESTHETIC_CHECKLIST_IDS}
        for cid in KINESTHETIC_CHECKLIST_IDS:
            if cid not in declared:
                violations.append(f"checklist_id_not_in_drb:{cid}")
    else:
        coverage = {}

    if lane_seat:
        if run_probes:
            run_and_sync_probes(
                vault_root,
                run_smokes=run_smokes,
                write_feedback=True,
                project_id=project_id,
            )
        violations.extend(
            _violations_from_live_probes(
                vault_root,
                run_smokes=run_smokes,
                project_id=project_id,
                checklist_ids=checklist_ids,
            )
        )
    else:
        if run_probes:
            run_and_sync_probes(
                vault_root,
                run_smokes=run_smokes,
                write_feedback=True,
                project_id=project_id,
            )
        feedback_v = validate_kinesthetic_feedback(
            vault_root,
            required_ids=KINESTHETIC_CHECKLIST_IDS,
        )
        violations.extend(feedback_v)

        pk = run_product_kinesthetic_honesty(vault_root, project_id=project_id)
        if not pk.ok:
            violations.extend(list(pk.violations))

    manifest = _read_manifest_flags(vault_root, project_id)
    alpha_vetted = bool(manifest.get("operator_closed_alpha_vetted"))
    factory_ship_valid = manifest.get("factory_ship_valid")

    if not lane_seat:
        if alpha_vetted and feedback_v:
            violations.append("premature_alpha_sign_without_surface_pass")

    if alpha_vetted and factory_ship_valid is True:
        violations.append("factory_ship_valid_true_while_surface_fail")
        violations.append("factory_ship_valid_true_while_surface_fail")

    if alpha_vetted and not (vault_root / DEFAULT_FEEDBACK_REL).is_file():
        violations.append("operator_closed_alpha_vetted_without_playtest_feedback_file")

    ok = len(violations) == 0
    lv = FactoryLittleValResult(
        little_val_ok=ok,
        anti_pattern_violations=violations,
        detail="surface_pass",
    )
    detail = "; ".join(violations) if violations else "surface_pass_ok"
    return SurfacePassResult(ok=ok, little_val=lv, detail=detail, checklist_coverage=coverage)


def run_usability_pass(vault_root: Path, *, gate_mode: str = "lane_seat") -> SurfacePassResult:
    """Alias — lane seats use structural-only; full surface is ``surface_pass`` at slice exit."""
    return run_surface_pass(vault_root, gate_mode=gate_mode)
