"""Bindings resolver — fail-closed; proven on blank fixture-project, not a product dump.

Fixture is synthesized in-process (no shipped vault tree with 1-Projects/ — that
would fail Trinity forbidden-prefix scan).
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

from eat_queue_core.weave.factory.bindings import (
    BINDING_MISSING,
    BindingMissingError,
    bindings_family_rel,
    game_repo_path,
    resolve,
)

FIXTURE_PROJECT_ID = "fixture-project"


def _write_fixture_vault(root: Path) -> None:
    pid = FIXTURE_PROJECT_ID
    bindings = root / "1-Projects" / pid / "Factory-DRB" / "bindings"
    bindings.mkdir(parents=True, exist_ok=True)
    (root / "1-Projects" / pid / "game").mkdir(parents=True, exist_ok=True)
    (root / "1-Projects" / pid / "Factory-DRB" / "factory-project.yaml").write_text(
        yaml.dump(
            {
                "schema_version": 1,
                "project_id": pid,
                "factory_greenlit": False,
                "slice_factory_greenlit": False,
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    families = {
        "identity": {
            "project_id": pid,
            "game_repo_path": f"1-Projects/{pid}/game",
            "archive_path": "",
            "queue_lane": "factory",
            "release_checks": [],
        },
        "engine": {"adapter_id": "", "build_command": "", "ports": {}},
        "proof-catalog": {"probes": {}, "required_playtest_ids": []},
        "lanes": {"lane_ids": [], "order": []},
        "host-law": {"entries": []},
        "legacy-refuse": {"refuse_strings": []},
    }
    for fam, body in families.items():
        (bindings / f"{fam}.yaml").write_text(
            yaml.dump(body, sort_keys=False), encoding="utf-8"
        )


class BindingsResolveTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="bindings-fixture-"))
        _write_fixture_vault(self.root)

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.root, ignore_errors=True)

    def test_path_helper_only_layout(self) -> None:
        rel = bindings_family_rel(FIXTURE_PROJECT_ID, "identity")
        self.assertEqual(
            rel,
            f"1-Projects/{FIXTURE_PROJECT_ID}/Factory-DRB/bindings/identity.yaml",
        )

    def test_resolve_identity_game_repo(self) -> None:
        rel = game_repo_path(self.root, FIXTURE_PROJECT_ID)
        self.assertEqual(rel, f"1-Projects/{FIXTURE_PROJECT_ID}/game")
        self.assertTrue((self.root / rel).is_dir())

    def test_missing_key_raises(self) -> None:
        with self.assertRaises(BindingMissingError) as ctx:
            resolve(self.root, FIXTURE_PROJECT_ID, "identity", "no_such_key")
        self.assertEqual(ctx.exception.code, BINDING_MISSING)

    def test_missing_family_file_raises(self) -> None:
        path = (
            self.root
            / f"1-Projects/{FIXTURE_PROJECT_ID}/Factory-DRB/bindings/identity.yaml"
        )
        path.unlink()
        with self.assertRaises(BindingMissingError):
            resolve(self.root, FIXTURE_PROJECT_ID, "identity", "game_repo_path")

    def test_no_silent_product_slug_in_resolve(self) -> None:
        # Blank fixture id only — harness must not invent a product project.
        with self.assertRaises(BindingMissingError):
            resolve(self.root, "some-other-project", "identity", "game_repo_path")


if __name__ == "__main__":
    unittest.main()
