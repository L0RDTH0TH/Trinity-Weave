"""Factory dispatch preflight — fail-closed before first lane agent.

Hard-fails dispatch / eat when:
1. Armed required paths ⊈ union(lane zone_write ∪ FACTORY_ZONES write)
2. project_id / game_repo_path / drb_ref identity drift
3. Slice checklist is shell-era while Prefer overlay says worldgen authorship

Host law: proxies (budgets, file existence) do not override this gate.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .prefer_authorship_contract import (
    load_armed_packet,
    slice_requires_prefer_authorship,
)
from .project_identity import (
    CANONICAL_PROJECT_ID,
    LEGACY_STRANDED_PROJECT_ID,
    check_identity_consistency,
)
from .structure_lint import DEFAULT_ZONES_REL, path_matches_zone_write, _in_zone

# Shell-era kinesthetic bars — wrong identity for Prefer worldgen authorship.
SHELL_ERA_CHECKLIST_IDS: frozenset[str] = frozenset(
    {
        "Nav_LookWhileMove_FP",
        "Nav_LookWhileMove_DM",
        "Flow_Launch",
        "Flow_DM_Mode",
        "Flow_Ortho_Tabletop",
        "Flow_Chargen",
        "Flow_Seats",
        "Flow_Tricam",
    }
)

# Allowed under worldgen Prefer (narrow presentation anti-leak only).
WORLDGEN_ALLOWED_CHECKLIST_IDS: frozenset[str] = frozenset(
    {
        "Anti_DevOnlyHUD",
    }
)


@dataclass(frozen=True)
class DispatchPreflightResult:
    ok: bool
    violations: tuple[str, ...]
    detail: str
    fail_closed: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "violations": list(self.violations),
            "detail": self.detail,
            "fail_closed": self.fail_closed,
            "gate": "factory_dispatch_preflight",
        }


def _load_zones(vault_root: Path, project_id: str | None = None) -> dict[str, Any]:
    candidates = [
        vault_root / DEFAULT_ZONES_REL,
    ]
    if project_id:
        candidates.insert(
            0,
            vault_root / f"1-Projects/{project_id}/Factory-DRB/FACTORY_ZONES.yaml",
        )
    for path in candidates:
        if path.is_file():
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            return data if isinstance(data, dict) else {}
    return {}


def union_owned_write_patterns(
    vault_root: Path,
    *,
    zone_write: list[str] | None = None,
    project_id: str | None = None,
) -> list[str]:
    """Union of lane zone_write + all FACTORY_ZONES write patterns."""
    patterns: list[str] = []
    for z in zone_write or []:
        if z and str(z) not in patterns:
            patterns.append(str(z))
    zones_doc = _load_zones(vault_root, project_id)
    zones = zones_doc.get("zones") if isinstance(zones_doc.get("zones"), dict) else {}
    for _zid, spec in zones.items():
        if not isinstance(spec, dict):
            continue
        for p in spec.get("write") or []:
            if p and str(p) not in patterns:
                patterns.append(str(p))
    return patterns


def res_path_to_repo_rel(res_path: str) -> str | None:
    """res://scenes/WorldgenCraft.tscn → scenes/WorldgenCraft.tscn"""
    s = str(res_path or "").strip()
    if s.startswith("res://"):
        return s[len("res://") :]
    if s and not s.startswith("/") and "://" not in s:
        return s.lstrip("./")
    return None


