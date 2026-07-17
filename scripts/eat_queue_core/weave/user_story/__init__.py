"""User-story track — vault roadmap feed into implementation factory."""

from .beat_auto_generate import run_beat_auto_generate
from .catalog_amendment import apply_catalog_amendment, build_execution_gap_queue_line
from .catalog_coverage import run_catalog_coverage, run_catalog_freeze_gate
from .depth_bump import bump_row_current_depth, try_weld_depth_bump_after_slice
from .rollout_slicer import run_rollout_slicer
from .work_order_translate import (
    FEED_VAULT_ROADMAP,
    VaultWorkOrderBundle,
    resolve_feed_authority,
    translate_vault_work_orders,
)

__all__ = [
    "FEED_VAULT_ROADMAP",
    "VaultWorkOrderBundle",
    "apply_catalog_amendment",
    "build_execution_gap_queue_line",
    "bump_row_current_depth",
    "resolve_feed_authority",
    "run_beat_auto_generate",
    "run_catalog_coverage",
    "run_catalog_freeze_gate",
    "run_rollout_slicer",
    "translate_vault_work_orders",
    "try_weld_depth_bump_after_slice",
]
