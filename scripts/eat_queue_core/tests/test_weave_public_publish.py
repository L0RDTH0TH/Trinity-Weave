"""Tests for Trinity-Weave public export — no project bleed."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from eat_queue_core.schedule_config import SchedulePlanesConfig
from eat_queue_core.weave_public_publish import (
    DEFAULT_FORBIDDEN_PREFIXES,
    compute_weave_publish_fingerprint,
    run_weave_public_sync,
    run_weave_publish_on_schedule_tick,
    scan_forbidden,
    sync_weave_public_export,
)


def _write_min_config(root: Path) -> Path:
    cfg = root / "Second-Brain-Config.md"
    cfg.write_text(
        """# Test

```yaml
weave_publish:
  enabled: true
  harness_enabled: true
  export_repo_root: "EXPORT_ROOT"
  branch: main
  push_on_sync: false
  export_contract:
    includes:
      - scripts/eat_queue_core/weave_public_publish.py
      - .technical/weave/components/
    forbidden_prefixes:
      - 1-Projects/
      - Roadmap/
      - Ingest/
```

```yaml
parallel_execution:
  enabled: false
  gitforge:
    lock_timeout_seconds: 2
```
""".replace("EXPORT_ROOT", str(root / "export")),
        encoding="utf-8",
    )
    return cfg


class TestWeavePublicPublish(unittest.TestCase):
    def test_scan_forbidden_detects_project_paths(self) -> None:
        hits = scan_forbidden(
            ["Docs/foo.md", "1-Projects/godot-genesis-mythos-master/goal.md", "weave/components/x.yaml"],
            list(DEFAULT_FORBIDDEN_PREFIXES),
        )
        self.assertEqual(len(hits), 1)
        self.assertTrue(hits[0].startswith("1-Projects/"))

    def test_sync_allowlist_only(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / "vault"
            export = Path(td) / "export"
            vault.mkdir()
            (vault / "scripts/eat_queue_core").mkdir(parents=True)
            (vault / "scripts/eat_queue_core/weave_public_publish.py").write_text("# ok\n", encoding="utf-8")
            (vault / ".technical/weave/components").mkdir(parents=True)
            (vault / ".technical/weave/components/public_surface_topology.yaml").write_text("id: x\n", encoding="utf-8")
            (vault / "1-Projects").mkdir()
            (vault / "1-Projects/secret.md").write_text("secret\n", encoding="utf-8")

            out = sync_weave_public_export(vault, export, cfg={})
            self.assertTrue(out.get("ok"), out)
            self.assertTrue((export / "scripts/eat_queue_core/weave_public_publish.py").is_file())
            self.assertFalse((export / "1-Projects").exists())

    def test_fingerprint_changes_when_file_changes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td)
            (vault / "scripts/eat_queue_core").mkdir(parents=True)
            f = vault / "scripts/eat_queue_core/weave_public_publish.py"
            f.write_text("v1\n", encoding="utf-8")
            fp1 = compute_weave_publish_fingerprint(vault, cfg={"export_contract": {"includes": ["scripts/eat_queue_core/weave_public_publish.py"]}})
            f.write_text("v2\n", encoding="utf-8")
            fp2 = compute_weave_publish_fingerprint(vault, cfg={"export_contract": {"includes": ["scripts/eat_queue_core/weave_public_publish.py"]}})
            self.assertNotEqual(fp1, fp2)

    def test_schedule_tick_skips_unchanged_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            wp_cfg = {
                "export_contract": {
                    "includes": ["scripts/eat_queue_core/weave_public_publish.py"],
                }
            }
            (t / "scripts/eat_queue_core").mkdir(parents=True)
            (t / "scripts/eat_queue_core/weave_public_publish.py").write_text("# stable\n", encoding="utf-8")
            fp = compute_weave_publish_fingerprint(t, cfg=wp_cfg)
            cfg = t / "c.md"
            cfg.write_text(
                """```yaml
weave_publish:
  enabled: true
  on_schedule_tick: true
  export_repo_root: "EXPORT"
  push_on_sync: false
  export_contract:
    includes:
      - scripts/eat_queue_core/weave_public_publish.py
schedule_planes:
  weave_publish_on_tick_enabled: true
  weave_publish_every_n_ticks: 1
```\n""".replace("EXPORT", str(t / "export")),
                encoding="utf-8",
            )
            state = {"tick_count": 1, "weave_publish_fingerprint": fp}
            planes = SchedulePlanesConfig()
            act = run_weave_publish_on_schedule_tick(
                t,
                cfg,
                state,
                tick_count=1,
                planes_cfg=planes,
            )
            self.assertIsNotNone(act)
            assert act is not None
            self.assertTrue(act.get("skipped"))
            self.assertEqual(act.get("reason"), "unchanged_fingerprint")

    def test_skip_when_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            cfg = t / "c.md"
            cfg.write_text("```yaml\nweave_publish:\n  enabled: false\n```\n", encoding="utf-8")
            r = run_weave_public_sync(t, cfg, push=False, use_lock=False)
            self.assertEqual(r.exit_code, 0)
            self.assertEqual(r.payload.get("reason"), "weave_publish_disabled")


    def test_observability_artifacts_generated(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td) / "vault"
            export = Path(td) / "export"
            vault.mkdir()
            export.mkdir()
            comp = vault / ".technical/weave/components"
            comp.mkdir(parents=True)
            (comp / "test_card.yaml").write_text(
                "id: test_card\nconceptual:\n  summary: A test card.\nmeta:\n  card_kind: meta\n",
                encoding="utf-8",
            )
            proposals = vault / ".technical/weave/component-proposals"
            proposals.mkdir(parents=True)
            (proposals / "prop_card.yaml").write_text(
                "id: prop_card\nstatus: proposal\nconceptual:\n  summary: Provisional.\n",
                encoding="utf-8",
            )
            shutil = __import__("shutil")
            shutil.copytree(comp, export / "weave" / "components")
            shutil.copytree(proposals, export / "weave" / "component-proposals")
            from eat_queue_core.weave_observability import write_observability_artifacts

            out = write_observability_artifacts(export, vault, fingerprint="abc123")
            self.assertTrue(out.get("ok"))
            self.assertTrue((export / "OBSERVABILITY.json").is_file())
            self.assertTrue((export / "weave" / "CARD-INDEX.md").is_file())
            payload = json.loads((export / "OBSERVABILITY.json").read_text())
            self.assertIn("test_card", payload.get("locked_card_ids", []))
            self.assertIn("prop_card", payload.get("provisional_card_ids", []))
            self.assertTrue(payload.get("card_index_includes_proposals"))


if __name__ == "__main__":
    unittest.main()
