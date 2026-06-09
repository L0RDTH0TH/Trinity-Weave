"""Smoke test (10e-b blanket rewrite for corps conduct).
Trinity: catchup_corpus_tunnel
"""

from __future__ import annotations

import importlib
import unittest


class TestTrinityCatchupSweepSmoke(unittest.TestCase):
    def test_module_importable(self) -> None:
        importlib.import_module("eat_queue_core.weave.trinity_catchup_sweep")
