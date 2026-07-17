"""Engine adapter registry — per-lane factory agent tooling (Exhibit A Phase 3)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

LANE_ADAPTER: dict[str, str] = {
    "asset": "blender_mcp",
    "techart": "godot_4_6_3_dotnet",
    "content": "vault_only",
    "presentation": "godot_4_6_3_dotnet",
    "audio": "vault_only",
    "module": "godot_4_6_3_dotnet",
}

ADAPTER_PORTS: dict[str, int | None] = {
    "blender_mcp": 9876,
    "godot_4_6_3_dotnet": 6505,
    "vault_only": None,
}


@dataclass(frozen=True)
class AdapterSpec:
    adapter_id: str
    mcp_port: int | None
    requires_mcp: bool
    run_dotnet_build: bool
    run_godot_smoke: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "mcp_port": self.mcp_port,
            "requires_mcp": self.requires_mcp,
            "run_dotnet_build": self.run_dotnet_build,
            "run_godot_smoke": self.run_godot_smoke,
        }


def adapter_for_lane(lane_id: str) -> AdapterSpec:
    lane_id = lane_id.strip().lower()
    adapter_id = LANE_ADAPTER.get(lane_id, "vault_only")
    port = ADAPTER_PORTS.get(adapter_id)
    return AdapterSpec(
        adapter_id=adapter_id,
        mcp_port=port,
        requires_mcp=adapter_id in ("blender_mcp", "godot_4_6_3_dotnet"),
        run_dotnet_build=adapter_id == "godot_4_6_3_dotnet",
        run_godot_smoke=adapter_id == "godot_4_6_3_dotnet" and lane_id in ("module", "presentation"),
    )
