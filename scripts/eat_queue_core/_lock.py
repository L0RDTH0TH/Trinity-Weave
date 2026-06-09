"""Shared gitforge_lock.py wrapper (single-writer parity with post_queue_gitforge)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def gitforge_lock_script(vault_root: Path) -> Path:
    return vault_root / "scripts" / "gitforge_lock.py"


def acquire_gitforge_lock(vault_root: Path, track: str, timeout_s: float) -> bool:
    script = gitforge_lock_script(vault_root)
    if not script.is_file():
        return False
    r = subprocess.run(
        [
            sys.executable,
            str(script),
            "acquire",
            "--vault-root",
            str(vault_root),
            "--track",
            track,
            "--timeout",
            str(int(timeout_s)),
        ],
        cwd=vault_root,
        capture_output=True,
        text=True,
        timeout=int(timeout_s) + 5,
    )
    return r.returncode == 0


def release_gitforge_lock(vault_root: Path) -> None:
    script = gitforge_lock_script(vault_root)
    if not script.is_file():
        return
    subprocess.run(
        [sys.executable, str(script), "release", "--vault-root", str(vault_root)],
        cwd=vault_root,
        capture_output=True,
        text=True,
        timeout=30,
    )
