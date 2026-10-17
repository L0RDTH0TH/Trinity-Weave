#!/usr/bin/env python3
"""CLI — Gate A ticket-map Prefer fidelity + Gate B hostile latch check.

Usage (vault root):
  PYTHONPATH=scripts python3 scripts/prefer_map_fidelity_check.py \\
    --armed 1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs/SLICE.armed.yaml

Exit 0 = ok (or not applicable). Exit 2 = violations.

Hostile Prefer (Gate B) is required for Prefer-applicable Success claims
(staging and KEEP). Run Task(validator) prefer_map_fidelity to set
map_fidelity_hostile_ok before claiming Success.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running from vault root without install
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from eat_queue_core.weave.factory.prefer_map_fidelity import (  # noqa: E402
    keep_latch_allowed,
    load_armed_yaml,
    load_prefer_result,
    validate_armed_map_fidelity,
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--vault",
        type=Path,
        default=Path.cwd(),
        help="Vault root (default: cwd)",
    )
    ap.add_argument(
        "--armed",
        type=Path,
        required=True,
        help="Path to *.armed.yaml (absolute or vault-relative)",
    )
    ap.add_argument(
        "--keep-latch",
        action="store_true",
        help="Also require hostile Prefer + operator F5 (pretend ask_success latch)",
    )
    ap.add_argument(
        "--operator-f5",
        action="store_true",
        help="With --keep-latch, mark operator F5 as ok",
    )
    ap.add_argument("--json", action="store_true", help="Print JSON result")
    args = ap.parse_args()
    vault = args.vault.resolve()
    armed_path = args.armed if args.armed.is_absolute() else vault / args.armed
    if not armed_path.is_file():
        print(f"missing_armed:{armed_path}", file=sys.stderr)
        return 2
    armed = load_armed_yaml(armed_path)
    pr = load_prefer_result(vault, str(armed.get("slice_id") or ""))
    if args.keep_latch:
        result = keep_latch_allowed(
            vault, armed, prefer_result=pr, operator_f5_ok=args.operator_f5
        )
    else:
        result = validate_armed_map_fidelity(vault, armed, prefer_result=pr)
    if args.json:
        print(json.dumps(result.as_dict(), indent=2))
    else:
        print(
            f"applicable={result.applicable} ok={result.ok} "
            f"gate_a={result.gate_a_applicable} gate_b={result.gate_b_applicable} "
            f"ticket_map_id={result.ticket_map_id or '-'}"
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
