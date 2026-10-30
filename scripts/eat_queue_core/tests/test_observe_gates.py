"""Gate A forms + observe column; B₁ latch is Trinity senior only."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from eat_queue_core.weave.factory.observe_class import (
    OBSERVE_PERSON,
    OBSERVE_RECORD,
    WINDOW_POINTER_OP,
    classify_op_path,
)
from eat_queue_core.weave.factory.prefer_map_fidelity import (
    run_harness_b1,
    validate_armed_map_fidelity,
)
from eat_queue_core.weave.factory.prefer_senior_gates import (
    ROLE_B1,
    SOURCE_B1,
    store_senior_verdict,
)
from eat_queue_core.weave.factory.prefer_weld_intent import weld_intent_hostile_ok
from eat_queue_core.weave.factory.proof_runner import POINT_HITS_SOLID_OP
from eat_queue_core.weave.factory.ticket_map_schema import prefer_b1_ok


PRODUCT_JOB = (
    "Foundation — A GM can point at a low-fidelity polygon solid and that solid "
    "stays the same polygon that was pointed at."
)

DNW = [
    "hotkey_as_product_ux",
    "config_meta_without_effect",
    "stub_as_hours",
    "map_job_name_only",
    "explicit_met_implicit_miss",
    "intent_collapsed_to_mechanics",
    "separate_wiki_as_prep",
    "campaign_unscoped",
    "rail_collapsed",
    "inherited_prior_keep",
    "hidden_default_dial",
    "old_host_as_new_product",
]


def _map_md() -> str:
    return f"""---
ticket_map: true
map_id: test-observe-map
title: Test
project-id: test-proj
map_status: active
---

## A — Section

