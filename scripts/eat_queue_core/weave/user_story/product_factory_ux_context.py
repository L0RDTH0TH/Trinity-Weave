"""Build and validate ux_context envelope for execution RESUME_ROADMAP."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .catalog_io import catalog_rows_by_id, load_json, load_yaml, user_story_paths
from .depth_scope import scope_path
from .product_factory_budget import budget_row_ids


@dataclass(frozen=True)
class UxContextValidation:
    ok: bool
    violations: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "violations": list(self.violations)}


def build_ux_context(
    vault_root: Path,
    *,
    project_id: str,
    active_slice: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Scope paths from catalog + rollout budget; dispatch_depth from active_slice when set."""
    vault_root = vault_root.resolve()
    pf_slice = active_slice
    if pf_slice is None:
        from .product_factory_state import load_product_factory

        pf = load_product_factory(vault_root, project_id)
        pf_slice = pf.get("active_slice") if isinstance(pf.get("active_slice"), dict) else None

    row_ids = budget_row_ids(vault_root, project_id)
    if pf_slice and isinstance(pf_slice.get("row_ids"), list) and pf_slice["row_ids"]:
        row_ids = [str(x) for x in pf_slice["row_ids"] if x]

    paths = user_story_paths(vault_root, project_id)
    budget = load_json(paths["budget"])
    by_row = {
        str(r.get("row_id")): r
        for r in budget.get("rows") or []
        if isinstance(r, dict) and r.get("row_id")
    }

    dispatch_depth_override = None
    if pf_slice and pf_slice.get("dispatch_depth") is not None:
        dispatch_depth_override = int(pf_slice["dispatch_depth"])

    l5_paths: list[str] = []
    target_scope_paths: list[str] = []
    dispatch_scope_paths: list[str] = []
    for rid in row_ids:
        l5 = scope_path(vault_root, project_id, rid, 5)
        if l5.is_file():
            l5_paths.append(str(l5.relative_to(vault_root)))
        br = by_row.get(rid) or {}
        tgt = int(br.get("target_depth") or 0)
        if tgt > 0:
            sp_tgt = scope_path(vault_root, project_id, rid, tgt)
            if sp_tgt.is_file():
                target_scope_paths.append(str(sp_tgt.relative_to(vault_root)))
        depth = dispatch_depth_override if dispatch_depth_override is not None else tgt
        if depth > 0:
            sp = scope_path(vault_root, project_id, rid, depth)
            if sp.is_file():
                dispatch_scope_paths.append(str(sp.relative_to(vault_root)))

    return {
        "catalog_row_ids": row_ids,
        "l5_paths": l5_paths,
        "target_scope_paths": target_scope_paths,
        "dispatch_scope_paths": dispatch_scope_paths,
    }


def validate_ux_context(params: dict[str, Any]) -> UxContextValidation:
    """Required when product_factory_run_id is set on execution RESUME_ROADMAP."""
    ux = params.get("ux_context")
    if not isinstance(ux, dict):
        return UxContextValidation(False, ("ux_context_missing",))
    violations: list[str] = []
    rows = ux.get("catalog_row_ids")
    if not isinstance(rows, list) or not rows:
        violations.append("ux_context.catalog_row_ids_empty")
    l5 = ux.get("l5_paths")
    if not isinstance(l5, list) or not l5:
        violations.append("ux_context.l5_paths_empty")
    scopes = ux.get("dispatch_scope_paths")
    if not isinstance(scopes, list) or not scopes:
        violations.append("ux_context.dispatch_scope_paths_empty")
    return UxContextValidation(len(violations) == 0, tuple(violations))


def is_product_factory_execution_resume(params: dict[str, Any]) -> bool:
    if not params.get("product_factory_run_id"):
        return False
    action = str(params.get("action") or "").lower()
    if action == "bootstrap-execution-track":
        return False
    track = str(params.get("roadmap_track") or "execution").lower()
    return track == "execution" and action in ("deepen", "deepen-phase")


def is_product_factory_conceptual_resume(params: dict[str, Any]) -> bool:
    if not params.get("product_factory_run_id"):
        return False
    track = str(params.get("roadmap_track") or "").lower()
    action = str(params.get("action") or "").lower()
    return track == "conceptual" and action in ("deepen", "deepen-phase")


def is_product_factory_roadmap_resume(params: dict[str, Any]) -> bool:
    return is_product_factory_execution_resume(params) or is_product_factory_conceptual_resume(params)


def format_ux_context_handoff(params: dict[str, Any]) -> str:
    """Markdown block injected into RESUME_ROADMAP agent context."""
    ux = params.get("ux_context")
    if not isinstance(ux, dict):
        return ""
    rows = ux.get("catalog_row_ids") or []
    l5_paths = ux.get("l5_paths") or []
    scope_paths = ux.get("dispatch_scope_paths") or []
    lines = [
        "## Product factory UX context (required)",
        "",
        f"- **run_id:** `{params.get('product_factory_run_id')}`",
        f"- **catalog_row_ids:** {', '.join(f'`{r}`' for r in rows)}",
        "",
        "### L5 vision (operator bar)",
    ]
    for p in l5_paths:
        lines.append(f"- [[{p}]]")
    lines.extend(["", "### Target-depth scopes (do not exceed UX bar)", ""])
    for p in scope_paths:
        lines.append(f"- [[{p}]]")
    lines.extend(
        [
            "",
            "Execution deepen **must** align handoff notes with these scope files — "
            "do not invent UX outside L5/L{n} substance.",
        ]
    )
    return "\n".join(lines) + "\n"


def merge_ux_context_into_params(
    vault_root: Path,
    *,
    project_id: str,
    params: dict[str, Any],
) -> dict[str, Any]:
    """Fill or refresh ux_context on execution product-factory RESUME params."""
    out = dict(params)
    if not is_product_factory_execution_resume(out):
        return out
    ux = out.get("ux_context")
    if not isinstance(ux, dict) or not ux.get("l5_paths"):
        pf = None
        try:
            from .product_factory_state import load_product_factory

            pf = load_product_factory(vault_root, project_id)
            active = pf.get("active_slice") if isinstance(pf.get("active_slice"), dict) else None
        except Exception:
            active = None
        out["ux_context"] = build_ux_context(vault_root, project_id=project_id, active_slice=active)
    guidance = str(out.get("user_guidance") or "")
    block = format_ux_context_handoff(out)
    if block and block not in guidance:
        out["user_guidance"] = (guidance.rstrip() + "\n\n" + block).strip()
    return out
