"""Load and validate Tech-Stack-Manifest-v1.yaml."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .factory_drb_paths import (
    drb_artifact_path,
    resolve_project_id,
    tech_stack_manifest_path,
)
from .stack_domain_registry import load_stack_domain_registry

DEFAULT_MANIFEST_REL = (
    "1-Projects/genesis-mythos-master/Factory-DRB/Tech-Stack-Manifest-v1.yaml"
)

ROW_KINDS_INTEGRATABLE = frozenset({"locked", "integrated"})
ROW_KINDS_SKELETON = frozenset({"skeleton", "candidate_search"})


@dataclass(frozen=True)
class ManifestRow:
    id: str
    stack_domain_id: str | None
    category: str
    status: str
    row_kind: str
    baseline_required: bool
    repo_path: str | None
    wrap_policy: str | None
    operational_confirmed: bool
    poc_canonical: bool
    interop_required: bool
    raw: dict[str, Any]

    @property
    def r1_required(self) -> bool:
        """Backward compat alias."""
        return self.baseline_required


@dataclass(frozen=True)
class TechStackManifest:
    path: Path
    project_id: str
    game_repo_path: str
    pipeline_certified: bool
    operator_stack_baseline_vetted: bool
    rows: tuple[ManifestRow, ...]

    def baseline_required_rows(self) -> tuple[ManifestRow, ...]:
        return tuple(r for r in self.rows if r.baseline_required)

    def r1_required_rows(self) -> tuple[ManifestRow, ...]:
        return self.baseline_required_rows()

    def row_by_id(self, row_id: str) -> ManifestRow | None:
        for row in self.rows:
            if row.id == row_id:
                return row
        return None

    def row_by_stack_domain(self, domain_id: str) -> ManifestRow | None:
        for row in self.rows:
            if row.stack_domain_id == domain_id:
                return row
        return None


def _load_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore[import-untyped]

        data = yaml.safe_load(text)
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"invalid yaml: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"manifest root must be mapping: {path}")
    return data


def load_manifest(
    vault_root: Path,
    project_id: str | None = None,
    manifest_rel: str | None = None,
) -> TechStackManifest:
    if manifest_rel:
        path = vault_root / manifest_rel
    else:
        path = tech_stack_manifest_path(vault_root, project_id)
    if not path.is_file():
        raise FileNotFoundError(f"manifest missing: {path}")

    data = _load_yaml(path)
    rows_raw = data.get("rows") or []
    if not isinstance(rows_raw, list):
        raise ValueError("manifest rows must be a list")

    rows: list[ManifestRow] = []
    for item in rows_raw:
        if not isinstance(item, dict) or "id" not in item:
            raise ValueError("each manifest row must be a mapping with id")
        rows.append(
            ManifestRow(
                id=str(item["id"]),
                stack_domain_id=item.get("stack_domain_id"),
                category=str(item.get("category", "")),
                status=str(item.get("status", "draft")),
                row_kind=str(item.get("row_kind", "candidate_search")),
                baseline_required=bool(item.get("baseline_required", False)),
                repo_path=item.get("repo_path"),
                wrap_policy=item.get("wrap_policy"),
                operational_confirmed=bool(item.get("operational_confirmed", False)),
                poc_canonical=bool(item.get("poc_canonical", False)),
                interop_required=bool(item.get("interop_required", False)),
                raw=item,
            )
        )

    return TechStackManifest(
        path=path,
        project_id=str(data.get("project_id", "")),
        game_repo_path=str(data.get("game_repo_path", "")),
        pipeline_certified=bool(data.get("pipeline_certified", False)),
        operator_stack_baseline_vetted=bool(data.get("operator_stack_baseline_vetted", False)),
        rows=tuple(rows),
    )


def validate_manifest_schema(
    manifest: TechStackManifest,
    vault_root: Path,
    *,
    expected_project_id: str | None = None,
) -> list[str]:
    """Return list of schema violations (empty = ok)."""
    violations: list[str] = []
    expected = expected_project_id or manifest.project_id or resolve_project_id(vault_root, None)
    if manifest.project_id and expected and manifest.project_id != expected:
        violations.append(f"unexpected project_id: {manifest.project_id} (expected {expected})")
    if not manifest.game_repo_path:
        violations.append("game_repo_path missing")

    ids = [r.id for r in manifest.rows]
    if len(ids) != len(set(ids)):
        violations.append("duplicate manifest row ids")

    try:
        pid = manifest.project_id or resolve_project_id(vault_root, None)
        registry = load_stack_domain_registry(vault_root, project_id=pid)
    except FileNotFoundError:
        violations.append("stack_domain_registry missing")
        return violations

    if registry.poc_canonical:
        violations.append("registry poc_canonical must be false")

    baseline_domains = {d.id for d in registry.domains if d.baseline_required}
    manifest_domains = {r.stack_domain_id for r in manifest.baseline_required_rows() if r.stack_domain_id}
    missing_domains = baseline_domains - manifest_domains - {"engine_runtime"}
    if missing_domains:
        violations.append(f"manifest missing baseline domains: {sorted(missing_domains)}")

    for row in manifest.rows:
        if row.row_kind in ROW_KINDS_SKELETON and row.operational_confirmed:
            violations.append(f"skeleton_marked_operational:{row.id}")
        if row.poc_canonical:
            violations.append(f"poc_assumed_locked:{row.id}")
        if row.status == "locked" and row.id != "engine-godot-463-dotnet":
            if not row.operational_confirmed or not row.raw.get("interop_receipt_id"):
                violations.append(f"locked_without_interop:{row.id}")

    if manifest.operator_stack_baseline_vetted:
        pending = [
            r.id
            for r in manifest.baseline_required_rows()
            if not r.operational_confirmed or r.row_kind in ROW_KINDS_SKELETON
        ]
        if pending:
            violations.append(f"stack_vetted_but_rows_pending:{pending}")

    # Surface seat honesty — factory_ship_valid cannot be true without surface pass green
    manifest_path = manifest.path
    try:
        import yaml  # type: ignore[import-untyped]

        raw = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        if isinstance(raw, dict):
            if raw.get("factory_ship_valid") is True:
                from .surface_pass import run_surface_pass

                surface = run_surface_pass(vault_root)
                if not surface.ok:
                    violations.append("factory_ship_valid_true_while_surface_fail")
            if raw.get("operator_closed_alpha_vetted") and raw.get("factory_ship_valid") is not False:
                if raw.get("surface_pass_required"):
                    violations.append("closed_alpha_vetted_without_factory_ship_valid_false")
    except Exception:  # noqa: BLE001
        pass

    return violations


def check_honesty_invariants(manifest: TechStackManifest) -> list[str]:
    """Anti-patterns independent of registry file."""
    violations: list[str] = []
    for row in manifest.rows:
        if row.row_kind in ROW_KINDS_SKELETON and row.operational_confirmed:
            violations.append(f"skeleton_marked_operational:{row.id}")
        if row.poc_canonical:
            violations.append(f"poc_assumed_locked:{row.id}")
    return violations
