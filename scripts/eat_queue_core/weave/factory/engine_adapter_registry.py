"""Engine adapter resolve — from project bindings/engine.yaml + lanes.yaml only.

No baked lane→adapter map and no silent vault_only fallback for forgotten lanes.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .bindings import BindingMissingError, load_family, require_project_id


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


def adapter_for_lane(
    lane_id: str,
    *,
    vault_root: Path | None = None,
    project_id: str | None = None,
) -> AdapterSpec:
    """Resolve adapter for a lane from bindings. Missing engine/lanes raises."""
    lid = lane_id.strip().lower()
    if vault_root is None or not str(project_id or "").strip():
        raise BindingMissingError(
            "binding_missing",
            "adapter_for_lane:project_id_and_vault_required",
        )
    pid = require_project_id(project_id)
    engine = load_family(vault_root, pid, "engine")
    lanes = load_family(vault_root, pid, "lanes")

    lane_adapters = lanes.get("lane_adapters")
    if not isinstance(lane_adapters, dict):
        lane_adapters = {}
    adapter_id = str(lane_adapters.get(lid) or engine.get("adapter_id") or "").strip()
    if not adapter_id:
        raise BindingMissingError(
            "binding_missing",
            f"adapter_for_lane:no_adapter:{lid}",
        )

    ports = engine.get("ports")
    if not isinstance(ports, dict):
        ports = {}
    port_raw = ports.get(adapter_id)
    port = int(port_raw) if port_raw is not None and str(port_raw).strip() != "" else None

    flags = engine.get("adapter_flags")
    if not isinstance(flags, dict):
        flags = {}
    af = flags.get(adapter_id) if isinstance(flags.get(adapter_id), dict) else {}

    return AdapterSpec(
        adapter_id=adapter_id,
        mcp_port=port,
        requires_mcp=bool(af.get("requires_mcp")),
        run_dotnet_build=bool(af.get("run_dotnet_build")),
        run_godot_smoke=bool(af.get("run_engine_smoke")),
    )
