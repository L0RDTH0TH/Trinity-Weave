"""Half B overnight wave satisfaction — release-plan active_wave_complete.

Legacy depth-budget stop remains in factory_levels.py until release_plan_feed flips.
"""

from __future__ import annotations

from pathlib import Path

from ..user_story.release_plan import active_wave_complete, factory_wave_satisfied

__all__ = ["active_wave_complete", "factory_wave_satisfied", "factory_levels_satisfied_compat"]


def factory_levels_satisfied_compat(vault_root: Path, project_id: str) -> tuple[bool, str]:
    """Prefer wave exit when release_plan_feed is on; else legacy budget levels."""
    from ..user_story.release_plan import release_plan_feed_enabled
    from .factory_levels import factory_levels_satisfied

    if release_plan_feed_enabled(vault_root, project_id):
        return active_wave_complete(vault_root, project_id)
    return factory_levels_satisfied(vault_root, project_id)
