"""Goal packet profile matrix — warehouse → factory → subfactory validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .conceptual_track_ready import conceptual_map_complete, roadmap_tree_complete
from .execution_track_ready import execution_map_complete
from .product_factory_state import FACTORY_STAGED, load_product_factory, normalize_completed_phases

WAREHOUSE_TOKENS = frozenset({"weave", "knowledge", "software"})
SUBFACTORY_BY_WAREHOUSE: dict[str, frozenset[str]] = {
    "weave": frozenset({"maintenance", "queue_bus"}),
    "knowledge": frozenset({"library", "museum"}),
    "software": frozenset({"half_a", "half_b", "re_bench"}),
}
SESSION_MODES = frozenset({"bootstrap", "resume", "remint", "deepen_only"})


@dataclass
class ProfileValidation:
    ok: bool
    warehouse: str = ""
    subfactory: str = ""
    session_mode: str = ""
    violations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "warehouse": self.warehouse,
            "subfactory": self.subfactory,
            "session_mode": self.session_mode,
            "violations": list(self.violations),
        }


def _infer_profile(packet: dict[str, Any]) -> tuple[str, str, str]:
    hints = packet.get("planner_hints") if isinstance(packet.get("planner_hints"), dict) else {}
    warehouse = str(hints.get("warehouse") or "").lower().strip()
    subfactory = str(hints.get("subfactory") or "").lower().strip()
    session = str(hints.get("session_mode") or "").lower().strip()

    if str(hints.get("effective_track") or "").lower() == "implementation":
        warehouse = warehouse or "software"
        subfactory = subfactory or "half_b"
    elif hints.get("product_factory") is True or str(hints.get("factory_profile") or "").lower() in (
        "half_a",
        "roadmap",
        "product_factory",
    ):
        warehouse = warehouse or "software"
        subfactory = subfactory or "half_a"

    if hints.get("ingest_batch") or hints.get("primary_mode") == "INGEST_MODE":
        warehouse = warehouse or "knowledge"
        subfactory = subfactory or "library"

    if hints.get("fresh_greenfield") and not session:
        session = "bootstrap"
    elif hints.get("resume_factory") and not session:
        session = "resume"
    elif hints.get("mint_batch") and not session:
        session = "remint"

    return warehouse, subfactory, session


def validate_goal_packet_profile(
    packet: dict[str, Any],
    vault_root: Path | None = None,
) -> ProfileValidation:
    violations: list[str] = []
    if not isinstance(packet, dict):
        return ProfileValidation(False, violations=["invalid_packet"])

    if packet.get("confirmed_by_operator") is not True:
        violations.append("confirmed_by_operator_required")

    pid = str(packet.get("project_id") or "").strip()
    if not pid:
        violations.append("project_id_required")

    warehouse, subfactory, session = _infer_profile(packet)

    if warehouse and warehouse not in WAREHOUSE_TOKENS:
        violations.append(f"unknown_warehouse:{warehouse}")

    if warehouse and subfactory:
        allowed = SUBFACTORY_BY_WAREHOUSE.get(warehouse, frozenset())
        if allowed and subfactory not in allowed:
            violations.append(f"subfactory_not_in_warehouse:{subfactory}:{warehouse}")

    if session and session not in SESSION_MODES:
        violations.append(f"unknown_session_mode:{session}")

    if vault_root and pid:
        vault_root = vault_root.resolve()
        hints = packet.get("planner_hints") if isinstance(packet.get("planner_hints"), dict) else {}

        if session == "remint" and hints.get("fresh_greenfield") is True:
            violations.append("deprecated_fresh_greenfield_on_remint")

        if subfactory == "half_b" or str(hints.get("effective_track") or "").lower() == "implementation":
            pf = load_product_factory(vault_root, pid)
            completed = normalize_completed_phases(list(pf.get("completed_phases") or []))
            if FACTORY_STAGED not in completed:
                exec_ok, exec_reason = execution_map_complete(vault_root, pid)
                if not exec_ok and exec_reason != "execution_track_missing":
                    violations.append(f"implementation_without_handoff:{exec_reason}")

        if session == "bootstrap" and roadmap_tree_complete(vault_root, pid):
            if hints.get("force_factory_bootstrap") is not True:
                violations.append("bootstrap_with_existing_tree_use_resume")

    ok = len(violations) == 0
    return ProfileValidation(
        ok=ok,
        warehouse=warehouse,
        subfactory=subfactory,
        session_mode=session,
        violations=violations,
    )
