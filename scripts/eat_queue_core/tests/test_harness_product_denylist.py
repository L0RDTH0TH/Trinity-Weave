"""Regression net — production scripts must not embed product poison.

Grow PASS1_TOKENS / STRUCTURAL only in the same commit that deletes those
strings from production. Tests/ may still mention them.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SCRIPTS_ROOT = Path(__file__).resolve().parents[1]  # eat_queue_core/

# Pass 1 — tokens this pass removes from production. Extend in Pass 2/3 commits.
PASS1_TOKENS: tuple[str, ...] = (
    "genesis-mythos-demo",
    "genesis-mythos-alpha",
    "Horizon-Q3",
    "CANONICAL_PROJECT_ID",
    "DEFAULT_PILOT_PROJECT_ID",
    "DEFAULT_GAME_REPO_REL",
)

# Pass 2 — only tokens this commit deletes from production.
# Terrain3D / DualGrid / Sparky / points_as_grid / ClosedAlpha wait for Pass 3
# (prefer_authorship → host-law data rows).
PASS2_TOKENS: tuple[str, ...] = (
    "LaunchShell",
    "PlayRegion",
    "half_b",
    "alpha_core_loop",
    "LANE_ADAPTER",
    "cs_type_exists",
    "main_scene_equals",
    "KINESTHETIC_IDS",
    "SLICE_LANE_CHECKLISTS",
)


# Pass 4 — eat-path fail-closed; same commit that deletes these from production.
PASS4_TOKENS: tuple[str, ...] = (
    "Flow_Launch",
    "Nav_LookWhileMove_FP",
    "Nav_LookWhileMove_DM",
    "Flow_DM_Mode",
    "Flow_Ortho_Tabletop",
    "Terrain3D",
    "DualGrid",
    "points_as_grid",
    "Y19Mw5YsgjI",
    "GameHud",
    "Hot Wheels",
    "godot_4_6_3_dotnet",
    "KINESTHETIC_CHECKLIST_IDS",
    "YT_CANONICAL",
    "WORLDGEN_SLICE_MARKERS",
    "run_closed_alpha_release_readiness_pass",
    "resolve_godot_binary",
)

# Structural — engine/path product shapes outside the one bindings path helper.
STRUCTURAL_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("res_uri", re.compile(r"res://")),
    ("tscn", re.compile(r"\.tscn\b")),
    ("code_repos", re.compile(r"Code-Repos/")),
    (
        "baked_projects_slug",
        re.compile(r"1-Projects/[A-Za-z0-9_-]+/"),
    ),
)

# Production files allowed to contain the vault-layout pattern via bindings helper only.
_PATH_HELPER_ALLOW: frozenset[str] = frozenset(
    {
        "weave/factory/bindings.py",
    }
)


def _iter_production_py() -> list[Path]:
    out: list[Path] = []
    for path in SCRIPTS_ROOT.rglob("*.py"):
        rel = path.relative_to(SCRIPTS_ROOT).as_posix()
        if rel.startswith("tests/"):
            continue
        if "/__pycache__/" in f"/{rel}/":
            continue
        out.append(path)
    return out


class HarnessProductDenylistTests(unittest.TestCase):
    def test_pass1_tokens_absent_from_production(self) -> None:
        hits: list[str] = []
        for path in _iter_production_py():
            text = path.read_text(encoding="utf-8", errors="replace")
            rel = path.relative_to(SCRIPTS_ROOT).as_posix()
            for tok in PASS1_TOKENS:
                if tok in text:
                    hits.append(f"{rel}:{tok}")
        self.assertEqual(
            hits,
            [],
            "Pass-1 denylist tokens still in production:\n" + "\n".join(hits),
        )

    def test_pass2_tokens_absent_from_production(self) -> None:
        hits: list[str] = []
        for path in _iter_production_py():
            text = path.read_text(encoding="utf-8", errors="replace")
            rel = path.relative_to(SCRIPTS_ROOT).as_posix()
            for tok in PASS2_TOKENS:
                if tok in text:
                    hits.append(f"{rel}:{tok}")
        self.assertEqual(
            hits,
            [],
            "Pass-2 denylist tokens still in production:\n" + "\n".join(hits),
        )


    def test_pass4_tokens_absent_from_production(self) -> None:
        hits: list[str] = []
        for path in _iter_production_py():
            text = path.read_text(encoding="utf-8", errors="replace")
            rel = path.relative_to(SCRIPTS_ROOT).as_posix()
            for tok in PASS4_TOKENS:
                if tok in text:
                    hits.append(f"{rel}:{tok}")
        # Lane default: production must not default queue/lane to "godot".
        lane_pat = re.compile(
            r'(?:queue_lane|lane)\s*=\s*"godot"|default\s*=\s*"godot"|or\s+"godot"'
        )
        for path in _iter_production_py():
            text = path.read_text(encoding="utf-8", errors="replace")
            rel = path.relative_to(SCRIPTS_ROOT).as_posix()
            # Parallel-track enumerations in trinity_* are infrastructure, not factory lane defaults.
            if rel.startswith("weave/trinity_"):
                continue
            for m in lane_pat.finditer(text):
                hits.append(f"{rel}:godot_lane_default:{m.group(0)}")
        self.assertEqual(
            hits,
            [],
            "Pass-4 denylist tokens still in production:\n" + "\n".join(hits),
        )

    def test_structural_product_shapes_absent(self) -> None:
        hits: list[str] = []
        for path in _iter_production_py():
            rel = path.relative_to(SCRIPTS_ROOT).as_posix()
            text = path.read_text(encoding="utf-8", errors="replace")
            for name, pat in STRUCTURAL_PATTERNS:
                if name == "baked_projects_slug" and rel in _PATH_HELPER_ALLOW:
                    # bindings.py may contain the layout template once.
                    if text.count("1-Projects/") <= 2 and "Factory-DRB/bindings" in text:
                        continue
                if pat.search(text):
                    hits.append(f"{rel}:{name}")
        self.assertEqual(
            hits,
            [],
            "Structural product shapes still in production:\n" + "\n".join(hits),
        )


if __name__ == "__main__":
    unittest.main()
