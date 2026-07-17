"""Budgeted push for Trinity-Weave main or project branches."""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

from ._lock import acquire_gitforge_lock as _acquire_lock
from ._lock import release_gitforge_lock as _release_lock
from .git_push_policy import effective_push, git_push_enabled
from .grok_bridge_config import load_grok_bridge, project_branch_name
from .live_config import load_live_config

PUSH_STATE_REL = Path(".technical/grok-bridge/push-state.json")


@dataclass
class ProjectBridgePushResult:
    status: str
    exit_code: int
    payload: dict[str, Any]


def _git() -> str:
    return os.environ.get("GIT_PYTHON_GIT_EXECUTABLE", "git")


def _run(argv: list[str], *, cwd: Path, timeout: int = 300) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_push_state(vault_root: Path) -> dict[str, Any]:
    path = vault_root / PUSH_STATE_REL
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def _save_push_state(vault_root: Path, state: dict[str, Any]) -> None:
    path = vault_root / PUSH_STATE_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def _commits_ahead(export_root: Path, branch: str) -> int:
    git = _git()
    _run([git, "checkout", branch], cwd=export_root, timeout=60)
    r = _run([git, "rev-list", "--count", f"origin/{branch}..HEAD"], cwd=export_root, timeout=60)
    if r.returncode != 0:
        r2 = _run([git, "rev-list", "--count", "HEAD"], cwd=export_root, timeout=60)
        try:
            return int((r2.stdout or "0").strip())
        except ValueError:
            return 0
    try:
        return int((r.stdout or "0").strip())
    except ValueError:
        return 0


def push_allowed(
    vault_root: Path,
    cfg: dict[str, Any],
    *,
    force: bool = False,
    merged: dict[str, Any] | None = None,
) -> tuple[bool, str]:
    if merged and not git_push_enabled(merged):
        return False, "push_disabled"
    pe = cfg.get("push_economy") or {}
    if not force or not pe.get("allow_force_push_override", True):
        state = _load_push_state(vault_root)
        last = state.get("last_push_utc")
        cooldown_h = float(pe.get("push_cooldown_hours") or 24)
        if last:
            try:
                last_dt = datetime.fromisoformat(str(last).replace("Z", "+00:00"))
                if datetime.now(timezone.utc) < last_dt + timedelta(hours=cooldown_h):
                    return False, "cooldown"
            except ValueError:
                pass
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        week = datetime.now(timezone.utc).strftime("%G-W%V")
        daily = int(state.get("pushes_today") or 0) if state.get("daily_key") == today else 0
        weekly = int(state.get("pushes_week") or 0) if state.get("weekly_key") == week else 0
        if daily >= int(pe.get("max_pushes_per_day") or 1):
            return False, "daily_budget"
        if weekly >= int(pe.get("max_pushes_per_week") or 5):
            return False, "weekly_budget"
    return True, "ok"


def run_project_bridge_push(
    vault_root: Path,
    config_path: Path,
    *,
    branch: str | None = None,
    force: bool = False,
    use_lock: bool = True,
) -> ProjectBridgePushResult:
    vault_root = vault_root.resolve()
    merged = load_live_config(vault_root, config_path=config_path)
    cfg = load_grok_bridge(vault_root, config_path)
    export_root = Path(cfg["export_repo_root"])
    main_branch = cfg.get("main_branch") or "main"
    target_branch = branch or project_branch_name(cfg)

    if not cfg.get("enabled", True):
        return ProjectBridgePushResult("skipped", 0, {"reason": "grok_bridge_disabled"})

    allowed, reason = push_allowed(vault_root, cfg, force=force, merged=merged)
    if not allowed:
        return ProjectBridgePushResult("skipped", 0, {"reason": reason, "branch": target_branch})

    if not effective_push(True, merged):
        return ProjectBridgePushResult("skipped", 0, {"reason": "git_push_disabled", "branch": target_branch})

    lock_acquired = False
    if use_lock:
        lock_acquired = _acquire_lock(vault_root, "project_bridge_push", 30.0)
        if not lock_acquired:
            return ProjectBridgePushResult("skipped", 0, {"reason": "gitforge_lock_held"})

    try:
        from .project_bridge_sync import verify_trinity_remote

        ok_remote, remote_actual = verify_trinity_remote(export_root, cfg["remote_url"])
        if not ok_remote:
            return ProjectBridgePushResult("failed", 1, {"error": "wrong_export_remote", "remote": remote_actual})

        git = _git()
        ahead = _commits_ahead(export_root, target_branch)
        if ahead == 0:
            return ProjectBridgePushResult("completed", 0, {"branch": target_branch, "pushed": False, "reason": "nothing_to_push"})

        pu = _run([git, "push", "-u", "origin", target_branch], cwd=export_root, timeout=300)
        if pu.returncode != 0:
            return ProjectBridgePushResult(
                "failed",
                1,
                {"error": "push_failed", "stderr": pu.stderr, "branch": target_branch},
            )

        state = _load_push_state(vault_root)
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        week = datetime.now(timezone.utc).strftime("%G-W%V")
        state["last_push_utc"] = _utc_iso()
        state["last_branch"] = target_branch
        state["daily_key"] = today
        state["weekly_key"] = week
        state["pushes_today"] = (int(state.get("pushes_today") or 0) if state.get("daily_key") == today else 0) + 1
        state["pushes_week"] = (int(state.get("pushes_week") or 0) if state.get("weekly_key") == week else 0) + 1
        if force:
            state["last_force"] = _utc_iso()
        _save_push_state(vault_root, state)

        _run([git, "checkout", main_branch], cwd=export_root, timeout=60)

        from .grok_bridge_status import write_grok_bridge_status

        status_out = write_grok_bridge_status(vault_root, config_path, cfg=cfg)

        return ProjectBridgePushResult(
            "completed",
            0,
            {
                "branch": target_branch,
                "pushed": True,
                "commits_ahead_before": ahead,
                "force": force,
                "status": status_out,
            },
        )
    finally:
        if lock_acquired:
            _release_lock(vault_root)
