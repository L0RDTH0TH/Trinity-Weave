"""Review Seat implementations — factory honesty welds (Exhibit A catalog)."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .drop_contract_base import DROP_CONTRACTS, load_drop_manifest, validate_drop_manifest
from .factory_little_val import FactoryLittleValResult
from .review_pass_runner import ReviewPassResult


@dataclass(frozen=True)
class SeatContext:
    game_repo_rel: str = ""
    lane_id: str | None = None
    job: dict[str, Any] | None = None
    changed_paths: tuple[str, ...] | None = None


def _lv(ok: bool, violations: list[str], detail: str) -> FactoryLittleValResult:
    return FactoryLittleValResult(little_val_ok=ok, anti_pattern_violations=violations, detail=detail)


def _seat(name: str, ok: bool, violations: list[str], detail: str) -> ReviewPassResult:
    return ReviewPassResult(name, ok, _lv(ok, violations, detail), detail)


def _repo(vault_root: Path, rel: str) -> Path:
    return vault_root / rel.strip("/")


def run_compliance_pass(vault_root: Path, *, game_repo_rel: str = "", lane_id: str | None = None, **_: Any) -> ReviewPassResult:
    violations: list[str] = []
    if not game_repo_rel:
        return _seat("compliance_pass", False, ["missing_game_repo"], "missing_game_repo")
    repo = _repo(vault_root, game_repo_rel)
    for ctype in DROP_CONTRACTS:
        data = load_drop_manifest(repo, ctype)
        if not data:
            continue
        violations.extend(f"{ctype}:{v}" for v in validate_drop_manifest(data, contract_type=ctype))
        for row in data.get("drops") or []:
            if not isinstance(row, dict):
                continue
            if not row.get("license_spdx"):
                violations.append(f"missing_license:{row.get('drop_id')}")
            if not row.get("receipt_id") and not row.get("generated_by_receipt_id"):
                violations.append(f"missing_receipt:{row.get('drop_id')}")
    ok = not violations
    return _seat("compliance_pass", ok, violations, "; ".join(violations) or "compliance_pass_ok")


def run_canon_pass(vault_root: Path, *, game_repo_rel: str = "", **_: Any) -> ReviewPassResult:
    violations: list[str] = []
    if not game_repo_rel:
        return _seat("canon_pass", False, ["missing_game_repo"], "missing_game_repo")
    canon = _repo(vault_root, game_repo_rel) / "content/_factory/canon-index.yaml"
    cdc = load_drop_manifest(_repo(vault_root, game_repo_rel), "cdc")
    if not canon.is_file():
        violations.append("missing_canon_index")
    if not (cdc.get("drops") or []):
        violations.append("cdc_empty_for_canon_pass")
    ok = not violations
    return _seat("canon_pass", ok, violations, "; ".join(violations) or "canon_pass_ok")


def run_art_direction_pass(vault_root: Path, *, game_repo_rel: str = "", **_: Any) -> ReviewPassResult:
    violations: list[str] = []
    vsc = vault_root / "1-Projects/genesis-mythos-master/Factory-DRB/Visual-Style-Charter-v1.md"
    if not vsc.is_file():
        violations.append("missing_visual_style_charter")
    if game_repo_rel:
        repo = _repo(vault_root, game_repo_rel)
        if (repo / "Main.tscn").is_file():
            violations.append("q3_acceptance_remnant_on_main")
    ok = not violations
    return _seat("art_direction_pass", ok, violations, "; ".join(violations) or "art_direction_pass_ok")


def run_integration_pass(vault_root: Path, *, game_repo_rel: str = "", **_: Any) -> ReviewPassResult:
    violations: list[str] = []
    if not game_repo_rel:
        return _seat("integration_pass", False, ["missing_game_repo"], "missing_game_repo")
    repo = _repo(vault_root, game_repo_rel)
    if not (repo / "project.godot").is_file():
        violations.append("missing:project.godot")
    csprojs = list(repo.glob("*.csproj"))
    if not csprojs:
        violations.append("missing:csproj")
    else:
        dotnet = os.environ.get("DOTNET_ROOT", str(Path.home() / ".dotnet"))
        dotnet_bin = Path(dotnet) / "dotnet" if Path(dotnet).is_dir() else Path("dotnet")
        try:
            r = subprocess.run(
                [str(dotnet_bin), "build", str(csprojs[0])],
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=180,
            )
            if r.returncode != 0:
                violations.append("dotnet_build_fail")
        except (subprocess.TimeoutExpired, OSError) as e:
            violations.append(f"dotnet_build_error:{e}")
    ok = not violations
    return _seat("integration_pass", ok, violations, "; ".join(violations) or "integration_pass_ok")


def run_reliability_pass(vault_root: Path, *, game_repo_rel: str = "", **_: Any) -> ReviewPassResult:
    violations: list[str] = []
    if game_repo_rel:
        repo = _repo(vault_root, game_repo_rel)
        if not (repo / "Systems").is_dir() and not (repo / "Core").is_dir():
            violations.append("missing_systems_or_core")
    ok = not violations
    return _seat("reliability_pass", ok, violations, "; ".join(violations) or "reliability_pass_ok")


TAGGED_STUB_SEATS = frozenset({"perf_pass", "balance_pass", "juice_pass"})


def _tagged_stub_seat(name: str, vault_root: Path, *, job: dict[str, Any] | None = None, **_: Any) -> ReviewPassResult:
    tagged = set((job or {}).get("review_passes") or [])
    if name not in tagged:
        return _seat(name, True, [], f"{name}_skipped_not_tagged")
    return _seat(name, True, [], f"{name}_tagged_stub_alpha")


def run_perf_pass(vault_root: Path, *, job: dict[str, Any] | None = None, **kw: Any) -> ReviewPassResult:
    return _tagged_stub_seat("perf_pass", vault_root, job=job, **kw)


def run_balance_pass(vault_root: Path, *, job: dict[str, Any] | None = None, **kw: Any) -> ReviewPassResult:
    return _tagged_stub_seat("balance_pass", vault_root, job=job, **kw)


def run_juice_pass(vault_root: Path, *, job: dict[str, Any] | None = None, **kw: Any) -> ReviewPassResult:
    return _tagged_stub_seat("juice_pass", vault_root, job=job, **kw)


def run_observability_pass(
    vault_root: Path,
    *,
    game_repo_rel: str = "",
    job: dict[str, Any] | None = None,
    changed_paths: tuple[str, ...] | None = None,
    **_: Any,
) -> ReviewPassResult:
    tagged = set((job or {}).get("review_passes") or [])
    if "observability_pass" not in tagged:
        return _seat("observability_pass", True, [], "observability_pass_skipped_not_tagged")
    violations: list[str] = []
    if not game_repo_rel:
        return _seat("observability_pass", False, ["missing_game_repo"], "missing_game_repo")
    repo = _repo(vault_root, game_repo_rel)
    for rel in ("Core/ClosedAlpha/AlphaFactoryLog.cs", "Core/ClosedAlpha/PlaytestLog.cs"):
        if not (repo / rel).is_file():
            violations.append(f"missing:{rel}")
    if changed_paths:
        for rel in changed_paths:
            if not rel.endswith(".cs"):
                continue
            if not rel.startswith(("Core/", "Systems/", "UI/")):
                continue
            full = repo / rel
            if not full.is_file():
                continue
            text = full.read_text(encoding="utf-8", errors="replace")
            if "GD.Print(" in text and "AlphaFactoryLog" not in text and "PlaytestLog" not in text:
                violations.append(f"console_only_logging:{rel}")
    ok = not violations
    return _seat("observability_pass", ok, violations, "; ".join(violations) or "observability_pass_ok")


def run_extensibility_pass(vault_root: Path, *, game_repo_rel: str = "", **_: Any) -> ReviewPassResult:
    violations: list[str] = []
    if game_repo_rel:
        repo = _repo(vault_root, game_repo_rel)
        spine = vault_root / "1-Projects/genesis-mythos-master/Factory-DRB/Spine-Host-Contract-v0.md"
        if not spine.is_file():
            violations.append("missing_spine_host_contract")
        if not (repo / "Core").is_dir():
            violations.append("missing_core_for_extensibility")
    ok = not violations
    return _seat("extensibility_pass", ok, violations, "; ".join(violations) or "extensibility_pass_ok")


def run_narrative_audio_pass(vault_root: Path, *, game_repo_rel: str = "", **_: Any) -> ReviewPassResult:
    violations: list[str] = []
    if game_repo_rel:
        audc = load_drop_manifest(_repo(vault_root, game_repo_rel), "audc")
        if not (audc.get("drops") or []):
            violations.append("audc_empty")
    ok = not violations
    return _seat("narrative_audio_pass", ok, violations, "; ".join(violations) or "narrative_audio_pass_ok")


def run_interconnect_pass(vault_root: Path, **_: Any) -> ReviewPassResult:
    from .interop_pass import run_interop_pass

    interop = run_interop_pass(vault_root)
    return ReviewPassResult("interconnect_pass", interop.ok, interop.little_val, interop.detail)


def run_stack_integrate_pass_seat(vault_root: Path, *, dry_run: bool | None = None, **_: Any) -> ReviewPassResult:
    from .stack_integrate import run_stack_integrate_pass

    if dry_run is None:
        dry_run = False
    r = run_stack_integrate_pass(vault_root, dry_run=dry_run)
    return ReviewPassResult("stack_integrate_pass", r.ok, r.little_val, r.detail)


def run_product_kinesthetic_honesty_seat(vault_root: Path, **_: Any) -> ReviewPassResult:
    from .product_kinesthetic_honesty import run_product_kinesthetic_honesty

    r = run_product_kinesthetic_honesty(vault_root)
    lv = _lv(r.ok, list(r.violations), r.detail)
    return ReviewPassResult("product_kinesthetic_honesty", r.ok, lv, r.detail)
