"""Review passes for pipeline proof and stack baseline vetting."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .factory_little_val import FactoryLittleValResult, merge_results
from .interop_pass import run_interop_pass
from .stack_integrate import run_stack_integrate_pass
from .tech_stack_manifest import ROW_KINDS_SKELETON, check_honesty_invariants, load_manifest, validate_manifest_schema
from .structure_lint import run_structure_pass
from .surface_pass import run_surface_pass
from .module_fit_lint import run_module_fit_pass
from .interpretation_pass import run_interpretation_pass
from .factory_output_gate import run_factory_output_gate


@dataclass(frozen=True)
class ReviewPassResult:
    pass_name: str
    ok: bool
    little_val: FactoryLittleValResult
    detail: str


def run_pipeline_proof_pass(vault_root: Path) -> ReviewPassResult:
    manifest = load_manifest(vault_root)
    violations: list[str] = []

    if not manifest.pipeline_certified:
        violations.append("pipeline_not_certified")

    violations.extend(check_honesty_invariants(manifest))
    violations.extend(validate_manifest_schema(manifest, vault_root))

    integrate = run_stack_integrate_pass(vault_root, dry_run=True)
    engine_rec = next(
        (r for r in integrate.receipts if r.get("manifest_row_id") == "engine-godot-463-dotnet"),
        None,
    )
    if not engine_rec or engine_rec.get("status") != "integrated":
        violations.append("engine_not_integrated")

    engine = manifest.row_by_id("engine-godot-463-dotnet")
    if not engine or not engine.operational_confirmed:
        violations.append("engine_not_operational")

    ok = len(violations) == 0
    lv = FactoryLittleValResult(
        little_val_ok=ok,
        anti_pattern_violations=violations,
        detail="pipeline_proof_pass",
    )
    return ReviewPassResult("pipeline_proof_pass", ok, lv, "; ".join(violations) or "ok")


def run_stack_operational_pass(vault_root: Path) -> ReviewPassResult:
    manifest = load_manifest(vault_root)
    game_repo = vault_root / manifest.game_repo_path
    violations: list[str] = []

    if not (game_repo / "project.godot").is_file():
        violations.append("missing:project.godot")
    if not list(game_repo.glob("*.csproj")):
        violations.append("missing:csproj")

    ci = game_repo / ".github/workflows/godot-ci.yml"
    if ci.is_file():
        text = ci.read_text(encoding="utf-8", errors="replace")
        if "continue-on-error: true" in text:
            violations.append("ci_continue_on_error_not_baseline")
    else:
        violations.append("missing:godot-ci.yml")

    for row in manifest.baseline_required_rows():
        if row.row_kind in ROW_KINDS_SKELETON and row.operational_confirmed:
            violations.append(f"skeleton_marked_operational:{row.id}")

    lv = FactoryLittleValResult(
        little_val_ok=len(violations) == 0,
        anti_pattern_violations=violations,
        detail="stack_operational_pass",
    )
    return ReviewPassResult("stack_operational_pass", lv.little_val_ok, lv, "; ".join(violations) or "ok")


def run_interconnect_pass_minimal(vault_root: Path) -> ReviewPassResult:
    """Legacy alias — delegates to interop_pass."""
    interop = run_interop_pass(vault_root)
    return ReviewPassResult(
        "interconnect_pass_minimal",
        interop.ok,
        interop.little_val,
        interop.detail,
    )


def run_release_readiness_pass(vault_root: Path) -> ReviewPassResult:
    manifest = load_manifest(vault_root)
    if not manifest.operator_stack_baseline_vetted:
        lv = FactoryLittleValResult(
            little_val_ok=False,
            anti_pattern_violations=["operator_stack_baseline_not_vetted"],
            detail="release_readiness_pass",
        )
        return ReviewPassResult("release_readiness_pass", False, lv, "operator_stack_baseline_vetted is false")

    integrate = run_stack_integrate_pass(vault_root, dry_run=True)
    operational = run_stack_operational_pass(vault_root)
    interop = run_interop_pass(vault_root)
    merged = merge_results(integrate.little_val, operational.little_val, interop.little_val)

    pending = [
        r.id
        for r in manifest.baseline_required_rows()
        if not r.operational_confirmed or r.row_kind in ROW_KINDS_SKELETON
    ]
    if pending:
        merged.anti_pattern_violations.append(f"baseline_rows_pending:{pending}")

    ok = merged.little_val_ok and not pending
    merged.little_val_ok = ok
    return ReviewPassResult("release_readiness_pass", ok, merged, merged.detail)


def run_all_baseline_passes(vault_root: Path) -> dict[str, Any]:
    interop = run_interop_pass(vault_root)
    results = {
        "pipeline_proof_pass": run_pipeline_proof_pass(vault_root),
        "stack_integrate_pass": run_stack_integrate_pass(vault_root, dry_run=True),
        "interop_pass": ReviewPassResult("interop_pass", interop.ok, interop.little_val, interop.detail),
        "stack_operational_pass": run_stack_operational_pass(vault_root),
        "release_readiness_pass": run_release_readiness_pass(vault_root),
    }
    all_ok = all(r.ok for r in results.values())
    return {"all_ok": all_ok, "passes": results}


def run_all_r1_passes(vault_root: Path) -> dict[str, Any]:
    """Backward-compatible alias."""
    return run_all_baseline_passes(vault_root)


def _import_review_seats():
    from . import review_seats

    return review_seats


TAGGED_STUB_SEATS = frozenset({"perf_pass", "balance_pass", "juice_pass", "observability_pass"})


def _surface_pass_runner(vault_root: Path, *, gate_mode: str, **kw: Any) -> Any:
    run_probes = kw.get("run_probes")
    if run_probes is None:
        run_probes = gate_mode == "lane_seat"
    job = kw.get("job") if isinstance(kw.get("job"), dict) else {}
    params = job.get("params") if isinstance(job.get("params"), dict) else {}
    raw_ids = params.get("checklist_ids") or job.get("checklist_ids") or []
    checklist_ids = tuple(str(x) for x in raw_ids if x) or None
    return run_surface_pass(
        vault_root,
        run_probes=bool(run_probes),
        run_smokes=bool(kw.get("run_smokes", False)),
        gate_mode=gate_mode,
        checklist_ids=checklist_ids,
    )


PASS_RUNNERS: dict[str, Any] = {
    "structure_pass": lambda v, **kw: run_structure_pass(v, changed_paths=kw.get("changed_paths")),
    "surface_pass": lambda v, **kw: _surface_pass_runner(
        v, gate_mode=str(kw.pop("gate_mode", None) or "full"), **kw
    ),
    "usability_pass": lambda v, **kw: _surface_pass_runner(
        v, gate_mode=str(kw.pop("gate_mode", None) or "lane_seat"), **kw
    ),
    "module_fit_pass": lambda v, **kw: run_module_fit_pass(
        v, lane_id=str(kw.get("lane_id") or "module"), game_repo_rel=str(kw.get("game_repo_rel") or "")
    ),
    "interpretation_pass": lambda v, **kw: run_interpretation_pass(
        v, lane_id=kw.get("lane_id"), job=kw.get("job")
    ),
    "factory_output_conduct": lambda v, **kw: run_factory_output_gate(v, mode="block"),
    "closed_alpha_release_readiness_pass": lambda v, **kw: __import__(
        "eat_queue_core.weave.factory.closed_alpha_passes",
        fromlist=["run_closed_alpha_release_readiness_pass"],
    ).run_closed_alpha_release_readiness_pass(v),
    "product_kinesthetic_honesty": lambda v, **kw: _import_review_seats().run_product_kinesthetic_honesty_seat(v, **kw),
    "compliance_pass": lambda v, **kw: _import_review_seats().run_compliance_pass(v, **kw),
    "canon_pass": lambda v, **kw: _import_review_seats().run_canon_pass(v, **kw),
    "art_direction_pass": lambda v, **kw: _import_review_seats().run_art_direction_pass(v, **kw),
    "integration_pass": lambda v, **kw: _import_review_seats().run_integration_pass(v, **kw),
    "reliability_pass": lambda v, **kw: _import_review_seats().run_reliability_pass(v, **kw),
    "perf_pass": lambda v, **kw: _import_review_seats().run_perf_pass(v, **kw),
    "balance_pass": lambda v, **kw: _import_review_seats().run_balance_pass(v, **kw),
    "juice_pass": lambda v, **kw: _import_review_seats().run_juice_pass(v, **kw),
    "observability_pass": lambda v, **kw: _import_review_seats().run_observability_pass(v, **kw),
    "extensibility_pass": lambda v, **kw: _import_review_seats().run_extensibility_pass(v, **kw),
    "narrative_audio_pass": lambda v, **kw: _import_review_seats().run_narrative_audio_pass(v, **kw),
    "interconnect_pass": lambda v, **kw: _import_review_seats().run_interconnect_pass(v, **kw),
    "stack_integrate_pass": lambda v, **kw: _import_review_seats().run_stack_integrate_pass_seat(v, **kw),
    "playtest_trace_ingest": lambda v, **kw: __import__(
        "eat_queue_core.weave.factory.factory_exit_gates",
        fromlist=["run_playtest_trace_ingest_gate"],
    ).run_playtest_trace_ingest_gate(v, **kw),
    "operator_confirm_all_kinesthetic": lambda v, **kw: __import__(
        "eat_queue_core.weave.factory.factory_exit_gates",
        fromlist=["run_operator_confirm_all_kinesthetic_gate"],
    ).run_operator_confirm_all_kinesthetic_gate(v, **kw),
}


def _normalize_pass_result(name: str, raw: Any) -> ReviewPassResult:
    if isinstance(raw, ReviewPassResult):
        return raw
    ok = bool(getattr(raw, "ok", False))
    lv = getattr(raw, "little_val", None)
    if lv is None:
        lv = FactoryLittleValResult(ok, [], name)
    detail = str(getattr(raw, "detail", name))
    return ReviewPassResult(name, ok, lv, detail)


def run_slice_exit_gates(
    vault_root: Path,
    *,
    exit_gates: list[str],
    game_repo_rel: str,
    lane_id: str | None = None,
    job: dict[str, Any] | None = None,
    changed_paths: tuple[str, ...] | None = None,
    run_probes: bool = False,
    stack_integrate_dry_run: bool | None = None,
    lane_seat: bool = False,
) -> dict[str, Any]:
    """Run slice exit_gates after lane or slice work."""
    results: dict[str, ReviewPassResult] = {}
    kw: dict[str, Any] = {
        "game_repo_rel": game_repo_rel,
        "lane_id": lane_id,
        "job": job,
        "changed_paths": changed_paths,
        "run_probes": run_probes,
        "dry_run": stack_integrate_dry_run,
        "lane_seat": lane_seat,
        "gate_mode": "lane_seat" if lane_seat else "full",
    }
    tagged = set((job or {}).get("review_passes") or [])
    for gate in exit_gates:
        name = str(gate).strip()
        if name in TAGGED_STUB_SEATS and name not in tagged:
            lv = FactoryLittleValResult(True, [], name)
            results[name] = ReviewPassResult(name, True, lv, f"{name}_not_required_untagged")
            continue
        runner = PASS_RUNNERS.get(name)
        if runner is None:
            lv = FactoryLittleValResult(False, [f"unknown_exit_gate:{name}"], name)
            results[name] = ReviewPassResult(name, False, lv, f"unknown_exit_gate:{name}")
            continue
        raw = runner(vault_root, **kw)
        results[name] = _normalize_pass_result(name, raw)
    all_ok = all(r.ok for r in results.values())
    return {"all_ok": all_ok, "passes": results}
