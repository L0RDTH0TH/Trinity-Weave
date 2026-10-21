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
