"""UX mint series packs — primary walk parents (product_contract altitude only)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .catalog_io import project_root

SERIES_DIR_REL = Path("Templates/Roadmap/User-Story/UX-MINT-SERIES")
CORE_FILE = "UX-MINT-SERIES.core.yaml"
MANIFEST_FILE = "manifest.yaml"
PROJECT_OVERLAY = "UX-MINT-SERIES.project.yaml"

VALID_ALTITUDES = frozenset({"product_contract", "experience_texture", "scene_exemplar"})
SERIES_PARENT_ALTITUDE = "product_contract"


def series_template_dir(vault_root: Path) -> Path:
    return vault_root.resolve() / SERIES_DIR_REL


def series_project_overlay_path(vault_root: Path, project_id: str) -> Path:
    return project_root(vault_root, project_id) / "Roadmap" / "User-Story" / PROJECT_OVERLAY


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def load_ux_mint_series(vault_root: Path, project_id: str) -> dict[str, Any]:
    """
    Load series packs from Templates + optional project overlay.

    Returns {schema_version, packs: [pack dicts with members]}.
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    root = series_template_dir(vault_root)
    manifest = _load_yaml(root / MANIFEST_FILE)
    core = _load_yaml(root / CORE_FILE)
    packs_by_id: dict[str, dict[str, Any]] = {}
    for pack in core.get("series_packs") or []:
        if not isinstance(pack, dict):
            continue
        sid = str(pack.get("id") or "").strip()
        if sid:
            packs_by_id[sid] = dict(pack)

    enabled = [str(x) for x in (manifest.get("default_packs") or list(packs_by_id.keys()))]
    overlay: dict[str, Any] = {}
    if pid:
        overlay = _load_yaml(series_project_overlay_path(vault_root, pid))
    if overlay:
        if overlay.get("enabled_packs") is not None:
            enabled = [str(x) for x in overlay["enabled_packs"]]
        for d in overlay.get("disabled_packs") or []:
            ds = str(d)
            enabled = [e for e in enabled if e != ds]
        for pack in overlay.get("extra_packs") or []:
            if isinstance(pack, dict) and pack.get("id"):
                packs_by_id[str(pack["id"])] = dict(pack)
                if str(pack["id"]) not in enabled:
                    enabled.append(str(pack["id"]))
        # Member label/summary overrides: {pack_id: {role_key: {label, summary, ...}}}
        overrides = overlay.get("member_overrides") or {}
        if isinstance(overrides, dict):
            for pack_id, by_role in overrides.items():
                pack = packs_by_id.get(str(pack_id))
                if not pack or not isinstance(by_role, dict):
                    continue
                members = list(pack.get("members") or [])
                for i, mem in enumerate(members):
                    if not isinstance(mem, dict):
                        continue
                    rk = str(mem.get("role_key") or "")
                    ov = by_role.get(rk)
                    if isinstance(ov, dict):
                        merged = dict(mem)
                        merged.update(ov)
                        members[i] = merged
                pack["members"] = members

    ordered: list[dict[str, Any]] = []
    for sid in enabled:
        pack = packs_by_id.get(sid)
        if pack:
            ordered.append(pack)
    return {
        "schema_version": int(core.get("schema_version") or manifest.get("schema_version") or 1),
        "packs": ordered,
        "enabled_pack_ids": enabled,
    }


