"""Phase 13 — host_weld_sync harness tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[3]


class TestTrinityHostWeldSync(unittest.TestCase):
    def test_production_legacy_count_zero_on_cutover_vault(self) -> None:
        from eat_queue_core.weave.trinity_host_weld_sync import (
            count_production_legacy_mdc,
            load_host_weld_manifest,
        )

        manifest = load_host_weld_manifest(VAULT_ROOT)
        scan = count_production_legacy_mdc(
            VAULT_ROOT, socket_retained=list(manifest.get("socket_retained") or [])
        )
        self.assertEqual(scan["count"], 0, scan.get("legacy_paths"))

    def test_dry_run_reports_safety_candidate(self) -> None:
        from eat_queue_core.weave.trinity_host_weld_sync import run_host_weld_sync

        out = run_host_weld_sync(VAULT_ROOT, dry_run=True, full_corpus=True)
        self.assertTrue(out.get("ok"), out)
        self.assertEqual(out.get("host_weld_production_legacy_count"), 0)
        candidates = out.get("host_weld_surgery_candidates") or []
        slugs = {c.get("slug") for c in candidates}
        self.assertIn("safety", slugs)

    def test_mint_missing_safety_slug(self) -> None:
        from eat_queue_core.weave.trinity_host_weld_sync import run_host_weld_sync

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hw = root / ".technical/weave/host-weld"
            live = hw / "live"
            live.mkdir(parents=True)
            (hw / "manifest.yaml").write_text(
                (VAULT_ROOT / ".technical/weave/host-weld/manifest.yaml").read_text(),
                encoding="utf-8",
            )
            (root / ".technical/weave/components").mkdir(parents=True)
            src = VAULT_ROOT / ".technical/weave/components/host_execution_safety_contract.yaml"
            (root / ".technical/weave/components/host_execution_safety_contract.yaml").write_text(
                src.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (root / ".cursor/rules/always").mkdir(parents=True)
            for rel in (
                ".cursor/rules/always/host-weld-bridge.mdc",
                ".cursor/rules/agents/execution-safety-blacklist.mdc",
                ".cursor/rules/agents/curator-mandatory-backup.mdc",
                ".cursor/rules/always/watcher-result-append.mdc",
            ):
                Path(root / rel).parent.mkdir(parents=True, exist_ok=True)
                Path(root / rel).write_text("---\n---\n", encoding="utf-8")

            safety = live / "safety.md"
            if safety.is_file():
                safety.unlink()

            out = run_host_weld_sync(root, dry_run=False, full_corpus=True)
            self.assertTrue(out.get("ok"), out)
            self.assertTrue(safety.is_file())
            applied = out.get("host_weld_surgeries_applied") or []
            self.assertTrue(any(a.get("slug") == "safety" for a in applied))


if __name__ == "__main__":
    unittest.main()