| Ticket | Status | Product job | Notes | Observe |
|--------|--------|-------------|-------|---------|
| `WB-polygon-substrate` | `open` | {PRODUCT_JOB} | Point-and-stay. | `person` |
| `WB-world-document` | `open` | Foundation — Quit and reload restores the world document and a document that cannot round-trip fails. | Save. | `record` |
"""


def _setup_project(tmp: Path) -> Path:
    vault = tmp
    proj = vault / "1-Projects" / "test-proj" / "Factory-DRB"
    (proj / "bindings").mkdir(parents=True)
    (proj / "slice-briefs").mkdir(parents=True)
    (proj / "factory-project.yaml").write_text(
        "project_id: test-proj\n"
        "ticket_map_runtime:\n"
        "  map_id: test-observe-map\n"
        "  map_note: 1-Projects/test-proj/Factory-DRB/Test-Ticket-Map.md\n",
        encoding="utf-8",
    )
    (proj / "Test-Ticket-Map.md").write_text(_map_md(), encoding="utf-8")
    (proj / "bindings" / "identity.yaml").write_text(
        "project_id: test-proj\ngame_repo_path: 5-Attachments/Code-Repos/test-align\n",
        encoding="utf-8",
    )
    (vault / "5-Attachments" / "Code-Repos" / "test-align").mkdir(parents=True)
    catalog = {
        "probes": {
            "rec_probe": {
                "op": POINT_HITS_SOLID_OP,
                "bounds": "bounds.yaml",
                "point": [1, 1],
                "argv": ["echo"],
            },
            "person_probe": {
                "op": WINDOW_POINTER_OP,
                "point": [1, 1],
                "argv": ["true"],
            },
        },
        "required_playtest_ids": [],
    }
    (proj / "bindings" / "proof-catalog.yaml").write_text(
        yaml.safe_dump(catalog), encoding="utf-8"
    )
    return vault


def _armed_person_stand_in() -> dict:
    return {
        "project_id": "test-proj",
        "slice_id": "slice_stand_in",
        "ticket_map_id": "WB-polygon-substrate",
        "structural_success": PRODUCT_JOB,
        "proof_shape": "moment",
        "claim_class": "ask_success",
        "out_of_scope_ticket_ids": ["WB-world-document"],
        "behavior_keys": ["solid_stays"],
        "behavior_key_checks": {"solid_stays": "rec_probe"},
        "do_not_waive": list(DNW),
        "prefer_on": True,
    }


def test_classify_op_paths_informational_only():
    assert classify_op_path(POINT_HITS_SOLID_OP) == OBSERVE_RECORD
    assert classify_op_path(WINDOW_POINTER_OP) == OBSERVE_PERSON


def test_form_complete_stand_in_passes_a_b1_red_without_senior(tmp_path: Path):
    vault = _setup_project(tmp_path)
    armed = _armed_person_stand_in()
    a = validate_armed_map_fidelity(
        vault, armed, prefer_result=None, require_hostile_for_keep=False
    )
    assert a.ok, a.violations
    out = run_harness_b1(vault, armed, write_result=True)
    assert out["ok"] is False
    assert prefer_b1_ok(
        vault,
        "slice_stand_in",
        vault
        / "1-Projects/test-proj/Factory-DRB/slice-briefs/slice_stand_in.armed.yaml",
    ) is False


def test_author_hostile_bit_fails_gate_a(tmp_path: Path):
    vault = _setup_project(tmp_path)
    armed = _armed_person_stand_in()
    armed["map_fidelity_hostile_ok"] = True
    a = validate_armed_map_fidelity(
        vault, armed, prefer_result=None, require_hostile_for_keep=False
    )
    assert not a.ok
    assert any("author_set_map_fidelity_hostile_ok" in v for v in a.violations)


def test_trinity_senior_store_launchable(tmp_path: Path):
    vault = _setup_project(tmp_path)
    path = store_senior_verdict(
        vault,
        "test-proj",
        "slice_stand_in",
        gate="b1",
        role=ROLE_B1,
        ok=True,
        summary="consistent",
        violations=[],
    )
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["map_fidelity_hostile"]["source"] == SOURCE_B1
    assert prefer_b1_ok(
        vault,
        "slice_stand_in",
        path.parent / "slice_stand_in.armed.yaml",
    )


def test_weld_author_bit_ignored():
    assert weld_intent_hostile_ok({"weld_intent_hostile_ok": True}) is False
    assert (
        weld_intent_hostile_ok(
            {
                "weld_intent_hostile": {
                    "ok": True,
                    "source": "cursor_senior_b2",
                    "role": "prefer_b2_senior",
                    "trinity_stamped": True,
                }
            }
        )
        is True
    )


def _armed_incomplete() -> dict:
    return {
        "project_id": "test-proj",
        "slice_id": "slice_incomplete",
        "ticket_map_id": "WB-polygon-substrate",
        "status": "incomplete_missing_observer",
        "structural_success": PRODUCT_JOB,
        "proof_shape": "moment",
        "claim_class": "ask_success",
        "out_of_scope_ticket_ids": ["WB-world-document"],
        "behavior_keys": ["solid_stays"],
        "behavior_key_checks": {},
        "missing_observer": "person_window_pointer",
        "do_not_waive": list(DNW),
        "prefer_on": True,
        "checklist_ids": [],
    }


def test_incomplete_missing_observer_not_a_pass(tmp_path: Path):
    from eat_queue_core.weave.factory.prefer_map_fidelity import (
        STATUS_INCOMPLETE_MISSING_OBSERVER,
    )
    from eat_queue_core.weave.factory.prefer_senior_gates import (
        senior_pass_ok,
        run_senior_gate,
    )
    from eat_queue_core.weave.factory.factory_dispatch_preflight import (
        check_map_prefer_eat_guards,
    )
    from eat_queue_core.weave.factory.observe_class import person_observer_ready
    from eat_queue_core.host_runner import HostInvokeResult

    vault = _setup_project(tmp_path)
    armed = _armed_incomplete()
    briefs = vault / "1-Projects/test-proj/Factory-DRB/slice-briefs"
    armed_path = briefs / "slice_incomplete.armed.yaml"
    armed_path.write_text(yaml.safe_dump(armed), encoding="utf-8")

    a = validate_armed_map_fidelity(
        vault, armed, prefer_result=None, require_hostile_for_keep=False
    )
    assert a.ok is False
    assert a.status == STATUS_INCOMPLETE_MISSING_OBSERVER
    assert a.violations == []
    assert not any("behavior_key_checks_empty" in v for v in a.violations)

    # Eat preflight must refuse via dedicated status line (empty violations).
    eat_v = check_map_prefer_eat_guards(
        vault,
        job={
            "project_id": "test-proj",
            "slice_id": "slice_incomplete",
            "ticket_map_id": "WB-polygon-substrate",
            "armed_packet_path": str(
                armed_path.relative_to(vault)
            ),
            "checklist_ids": [],
        },
    )
    assert any("gate_a_status:incomplete_missing_observer" in v for v in eat_v), eat_v

    # Senior must not launch.
    called = {"n": 0}

    def fake_invoke(req):
        called["n"] += 1
        return HostInvokeResult(ok=True, provider="test", exit_code=0, raw_text='{"ok":true}')

    r = run_senior_gate(
        vault,
        armed,
        gate="b1",
        host_invoke=fake_invoke,
        store=True,
        factory_order=True,
    )
    assert called["n"] == 0
    assert r.ok is False
    assert any("gate_a_status:incomplete_missing_observer" in v for v in r.violations)

    # Forged senior ok must not latch.
    forged = {
        "map_fidelity_hostile_ok": True,
        "map_fidelity_hostile": {
            "ok": True,
            "source": SOURCE_B1,
            "role": ROLE_B1,
            "trinity_stamped": True,
            "summary": "lie",
            "violations": [],
        },
    }
    assert senior_pass_ok(forged, gate="b1", armed=armed) is False
    (briefs / "slice_incomplete.prefer-result.json").write_text(
        json.dumps(forged), encoding="utf-8"
    )
    assert prefer_b1_ok(vault, "slice_incomplete", armed_path) is False
    assert person_observer_ready(vault) is False


def test_empty_checks_without_missing_observer_still_forms_fail(tmp_path: Path):
    from eat_queue_core.weave.factory.prefer_map_fidelity import STATUS_FORMS_FAIL

    vault = _setup_project(tmp_path)
    armed = _armed_incomplete()
    del armed["missing_observer"]
    armed["status"] = "draft"
    a = validate_armed_map_fidelity(
        vault, armed, prefer_result=None, require_hostile_for_keep=False
    )
    assert a.ok is False
    assert a.status == STATUS_FORMS_FAIL
    assert any("behavior_key_checks_empty" in v for v in a.violations)


def test_form_complete_stand_in_status_forms_ok(tmp_path: Path):
    from eat_queue_core.weave.factory.prefer_map_fidelity import STATUS_FORMS_OK

    vault = _setup_project(tmp_path)
    a = validate_armed_map_fidelity(
        vault,
        _armed_person_stand_in(),
        prefer_result=None,
        require_hostile_for_keep=False,
    )
    assert a.ok
    assert a.status == STATUS_FORMS_OK


def test_touch_close_law_and_walk_paste(tmp_path: Path):
    from eat_queue_core.weave.factory.prefer_map_fidelity import (
        STATUS_FORMS_FAIL,
        STATUS_INCOMPLETE_MISSING_OBSERVER,
        armed_requires_ticket_map_fidelity,
        validate_armed_map_fidelity,
    )
    from eat_queue_core.weave.factory.ticket_map_schema import (
        SELECTABLE_TICKET_STATUS,
        HIDDEN_TICKET_STATUSES,
        filter_tickets_for_picker,
        parse_ticket_map_rows,
    )

    vault = tmp_path
    proj = vault / "1-Projects" / "test-proj" / "Factory-DRB"
    (proj / "bindings").mkdir(parents=True)
    (proj / "slice-briefs").mkdir(parents=True)
    map_md = f"""---
