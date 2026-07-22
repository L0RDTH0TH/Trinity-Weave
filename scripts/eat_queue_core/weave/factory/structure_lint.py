"""Oak structure_pass — FACTORY_ZONES write boundary lint (topology only)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .factory_little_val import FactoryLittleValResult

DEFAULT_ZONES_REL = "1-Projects/genesis-mythos-master/Factory-DRB/FACTORY_ZONES.yaml"
MANIFEST_REL = "1-Projects/genesis-mythos-master/Factory-DRB/Tech-Stack-Manifest-v1.yaml"


@dataclass(frozen=True)
class StructurePassResult:
    ok: bool
    little_val: FactoryLittleValResult
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "detail": self.detail,
            "violations": list(self.little_val.anti_pattern_violations),
        }


def _game_repo(vault_root: Path) -> Path:
    manifest = vault_root / MANIFEST_REL
    rel = "5-Attachments/Code-Repos/genesis-mythos-demo"
    if manifest.is_file():
        data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        if isinstance(data, dict) and data.get("game_repo_path"):
            rel = str(data["game_repo_path"])
    return vault_root / rel


def _load_zones(vault_root: Path) -> dict[str, Any]:
    path = vault_root / DEFAULT_ZONES_REL
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def _glob_match(rel_posix: str, pattern: str) -> bool:
    from fnmatch import fnmatch

    if pattern.startswith("!"):
        return False
    norm = rel_posix.replace("\\", "/")
    if fnmatch(norm, pattern):
        return True
    # simple ** support
    if "**" in pattern:
        prefix = pattern.split("**")[0].rstrip("/")
        if prefix and norm.startswith(prefix):
            return True
    return fnmatch(norm, pattern)


def _in_zone(rel_posix: str, write_patterns: list[str]) -> bool:
    excluded = [p[1:] for p in write_patterns if p.startswith("!")]
    for ex in excluded:
        if _glob_match(rel_posix, ex):
            return False
    return any(_glob_match(rel_posix, p) for p in write_patterns if not p.startswith("!"))


def path_matches_zone_write(rel_posix: str, zone_write: list[str]) -> bool:
    """True when rel_posix matches any lane zone_write glob."""
    if not zone_write:
        return False
    return _in_zone(rel_posix.replace("\\", "/"), zone_write)


def filter_paths_to_zone_write(
    paths: set[str] | tuple[str, ...] | list[str],
    zone_write: list[str],
) -> tuple[str, ...]:
    """Keep only repo-relative paths that fall inside zone_write patterns."""
    if not zone_write:
        return tuple(sorted(set(paths)))
    kept = {p for p in paths if path_matches_zone_write(p, zone_write)}
    return tuple(sorted(kept))


def run_structure_pass(
    vault_root: Path,
    *,
    changed_paths: tuple[str, ...] | None = None,
) -> StructurePassResult:
    """
    Topology lint — paths must land in declared factory zones.

    Default: validate zones file + critical Closed Alpha paths only (no full-repo orphan sweep).
    """
    violations: list[str] = []
    zones_doc = _load_zones(vault_root)
    if not zones_doc.get("zones"):
        violations.append("missing_factory_zones")
        lv = FactoryLittleValResult(False, violations, "structure_pass")
        return StructurePassResult(False, lv, "missing_factory_zones")

    zones: dict[str, Any] = zones_doc["zones"]
    repo = _game_repo(vault_root)
    if not repo.is_dir():
        violations.append("game_repo_missing")
        lv = FactoryLittleValResult(False, violations, "structure_pass")
        return StructurePassResult(False, lv, "game_repo_missing")

    if changed_paths is None:
        changed_paths = (
            "PlayRegion.tscn",
            "PlayRegion.cs",
            "LaunchShell.tscn",
            "LaunchShell.cs",
            "Player/PlayerFP.cs",
            "Camera/SparkyDmFreeCamRig.cs",
            "UI/GameHud.cs",
            "Core/ClosedAlpha/Q3StackCameraSync.cs",
            "assets/_factory/adc-closed-alpha-env-v1.json",
        )
    elif not changed_paths:
        ok = len(violations) == 0
        lv = FactoryLittleValResult(ok, violations, "structure_pass")
        return StructurePassResult(ok, lv, "structure_pass_no_paths")

    for rel in changed_paths:
        if rel.startswith("addons/"):
            continue
        owners = [zid for zid, spec in zones.items() if _in_zone(rel, list(spec.get("write") or []))]
        if len(owners) > 1:
            violations.append(f"cross_zone_ambiguous:{rel}:{owners}")
        elif len(owners) == 0:
            violations.append(f"orphan_path_no_zone:{rel}")

    ok = len(violations) == 0
    lv = FactoryLittleValResult(ok, violations, "structure_pass")
    detail = "; ".join(violations) if violations else "structure_pass_ok"
    return StructurePassResult(ok, lv, detail)
