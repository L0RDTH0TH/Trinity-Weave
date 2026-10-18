#!/usr/bin/env python3
"""Ticket-map battery — arrow-key Map→Ticket picker → FACTORY WELD clipboard.

Vault-wide: any conforming ticket_map (see Docs/Ticket-Map-Schema.md).
Not project-specific.

Picker source of truth = map ∩ Prefer (*.armed.yaml with ticket_map_id on that map).
Prefer is a draft until Gate B₁ (map_fidelity_hostile_ok: true); only then is it
launchable. f5_good Prefer-linked rows are the primary grey trail.
Multiple Prefer slices per map id → multiple list rows (same ticket_map_id under the hood).

Usage:
  PYTHONPATH=scripts python3 scripts/factory_weld_launch_clip.py
  PYTHONPATH=scripts python3 scripts/factory_weld_launch_clip.py --map world-builder-mini-game
  PYTHONPATH=scripts python3 scripts/factory_weld_launch_clip.py --ticket-map-id PLACE-product
  PYTHONPATH=scripts python3 scripts/factory_weld_launch_clip.py --stdout-only --dry-run
  PYTHONPATH=scripts python3 scripts/factory_weld_launch_clip.py --all-tickets  # B₁-pending + deferred (disabled)
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# Allow running as scripts/factory_weld_launch_clip.py from vault root
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from eat_queue_core.weave.factory.ticket_map_schema import (  # noqa: E402
    SELECTABLE_TICKET_STATUS,
    LivePickerRow,
    TicketMapDoc,
    build_factory_weld_prompt,
    build_live_picker_rows,
    discover_ticket_maps,
    format_live_picker_label,
    prefer_dict_from_live_row,
    resolve_prefer_for_ticket,
)


def _vault_root() -> Path:
    # scripts/ → vault root
    return Path(__file__).resolve().parent.parent


def _copy_clipboard(text: str) -> bool:
    for cmd in (
        ["wl-copy"],
        ["xclip", "-selection", "clipboard"],
        ["pbcopy"],
    ):
        if not shutil.which(cmd[0]):
            continue
        try:
            subprocess.run(
                cmd,
                input=text.encode("utf-8"),
                check=True,
                timeout=10,
            )
            return True
        except (OSError, subprocess.SubprocessError):
            continue
    return False


def _pick_map(maps: list[TicketMapDoc]) -> TicketMapDoc | None:
    try:
        import questionary
        from questionary import Choice
    except ImportError:
        print(
            "questionary required for interactive pick: "
            "pip install -r scripts/eat_queue_core/requirements.txt",
            file=sys.stderr,
        )
        return None

    choices = []
    for m in maps:
        star = ""
        if m.active_recovery:
            star = f"  ★ recovery={m.active_recovery}"
        label = (
            f"{m.title}  [{m.map_status}]  project={m.project_id or '?'}  "
            f"updated={m.updated or m.created or '?'}{star}"
        )
        choices.append(Choice(title=label, value=m))
    if not choices:
        print("No ticket maps found (ticket_map: true, map_status != deferred).", file=sys.stderr)
        return None
    return questionary.select(
        "Ticket map (newest first):",
        choices=choices,
        use_shortcuts=False,
        use_arrow_keys=True,
    ).ask()


def _pick_live_ticket(
    vault: Path,
    map_doc: TicketMapDoc,
    *,
    show_hidden: bool = False,
) -> LivePickerRow | None:
    try:
        import questionary
        from questionary import Choice
    except ImportError:
        print("questionary required", file=sys.stderr)
        return None

    ordered = build_live_picker_rows(
        vault, map_doc, show_hidden=show_hidden
    )
    if not ordered:
        print(
            "No Prefer-linked tickets on this map "
            "(need *.armed.yaml with ticket_map_id matching a map row).",
            file=sys.stderr,
        )
        return None

    id_width = max((len(r.ticket_map_id) for r in ordered), default=22)
    id_width = max(id_width, 12)
    slice_width = max((len(r.slice_id) for r in ordered), default=8)
    choices = []
    launchable = 0
    for row in ordered:
        label = format_live_picker_label(
            row,
            recovery_id=map_doc.active_recovery or "",
            id_width=id_width,
            slice_width=slice_width,
        )
        if row.launchable:
            choices.append(Choice(title=label, value=row))
            launchable += 1
        elif row.b1_pending:
            choices.append(
                Choice(
                    title=label,
                    value=row,
                    disabled="B₁ pending",
                )
            )
        elif row.trail:
            choices.append(
                Choice(
                    title=label,
                    value=row,
                    disabled="F5 trail — browse only (same ticket_map_id)",
                )
            )
        else:
            choices.append(
                Choice(title=label, value=row, disabled=row.status or "hidden")
            )

    if launchable == 0:
        print(
            "No launchable Prefer∩map rows (need Status open + map_fidelity_hostile_ok). "
            "Pass Gate B₁, or use --all-tickets to browse B₁-pending drafts.",
            file=sys.stderr,
        )

    return questionary.select(
        "Prefer∩map (id · slice; open+B₁=launch; f5_good=trail):",
        choices=choices,
        use_arrow_keys=True,
    ).ask()


def _resolve_map_by_id(vault: Path, map_id: str) -> TicketMapDoc | None:
    for m in discover_ticket_maps(vault, include_deferred_maps=True):
        if m.map_id == map_id or m.rel_path.endswith(map_id):
            if m.map_status == "deferred":
                print(f"Map {map_id} is deferred (hidden from default list).", file=sys.stderr)
            return m
    return None


def _resolve_ticket_across_maps(vault: Path, ticket_map_id: str):
    for m in discover_ticket_maps(vault, include_deferred_maps=True):
        t = m.tickets.get(ticket_map_id)
        if t:
            return m, t
    return None, None


def _pick_live_for_ticket_id(
    vault: Path,
    map_doc: TicketMapDoc,
    ticket_map_id: str,
    *,
    slice_hint: str = "",
) -> LivePickerRow | None:
    rows = [
        r
        for r in build_live_picker_rows(vault, map_doc, show_hidden=True)
        if r.ticket_map_id == ticket_map_id
    ]
    if not rows:
        return None
    if slice_hint:
        for r in rows:
            if r.slice_id == slice_hint:
                return r
    # recovery slice, else newest
    if map_doc.active_recovery == ticket_map_id and map_doc.active_recovery_slice:
        for r in rows:
            if r.slice_id == map_doc.active_recovery_slice:
                return r
    rows.sort(key=lambda r: r.mtime, reverse=True)
    return rows[0]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="FACTORY WELD launch prompt → clipboard")
    ap.add_argument("--vault-root", type=Path, default=None)
    ap.add_argument("--map", dest="map_id", default="", help="map_id skip map picker")
    ap.add_argument("--ticket-map-id", default="", help="ticket id skip ticket picker")
    ap.add_argument("--slice", dest="slice_id", default="", help="Prefer slice hint")
    ap.add_argument("--stdout-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="print only; no clipboard")
    ap.add_argument(
        "--all-tickets",
        action="store_true",
        help=(
            "include B₁-pending Prefer drafts and deferred/superseded "
            "Prefer-linked rows (disabled; still non-launch)"
        ),
    )
    args = ap.parse_args(argv)

    vault = (args.vault_root or _vault_root()).resolve()
    maps = discover_ticket_maps(vault)
    if not maps and not args.map_id:
        print("No ticket maps discovered under 1-Projects / 3-Resources.", file=sys.stderr)
        return 1

    map_doc: TicketMapDoc | None = None
    live: LivePickerRow | None = None
    ticket = None

    if args.ticket_map_id and not args.map_id:
        map_doc, ticket = _resolve_ticket_across_maps(vault, args.ticket_map_id)
        if not map_doc or not ticket:
            print(f"ticket_map_id not found: {args.ticket_map_id}", file=sys.stderr)
            return 1
        live = _pick_live_for_ticket_id(
            vault, map_doc, args.ticket_map_id, slice_hint=args.slice_id
        )
    else:
        if args.map_id:
            map_doc = _resolve_map_by_id(vault, args.map_id)
            if map_doc is None:
                print(f"map_id not found: {args.map_id}", file=sys.stderr)
                return 1
        else:
            map_doc = _pick_map(maps)
            if map_doc is None:
                return 1

        if args.ticket_map_id:
            ticket = map_doc.tickets.get(args.ticket_map_id)
            if ticket is None:
                print(
                    f"ticket {args.ticket_map_id} not on map {map_doc.map_id}",
                    file=sys.stderr,
                )
                return 1
            live = _pick_live_for_ticket_id(
                vault, map_doc, args.ticket_map_id, slice_hint=args.slice_id
            )
        else:
            live = _pick_live_ticket(vault, map_doc, show_hidden=args.all_tickets)
            if live is None:
                return 1
            ticket = live.ticket

    if live is None and ticket is not None:
        # CLI ticket id without Prefer — still emit prompt with prefer_missing
        slice_hint = args.slice_id or map_doc.active_recovery_slice or ""
        if map_doc.active_recovery == ticket.ticket_map_id and map_doc.active_recovery_slice:
            slice_hint = map_doc.active_recovery_slice
        prefer = resolve_prefer_for_ticket(
            vault,
            project_id=map_doc.project_id,
            ticket_map_id=ticket.ticket_map_id,
            slice_hint=slice_hint,
        )
    else:
        assert live is not None and map_doc is not None
        ticket = live.ticket
        prefer = prefer_dict_from_live_row(vault, live)
        if args.slice_id and live.slice_id != args.slice_id:
            # honor explicit --slice over picker/default
            prefer = resolve_prefer_for_ticket(
                vault,
                project_id=map_doc.project_id,
                ticket_map_id=ticket.ticket_map_id,
                slice_hint=args.slice_id,
            )

    if live is not None and live.b1_pending:
        print(
            f"Selected slice {live.slice_id} is B₁ pending "
            "(map_fidelity_hostile_ok not true) — prompt still emitted for browse; "
            "do not GREENLIGHT until Gate B₁ passes.",
            file=sys.stderr,
        )
    elif ticket.status != SELECTABLE_TICKET_STATUS:
        print(
            f"Selected ticket status={ticket.status} (not open) — "
            "prompt still emitted for browse; do not GREENLIGHT until Status is open.",
            file=sys.stderr,
        )

    prompt = build_factory_weld_prompt(map_doc=map_doc, ticket=ticket, prefer=prefer)
    print(prompt)
    if args.dry_run or args.stdout_only:
        if args.stdout_only and not args.dry_run:
            pass
        return 0
    if _copy_clipboard(prompt):
        print("\n--- copied to clipboard — paste into Cursor when validated ---", file=sys.stderr)
    else:
        print(
            "\n--- clipboard unavailable; copy from stdout ---",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
