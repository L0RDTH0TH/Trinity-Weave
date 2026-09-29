"""Release plan — Loop 2 planner replacing slice-depth-budget.

Normative: Factory-Vocabulary + CDR release-plan-loop2-migration-2026-09-28.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .catalog_io import catalog_rows_by_id, load_yaml, parse_state_frontmatter, user_story_paths
from .depth_scope import scope_path
from .product_factory_state import load_product_factory

VALID_WAVES = ("alpha", "beta", "rc", "ga")
VALID_FIDELITY = ("stub", "playable", "polish")

FIDELITY_DEFS = {
    "stub": (
        "Structure and contracts present; happy path may be incomplete or mocked; "
        "not demoable as a real player/DM session beat."
    ),
    "playable": (
        "An operator (or playtest) can complete the package's named session beat(s) "
        "end-to-end without builder workarounds; failure modes are honest, not silent."
    ),
    "polish": (
        "Playable bar met plus UX/edge cases and presentation bar in the package "
        "exit_criteria (no known-broken-but-shippable escapes)."
    ),
}


@dataclass(frozen=True)
class PackageView:
    wave_id: str
    package_id: str
    catalog_row_ids: tuple[str, ...]
    fidelity: str
    exit_criteria: tuple[str, ...]
    status: str
    requires: dict[str, bool]

    def to_dict(self) -> dict[str, Any]:
        return {
            "wave_id": self.wave_id,
            "package_id": self.package_id,
            "catalog_row_ids": list(self.catalog_row_ids),
            "fidelity": self.fidelity,
            "exit_criteria": list(self.exit_criteria),
            "status": self.status,
            "requires": dict(self.requires),
        }


def release_plan_path(vault_root: Path, project_id: str) -> Path:
    paths = user_story_paths(vault_root, project_id)
    return paths["release_plan"]


def load_release_plan(vault_root: Path, project_id: str) -> dict[str, Any]:
    path = release_plan_path(vault_root, project_id)
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def save_release_plan(vault_root: Path, project_id: str, plan: dict[str, Any]) -> Path:
    path = release_plan_path(vault_root, project_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.dump(plan, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return path


def release_plan_feed_enabled(vault_root: Path, project_id: str) -> bool:
    """Default false until tests green and operator/config flips the flag."""
    pf = load_product_factory(vault_root, project_id)
    if "release_plan_feed" in pf:
        return bool(pf.get("release_plan_feed"))
    try:
        from ..factory.factory_output_gate import parse_factory_orchestrator_yaml

        cfg = parse_factory_orchestrator_yaml(vault_root / "3-Resources/Second-Brain-Config.md")
        fo = cfg.get("factory_orchestrator") if isinstance(cfg.get("factory_orchestrator"), dict) else {}
        if "release_plan_feed" in fo:
            return bool(fo.get("release_plan_feed"))
    except Exception:
        pass
    return False


def iter_packages(plan: dict[str, Any]) -> list[PackageView]:
    out: list[PackageView] = []
    for wave in plan.get("waves") or []:
        if not isinstance(wave, dict):
            continue
        wid = str(wave.get("id") or "")
        for pkg in wave.get("packages") or []:
            if not isinstance(pkg, dict):
                continue
            req = pkg.get("requires") if isinstance(pkg.get("requires"), dict) else {}
            rows = pkg.get("catalog_row_ids") or []
            if not isinstance(rows, list):
                rows = []
            criteria = pkg.get("exit_criteria") or []
            if not isinstance(criteria, list):
                criteria = []
            out.append(
                PackageView(
                    wave_id=wid,
                    package_id=str(pkg.get("id") or ""),
                    catalog_row_ids=tuple(str(r) for r in rows if r),
                    fidelity=str(pkg.get("fidelity") or ""),
                    exit_criteria=tuple(str(c) for c in criteria if c),
                    status=str(pkg.get("status") or "pending"),
                    requires={
                        "conceptual_pins": bool(req.get("conceptual_pins", True)),
                        "execution_pins": bool(req.get("execution_pins", True)),
                        "l5": bool(req.get("l5", True)),
                    },
                )
            )
    return out


def packages_for_wave(plan: dict[str, Any], wave_id: str) -> list[PackageView]:
    return [p for p in iter_packages(plan) if p.wave_id == wave_id]


def get_package(plan: dict[str, Any], wave_id: str, package_id: str) -> PackageView | None:
    for p in packages_for_wave(plan, wave_id):
        if p.package_id == package_id:
            return p
    return None


def validate_release_plan_schema(plan: dict[str, Any]) -> list[str]:
    """Structural validation — does not invent readiness."""
    errors: list[str] = []
    if not plan:
        return ["release_plan_missing"]
    if int(plan.get("schema_version") or 0) < 1:
        errors.append("schema_version_lt_1")
    active = str(plan.get("active_wave") or "")
    if active and active not in VALID_WAVES:
        errors.append(f"invalid_active_wave:{active}")
    waves = plan.get("waves")
    if not isinstance(waves, list) or not waves:
        errors.append("waves_empty")
        return errors
    seen_wave: set[str] = set()
    for wave in waves:
        if not isinstance(wave, dict):
            errors.append("wave_not_object")
            continue
        wid = str(wave.get("id") or "")
        if wid not in VALID_WAVES:
            errors.append(f"invalid_wave_id:{wid}")
        if wid in seen_wave:
            errors.append(f"duplicate_wave:{wid}")
        seen_wave.add(wid)
        pkgs = wave.get("packages") or []
        if not isinstance(pkgs, list) or not pkgs:
            errors.append(f"wave_no_packages:{wid}")
            continue
        seen_pkg: set[str] = set()
        for pkg in pkgs:
            if not isinstance(pkg, dict):
                errors.append(f"package_not_object:{wid}")
                continue
            pid = str(pkg.get("id") or "")
            if not pid:
                errors.append(f"package_missing_id:{wid}")
                continue
            if pid in seen_pkg:
                errors.append(f"duplicate_package:{wid}/{pid}")
            seen_pkg.add(pid)
            fid = str(pkg.get("fidelity") or "")
            if fid not in VALID_FIDELITY:
                errors.append(f"invalid_fidelity:{wid}/{pid}:{fid}")
            rows = pkg.get("catalog_row_ids") or []
            if not isinstance(rows, list) or not rows:
                errors.append(f"package_no_rows:{wid}/{pid}")
            criteria = pkg.get("exit_criteria") or []
            if not isinstance(criteria, list) or not criteria:
                errors.append(f"package_no_exit_criteria:{wid}/{pid}")
            status = str(pkg.get("status") or "pending")
            if status not in ("pending", "complete"):
                errors.append(f"invalid_package_status:{wid}/{pid}:{status}")
    if active and active not in seen_wave:
        errors.append(f"active_wave_not_in_waves:{active}")
    return errors


def package_row_readiness(
    vault_root: Path,
    project_id: str,
    pkg: PackageView,
    *,
    catalog_by_id: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    """Check L5 / conceptual pins for package rows when requires.* is true."""
    gaps: list[str] = []
    if catalog_by_id is None:
        catalog = load_yaml(user_story_paths(vault_root, project_id)["catalog"])
        catalog_by_id = catalog_rows_by_id(catalog)
    for rid in pkg.catalog_row_ids:
        row = catalog_by_id.get(rid) or {}
        if not row:
            gaps.append(f"unknown_row:{pkg.package_id}:{rid}")
            continue
        if pkg.requires.get("l5"):
            l5 = scope_path(vault_root, project_id, rid, 5)
            if not l5.is_file() or len(l5.read_text(encoding="utf-8", errors="replace").strip()) < 80:
                gaps.append(f"l5_missing:{pkg.package_id}:{rid}")
        if pkg.requires.get("conceptual_pins"):
            pin = str(row.get("conceptual_pin") or "").strip()
            waived = bool(row.get("pin_waived"))
            if not pin and not waived:
                gaps.append(f"conceptual_pin_missing:{pkg.package_id}:{rid}")
        if pkg.requires.get("execution_pins"):
            pins = row.get("execution_pins") or []
            if not isinstance(pins, list) or not pins:
                gaps.append(f"execution_pins_empty:{pkg.package_id}:{rid}")
    return gaps


def package_meets_exit(pkg: PackageView) -> tuple[bool, str]:
    """Weld receipt + exit_criteria presence + fidelity enum (operator attest via status)."""
    if pkg.status != "complete":
        return False, f"status_not_complete:{pkg.package_id}"
    if not pkg.exit_criteria:
        return False, f"exit_criteria_empty:{pkg.package_id}"
    if pkg.fidelity not in VALID_FIDELITY:
        return False, f"fidelity_invalid:{pkg.package_id}"
    return True, "ok"


def active_wave_complete(vault_root: Path, project_id: str) -> tuple[bool, str]:
    """True iff every package in active_wave meets exit_criteria and fidelity (via status complete).

    Partial waves do not count. Unfinished lane_batches are not modeled here —
    package status must not be marked complete until the package beat is honestly done.
    """
    plan = load_release_plan(vault_root, project_id)
    schema_errs = validate_release_plan_schema(plan)
    if schema_errs:
        return False, "schema:" + ";".join(schema_errs)
    active = str(plan.get("active_wave") or "")
    pkgs = packages_for_wave(plan, active)
    if not pkgs:
        return False, f"no_packages_in_active_wave:{active}"
    incomplete: list[str] = []
    for pkg in pkgs:
        ok, detail = package_meets_exit(pkg)
        if not ok:
            incomplete.append(detail)
    if incomplete:
        return False, "incomplete:" + ",".join(incomplete)
    return True, f"active_wave_complete:{active}"


def factory_wave_satisfied(vault_root: Path, project_id: str) -> tuple[bool, str]:
    """Alias for Half B overnight stop."""
    return active_wave_complete(vault_root, project_id)


def loop2_release_plan_checks(
    vault_root: Path,
    project_id: str,
    *,
    require_execution_pins: bool = False,
) -> list[tuple[str, bool, str]]:
    """Sub-checks for Operator Loop 2 under release_plan_feed."""
    plan = load_release_plan(vault_root, project_id)
    schema_errs = validate_release_plan_schema(plan)
    checks: list[tuple[str, bool, str]] = [
        (
            "release_plan_schema",
            not schema_errs,
            "ok" if not schema_errs else ";".join(schema_errs),
        ),
    ]
    paths = user_story_paths(vault_root, project_id)
    checks.append(
        (
            "catalog_exists",
            paths["catalog"].is_file(),
            "catalog_ok" if paths["catalog"].is_file() else "catalog_missing",
        )
    )
    if schema_errs:
        return checks

    catalog = load_yaml(paths["catalog"])
    catalog_by_id = catalog_rows_by_id(catalog)
    active = str(plan.get("active_wave") or "")
    pkgs = packages_for_wave(plan, active)
    all_gaps: list[str] = []
    for pkg in pkgs:
        soft = PackageView(
            wave_id=pkg.wave_id,
            package_id=pkg.package_id,
            catalog_row_ids=pkg.catalog_row_ids,
            fidelity=pkg.fidelity,
            exit_criteria=pkg.exit_criteria,
            status=pkg.status,
            requires={
                "conceptual_pins": pkg.requires.get("conceptual_pins", True),
                "execution_pins": require_execution_pins and pkg.requires.get("execution_pins", True),
                "l5": pkg.requires.get("l5", True),
            },
        )
        all_gaps.extend(
            package_row_readiness(vault_root, project_id, soft, catalog_by_id=catalog_by_id)
        )

    checks.append(
        (
            "active_wave_package_rows_ready",
            not all_gaps,
            "ok" if not all_gaps else ";".join(all_gaps),
        )
    )
    state = parse_state_frontmatter(paths["state"])
    signed = bool(state.get("catalog_signed_at") or state.get("release_plan_signed_at"))
    checks.append(
        (
            "release_plan_or_catalog_signed",
            signed,
            "signed" if signed else "awaiting_sign",
        )
    )
    return checks