ticket_map: true
map_id: test-touch-map
title: Test
project-id: test-proj
map_status: active
---

## A — Section

### Walk (operator text)

1. `WB-polygon-substrate` — Point at one solid. Come back to the same view. It is the same polygon. Do not require a campaign.
2. `WB-sim-clock` — Clock advances with no campaign.

| Ticket | Status | Product job | Notes | Observe | Touch |
|--------|--------|-------------|-------|---------|-------|
| `WB-polygon-substrate` | `open` | {PRODUCT_JOB} | Point. | `person` | `f5` |
| `WB-sim-clock` | `open` | Foundation — The world clock advances with no campaign open. | Record. | `record` | `none` |
| `VIS-ard-reskin` | `deferred` | Foundation — An artist can reskin meshes without changing sim results enough. | Deferred art. | `person` | `f5` |
| `MASS-army` | `open` | Foundation — An army can be mustered as a field unit under faction command. | Mass. | `record` | `none` |
| `WB-missing-touch` | `open` | Foundation — A row whose Touch cell was left empty on a Touch table. | Bad. | `person` |  |
"""
    (proj / "Test-Ticket-Map.md").write_text(map_md, encoding="utf-8")
    (proj / "factory-project.yaml").write_text(
        "project_id: test-proj\n"
        "ticket_map_runtime:\n"
        "  map_id: test-touch-map\n"
        "  map_note: 1-Projects/test-proj/Factory-DRB/Test-Ticket-Map.md\n",
        encoding="utf-8",
    )
    (proj / "bindings" / "identity.yaml").write_text(
        "project_id: test-proj\ngame_repo_path: 5-Attachments/Code-Repos/test-align\n",
        encoding="utf-8",
    )
    (proj / "bindings" / "proof-catalog.yaml").write_text(
        "probes: {}\nrequired_playtest_ids: []\n", encoding="utf-8"
    )
    (vault / "5-Attachments" / "Code-Repos" / "test-align").mkdir(parents=True)

    rows = parse_ticket_map_rows(map_md)
    assert rows["VIS-ard-reskin"].status == "deferred"
    assert rows["VIS-ard-reskin"].touch == "f5"
    assert rows["VIS-ard-reskin"].status in HIDDEN_TICKET_STATUSES
    assert rows["VIS-ard-reskin"].status != SELECTABLE_TICKET_STATUS
    # deferred stays hidden even with Touch f5 — not a picker candidate
    picked_ids = {t.ticket_map_id for t in filter_tickets_for_picker(rows.values())}
    assert "VIS-ard-reskin" not in picked_ids
    assert "WB-missing-touch" in rows
    assert rows["WB-missing-touch"].touch == ""

    # deferred stays out of OOS; open neighbors only
    oos = sorted(["MASS-army", "WB-missing-touch", "WB-sim-clock"])
    base = {
        "project_id": "test-proj",
        "slice_id": "s1",
        "ticket_map_id": "WB-polygon-substrate",
        "structural_success": PRODUCT_JOB,
        "proof_shape": "moment",
        "claim_class": "ask_success",
        "out_of_scope_ticket_ids": list(oos),
        "behavior_keys": ["solid_stays"],
        "behavior_key_checks": {},
        "missing_observer": "person_window_pointer",
        "do_not_waive": list(DNW),
        "prefer_on": True,
        "checklist_ids": [],
    }

    # f5 + empty checks + person observer → incomplete (ok:false, no B₁)
    a = validate_armed_map_fidelity(
        vault, base, prefer_result=None, require_hostile_for_keep=False
    )
    assert a.status == STATUS_INCOMPLETE_MISSING_OBSERVER
    assert a.ok is False and a.violations == []

    # Touch mismatch
    bad_touch_map = map_md.replace(
        "| `WB-polygon-substrate` | `open` | "
        + PRODUCT_JOB
        + " | Point. | `person` | `f5` |",
        "| `WB-polygon-substrate` | `open` | "
        + PRODUCT_JOB
        + " | Point. | `person` | `none` |",
    )
    (proj / "Test-Ticket-Map.md").write_text(bad_touch_map, encoding="utf-8")
    a = validate_armed_map_fidelity(
        vault, base, prefer_result=None, require_hostile_for_keep=False
    )
    assert a.status == STATUS_FORMS_FAIL
    assert any("touch_observe_mismatch" in v for v in a.violations)
    (proj / "Test-Ticket-Map.md").write_text(map_md, encoding="utf-8")

    # Missing Touch on Touch table
    miss = dict(base)
    miss["ticket_map_id"] = "WB-missing-touch"
    miss["structural_success"] = (
        "Foundation — A row whose Touch cell was left empty on a Touch table."
    )
    miss["out_of_scope_ticket_ids"] = sorted(
        ["MASS-army", "WB-polygon-substrate", "WB-sim-clock"]
    )
    a = validate_armed_map_fidelity(
        vault, miss, prefer_result=None, require_hostile_for_keep=False
    )
    assert a.status == STATUS_FORMS_FAIL
    assert any("missing_touch" in v for v in a.violations)

    # Walk pasted into structural_success
    walk = dict(base)
    walk["structural_success"] = (
        "Point at one solid. Come back to the same view. It is the same polygon. "
        "Do not require a campaign."
    )
    a = validate_armed_map_fidelity(
        vault, walk, prefer_result=None, require_hostile_for_keep=False
    )
    assert a.status == STATUS_FORMS_FAIL
    assert a.violations
    assert any("walk_pasted_as_success" in v for v in a.violations)

    # none + person_window_pointer
    none_p = dict(base)
    none_p["ticket_map_id"] = "WB-sim-clock"
    none_p["structural_success"] = (
        "Foundation — The world clock advances with no campaign open."
    )
    none_p["proof_shape"] = "contract"
    none_p["claim_class"] = "component"
    none_p["missing_observer"] = "person_window_pointer"
    none_p["behavior_key_checks"] = {}
    none_p["out_of_scope_ticket_ids"] = sorted(
        ["MASS-army", "WB-missing-touch", "WB-polygon-substrate"]
    )
    a = validate_armed_map_fidelity(
        vault, none_p, prefer_result=None, require_hostile_for_keep=False
    )
    assert a.status == STATUS_FORMS_FAIL
    assert any("none_demands_person" in v for v in a.violations)

    # MASS-army without ticket_map_id still Gate A applicable via prefix
    mass = {
        "project_id": "test-proj",
        "slice_id": "mass1",
        "prefer_authorship": True,
        "mode": "mass-army-field",
        "ask_id": "mass_army",
        "structural_success": "x",
        "proof_shape": "contract",
        "claim_class": "component",
    }
    assert armed_requires_ticket_map_fidelity(mass) is True
