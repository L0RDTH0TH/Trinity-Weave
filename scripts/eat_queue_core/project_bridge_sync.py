"""Sync project surface to Trinity-Weave project/* branch with safe switch preflight."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ._lock import acquire_gitforge_lock as _acquire_lock
from ._lock import release_gitforge_lock as _release_lock
from .git_push_policy import effective_push
from .grok_bridge_config import load_grok_bridge, project_branch_name, project_dir
from .grok_bridge_export_session import clear_session, read_session, write_session
from .live_config import load_live_config
from .weave.project_observability import write_project_observability_artifacts
from .weave.project_tertiary_index import write_tertiary_artifacts

MAIN_FORBIDDEN_PREFIXES = (
    "Roadmap/",
    "1-Projects/",
    "2-Areas/",
    "Ingest/",
    "4-Archives/",
    "5-Attachments/",
    "TERTIARY-INDEX.json",
    "PROJECT-OBSERVABILITY.json",
    "GROK-PROJECT-START.md",
)

# Project branches are instance-only — never ship weave law / harness / Docs from main.
PROJECT_ALLOWED_EXACT = frozenset(
    {
        "GROK-PROJECT-START.md",
        "PROJECT-OBSERVABILITY.json",
        "TERTIARY-INDEX.json",
    }
)
PROJECT_ALLOWED_PREFIXES = (
    "Roadmap/",
)


@dataclass
class ProjectBridgeSyncResult:
    status: str
    exit_code: int
    payload: dict[str, Any]


def _git() -> str:
    return os.environ.get("GIT_PYTHON_GIT_EXECUTABLE", "git")


def _run(argv: list[str], *, cwd: Path, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def verify_trinity_remote(export_root: Path, expected_url: str) -> tuple[bool, str]:
    r = _run([_git(), "remote", "get-url", "origin"], cwd=export_root, timeout=30)
    if r.returncode != 0:
        return False, (r.stderr or r.stdout or "no origin").strip()
    actual = (r.stdout or "").strip()
    norm = lambda u: re.sub(r"\.git$", "", u.rstrip("/")).lower()
    if norm(actual) != norm(expected_url):
        return False, actual
    if "genesis-mythos-master-roadmap" in actual.lower() or "gmm-roadmap" in actual.lower():
        return False, actual
    return True, actual


def _is_project_allowed_rel(rel: str, project_id: str | None = None) -> bool:
    if rel in PROJECT_ALLOWED_EXACT:
        return True
    for prefix in PROJECT_ALLOWED_PREFIXES:
        if rel.startswith(prefix):
            return True
    if project_id:
        if rel == f"{project_id}-goal.md" or rel == f"{project_id}-Roadmap-MOC.md":
            return True
    # Allow goal/MOC naming without requiring project_id when scanning loosely
    if rel.endswith("-goal.md") or rel.endswith("-Roadmap-MOC.md"):
        if "/" not in rel:
            return True
    return False


def scan_branch_forbidden(export_root: Path, branch: str, *, project_id: str | None = None) -> list[str]:
    hits: list[str] = []
    for root, dirs, files in os.walk(export_root):
        # skip .git
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in files:
            rel = (Path(root) / name).relative_to(export_root).as_posix()
            if branch == "main":
                for prefix in MAIN_FORBIDDEN_PREFIXES:
                    if rel.startswith(prefix) or rel == prefix.rstrip("/"):
                        hits.append(rel)
                        break
            else:
                # project/* — anything outside allowlist is forbidden (incl. weave/, scripts/, Docs/)
                if not _is_project_allowed_rel(rel, project_id):
                    hits.append(rel)
    return hits


def wipe_export_worktree(export_root: Path) -> list[str]:
    """Remove all worktree entries except `.git`. Returns removed names."""
    removed: list[str] = []
    for child in list(export_root.iterdir()):
        if child.name == ".git":
            continue
        removed.append(child.name)
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink(missing_ok=True)
    return removed


def checkout_orphan_project_branch(
    export_root: Path,
    branch: str,
    *,
    main_branch: str,
) -> dict[str, Any]:
    """Create/replace local project branch as orphan (no weave history)."""
    git = _git()
    # Always start from main so we drop polluted project tip before orphaning.
    co_main = _run([git, "checkout", main_branch], cwd=export_root, timeout=60)
    if co_main.returncode != 0:
        return {"ok": False, "error": "checkout_main_failed", "stderr": co_main.stderr}
    # Delete local branch if present (remote tip replaced on force push).
    _run([git, "branch", "-D", branch], cwd=export_root, timeout=30)
    orphan = _run([git, "checkout", "--orphan", branch], cwd=export_root, timeout=60)
    if orphan.returncode != 0:
        return {"ok": False, "error": "orphan_checkout_failed", "stderr": orphan.stderr}
    # Clear index + worktree leftovers from the start-point tree.
    _run([git, "rm", "-rf", "--ignore-unmatch", "."], cwd=export_root, timeout=120)
    removed = wipe_export_worktree(export_root)
    return {"ok": True, "removed": removed}


def heal_stale_session(vault_root: Path, export_root: Path, cfg: dict[str, Any]) -> dict[str, Any] | None:
    session = read_session(vault_root)
    if not session or not session.get("in_progress"):
        return None
    git = _git()
    main_branch = cfg.get("main_branch") or "main"
    target = str(session.get("target_branch") or "")
    healed: dict[str, Any] = {"healed": True, "session": session}
    try:
        cur = _run([git, "rev-parse", "--abbrev-ref", "HEAD"], cwd=export_root, timeout=30)
        current = (cur.stdout or "").strip()
        if current != main_branch:
            _run([git, "checkout", main_branch], cwd=export_root, timeout=60)
        healed["restored_branch"] = main_branch
    except Exception as exc:  # noqa: BLE001
        healed["error"] = str(exc)
    clear_session(vault_root)
    return healed


def _project_files_to_copy(project_root: Path, project_id: str) -> list[tuple[Path, str]]:
    pairs: list[tuple[Path, str]] = []
    for name in (
        "GROK-PROJECT-START.md",
        "PROJECT-OBSERVABILITY.json",
        "TERTIARY-INDEX.json",
        f"{project_id}-goal.md",
        f"{project_id}-Roadmap-MOC.md",
    ):
        src = project_root / name
        if src.is_file():
            pairs.append((src, name))
    roadmap = project_root / "Roadmap"
    if roadmap.is_dir():
        pairs.append((roadmap, "Roadmap"))
    return pairs


def sync_project_to_export(
    vault_root: Path,
    export_root: Path,
    project_id: str,
    *,
    cfg: dict[str, Any],
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    export_root = export_root.resolve()
    project_root = project_dir(vault_root, project_id)
    branch = project_branch_name(cfg, project_id)
    main_branch = cfg.get("main_branch") or "main"

    ok_remote, remote_actual = verify_trinity_remote(export_root, cfg["remote_url"])
    if not ok_remote:
        return {"ok": False, "error": "wrong_export_remote", "remote_actual": remote_actual}

    heal = heal_stale_session(vault_root, export_root, cfg)
    git = _git()

    lock_name = "grok_bridge_sync"
    prev_branch_r = _run([git, "rev-parse", "--abbrev-ref", "HEAD"], cwd=export_root, timeout=30)
    previous_branch = (prev_branch_r.stdout or main_branch).strip()
    prev_head_r = _run([git, "rev-parse", "HEAD"], cwd=export_root, timeout=30)
    previous_head = (prev_head_r.stdout or "").strip()

    write_session(
        vault_root,
        {
            "in_progress": True,
            "previous_branch": previous_branch,
            "previous_head": previous_head,
            "target_branch": branch,
            "export_root": str(export_root),
            "remote_url": remote_actual,
        },
    )

    try:
        st = _run([git, "status", "--porcelain"], cwd=export_root, timeout=60)
        if st.returncode != 0:
            return {"ok": False, "error": "git_status_failed", "stderr": st.stderr}
        if (st.stdout or "").strip():
            return {"ok": False, "error": "export_worktree_dirty", "status": st.stdout[:500]}

        orphan = checkout_orphan_project_branch(
            export_root, branch, main_branch=main_branch
        )
        if not orphan.get("ok"):
            return orphan

        copied: list[str] = []
        for src, dest_name in _project_files_to_copy(project_root, project_id):
            dest = export_root / dest_name
            if src.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(
                    src,
                    dest,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
                )
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
            copied.append(dest_name)

        hits = scan_branch_forbidden(export_root, branch, project_id=project_id)
        if hits:
            return {"ok": False, "error": "forbidden_on_branch", "paths": hits[:40]}

        msg = f"chore(grok-bridge): project sync {project_id} {_utc_now()}"
        _run([git, "add", "-A"], cwd=export_root, timeout=120)
        commit_sha = None
        if (_run([git, "status", "--porcelain"], cwd=export_root).stdout or "").strip():
            c = _run([git, "commit", "-m", msg], cwd=export_root, timeout=120)
            if c.returncode != 0:
                return {"ok": False, "error": "commit_failed", "stderr": c.stderr}
            rev = _run([git, "rev-parse", "HEAD"], cwd=export_root, timeout=30)
            commit_sha = (rev.stdout or "").strip()
        else:
            return {"ok": False, "error": "nothing_to_commit", "copied": copied}

        return {
            "ok": True,
            "branch": branch,
            "copied": copied,
            "commit": commit_sha,
            "orphan": True,
            "heal": heal,
        }
    finally:
        _run([git, "checkout", main_branch], cwd=export_root, timeout=60)
        clear_session(vault_root)


def run_project_bridge_sync(
    vault_root: Path,
    config_path: Path,
    *,
    project_id: str | None = None,
    push: bool = False,
    use_lock: bool = True,
) -> ProjectBridgeSyncResult:
    vault_root = vault_root.resolve()
    merged = load_live_config(vault_root, config_path=config_path)
    cfg = load_grok_bridge(vault_root, config_path)

    if not cfg.get("enabled", True):
        return ProjectBridgeSyncResult("skipped", 0, {"reason": "grok_bridge_disabled"})

    pid = project_id or cfg["pilot_project_id"]
    export_root = Path(cfg["export_repo_root"])

    lock_acquired = False
    if use_lock:
        lock_acquired = _acquire_lock(vault_root, "project_bridge_sync", 30.0)
        if not lock_acquired:
            return ProjectBridgeSyncResult("skipped", 0, {"reason": "gitforge_lock_held"})

    try:
        tertiary = write_tertiary_artifacts(vault_root, pid, deny_globs=cfg.get("deny_globs"))
        obs = write_project_observability_artifacts(
            vault_root,
            pid,
            cfg=cfg,
            tertiary_fingerprint=str(tertiary.get("fingerprint") or ""),
        )

        if not export_root.is_dir():
            return ProjectBridgeSyncResult(
                "failed",
                1,
                {"reason": "export_root_missing", "path": str(export_root)},
            )

        sync_out = sync_project_to_export(vault_root, export_root, pid, cfg=cfg)
        if not sync_out.get("ok"):
            return ProjectBridgeSyncResult("failed", 1, sync_out)

        from .grok_bridge_status import write_grok_bridge_status

        status_out = write_grok_bridge_status(vault_root, config_path, cfg=cfg)

        payload = {
            "project_id": pid,
            "tertiary": tertiary,
            "observability": obs,
            "sync": sync_out,
            "status": status_out,
            "local_current": True,
        }

        if push and effective_push(True, merged):
            from .project_bridge_push import run_project_bridge_push

            push_result = run_project_bridge_push(
                vault_root,
                config_path,
                branch=sync_out.get("branch"),
                use_lock=False,
            )
            payload["push"] = push_result.payload

        return ProjectBridgeSyncResult("completed", 0, payload)
    finally:
        if lock_acquired:
            _release_lock(vault_root)
