"""Engine-neutral proof_runner — empty checklist no-op; unknown probe fails."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

from eat_queue_core.weave.factory.proof_runner import (
    UnknownProbeError,
    run_named_probes,
)


def _vault_with_catalog(probes: dict) -> tuple[Path, str]:
    root = Path(tempfile.mkdtemp(prefix="proof-runner-"))
    pid = "fixture-project"
    bindings = root / "1-Projects" / pid / "Factory-DRB" / "bindings"
    bindings.mkdir(parents=True)
    (root / "1-Projects" / pid / "game").mkdir(parents=True)
    (bindings / "identity.yaml").write_text(
        yaml.dump({"project_id": pid, "game_repo_path": f"1-Projects/{pid}/game"}),
        encoding="utf-8",
    )
    (bindings / "proof-catalog.yaml").write_text(
        yaml.dump({"probes": probes}), encoding="utf-8"
    )
    for fam in ("engine", "lanes", "host-law", "legacy-refuse"):
        (bindings / f"{fam}.yaml").write_text("{}\n", encoding="utf-8")
    return root, pid


class ProofRunnerTests(unittest.TestCase):
    def test_empty_checklist_runs_nothing(self) -> None:
        root, pid = _vault_with_catalog(
            {"p1": {"op": "file_exists", "path": "README"}}
        )
        self.assertEqual(run_named_probes(root, pid, []), [])

    def test_unknown_probe_raises(self) -> None:
        root, pid = _vault_with_catalog({})
        with self.assertRaises(UnknownProbeError):
            run_named_probes(root, pid, ["no_such_probe"])

    def test_file_exists_op(self) -> None:
        root, pid = _vault_with_catalog(
            {"readme": {"op": "file_exists", "path": "marker.txt"}}
        )
        game = root / "1-Projects" / pid / "game"
        (game / "marker.txt").write_text("ok", encoding="utf-8")
        out = run_named_probes(root, pid, ["readme"])
        self.assertEqual(len(out), 1)
        self.assertTrue(out[0].ok)


if __name__ == "__main__":
    unittest.main()
