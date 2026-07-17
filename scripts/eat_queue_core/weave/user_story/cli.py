"""CLI for user-story operator loop and roadmap factory."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .operator_user_story_confirm import confirm_catalog_sign, confirm_user_story_row
from .scope_validation import confirm_scopes_validated, list_scope_validation_status
from .operator_user_story_session import run_operator_user_story_session
from .roadmap_factory_handlers import handle_roadmap_factory_entry
from .product_factory_pipeline import (
    bootstrap as product_factory_bootstrap,
    confirm_slice_selection,
    product_factory_status,
    tick as product_factory_tick,
)
from .user_story_brief import write_user_story_brief
from .user_story_feedback import list_pending_user_story_confirmations
from .user_story_session_ingest import ingest_user_story_session


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="User story / roadmap factory CLI")
    parser.add_argument("--vault-root", type=Path, default=Path("."))
    sub = parser.add_subparsers(dest="cmd", required=True)

    usb = sub.add_parser("user-story-brief", help="Write operator UserStory-Brief")
    usb.add_argument("--project-id", default="godot-genesis-mythos-master")

    ops = sub.add_parser("operator-user-story-session", help="Ingest session + list pending")
    ops.add_argument("--project-id", default="godot-genesis-mythos-master")
    ops.add_argument("--session", type=Path, default=None)

    ing = sub.add_parser("user-story-ingest", help="Ingest user_story_mark JSONL session")
    ing.add_argument("--project-id", default="godot-genesis-mythos-master")
    ing.add_argument("--session", type=Path, default=None)
    ing.add_argument("--dry-run", action="store_true")

    oc = sub.add_parser("operator-user-story-confirm", help="Confirm row or catalog sign")
    oc.add_argument("--project-id", default="godot-genesis-mythos-master")
    oc.add_argument("--list", action="store_true")
    oc.add_argument("--row-id", default=None)
    oc.add_argument("--pass", dest="pass_val", type=str, default=None)
    oc.add_argument("--notes", default="")
    oc.add_argument("--confirm", action="store_true")
    oc.add_argument("--catalog-sign", action="store_true")

    rel = sub.add_parser(
        "roadmap-factory-relaunch",
        help="Deprecated — use roadmap-factory-bootstrap (resets factory cursor)",
    )
    rel.add_argument("--project-id", default="godot-genesis-mythos-master")
    rel.add_argument("--pmg-path", default=None)
    rel.add_argument("--skip-operator-gates", action="store_true")
    rel.add_argument("--dry-run", action="store_true")

    rfb = sub.add_parser(
        "roadmap-factory-bootstrap",
        help="First factory boot — reset product_factory cursor + conductor tick",
    )
    rfb.add_argument("--project-id", default="godot-genesis-mythos-master")
    rfb.add_argument("--pmg-path", default=None)
    rfb.add_argument("--skip-operator-gates", action="store_true")
    rfb.add_argument("--dry-run", action="store_true")

    pfr = sub.add_parser(
        "product-factory-relaunch",
        help="Deprecated — use product-factory-bootstrap (resets factory cursor)",
    )
    pfr.add_argument("--project-id", default="godot-genesis-mythos-master")
    pfr.add_argument("--pmg-path", default=None)
    pfr.add_argument("--dry-run", action="store_true")
    pfr.add_argument("--skip-agent-enqueue", action="store_true")

    pfb = sub.add_parser(
        "product-factory-bootstrap",
        help="First factory boot — reset product_factory cursor + conductor tick",
    )
    pfb.add_argument("--project-id", default="godot-genesis-mythos-master")
    pfb.add_argument("--pmg-path", default=None)
    pfb.add_argument("--dry-run", action="store_true")
    pfb.add_argument("--skip-agent-enqueue", action="store_true")

    pfs = sub.add_parser("product-factory-status", help="Product factory phase + operator loops")
    pfs.add_argument("--project-id", default="godot-genesis-mythos-master")

    pft = sub.add_parser("product-factory-tick", help="Advance conductor one pass")
    pft.add_argument("--project-id", default="godot-genesis-mythos-master")
    pft.add_argument("--dry-run", action="store_true")
    pft.add_argument("--skip-agent-enqueue", action="store_true")

    pfc = sub.add_parser("product-factory-confirm-slice", help="Loop 3 — confirm active slice")
    pfc.add_argument("--project-id", default="godot-genesis-mythos-master")
    pfc.add_argument("--row-ids", required=True, help="Comma-separated catalog row ids")
    pfc.add_argument("--dispatch-depth", type=int, required=True)

    ds = sub.add_parser("depth-slice", help="L5 complete → L4..L1 scope files (top-down)")
    ds.add_argument("--project-id", default="godot-genesis-mythos-master")
    ds.add_argument("--row-id", default=None)
    ds.add_argument("--row-ids", default=None, help="Comma-separated row ids")
    ds.add_argument("--no-bootstrap", action="store_true")

    osv = sub.add_parser(
        "operator-scope-validate",
        help="Loop 2 — operator attestation of L5..target_depth scope files per row",
    )
    osv.add_argument("--project-id", default="godot-genesis-mythos-master")
    osv.add_argument("--list", action="store_true")
    osv.add_argument("--row-id", default=None)
    osv.add_argument("--notes", default="")
    osv.add_argument("--confirm", action="store_true")

    hnd = sub.add_parser("handle-mode", help="Run one roadmap factory queue mode")
    hnd.add_argument("--mode", required=True)
    hnd.add_argument("--project-id", default="godot-genesis-mythos-master")
    hnd.add_argument("--params-json", default="{}")

    args = parser.parse_args(argv)
    root = args.vault_root.resolve()
    pid = args.project_id

    if args.cmd == "user-story-brief":
        out = write_user_story_brief(root, project_id=pid)
        print(json.dumps(out.to_dict(), indent=2))
        return 0 if out.ok else 1

    if args.cmd == "operator-user-story-session":
        out = run_operator_user_story_session(root, project_id=pid, session_path=args.session)
        print(json.dumps(out.to_dict(), indent=2))
        return 0 if out.ok else 1

    if args.cmd == "user-story-ingest":
        out = ingest_user_story_session(
            root,
            project_id=pid,
            session_path=args.session,
            write_feedback=not args.dry_run,
        )
        print(json.dumps(out.to_dict(), indent=2))
        return 0 if out.ok else 1

    if args.cmd == "operator-user-story-confirm":
        if args.list:
            pending = list_pending_user_story_confirmations(root, pid)
            print(json.dumps({"pending": pending}, indent=2))
            return 0
        if args.catalog_sign:
            out = confirm_catalog_sign(root, project_id=pid)
            print(json.dumps(out.to_dict(), indent=2))
            return 0 if out.ok else 1
        if not args.row_id:
            print(json.dumps({"ok": False, "error": "row_id_or_catalog_sign_required"}), file=sys.stderr)
            return 2
        pv = args.pass_val
        if pv is None:
            print(json.dumps({"ok": False, "error": "pass_required"}), file=sys.stderr)
            return 2
        out = confirm_user_story_row(
            root,
            project_id=pid,
            row_id=args.row_id,
            pass_=str(pv).lower() in ("true", "1", "yes"),
            notes=args.notes,
            operator_confirmed=args.confirm or True,
        )
        print(json.dumps(out.to_dict(), indent=2))
        return 0 if out.ok else 1

    if args.cmd in ("roadmap-factory-relaunch", "roadmap-factory-bootstrap"):
        params: dict = {}
        if args.pmg_path:
            params["pmg_path"] = args.pmg_path
        if args.skip_operator_gates:
            params["skip_agent_enqueue"] = True
        if args.dry_run:
            params["dry_run"] = True
        if args.cmd == "roadmap-factory-relaunch":
            print(
                "warning: roadmap-factory-relaunch is deprecated; use roadmap-factory-bootstrap",
                file=sys.stderr,
            )
        out = product_factory_bootstrap(root, project_id=pid, params=params)
        print(json.dumps(out, indent=2))
        return 0 if out.get("ok") or out.get("blocked_at") else 1

    if args.cmd in ("product-factory-relaunch", "product-factory-bootstrap"):
        params = {}
        if args.pmg_path:
            params["pmg_path"] = args.pmg_path
        if args.dry_run:
            params["dry_run"] = True
        if args.skip_agent_enqueue:
            params["skip_agent_enqueue"] = True
        if args.cmd == "product-factory-relaunch":
            print(
                "warning: product-factory-relaunch is deprecated; use product-factory-bootstrap",
                file=sys.stderr,
            )
        out = product_factory_bootstrap(root, project_id=pid, params=params)
        print(json.dumps(out, indent=2))
        return 0 if out.get("ok") or out.get("blocked_at") else 1

    if args.cmd == "product-factory-status":
        out = product_factory_status(root, project_id=pid)
        print(json.dumps(out, indent=2))
        return 0

    if args.cmd == "product-factory-tick":
        params = {}
        if args.dry_run:
            params["dry_run"] = True
        if args.skip_agent_enqueue:
            params["skip_agent_enqueue"] = True
        out = product_factory_tick(root, project_id=pid, params=params)
        print(json.dumps(out.to_dict(), indent=2))
        return 0 if out.ok or out.blocked_at else 1

    if args.cmd == "product-factory-confirm-slice":
        row_ids = [x.strip() for x in args.row_ids.split(",") if x.strip()]
        out = confirm_slice_selection(
            root, project_id=pid, row_ids=row_ids, dispatch_depth=args.dispatch_depth
        )
        print(json.dumps(out, indent=2))
        return 0 if out.get("ok") else 1

    if args.cmd == "depth-slice":
        from .depth_slicer import run_depth_slicer

        row_ids = None
        if args.row_ids:
            row_ids = [x.strip() for x in args.row_ids.split(",") if x.strip()]
        out = run_depth_slicer(
            root,
            project_id=pid,
            row_id=args.row_id,
            row_ids=row_ids,
            bootstrap_l5=not args.no_bootstrap,
        )
        print(json.dumps(out, indent=2))
        return 0 if out.get("ok") else 1

    if args.cmd == "operator-scope-validate":
        if args.list:
            rows = list_scope_validation_status(root, project_id=pid)
            print(json.dumps({"rows": rows}, indent=2))
            return 0
        if not args.row_id:
            print(json.dumps({"ok": False, "error": "row_id_or_list_required"}), file=sys.stderr)
            return 1
        if not args.confirm:
            rows = list_scope_validation_status(root, project_id=pid, row_ids=[args.row_id])
            print(json.dumps({"preview": rows[0] if rows else {}, "hint": "pass --confirm to attest"}, indent=2))
            return 0
        out = confirm_scopes_validated(root, project_id=pid, row_id=args.row_id, notes=args.notes)
        print(json.dumps(out.to_dict(), indent=2))
        return 0 if out.ok else 1

    if args.cmd == "handle-mode":
        import json as _json

        params = _json.loads(args.params_json or "{}")
        out = handle_roadmap_factory_entry(
            root,
            {"id": "cli-handle", "mode": args.mode, "project_id": pid, "params": params},
        )
        print(json.dumps(out, indent=2))
        return 0 if out.get("ok") else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
