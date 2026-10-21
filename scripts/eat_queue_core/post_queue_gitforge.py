"""Deterministic GitForge post–A.7: lock, vault git, optional export sync, audit log."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .git_push_policy import git_push_enabled
from .gitforge_config import (
    get_gitforge_config,
    get_parallel_execution_config,
    lock_timeout_seconds,
    merge_yaml_blocks_from_config,
)
from .live_config import load_live_config
from ._lock import acquire_gitforge_lock as _acquire_lock_impl
from ._lock import release_gitforge_lock as _release_lock_impl


@dataclass
class PostQueueGitForgeResult:
    status: str  # completed | skipped | failed | pending_clarifier
    exit_code: int  # 0 ok/skip; non-zero hard fail
    payload: dict[str, Any]

    def to_json(self) -> str:
        return json.dumps(self.payload, indent=2)


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _run(
    argv: list[str],
    *,
    cwd: Path | None = None,
    timeout: int = 600,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def _append_audit(vault_root: Path, lines: list[str]) -> Path | None:
    rel = Path("3-Resources/Second-Brain/Docs/git-audit-log.md")
    path = vault_root / rel
    if not path.parent.is_dir():
        return None
    heading = f"\n### {_utc_now()} — gitforge | harness\n\n"
    body = "\n".join(lines) + "\n"
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(heading)
            f.write(body)
        return path
    except OSError:
        return None


def _git_executable() -> str:
    return os.environ.get("GIT_PYTHON_GIT_EXECUTABLE", "git")


def _acquire_lock(vault_root: Path, track: str, timeout_s: float) -> bool:
    return _acquire_lock_impl(vault_root, track, timeout_s)


def _release_lock(vault_root: Path) -> None:
    _release_lock_impl(vault_root)


def _rsync_delete(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    _run(["rsync", "-a", "--delete", str(src) + "/", str(dst) + "/"], timeout=600).check_returncode()


def _sync_integration_export(vault_root: Path, export_root: Path, gmm_project_root: Path | None) -> None:
    """Mirror vault → export per git-push-workflow Step 1 (integration)."""
    v = vault_root.resolve()
    sb = v / "3-Resources/Second-Brain"
    er = export_root.resolve()
    shutil_mod = __import__("shutil")
    # README
    readme_src = sb / "Docs/GitHub-Export-Repository-README.md"
    if readme_src.is_file():
        shutil_mod.copy2(readme_src, er / "README.md")
    for sub in ("agents", "rules", "skills", "sync"):
        _rsync_delete(v / ".cursor" / sub, er / ".cursor" / sub)
    er.joinpath("scripts").mkdir(parents=True, exist_ok=True)
    _rsync_delete(v / "scripts" / "eat_queue_core", er / "scripts" / "eat_queue_core")
    for name in ("queue-gate-compute.py", "gitforge_lock.py"):
        p = v / "scripts" / name
        if p.is_file():
            shutil_mod.copy2(p, er / "scripts" / name)
    _rsync_delete(sb / "Docs", er / "Docs")
    core = er / "Docs" / "Core"
    core.mkdir(parents=True, exist_ok=True)
    for f in sb.glob("*.md"):
        shutil_mod.copy2(f, core / f.name)
    rs = v / "Roadmap Structure.md"
    if rs.is_file():
        shutil_mod.copy2(rs, core / "Roadmap Structure.md")
    for name in ("Errors.md", "Watcher-Result.md", "Watcher-Signal.md"):
        p = v / "3-Resources" / name
        if p.is_file():
            shutil_mod.copy2(p, core / name)
    rts = sb / "Docs" / "Core" / "Run-Telemetry-Summary.md"
    if rts.is_file():
        shutil_mod.copy2(rts, core / "Run-Telemetry-Summary.md")
    uflow = sb / "Second-Brain-User-Flows"
    if uflow.is_dir():
        _rsync_delete(uflow, er / "Docs" / "Second-Brain-User-Flows")
    if gmm_project_root and gmm_project_root.is_dir():
        proj = gmm_project_root.resolve()
        pid = proj.name
        _rsync_delete(proj / "Roadmap", er / "Roadmap")
        for suffix in (f"{pid}-goal.md", f"{pid}-Roadmap-MOC.md"):
            src = proj / suffix
            if src.is_file():
                shutil_mod.copy2(src, er / suffix)


def _sync_engine_export(vault_root: Path, export_root: Path, gmm_project_root: Path) -> None:
    proj = gmm_project_root.resolve()
    er = export_root.resolve()
    pid = proj.name
    shutil_mod = __import__("shutil")
    _rsync_delete(proj / "Roadmap", er / "Roadmap")
    for suffix in (f"{pid}-goal.md", f"{pid}-Roadmap-MOC.md"):
        src = proj / suffix
        if src.is_file():
            shutil_mod.copy2(src, er / suffix)


def _export_forbidden_on_engine(paths: list[str]) -> bool:
    for p in paths:
        pl = p.replace("\\", "/").strip()
        if pl.startswith(".cursor/") or pl.startswith("scripts/") or pl.startswith("Docs/"):
            return True
    return False


def _resolve_gmm_from_handoff(vault_root: Path, handoff: dict[str, Any], pe: dict[str, Any]) -> Path | None:
    pt = handoff.get("parallel_track")
    if not pt:
        return None
    tracks = pe.get("tracks")
    if not isinstance(tracks, list):
        return None
    for tr in tracks:
        if not isinstance(tr, dict):
            continue
        if str(tr.get("id", "")).lower() == str(pt).lower():
            lid = tr.get("lane_project_id")
            if isinstance(lid, str) and lid.strip():
                p = vault_root / "1-Projects" / lid.strip()
                if p.is_dir():
                    return p
    return None


def _vault_remote_ok(vault_root: Path) -> bool:
    git = _git_executable()
    r = _run([git, "remote", "-v"], cwd=vault_root, timeout=30)
    return r.returncode == 0 and "origin" in (r.stdout or "")


def _export_remote_ok(export_root: Path) -> bool:
    git = _git_executable()
    r = _run([git, "remote", "-v"], cwd=export_root, timeout=30)
    return r.returncode == 0 and bool((r.stdout or "").strip())


def run_post_queue_gitforge(
    vault_root: Path,
    handoff: dict[str, Any],
    config_path: Path,
) -> PostQueueGitForgeResult:
    vault_root = vault_root.resolve()
    merged = load_live_config(vault_root, config_path=config_path)
    gf = get_gitforge_config(merged)
    pe = get_parallel_execution_config(merged)
    allow_remote_push = git_push_enabled(merged)

    def finish(
        status: str,
        exit_code: int,
        payload: dict[str, Any],
        audit_lines: list[str] | None = None,
    ) -> PostQueueGitForgeResult:
        if audit_lines is None:
            audit_lines = [
                f"| result | {status} |",
                f"| vault_root | `{vault_root}` |",
            ]
        _append_audit(vault_root, audit_lines)
        payload_out = dict(payload)
        payload_out["status"] = status
        payload_out["exit_code"] = exit_code
        return PostQueueGitForgeResult(status=status, exit_code=exit_code, payload=payload_out)

    harness_enabled = gf.get("harness_enabled", True)
    if harness_enabled is False:
        return finish(
            "skipped",
            0,
            {"reason": "harness_disabled", "message": "gitforge.harness_enabled is false"},
            audit_lines=[
                "| result | skipped |",
                "| reason | harness_disabled |",
                f"| vault_root | `{vault_root}` |",
            ],
        )

    if not handoff.get("queue_success", False):
        return finish(
            "skipped",
            0,
            {"reason": "queue_not_clean_success", "message": "queue_success false"},
            audit_lines=[
                "| result | skipped |",
                "| reason | queue_not_clean_success |",
                f"| vault_root | `{vault_root}` |",
            ],
        )

    mode = str(handoff.get("mode") or "balance").lower()
    if mode == "fast":
        return finish(
            "skipped",
            0,
            {"reason": "unexpected_fast_mode_handoff", "message": "mode fast"},
            audit_lines=[
                "| result | skipped |",
                "| reason | unexpected_fast_mode_handoff |",
            ],
        )

    require_clarifier = bool(gf.get("require_clarifier", False))
    clar = (handoff.get("clarifier_input") or "").strip()
    if require_clarifier and not clar:
        return finish(
            "pending_clarifier",
            0,
            {"reason": "pending_clarifier", "message": "clarifier required by config"},
            audit_lines=[
                "| result | pending_clarifier |",
                "| reason | missing clarifier_input |",
            ],
        )

    if not gf.get("enabled", True):
        return finish(
            "skipped",
            0,
            {"reason": "gitforge_disabled", "message": "gitforge.enabled false"},
        )

    track = str(handoff.get("parallel_track") or "unknown").lower()
    timeout_s = float(lock_timeout_seconds(pe, gf))
    lock_acquired = _acquire_lock(vault_root, track, timeout_s)
    if not lock_acquired:
        return finish(
            "skipped",
            0,
            {
                "reason": "gitforge_lock_held",
                "message": "GitForge skipped — lock held by other track",
                "parallel_track": handoff.get("parallel_track"),
                "lock_held_skip": True,
            },
            audit_lines=[
                "| result | skipped |",
                "| reason | gitforge_lock_held |",
                f"| parallel_track | {handoff.get('parallel_track', '—')} |",
            ],
        )

    actions: list[str] = ["audit_logged"]
    vault_commit_sha: str | None = None
    export_commit_sha: str | None = None

    try:
        git = _git_executable()
        if not _vault_remote_ok(vault_root):
            return finish(
                "failed",
                1,
                {
                    "reason": "remote_check_failed",
                    "message": "vault repo has no origin remote",
                    "actions": actions,
                },
                audit_lines=[
                    "| result | failed |",
                    "| reason | remote_check_failed (vault) |",
                ],
            )

        st = _run([git, "status", "--porcelain"], cwd=vault_root, timeout=60)
        if st.returncode != 0:
            return finish(
                "failed",
                1,
                {"reason": "git_status_failed", "stderr": st.stderr},
            )

        dirty = bool((st.stdout or "").strip())
        source_mode = handoff.get("source_pipeline_mode") or "balance"
        run_id = handoff.get("eat_queue_run_id") or ""
        summary = (handoff.get("changes_summary") or "")[:120]
        subj_parts = ["chore(vault): eat-queue"]
        if run_id:
            subj_parts.append(str(run_id))
        if summary:
            subj_parts.append(summary)
        subj_parts.append(f"[{source_mode}]")
        if clar:
            subj_parts.insert(1, clar[:40])
        subject = " ".join(subj_parts)[:200]

        if dirty:
            _run([git, "add", "-A"], cwd=vault_root, timeout=120).check_returncode()
            c = _run([git, "commit", "-m", subject], cwd=vault_root, timeout=120)
            if c.returncode != 0:
                return finish(
                    "failed",
                    1,
                    {
                        "reason": "vault_commit_failed",
                        "stderr": c.stderr,
                        "actions": actions,
                    },
                )
            actions.append("commit_attempted")
            rev = _run([git, "rev-parse", "HEAD"], cwd=vault_root, timeout=30)
            if rev.returncode == 0:
                vault_commit_sha = (rev.stdout or "").strip()

            dry = _run([git, "push", "--dry-run"], cwd=vault_root, timeout=120)
            if dry.returncode != 0:
                return finish(
                    "failed",
                    1,
                    {
                        "reason": "vault_push_dry_run_failed",
                        "stderr": dry.stderr,
                        "actions": actions,
                    },
                )
            pu = _run([git, "push"], cwd=vault_root, timeout=300)
            if pu.returncode != 0:
                return finish(
                    "failed",
                    1,
                    {
                        "reason": "vault_push_failed",
                        "stderr": pu.stderr,
                        "actions": actions,
                    },
                )
            actions.append("push_attempted")
        else:
            actions.append("vault_clean_no_commit")

        modes = gf.get("modes") if isinstance(gf.get("modes"), dict) else {}
        balance = modes.get("balance") if isinstance(modes.get("balance"), dict) else {}
        export_sync = bool(balance.get("export_sync", False))

        export_root_s = gf.get("export_repo_root")
        integration_branch = str(gf.get("integration_branch") or "iteration-2-roadmap-rules")

        if export_sync and isinstance(export_root_s, str) and export_root_s.strip():
            export_root = Path(export_root_s).expanduser().resolve()
            if not export_root.is_dir():
                return finish(
                    "failed",
                    1,
                    {
                        "reason": "export_repo_missing",
                        "export_repo_root": str(export_root),
                        "actions": actions,
                    },
                )
            if not _export_remote_ok(export_root):
                return finish(
                    "failed",
                    1,
                    {"reason": "remote_check_failed", "message": "export repo has no remote", "actions": actions},
                )

            br = _run([git, "branch", "--show-current"], cwd=export_root, timeout=30)
            cur_branch = (br.stdout or "").strip() if br.returncode == 0 else ""

            gmm = _resolve_gmm_from_handoff(vault_root, handoff, pe)
            env_gmm = os.environ.get("GMM_PROJECT_ROOT")
            if env_gmm:
                eg = Path(env_gmm).expanduser()
                if eg.is_dir():
                    gmm = eg.resolve()

            try:
                if cur_branch == integration_branch:
                    _sync_integration_export(vault_root, export_root, gmm)
                elif cur_branch != integration_branch and (
                    cur_branch.startswith("project/")
                    or cur_branch.startswith("sandbox-")
                    or os.environ.get("GMM_PROJECT_ROOT")
                ):
                    # Engine export for project/sandbox tracks — no baked product slugs.
                    if not gmm or not gmm.is_dir():
                        return finish(
                            "failed",
                            1,
                            {
                                "reason": "gmm_project_root_required",
                                "message": "engine export requires GMM_PROJECT_ROOT or resolvable parallel_track",
                                "actions": actions,
                            },
                        )
                    _sync_engine_export(vault_root, export_root, gmm)
                else:
                    return finish(
                        "failed",
                        1,
                        {
                            "reason": "export_branch_unknown",
                            "branch": cur_branch,
                            "actions": actions,
                        },
                    )

                st2 = _run([git, "status", "--porcelain"], cwd=export_root, timeout=60)
                paths_changed = [x[3:] for x in (st2.stdout or "").splitlines() if len(x) > 3]

                if cur_branch != integration_branch and _export_forbidden_on_engine(paths_changed):
                    return finish(
                        "failed",
                        1,
                        {
                            "reason": "engine_branch_forbidden_global_surfaces",
                            "paths_sample": paths_changed[:20],
                            "actions": actions,
                        },
                    )

                if (st2.stdout or "").strip():
                    _run([git, "add", "-A"], cwd=export_root, timeout=120).check_returncode()
                    ec = _run(
                        [git, "commit", "-m", f"chore(export): sync from vault {run_id or summary or 'eat-queue'}"],
                        cwd=export_root,
                        timeout=120,
                    )
                    if ec.returncode != 0:
                        return finish(
                            "failed",
                            1,
                            {"reason": "export_commit_failed", "stderr": ec.stderr, "actions": actions},
                        )
                    er = _run([git, "rev-parse", "HEAD"], cwd=export_root, timeout=30)
                    if er.returncode == 0:
                        export_commit_sha = (er.stdout or "").strip()
                    if allow_remote_push:
                        ep = _run([git, "push"], cwd=export_root, timeout=300)
                        if ep.returncode != 0:
                            return finish(
                                "failed",
                                1,
                                {"reason": "export_push_failed", "stderr": ep.stderr, "actions": actions},
                            )
                        actions.append("export_sync_attempted")
                    else:
                        actions.append("export_push_skipped_git_push_disabled")
            except OSError as e:
                return finish(
                    "failed",
                    1,
                    {"reason": "export_sync_exception", "error": str(e)[:500], "actions": actions},
                )
        else:
            actions.append("export_sync_skipped")

        payload = {
            "gitforge_result": {
                "status": "completed",
                "queue_success": True,
                "mode": "balance",
                "source_pipeline_mode": source_mode,
                "actions": actions,
                "message": "harness post_queue_gitforge completed",
                "git_push_enabled": allow_remote_push,
            },
            "vault_commit": vault_commit_sha,
            "export_commit": export_commit_sha,
            "parallel_track": handoff.get("parallel_track"),
        }
        audit_lines = [
            "| result | completed |",
            f"| actions | {'; '.join(actions)} |",
            f"| vault_commit | `{vault_commit_sha or '—'}` |",
            f"| export_commit | `{export_commit_sha or '—'}` |",
        ]
        _append_audit(vault_root, audit_lines)
        payload["status"] = "completed"
        payload["exit_code"] = 0
        return PostQueueGitForgeResult(status="completed", exit_code=0, payload=payload)

    finally:
        _release_lock(vault_root)


def load_handoff_json(path: Path | None, stdin_text: str | None) -> dict[str, Any]:
    if path is not None:
        raw = path.read_text(encoding="utf-8")
    elif stdin_text is not None:
        raw = stdin_text
    else:
        raise ValueError("handoff file or stdin required")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("handoff must be a JSON object")
    return data
