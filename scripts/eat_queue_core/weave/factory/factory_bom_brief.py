"""Operator-facing Factory BOM brief (generated from verifiers)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..factory.factory_output_gate import parse_factory_orchestrator_yaml
from .factory_bom import BomStatus, BomStepResult, evaluate_factory_bom
from .factory_bom_io import product_bom_path

_LOOP_SECTION_LABELS: dict[str, str] = {
    "operator_loop_1_pmg": "Operator loop 1 — PMG",
    "operator_loop_2_catalog_levels": "Operator loop 2 — catalog + levels",
    "execution_engineering": "Execution engineering (machine)",
    "operator_loop_3_slice_selection": "Operator loop 3 — slice selection",
    "product": "Product",
    "implementation_factory": "Implementation factory",
    "build_progress": "Build progress",
    "product_acceptance": "Product acceptance",
    "roadmap_factory": "Roadmap factory (legacy)",
}


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def brief_dir(vault_root: Path, project_id: str) -> Path:
    cfg = parse_factory_orchestrator_yaml(vault_root / "3-Resources/Second-Brain-Config.md")
    fb = cfg.get("factory_bom") if isinstance(cfg.get("factory_bom"), dict) else {}
    rel = str(
        fb.get("brief_dir_rel")
        or f"1-Projects/{project_id}/Factory-DRB/operator-feedback/factory-bom-briefs"
    )
    if not rel.startswith("1-Projects/"):
        rel = f"1-Projects/{project_id}/{rel.lstrip('/')}"
    return vault_root / rel


@dataclass(frozen=True)
class FactoryBomBriefResult:
    ok: bool
    path: str
    blocked_at: str | None
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "path": self.path,
            "blocked_at": self.blocked_at,
            "detail": self.detail,
        }


_STATUS_ICON = {
    BomStatus.PASS: "✅",
    BomStatus.PARTIAL: "🟡",
    BomStatus.MISSING: "❌",
    BomStatus.WAIVED: "⏭️",
    BomStatus.NOT_APPLICABLE: "—",
}


def _section_order(steps: tuple[BomStepResult, ...]) -> list[str]:
    seen: list[str] = []
    for step in steps:
        if step.section not in seen:
            seen.append(step.section)
    preferred = list(_LOOP_SECTION_LABELS.keys())
    ordered = [s for s in preferred if s in seen]
    ordered.extend(s for s in seen if s not in ordered)
    return ordered


def _render_loop_section(lines: list[str], section: str, section_steps: list[BomStepResult]) -> None:
    label = _LOOP_SECTION_LABELS.get(section, section.replace("_", " ").title())
    lines.append(f"## {label}")
    lines.append("")
    aggregate = next((s for s in section_steps if s.step_id == section), None)
    if aggregate:
        icon = _STATUS_ICON.get(aggregate.status, "?")
        req = " *(required)*" if aggregate.required else ""
        lines.append(f"**Loop status:** {icon} `{aggregate.status.value}`{req}")
        lines.append(f"- detail: {aggregate.detail}")
        lines.append("")
        subs = [s for s in section_steps if s.step_id != section]
        if subs:
            lines.append("**Sub-checks:**")
            lines.append("")
            for step in subs:
                icon = _STATUS_ICON.get(step.status, "?")
                lines.append(f"- {icon} `{step.step_id}` — {step.detail}")
            lines.append("")
    else:
        for step in section_steps:
            icon = _STATUS_ICON.get(step.status, "?")
            req = " *(required)*" if step.required else ""
            lines.append(f"- {icon} **{step.label}**{req} — `{step.status.value}`")
            lines.append(f"  - artifact: `{step.artifact_ref}`")
            lines.append(f"  - detail: {step.detail}")
            lines.append("")


def write_factory_bom_brief(
    vault_root: Path,
    *,
    project_id: str,
) -> FactoryBomBriefResult:
    vault_root = vault_root.resolve()
    result = evaluate_factory_bom(vault_root, project_id=project_id)
    out_dir = brief_dir(vault_root, project_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = _utc_stamp()
    out_path = out_dir / f"Factory-BOM-Brief-{stamp}.md"

    ver = result.versioning
    lines = [
        "---",
        f"title: Factory BOM Brief {stamp}",
        f"project-id: {project_id}",
        "brief_kind: factory_bom",
        f"blocked_at: {result.blocked_at or ''}",
        f"bom_ok: {str(result.ok).lower()}",
        "---",
        "",
        f"# Factory BOM — {project_id}",
        "",
        "> Three operator loops + machine phases. Same checklist for operator and factory.",
        "",
    ]
    if ver:
        lines.extend(
            [
                "## Version pins",
                "",
                "| Field | Value |",
                "|-------|-------|",
                f"| product_version | `{ver.product_version}` |",
                f"| bom_schema_version | {ver.bom_schema_version} |",
                f"| bom_revision | {ver.bom_revision} |",
                f"| release_definition | `{ver.release_definition_ref}` |",
                f"| weave_core | `{ver.weave_core_version}` |",
                "",
            ]
        )

    if result.blocked_at:
        if result.blocked_at.startswith("operator_loop_"):
            lines.append(f"**Operator blocked at:** `{result.blocked_at}`")
        else:
            lines.append(f"**Blocked at:** `{result.blocked_at}`")
        lines.append("")

    by_section: dict[str, list[BomStepResult]] = {}
    for step in result.steps:
        by_section.setdefault(step.section, []).append(step)

    for section in _section_order(result.steps):
        _render_loop_section(lines, section, by_section.get(section, []))

    lines.extend(
        [
            "## Summary",
            "",
            f"- pass: {result.summary.get('pass', 0)}",
            f"- partial: {result.summary.get('partial', 0)}",
            f"- missing: {result.summary.get('missing', 0)}",
            f"- waived: {result.summary.get('waived', 0)}",
            "",
            f"BOM manifest: `{product_bom_path(vault_root, project_id).relative_to(vault_root)}`",
        ]
    )

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    latest = out_dir / "latest.md"
    latest.write_text(out_path.read_text(encoding="utf-8"), encoding="utf-8")
    return FactoryBomBriefResult(
        ok=result.ok,
        path=str(out_path.relative_to(vault_root)),
        blocked_at=result.blocked_at,
        detail="factory_bom_brief_written",
    )
