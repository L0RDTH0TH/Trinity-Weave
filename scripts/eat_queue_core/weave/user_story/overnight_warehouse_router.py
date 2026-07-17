"""Overnight warehouse router — Weave engine dispatches by goal packet profile."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ...architect_pq_planner import implementation_track_active
from ..factory.factory_levels import implementation_factory_overnight
from .goal_packet_profile import ProfileValidation, validate_goal_packet_profile
from .product_factory_packet import product_factory_roadmap_packet


@dataclass(frozen=True)
class OvernightWarehouseContext:
    """Which overnight preflight rails apply for this goal packet."""

    profile: ProfileValidation
    warehouse: str
    subfactory: str
    session_mode: str
    run_factory_cursor: bool
    run_implementation_cursor: bool
    run_half_a_tick_preflight: bool
    run_half_b_factory_dispatch: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "warehouse": self.warehouse,
            "subfactory": self.subfactory,
            "session_mode": self.session_mode,
            "run_factory_cursor": self.run_factory_cursor,
            "run_implementation_cursor": self.run_implementation_cursor,
            "run_half_a_tick_preflight": self.run_half_a_tick_preflight,
            "run_half_b_factory_dispatch": self.run_half_b_factory_dispatch,
            "profile": self.profile.to_dict(),
        }


def resolve_overnight_warehouse(
    packet: dict[str, Any],
    vault_root: Path | None = None,
) -> OvernightWarehouseContext:
    """
    Route overnight preflight by warehouse → subfactory.

    Weave serves all warehouses; Software Half A/B rails must not run on Knowledge/Weave packets.
    """
    profile = validate_goal_packet_profile(packet, vault_root)
    warehouse = profile.warehouse or ""
    subfactory = profile.subfactory or ""
    session = profile.session_mode or ""

    if implementation_factory_overnight(packet):
        warehouse = warehouse or "software"
        subfactory = subfactory or "half_b"
    elif product_factory_roadmap_packet(packet):
        warehouse = warehouse or "software"
        subfactory = subfactory or "half_a"

    half_a = warehouse == "software" and subfactory == "half_a" and product_factory_roadmap_packet(packet)
    half_b = warehouse == "software" and (
        subfactory == "half_b" or implementation_factory_overnight(packet)
    )

    pid = str(packet.get("project_id") or "").strip()
    run_factory = bool(pid and half_a)
    run_impl = bool(pid and half_b)

    return OvernightWarehouseContext(
        profile=profile,
        warehouse=warehouse,
        subfactory=subfactory,
        session_mode=session,
        run_factory_cursor=run_factory,
        run_implementation_cursor=run_impl,
        run_half_a_tick_preflight=run_factory,
        run_half_b_factory_dispatch=half_b and implementation_track_active(packet),
    )
