"""Cross-project UX mint taxonomy — split core + domain packs + project overlay."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

import yaml

from .catalog_io import load_yaml, project_root, user_story_paths
from .catalog_mint_propose import _find_pmg_path

DEFAULT_PILLARS_DND = ("exploration", "combat", "roleplay")
TAXONOMY_DIR_REL = Path("Templates/Roadmap/User-Story/UX-MINT-TAXONOMY")
LEGACY_MONOLITH_REL = Path("Templates/Roadmap/User-Story/UX-MINT-TAXONOMY.yaml")

_CAMEL_API = re.compile(
    r"\b([A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)+)(Slot|Handle|Gate|Policy|Manifest|Controller|Rig)\b"
)
_PHASE_LABEL_RE = re.compile(r"^phase\s+[\d.]+", re.IGNORECASE)
_FM_PRODUCT_KIND = re.compile(r"^product_kind:\s*(\S+)\s*$", re.MULTILINE)


def taxonomy_dir(vault_root: Path) -> Path:
    return vault_root.resolve() / TAXONOMY_DIR_REL


def taxonomy_overlay_path(vault_root: Path, project_id: str) -> Path:
    return project_root(vault_root, project_id) / "Roadmap" / "User-Story" / "UX-MINT-TAXONOMY.overlay.yaml"


def taxonomy_project_profile_path(vault_root: Path, project_id: str) -> Path:
    return project_root(vault_root, project_id) / "Roadmap" / "User-Story" / "UX-MINT-TAXONOMY.project.yaml"


def _merge_slots(base: list[dict[str, Any]], extra: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for s in base:
        sid = str(s.get("id") or "").strip()
        if sid:
            by_id[sid] = dict(s)
    for s in extra:
        sid = str(s.get("id") or "").strip()
        if not sid:
            continue
        by_id[sid] = {**by_id.get(sid, {}), **s}
    return list(by_id.values())


def _load_yaml_dict(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = load_yaml(path)
    return data if isinstance(data, dict) else {}


def _resolve_domain_pack_ids(
    vault_root: Path,
    project_id: str,
    manifest: dict[str, Any],
    profile: dict[str, Any],
) -> list[str]:
    """Resolve which domain packs to load for this project."""
    if "domain_packs" in profile:
        raw = profile.get("domain_packs")
        if raw is None:
            return list(manifest.get("default_domain_packs") or [])
        if isinstance(raw, list):
            return [str(x).strip() for x in raw if str(x).strip()]
        return []

    product_kind = str(profile.get("product_kind") or "").strip()
    if not product_kind:
        pmg = _find_pmg_path(vault_root, project_id)
        if pmg and pmg.is_file():
            head = pmg.read_text(encoding="utf-8", errors="replace")[:4000]
            m = _FM_PRODUCT_KIND.search(head)
            if m:
                product_kind = m.group(1).strip()

    packs_cfg = manifest.get("domain_packs") or {}
    if product_kind and isinstance(packs_cfg, dict):
        for pack_id, meta in packs_cfg.items():
            if not isinstance(meta, dict):
                continue
            kinds = [str(k).lower() for k in (meta.get("product_kinds") or [])]
            if product_kind.lower() in kinds or product_kind.lower() == str(pack_id).lower():
                return [str(pack_id)]

    return [str(x) for x in (manifest.get("default_domain_packs") or []) if x]


def _resolved_pillars(taxonomy: dict[str, Any]) -> tuple[str, ...]:
    pset = str(taxonomy.get("pillar_set") or "none").strip()
    sets = taxonomy.get("pillar_sets") or {}
    if isinstance(sets, dict) and pset in sets:
        raw = sets[pset]
        if isinstance(raw, list) and raw:
            return tuple(str(p) for p in raw)
    if pset == "dnd_three":
        return DEFAULT_PILLARS_DND
    return ()


def load_ux_mint_taxonomy(vault_root: Path, project_id: str | None = None) -> dict[str, Any]:
    """
    Load merged taxonomy: core → domain pack(s) → project overlay.

    Project profile (`UX-MINT-TAXONOMY.project.yaml`):
      domain_packs: [] | [game_vtt] | …
      product_kind: web_app  (when pack defines product_kinds)
    """
    vault_root = vault_root.resolve()
    tdir = taxonomy_dir(vault_root)
    manifest_path = tdir / "manifest.yaml"

    if not manifest_path.is_file():
        legacy = vault_root / LEGACY_MONOLITH_REL
        if legacy.is_file():
            data = _load_yaml_dict(legacy)
            data.setdefault("taxonomy_layers", ["legacy_monolith"])
            return data
        return {"schema_version": 1, "slots": [], "pillar_set": "none", "pillar_sets": {"none": []}}

    manifest = _load_yaml_dict(manifest_path)
    core_rel = str(manifest.get("core_path") or "UX-MINT-TAXONOMY.core.yaml")
    core = _load_yaml_dict(tdir / core_rel)
    slots = [s for s in (core.get("slots") or []) if isinstance(s, dict)]
    layers = ["core"]
    pillar_set = str(core.get("pillar_set") or "none")
    faces = list(core.get("faces") or [])
    pillar_sets = dict(core.get("pillar_sets") or {})

    profile: dict[str, Any] = {}
    pack_ids: list[str] = []
    if project_id:
        profile = _load_yaml_dict(taxonomy_project_profile_path(vault_root, project_id))
        pack_ids = _resolve_domain_pack_ids(vault_root, project_id, manifest, profile)

    packs_cfg = manifest.get("domain_packs") or {}
    for pack_id in pack_ids:
        meta = packs_cfg.get(pack_id) if isinstance(packs_cfg, dict) else None
        if not isinstance(meta, dict):
            continue
        pack_path = tdir / str(meta.get("path") or f"domains/{pack_id}.yaml")
        pack_doc = _load_yaml_dict(pack_path)
        pack_slots = [s for s in (pack_doc.get("slots") or []) if isinstance(s, dict)]
        slots = _merge_slots(slots, pack_slots)
        layers.append(f"domain:{pack_id}")
        if pack_doc.get("pillar_set"):
            pillar_set = str(pack_doc["pillar_set"])
        if pack_doc.get("faces"):
            faces = list({*faces, *(pack_doc.get("faces") or [])})
        if pack_doc.get("pillar_sets"):
            pillar_sets.update(pack_doc.get("pillar_sets") or {})

    data: dict[str, Any] = {
        "schema_version": core.get("schema_version") or 1,
        "layer": "merged",
        "purpose": core.get("purpose"),
        "llm_feed_first": core.get("llm_feed_first", True),
        "faces": faces,
        "pillar_sets": pillar_sets,
        "pillar_set": pillar_set,
        "hybrid_tiers": core.get("hybrid_tiers") or manifest.get("hybrid_tiers"),
        "slots": slots,
        "taxonomy_layers": layers,
        "domain_packs": pack_ids,
        "taxonomy_manifest": str(manifest_path.relative_to(vault_root)),
        "taxonomy_core": str((tdir / core_rel).relative_to(vault_root)),
    }
    if profile:
        data["taxonomy_profile"] = profile

    if project_id:
        overlay = taxonomy_overlay_path(vault_root, project_id)
        if overlay.is_file():
            ov = _load_yaml_dict(overlay)
            extra = [s for s in (ov.get("slots") or []) if isinstance(s, dict)]
            slots = _merge_slots(slots, extra)
            data["slots"] = slots
            data["taxonomy_layers"] = [*layers, "overlay"]
            for k, v in ov.items():
                if k != "slots":
                    data[k] = v

    data["resolved_pillars"] = list(_resolved_pillars(data))
    return data


def _read_text(path: Path | None, *, limit: int | None = None) -> str:
    if path is None or not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4 :].lstrip("\n")
    if limit is not None and len(text) > limit:
        return text[:limit]
    return text


def _chunk(
    chunks: list[tuple[str, str]],
    seen: set[str],
    prefix: str,
    path: Path,
    vault_root: Path,
    *,
    limit: int,
    budget: list[int],
    max_chunks: int,
) -> None:
    if budget[0] >= max_chunks:
        return
    if not path.is_file():
        return
    try:
        rel = str(path.resolve().relative_to(vault_root.resolve()))
    except ValueError:
        rel = str(path)
    text = _read_text(path, limit=limit)
    if not text.strip():
        return
    digest = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]
    if digest in seen:
        return
    seen.add(digest)
    chunks.append((f"{prefix}:{rel}", text))
    budget[0] += 1


_PHASE_BAND_RE = re.compile(r"phase[-_]?([1-6])\b", re.IGNORECASE)
_USER_STORY_SKIP = {
    "influence-deck.md",
    "user-story-state.md",
    "mint-backlog.md",
    "catalog-mint-blank.md",
    "mint-epoch.md",
    "slice-catalog.yaml",
}

_ACTUAL_PLAY_SKIP_NAMES = {
    "readme.md",
    "_template.md",
}


def actual_play_feedstock_dir(vault_root: Path, project_id: str) -> Path:
    """Project folder for phenomenological moment / feel-pattern cards."""
    return project_root(vault_root, project_id) / "Roadmap" / "User-Story" / "Actual-Play-Feedstock"


def _is_actual_play_moment_card(path: Path) -> bool:
    name = path.name.lower()
    if name in _ACTUAL_PLAY_SKIP_NAMES or not name.endswith(".md"):
        return False
    if name.startswith("_"):
        return False
    return True


def _project_aliases(pid: str) -> set[str]:
    """Filename/path aliases for project-scoped research matching."""
    raw = str(pid or "").strip().lower()
    if not raw:
        return set()
    aliases = {raw, raw.replace("_", "-"), raw.replace("-", "_")}
    parts = [p for p in re.split(r"[-_]", raw) if p]
    if len(parts) >= 2:
        aliases.add("".join(p[0] for p in parts))
    return aliases


def _path_matches_project(path: Path, aliases: set[str]) -> bool:
    blob = str(path).lower()
    name = path.name.lower()
    if any(a and a in blob for a in aliases):
        return True
    return any(k in name for k in ("influence", "gap-stack", "lore", "world-anvil", "worldanvil"))


def _roadmap_phase_band(path: Path) -> int:
    """Lower = higher harvest priority. Prefer Phase 4–6 + conceptual over Phase 1–3."""
    s = str(path).lower()
    if "conceptual-decision" in s or "/cdr/" in s:
        return 1
    m = _PHASE_BAND_RE.search(s)
    if m:
        n = int(m.group(1))
        if n >= 4:
            return 0
        return 2
    if any(k in s for k in ("perspective", "agency", "chrome", "presentation", "hud", "worldgen", "faction")):
        return 1
    return 3


def _skip_user_story_noise(path: Path, vault_root: Path) -> bool:
    try:
        rel = str(path.resolve().relative_to(vault_root.resolve())).lower()
    except ValueError:
        rel = str(path).lower()
    if "user-story" not in rel:
        return False
    name = path.name.lower()
    if name in _USER_STORY_SKIP or name.startswith("mint-backlog"):
        return True
    if "/versions/" in rel.replace("\\", "/"):
        return True
    # Actual-play cards load via dedicated tier — skip in pin walk.
    if "actual-play-feedstock" in rel.replace("\\", "/"):
        return True
    return False


def collect_ux_mint_feedstock(
    vault_root: Path,
    project_id: str,
    *,
    pmg_path: Path | None = None,
    max_chunks: int = 120,
    per_file_limit: int = 8000,
    pmg_limit: int = 50000,
    actual_play_limit: int = 10000,
    max_actual_play_cards: int = 60,
) -> list[tuple[str, str]]:
    """
    Authority-ordered feedstock for backlog expansion.

    Priority (fill budget in order — do not let Phase 1–3 starve later tiers):
      0 PMG (full / high limit)
      1 Actual-Play-Feedstock moment / feel-pattern cards (human phenomenology)
      2 influence deck
      3 Agent-Research (project aliases + influence/lore)
      4 rules CDRs + Factory-DRB
      5 Phase 4–6 + UX-relevant pins
      6 Conceptual Decision Records (remaining)
      7 other roadmap (Phase 1–3 fill)
      8 Resources / Archives (cite-only tail)
    """
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    aliases = _project_aliases(pid)
    chunks: list[tuple[str, str]] = []
    seen: set[str] = set()
    budget = [0]
    root = project_root(vault_root, pid)

    def add(prefix: str, path: Path, *, limit: int) -> None:
        _chunk(chunks, seen, prefix, path, vault_root, limit=limit, budget=budget, max_chunks=max_chunks)

    # --- Tier 0: PMG ---
    pmg = pmg_path or _find_pmg_path(vault_root, pid)
    if pmg:
        add("pmg", pmg, limit=pmg_limit)

    # --- Tier 1: actual-play / feel-pattern moment cards ---
    ap_dir = actual_play_feedstock_dir(vault_root, pid)
    if ap_dir.is_dir():
        ap_files = sorted(p for p in ap_dir.rglob("*.md") if _is_actual_play_moment_card(p))
        for p in ap_files[:max_actual_play_cards]:
            if budget[0] >= max_chunks:
                break
            add("actual_play", p, limit=actual_play_limit)

    # --- Tier 2: influence ---
    paths = user_story_paths(vault_root, pid)
    influence = paths.get("influence")
    if isinstance(influence, Path) and influence.is_file():
        add("research", influence, limit=per_file_limit)

    # --- Tier 2: Agent-Research ---
    research_roots = [
        vault_root / "Ingest" / "Agent-Research",
        vault_root / "Ingest" / "Agent-Research" / "Raw",
    ]
    research_files: list[Path] = []
    for rr in research_roots:
        if not rr.is_dir():
            continue
        for p in sorted(rr.rglob("*.md")):
            if _path_matches_project(p, aliases):
                research_files.append(p)
    for p in research_files[:40]:
        if budget[0] >= max_chunks:
            break
        add("research", p, limit=min(5000, per_file_limit))

    # --- Tier 3: rules + Factory-DRB ---
    cdr = root / "Roadmap" / "Conceptual-Decision-Records"
    if cdr.is_dir():
        rules_paths = sorted(
            {
                *cdr.glob("*rules*"),
                *cdr.glob("*srd*"),
                *cdr.glob("*Rules*"),
                *cdr.glob("*SRD*"),
            }
        )
        for p in rules_paths:
            if budget[0] >= max_chunks:
                break
            add("rules", p, limit=per_file_limit)

    factory = root / "Factory-DRB"
    if factory.is_dir():
        factory_md = sorted(factory.rglob("*.md"))[:12]
        for p in factory_md:
            if budget[0] >= max_chunks:
                break
            add("rules", p, limit=min(4000, per_file_limit))

    # --- Tiers 4–6: roadmap pins by phase band ---
    roadmap = root / "Roadmap"
    if roadmap.is_dir():
        candidates: list[tuple[int, int, Path]] = []
        for p in roadmap.rglob("*.md"):
            if _skip_user_story_noise(p, vault_root):
                continue
            band = _roadmap_phase_band(p)
            # Prefer roll-ups slightly within a band
            rollup_bias = 0 if "roll-up" in p.name.lower() or "roll_up" in p.name.lower() else 1
            candidates.append((band, rollup_bias, p))
        candidates.sort(key=lambda t: (t[0], t[1], str(t[2]).lower()))
        for _band, _rb, p in candidates:
            if budget[0] >= max_chunks:
                break
            add("pin", p, limit=per_file_limit)

    # --- Tier 7: Resources ---
    res = vault_root / "3-Resources" / pid
    if res.is_dir():
        for p in sorted(res.rglob("*.md"))[:25]:
            if budget[0] >= max_chunks:
                break
            add("resource", p, limit=min(4000, per_file_limit))

    # --- Tier 8: Archives (cite-only) ---
    arch = vault_root / "4-Archives" / "Projects" / pid
    if arch.is_dir():
        for p in sorted(arch.rglob("*.md"))[:15]:
            if budget[0] >= max_chunks:
                break
            add("archive", p, limit=min(3000, per_file_limit))

    return chunks


def _feedstock_blob(chunks: list[tuple[str, str]]) -> str:
    return "\n".join(t for _, t in chunks).lower()


def _slot_hit(slot: dict[str, Any], blob: str) -> tuple[bool, str]:
    detects = slot.get("detect") or []
    for d in detects:
        dd = str(d).lower().strip()
        if dd and dd in blob:
            return True, dd
    return False, ""


def _chunk_priority(ref: str) -> int:
    """Lower = prefer for enrichment when multiple chunks match a needle."""
    if ref.startswith("actual_play:"):
        return 0
    if ref.startswith("pmg:"):
        return 1
    if ref.startswith("research:"):
        return 2
    if ref.startswith("pin:"):
        return 3
    if ref.startswith("rules:"):
        return 4
    return 5


def _best_chunk(
    chunks: list[tuple[str, str]],
    needle: str,
) -> tuple[str, str]:
    """Return (derived_from_ref, text) for the best matching chunk."""
    needle = (needle or "").lower()
    if needle:
        hits = [(ref, text) for ref, text in chunks if needle in text.lower()]
        if hits:
            hits.sort(key=lambda ct: (_chunk_priority(ct[0]), ct[0]))
            return hits[0][0], hits[0][1]
    if chunks:
        ordered = sorted(chunks, key=lambda ct: (_chunk_priority(ct[0]), ct[0]))
        return ordered[0][0], ordered[0][1]
    return "", ""


def _best_derived(chunks: list[tuple[str, str]], needle: str) -> str:
    ref, _ = _best_chunk(chunks, needle)
    return ref


def _excerpt_around(text: str, needle: str, *, radius: int = 240) -> str:
    """Pull a short prose excerpt around the first needle hit."""
    if not text:
        return ""
    low = text.lower()
    idx = low.find((needle or "").lower()) if needle else -1
    if idx < 0:
        # First non-empty paragraph-ish lines
        lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
        blob = " ".join(lines[:4])
        return re.sub(r"\s+", " ", blob)[: radius * 2].strip()
    start = max(0, idx - radius)
    end = min(len(text), idx + len(needle) + radius)
    snippet = text[start:end]
    snippet = re.sub(r"\s+", " ", snippet).strip()
    if start > 0:
        snippet = "…" + snippet
    if end < len(text):
        snippet = snippet + "…"
    return snippet


def _pillar_notes_from_text(text: str, pillars: tuple[str, ...], *, hit: bool) -> str:
    if not pillars:
        return ""
    low = text.lower()
    parts: list[str] = []
    for p in pillars:
        if p.lower() in low:
            parts.append(f"{p}: mentioned in feedstock")
        elif hit:
            parts.append(f"{p}: (infer from mode)")
        else:
            parts.append(f"{p}: (fill)")
    return " | ".join(parts)


def _slug(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", text.lower()).strip("_")
    return s[:48] or "ux_item"


def _pin_path_from_ref(derived: str) -> str:
    """Vault-relative path for conceptual_pin when derived_from is pin:/pmg:/research:."""
    if not derived or ":" not in derived:
        return ""
    prefix, _, rest = derived.partition(":")
    if prefix in {"pin", "pmg", "research", "rules", "resource", "actual_play"} and rest:
        return rest
    return ""


def expand_taxonomy_to_items(
    taxonomy: dict[str, Any],
    chunks: list[tuple[str, str]],
) -> list[dict[str, Any]]:
    """Emit experience nouns for every required taxonomy slot (enriched from feedstock)."""
    blob = _feedstock_blob(chunks)
    pillars = tuple(taxonomy.get("resolved_pillars") or _resolved_pillars(taxonomy))

    items: list[dict[str, Any]] = []
    for slot in taxonomy.get("slots") or []:
        if not isinstance(slot, dict):
            continue
        sid = str(slot.get("id") or "").strip()
        if not sid:
            continue
        tier = str(slot.get("mode_tier") or "multi_pillar")
        face = str(slot.get("catalog_face") or "system")
        hit, needle = _slot_hit(slot, blob)
        derived, chunk_text = _best_chunk(chunks, needle if hit else "")
        if not hit and chunks:
            # Still attach best available pin for gap rows (PMG / first UX pin)
            for pref in ("actual_play:", "pmg:", "pin:", "research:", "rules:"):
                match = next(((r, t) for r, t in chunks if r.startswith(pref)), None)
                if match:
                    derived, chunk_text = match
                    break
        base_label = str(slot.get("label") or sid)
        # Walk-facing summary stays product-contract language only.
        # Feedstock / pillar evidence goes to notes — never concatenated into summary.
        base_summary = str(slot.get("summary") or "").strip()
        dim = str(slot.get("dimension") or "ui_surface")
        axis = str(slot.get("ux_axis") or "agency")
        pin = _pin_path_from_ref(derived) if hit else ("needs pin" if not hit else "")
        if hit and not pin:
            pin = _pin_path_from_ref(derived)
        excerpt = _excerpt_around(chunk_text, needle if hit else "", radius=220) if chunk_text else ""
        note_parts: list[str] = []
        if not hit:
            note_parts.append(f"coverage_gap: no strong feedstock hit for slot `{sid}`")
            if not base_summary:
                base_summary = (
                    f"Capability contract for taxonomy slot `{sid}` — "
                    "await feedstock grounding under its series parent."
                )
        if excerpt:
            note_parts.append(f"feedstock_excerpt: {excerpt[:400]}")

        # Coverage rows are supplementary to Actual-Play phenomenology.
        # critical_matrix: one shared row (pillar notes carry explore/combat/roleplay cues)
        # instead of aggressive triplication that dilutes the mint walk.
        if tier == "critical_matrix" and pillars:
            pillar_notes = _pillar_notes_from_text(chunk_text, pillars, hit=hit)
            if pillar_notes:
                note_parts.append(f"pillars: {pillar_notes}")
            items.append(
                {
                    "id": f"ux_{_slug(sid)}",
                    "label": base_label,
                    "dimension": dim,
                    "ux_axis": axis,
                    "summary": base_summary,
                    "notes": "; ".join(note_parts),
                    "conceptual_pin": pin if hit else "needs pin",
                    "derived_from": derived,
                    "ux_family": str(slot.get("mode_family") or sid),
                    "status": "pending",
                    "catalog_face": face,
                    "experience_mode": sid,
                    "mode_tier": tier,
                    "dnd_pillar": "shared",
                    "feedstock_hit": hit,
                    "pillar_notes": pillar_notes,
                    "supplement": True,
                    "coverage_slot": True,
                    "walk_tier": "coverage",
                }
            )
        else:
            pillar = str(slot.get("dnd_pillar") or ("shared" if tier == "shared_chrome" else "shared"))
            pillar_notes = ""
            if tier == "multi_pillar" and pillars:
                pillar_notes = _pillar_notes_from_text(chunk_text, pillars, hit=hit)
            if pillar_notes:
                note_parts.append(f"pillars: {pillar_notes}")
            items.append(
                {
                    "id": f"ux_{_slug(sid)}",
                    "label": base_label,
                    "dimension": dim,
                    "ux_axis": axis,
                    "summary": base_summary,
                    "notes": "; ".join(note_parts),
                    "conceptual_pin": pin if hit else "needs pin",
                    "derived_from": derived,
                    "ux_family": str(slot.get("mode_family") or sid),
                    "status": "pending",
                    "catalog_face": face,
                    "experience_mode": sid,
                    "mode_tier": tier,
                    "dnd_pillar": pillar,
                    "feedstock_hit": hit,
                    "pillar_notes": pillar_notes,
                    "supplement": True,
                    "coverage_slot": True,
                    "walk_tier": "coverage",
                }
            )
    return items


def assert_taxonomy_coverage(
    items: list[dict[str, Any]],
    taxonomy: dict[str, Any],
    *,
    waived_slots: list[str] | None = None,
) -> tuple[bool, tuple[str, ...]]:
    """Every taxonomy slot id must appear as experience_mode on a non-dropped item."""
    waived = {str(a) for a in (waived_slots or [])}
    present: set[str] = set()
    for it in items:
        if str(it.get("status") or "") == "dropped":
            continue
        mode = str(it.get("experience_mode") or "").strip()
        if mode:
            present.add(mode)
        iid = str(it.get("id") or "")
        for slot in taxonomy.get("slots") or []:
            sid = str(slot.get("id") or "")
            if sid and (iid == f"ux_{sid}" or iid.startswith(f"ux_{_slug(sid)}_")):
                present.add(sid)
    missing = []
    for slot in taxonomy.get("slots") or []:
        sid = str(slot.get("id") or "").strip()
        if not sid or sid in waived:
            continue
        if sid not in present:
            missing.append(sid)
    return (len(missing) == 0, tuple(missing))


def is_api_heading(title: str) -> bool:
    if _PHASE_LABEL_RE.match(title.strip()):
        return True
    if _CAMEL_API.search(title):
        return True
    return False
