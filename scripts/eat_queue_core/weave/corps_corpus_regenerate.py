"""Phase 10e — optional corpus regenerate-complete for trinity_weave_self_wrap.

Archives unlocked provisional cards (+ sole-owned proof tests) to
``4-Archives/Weave/Trinity-Corpus/<stamp>/``, then regens cards with shared-test
anchors. Embedded 11a-lite dedupe skips duplicate ``harness_*`` when a module
component card is in the same archive batch.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .governance import append_metric_row
from .trinity_card import contract_proof_paths, get_touch, normalize_card
from .trinity_card_generate import build_draft_card, DiscoveryAnchor
from .trinity_card_paths import (
    component_proposals_dir,
    components_dir,
    is_locked_card,
    list_provisional_trinity_card_ids,
    load_trinity_card,
    write_trinity_card,
)
from .trinity_dual_lock import (
    is_conceptual_spine_locked,
    is_full_operator_lock,
    is_maintenance_core_id,
)
from .trinity_touch_refresh import propose_behavior_signals

META_CARD_ID = "trinity_card_authoring"
HARNESS_PREFIX = "harness_"


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _norm_proof_path(raw: str) -> str:
    return str(raw).strip().replace("\\", "/")


def _is_regen_relocatable_test_path(rel: str) -> bool:
    """Only pytest modules under ``scripts/eat_queue_core/tests/`` may be trashed on 10e.

    Production modules (e.g. ``scripts/eat_queue_core/models.py``) must never be moved
    even when every referencing card is in the archive batch.
    """
    norm = _norm_proof_path(rel)
    if not norm.endswith(".py"):
        return False
    if not norm.startswith("scripts/eat_queue_core/tests/"):
        return False
    return Path(norm).name.startswith("test_")


def _load_card_safe(vault_root: Path, tid: str) -> dict[str, Any] | None:
    try:
        return load_trinity_card(vault_root, tid, prefer="provisional")
    except (OSError, ValueError, FileNotFoundError):
        try:
            return load_trinity_card(vault_root, tid, prefer="locked")
        except (OSError, ValueError, FileNotFoundError):
            return None


def is_regen_eligible(vault_root: Path, trinity_id: str, card: dict[str, Any]) -> bool:
    tid = str(trinity_id).strip()
    if not tid or tid.startswith("_"):
        return False
    if is_maintenance_core_id(vault_root, tid):
        return False
    if is_full_operator_lock(card) or is_locked_card(card):
        return False
    if is_conceptual_spine_locked(card):
        return False
    return True


def list_regen_eligible_ids(vault_root: Path) -> list[str]:
    vault_root = vault_root.resolve()
    out: list[str] = []
    seen: set[str] = set()

    for tid in list_provisional_trinity_card_ids(vault_root):
        card = _load_card_safe(vault_root, tid)
        if card and is_regen_eligible(vault_root, tid, card) and tid not in seen:
            seen.add(tid)
            out.append(tid)

    comp = components_dir(vault_root)
    if comp.is_dir():
        for p in sorted(comp.glob("*.yaml")):
            tid = p.stem
            if tid in seen or tid.startswith("_"):
                continue
            card = _load_card_safe(vault_root, tid)
            if card and is_regen_eligible(vault_root, tid, card):
                seen.add(tid)
                out.append(tid)
    return sorted(out)


def _card_ids_referencing_proof(
    vault_root: Path,
    *,
    include_locked: bool = True,
) -> dict[str, set[str]]:
    refs: dict[str, set[str]] = {}
    ids = list(list_provisional_trinity_card_ids(vault_root))
    if include_locked:
        locked_dir = components_dir(vault_root)
        if locked_dir.is_dir():
            for p in locked_dir.glob("*.yaml"):
                if p.stem not in ids:
                    ids.append(p.stem)
    for tid in ids:
        card = _load_card_safe(vault_root, tid)
        if not card:
            continue
        for raw in contract_proof_paths(card):
            rel = _norm_proof_path(raw)
            if not rel:
                continue
            refs.setdefault(rel, set()).add(tid)
    return refs


def classify_test_ownership(
    vault_root: Path,
    archive_ids: list[str],
) -> dict[str, Any]:
    """Partition proof paths into sole-owned vs shared/locked-anchor buckets."""
    archive_set = set(archive_ids)
    refs = _card_ids_referencing_proof(vault_root, include_locked=True)
    sole_owned: list[str] = []
    shared_anchors: list[dict[str, Any]] = []
    skipped_relocate_paths: list[str] = []

    for rel, card_ids in sorted(refs.items()):
        if not rel.endswith(".py"):
            continue
        archiving = card_ids & archive_set
        if not archiving:
            continue
        surviving = card_ids - archive_set
        locked_survivors = [
            tid
            for tid in surviving
            if (c := _load_card_safe(vault_root, tid)) and is_locked_card(c)
        ]
        if surviving or locked_survivors:
            shared_anchors.append(
                {
                    "proof_path": rel,
                    "archived_card_ids": sorted(archiving),
                    "surviving_card_ids": sorted(surviving),
                    "locked_anchor_ids": sorted(locked_survivors),
                }
            )
        elif _is_regen_relocatable_test_path(rel):
            sole_owned.append(rel)
        else:
            skipped_relocate_paths.append(rel)

    return {
        "sole_owned_tests": sole_owned,
        "shared_anchors": shared_anchors,
        "skipped_relocate_paths": skipped_relocate_paths,
        "proof_ref_count": len(refs),
    }


def _11a_doctrine_loaded(vault_root: Path) -> tuple[bool, str]:
    """Return (has_doctrine, detail). Phase 11a on A-meta trinity_card_authoring."""
    from .trinity_card_11a import doctrine_present_in_card

    try:
        card = load_trinity_card(vault_root, META_CARD_ID, prefer="locked")
    except (OSError, ValueError, FileNotFoundError):
        return False, "trinity_card_authoring_missing"
    return doctrine_present_in_card(card)


def _should_skip_harness_regen(tid: str, archive_set: set[str]) -> bool:
    if not tid.startswith(HARNESS_PREFIX):
        return False
    stem = tid[len(HARNESS_PREFIX) :]
    return bool(stem and stem in archive_set and stem != tid)


def _merge_orphan_harness_commands(
    module_tid: str,
    archived_card: dict[str, Any],
    archived_cards: dict[str, dict[str, Any]],
    archive_set: set[str],
) -> list[str]:
    """11a-lite: fold harness_{module} twin commands into the module card on regen."""
    touch = get_touch(archived_card)
    cmds: list[str] = []
    seen: set[str] = set()
    for raw in touch.get("harness_commands") or []:
        c = str(raw).strip()
        if c and c not in seen:
            seen.add(c)
            cmds.append(c)
    if module_tid not in seen:
        seen.add(module_tid)
        cmds.append(module_tid)

    orphan_tid = f"{HARNESS_PREFIX}{module_tid}"
    if orphan_tid in archive_set:
        orphan = archived_cards.get(orphan_tid) or {}
        orphan_touch = get_touch(orphan)
        stem = module_tid
        if stem not in seen:
            seen.add(stem)
            cmds.append(stem)
        for raw in orphan_touch.get("harness_commands") or []:
            c = str(raw).strip()
            if c and c not in seen:
                seen.add(c)
                cmds.append(c)
    return cmds


def _move_to_trash(vault_root: Path, rel_path: str) -> None:
    script = vault_root / "scripts" / "move-to-trash.sh"
    if not script.is_file():
        raise FileNotFoundError(f"move-to-trash missing: {script}")
    subprocess.run(
        [str(script), rel_path],
        cwd=str(vault_root.resolve()),
        check=True,
        capture_output=True,
        text=True,
    )


def _archive_file(vault_root: Path, src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(src.read_bytes())
    rel = src.relative_to(vault_root.resolve()).as_posix()
    _move_to_trash(vault_root, rel)


def archive_unlocked_corpus(
    vault_root: Path,
    archive_ids: list[str],
    *,
    archive_root: Path,
    ownership: dict[str, Any],
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    cards_dir = archive_root / "cards"
    tests_dir = archive_root / "tests"
    archived_cards: list[str] = []
    moved_tests: list[str] = []
    errors: list[str] = []

    for tid in archive_ids:
        for tier, base in (
            ("provisional", component_proposals_dir(vault_root)),
            ("locked", components_dir(vault_root)),
        ):
            src = base / f"{tid}.yaml"
            if not src.is_file():
                continue
            try:
                _archive_file(vault_root, src, cards_dir / f"{tid}.yaml")
                archived_cards.append(tid)
            except (OSError, subprocess.CalledProcessError) as e:
                errors.append(f"card:{tid}:{e}")
            break

    for rel in ownership.get("sole_owned_tests") or []:
        src = vault_root / rel
        if not src.is_file():
            continue
        try:
            _archive_file(vault_root, src, tests_dir / Path(rel).name)
            moved_tests.append(rel)
        except (OSError, subprocess.CalledProcessError) as e:
            errors.append(f"test:{rel}:{e}")

    return {
        "archived_card_count": len(archived_cards),
        "archived_card_ids": archived_cards,
        "sole_owned_tests_moved": moved_tests,
        "errors": errors,
    }


def _anchor_proof_paths(
    vault_root: Path,
    archived_card: dict[str, Any],
    shared_anchors: list[dict[str, Any]],
    tid: str,
) -> list[str]:
    proofs = [_norm_proof_path(p) for p in contract_proof_paths(archived_card) if str(p).strip()]
    anchor_paths: list[str] = []
    for row in shared_anchors:
        if tid in (row.get("archived_card_ids") or []):
            anchor_paths.append(_norm_proof_path(row["proof_path"]))
    merged: list[str] = []
    seen: set[str] = set()
    for p in proofs + anchor_paths:
        if p and p not in seen and (vault_root / p).exists():
            seen.add(p)
            merged.append(p)
    return merged


def regenerate_archived_card(
    vault_root: Path,
    tid: str,
    archived_card: dict[str, Any],
    *,
    shared_anchors: list[dict[str, Any]],
    archived_cards: dict[str, dict[str, Any]] | None = None,
    archive_set: set[str] | None = None,
    dry_run: bool = False,
    meta_lens_force_align: bool = False,
) -> dict[str, Any]:
    touch = get_touch(archived_card)
    primary_paths = [_norm_proof_path(p) for p in (touch.get("primary_paths") or []) if str(p).strip()]
    primary = primary_paths[0] if primary_paths else f"scripts/eat_queue_core/{tid}.py"
    component = str(archived_card.get("id") or tid).replace("_", " ")

    anchors = [DiscoveryAnchor(path=primary, role="regenerate_complete")]
    card, legs, card_class = build_draft_card(
        vault_root,
        trinity_id=tid,
        component=component,
        primary_path=primary,
        source_kind="regenerate_complete",
        anchors=anchors,
    )

    card["conceptual"] = archived_card.get("conceptual") or card.get("conceptual")
    if meta_lens_force_align:
        from .trinity_meta_lens_regen import apply_meta_lens_force_align, summarize_force_align_delta

        before = normalize_card(dict(card))
        card = apply_meta_lens_force_align(vault_root, card, archived_card, tid)
        lens_delta = summarize_force_align_delta(before, card)
    else:
        card["rules"] = archived_card.get("rules") or card.get("rules")
        lens_delta = None

    card.pop("_meta_lens_overlay", None)

    proof_paths = _anchor_proof_paths(vault_root, archived_card, shared_anchors, tid)
    if proof_paths:
        card.setdefault("contract", {})["proof"] = proof_paths
        scan_card = normalize_card(dict(card))
        proposed = propose_behavior_signals(vault_root, scan_card)
        if proposed:
            card.setdefault("touch", {})["behavior_signals"] = proposed[:16]

    harness_cmds = touch.get("harness_commands") or []
    if archived_cards is not None and archive_set is not None and not tid.startswith(HARNESS_PREFIX):
        harness_cmds = _merge_orphan_harness_commands(
            tid, archived_card, archived_cards, archive_set
        )
    elif harness_cmds:
        harness_cmds = list(harness_cmds)
    if harness_cmds:
        card.setdefault("touch", {})["harness_commands"] = harness_cmds

    card["meta"] = dict(card.get("meta") or {})
    card["meta"]["card_class"] = card_class
    card["meta"]["leg_status"] = asdict(legs)
    card["meta"].setdefault("source", {})["regenerated_at"] = _now_iso()
    card["meta"]["source"]["regenerate_complete"] = True
    if meta_lens_force_align:
        card["meta"]["source"]["meta_lens_force_align"] = True

    if not dry_run:
        write_trinity_card(
            vault_root,
            tid,
            card,
            tier="provisional",
            mutation_action="corps_regenerate_complete",
            operator_override=True,
        )

    result: dict[str, Any] = {
        "trinity_id": tid,
        "regenerated": True,
        "card_class": card_class,
        "proof_paths": proof_paths[:8],
        "behavior_signals": (card.get("touch") or {}).get("behavior_signals", [])[:8],
        "meta_lens_force_align": bool(meta_lens_force_align),
    }
    if lens_delta is not None:
        result["meta_lens_delta"] = lens_delta
    return result


def run_regenerate_complete(
    vault_root: Path,
    *,
    dry_run: bool = False,
    operator_mutation_on_core: bool = False,
    cli_requested: bool = False,
    meta_lens_force_align: bool = False,
) -> dict[str, Any]:
    """Archive eligible corpus + regen with shared-test anchors (10e)."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    config_enabled = bool(getattr(cfg, "corps_regenerate_complete_enabled", False))
    config_lens = bool(getattr(cfg, "corps_regen_meta_lens_force_align_enabled", False))
    lens_align = bool(meta_lens_force_align or config_lens)
    enabled = config_enabled or bool(cli_requested)
    rec: dict[str, Any] = {
        "ok": True,
        "enabled": enabled,
        "config_enabled": config_enabled,
        "cli_override": bool(cli_requested and not config_enabled),
        "meta_lens_force_align": lens_align,
        "meta_lens_force_align_cli": bool(meta_lens_force_align),
        "dry_run": dry_run,
        "started_at": _now_iso(),
    }

    if not enabled:
        return {
            "ok": True,
            "skipped": True,
            "reason": "corps_regenerate_complete_disabled",
            "enabled": False,
            "config_enabled": config_enabled,
            "hint": "Pass --regenerate-complete on trinity_weave_self_wrap or set trinity_corps_regenerate_complete_enabled: true",
        }

    require_11a = getattr(cfg, "corps_regenerate_require_11a", True)
    has_11a, detail = _11a_doctrine_loaded(vault_root)
    if require_11a and not has_11a:
        return {
            "ok": False,
            "skipped": True,
            "reason": "11a_doctrine_required",
            "detail": detail,
            "hint": "Update trinity_card_authoring with card_kind doctrine or set trinity_corps_regenerate_require_11a: false",
        }

    if lens_align:
        from .trinity_meta_lens_regen import validate_meta_lens_regen_prerequisites

        gate = validate_meta_lens_regen_prerequisites(vault_root)
        rec["meta_lens_gate"] = gate
        if not gate.get("ok"):
            return {
                **rec,
                "ok": False,
                "skipped": True,
                "reason": gate.get("reason") or "meta_lens_gate_failed",
                "hint": gate.get("hint"),
            }

    archive_ids = list_regen_eligible_ids(vault_root)
    if not archive_ids:
        return {
            "ok": True,
            "skipped": True,
            "reason": "no_regen_eligible_cards",
            "enabled": True,
        }

    ownership = classify_test_ownership(vault_root, archive_ids)
    stamp = _stamp()
    archive_rel = getattr(cfg, "corps_corpus_archive_root", "4-Archives/Weave/Trinity-Corpus")
    archive_root = vault_root / archive_rel / stamp
    rec["regen_stamp"] = stamp
    rec["archive_path"] = str(archive_root.relative_to(vault_root))
    rec["eligible_card_count"] = len(archive_ids)

    if dry_run:
        rec["ownership"] = ownership
        rec["would_archive_ids"] = archive_ids
        rec["skipped_writes"] = True
        if lens_align and archive_ids:
            from .trinity_meta_lens_regen import apply_meta_lens_force_align, summarize_force_align_delta

            sample_tid = archive_ids[0]
            sample_archived = _load_card_safe(vault_root, sample_tid)
            if sample_archived:
                touch = get_touch(sample_archived)
                primary_paths = [
                    _norm_proof_path(p) for p in (touch.get("primary_paths") or []) if str(p).strip()
                ]
                primary = primary_paths[0] if primary_paths else f"scripts/eat_queue_core/{sample_tid}.py"
                draft, _, _ = build_draft_card(
                    vault_root,
                    trinity_id=sample_tid,
                    component=sample_tid.replace("_", " "),
                    primary_path=primary,
                    source_kind="regenerate_complete",
                    anchors=[DiscoveryAnchor(path=primary, role="regenerate_complete")],
                )
                draft["conceptual"] = sample_archived.get("conceptual") or draft.get("conceptual")
                before = normalize_card(dict(draft))
                after = apply_meta_lens_force_align(vault_root, draft, sample_archived, sample_tid)
                after.pop("_meta_lens_overlay", None)
                rec["meta_lens_sample"] = {
                    "trinity_id": sample_tid,
                    "delta": summarize_force_align_delta(before, after),
                }
        from .corps_test_compensation import run_test_compensation

        rec["test_compensation"] = run_test_compensation(
            vault_root,
            archive_ids=archive_ids,
            archived_cards={
                tid: c for tid in archive_ids if (c := _load_card_safe(vault_root, tid))
            },
            ownership=ownership,
            regen_tids=archive_ids,
            dry_run=True,
        )
        return rec

    archive_set = set(archive_ids)
    archived_cards: dict[str, dict[str, Any]] = {}
    for tid in archive_ids:
        card = _load_card_safe(vault_root, tid)
        if card:
            archived_cards[tid] = card

    archive_result = archive_unlocked_corpus(
        vault_root,
        archive_ids,
        archive_root=archive_root,
        ownership=ownership,
    )
    rec.update(
        {
            "archived_card_count": archive_result.get("archived_card_count", 0),
            "sole_owned_tests_moved": archive_result.get("sole_owned_tests_moved", []),
        }
    )
    if archive_result.get("errors"):
        rec["archive_errors"] = archive_result["errors"]
        rec["ok"] = False

    regen_results: list[dict[str, Any]] = []
    skipped_harness: list[str] = []
    shared_anchors = ownership.get("shared_anchors") or []

    from .trinity_dual_lock import operator_mutation_ctx

    def _write_regen_checkpoint() -> None:
        checkpoint = {
            "stamp": stamp,
            "phase": "post_regen_pre_compensation",
            "created_at": _now_iso(),
            "archive_ids": archive_ids,
            "archived_card_count": rec.get("archived_card_count"),
            "regenerated_count": rec.get("regenerated_count"),
            "regen_results": regen_results[:40],
            "meta_lens_force_align": lens_align,
        }
        archive_root.mkdir(parents=True, exist_ok=True)
        (archive_root / "manifest.checkpoint.json").write_text(
            json.dumps(checkpoint, indent=2) + "\n",
            encoding="utf-8",
        )

    op_token = operator_mutation_ctx.set(
        bool(operator_mutation_on_core or cli_requested or enabled)
    )
    compensation: dict[str, Any] = {}
    try:
        for tid in archive_ids:
            if _should_skip_harness_regen(tid, archive_set):
                skipped_harness.append(tid)
                continue
            archived = archived_cards.get(tid)
            if not archived:
                continue
            try:
                regen_results.append(
                    regenerate_archived_card(
                        vault_root,
                        tid,
                        archived,
                        shared_anchors=shared_anchors,
                        archived_cards=archived_cards,
                        archive_set=archive_set,
                        dry_run=False,
                        meta_lens_force_align=lens_align,
                    )
                )
            except (OSError, ValueError) as e:
                regen_results.append(
                    {"trinity_id": tid, "regenerated": False, "error": str(e)}
                )
                rec["ok"] = False

        rec["shared_tests_anchored"] = len(shared_anchors)
        rec["regenerated_count"] = sum(1 for r in regen_results if r.get("regenerated"))
        if rec.get("archived_card_count", 0) > 0 and rec.get("regenerated_count", 0) == 0:
            rec["ok"] = False
            rec.setdefault("reason", "zero_regenerated_after_archive")
        rec["skipped_harness_duplicate"] = skipped_harness
        rec["regen_results"] = regen_results[:40]

        _write_regen_checkpoint()

        regen_tids = [r["trinity_id"] for r in regen_results if r.get("regenerated")]
        from .corps_test_compensation import run_test_compensation

        try:
            compensation = run_test_compensation(
                vault_root,
                archive_ids=archive_ids,
                archived_cards=archived_cards,
                ownership=ownership,
                regen_tids=regen_tids,
                dry_run=False,
                regenerate_burn=True,
                skip_proof_verify=True,
            )
        except (OSError, ValueError) as e:
            compensation = {
                "ok": False,
                "compensation_ok": False,
                "error": str(e),
            }
            rec["ok"] = False
    finally:
        operator_mutation_ctx.reset(op_token)

    rec["test_compensation"] = compensation
    if compensation and not compensation.get("compensation_ok", True) and not compensation.get(
        "skipped"
    ):
        rec["ok"] = False

    manifest = {
        "stamp": stamp,
        "created_at": _now_iso(),
        "archive_ids": archive_ids,
        "ownership": ownership,
        "archive_result": archive_result,
        "regenerated_count": rec["regenerated_count"],
        "skipped_harness_duplicate": skipped_harness,
        "test_compensation": compensation,
        "operator_mutation_on_core": operator_mutation_on_core,
        "meta_lens_force_align": lens_align,
        "11a_detail": detail,
    }
    archive_root.mkdir(parents=True, exist_ok=True)
    (archive_root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (archive_root / "anchors.json").write_text(
        json.dumps({"shared_anchors": shared_anchors}, indent=2) + "\n",
        encoding="utf-8",
    )

    append_metric_row(
        vault_root,
        {
            "metric_type": "corps_regenerate_complete",
            "ok": rec.get("ok"),
            "archived_card_count": rec.get("archived_card_count"),
            "regenerated_count": rec.get("regenerated_count"),
            "stamp": stamp,
        },
    )
    rec["completed_at"] = _now_iso()
    return rec
