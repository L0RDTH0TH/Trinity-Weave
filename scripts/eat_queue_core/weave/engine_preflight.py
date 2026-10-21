"""Engine preflight — run project build_command argv only; no binary invent.

Empty build_command → no checks that invent Godot/dotnet. Non-empty →
command_exits_zero style run of that argv in the game repo.
"""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path
from typing import Any


def run_engine_preflight(
    vault_root: Path,
    repo_rel: str,
    *,
    project_id: str | None = None,
    build_command: str | None = None,
    requires_mcp: bool = False,
    mcp_port: int | None = None,
    run_dotnet_build: bool = False,
) -> dict[str, Any]:
    """Return ok + checks. Does not search for Godot or invent dotnet builds."""
    del run_dotnet_build  # legacy kw ignored — use build_command only
    vault_root = vault_root.resolve()
    repo = Path(repo_rel)
    if not repo.is_absolute():
        repo = vault_root / repo
    checks: list[dict[str, Any]] = []

    cmd = (build_command or "").strip()
    if not cmd and project_id:
        from .factory.bindings import BindingMissingError, resolve as bind_resolve

        try:
            cmd = str(
                bind_resolve(vault_root, project_id, "engine", "build_command") or ""
            ).strip()
        except BindingMissingError:
            raise

    if requires_mcp and mcp_port is not None:
        import socket

        try:
            with socket.create_connection(("127.0.0.1", int(mcp_port)), timeout=1.5):
                mcp_ok = True
        except OSError:
            mcp_ok = False
        checks.append(
            {
                "check": "mcp_websocket",
                "status": "pass" if mcp_ok else "fail",
                "detail": f"127.0.0.1:{mcp_port}",
            }
        )

    if not cmd:
        return {
            "ok": True,
            "checks": checks
            + [{"check": "build_command", "status": "skip", "detail": "empty"}],
            "repo_root": str(repo.relative_to(vault_root))
            if repo.is_relative_to(vault_root)
            else str(repo),
            "build_command": "",
        }

    argv = shlex.split(cmd) if isinstance(cmd, str) else [str(x) for x in cmd]
    try:
        proc = subprocess.run(
            argv,
            cwd=str(repo),
            capture_output=True,
            text=True,
            timeout=300,
        )
        ok = proc.returncode == 0
        checks.append(
            {
                "check": "build_command",
                "status": "pass" if ok else "fail",
                "argv": argv,
                "exit_code": proc.returncode,
                "stderr_tail": (proc.stderr or "")[-500:],
            }
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        checks.append(
            {"check": "build_command", "status": "fail", "error": str(exc), "argv": argv}
        )

    failed = [c for c in checks if c.get("status") == "fail"]
    return {
        "ok": len(failed) == 0,
        "checks": checks,
        "repo_root": str(repo.relative_to(vault_root))
        if repo.is_relative_to(vault_root)
        else str(repo),
        "build_command": cmd,
    }
