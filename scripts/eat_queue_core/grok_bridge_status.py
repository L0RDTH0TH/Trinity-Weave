"""Grok bridge status surface — md + json for bone pilot and Grok."""

from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

from .grok_bridge_config import load_grok_bridge, project_branch_name
from .live_config import load_live_config
from .project_bridge_sync import verify_trinity_remote
from .weave_public_publish import compute_weave_publish_fingerprint, get_weave_publish_config

STATUS_MD_REL = Path("3-Resources/Second-Brain/Docs/Grok-Bridge-Status.md")
STATUS_JSON_REL = Path("3-Resources/Second-Brain/Docs/Grok-Bridge-Status.json")


def _git() -> str:
    return os.environ.get("GIT_PYTHON_GIT_EXECUTABLE", "git")


def _run(argv: list[str], *, cwd: Path, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _branch_commits_ahead(export_root: Path, branch: str) -> int:
    git = _git()
    cur = _run([git, "rev-parse", "--abbrev-ref", "HEAD"], cwd=export_root, timeout=30)
    current = (cur.stdout or "main").strip()
    _run([git, "checkout", branch], cwd=export_root, timeout=60)
    r = _run([git, "rev-list", "--count", f"origin/{branch}..HEAD"], cwd=export_root, timeout=60)
    if current:
        _run([git, "checkout", current], cwd=export_root, timeout=60)
    if r.returncode != 0:
        return 0
    try:
        return int((r.stdout or "0").strip())
    except ValueError:
        return 0


def compute_recommendation(
    *,
    main_ahead: int,
    project_ahead: int,
    weave_dirty: bool,
    push_disabled: bool,
    cooldown_active: bool,
) -> str:
    if push_disabled:
        return "push_disabled"
    if cooldown_active:
        return "awaiting_push_window"
    if weave_dirty and main_ahead > 0:
        return "push_main_recommended"
    if project_ahead > 0:
        return "push_project_recommended"
    if main_ahead == 0 and project_ahead == 0:
        return "local_fresh"
    return "local_fresh"


def build_status_payload(vault_root: Path, config_path: Path, *, cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    if cfg is None:
        cfg = load_grok_bridge(vault_root, config_path)
    merged = load_live_config(vault_root, config_path=config_path)
    wp = get_weave_publish_config(merged)
    export_root = Path(cfg["export_repo_root"])
    main_branch = cfg.get("main_branch") or "main"
    project_branch = project_branch_name(cfg)

    from .git_push_policy import git_push_enabled
    from .project_bridge_push import _load_push_state, push_allowed

    push_disabled = not git_push_enabled(merged)
    allowed, block_reason = push_allowed(vault_root, cfg, merged=merged)
    cooldown_active = block_reason == "cooldown"

    main_ahead = 0
    project_ahead = 0
    remote_ok = False
    remote_actual = ""
    if export_root.is_dir():
        remote_ok, remote_actual = verify_trinity_remote(export_root, cfg["remote_url"])
        if remote_ok:
            main_ahead = _branch_commits_ahead(export_root, main_branch)
            project_ahead = _branch_commits_ahead(export_root, project_branch)

    weave_fp = compute_weave_publish_fingerprint(vault_root, cfg=wp) if wp else ""
    push_state = _load_push_state(vault_root)
    last_push = push_state.get("last_push_utc")

    project_root = vault_root / "1-Projects" / cfg["pilot_project_id"]
    project_fp = ""
    obs_path = project_root / "PROJECT-OBSERVABILITY.json"
    if obs_path.is_file():
        try:
            obs = json.loads(obs_path.read_text(encoding="utf-8"))
            project_fp = str(obs.get("input_fingerprint") or "")
        except (OSError, ValueError):
            pass

    recommendation = compute_recommendation(
        main_ahead=main_ahead,
        project_ahead=project_ahead,
        weave_dirty=True,
        push_disabled=push_disabled,
        cooldown_active=cooldown_active,
    )

    next_eligible = None
    if cooldown_active and last_push:
        try:
            pe = cfg.get("push_economy") or {}
            last_dt = datetime.fromisoformat(str(last_push).replace("Z", "+00:00"))
            next_eligible = (last_dt + timedelta(hours=float(pe.get("push_cooldown_hours") or 24))).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        except ValueError:
            pass

    return {
        "schema_version": 1,
        "generated_utc": _utc_iso(),
        "export_repo_root": str(export_root),
        "remote_ok": remote_ok,
        "remote_actual": remote_actual,
        "active_branches": [main_branch, project_branch],
        "commits_ahead_per_branch": {main_branch: main_ahead, project_branch: project_ahead},
        "local_fingerprint": {"weave": weave_fp[:16] if weave_fp else "", "project": project_fp[:16] if project_fp else ""},
        "awaiting_push": main_ahead > 0 or project_ahead > 0,
        "last_successful_push_utc": last_push,
        "next_eligible_push_utc": next_eligible,
        "push_skipped_reason": block_reason if not allowed else None,
        "recommendation": recommendation,
        "gmmr_zero_bridge_budget": cfg.get("gmmr_zero_bridge_budget", True),
    }


def render_status_md(payload: dict[str, Any]) -> str:
    lines = [
        "# Grok Bridge Status",
        "",
        f"Generated: `{payload.get('generated_utc')}`",
        "",
        f"**Recommendation:** `{payload.get('recommendation')}`",
        "",
        "## Branches",
        "",
    ]
    for branch, ahead in (payload.get("commits_ahead_per_branch") or {}).items():
        lines.append(f"- `{branch}`: commits ahead = **{ahead}**")
    lines.extend(
        [
            "",
            "## Push",
            "",
            f"- Last successful push: `{payload.get('last_successful_push_utc') or '—'}`",
            f"- Next eligible push: `{payload.get('next_eligible_push_utc') or '—'}`",
            f"- Awaiting push: **{payload.get('awaiting_push')}**",
            f"- Remote OK (Trinity-Weave): **{payload.get('remote_ok')}**",
            "",
            "Machine-readable: `Grok-Bridge-Status.json` (same folder).",
            "",
        ]
    )
    return "\n".join(lines)


def write_grok_bridge_status(
    vault_root: Path,
    config_path: Path,
    *,
    cfg: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = build_status_payload(vault_root, config_path, cfg=cfg)
    md_path = vault_root / STATUS_MD_REL
    json_path = vault_root / STATUS_JSON_REL
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(render_status_md(payload), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "md": md_path.relative_to(vault_root).as_posix(), "json": json_path.relative_to(vault_root).as_posix(), "recommendation": payload.get("recommendation")}
