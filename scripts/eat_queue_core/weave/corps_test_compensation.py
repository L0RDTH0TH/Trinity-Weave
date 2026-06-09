"""Phase 10e-b — blanket test rewrite after card regen; surgical adapt for locked-touch only."""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .corps_repair_audit import append_corps_repair_audit
from .corps_smoke_test import (
    module_path_to_import,
    rewrite_blanket_smoke_test,
    smoke_test_path_for_module,
)
from .trinity_card import contract_proof_paths, get_touch, normalize_card
from .trinity_card_paths import load_trinity_card, write_trinity_card
from .trinity_touch_refresh import propose_behavior_signals


def _norm_path(raw: str) -> str:
    return str(raw or "").strip().replace("\\", "/")


def _primary_paths(card: dict[str, Any]) -> list[str]:
    touch = get_touch(card)
    return [_norm_path(p) for p in (touch.get("primary_paths") or []) if str(p).strip()]


def locked_touched_proof_paths(ownership: dict[str, Any]) -> set[str]:
    """Tests referenced by a locked card — surgical only, never blanket overwrite."""
    out: set[str] = set()
    for row in ownership.get("shared_anchors") or []:
        if row.get("locked_anchor_ids"):
            rel = _norm_path(row.get("proof_path") or "")
            if rel:
                out.add(rel)
    return out


def _file_hash(path: Path) -> str:
    if not path.is_file():
        return ""
    blob = path.read_bytes()
    return hashlib.sha256(blob).hexdigest()[:16]


