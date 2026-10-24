"""Prefer-align — fail-closed gate before the implementation seat.

Writes nothing. Prefer is source of truth. Incomplete Prefers return to Ticketment.
No product nouns in this module (denylist-safe).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class PreferAlignResult:
    ok: bool
    violations: tuple[str, ...]
    detail: str
    # In-memory context only — never written to vault files.
    context: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "violations": list(self.violations),
            "detail": self.detail,
            "context": dict(self.context),
            "gate": "prefer_align",
        }


def _truthy(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, str) and value.strip().lower() in {"true", "1", "yes"}:
        return True
    return False


def _host_law_ids(armed: dict[str, Any]) -> list[str]:
    raw = armed.get("host_law_ids")
    if not isinstance(raw, list):
        return []
    return [str(x).strip() for x in raw if str(x).strip()]


def _behavior_keys(armed: dict[str, Any]) -> list[str]:
    raw = armed.get("behavior_keys")
    if not isinstance(raw, list):
        return []
    return [str(x).strip() for x in raw if str(x).strip()]


def _prefer_named_entries(armed: dict[str, Any]) -> set[str]:
    """Entries Prefer explicitly named (allowed_entries + single entry fields)."""
    named: set[str] = set()
    for key in ("allowed_entries", "named_entries", "entry_ids"):
        raw = armed.get(key)
        if isinstance(raw, list):
            named.update(str(x).strip() for x in raw if str(x).strip())
    for key in ("launch_scene", "entry_scene", "main_scene"):
        val = str(armed.get(key) or "").strip()
        if val:
            named.add(val)
    return named


def _collect_cite_strings(armed: dict[str, Any]) -> list[str]:
    """Any cite field on the packet, including nested locks.*.law_cite and prefer_law."""
    cites: list[str] = []

    def walk(obj: Any, path: str = "") -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                kk = str(k)
                p = f"{path}.{kk}" if path else kk
                if kk in {"law_cite", "cite", "prefer_law", "vault_cite"} and v not in (
                    None,
                    "",
                ):
                    cites.append(str(v).strip())
                else:
                    walk(v, p)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                walk(item, f"{path}[{i}]")

    walk(armed)
    # Top-level prefer_law may be a short name still counting as a cite when host_law_ids empty.
    pl = armed.get("prefer_law")
    if pl not in (None, "") and str(pl).strip() not in cites:
        cites.append(str(pl).strip())
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    if isinstance(locks, dict) and locks.get("prefer_law") not in (None, ""):
        s = str(locks["prefer_law"]).strip()
        if s and s not in cites:
            cites.append(s)
    return [c for c in cites if c]


def _topology_armed(armed: dict[str, Any]) -> bool:
    """Only topology_law: true. Refuse names containing dual are not a topology arm."""
    if _truthy(armed.get("topology_law")):
        return True
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    if _truthy(locks.get("topology_law")):
        return True
    return False


def _weave_track_opt_in(armed: dict[str, Any]) -> bool:
    """Explicit Prefer field only. Absent = not opted in."""
    for key in ("weave_track_opt_in", "require_weave_track", "opt_in_weave_track"):
        if key in armed:
            return _truthy(armed.get(key))
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    for key in ("weave_track_opt_in", "require_weave_track", "opt_in_weave_track"):
        if key in locks:
            return _truthy(locks.get(key))
    return False


def _load_factory_project_game_repo(vault_root: Path, project_id: str) -> str | None:
    """Return game_repo_path from factory-project.yaml if present, else None."""
    from .bindings import factory_drb_rel

    path = vault_root / factory_drb_rel(project_id, "factory-project.yaml")
    if not path.is_file():
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return None
    if not isinstance(data, dict):
        return None
    raw = data.get("game_repo_path")
    if raw in (None, ""):
        return None
    return str(raw).strip().strip("/")


def discover_write_target_entries(
    vault_root: Path, write_target: str | None
) -> list[str]:
    """List non-dot files under Prefer/identity write target (relative paths).

    No product nouns. Empty target → []. Caller passes this list as
    ``observed_entries`` so unnamed entries block when Prefer names none.
    """
    rel = str(write_target or "").strip().strip("/")
    if not rel:
        return []
    root = (vault_root / rel).resolve()
    vault = vault_root.resolve()
    try:
        root.relative_to(vault)
    except ValueError:
        return []
    if not root.is_dir():
        return []
    found: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        name = path.name
        if name.startswith("."):
            continue
        found.append(path.relative_to(root).as_posix())
    return found


def resolve_write_target_rel(
    vault_root: Path,
    *,
    armed: dict[str, Any] | None,
    project_id: str,
) -> str:
    """Prefer live_write_target, else identity game_repo_path. No silent heal."""
    armed = armed if isinstance(armed, dict) else {}
    live = str(armed.get("live_write_target") or "").strip().strip("/")
    if live:
        return live
    from .bindings import BindingMissingError, game_repo_path as bind_game_repo

    try:
        return str(bind_game_repo(vault_root, project_id) or "").strip().strip("/")
    except BindingMissingError:
        return ""


def run_prefer_align(
    vault_root: Path,
    *,
    armed: dict[str, Any] | None,
    project_id: str,
    observed_entries: list[str] | None = None,
    umbrella_slice_id: str | None = None,
    require_weave_track_coupled: bool | None = None,
) -> PreferAlignResult:
    """Fail-closed Prefer-align. Writes nothing to the vault."""
    vault_root = vault_root.resolve()
    violations: list[str] = []
    armed = armed if isinstance(armed, dict) else {}
    if not armed:
        return PreferAlignResult(
            False, ("prefer_align:armed_missing",), "prefer_align:armed_missing", {}
        )

    keys = _behavior_keys(armed)
    if not keys:
        violations.append("prefer_align:behavior_keys_empty")

    # Prefer must name a check per key — silence stays a fail.
    checks_raw = armed.get("behavior_key_checks")
    checks: dict[str, str] = {}
    if isinstance(checks_raw, dict):
        checks = {
            str(k).strip(): str(v).strip()
            for k, v in checks_raw.items()
            if str(k).strip() and str(v).strip()
        }
    if keys:
        if not checks:
            violations.append("prefer_align:behavior_key_checks_missing")
        else:
            missing = [k for k in keys if k not in checks]
            if missing:
                violations.append(
                    "prefer_align:behavior_key_checks_incomplete:"
                    + ",".join(missing[:8])
                )
            extras = sorted(set(checks) - set(keys))
            if extras:
                violations.append(
                    "prefer_align:behavior_key_checks_extra:"
                    + ",".join(extras[:8])
                )

    host_ids = _host_law_ids(armed)
    cites = _collect_cite_strings(armed)
    if cites and not host_ids:
        violations.append("prefer_align:host_law_cite_without_host_law_ids")

    if _topology_armed(armed) and not host_ids:
        # Topology arm without host_law opt-in is allowed only with topology_law;
        # host-law cites already covered. Topology alone does not require host_law_ids.
        # Spec: "A host-law cite or topology arm is present while host_law_ids is empty"
        # — topology arm WITH empty host_law_ids blocks? Re-read:
        # "A host-law cite or topology arm is present while host_law_ids is empty."
        # Yes — topology arm while host_law_ids empty blocks.
        violations.append("prefer_align:topology_arm_without_host_law_ids")

    # Wait - re-read again. "topology_law: true is the only topology arm"
    # And "A host-law cite or topology arm is present while host_law_ids is empty"
    # So topology_law true + empty host_law_ids = block. That seems harsh for contract
    # seats that want topology without host-law cites. User was explicit: block.
    # Keep it.

    named = _prefer_named_entries(armed)
    observed = [str(x).strip() for x in (observed_entries or []) if str(x).strip()]
    if not named and observed:
        violations.append("prefer_align:unnamed_entries_present")
    elif named:
        extras = sorted(set(observed) - named)
        if extras:
            violations.append(
                "prefer_align:entry_not_named_by_prefer:" + ",".join(extras[:8])
            )

    # Write target: Prefer live_write_target or identity only.
    from .bindings import BindingMissingError, game_repo_path as bind_game_repo

    try:
        identity_repo = bind_game_repo(vault_root, project_id)
    except BindingMissingError as exc:
        violations.append(f"prefer_align:identity_game_repo:{exc.detail}")
        identity_repo = ""

    live = str(armed.get("live_write_target") or "").strip().strip("/")
    write_target = live or identity_repo

    fp_repo = _load_factory_project_game_repo(vault_root, project_id)
    if fp_repo is not None and identity_repo and fp_repo != identity_repo:
        violations.append("prefer_align:factory_project_game_repo_disagree")
    if fp_repo is not None and live and fp_repo != live.strip("/"):
        # Prefer named live target; factory-project copy disagrees → block
        if fp_repo != live:
            violations.append("prefer_align:factory_project_game_repo_disagree_live")

    # Umbrella pointing at a different Prefer → block (do not delete yaml).
    armed_sid = str(armed.get("slice_id") or armed.get("armed_slice_id") or "").strip()
    umbrella = str(umbrella_slice_id or armed.get("umbrella_slice_id") or "").strip()
    if umbrella and armed_sid and umbrella != armed_sid:
        violations.append("prefer_align:umbrella_points_elsewhere")

    # Weave-track: project requires coupled AND Prefer did not opt in → block.
    # Do not flip require_weave_track_coupled at runtime.
    coupled = require_weave_track_coupled
    if coupled is None:
        # Read from factory-project bootstrap only for the check — do not write.
        from .bindings import factory_drb_rel

        fp = vault_root / factory_drb_rel(project_id, "factory-project.yaml")
        coupled = False
        if fp.is_file():
            try:
                data = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
            except (OSError, yaml.YAMLError):
                data = {}
            if isinstance(data, dict):
                boot = data.get("factory_bootstrap")
                if isinstance(boot, dict):
                    coupled = boot.get("require_weave_track_coupled") is True
    if coupled and not _weave_track_opt_in(armed):
        violations.append("prefer_align:weave_track_required_without_opt_in")

    ctx = {
        "write_target": write_target,
        "behavior_keys": keys,
        "behavior_key_checks": dict(checks),
        "host_law_ids": host_ids,
        "allowed_entries": sorted(named),
        "zone_ownership": armed.get("zone_ownership")
        if isinstance(armed.get("zone_ownership"), dict)
        else {},
    }
    ok = len(violations) == 0
    detail = "; ".join(violations) if violations else "prefer_align_ok"
    return PreferAlignResult(ok, tuple(violations), detail, ctx)
