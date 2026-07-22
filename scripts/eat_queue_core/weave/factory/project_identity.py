"""Factory project identity — config-driven, fail-closed (no silent slug defaults).

Closes the rename-propagation gap: when ``factory_orchestrator.project_id`` is
unset and no explicit ``project_id`` is passed, raise ``ProjectIdMissingError``
instead of falling back to a hardcoded legacy slug.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .factory_output_gate import parse_factory_orchestrator_yaml

PROJECT_ID_MISSING_MSG = (
    "project_id missing — set factory_orchestrator.project_id in "
    "3-Resources/Second-Brain-Config.md (or pass project_id explicitly)"
)

# Historical slug retained only for honesty / migration detection — never a default.
LEGACY_STRANDED_PROJECT_ID = "godot-genesis-mythos-master"
CANONICAL_PROJECT_ID = "genesis-mythos-master"

INERT_ROOT_PREFIXES: tuple[str, ...] = (
    "4-Archives/",
    ".trash/",
    ".backups/",
)


class ProjectIdMissingError(ValueError):
    """Raised when factory project_id cannot be resolved without a silent default."""

    def __init__(self, message: str = PROJECT_ID_MISSING_MSG) -> None:
        super().__init__(message)
        self.code = "project_id_missing"


def config_path(vault_root: Path) -> Path:
    return vault_root / "3-Resources/Second-Brain-Config.md"


def load_factory_orchestrator_cfg(vault_root: Path) -> dict[str, Any]:
    return parse_factory_orchestrator_yaml(config_path(vault_root))


def resolve_project_id(vault_root: Path, project_id: str | None = None) -> str:
    """
    Resolve project_id fail-closed.

    Order: explicit arg → factory_orchestrator.project_id → raise.
    Never returns a hardcoded legacy slug.
    """
    if project_id and str(project_id).strip():
        return str(project_id).strip()
    cfg = load_factory_orchestrator_cfg(vault_root)
    cfg_pid = cfg.get("project_id")
    if cfg_pid and str(cfg_pid).strip():
        return str(cfg_pid).strip()
    raise ProjectIdMissingError()


def check_identity_consistency(vault_root: Path) -> dict[str, Any]:
    """
    Honesty gate: config project_id, live 1-Projects/<id>/, and Factory-DRB
    must agree. Detects stranded legacy binding sites in factory_orchestrator paths.
    """
    vault_root = vault_root.resolve()
    issues: list[str] = []
    cfg = load_factory_orchestrator_cfg(vault_root)
    cfg_pid = str(cfg.get("project_id") or "").strip()
    if not cfg_pid:
        issues.append("config_project_id_missing")
        return {
            "ok": False,
            "project_id": "",
            "issues": issues,
            "gap": "rename_without_propagation_silent_default",
        }

    live_root = vault_root / "1-Projects" / cfg_pid
    if not live_root.is_dir():
        issues.append(f"live_project_dir_missing:1-Projects/{cfg_pid}")

    drb = live_root / "Factory-DRB"
    if not drb.is_dir():
        issues.append(f"factory_drb_missing:1-Projects/{cfg_pid}/Factory-DRB")

    # Path fields that must not still point at the stranded legacy slug.
    path_keys = (
        "manifest_path",
        "stack_domain_registry_path",
        "operator_feedback_path",
        "playtest_brief_dir",
    )
    for key in path_keys:
        val = str(cfg.get(key) or "")
        if LEGACY_STRANDED_PROJECT_ID in val:
            issues.append(f"stranded_legacy_path:{key}")

    roots = cfg.get("lane_charter_roots")
    if isinstance(roots, list):
        for i, root in enumerate(roots):
            if LEGACY_STRANDED_PROJECT_ID in str(root):
                issues.append(f"stranded_legacy_path:lane_charter_roots[{i}]")

    # Hardcoded defaults in source must not reintroduce the silent fallback.
    factory_project_py = (
        vault_root
        / "scripts/eat_queue_core/weave/factory/factory_project.py"
    )
    if factory_project_py.is_file():
        text = factory_project_py.read_text(encoding="utf-8")
        if f'DEFAULT_PROJECT_ID = "{LEGACY_STRANDED_PROJECT_ID}"' in text:
            issues.append("silent_default_still_present:factory_project.py")

    return {
        "ok": len(issues) == 0,
        "project_id": cfg_pid,
        "issues": issues,
        "gap_closed": "identity_fail_closed_no_silent_default",
        "failure_mode_documented": (
            "rename_without_propagation + silent DEFAULT_PROJECT_ID allowed "
            "factory harness to keep resolving a stranded slug while live "
            "roadmap used a new name; honesty detected stranding but nothing "
            "fail-closed when identity sites disagreed"
        ),
    }


def path_is_under_inert_root(rel_path: str) -> bool:
    """True when a vault-relative path is under an archive-inert root."""
    norm = rel_path.replace("\\", "/")
    while norm.startswith("./"):
        norm = norm[2:]
    return any(norm == p.rstrip("/") or norm.startswith(p) for p in INERT_ROOT_PREFIXES)