def surgical_adapt_shared_anchor(
    vault_root: Path,
    proof_path: str,
    *,
    archived_cards: dict[str, dict[str, Any]],
    regen_tids: set[str],
    dry_run: bool = False,
) -> dict[str, Any]:
    """Minimal path/import patches when a locked card shares this test file."""
    vault_root = vault_root.resolve()
    rel = _norm_path(proof_path)
    path = vault_root / rel
    rec: dict[str, Any] = {
        "proof_path": rel,
        "mode": "surgical",
        "patched": False,
        "replacements": [],
    }
    if not path.is_file():
        rec["reason"] = "missing_test_file"
        return rec

    before_hash = _file_hash(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text
    replacements: list[dict[str, str]] = []

    for tid in regen_tids:
        old_card = archived_cards.get(tid)
        if not old_card:
            continue
        try:
            new_card = load_trinity_card(vault_root, tid, prefer="provisional")
        except (OSError, ValueError, FileNotFoundError):
            continue
        old_ps = _primary_paths(old_card)
        new_ps = _primary_paths(new_card)
        for old_p, new_p in zip(old_ps, new_ps):
            if not old_p or not new_p or old_p == new_p:
                continue
            if old_p in text:
                text = text.replace(old_p, new_p)
                replacements.append({"kind": "path", "from": old_p, "to": new_p})
            old_mod = module_path_to_import(old_p)
            new_mod = module_path_to_import(new_p)
            if old_mod and new_mod and old_mod != new_mod and old_mod in text:
                text = text.replace(old_mod, new_mod)
                replacements.append({"kind": "import", "from": old_mod, "to": new_mod})

    if text == original:
        rec["reason"] = "unchanged"
        rec["before_hash"] = before_hash
        rec["after_hash"] = before_hash
        return rec

    rec["replacements"] = replacements
    rec["before_hash"] = before_hash
    if dry_run:
        rec["would_patch"] = True
        rec["after_hash"] = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
        return rec

    path.write_text(text, encoding="utf-8")
    rec["patched"] = True
    rec["after_hash"] = _file_hash(path)
    append_corps_repair_audit(
        vault_root,
        {
            "event": "test_compensation",
            "repair_type": "surgical_shared_anchor",
            "proof_path": rel,
            "before_hash": before_hash,
            "after_hash": rec["after_hash"],
            "replacements": replacements,
        },
    )
    return rec


def blanket_rewrite_for_card(
    vault_root: Path,
    tid: str,
    *,
    archived_card: dict[str, Any],
    locked_paths: set[str],
    dry_run: bool = False,
    regenerate_burn: bool = False,
) -> dict[str, Any]:
    """Blanket smoke test for regen'd card unless its proof path is locked-touched."""
    vault_root = vault_root.resolve()
    rec: dict[str, Any] = {"trinity_id": tid, "mode": "blanket", "rewritten": False}

    try:
        card = load_trinity_card(vault_root, tid, prefer="provisional")
    except (OSError, ValueError, FileNotFoundError):
        primary = _primary_paths(archived_card)
        primary_path = primary[0] if primary else f"scripts/eat_queue_core/{tid}.py"
        card = {"touch": {"primary_paths": [primary_path]}}
    else:
        primary = _primary_paths(card)
        primary_path = primary[0] if primary else f"scripts/eat_queue_core/{tid}.py"

    test_path = smoke_test_path_for_module(vault_root, primary_path)
    if test_path is None:
        rec["reason"] = "no_test_path_for_primary"
        return rec

    rel_test = test_path.relative_to(vault_root).as_posix()
    rec["proof_path"] = rel_test
    rec["primary_path"] = primary_path

    if rel_test in locked_paths:
        rec["skipped"] = True
        rec["reason"] = "locked_touched_shared_anchor"
        return rec

    if dry_run:
        rec["would_rewrite"] = True
        return rec

    rewrite_blanket_smoke_test(vault_root, primary_path, trinity_id=tid)
    card = load_trinity_card(vault_root, tid, prefer="provisional")
    card.setdefault("contract", {})["proof"] = [rel_test]
    scan = normalize_card(dict(card))
    proposed = propose_behavior_signals(vault_root, scan)
    if proposed:
        card.setdefault("touch", {})["behavior_signals"] = proposed[:16]
    write_trinity_card(
        vault_root,
        tid,
        card,
        tier="provisional",
        mutation_action="corps_regenerate_test_compensation",
        operator_override=regenerate_burn or None,
    )

    rec["rewritten"] = True
    rec["behavior_signals"] = (card.get("touch") or {}).get("behavior_signals", [])[:8]
    append_corps_repair_audit(
        vault_root,
        {
            "event": "test_compensation",
            "repair_type": "blanket_rewrite",
            "trinity_id": tid,
            "proof_path": rel_test,
            "primary_path": primary_path,
        },
    )
    return rec


def blanket_rewrite_shared_non_locked(
    vault_root: Path,
    proof_path: str,
    *,
    primary_path: str,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Start fresh on shared tests that are not locked-touched."""
    rel = _norm_path(proof_path)
    rec: dict[str, Any] = {"proof_path": rel, "mode": "blanket_shared", "rewritten": False}
    if dry_run:
        rec["would_rewrite"] = True
        return rec
    rewrite_blanket_smoke_test(
        vault_root,
        primary_path,
        trinity_id=None,
        dest_rel_path=rel,
    )
    rec["rewritten"] = True
    append_corps_repair_audit(
        vault_root,
        {
            "event": "test_compensation",
            "repair_type": "blanket_shared_anchor",
            "proof_path": rel,
            "primary_path": primary_path,
        },
    )
    return rec


def _test_module_dotted(vault_root: Path, rel_test: str) -> str:
    """``eat_queue_core.tests.test_foo`` from repo-relative test path."""
    p = (vault_root / rel_test).resolve()
    scripts = (vault_root / "scripts").resolve()
    rel = p.relative_to(scripts)
    return ".".join(rel.with_suffix("").parts)


def _is_pytest_style_file(vault_root: Path, rel_test: str) -> bool:
    py_path = vault_root / rel_test
    try:
        head = py_path.read_text(encoding="utf-8", errors="replace")[:12000]
    except OSError:
        return False
    return (
        "import pytest" in head
        or "@pytest.fixture" in head
        or "@pytest.mark" in head
    )


def _proof_subprocess_env(vault_root: Path) -> dict[str, str]:
    """Same contract as ``trinity_behavior_proof._run_subprocess_proof``."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str((vault_root / "scripts").resolve())
    env.setdefault("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "1")
    return env


def verify_compensation_proof_file(vault_root: Path, rel_test: str) -> dict[str, Any]:
    """Run the proof file — unittest for 10e-b smoke tests; pytest only when file uses pytest.

    Raw ``python3 -m pytest`` without ``PYTEST_DISABLE_PLUGIN_AUTOLOAD`` can fail before
    any test runs (broken third-party plugins). This gate must actually execute tests.
    """
    vault_root = vault_root.resolve()
    rel = _norm_path(rel_test)
    py_path = vault_root / rel
    if not py_path.is_file():
        return {
            "proof_path": rel,
            "ok": False,
            "runner": "none",
            "detail": "missing_test_file",
        }

    env = _proof_subprocess_env(vault_root)
    if _is_pytest_style_file(vault_root, rel):
        runner = "pytest"
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            rel,
            "-q",
            "--tb=line",
            "--no-header",
        ]
    else:
        runner = "unittest"
        cmd = [sys.executable, "-m", "unittest", _test_module_dotted(vault_root, rel)]

    try:
        proc = subprocess.run(
            cmd,
            cwd=str(vault_root),
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        return {
            "proof_path": rel,
            "ok": False,
            "runner": runner,
            "detail": "timeout after 120s",
        }
    except OSError as e:
        return {
            "proof_path": rel,
            "ok": False,
            "runner": runner,
            "detail": str(e),
        }

    tail = (proc.stderr or proc.stdout or "").strip()
    if len(tail) > 500:
        tail = tail[-500:]
    out: dict[str, Any] = {
        "proof_path": rel,
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "runner": runner,
        "stderr_tail": tail,
    }
    if proc.returncode != 0 and not tail:
        out["detail"] = f"exit {proc.returncode}"
    plugin_load_failed = (
        runner == "pytest"
        and "VerifiedHTTPSConnection" in tail
        and "pytest" in tail.lower()
    )
    if plugin_load_failed:
        out["failure_class"] = "pytest_plugin_load"
        out["detail"] = (
            "pytest exited before running tests (plugin autoload); "
            "retry uses PYTEST_DISABLE_PLUGIN_AUTOLOAD=1"
        )
    return out


def run_test_compensation(
    vault_root: Path,
    *,
    archive_ids: list[str],
    archived_cards: dict[str, dict[str, Any]],
    ownership: dict[str, Any],
    regen_tids: list[str],
    dry_run: bool = False,
    regenerate_burn: bool = False,
    skip_proof_verify: bool = False,
) -> dict[str, Any]:
    """10e-b: blanket rewrite all non-locked tests; surgical only for locked-touch shared anchors."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    mode = getattr(cfg, "corps_regenerate_test_compensation_mode", "paired")
    enabled = getattr(cfg, "corps_regenerate_test_compensation_enabled", True)
    surgical = getattr(cfg, "corps_shared_test_surgical_adapt", True)

    rec: dict[str, Any] = {
        "ok": True,
        "enabled": enabled,
        "mode": mode,
        "dry_run": dry_run,
        "blanket_rewrites": [],
        "surgical_patches": [],
        "shared_blanket_rewrites": [],
        "verification_failures": [],
        "pytest_failures": [],  # legacy alias; same rows as verification_failures
    }

    if not enabled or mode == "anchor_only":
        rec["skipped"] = True
        rec["reason"] = "test_compensation_disabled_or_anchor_only"
        return rec

    locked_paths = locked_touched_proof_paths(ownership)
    rec["locked_touched_paths"] = sorted(locked_paths)
    regen_set = set(regen_tids)

    blanket_count = 0
    for tid in regen_tids:
        archived = archived_cards.get(tid)
        if not archived:
            continue
        row = blanket_rewrite_for_card(
            vault_root,
            tid,
            archived_card=archived,
            locked_paths=locked_paths,
            dry_run=dry_run,
            regenerate_burn=regenerate_burn,
        )
        rec["blanket_rewrites"].append(row)
        if row.get("rewritten") or row.get("would_rewrite"):
            blanket_count += 1

    surgical_count = 0
    skipped_unchanged = 0
    if surgical:
        for anchor in ownership.get("shared_anchors") or []:
            proof_path = _norm_path(anchor.get("proof_path") or "")
            if not proof_path or proof_path not in locked_paths:
                continue
            archived_in_batch = set(anchor.get("archived_card_ids") or []) & regen_set
            if not archived_in_batch:
                continue
            patch = surgical_adapt_shared_anchor(
                vault_root,
                proof_path,
                archived_cards=archived_cards,
                regen_tids=archived_in_batch,
                dry_run=dry_run,
            )
            rec["surgical_patches"].append(patch)
            if patch.get("patched") or patch.get("would_patch"):
                surgical_count += 1
            elif patch.get("reason") == "unchanged":
                skipped_unchanged += 1

    shared_blanket_count = 0
    for anchor in ownership.get("shared_anchors") or []:
        proof_path = _norm_path(anchor.get("proof_path") or "")
        if not proof_path or proof_path in locked_paths:
            continue
        archived_in_batch = set(anchor.get("archived_card_ids") or []) & regen_set
        if not archived_in_batch:
            continue
        first_tid = sorted(archived_in_batch)[0]
        archived = archived_cards.get(first_tid) or {}
        primary = _primary_paths(archived)
        primary_path = primary[0] if primary else f"scripts/eat_queue_core/{first_tid}.py"
        row = blanket_rewrite_shared_non_locked(
            vault_root,
            proof_path,
            primary_path=primary_path,
            dry_run=dry_run,
        )
        rec["shared_blanket_rewrites"].append(row)
        if row.get("rewritten") or row.get("would_rewrite"):
            shared_blanket_count += 1

    rec["sole_owned_reauthored"] = blanket_count
    rec["shared_surgical_patched"] = surgical_count
    rec["shared_blanket_rewritten"] = shared_blanket_count
    rec["shared_skipped_unchanged"] = skipped_unchanged

    if not dry_run and not skip_proof_verify:
        verify_targets: set[str] = set()
        for row in rec["blanket_rewrites"]:
            if row.get("rewritten") and row.get("proof_path"):
                verify_targets.add(row["proof_path"])
        for row in rec["surgical_patches"]:
            if row.get("patched") and row.get("proof_path"):
                verify_targets.add(row["proof_path"])
        for row in rec["shared_blanket_rewrites"]:
            if row.get("rewritten") and row.get("proof_path"):
                verify_targets.add(row["proof_path"])
        failures: list[dict[str, Any]] = []
        verified_ok = 0
        for rel in sorted(verify_targets):
            pr = verify_compensation_proof_file(vault_root, rel)
            if pr.get("ok"):
                verified_ok += 1
            else:
                failures.append(pr)
        rec["proofs_verified_ok"] = verified_ok
        rec["proofs_verified_total"] = len(verify_targets)
        rec["verification_failures"] = failures
        rec["pytest_failures"] = failures
        rec["compensation_ok"] = len(failures) == 0
        if failures:
            rec["ok"] = False
    elif not dry_run and skip_proof_verify:
        rec["proofs_verified_ok"] = 0
        rec["proofs_verified_total"] = 0
        rec["verification_skipped"] = True
        rec["compensation_ok"] = True

    rec["blanket_rewrites"] = rec["blanket_rewrites"][:40]
    rec["surgical_patches"] = rec["surgical_patches"][:20]
    rec["shared_blanket_rewrites"] = rec["shared_blanket_rewrites"][:20]
    return rec
