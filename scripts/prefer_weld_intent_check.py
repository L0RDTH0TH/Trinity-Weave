#!/usr/bin/env python3
"""CLI — Gate B₂ weld intent hostile latch (post-weld).

Usage (vault root):
  PYTHONPATH=scripts python3 scripts/prefer_weld_intent_check.py \\
    --armed 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/SLICE.armed.yaml

  PYTHONPATH=scripts python3 scripts/prefer_weld_intent_check.py \\
    --receipt path/to/receipt.md

Exit 0 = ok (or not applicable / bypass). Exit 2 = violations.

Smoke path (documented): after Gate B₁ → GREENLIGHT → weld LIVE → run B₂
(VALIDATE prefer_weld_intent → weld_intent_hostile_ok) → operator F5.
Do not treat proof tags / factory logs as pass evidence.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from eat_queue_core.weave.factory.prefer_weld_intent import (  # noqa: E402
    evaluate_behavior_evidence,
    load_armed_yaml,
    load_prefer_result,
    post_weld_keep_latch,
    scan_chat_hotfix_receipt,
    validate_weld_intent_latch,
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vault", type=Path, default=Path.cwd())
    ap.add_argument("--armed", type=Path, help="Path to *.armed.yaml")
    ap.add_argument("--receipt", type=Path, help="Chat/hotfix receipt (.md/.json)")
    ap.add_argument(
        "--evidence-json",
        type=Path,
        help="Optional evidence pack JSON (behavior checklist)",
    )
    ap.add_argument(
        "--keep-latch",
        action="store_true",
        help="Also require B₁ + B₂ + operator F5",
    )
    ap.add_argument("--operator-f5", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    vault = args.vault.resolve()

    evidence = None
    if args.evidence_json:
        ep = (
            args.evidence_json
            if args.evidence_json.is_absolute()
            else vault / args.evidence_json
        )
        evidence = json.loads(ep.read_text(encoding="utf-8"))

    if args.receipt:
        rpath = args.receipt if args.receipt.is_absolute() else vault / args.receipt
        text = rpath.read_text(encoding="utf-8", errors="replace")
        pr = None
        if args.armed:
            apath = args.armed if args.armed.is_absolute() else vault / args.armed
            armed = load_armed_yaml(apath)
            pr = load_prefer_result(vault, str(armed.get("slice_id") or ""))
        result = scan_chat_hotfix_receipt(text, prefer_result=pr)
        if evidence:
            beh = evaluate_behavior_evidence(evidence)
            result.violations = sorted(set(result.violations + beh.violations))
            result.ok = result.ok and beh.ok
            result.evidence_pack = beh.evidence_pack
    elif args.armed:
        apath = args.armed if args.armed.is_absolute() else vault / args.armed
        if not apath.is_file():
            print(f"missing_armed:{apath}", file=sys.stderr)
            return 2
        armed = load_armed_yaml(apath)
        pr = load_prefer_result(vault, str(armed.get("slice_id") or ""))
        if args.keep_latch:
            result = post_weld_keep_latch(
                armed,
                prefer_result=pr,
                evidence_pack=evidence,
                operator_f5_ok=args.operator_f5,
            )
        else:
            result = validate_weld_intent_latch(
                armed, prefer_result=pr, evidence_pack=evidence
            )
    else:
        print("need --armed and/or --receipt", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result.as_dict(), indent=2))
    else:
        print(
            f"applicable={result.applicable} ok={result.ok} "
            f"live_weld={result.live_weld_claimed} bypass={result.bypass}"
        )
        for v in result.violations:
            print(f"VIOLATION {v}")
        for w in result.warnings:
            print(f"WARNING {w}")
    if not result.applicable:
        return 0
    return 0 if result.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
