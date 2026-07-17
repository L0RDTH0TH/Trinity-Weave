"""Tests for Grok project bridge — sync, remote gate, proposals on main."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from eat_queue_core.grok_bridge_config import resolve_grok_bridge
from eat_queue_core.grok_bridge_export_session import clear_session, read_session, write_session
from eat_queue_core.project_bridge_sync import (
    scan_branch_forbidden,
    sync_project_to_export,
    verify_trinity_remote,
)
from eat_queue_core.weave_observability import build_card_index_rows, write_observability_artifacts
from eat_queue_core.weave_public_publish import DEFAULT_FORBIDDEN_PREFIXES, sync_weave_public_export


def _git_init(path: Path, remote_url: str) -> None:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "t@test"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=path, check=True, capture_output=True)
    (path / "README.md").write_text("# x\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "checkout", "-b", "main"], cwd=path, check=True, capture_output=True)


class TestGrokBridge(unittest.TestCase):
    def test_component_proposals_not_forbidden_prefix(self) -> None:
        self.assertNotIn("component-proposals/", DEFAULT_FORBIDDEN_PREFIXES)

    def test_proposals_in_card_index(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            export = Path(td) / "export"
            (export / "weave/components").mkdir(parents=True)
            (export / "weave/component-proposals").mkdir(parents=True)
            (export / "weave/components/locked_card.yaml").write_text(
                "id: locked_card\nmeta:\n  card_kind: meta\n  promotion_tier: locked\nconceptual:\n  summary: Locked.\n",
                encoding="utf-8",
            )
            (export / "weave/component-proposals/catalog_mint_gate.yaml").write_text(
                "id: catalog_mint_gate\nstatus: proposal\nconceptual:\n  summary: Mint gate.\n",
                encoding="utf-8",
            )
            rows = build_card_index_rows(export)
            ids = [r["id"] for r in rows]
            self.assertIn("locked_card", ids)
            self.assertIn("catalog_mint_gate", ids)
            prov = [r for r in rows if r["id"] == "catalog_mint_gate"][0]
            self.assertEqual(prov["status"], "provisional")

    def test_sync_exports_proposals(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / "vault"
            export = Path(td) / "export"
            vault.mkdir()
            prop = vault / ".technical/weave/component-proposals"
            prop.mkdir(parents=True)
            (prop / "catalog_mint_gate.yaml").write_text("id: catalog_mint_gate\n", encoding="utf-8")
            (vault / "scripts/eat_queue_core").mkdir(parents=True)
            (vault / "scripts/eat_queue_core/weave_public_publish.py").write_text("# ok\n", encoding="utf-8")
            cfg = {
                "export_contract": {
                    "includes": [
                        "scripts/eat_queue_core/weave_public_publish.py",
                        ".technical/weave/component-proposals/",
                    ],
                    "forbidden_prefixes": list(DEFAULT_FORBIDDEN_PREFIXES),
                }
            }
            out = sync_weave_public_export(vault, export, cfg=cfg)
            self.assertTrue(out.get("ok"), out)
            self.assertTrue((export / "weave/component-proposals/catalog_mint_gate.yaml").is_file())

    def test_wrong_remote_aborts(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            export = Path(td) / "export"
            export.mkdir()
            _git_init(export, "https://github.com/L0RDTH0TH/genesis-mythos-master-roadmap.git")
            ok, actual = verify_trinity_remote(
                export,
                "https://github.com/L0RDTH0TH/Trinity-Weave.git",
            )
            self.assertFalse(ok)
            self.assertIn("genesis-mythos", actual)

    def test_project_sync_isolation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / "vault"
            export = Path(td) / "export"
            vault.mkdir()
            pid = "godot-genesis-mythos-master"
            proj = vault / "1-Projects" / pid
            proj.mkdir(parents=True)
            (proj / "GROK-PROJECT-START.md").write_text("# start\n", encoding="utf-8")
            (proj / "PROJECT-OBSERVABILITY.json").write_text('{"project_id":"x"}\n', encoding="utf-8")
            (proj / "TERTIARY-INDEX.json").write_text('{"entries":[]}\n', encoding="utf-8")
            _git_init(export, "https://github.com/L0RDTH0TH/Trinity-Weave.git")
            main_head_before = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=export, text=True
            ).strip()

            cfg = resolve_grok_bridge(
                {
                    "grok_bridge": {"pilot_project_id": pid},
                    "weave_publish": {"remote_url": "https://github.com/L0RDTH0TH/Trinity-Weave.git"},
                }
            )
            out = sync_project_to_export(vault, export, pid, cfg=cfg)
            self.assertTrue(out.get("ok"), out)

            subprocess.run(["git", "checkout", "main"], cwd=export, check=True, capture_output=True)
            main_head_after = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=export, text=True
            ).strip()
            self.assertEqual(main_head_before, main_head_after)

    def test_main_forbidden_roadmap_on_main_branch_scan(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            export = Path(td) / "export"
            export.mkdir()
            (export / "Roadmap").mkdir()
            (export / "Roadmap/x.md").write_text("x", encoding="utf-8")
            hits = scan_branch_forbidden(export, "main")
            self.assertTrue(any(h.startswith("Roadmap/") for h in hits))

    def test_session_heal_clears_in_progress(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / "vault"
            vault.mkdir()
            write_session(vault, {"in_progress": True, "target_branch": "project/x"})
            self.assertIsNotNone(read_session(vault))
            clear_session(vault)
            self.assertIsNone(read_session(vault))

    def test_gmmr_path_never_used_by_sync(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / "vault"
            gmmr = Path(td) / "gmm-export"
            export = Path(td) / "trinity-export"
            vault.mkdir()
            gmmr.mkdir()
            pid = "godot-genesis-mythos-master"
            proj = vault / "1-Projects" / pid
            proj.mkdir(parents=True)
            (proj / "GROK-PROJECT-START.md").write_text("# s\n", encoding="utf-8")
            (proj / "PROJECT-OBSERVABILITY.json").write_text("{}\n", encoding="utf-8")
            (proj / "TERTIARY-INDEX.json").write_text('{"entries":[]}\n', encoding="utf-8")
            _git_init(export, "https://github.com/L0RDTH0TH/Trinity-Weave.git")
            marker = gmmr / "marker.txt"
            marker.write_text("before\n", encoding="utf-8")
            cfg = resolve_grok_bridge({"grok_bridge": {"pilot_project_id": pid}})
            cfg["export_repo_root"] = str(export)
            sync_project_to_export(vault, export, pid, cfg=cfg)
            self.assertEqual(marker.read_text(), "before\n")

    def test_fulfill_broker_requires_operator_ack(self) -> None:
        from eat_queue_core.grok_fulfill_broker import build_fulfill_pack

        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / "vault"
            vault.mkdir()
            cfg = resolve_grok_bridge({"grok_bridge": {"pilot_project_id": "godot-genesis-mythos-master"}})
            req = {
                "request_id": "t1",
                "project_id": "godot-genesis-mythos-master",
                "purpose": "test",
                "node_ids": ["tert_missing"],
            }
            out = build_fulfill_pack(vault, req, cfg=cfg, operator_ack=False)
            self.assertFalse(out.get("ok"))
            self.assertIn("operator_ack_required", out.get("errors", []))


if __name__ == "__main__":
    unittest.main()
