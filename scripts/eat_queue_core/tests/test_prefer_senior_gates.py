"""Anti-stamp locks for Trinity-stored Cursor senior B₁/B₂."""

from __future__ import annotations

import json
from pathlib import Path

from eat_queue_core.host_runner import HostInvokeRequest, HostInvokeResult
from eat_queue_core.weave.factory.prefer_map_fidelity import (
    run_harness_b1,
    validate_armed_map_fidelity,
)
from eat_queue_core.weave.factory.prefer_senior_gates import (
    ROLE_B1,
    SOURCE_B1,
    parse_senior_stdout,
    run_senior_gate,
    senior_pass_ok,
    store_senior_verdict,
)
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


def _setup(tmp: Path) -> tuple[Path, dict]:
    vault = tmp
    proj = vault / "1-Projects" / "test-proj" / "Factory-DRB"
    (proj / "bindings").mkdir(parents=True)
    (proj / "slice-briefs").mkdir(parents=True)
    map_rel = "1-Projects/test-proj/Factory-DRB/Test-Ticket-Map.md"
    (proj / "Test-Ticket-Map.md").write_text(
        f"""---
ticket_map: true
map_id: test-observe-map
map_status: active
project-id: test-proj
---

## A

| Ticket | Status | Product job | Notes | Observe |
|--------|--------|-------------|-------|---------|
| `WB-polygon-substrate` | `open` | {PRODUCT_JOB} | n | `person` |
| `WB-world-document` | `open` | Foundation — Quit and reload restores the world document. | n | `record` |
""",
        encoding="utf-8",
    )
    (proj / "factory-project.yaml").write_text(
        "project_id: test-proj\n"
        "ticket_map_runtime:\n"
        "  map_id: test-observe-map\n"
        f"  map_note: {map_rel}\n",
        encoding="utf-8",
    )
    (proj / "bindings" / "proof-catalog.yaml").write_text(
        "probes:\n  p1:\n    op: file_exists\n    path: x\n"
        "required_playtest_ids: []\n",
        encoding="utf-8",
    )
    (vault / "5-Attachments" / "Code-Repos" / "test-align").mkdir(parents=True)
    (proj / "bindings" / "identity.yaml").write_text(
        "project_id: test-proj\ngame_repo_path: 5-Attachments/Code-Repos/test-align\n",
        encoding="utf-8",
    )
    armed = {
        "project_id": "test-proj",
        "slice_id": "slice_r7",
        "ticket_map_id": "WB-polygon-substrate",
        "structural_success": PRODUCT_JOB,
        "proof_shape": "moment",
        "claim_class": "ask_success",
        "out_of_scope_ticket_ids": ["WB-world-document"],
        "behavior_keys": ["solid_stays"],
        "behavior_key_checks": {"solid_stays": "p1"},
        "observer": "operator",
        "observer_when": "after_build",
        "do_not_waive": list(DNW),
        "prefer_on": True,
    }
    (proj / "slice-briefs" / "slice_r7.armed.yaml").write_text(
        "slice_id: slice_r7\n", encoding="utf-8"
    )
    return vault, armed


def test_parse_discards_need_for_model_source():
    raw = '```json\n{"ok": true, "source": "cursor_senior_b1", "summary": "x", "violations": []}\n```'
    parsed = parse_senior_stdout(raw)
    assert parsed is not None
    assert parsed.get("ok") is True
    # Caller must ignore model source — trinity stamps


def test_disk_shaped_json_without_trinity_stamp_red(tmp_path: Path):
    vault, armed = _setup(tmp_path)
    pr = (
        vault
        / "1-Projects/test-proj/Factory-DRB/slice-briefs/slice_r7.prefer-result.json"
    )
    pr.write_text(
        json.dumps(
            {
                "map_fidelity_hostile_ok": True,
                "map_fidelity_hostile": {
                    "ok": True,
                    "source": SOURCE_B1,
                    "role": ROLE_B1,
                    # missing trinity_stamped
                },
            }
        ),
        encoding="utf-8",
    )
    assert senior_pass_ok(json.loads(pr.read_text()), gate="b1") is False
    assert prefer_b1_ok(vault, "slice_r7", pr.parent / "slice_r7.armed.yaml") is False


def test_model_source_tag_alone_red(tmp_path: Path):
    vault, armed = _setup(tmp_path)
    # Forge disk with model-looking source but wrong role / no stamp
    data = {
        "map_fidelity_hostile": {
            "ok": True,
            "source": SOURCE_B1,
            "trinity_stamped": True,
            "role": "not_the_senior_role",
        }
    }
    assert senior_pass_ok(data, gate="b1") is False


