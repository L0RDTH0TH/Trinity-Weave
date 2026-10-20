#!/usr/bin/env python3
"""CLI — print Ticketment draft bundle for one ticket_map_id (JSON).

Usage (vault root):
  PYTHONPATH=scripts python3 scripts/prefer_ticketment_bundle.py \\
    --ticket WB-polygon-substrate
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from eat_queue_core.weave.factory.prefer_ticketment import (  # noqa: E402
    build_ticketment_bundle,
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vault", type=Path, default=Path.cwd())
    ap.add_argument("--ticket", required=True, help="ticket_map_id")
    ap.add_argument("--project-id", default=None)
    args = ap.parse_args()
    bundle = build_ticketment_bundle(
        args.vault.resolve(),
        args.ticket,
        project_id=args.project_id,
    )
    print(json.dumps(bundle, indent=2))
    return 0 if bundle.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
