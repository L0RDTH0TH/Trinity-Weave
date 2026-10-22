"""Vault-wide ticket-map schema + FACTORY GREENLIGHT WELD prompt (no project hardcode)."""

from __future__ import annotations

from pathlib import Path

from eat_queue_core.weave.factory.prefer_map_fidelity import (
    parse_ticket_map_rows as fidelity_parse,
)
from eat_queue_core.weave.factory.ticket_map_schema import (
    MapTicketRow,
    build_factory_weld_prompt,
    build_live_picker_rows,
    discover_ticket_maps,
    filter_tickets_for_picker,
    format_live_picker_label,
    format_picker_ticket_label,
    infer_ticket_status,
    load_ticket_map_doc,
    parse_ticket_map_rows,
    prefer_b1_ok,
    resolve_prefer_for_ticket,
    strip_job_markup,
    tickets_newest_first,
)

FIXTURE_VAULT = (
    Path(__file__).resolve().parent / "fixtures" / "ticket_maps_vault"
)


def test_discover_hides_deferred_map_keeps_complete():
    docs = discover_ticket_maps(FIXTURE_VAULT)
    ids = {d.map_id for d in docs}
    assert "alpha-fixture" in ids
    assert "beta-fixture" in ids
    assert "deferred-fixture" not in ids
    # newest updated first
    assert docs[0].map_id == "alpha-fixture"


def test_discover_include_deferred():
    docs = discover_ticket_maps(FIXTURE_VAULT, include_deferred_maps=True)
    assert any(d.map_id == "deferred-fixture" for d in docs)


def test_filter_tickets_hides_deferred_greys_f5():
    alpha = next(d for d in discover_ticket_maps(FIXTURE_VAULT) if d.map_id == "alpha-fixture")
    shown = filter_tickets_for_picker(alpha.tickets.values())
    statuses = {t.ticket_map_id: t.status for t in shown}
    assert "ALPHA-open" in statuses and statuses["ALPHA-open"] == "open"
    assert "ALPHA-done" in statuses and statuses["ALPHA-done"] == "f5_good"
    assert "ALPHA-park" not in statuses
    assert "ALPHA-old" not in statuses


def test_live_picker_map_intersect_prefer_multislices_and_trail():
    alpha = next(d for d in discover_ticket_maps(FIXTURE_VAULT) if d.map_id == "alpha-fixture")
    live = build_live_picker_rows(FIXTURE_VAULT, alpha)
    ids = [r.ticket_map_id for r in live]
    slices = {(r.ticket_map_id, r.slice_id) for r in live}
    # Prefer-linked only — park/superseded without armed stay out
    assert "ALPHA-park" not in ids
    assert "ALPHA-old" not in ids
    # B₁-ready r1 is launchable; r2 has no prefer-result → omitted from default
    assert ("ALPHA-open", "alpha_open_r1") in slices
    assert ("ALPHA-open", "alpha_open_r2") not in slices
    r1 = next(r for r in live if r.slice_id == "alpha_open_r1")
    assert r1.launchable
    assert r1.map_fidelity_hostile_ok is True
    # Primary f5 trail still shown
    assert any(r.trail and r.ticket_map_id == "ALPHA-done" for r in live)
    # Recovery open (B₁-ready) before trail
    assert live[0].ticket_map_id == "ALPHA-open"
    assert live[0].launchable
    label = format_live_picker_label(
        live[0], recovery_id="ALPHA-open", id_width=12, slice_width=14
    )
    assert label.startswith("★ ALPHA-open")
    assert "alpha_open" in label
    assert label.index("ALPHA-open") < label.index("·")

    # --all-tickets: B₁-pending draft appears but is not launchable
    all_live = build_live_picker_rows(FIXTURE_VAULT, alpha, show_hidden=True)
    all_slices = {(r.ticket_map_id, r.slice_id) for r in all_live}
    assert ("ALPHA-open", "alpha_open_r2") in all_slices
    r2 = next(r for r in all_live if r.slice_id == "alpha_open_r2")
    assert not r2.launchable
    assert r2.b1_pending


def test_prefer_b1_ok_fail_closed_and_true():
    briefs = (
        FIXTURE_VAULT
        / "1-Projects/proj_a/Factory-DRB/slice-briefs"
    )
    armed_r1 = briefs / "alpha_open_r1.armed.yaml"
    armed_r2 = briefs / "alpha_open_r2.armed.yaml"
    assert prefer_b1_ok(FIXTURE_VAULT, "alpha_open_r1", armed_r1) is True
    # Missing prefer-result → fail closed
    assert prefer_b1_ok(FIXTURE_VAULT, "alpha_open_r2", armed_r2) is False
    # Relative armed path also works
    rel = "1-Projects/proj_a/Factory-DRB/slice-briefs/alpha_open_r1.armed.yaml"
    assert prefer_b1_ok(FIXTURE_VAULT, "alpha_open_r1", rel) is True


