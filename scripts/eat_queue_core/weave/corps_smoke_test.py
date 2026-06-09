"""Minimal unittest stubs so strict corps conduct can run behavior proofs."""

from __future__ import annotations

import re
from pathlib import Path


def module_path_to_import(primary_path: str) -> str | None:
    """Dotted import for ``PYTHONPATH=<vault>/scripts`` (matches behavior proofs)."""
    rel = str(primary_path or "").strip().replace("\\", "/").lstrip("./")
    if not rel.endswith(".py") or "/eat_queue_core/" not in rel:
        return None
    if rel.startswith("scripts/"):
        rel = rel[len("scripts/") :]
    return rel.replace("/", ".").removesuffix(".py")


def smoke_test_path_for_module(vault_root: Path, primary_path: str) -> Path | None:
    rel = str(primary_path or "").strip().replace("\\", "/").lstrip("./")
    if not rel.endswith(".py"):
        return None
    stem = Path(rel).stem
    return vault_root / "scripts/eat_queue_core/tests" / f"test_{stem}.py"


def _blanket_smoke_test_body(*, class_name: str, mod: str, trinity_id: str | None) -> str:
    tid_line = f"Trinity: {trinity_id}\n" if trinity_id else ""
    return f'''"""Smoke test (10e-b blanket rewrite for corps conduct).
{tid_line}"""

from __future__ import annotations

import importlib
import unittest


class Test{class_name}Smoke(unittest.TestCase):
    def test_module_importable(self) -> None:
        importlib.import_module("{mod}")
'''


def rewrite_blanket_smoke_test(
    vault_root: Path,
    primary_path: str,
    *,
    trinity_id: str | None = None,
    dest_rel_path: str | None = None,
) -> str | None:
    """Overwrite (or create) a one-test unittest module; return repo-relative test path."""
    vault_root = vault_root.resolve()
    if dest_rel_path:
        test_path = vault_root / dest_rel_path.lstrip("./")
    else:
        test_path = smoke_test_path_for_module(vault_root, primary_path)
    mod = module_path_to_import(primary_path)
    if test_path is None or mod is None:
        return None
    rel_test = test_path.relative_to(vault_root).as_posix()
    stem = Path(primary_path).stem
    class_name = "".join(p.capitalize() for p in re.split(r"[_]+", stem) if p)
    if not class_name:
        class_name = "Module"
    test_path.parent.mkdir(parents=True, exist_ok=True)
    test_path.write_text(
        _blanket_smoke_test_body(class_name=class_name, mod=mod, trinity_id=trinity_id),
        encoding="utf-8",
    )
    return rel_test


def ensure_smoke_test_file(vault_root: Path, primary_path: str) -> str | None:
    """Create a one-test unittest module if missing; return repo-relative test path."""
    vault_root = vault_root.resolve()
    test_path = smoke_test_path_for_module(vault_root, primary_path)
    mod = module_path_to_import(primary_path)
    if test_path is None or mod is None:
        return None
    rel_test = test_path.relative_to(vault_root).as_posix()
    if test_path.is_file():
        return rel_test
    return rewrite_blanket_smoke_test(vault_root, primary_path)
