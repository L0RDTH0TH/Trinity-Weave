"""Roadmap deepen traversal helpers (depth-first branch closure; not factory logic)."""

from .branch_depth import (
    branch_split_warrant,
    load_deepen_traversal_config,
    oversized_note_without_children,
    subphase_index_depth,
)
from .deepen_enqueue import merge_deepen_params, sticky_deepen_params
from .roadmap_path_resolver import (
    attach_deepen_path_hint,
    load_path_resolver_config,
    roadmap_path_for,
    scan_structural_path_violations,
)
from .roadmap_repath_organize import organize_roadmap_paths

__all__ = [
    "attach_deepen_path_hint",
    "branch_split_warrant",
    "load_deepen_traversal_config",
    "load_path_resolver_config",
    "merge_deepen_params",
    "organize_roadmap_paths",
    "oversized_note_without_children",
    "roadmap_path_for",
    "scan_structural_path_violations",
    "sticky_deepen_params",
    "subphase_index_depth",
]