def extract_armed_required_paths(armed: dict[str, Any]) -> list[str]:
    """Paths the Prefer weld must own before lane agent runs."""
    out: list[str] = []
    scene = res_path_to_repo_rel(str(armed.get("worldgen_entry_scene") or ""))
    if scene:
        out.append(scene)

    terrain = armed.get("terrain3d_prep") if isinstance(armed.get("terrain3d_prep"), dict) else {}
    feed = armed.get("terrain3d_feed") if isinstance(armed.get("terrain3d_feed"), dict) else {}
    if terrain.get("live_addon_present") or feed.get("vendor_already_on_disk"):
        out.append("addons/terrain_3d/")
    first = str(terrain.get("first_weld_action") or "")
    if "addons/terrain_3d" in first:
        out.append("addons/terrain_3d/")

    zone_own = armed.get("zone_ownership")
    if isinstance(zone_own, dict):
        for _lane, paths in zone_own.items():
            if isinstance(paths, list):
                for p in paths:
                    if p:
                        out.append(str(p).rstrip("*").rstrip("/") + ("/" if str(p).endswith("**") or str(p).endswith("/") else ""))
                        # Keep glob as-is for matching
                        out.append(str(p))

    # Dedupe preserving order
    seen: set[str] = set()
    uniq: list[str] = []
    for p in out:
        norm = p.replace("\\", "/")
        if norm not in seen:
            seen.add(norm)
            uniq.append(norm)
    return uniq


def path_owned_by_union(rel_posix: str, patterns: list[str]) -> bool:
    """True when path or its prefix matches any write pattern in the union."""
    norm = rel_posix.replace("\\", "/").lstrip("./")
    if not patterns:
        return False
    if path_matches_zone_write(norm, patterns):
        return True
    # Directory markers (addons/terrain_3d/) — match as prefix of zone globs.
    stripped = norm.rstrip("/")
    for pat in patterns:
        p = str(pat).replace("\\", "/")
        if p.startswith("!"):
            continue
        base = p.split("**")[0].rstrip("/")
        if base and (stripped == base or stripped.startswith(base + "/") or base.startswith(stripped)):
            return True
        if path_matches_zone_write(stripped + "/dummy", [p]) or path_matches_zone_write(
            stripped, [p]
        ):
            return True
    return _in_zone(norm, patterns) if patterns else False


def check_armed_paths_owned(
    vault_root: Path,
    *,
    job: dict[str, Any],
    zone_write: list[str] | None = None,
    project_id: str | None = None,
) -> list[str]:
    armed = load_armed_packet(vault_root, job)
    if not armed:
        # Also accept inline armed paths on job.
        inline = job.get("armed_required_paths") or []
        if not inline:
            return []
        required = [str(x) for x in inline if x]
    else:
        required = extract_armed_required_paths(armed)
    if not required:
        return []

    zw = zone_write if zone_write is not None else [str(z) for z in (job.get("zone_write") or []) if z]
    patterns = union_owned_write_patterns(
        vault_root, zone_write=zw, project_id=project_id or str(job.get("project_id") or "")
    )
    violations: list[str] = []
    for rel in required:
        # Skip pure globs from zone_ownership that are themselves patterns.
        if "*" in rel and not rel.endswith("/"):
            # Glob must appear in union patterns (ownership declared).
            if rel not in patterns and not any(
                path_matches_zone_write(rel.replace("**", "x").replace("*", "x"), [p])
                or p == rel
                for p in patterns
            ):
                # If the glob itself is a zone pattern entry, ok when present in FACTORY_ZONES.
                if rel not in patterns:
                    # Treat as owned when any zone pattern equals or covers it.
                    covered = any(
                        p.rstrip("/") == rel.rstrip("/")
                        or p.startswith(rel.rstrip("*").rstrip("/"))
                        or rel.startswith(p.rstrip("*").rstrip("/"))
                        for p in patterns
                        if not str(p).startswith("!")
                    )
                    if not covered:
                        violations.append(f"armed_path_unowned:{rel}")
            continue
        if not path_owned_by_union(rel, patterns):
            violations.append(f"armed_path_unowned:{rel}")
    return violations


