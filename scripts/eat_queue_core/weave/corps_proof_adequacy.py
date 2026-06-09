"""Proof adequacy heuristic (Grok C / T2.5) — intent-conduct quality beyond import smoke."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .trinity_behavior_proof import find_test_file_for_signal, run_card_behavior_proofs
from .trinity_card import contract_proof_paths, get_touch


def _primary_case_text(card: dict[str, Any]) -> str:
    conceptual = card.get("conceptual") or {}
    if isinstance(conceptual, dict):
        return str(conceptual.get("primary_case") or "").lower()
    return ""


def _primary_path_modules(card: dict[str, Any]) -> set[str]:
    mods: set[str] = set()
    for raw in get_touch(card).get("primary_paths") or []:
        rel = str(raw).strip().replace("\\", "/")
        if rel.endswith(".py"):
            mods.add(Path(rel).stem.lower())
    return mods


def _test_body_adequacy(
    vault_root: Path,
    card: dict[str, Any],
    test_name: str,
) -> tuple[int, list[str]]:
    """Return (score 0-3, reasons)."""
    reasons: list[str] = []
    score = 0
    path = find_test_file_for_signal(vault_root, card, test_name)
    if not path or not path.is_file():
        return 0, ["no_test_file"]
    body = path.read_text(encoding="utf-8", errors="replace")
    if "importlib.import_module" in body and "assert" not in body:
        return 0, ["import_only"]
    score += 1
    reasons.append("has_assertions")
    mods = _primary_path_modules(card)
    if mods and any(m in body.lower() for m in mods):
        score += 1
        reasons.append("references_primary_module")
    case = _primary_case_text(card)
    if case:
        verbs = [w for w in re.findall(r"[a-z]{4,}", case) if w not in ("when", "that", "with", "from")]
        if any(v in body.lower() for v in verbs[:8]):
            score += 1
            reasons.append("maps_primary_case")
    rules = card.get("rules") or {}
    if isinstance(rules, dict):
        blob = json.dumps(rules, default=str).lower()
        for token in ("lane", "pseudo_clock", "isolate", "queue"):
            if token in blob and token in body.lower():
                score = min(3, score + 1)
                reasons.append(f"exercises_{token}")
                break
    return min(3, score), reasons[:4]


def score_proof_adequacy(
    vault_root: Path,
    card: dict[str, Any],
    *,
    proofs: list[Any] | None = None,
) -> dict[str, Any]:
    """Per-card adequacy 0–3 and whether signals resolve."""
    vault_root = vault_root.resolve()
    touch = get_touch(card)
    signals = [str(s).strip() for s in (touch.get("behavior_signals") or []) if str(s).strip()]
    proof_paths = list(contract_proof_paths(card))
    resolved = 0
    for sig in signals:
        if sig.startswith("test_") and find_test_file_for_signal(vault_root, card, sig):
            resolved += 1
    if proofs is None:
        proofs = run_card_behavior_proofs(vault_root, card)
    intent_tests = [
        p for p in proofs if getattr(p, "test_name", "").startswith("test_")
        and getattr(p, "test_name", "") != "test_module_importable"
    ]
    if not intent_tests:
        intent_tests = [p for p in proofs if getattr(p, "ok", False)]
    per_test: list[dict[str, Any]] = []
    best = 0
    for p in intent_tests[:6]:
        name = str(getattr(p, "test_name", "") or "")
        if not name.startswith("test_"):
            continue
        sc, why = _test_body_adequacy(vault_root, card, name)
        best = max(best, sc)
        per_test.append({"test_name": name, "score": sc, "reasons": why})
    if not per_test and signals:
        for sig in signals[:3]:
            if sig.startswith("test_"):
                sc, why = _test_body_adequacy(vault_root, card, sig)
                best = max(best, sc)
                per_test.append({"test_name": sig, "score": sc, "reasons": why})
    low = best < 2 and bool(signals)
    return {
        "proof_adequacy_score": best,
        "signals_total": len(signals),
        "signals_resolved": resolved,
        "proof_paths": proof_paths[:4],
        "per_test": per_test,
        "low_adequacy": low,
    }


def summarize_adequacy_from_nerves(nerves: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate low-adequacy count from nerve rows."""
    low = 0
    scores: list[int] = []
    for n in nerves:
        if not isinstance(n, dict):
            continue
        pa = n.get("proof_adequacy") or {}
        if isinstance(pa, dict):
            sc = int(pa.get("proof_adequacy_score") or 0)
            scores.append(sc)
            if pa.get("low_adequacy"):
                low += 1
    return {
        "low_adequacy_count": low,
        "avg_adequacy_score": round(sum(scores) / len(scores), 2) if scores else None,
        "tested_with_adequacy": len(scores),
    }
