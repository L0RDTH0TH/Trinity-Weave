"""Engine preflight — MCP, Godot binary, dotnet build baseline."""

from __future__ import annotations

import os
import shutil
import socket
import subprocess
from pathlib import Path
from typing import Any


def _tcp_open(host: str, port: int, timeout: float = 1.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def resolve_godot_binary() -> str | None:
    for candidate in (
        os.environ.get("GODOT_BIN"),
        shutil.which("godot"),
        str(Path.home() / ".local/bin/godot"),
        str(Path.home() / "Applications/godot-4.6.3-mono/Godot_v4.6.3-stable_mono_linux_x86_64"),
    ):
        if candidate and Path(candidate).is_file():
            return candidate
    return None


def resolve_dotnet_binary() -> str | None:
    for candidate in (
        os.environ.get("DOTNET_ROOT"),
        str(Path.home() / ".dotnet/dotnet"),
        shutil.which("dotnet"),
    ):
        if not candidate:
            continue
        p = Path(candidate)
        if p.is_file():
            return str(p)
        dotnet = p / "dotnet"
        if dotnet.is_file():
            return str(dotnet)
    return shutil.which("dotnet")


def run_engine_preflight(
    vault_root: Path,
    repo_rel: str,
    *,
    requires_mcp: bool = True,
    mcp_port: int = 6505,
    run_dotnet_build: bool = True,
) -> dict[str, Any]:
    """Return ok + checks list; does not mutate vault."""
    vault_root = vault_root.resolve()
    repo = Path(repo_rel)
    if not repo.is_absolute():
        repo = vault_root / repo
    checks: list[dict[str, Any]] = []

    if requires_mcp:
        mcp_ok = _tcp_open("127.0.0.1", mcp_port)
        checks.append(
            {
                "check": "mcp_websocket",
                "status": "pass" if mcp_ok else "fail",
                "detail": f"127.0.0.1:{mcp_port}",
            }
        )
    else:
        checks.append({"check": "mcp_websocket", "status": "skip", "detail": "not required"})

    godot = resolve_godot_binary()
    checks.append(
        {
            "check": "godot_binary",
            "status": "pass" if godot else "warn",
            "detail": godot or "not found",
        }
    )

    dotnet = resolve_dotnet_binary()
    checks.append(
        {
            "check": "dotnet_binary",
            "status": "pass" if dotnet else "fail",
            "detail": dotnet or "not found",
        }
    )

    pg = repo / "project.godot"
    checks.append(
        {
            "check": "project_godot",
            "status": "pass" if pg.is_file() else "fail",
            "path": str(pg.relative_to(vault_root)) if pg.is_file() else str(pg),
        }
    )

    if run_dotnet_build and dotnet and (repo / "GenesisMythosDemo.csproj").is_file():
        try:
            r = subprocess.run(
                [dotnet, "build", str(repo / "GenesisMythosDemo.csproj")],
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=180,
            )
            checks.append(
                {
                    "check": "dotnet_build_baseline",
                    "status": "pass" if r.returncode == 0 else "fail",
                    "exit_code": r.returncode,
                    "stderr_tail": (r.stderr or "")[-500:],
                }
            )
        except (subprocess.TimeoutExpired, OSError) as e:
            checks.append({"check": "dotnet_build_baseline", "status": "fail", "error": str(e)})
    elif run_dotnet_build:
        checks.append({"check": "dotnet_build_baseline", "status": "skip", "detail": "no csproj"})

    failed = [c for c in checks if c.get("status") == "fail"]
    return {
        "ok": len(failed) == 0,
        "checks": checks,
        "repo_root": str(repo.relative_to(vault_root)) if repo.is_relative_to(vault_root) else str(repo),
        "godot_binary": godot,
        "dotnet_binary": dotnet,
    }
