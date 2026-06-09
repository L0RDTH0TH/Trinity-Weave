"""Single live config — ``3-Resources/Second-Brain-Config.md`` (runtime source of truth)."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from .config_loader import (
    parse_decision_matrix_yaml,
    parse_parallel_execution_yaml,
    parse_queue_section_yaml,
)
from .gitforge_config import merge_yaml_blocks_from_config

LIVE_CONFIG_REL = "3-Resources/Second-Brain-Config.md"
REFERENCE_CONFIG_REL = "3-Resources/Second-Brain/Docs/Core/Second-Brain-Config.md"


def live_config_path(vault_root: Path) -> Path:
    return (vault_root / LIVE_CONFIG_REL).resolve()


def reference_config_path(vault_root: Path) -> Path:
    return (vault_root / REFERENCE_CONFIG_REL).resolve()


def _deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(base)
    for k, v in overlay.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)  # type: ignore[arg-type]
        else:
            out[k] = v
    return out


def load_live_config(
    vault_root: Path,
    *,
    config_path: Path | None = None,
    fill_missing_from_reference: bool = False,
) -> dict[str, Any]:
    """
    Load machine-readable config from the live file.

    Merge order: fenced ```yaml``` blocks, then plain top-level sections (plain wins).
    """
    path = config_path if config_path is not None else live_config_path(vault_root)
    if not path.is_file():
        return {}
    fenced = merge_yaml_blocks_from_config(path)
    plain_q = parse_queue_section_yaml(path)
    plain_dm = parse_decision_matrix_yaml(path)
    plain_pe = parse_parallel_execution_yaml(path)
    merged: dict[str, Any] = dict(fenced)
    if plain_q:
        q_existing = merged.get("queue")
        if isinstance(q_existing, dict):
            merged["queue"] = _deep_merge(q_existing, plain_q)
        else:
            merged["queue"] = dict(plain_q)
    if plain_dm:
        dm_existing = merged.get("decision_matrix")
        if isinstance(dm_existing, dict):
            merged["decision_matrix"] = _deep_merge(dm_existing, plain_dm)
        else:
            merged["decision_matrix"] = dict(plain_dm)
    if plain_pe:
        pe_existing = merged.get("parallel_execution")
        if isinstance(pe_existing, dict):
            merged["parallel_execution"] = _deep_merge(pe_existing, plain_pe)
        else:
            merged["parallel_execution"] = dict(plain_pe)
    if fill_missing_from_reference:
        ref_p = reference_config_path(vault_root)
        if ref_p.is_file() and ref_p.resolve() != path.resolve():
            ref_blocks = merge_yaml_blocks_from_config(ref_p)
            for k, v in ref_blocks.items():
                if k not in merged:
                    merged[k] = v
    return merged


def live_queue_section(
    vault_root: Path, *, config_path: Path | None = None
) -> dict[str, Any]:
    q = load_live_config(vault_root, config_path=config_path).get("queue")
    return q if isinstance(q, dict) else {}


def live_parallel_execution(
    vault_root: Path, *, config_path: Path | None = None
) -> dict[str, Any]:
    pe = load_live_config(vault_root, config_path=config_path).get("parallel_execution")
    return pe if isinstance(pe, dict) else {}


def live_decision_matrix_block(
    vault_root: Path, *, config_path: Path | None = None
) -> dict[str, Any]:
    dm = load_live_config(vault_root, config_path=config_path).get("decision_matrix")
    return dm if isinstance(dm, dict) else {}
