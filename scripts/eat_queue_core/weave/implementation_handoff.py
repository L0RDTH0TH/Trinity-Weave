"""Half B handoff — Prefer success + behavior_keys only; no method invent."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .persona_handoff import format_persona_block, merge_persona_into_params


def _load_armed_from_params(
    vault_root: Path, params: dict[str, Any]
) -> dict[str, Any]:
    rel = str(params.get("armed_packet_path") or "").strip()
    if not rel:
        return {}
    path = vault_root / rel
    if not path.is_file():
        return {}
    try:
        import yaml

        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def _behavior_keys_from_armed(armed: dict[str, Any]) -> list[str]:
    """Sole source: Prefer packet behavior_keys. Do not invent."""
    raw = armed.get("behavior_keys")
    if not isinstance(raw, list):
        return []
    return [str(x).strip() for x in raw if str(x).strip()]


def _success_from_armed(armed: dict[str, Any], params: dict[str, Any]) -> str:
    for key in ("structural_success", "success", "prefer_success", "done_when"):
        val = armed.get(key)
        if val and str(val).strip():
            return str(val).strip()
    return str(params.get("user_guidance") or "").strip()


def _refuses_from_armed(armed: dict[str, Any]) -> list[str]:
    for key in ("do_not_waive", "refuse", "refuses"):
        raw = armed.get(key)
        if isinstance(raw, list):
            return [str(x).strip() for x in raw if str(x).strip()]
    return []


def build_implementation_handoff(
    vault_root: Path,
    *,
    lane: str,
    entry: dict[str, Any],
    charter: dict[str, Any],
    goal_packet: dict[str, Any] | None,
) -> str:
    """Handoff body = success + behavior_keys from armed Prefer. No method."""
    del goal_packet, charter
    vault_root = vault_root.resolve()
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    armed = _load_armed_from_params(vault_root, params)
    keys = _behavior_keys_from_armed(armed)
    success = _success_from_armed(armed, params) or "(Prefer success unset)"
    refuses = _refuses_from_armed(armed)
    keys_block = (
        "\n".join(f"- `{k}`" for k in keys) if keys else "- (Prefer behavior_keys empty)"
    )
    refuse_block = (
        "\n".join(f"- `{r}`" for r in refuses) if refuses else "- (none)"
    )
    persona_params = merge_persona_into_params(dict(params))
    persona_block = format_persona_block(
        persona_params.get("persona_handoff")
        if isinstance(persona_params.get("persona_handoff"), dict)
        else {}
    )
    seat = str(lane or "implementation").strip() or "implementation"
    return (
        f"{persona_block}"
        f"You are the **Implementation** seat (Half B).\n\n"
        f"Vault root: `{vault_root}`\n"
        f"Seat: `{seat}`\n\n"
        f"## Success (Prefer)\n{success}\n\n"
        f"## Behavior keys (must hold)\n{keys_block}\n\n"
        f"## Refuse / do_not_waive\n{refuse_block}\n\n"
        f"## Constraints\n"
        f"- Choose any reasonable **how**. The harness does not prescribe method, "
        f"engine, scene, or folder layout.\n"
        f"- Do **not** edit `.cursor/rules/**`\n"
        f"- Build only if `engine.yaml` `build_command` is non-empty\n\n"
        f"## Finish\n"
        f"Evidence that each behavior key holds. No method stamp required.\n"
    )


def build_factory_lane_handoff(
    vault_root: Path,
    *,
    lane: str,
    entry: dict[str, Any],
    goal_packet: dict[str, Any] | None,
) -> str:
    """Same keys-only handoff for factory_lane entries."""
    return build_implementation_handoff(
        vault_root,
        lane=lane,
        entry=entry,
        charter={},
        goal_packet=goal_packet,
    )
