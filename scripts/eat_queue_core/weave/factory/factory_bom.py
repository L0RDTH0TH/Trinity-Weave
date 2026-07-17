"""Product Factory BOM — shared operator/factory setup checklist."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable

from ..user_story.catalog_coverage import run_catalog_coverage, run_catalog_freeze_gate
from ..user_story.catalog_io import catalog_rows_by_id, load_json, load_yaml, parse_state_frontmatter, user_story_paths
from ..user_story.catalog_mint_propose import _find_pmg_path
from ..user_story.depth_scope import scope_path
from ..user_story.user_story_feedback import all_rows_operator_confirmed, list_pending_user_story_confirmations
from ..versioning_contract import (
    BOM_SCHEMA_VERSION,
    VersionLayers,
    check_bom_schema_compat,
    check_weave_core_compat,
    parse_version_block,
)
from .factory_bom_io import load_product_bom, parse_release_frontmatter, product_bom_path
from .factory_output_gate import parse_factory_orchestrator_yaml
from .lane_charters import validate_six_lane_charters
from .tech_stack_manifest import load_manifest


class BomStatus(str, Enum):
    MISSING = "missing"
    PARTIAL = "partial"
    PASS = "pass"
    WAIVED = "waived"
    NOT_APPLICABLE = "not_applicable"


@dataclass(frozen=True)
class BomStepResult:
    step_id: str
    section: str
    label: str
    status: BomStatus
    required: bool
    artifact_ref: str
    detail: str
    verifier: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "section": self.section,
            "label": self.label,
            "status": self.status.value,
            "required": self.required,
            "artifact_ref": self.artifact_ref,
            "detail": self.detail,
            "verifier": self.verifier,
        }


@dataclass(frozen=True)
class FactoryBomResult:
    ok: bool
    blocked_at: str | None
    product_id: str
    versioning: VersionLayers | None
    steps: tuple[BomStepResult, ...]
    summary: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "blocked_at": self.blocked_at,
            "product_id": self.product_id,
            "versioning": self.versioning.to_dict() if self.versioning else None,
            "steps": [s.to_dict() for s in self.steps],
            "summary": dict(self.summary),
            "bom_schema_version": BOM_SCHEMA_VERSION,
        }


def _step(
    step_id: str,
    section: str,
    label: str,
    *,
    status: BomStatus,
    required: bool,
    artifact_ref: str,
    detail: str,
    verifier: str,
) -> BomStepResult:
    return BomStepResult(
        step_id=step_id,
        section=section,
        label=label,
        status=status,
        required=required,
        artifact_ref=artifact_ref,
        detail=detail,
        verifier=verifier,
    )


def _waived(step_id: str, doc: dict[str, Any]) -> bool:
    waived = doc.get("waived_steps") or []
    if isinstance(waived, str):
        waived = [waived]
    return step_id in (waived if isinstance(waived, list) else [])


def _budget_row_ids(vault_root: Path, project_id: str) -> list[str]:
    paths = user_story_paths(vault_root, project_id)
    budget = load_json(paths["budget"])
    ids: list[str] = []
    for row in budget.get("rows") or []:
        if isinstance(row, dict) and row.get("row_id"):
            ids.append(str(row["row_id"]))
    return ids


def _evaluate_product_section(
    vault_root: Path, project_id: str, doc: dict[str, Any]
) -> list[BomStepResult]:
    steps: list[BomStepResult] = []
    bom_path = product_bom_path(vault_root, project_id)

    if bom_path.is_file():
        ver = parse_version_block(doc)
        ok_schema, schema_detail = check_bom_schema_compat(ver.bom_schema_version)
        weave_ok, weave_detail = check_weave_core_compat(doc)
        status = BomStatus.PASS if ok_schema else BomStatus.MISSING
        if ok_schema and not weave_ok:
            status = BomStatus.PARTIAL
        steps.append(
            _step(
                "product_bom_declared",
                "product",
                "Product BOM manifest exists",
                status=status,
                required=True,
                artifact_ref=str(bom_path.relative_to(vault_root)),
                detail=f"{schema_detail}; {weave_detail}",
                verifier="factory_bom_io.load_product_bom",
            )
        )
    else:
        steps.append(
            _step(
                "product_bom_declared",
                "product",
                "Product BOM manifest exists",
                status=BomStatus.MISSING,
                required=True,
                artifact_ref=str(bom_path.relative_to(vault_root)),
                detail="product_bom_missing",
                verifier="factory_bom_io.load_product_bom",
            )
        )
        return steps

    ver = parse_version_block(doc)
    rel_ref = ver.release_definition_ref
    if not rel_ref:
        steps.append(
            _step(
                "release_definition_linked",
                "product",
                "Release definition linked",
                status=BomStatus.MISSING,
                required=True,
                artifact_ref="(release_definition_ref)",
                detail="release_definition_ref_unset",
                verifier="versioning_contract.parse_version_block",
            )
        )
    else:
        if rel_ref.startswith("1-Projects/"):
            rel_path = vault_root / rel_ref
        else:
            rel_path = vault_root / f"1-Projects/{project_id}" / rel_ref.lstrip("/")
        exists = rel_path.is_file()
        fm = parse_release_frontmatter(rel_path) if exists else {}
        title = str(fm.get("title") or "")
        match = (
            exists
            and ver.product_version
            and (title == ver.product_version or ver.product_version in rel_ref)
        )
        steps.append(
            _step(
                "release_definition_linked",
                "product",
                "Release definition linked",
                status=BomStatus.PASS if exists else BomStatus.MISSING,
                required=True,
                artifact_ref=rel_ref,
                detail="release_definition_ok" if exists else "release_definition_missing",
                verifier="factory_bom_io.parse_release_frontmatter",
            )
        )
        steps.append(
            _step(
                "product_version_aligned",
                "product",
                "Product version matches release definition",
                status=BomStatus.PASS if match else (BomStatus.PARTIAL if exists else BomStatus.MISSING),
                required=True,
                artifact_ref=rel_ref,
                detail=f"product_version={ver.product_version}:release_title={title}",
                verifier="versioning_contract.parse_version_block",
            )
        )

    return steps


def _evaluate_roadmap_section(vault_root: Path, project_id: str, doc: dict[str, Any]) -> list[BomStepResult]:
    steps: list[BomStepResult] = []
    paths = user_story_paths(vault_root, project_id)
    state = parse_state_frontmatter(paths["state"])

    pmg = _find_pmg_path(vault_root, project_id)
    steps.append(
        _step(
            "pmg_exists",
            "roadmap_factory",
            "Project Master Goal (PMG) exists",
            status=BomStatus.PASS if pmg else BomStatus.MISSING,
            required=True,
            artifact_ref=str(pmg.relative_to(vault_root)) if pmg else f"1-Projects/{project_id}/*Master*Goal*",
            detail="pmg_found" if pmg else "pmg_missing",
            verifier="catalog_mint_propose._find_pmg_path",
        )
    )

    catalog_ok = paths["catalog"].is_file()
    steps.append(
        _step(
            "catalog_exists",
            "roadmap_factory",
            "Slice catalog exists",
            status=BomStatus.PASS if catalog_ok else BomStatus.MISSING,
            required=True,
            artifact_ref=str(paths["catalog"].relative_to(vault_root)),
            detail="catalog_ok" if catalog_ok else "catalog_missing",
            verifier="catalog_io.user_story_paths",
        )
    )

    cov = run_catalog_coverage(vault_root, project_id=project_id)
    steps.append(
        _step(
            "catalog_coverage",
            "roadmap_factory",
            "Catalog coverage (pins + rows)",
            status=BomStatus.PASS if cov.ok else BomStatus.MISSING,
            required=True,
            artifact_ref=str(paths["catalog"].relative_to(vault_root)),
            detail="; ".join(cov.violations) if cov.violations else "coverage_ok",
            verifier="catalog_coverage.run_catalog_coverage",
        )
    )

    signed = bool(state.get("catalog_signed_at"))
    sid = "catalog_signed"
    steps.append(
        _step(
            sid,
            "roadmap_factory",
            "Catalog operator sign-off",
            status=BomStatus.WAIVED
            if _waived(sid, doc)
            else (BomStatus.PASS if signed else BomStatus.MISSING),
            required=not _waived(sid, doc),
            artifact_ref=str(paths["state"].relative_to(vault_root)),
            detail=str(state.get("catalog_signed_at") or "catalog_not_signed"),
            verifier="operator_user_story_confirm.catalog_is_signed",
        )
    )

    dc_ver = state.get("depth_charter_version")
    steps.append(
        _step(
            "depth_charter_versioned",
            "roadmap_factory",
            "Depth charter version pinned",
            status=BomStatus.PASS if dc_ver else BomStatus.MISSING,
            required=True,
            artifact_ref=str(paths["depth_charter"].relative_to(vault_root)),
            detail=str(dc_ver or "depth_charter_version_missing"),
            verifier="catalog_freeze_gate",
        )
    )

    row_ids = _budget_row_ids(vault_root, project_id)
    if not row_ids:
        catalog = load_yaml(paths["catalog"])
        row_ids = [rid for rid, r in catalog_rows_by_id(catalog).items() if r.get("planned")]

    l5_missing: list[str] = []
    for rid in row_ids:
        l5 = scope_path(vault_root, project_id, rid, 5)
        if not l5.is_file() or len(l5.read_text(encoding="utf-8", errors="replace").strip()) < 80:
            l5_missing.append(rid)

    steps.append(
        _step(
            "l5_complete_per_row",
            "roadmap_factory",
            "L5 complete vision per assigned row",
            status=BomStatus.PASS if not l5_missing else BomStatus.PARTIAL,
            required=True,
            artifact_ref=str(paths["scopes_dir"].relative_to(vault_root)),
            detail=f"missing_or_thin:{l5_missing}" if l5_missing else "l5_ok",
            verifier="depth_scope.scope_path",
        )
    )

    l1_missing: list[str] = []
    for rid in row_ids:
        l1 = scope_path(vault_root, project_id, rid, 1)
        if not l1.is_file():
            l1_missing.append(rid)

    steps.append(
        _step(
            "depth_sliced",
            "roadmap_factory",
            "Depth slicer output (L1..L5 scopes)",
            status=BomStatus.PASS if not l1_missing else BomStatus.MISSING,
            required=True,
            artifact_ref=str(paths["scopes_dir"].relative_to(vault_root)),
            detail=f"missing_l1:{l1_missing}" if l1_missing else "depth_sliced_ok",
            verifier="depth_slicer.run_depth_slicer",
        )
    )

    budget = load_json(paths["budget"])
    has_budget = bool(budget.get("rows"))
    steps.append(
        _step(
            "rollout_budget_set",
            "roadmap_factory",
            "Operator rollout budget set",
            status=BomStatus.PASS if has_budget else BomStatus.MISSING,
            required=True,
            artifact_ref=str(paths["budget"].relative_to(vault_root)),
            detail=f"rollout_version={budget.get('rollout_version')}" if has_budget else "budget_missing",
            verifier="rollout_slicer.run_rollout_slicer",
        )
    )

    confirmed = all_rows_operator_confirmed(vault_root, project_id, row_ids) if row_ids else False
    pending = list_pending_user_story_confirmations(vault_root, project_id)
    sid = "operator_experiential"
    steps.append(
        _step(
            sid,
            "roadmap_factory",
            "Operator experiential confirm per row",
            status=BomStatus.WAIVED
            if _waived(sid, doc)
            else (BomStatus.PASS if confirmed else BomStatus.MISSING),
            required=not _waived(sid, doc),
            artifact_ref="Factory-DRB/operator-feedback/user-story-operator-feedback.yaml",
            detail=f"pending={len(pending)}" if pending else "all_confirmed",
            verifier="user_story_feedback.all_rows_operator_confirmed",
        )
    )

    freeze = run_catalog_freeze_gate(vault_root, project_id=project_id)
    steps.append(
        _step(
            "catalog_freeze_ready",
            "roadmap_factory",
            "Catalog freeze gate (pre-conceptual lock)",
            status=BomStatus.PASS if freeze.get("ok") else BomStatus.PARTIAL,
            required=False,
            artifact_ref=str(paths["catalog"].relative_to(vault_root)),
            detail="; ".join(freeze.get("violations") or []) or "freeze_ok",
            verifier="catalog_coverage.run_catalog_freeze_gate",
        )
    )

    return steps


def _evaluate_implementation_section(
    vault_root: Path, project_id: str, doc: dict[str, Any]
) -> list[BomStepResult]:
    steps: list[BomStepResult] = []
    cfg = parse_factory_orchestrator_yaml(vault_root / "3-Resources/Second-Brain-Config.md")
    fo = cfg.get("factory_orchestrator") if isinstance(cfg.get("factory_orchestrator"), dict) else {}
    feed = str(fo.get("feed_authority") or "vault_roadmap")

    steps.append(
        _step(
            "feed_authority_declared",
            "implementation_factory",
            "Factory feed authority declared",
            status=BomStatus.PASS,
            required=True,
            artifact_ref="3-Resources/Second-Brain-Config.md",
            detail=f"feed_authority={feed}",
            verifier="factory_output_gate.parse_factory_orchestrator_yaml",
        )
    )

    if feed == "vault_roadmap":
        paths = user_story_paths(vault_root, project_id)
        state = parse_state_frontmatter(paths["state"])
        budget = load_json(paths["budget"])
        row_ids = _budget_row_ids(vault_root, project_id)
        signed = bool(state.get("catalog_signed_at"))
        has_budget = bool(budget.get("rows"))
        sliced = all(
            scope_path(vault_root, project_id, rid, 1).is_file() for rid in row_ids
        ) if row_ids else False
        ready = signed and has_budget and sliced
        status = BomStatus.PASS if ready else BomStatus.PARTIAL
        detail = f"signed={signed}:budget={has_budget}:sliced={sliced}"
    else:
        status = BomStatus.PARTIAL
        detail = f"feed_authority={feed}:roadmap_feed_not_primary"

    steps.append(
        _step(
            "vault_roadmap_feed_ready",
            "implementation_factory",
            "Vault roadmap feed armed",
            status=status,
            required=feed == "vault_roadmap",
            artifact_ref="3-Resources/Second-Brain-Config.md",
            detail=detail,
            verifier="work_order_translate.translate_vault_work_orders",
        )
    )

    charter_v = validate_six_lane_charters(vault_root)
    steps.append(
        _step(
            "lane_charters_active",
            "implementation_factory",
            "Six lane charters active",
            status=BomStatus.PASS if not charter_v else BomStatus.MISSING,
            required=True,
            artifact_ref=".technical/parallel/*/milestone-charter.yaml",
            detail="; ".join(charter_v) if charter_v else "charters_ok",
            verifier="lane_charters.validate_six_lane_charters",
        )
    )

    try:
        manifest = load_manifest(vault_root)
        vetted = bool(manifest.operator_stack_baseline_vetted)
    except (FileNotFoundError, OSError, ValueError):
        vetted = False

    steps.append(
        _step(
            "stack_baseline_vetted",
            "implementation_factory",
            "Stack baseline vetted (Product 1)",
            status=BomStatus.PASS if vetted else BomStatus.MISSING,
            required=True,
            artifact_ref="Factory-DRB/tech-stack-manifest.yaml",
            detail="stack_baseline_vetted" if vetted else "stack_baseline_not_vetted",
            verifier="tech_stack_manifest.load_manifest",
        )
    )

    ver = parse_version_block(doc) if doc else None
    game_repo = ""
    if ver and ver.release_definition_ref:
        rel = ver.release_definition_ref
        rel_path = vault_root / f"1-Projects/{project_id}" / rel.lstrip("/")
        if not rel.startswith("1-Projects/"):
            rel_path = vault_root / f"1-Projects/{project_id}" / rel.lstrip("/")
        fm = parse_release_frontmatter(rel_path)
        game_repo = str(fm.get("game_repo") or "")

    game_path = vault_root / game_repo if game_repo else None
    steps.append(
        _step(
            "game_repo_exists",
            "implementation_factory",
            "Game repo path exists",
            status=BomStatus.PASS
            if game_path and game_path.is_dir()
            else (BomStatus.PARTIAL if game_repo else BomStatus.MISSING),
            required=bool(game_repo),
            artifact_ref=game_repo or "(game_repo from release definition)",
            detail="game_repo_ok" if game_path and game_path.is_dir() else "game_repo_missing",
            verifier="factory_bom_io.parse_release_frontmatter",
        )
    )

    return steps


def _evaluate_progress_section(vault_root: Path, project_id: str) -> list[BomStepResult]:
    paths = user_story_paths(vault_root, project_id)
    budget = load_json(paths["budget"])
    rows = budget.get("rows") or []
    if not rows:
        return [
            _step(
                "depth_weld_progress",
                "build_progress",
                "Per-row depth weld progress",
                status=BomStatus.MISSING,
                required=False,
                artifact_ref=str(paths["budget"].relative_to(vault_root)),
                detail="no_budget_rows",
                verifier="depth_bump.bump_row_current_depth",
            )
        ]

    partial_rows: list[str] = []
    complete_rows: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        rid = str(row.get("row_id") or "")
        cur = int(row.get("current_depth") or 0)
        tgt = int(row.get("target_depth") or 0)
        if cur >= tgt and tgt > 0:
            complete_rows.append(f"{rid}:{cur}/{tgt}")
        else:
            partial_rows.append(f"{rid}:{cur}/{tgt}")

    status = BomStatus.PASS if not partial_rows else BomStatus.PARTIAL
    return [
        _step(
            "depth_weld_progress",
            "build_progress",
            "Per-row depth weld progress",
            status=status,
            required=False,
            artifact_ref=str(paths["budget"].relative_to(vault_root)),
            detail=f"complete=[{', '.join(complete_rows)}]; pending=[{', '.join(partial_rows)}]",
            verifier="slice-depth-budget.json",
        )
    ]


def _evaluate_acceptance_section(
    vault_root: Path, project_id: str, doc: dict[str, Any]
) -> list[BomStepResult]:
    enforce = bool(doc.get("enforce_product_acceptance"))
    steps: list[BomStepResult] = []

    try:
        from .surface_pass import run_surface_pass

        surface = run_surface_pass(vault_root, run_probes=False, run_smokes=False)
        surface_ok = surface.ok
        surface_detail = "; ".join(surface.little_val.anti_pattern_violations) if not surface_ok else "surface_pass_ok"
    except Exception as exc:  # noqa: BLE001 — BOM must not crash on optional tier
        surface_ok = False
        surface_detail = f"surface_pass_error:{exc}"

    sid = "surface_pass"
    steps.append(
        _step(
            sid,
            "product_acceptance",
            "Surface pass (human operability)",
            status=BomStatus.WAIVED
            if _waived(sid, doc)
            else (BomStatus.PASS if surface_ok else BomStatus.MISSING),
            required=enforce and not _waived(sid, doc),
            artifact_ref="Factory-DRB/Gate-Precedence-Conflict-Doctrine-v1.md",
            detail=surface_detail,
            verifier="surface_pass.run_surface_pass",
        )
    )

    return steps


SECTION_EVALUATORS: dict[str, Callable[..., list[BomStepResult]]] = {
    "product": _evaluate_product_section,
    "roadmap_factory": _evaluate_roadmap_section,
    "implementation_factory": _evaluate_implementation_section,
    "build_progress": lambda vr, pid, doc: _evaluate_progress_section(vr, pid),
    "product_acceptance": _evaluate_acceptance_section,
}


def evaluate_factory_bom(
    vault_root: Path,
    *,
    project_id: str,
    sections: tuple[str, ...] | None = None,
) -> FactoryBomResult:
    """
    Evaluate Product Factory BOM — delegates to existing verifiers only.

    Returns blocked_at = first required step that is missing/partial.
    v2 manifests use operator loop ids for blocked_at.
    """
    vault_root = vault_root.resolve()
    doc = load_product_bom(vault_root, project_id)
    versioning = parse_version_block(doc) if doc else None
    schema = versioning.bom_schema_version if versioning else BOM_SCHEMA_VERSION
    if schema >= 2:
        return evaluate_factory_bom_v2(vault_root, project_id=project_id, sections=sections, doc=doc)

    active_sections = sections or tuple(SECTION_EVALUATORS.keys())
    all_steps: list[BomStepResult] = []

    for section in active_sections:
        fn = SECTION_EVALUATORS.get(section)
        if not fn:
            continue
        if section in ("build_progress",):
            all_steps.extend(fn(vault_root, project_id, doc))
        else:
            all_steps.extend(fn(vault_root, project_id, doc))

    summary: dict[str, int] = {}
    for st in BomStatus:
        summary[st.value] = sum(1 for s in all_steps if s.status == st)

    blocked_at: str | None = None
    for step in all_steps:
        if not step.required:
            continue
        if step.status in (BomStatus.MISSING, BomStatus.PARTIAL):
            blocked_at = step.step_id
            break

    ok = blocked_at is None
    return FactoryBomResult(
        ok=ok,
        blocked_at=blocked_at,
        product_id=project_id,
        versioning=versioning,
        steps=tuple(all_steps),
        summary=summary,
    )


def bom_blocks_factory_stage(
    vault_root: Path,
    *,
    project_id: str,
    sections: tuple[str, ...] = ("product", "roadmap_factory", "implementation_factory"),
) -> tuple[bool, str | None, FactoryBomResult]:
    """Gate hook for ROADMAP_FACTORY_STAGE_FACTORY / orchestrator."""
    doc = load_product_bom(vault_root, project_id)
    ver = parse_version_block(doc) if doc else None
    if ver and ver.bom_schema_version >= 2:
        return bom_blocks_factory_stage_v2(vault_root, project_id=project_id)
    result = evaluate_factory_bom(vault_root, project_id=project_id, sections=sections)
    return result.ok, result.blocked_at, result


def _loop_step_from_check(loop_id: str, label: str, sub_checks: tuple[tuple[str, bool, str], ...]) -> list[BomStepResult]:
    """Expand loop aggregate into BOM steps (aggregate + sub-checks)."""
    ok = all(c[1] for c in sub_checks)
    status = BomStatus.PASS if ok else BomStatus.MISSING
    steps: list[BomStepResult] = [
        _step(
            loop_id,
            loop_id,
            label,
            status=status,
            required=True,
            artifact_ref="user-story-state.md",
            detail="loop_ok" if ok else next((c[2] for c in sub_checks if not c[1]), "loop_incomplete"),
            verifier="product_factory_loops",
        )
    ]
    for sid, passed, detail in sub_checks:
        steps.append(
            _step(
                sid,
                loop_id,
                sid.replace("_", " "),
                status=BomStatus.PASS if passed else BomStatus.MISSING,
                required=False,
                artifact_ref="",
                detail=detail,
                verifier="product_factory_loops",
            )
        )
    return steps


def evaluate_factory_bom_v2(
    vault_root: Path,
    *,
    project_id: str,
    sections: tuple[str, ...] | None = None,
    doc: dict[str, Any] | None = None,
) -> FactoryBomResult:
    from ..user_story.product_factory_loops import (
        check_execution_engineering,
        check_operator_loop_1,
        check_operator_loop_2,
        check_operator_loop_3,
    )

    vault_root = vault_root.resolve()
    if doc is None:
        doc = load_product_bom(vault_root, project_id)
    versioning = parse_version_block(doc) if doc else None

    default_sections = (
        "product",
        "operator_loop_1_pmg",
        "operator_loop_2_catalog_levels",
        "execution_engineering",
        "operator_loop_3_slice_selection",
        "implementation_factory",
        "build_progress",
        "product_acceptance",
    )
    active = sections or default_sections
    all_steps: list[BomStepResult] = []

    if "product" in active:
        all_steps.extend(_evaluate_product_section(vault_root, project_id, doc or {}))

    l1 = check_operator_loop_1(vault_root, project_id)
    if "operator_loop_1_pmg" in active:
        all_steps.extend(_loop_step_from_check(l1.loop_id, "Operator loop 1 — PMG", l1.sub_checks))

    l2 = check_operator_loop_2(vault_root, project_id)
    if "operator_loop_2_catalog_levels" in active:
        all_steps.extend(
            _loop_step_from_check(l2.loop_id, "Operator loop 2 — catalog + levels", l2.sub_checks)
        )

    eng = check_execution_engineering(vault_root, project_id)
    if "execution_engineering" in active:
        all_steps.extend(
            _loop_step_from_check("execution_engineering", "Execution engineering (machine)", eng.sub_checks)
        )

    l3 = check_operator_loop_3(vault_root, project_id)
    if "operator_loop_3_slice_selection" in active:
        all_steps.extend(
            _loop_step_from_check(l3.loop_id, "Operator loop 3 — slice selection", l3.sub_checks)
        )

    if "implementation_factory" in active:
        all_steps.extend(_evaluate_implementation_section(vault_root, project_id, doc or {}))
    if "build_progress" in active:
        all_steps.extend(_evaluate_progress_section(vault_root, project_id))
    if "product_acceptance" in active:
        all_steps.extend(_evaluate_acceptance_section(vault_root, project_id, doc or {}))

    summary: dict[str, int] = {}
    for st in BomStatus:
        summary[st.value] = sum(1 for s in all_steps if s.status == st)

    blocked_at: str | None = None
    for loop_id, chk in (
        (l1.loop_id, l1),
        (l2.loop_id, l2),
        ("execution_engineering", eng),
        (l3.loop_id, l3),
    ):
        if not chk.ok:
            if loop_id.startswith("operator_loop_"):
                blocked_at = loop_id
            else:
                fail_sub = next((c[0] for c in chk.sub_checks if not c[1]), "execution_engineering")
                blocked_at = f"machine:{fail_sub}"
            break

    if blocked_at is None:
        for step in all_steps:
            if not step.required:
                continue
            if step.step_id.startswith("operator_loop_"):
                continue
            if step.section in (
                "operator_loop_1_pmg",
                "operator_loop_2_catalog_levels",
                "execution_engineering",
                "operator_loop_3_slice_selection",
            ):
                continue
            if step.status in (BomStatus.MISSING, BomStatus.PARTIAL):
                blocked_at = step.step_id
                break

    ok = blocked_at is None
    return FactoryBomResult(
        ok=ok,
        blocked_at=blocked_at,
        product_id=project_id,
        versioning=versioning,
        steps=tuple(all_steps),
        summary=summary,
    )


def bom_blocks_factory_stage_v2(
    vault_root: Path,
    *,
    project_id: str,
) -> tuple[bool, str | None, FactoryBomResult]:
    """Factory stage gate for BOM schema v2 — loops through implementation_factory."""
    sections = (
        "product",
        "operator_loop_1_pmg",
        "operator_loop_2_catalog_levels",
        "execution_engineering",
        "operator_loop_3_slice_selection",
        "implementation_factory",
    )
    result = evaluate_factory_bom_v2(vault_root, project_id=project_id, sections=sections)
    return result.ok, result.blocked_at, result
