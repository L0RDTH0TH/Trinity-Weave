"""Trinity conceptual spine cascade — polish stub Conceptual legs from validated corpus.

Phase after operator has locked ~25 anchor cards: forward-grow outcome/summary/
primary_case/edge_cases/misread_risks on remaining stubs using pairs_with,
concept-trinity-map, and locked production Conceptual legs. Touch/Rules left
unchanged unless --fix-legs.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .trinity_card import SCHEMA_VERSION, get_conceptual, normalize_card
from .trinity_card_generate import META_CARD_ID, SCHEMA_CARD, _is_locked
from .trinity_conceptual_doctrine import (
    build_conceptual_regen_pack_markdown,
    conceptual_has_machine_voice,
    conceptual_has_meta_contamination,
    conceptual_needs_experiential_rewrite,
    pick_gold_examples,
    synthesize_conceptual_human_vantage,
)
from .trinity_touch_refresh import components_dir, concept_map_path, load_trinity_card

DEFAULT_STUB_GLOBS = (
    ".technical/weave/proposals/**/stubs/**/*.yaml",
    ".technical/weave/proposals/governance-set-v1/stubs/*.yaml",
)


@dataclass
class CascadeTarget:
    trinity_id: str
    source_path: str
    reason: str


@dataclass
class CascadeRecord:
    trinity_id: str
    source_path: str
    output_path: str
    neighbors_used: list[str]
    written: bool
    skipped: bool
    skip_reason: str = ""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _default_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d-spine-cascade")


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"not a mapping: {path}")
    return data


def _dump_yaml(card: dict[str, Any]) -> str:
    return yaml.dump(card, sort_keys=False, allow_unicode=True, default_flow_style=False)


def load_conceptual_corpus(vault_root: Path) -> dict[str, dict[str, Any]]:
    """Locked production cards — doctrinal Conceptual legs only."""
    out: dict[str, dict[str, Any]] = {}
    comp = components_dir(vault_root)
    if not comp.is_dir():
        return out
    for path in sorted(comp.glob("*.yaml")):
        if path.stem in (SCHEMA_CARD, META_CARD_ID):
            continue
        try:
            card = load_trinity_card(vault_root, path.stem)
        except (OSError, ValueError):
            continue
        if not _is_locked(card):
            continue
        conceptual = get_conceptual(card)
        if conceptual.get("outcome") or conceptual.get("summary"):
            out[path.stem] = conceptual
    return out


def _concept_map_rows(vault_root: Path) -> dict[str, dict[str, Any]]:
    path = concept_map_path(vault_root)
    if not path.is_file():
        return {}
    try:
        data = _load_yaml(path)
    except (OSError, ValueError, yaml.YAMLError):
        return {}
    concepts = data.get("concepts")
    if not isinstance(concepts, dict):
        return {}
    by_tid: dict[str, dict[str, Any]] = {}
    for _key, row in concepts.items():
        if not isinstance(row, dict):
            continue
        tid = str(row.get("trinity_id") or "").strip()
        if tid:
            by_tid[tid] = row
    return by_tid


def _pairs_from_card(card: dict[str, Any]) -> list[str]:
    conceptual = get_conceptual(card)
    raw = conceptual.get("pairs_with")
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for item in raw:
        s = str(item).strip()
        if not s:
            continue
        # "foo — bar" or plain id
        token = re.split(r"\s+[—–-]\s+", s, maxsplit=1)[0].strip()
        if token and token not in out:
            out.append(token)
    return out


def resolve_neighbor_ids(
    vault_root: Path,
    trinity_id: str,
    card: dict[str, Any],
    corpus: dict[str, dict[str, Any]],
    *,
    max_neighbors: int = 5,
) -> list[str]:
    candidates: list[str] = []
    for nid in _pairs_from_card(card):
        if nid in corpus and nid != trinity_id and nid not in candidates:
            candidates.append(nid)

    cmap = _concept_map_rows(vault_root).get(trinity_id) or {}
    for key in ("pairs_with", "related_trinity_ids", "polar_pair"):
        val = cmap.get(key)
        if isinstance(val, list):
            for item in val:
                nid = str(item).strip().split()[0] if str(item).strip() else ""
                if nid in corpus and nid != trinity_id and nid not in candidates:
                    candidates.append(nid)
        elif isinstance(val, str) and val.strip():
            nid = val.strip().split()[0]
            if nid in corpus and nid != trinity_id and nid not in candidates:
                candidates.append(nid)

    # Same governance set ordinal (spine siblings)
    meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
    src = meta.get("source") if isinstance(meta.get("source"), dict) else {}
    ordinal = src.get("governance_set_ordinal")
    if ordinal is not None:
        comp = components_dir(vault_root)
        for path in comp.glob("*.yaml"):
            if path.stem == trinity_id or path.stem not in corpus:
                continue
            try:
                other = load_trinity_card(vault_root, path.stem)
            except (OSError, ValueError):
                continue
            om = other.get("meta") if isinstance(other.get("meta"), dict) else {}
            osrc = om.get("source") if isinstance(om.get("source"), dict) else {}
            if osrc.get("governance_set_ordinal") == ordinal and path.stem not in candidates:
                candidates.append(path.stem)

    # Fallback: invariant_registry + weave_governance anchors
    for anchor in ("invariant_registry", "weave_governance"):
        if anchor in corpus and anchor not in candidates and anchor != trinity_id:
            candidates.append(anchor)

    return candidates[:max_neighbors]


def _conceptual_needs_cascade(card: dict[str, Any]) -> tuple[bool, str]:
    meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
    if meta.get("conceptual_confirmed_at"):
        return False, "conceptual_confirmed_at set"
    conceptual = get_conceptual(card)
    summary = str(conceptual.get("summary") or "")
    outcome = str(conceptual.get("outcome") or "")
    if not outcome.strip() and not summary.strip():
        return True, "conceptual empty"
    if conceptual_needs_experiential_rewrite(card):
        return True, "machine_voice_or_meta_contamination"
    if meta.get("card_class") == "incomplete":
        return True, "card_class incomplete"
    if len(summary) < 80 and "operator" not in summary.lower():
        return True, "thin conceptual"
    src = meta.get("source") if isinstance(meta.get("source"), dict) else {}
    sc = src.get("spine_cascade")
    if isinstance(sc, dict):
        if sc.get("voice") != "experiential_vantage":
            return True, "prior_regen_not_experiential"
    return False, "conceptual looks polished"


def discover_unlocked_production_targets(
    vault_root: Path,
    *,
    trinity_id: str | None = None,
    extend_only: bool = False,
) -> list[CascadeTarget]:
    """Production components without conceptual lock (rare; not in LOCKED_SKIP_IDS corpus)."""
    targets: list[CascadeTarget] = []
    comp = components_dir(vault_root)
    if not comp.is_dir():
        return targets
    for path in sorted(comp.glob("*.yaml")):
        if path.name.startswith("_") or path.stem in (META_CARD_ID, SCHEMA_CARD):
            continue
        if trinity_id and path.stem != trinity_id:
            continue
        try:
            card = load_trinity_card(vault_root, path.stem)
        except (OSError, ValueError):
            continue
        if _is_locked(card):
            continue
        meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
        if meta.get("conceptual_confirmed_at") and not extend_only:
            continue
        needs, reason = _conceptual_needs_cascade(card)
        if not needs and not extend_only:
            continue
        rel = path.relative_to(vault_root).as_posix()
        targets.append(CascadeTarget(trinity_id=path.stem, source_path=rel, reason=reason))
    return targets


def discover_cascade_targets(
    vault_root: Path,
    *,
    stub_globs: tuple[str, ...] = DEFAULT_STUB_GLOBS,
    trinity_id: str | None = None,
    extend_only: bool = False,
    governance_stubs_only: bool = False,
    include_unlocked_production: bool = False,
) -> list[CascadeTarget]:
    if governance_stubs_only:
        stub_globs = (".technical/weave/proposals/governance-set-v1/stubs/*.yaml",)
    targets: list[CascadeTarget] = []
    seen: set[str] = set()

    def consider(path: Path) -> None:
        if not path.is_file() or path.name.startswith("_"):
            return
        try:
            card = _load_yaml(path)
        except (OSError, ValueError, yaml.YAMLError):
            return
        tid = str(card.get("id") or path.stem).strip()
        if not tid or tid in (META_CARD_ID, SCHEMA_CARD):
            return
        if trinity_id and tid != trinity_id:
            return
        if tid in seen:
            return
        prod = components_dir(vault_root) / f"{tid}.yaml"
        if prod.is_file():
            try:
                prod_card = load_trinity_card(vault_root, tid)
                if _is_locked(prod_card) and not extend_only:
                    return
                if prod_card.get("meta", {}).get("conceptual_confirmed_at") and not extend_only:
                    return
            except (OSError, ValueError):
                pass
        needs, reason = _conceptual_needs_cascade(card)
        if not needs and not extend_only:
            return
        seen.add(tid)
        rel = path.relative_to(vault_root).as_posix()
        targets.append(CascadeTarget(trinity_id=tid, source_path=rel, reason=reason))

    if trinity_id:
        # Explicit id: stub anywhere + governance stub
        for pattern in stub_globs:
            for path in vault_root.glob(pattern):
                if path.stem == trinity_id:
                    consider(path)
        gov = vault_root / f".technical/weave/proposals/governance-set-v1/stubs/{trinity_id}.yaml"
        if gov.is_file():
            consider(gov)
        return targets

    for pattern in stub_globs:
        for path in sorted(vault_root.glob(pattern)):
            consider(path)

    if include_unlocked_production:
        prod = discover_unlocked_production_targets(
            vault_root, trinity_id=trinity_id, extend_only=extend_only
        )
        seen = {t.trinity_id for t in targets}
        for t in prod:
            if t.trinity_id not in seen:
                targets.append(t)
                seen.add(t.trinity_id)
    return targets


# Back-compat alias for tests and imports.
synthesize_conceptual_leg = synthesize_conceptual_human_vantage


def build_cascade_pack_markdown(
    vault_root: Path,
    trinity_id: str,
    card: dict[str, Any],
    neighbor_ids: list[str],
    corpus: dict[str, dict[str, Any]],
    *,
    gold_examples: list[tuple[str, dict[str, Any]]] | None = None,
) -> str:
    return build_conceptual_regen_pack_markdown(
        vault_root,
        trinity_id,
        card,
        neighbor_ids,
        corpus,
        gold_examples=gold_examples,
    )


def apply_spine_cascade_to_card(
    card: dict[str, Any],
    new_conceptual: dict[str, Any],
    *,
    neighbor_ids: list[str],
    source_path: str,
) -> dict[str, Any]:
    out = dict(card)
    out["conceptual"] = new_conceptual
    meta = dict(out.get("meta") or {})
    meta["schema_version"] = SCHEMA_VERSION
    meta["card_class"] = "incomplete"
    src = dict(meta.get("source") or {})
    src["spine_cascade"] = {
        "at": _now_iso(),
        "neighbors_used": neighbor_ids,
        "source_stub": source_path,
        "method": "trinity_conceptual_regen_v3",
        "voice": "experiential_vantage",
    }
    src.pop("backfill_applied", None)
    meta["source"] = src
    meta.pop("conceptual_confirmed_at", None)
    meta.pop("rules_confirmed_at", None)
    out["meta"] = meta
    return normalize_card(out)


def stub_globs_for_proposal_stamp(proposal_stamp: str) -> tuple[str, ...]:
    base = f".technical/weave/proposals/{proposal_stamp.strip().strip('/')}"
    return (
        f"{base}/stubs/**/*.yaml",
        f"{base}/stubs/*.yaml",
    )


def run_trinity_spine_cascade(
    vault_root: Path,
    *,
    dry_run: bool = False,
    stamp: str | None = None,
    trinity_id: str | None = None,
    write_in_place: bool = False,
    extend_only: bool = False,
    fix_legs: bool = False,
    write_packs: bool = True,
    stub_globs: tuple[str, ...] = DEFAULT_STUB_GLOBS,
    governance_stubs_only: bool = False,
    proposal_stamp: str | None = None,
    include_unlocked_production: bool = False,
    force_machine_voice: bool = False,
) -> dict[str, Any]:
    if proposal_stamp:
        stub_globs = stub_globs_for_proposal_stamp(proposal_stamp)
        stamp = stamp or f"{proposal_stamp.strip().strip('/')}-spine-cascade"
    stamp = stamp or _default_stamp()
    corpus = load_conceptual_corpus(vault_root)
    if not corpus:
        return {
            "ok": False,
            "error": "no_locked_conceptual_corpus",
            "hint": "Lock anchor cards in .technical/weave/components/ first (conceptual_confirmed_at + rules_confirmed_at).",
        }

    gold_examples = pick_gold_examples(corpus)

    targets = discover_cascade_targets(
        vault_root,
        stub_globs=stub_globs,
        trinity_id=trinity_id,
        extend_only=extend_only,
        governance_stubs_only=governance_stubs_only,
        include_unlocked_production=include_unlocked_production,
    )
    if force_machine_voice:
        extra: list[CascadeTarget] = []
        seen_ids = {t.trinity_id for t in targets}
        for pattern in stub_globs:
            for path in sorted(vault_root.glob(pattern)):
                if not path.is_file() or path.name.startswith("_"):
                    continue
                try:
                    card = _load_yaml(path)
                except (OSError, ValueError, yaml.YAMLError):
                    continue
                tid = str(card.get("id") or path.stem).strip()
                if not tid or tid in seen_ids:
                    continue
                if trinity_id and tid != trinity_id:
                    continue
                meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
                if meta.get("conceptual_confirmed_at"):
                    continue
                prod = components_dir(vault_root) / f"{tid}.yaml"
                if prod.is_file():
                    try:
                        if _is_locked(load_trinity_card(vault_root, tid)):
                            continue
                    except (OSError, ValueError):
                        pass
                if conceptual_needs_experiential_rewrite(card):
                    rel = path.relative_to(vault_root).as_posix()
                    extra.append(
                        CascadeTarget(
                            trinity_id=tid,
                            source_path=rel,
                            reason="force_machine_voice",
                        )
                    )
                    seen_ids.add(tid)
        targets = targets + extra
    if not targets:
        return {
            "ok": True,
            "stamp": stamp,
            "dry_run": dry_run,
            "corpus_size": len(corpus),
            "targets": 0,
            "message": "no cascade targets found (stubs already polished or none on disk)",
        }

    out_dir = vault_root / ".technical/weave/proposals" / stamp
    stubs_dir = out_dir / "stubs"
    packs_dir = out_dir / "packs"

    records: list[CascadeRecord] = []
    written: list[str] = []

    for target in targets:
        src_path = vault_root / target.source_path
        card = _load_yaml(src_path)
        neighbor_ids = resolve_neighbor_ids(vault_root, target.trinity_id, card, corpus)
        new_c = synthesize_conceptual_human_vantage(
            vault_root,
            target.trinity_id,
            card,
            neighbor_ids,
            corpus,
            gold_examples=gold_examples,
        )
        updated = apply_spine_cascade_to_card(
            card,
            new_c,
            neighbor_ids=neighbor_ids,
            source_path=target.source_path,
        )
        if fix_legs:
            pass  # reserved — operator asked to leave legs unless flag set

        if write_in_place:
            dest = src_path
        else:
            dest = stubs_dir / f"{target.trinity_id}.yaml"

        rel_out = dest.relative_to(vault_root).as_posix()
        rec = CascadeRecord(
            trinity_id=target.trinity_id,
            source_path=target.source_path,
            output_path=rel_out,
            neighbors_used=neighbor_ids,
            written=False,
            skipped=False,
        )

        if dry_run:
            rec.skipped = True
            rec.skip_reason = "dry_run"
        else:
            from .trinity_dual_lock import assert_system_may_mutate

            assert_system_may_mutate(
                vault_root,
                target.trinity_id,
                "trinity_spine_cascade",
            )
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(_dump_yaml(updated), encoding="utf-8")
            written.append(rel_out)
            rec.written = True
            if write_packs:
                packs_dir.mkdir(parents=True, exist_ok=True)
                pack_path = packs_dir / f"{target.trinity_id}.md"
                pack_path.write_text(
                    build_cascade_pack_markdown(
                        vault_root, target.trinity_id, card, neighbor_ids, corpus
                    ),
                    encoding="utf-8",
                )

        records.append(rec)

    manifest = {
        "ok": True,
        "stamp": stamp,
        "generated_at": _now_iso(),
        "dry_run": dry_run,
        "write_in_place": write_in_place,
        "extend_only": extend_only,
        "governance_stubs_only": governance_stubs_only,
        "proposal_stamp": proposal_stamp,
        "fix_legs": fix_legs,
        "include_unlocked_production": include_unlocked_production,
        "force_machine_voice": force_machine_voice,
        "gold_example_ids": [g[0] for g in gold_examples],
        "corpus_size": len(corpus),
        "corpus_ids": sorted(corpus.keys()),
        "output_dir": out_dir.relative_to(vault_root).as_posix() if not dry_run else None,
        "targets": len(targets),
        "written_count": len(written),
        "written": written,
        "records": [asdict(r) for r in records],
    }

    if not dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        index_lines = [
            "# Spine cascade",
            "",
            f"Generated: {manifest['generated_at']}",
            "",
            f"Corpus: **{len(corpus)}** locked conceptual cards.",
            "",
            "| trinity_id | source | output | neighbors |",
            "|------------|--------|--------|-----------|",
        ]
        for r in records:
            nbr = ", ".join(r.neighbors_used[:3])
            if len(r.neighbors_used) > 3:
                nbr += "…"
            index_lines.append(
                f"| `{r.trinity_id}` | `{r.source_path}` | `{r.output_path}` | {nbr} |"
            )
        (out_dir / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    return manifest