def test_harness_b1_cannot_stamp(tmp_path: Path):
    vault, armed = _setup(tmp_path)
    out = run_harness_b1(vault, armed, write_result=True)
    assert out["ok"] is False
    assert any("not_authoritative" in v for v in out["violations"])
    pr = (
        vault
        / "1-Projects/test-proj/Factory-DRB/slice-briefs/slice_r7.prefer-result.json"
    )
    assert not pr.is_file()


def test_gate_a_pass_latch_red_until_trinity_store(tmp_path: Path):
    vault, armed = _setup(tmp_path)
    a = validate_armed_map_fidelity(
        vault, armed, prefer_result=None, require_hostile_for_keep=False
    )
    assert a.ok, a.violations
    assert prefer_b1_ok(
        vault, "slice_r7", vault / "1-Projects/test-proj/Factory-DRB/slice-briefs/x.armed.yaml"
    ) is False


def test_store_without_factory_order_refused(tmp_path: Path):
    vault, armed = _setup(tmp_path)

    def fake_invoke(req: HostInvokeRequest) -> HostInvokeResult:
        assert req.allow_writes is False
        assert "--force" not in ""  # request level
        return HostInvokeResult(
            ok=True,
            provider="cursor_cli",
            exit_code=0,
            raw_text='```json\n{"ok": true, "summary": "ok", "violations": []}\n```',
        )

    r = run_senior_gate(
        vault,
        armed,
        gate="b1",
        host_invoke=fake_invoke,
        store=True,
        factory_order=False,
    )
    assert r.ok is False
    assert "store_requires_factory_order" in r.violations[0]


def test_trinity_store_from_stdout_makes_launchable(tmp_path: Path):
    vault, armed = _setup(tmp_path)

    def fake_invoke(req: HostInvokeRequest) -> HostInvokeResult:
        assert req.role == ROLE_B1
        assert req.allow_writes is False
        return HostInvokeResult(
            ok=True,
            provider="cursor_cli",
            exit_code=0,
            raw_text=(
                '```json\n{"ok": true, "source": "forged_by_model", '
                '"summary": "consistent", "violations": []}\n```'
            ),
        )

    r = run_senior_gate(
        vault,
        armed,
        gate="b1",
        host_invoke=fake_invoke,
        store=True,
        factory_order=True,
    )
    assert r.ok is True
    assert r.source == SOURCE_B1  # Trinity stamp, not model
    pr = Path(r.prefer_result_path or "")
    data = json.loads(pr.read_text(encoding="utf-8"))
    assert data["map_fidelity_hostile"]["source"] == SOURCE_B1
    assert data["map_fidelity_hostile"]["trinity_stamped"] is True
    assert data["map_fidelity_hostile"]["role"] == ROLE_B1
    # Model source must not appear as authority
    assert prefer_b1_ok(vault, "slice_r7", pr.parent / "slice_r7.armed.yaml") is True


def test_senior_edit_fail_closed_discards_stdout(tmp_path: Path):
    vault, armed = _setup(tmp_path)
    catalog = (
        vault / "1-Projects/test-proj/Factory-DRB/bindings/proof-catalog.yaml"
    )

    def fake_invoke(req: HostInvokeRequest) -> HostInvokeResult:
        # Mutate catalog during "senior" run
        catalog.write_text(catalog.read_text(encoding="utf-8") + "# edited\n", encoding="utf-8")
        return HostInvokeResult(
            ok=True,
            provider="cursor_cli",
            exit_code=0,
            raw_text='```json\n{"ok": true, "summary": "lie", "violations": []}\n```',
        )

    r = run_senior_gate(
        vault,
        armed,
        gate="b1",
        host_invoke=fake_invoke,
        store=True,
        factory_order=True,
    )
    assert r.ok is False
    assert any("edited_watched_paths" in v for v in r.violations)
    assert prefer_b1_ok(
        vault, "slice_r7", vault / "1-Projects/test-proj/Factory-DRB/slice-briefs/x.yaml"
    ) is False


def test_print_flag_claim_does_not_bypass_senior(tmp_path: Path):
    """Probe print flags are claims; without Trinity senior store, latch stays red."""
    vault, armed = _setup(tmp_path)
    claim = "window_opened=1\npointer_injected=1\nop=window_pointer_inject\n"
    # Even if someone drops a harness_b1 shaped file, prefer_b1_ok stays red
    pr = (
        vault
        / "1-Projects/test-proj/Factory-DRB/slice-briefs/slice_r7.prefer-result.json"
    )
    pr.write_text(
        json.dumps(
            {
                "map_fidelity_hostile_ok": True,
                "map_fidelity_hostile": {
                    "ok": True,
                    "source": "harness_b1",
                    "classes": {"k": "person"},
                    "claim": claim,
                },
            }
        ),
        encoding="utf-8",
    )
    assert prefer_b1_ok(vault, "slice_r7", pr.parent / "slice_r7.armed.yaml") is False