def check_identity_drift(
    vault_root: Path,
    *,
    job: dict[str, Any],
    project_id: str | None = None,
    game_repo_rel: str | None = None,
) -> list[str]:
    """Detect godot-genesis-mythos-master vs genesis-mythos-master and path drift."""
    violations: list[str] = []
    pid = str(project_id or job.get("project_id") or "").strip()
    if pid == LEGACY_STRANDED_PROJECT_ID:
        violations.append(
            f"identity_drift:project_id_legacy_stranded:{LEGACY_STRANDED_PROJECT_ID}"
            f"_expected:{CANONICAL_PROJECT_ID}"
        )

    consistency = check_identity_consistency(vault_root)
    cfg_pid = str(consistency.get("project_id") or "")
    if pid and cfg_pid and pid != cfg_pid:
        # Allow explicit job override only when both are non-legacy and dirs exist —
        # still flag mixed legacy/canonical.
        if LEGACY_STRANDED_PROJECT_ID in (pid, cfg_pid):
            violations.append(f"identity_drift:job_vs_config:{pid}!={cfg_pid}")
        elif pid != cfg_pid:
            violations.append(f"identity_drift:job_vs_config:{pid}!={cfg_pid}")

    if not consistency.get("ok"):
        for issue in consistency.get("issues") or []:
            violations.append(f"identity_consistency:{issue}")

    drb_ref = str(job.get("drb_ref") or "")
    if LEGACY_STRANDED_PROJECT_ID in drb_ref:
        violations.append(f"identity_drift:drb_ref_legacy:{drb_ref}")

    repo = str(game_repo_rel or job.get("game_repo_rel") or job.get("repo_path") or "")
    zones = _load_zones(vault_root, pid or cfg_pid or None)
    expected = str(zones.get("game_repo_path") or "")
    if expected and repo:
        norm_repo = repo.strip("/").rstrip("/")
        norm_exp = expected.strip("/").rstrip("/")
        if norm_repo and norm_exp and norm_repo != norm_exp:
            # Allow suffix match (trailing slash / exhibit nesting).
            if not (
                norm_repo.endswith(norm_exp)
                or norm_exp.endswith(norm_repo)
                or norm_exp in norm_repo
                or norm_repo in norm_exp
            ):
                violations.append(
                    f"identity_drift:game_repo_path:{norm_repo}!={norm_exp}"
                )

    return violations


def check_shell_era_checklist_vs_worldgen(
    *,
    slice_id: str,
    job: dict[str, Any],
    checklist_ids: list[str] | None = None,
) -> list[str]:
    """Fail when Prefer worldgen authorship still carries shell-era Nav/Flow seats."""
    if not slice_requires_prefer_authorship(slice_id, job):
        return []
    ids = checklist_ids
    if ids is None:
        ids = [str(x) for x in (job.get("checklist_ids") or []) if x]
    violations: list[str] = []
    for cid in ids:
        if cid in SHELL_ERA_CHECKLIST_IDS and cid not in WORLDGEN_ALLOWED_CHECKLIST_IDS:
            violations.append(f"shell_era_checklist_on_worldgen_prefer:{cid}")
    return violations


def run_factory_dispatch_preflight(
    vault_root: Path,
    *,
    job: dict[str, Any] | None = None,
    project_id: str | None = None,
    game_repo_rel: str | None = None,
    zone_write: list[str] | None = None,
    checklist_ids: list[str] | None = None,
    skip_armed_path_check: bool = False,
) -> DispatchPreflightResult:
    """
    Fail-closed preflight before first lane agent / PQ stage.

    Returns ok=False with machine-readable violations; callers must not dispatch.
    """
    vault_root = vault_root.resolve()
    job = dict(job or {})
    slice_id = str(job.get("slice_id") or "")
    pid = str(project_id or job.get("project_id") or "").strip()
    zw = zone_write if zone_write is not None else [
        str(z) for z in (job.get("zone_write") or []) if z
    ]

    violations: list[str] = []
    violations.extend(
        check_identity_drift(
            vault_root, job=job, project_id=pid or None, game_repo_rel=game_repo_rel
        )
    )
    if not skip_armed_path_check and (
        job.get("armed_packet_path") or job.get("armed_required_paths")
    ):
        violations.extend(
            check_armed_paths_owned(
                vault_root, job=job, zone_write=zw, project_id=pid or None
            )
        )
    violations.extend(
        check_shell_era_checklist_vs_worldgen(
            slice_id=slice_id, job=job, checklist_ids=checklist_ids
        )
    )

    ok = len(violations) == 0
    detail = "; ".join(violations) if violations else "factory_dispatch_preflight_ok"
    return DispatchPreflightResult(ok=ok, violations=tuple(violations), detail=detail)
