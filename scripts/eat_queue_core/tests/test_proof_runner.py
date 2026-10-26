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

_TWO_RECT_BOUNDS = """
solids:
  - id: solid-a
    x0: 0.0
    y0: 0.0
    x1: 0.4
    y1: 0.4
  - id: solid-b
    x0: 0.6
    y0: 0.6
    x1: 1.0
    y1: 1.0
"""

_HONEST_HIT = """#!/usr/bin/env python3
import sys
from pathlib import Path
import yaml
argv = sys.argv[1:]
i = argv.index("--point")
x, y = float(argv[i + 1]), float(argv[i + 2])
raw = yaml.safe_load(Path("state/bounds.yaml").read_text())
for s in raw["solids"]:
    x0, y0, x1, y1 = s["x0"], s["y0"], s["x1"], s["y1"]
    if min(x0, x1) <= x <= max(x0, x1) and min(y0, y1) <= y <= max(y0, y1):
        print(s["id"])
        raise SystemExit(0)
raise SystemExit(1)
"""

_CONSTANT_A = """#!/usr/bin/env python3
print("solid-a")
"""

_ECHO_POINT = """#!/usr/bin/env python3
import sys
i = sys.argv.index("--point")
print(sys.argv[i + 1])
"""


def _vault_with_catalog(probes: dict) -> tuple[Path, str]:
    root = Path(tempfile.mkdtemp(prefix="proof-runner-"))
    pid = "fixture-project"
    bindings = root / "1-Projects" / pid / "Factory-DRB" / "bindings"
    bindings.mkdir(parents=True)
    game = root / "1-Projects" / pid / "game"
    game.mkdir(parents=True)
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


def _install_two_rects(game: Path) -> None:
    state = game / "state"
    state.mkdir(parents=True, exist_ok=True)
    (state / "bounds.yaml").write_text(_TWO_RECT_BOUNDS, encoding="utf-8")
    tools = game / "tools"
    tools.mkdir(parents=True, exist_ok=True)


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

    def test_point_hits_solid_honest_second_rect(self) -> None:
        root, pid = _vault_with_catalog(
            {
                "hit": {
                    "op": "point_hits_solid",
                    "bounds": "state/bounds.yaml",
                    "point": [0.8, 0.8],
                    "argv": ["python3", "tools/hit.py"],
                }
            }
        )
        game = root / "1-Projects" / pid / "game"
        _install_two_rects(game)
        (game / "tools" / "hit.py").write_text(_HONEST_HIT, encoding="utf-8")
        out = run_named_probes(root, pid, ["hit"])
        self.assertTrue(out[0].ok, out[0].detail)
        self.assertIn("solid-b", out[0].detail)

    def test_point_hits_solid_constant_first_id_fails_on_second_rect(self) -> None:
        root, pid = _vault_with_catalog(
            {
                "hit": {
                    "op": "point_hits_solid",
                    "bounds": "state/bounds.yaml",
                    "point": [0.8, 0.8],
                    "argv": ["python3", "tools/const.py"],
                }
            }
        )
        game = root / "1-Projects" / pid / "game"
        _install_two_rects(game)
        (game / "tools" / "const.py").write_text(_CONSTANT_A, encoding="utf-8")
        out = run_named_probes(root, pid, ["hit"])
        self.assertFalse(out[0].ok, out[0].detail)

    def test_point_hits_solid_echo_fails(self) -> None:
        root, pid = _vault_with_catalog(
            {
                "hit": {
                    "op": "point_hits_solid",
                    "bounds": "state/bounds.yaml",
                    "point": [0.2, 0.2],
                    "argv": ["python3", "tools/echo.py"],
                }
            }
        )
        game = root / "1-Projects" / pid / "game"
        _install_two_rects(game)
        (game / "tools" / "echo.py").write_text(_ECHO_POINT, encoding="utf-8")
        out = run_named_probes(root, pid, ["hit"])
        self.assertFalse(out[0].ok)
        self.assertIn("echoed_point", out[0].detail)

    def test_point_hits_solid_outside_both_fails(self) -> None:
        root, pid = _vault_with_catalog(
            {
                "hit": {
                    "op": "point_hits_solid",
                    "bounds": "state/bounds.yaml",
                    "point": [0.5, 0.5],
                    "argv": ["python3", "tools/const.py"],
                }
            }
        )
        game = root / "1-Projects" / pid / "game"
        _install_two_rects(game)
        (game / "tools" / "const.py").write_text(_CONSTANT_A, encoding="utf-8")
        out = run_named_probes(root, pid, ["hit"])
        self.assertFalse(out[0].ok)
        self.assertIn("point_outside_all_bounds", out[0].detail)

    def test_point_hits_solid_costume_forbidden(self) -> None:
        root, pid = _vault_with_catalog(
            {
                "hit": {
                    "op": "point_hits_solid",
                    "bounds": "state/bounds.yaml",
                    "point": [0.2, 0.2],
                    "argv": ["python3", "tools/hit.py"],
                    "equals_from": {"path": "state/bounds.yaml", "key": "solids.0.id"},
                }
            }
        )
        game = root / "1-Projects" / pid / "game"
        _install_two_rects(game)
        (game / "tools" / "hit.py").write_text(_HONEST_HIT, encoding="utf-8")
        out = run_named_probes(root, pid, ["hit"])
        self.assertFalse(out[0].ok)
        self.assertIn("costume_forbidden", out[0].detail)


if __name__ == "__main__":
    unittest.main()