def expand_series_to_items(series_doc: dict[str, Any]) -> list[dict[str, Any]]:
    """Expand series pack members into backlog items (walk_tier series only)."""
    out: list[dict[str, Any]] = []
    for pack in series_doc.get("packs") or []:
        if not isinstance(pack, dict):
            continue
        series_id = str(pack.get("id") or "").strip()
        if not series_id:
            continue
        try:
            walk_rank = int(pack.get("walk_rank") or 0)
        except (TypeError, ValueError):
            walk_rank = 0
        members = [m for m in (pack.get("members") or []) if isinstance(m, dict)]
        for order, mem in enumerate(members):
            role = str(mem.get("role_key") or "").strip()
            if not role:
                continue
            altitude = str(mem.get("altitude") or SERIES_PARENT_ALTITUDE).strip()
            if altitude != SERIES_PARENT_ALTITUDE:
                # Wrong altitude cannot be a series parent — skip (caller may thickener elsewhere)
                continue
            label = str(mem.get("label") or role).strip()
            summary = str(mem.get("summary") or "").strip()
            seat = mem.get("seat") or ["shared_table"]
            if isinstance(seat, str):
                seat = [seat]
            seat_list = [str(s) for s in seat]
            # DM-facing privileged surfaces must still mark dm_as_player (fun in scope)
            if "privileged_access" in seat_list and "dm_as_player" not in seat_list:
                if "player" not in seat_list:
                    seat_list.append("dm_as_player")
            does_not = mem.get("does_not_mandate") or []
            if not isinstance(does_not, list):
                does_not = [str(does_not)]
            item_id = f"ux_{role}" if not role.startswith("ux_") else role
            out.append(
                {
                    "id": item_id,
                    "label": label[:120],
                    "dimension": str(mem.get("dimension") or "ui_surface"),
                    "ux_axis": str(mem.get("ux_axis") or "agency"),
                    "summary": summary[:600] or f"Series parent ({series_id}/{role}).",
                    "conceptual_pin": str(mem.get("conceptual_pin") or "needs pin"),
                    "derived_from": f"series:{series_id}:{role}",
                    "ux_family": series_id,
                    "status": "pending",
                    "catalog_face": str(mem.get("catalog_face") or "table"),
                    "experience_mode": role,
                    "mode_tier": "series",
                    "dnd_pillar": str(mem.get("pillar") or "shared"),
                    "feedstock_hit": False,
                    "pillar_notes": "",
                    "supplement": False,
                    "coverage_slot": False,
                    "walk_tier": "series",
                    "series_id": series_id,
                    "series_order": order,
                    "series_walk_rank": walk_rank,
                    "altitude": SERIES_PARENT_ALTITUDE,
                    "seat": seat_list,
                    "time_scale": str(mem.get("time_scale") or ""),
                    "does_not_mandate": [str(x) for x in does_not],
                    "alternatives_not_banned": [],
                    "maps_to": "",
                }
            )
    return out


def render_lens_audit_markdown(
    project_id: str,
    series_items: list[dict[str, Any]],
    *,
    generated_at: str = "",
) -> str:
    """Tutorial-shaped coverage companion — cites series ids; not catalog authority."""
    lines = [
        "---",
        f"title: MINT-LENS-AUDIT — {project_id}",
        f"project-id: {project_id}",
        "para-type: Project",
        "authority: audit_companion_not_catalog",
        f"generated_at: {generated_at}" if generated_at else "generated_at: ",
        "---",
        "",
        f"# MINT-LENS-AUDIT — `{project_id}`",
        "",
        "Tutorial / play-flow **coverage lens** over series parents. Cite-only — "
        "does not replace `slice-catalog.yaml` or invent walk nouns.",
        "",
        "## Lens reminders",
        "",
        "- **Altitude:** series parents must be `product_contract` (not scene/texture).",
        "- **Anti-mandate:** AP = skin; name alternatives not banned before freeze/done.",
        "- **DM seat:** privileged access OK; refuse DM-as-infrastructure; keep `dm_as_player` fun visible.",
        "- **Depth-spread (later):** same-width child batches per depth until diminishing returns.",
        "",
        "## Tutorial chapters (by series)",
        "",
    ]
    by_series: dict[str, list[dict[str, Any]]] = {}
    for it in series_items:
        sid = str(it.get("series_id") or "unknown")
        by_series.setdefault(sid, []).append(it)
    for sid, members in sorted(
        by_series.items(),
        key=lambda kv: (
            min((int(m.get("series_walk_rank") or 99) for m in kv[1]), default=99),
            kv[0],
        ),
    ):
        lines.append(f"### Series `{sid}`")
        lines.append("")
        for m in sorted(members, key=lambda x: int(x.get("series_order") or 0)):
            iid = m.get("id")
            label = m.get("label")
            seat = m.get("seat") or []
            lines.append(f"- [ ] `{iid}` — {label}")
            lines.append(f"  - seat: `{', '.join(seat) if isinstance(seat, list) else seat}`")
            lines.append(f"  - time_scale: `{m.get('time_scale') or ''}`")
            dnm = m.get("does_not_mandate") or []
            if dnm:
                lines.append(f"  - does_not_mandate: {dnm}")
        lines.append("")
    lines.append("## Gaps to watch at prune")
    lines.append("")
    lines.append("- Missing lifecycle segment (creation → end game)?")
    lines.append("- Continuity / downtime contract present?")
    lines.append("- World authorship / modability present?")
    lines.append("- Any series parent that reads as a single CR/BG scene caption?")
    lines.append("")
    return "\n".join(lines)


def write_lens_audit(
    vault_root: Path,
    project_id: str,
    series_items: list[dict[str, Any]],
    *,
    generated_at: str = "",
) -> Path:
    us = project_root(vault_root, project_id) / "Roadmap" / "User-Story"
    us.mkdir(parents=True, exist_ok=True)
    path = us / "MINT-LENS-AUDIT.md"
    path.write_text(
        render_lens_audit_markdown(project_id, series_items, generated_at=generated_at),
        encoding="utf-8",
    )
    return path