def test_status_column_parse_and_legacy_infer():
    text = """
| Ticket | Status | Product job | Notes |
|--------|--------|-------------|-------|
| `T-NEW` | `open` | New style job here | notes |
"""
    rows = parse_ticket_map_rows(text)
    assert rows["T-NEW"].status == "open"
    legacy = """
| `T-LEG` | KEEP-real product job long enough | Operator F5 pass done |
"""
    rows2 = parse_ticket_map_rows(legacy)
    assert rows2["T-LEG"].status == "f5_good"
    assert infer_ticket_status("x", "Prefer draft awaiting Gate A+B pending") == "open"


def test_gate_a_parse_compat_with_status_column():
    text = """
| Ticket | Status | Product job | Notes |
|--------|--------|-------------|-------|
| `GEN-biomes` | `open` | Biomes with mechanical tags visible on dual grid | Prefer pack |
"""
    rows = fidelity_parse(text)
    assert "GEN-biomes" in rows
    assert rows["GEN-biomes"].product_job.startswith("Biomes")


def test_prefer_join_and_prompt():
    alpha = next(d for d in discover_ticket_maps(FIXTURE_VAULT) if d.map_id == "alpha-fixture")
    ticket = alpha.tickets["ALPHA-open"]
    prefer = resolve_prefer_for_ticket(
        FIXTURE_VAULT,
        project_id="proj_a",
        ticket_map_id="ALPHA-open",
        slice_hint="alpha_open_r1",
    )
    assert prefer["slice_id"] == "alpha_open_r1"
    assert prefer["armed"] is not None
    prompt = build_factory_weld_prompt(map_doc=alpha, ticket=ticket, prefer=prefer)
    assert "FACTORY GREENLIGHT WELD — ALPHA-open" in prompt
    assert "Gate B₁" in prompt and "Gate B₂" in prompt
    assert "Prefer-align" in prompt
    assert "Writes nothing" in prompt
    assert "alpha_open_r1" in prompt
    assert "GREENLIGHT WELD" in prompt


def test_recovery_sorted_first_among_open():
    alpha = next(d for d in discover_ticket_maps(FIXTURE_VAULT) if d.map_id == "alpha-fixture")
    shown = filter_tickets_for_picker(alpha.tickets.values())
    ordered = tickets_newest_first(shown, recovery_id="ALPHA-open")
    assert ordered[0].ticket_map_id == "ALPHA-open"


def test_picker_label_id_first_strips_markup():
    assert "same seat" in strip_job_markup("**same seat** bold")
    open_t = MapTicketRow(
        ticket_map_id="PLACE-product",
        product_job="Grey ghost → LMB → permanent opaque Full on **same seat**",
        welds="notes",
        status="open",
    )
    label = format_picker_ticket_label(
        open_t, recovery_id="PLACE-product", id_width=14, slice_id="slice_r1"
    )
    assert label.startswith("★ PLACE-product")
    assert "**" not in label
    assert "slice_r1" in label
    assert label.index("PLACE-product") < label.index("Grey")

    done = MapTicketRow(
        ticket_map_id="WORLD-new",
        product_job="DM opens a new world",
        welds="KEEP-real",
        status="f5_good",
    )
    grey = format_picker_ticket_label(done, id_width=14)
    assert grey.startswith("  [f5_good] WORLD-new")
    assert grey.index("WORLD-new") < grey.index("DM opens")


def test_session_prep_map_loads_if_present():
    vault = Path(__file__).resolve().parents[3]
    wb = (
        vault
        / "1-Projects/genesis-mythos-master/Factory-DRB/"
        "World-Builder-Session-Prep-Ticket-Map.md"
    )
    if not wb.is_file():
        return
    doc = load_ticket_map_doc(wb, vault_root=vault, require_flag=True)
    assert doc is not None
    assert doc.frontmatter.get("ticket_map") is True
    assert doc.map_id == "world-builder-session-prep"
    assert "WB-polygon-substrate" in doc.tickets
    assert doc.tickets["WB-polygon-substrate"].status == "open"
    from eat_queue_core.weave.factory.ticket_map_schema import (
        resolve_active_ticket_map_rel,
    )

    rel = resolve_active_ticket_map_rel(vault, project_id="genesis-mythos-master")
    assert rel and rel.endswith("World-Builder-Session-Prep-Ticket-Map.md")
    rows_via = __import__(
        "eat_queue_core.weave.factory.ticket_map_schema", fromlist=["load_ticket_map_rows"]
    ).load_ticket_map_rows(vault, ticket_map_id="WB-polygon-substrate")
    assert "WB-polygon-substrate" in rows_via
