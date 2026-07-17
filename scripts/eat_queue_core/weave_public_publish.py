"""Trinity-Weave public export — allowlisted weave slice; no project/factory bleed."""

from __future__ import annotations

import hashlib
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .git_push_policy import effective_push
from .gitforge_config import get_parallel_execution_config, lock_timeout_seconds, merge_yaml_blocks_from_config
from .live_config import load_live_config
from ._lock import acquire_gitforge_lock as _acquire_lock_impl
from ._lock import release_gitforge_lock as _release_lock_impl

# Normative forbidden prefixes — factory / project output must never land in Trinity-Weave.
DEFAULT_FORBIDDEN_PREFIXES: tuple[str, ...] = (
    "1-Projects/",
    "2-Areas/",
    "3-Resources/",
    "Ingest/",
    "Roadmap/",
    "4-Archives/",
    "5-Attachments/",
    ".technical/parallel/",
    ".technical/prompt-queue",
    ".technical/Run-Telemetry/",
    ".cursor/rules/",
    ".cursor/skills/",
    ".cursor/agents/",
    ".cursor/sync/",
    ".trash/",
)

# Vault-relative allowlist (light Phase 18 weave core).
DEFAULT_INCLUDE_PATHS: tuple[str, ...] = (
    "3-Resources/Second-Brain/Docs/Weave-Core-Manifest.md",
    "3-Resources/Second-Brain/Docs/External-Weave-Handoff.md",
    "3-Resources/Second-Brain/Docs/Grok-Trinity-Weave-Context.md",
    "3-Resources/Second-Brain/Docs/GROK-START-HERE.md",
    "3-Resources/Second-Brain/Docs/GROK-OBSERVABILITY.md",
    "3-Resources/Second-Brain/Docs/ARCHITECTURE-OVERVIEW.md",
    "3-Resources/Second-Brain/Docs/GLOSSARY-FOR-EXTERNAL-READERS.md",
    "3-Resources/Second-Brain/Docs/Maintenance-Trinity-Constitution.md",
    "3-Resources/Second-Brain/Docs/Trinity-Weave-Export-README.md",
    "3-Resources/Second-Brain/Docs/Grok-Second-Brain-Custom-Instructions.md",
    "3-Resources/Second-Brain/Docs/GROK-PROJECT-BRIDGE.md",
    "3-Resources/Second-Brain/Docs/Grok-Bridge-Status.md",
    "3-Resources/Second-Brain/Docs/Grok-Bridge-Status.json",
    "3-Resources/Second-Brain/Docs/gmm-catalog-mint/",
    "3-Resources/Second-Brain/Docs/meat-suit-entry/",
    ".technical/weave/components/",
    ".technical/weave/component-proposals/",
    ".technical/weave/trinity-partition-registry.yaml",
    ".technical/weave/host-weld/manifest.yaml",
    ".technical/weave/host-weld/live/",
    ".cursor/rules/always/host-weld-bridge.mdc",
    "scripts/eat_queue_core/weave/",
    "scripts/eat_queue_core/weave_public_publish.py",
    "scripts/eat_queue_core/weave_observability.py",
    "scripts/eat_queue_core/project_bridge_sync.py",
    "scripts/eat_queue_core/project_bridge_push.py",
    "scripts/eat_queue_core/grok_bridge_status.py",
    "scripts/eat_queue_core/grok_bridge_config.py",
    "scripts/eat_queue_core/grok_bridge_export_session.py",
    "scripts/eat_queue_core/grok_fulfill_broker.py",
    "scripts/eat_queue_core/weave/project_observability.py",
    "scripts/eat_queue_core/weave/project_tertiary_index.py",
    "scripts/eat_queue_core/post_queue_weave_publish.py",
    "scripts/eat_queue_core/harness.py",
    "scripts/eat_queue_core/live_config.py",
    "scripts/eat_queue_core/gitforge_config.py",
    "scripts/eat_queue_core/_lock.py",
    "scripts/eat_queue_core/schedule_tick.py",
    "scripts/eat_queue_core/schedule_planes.py",
    "scripts/eat_queue_core/schedule_state.py",
    "scripts/eat_queue_core/schedule_config.py",
    "scripts/eat_queue_core/pseudo_clock.py",
    "scripts/eat_queue_core/requirements.txt",
)

DEFAULT_TEST_GLOBS: tuple[str, ...] = (
    "scripts/eat_queue_core/tests/test_weave_public_publish.py",
    "scripts/eat_queue_core/tests/test_weave*.py",
    "scripts/eat_queue_core/tests/test_trinity*.py",
    "scripts/eat_queue_core/tests/test_schedule*.py",
    "scripts/eat_queue_core/tests/test_grok_guards.py",
    "scripts/eat_queue_core/tests/test_grok_bridge.py",
    "scripts/eat_queue_core/tests/test_pseudo_clock.py",
)


@dataclass
class WeavePublicPublishResult:
    status: str  # completed | skipped | failed
    exit_code: int
    payload: dict[str, Any]


def get_weave_publish_config(merged: dict[str, Any]) -> dict[str, Any]:
    raw = merged.get("weave_publish")
    return raw if isinstance(raw, dict) else {}


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _git_executable() -> str:
    return os.environ.get("GIT_PYTHON_GIT_EXECUTABLE", "git")


def _run(argv: list[str], *, cwd: Path | None = None, timeout: int = 600) -> subprocess.CompletedProcess[str]:
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
    heading = f"\n### {_utc_now()} — weave_publish | harness\n\n"
    body = "\n".join(lines) + "\n"
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(heading)
            f.write(body)
        return path
    except OSError:
        return None


def resolve_forbidden_prefixes(cfg: dict[str, Any]) -> list[str]:
    contract = cfg.get("export_contract")
    if isinstance(contract, dict):
        raw = contract.get("forbidden_prefixes")
        if isinstance(raw, list) and raw:
            return [str(x).replace("\\", "/").strip() for x in raw if str(x).strip()]
    return list(DEFAULT_FORBIDDEN_PREFIXES)


def resolve_include_paths(cfg: dict[str, Any], vault_root: Path) -> list[Path]:
    contract = cfg.get("export_contract")
    rels: list[str] = []
    if isinstance(contract, dict):
        raw = contract.get("includes")
        if isinstance(raw, list) and raw:
            rels = [str(x).replace("\\", "/").strip() for x in raw if str(x).strip()]
    if not rels:
        rels = list(DEFAULT_INCLUDE_PATHS)

    test_globs = DEFAULT_TEST_GLOBS
    if isinstance(contract, dict):
        tg = contract.get("test_includes")
        if isinstance(tg, list) and tg:
            test_globs = tuple(str(x) for x in tg)

    vault_root = vault_root.resolve()
    paths: list[Path] = []
    seen: set[str] = set()

    def add(p: Path) -> None:
        key = p.resolve().as_posix()
        if key not in seen and p.exists():
            seen.add(key)
            paths.append(p)

    for rel in rels:
        add(vault_root / rel)

    for pattern in test_globs:
        for p in vault_root.glob(pattern):
            add(p)

    return paths


def _export_map_path(vault_path: Path, vault_root: Path) -> str:
    """Map vault path to export-repo-relative path."""
    rel = vault_path.resolve().relative_to(vault_root.resolve()).as_posix()
    # Bone-pilot hub ships at repo root as meat-suit-entry/ (not under Docs/)
    mse_prefix = "3-Resources/Second-Brain/Docs/meat-suit-entry"
    if rel == mse_prefix:
        return "meat-suit-entry"
    if rel.startswith(mse_prefix + "/"):
        return "meat-suit-entry/" + rel[len(mse_prefix) + 1 :]
    if rel.startswith("3-Resources/Second-Brain/Docs/"):
        return "Docs/" + rel.split("3-Resources/Second-Brain/Docs/", 1)[1]
    if rel.startswith(".technical/weave/"):
        return "weave/" + rel.split(".technical/weave/", 1)[1]
    if rel.startswith(".technical/weave/host-weld/"):
        return rel.replace(".technical/weave/", "weave/", 1)
    if rel == ".cursor/rules/always/host-weld-bridge.mdc":
        return "Docs/Rules/host-weld-bridge.mdc"
    if rel.startswith("scripts/eat_queue_core/"):
        return rel
    return rel


def _fingerprint_file(path: Path) -> str:
    st = path.stat()
    return f"{path.resolve().as_posix()}:{st.st_mtime_ns}:{st.st_size}"


def compute_weave_publish_fingerprint(
    vault_root: Path,
    *,
    cfg: dict[str, Any] | None = None,
) -> str:
    """Content manifest hash for allowlisted weave sources (change detection)."""
    vault_root = vault_root.resolve()
    wp = cfg or {}
    sources = resolve_include_paths(wp, vault_root)
    parts: list[str] = []
    for src in sorted(sources, key=lambda p: p.as_posix()):
        if src.is_file():
            try:
                parts.append(_fingerprint_file(src))
            except OSError:
                continue
        elif src.is_dir():
            for f in sorted(src.rglob("*"), key=lambda p: p.as_posix()):
                if f.is_file():
                    try:
                        parts.append(_fingerprint_file(f))
                    except OSError:
                        continue
    payload = "\n".join(parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def weave_publish_commit_subject(
    *,
    tick_count: int | None = None,
    summary: str = "",
    trigger: str = "schedule_tick",
) -> str:
    """Standardized commit subject for Trinity-Weave external backup."""
    parts = ["chore(weave):", trigger]
    if tick_count is not None:
        parts.append(f"tick={tick_count}")
    parts.append("external-backup sync")
    if summary:
        parts.append(f"— {summary[:80]}")
    return " ".join(parts)[:200]


def run_weave_publish_on_schedule_tick(
    vault_root: Path,
    config_path: Path,
    state: dict[str, Any],
    *,
    tick_count: int,
    plane: str = "listener",
    planes_cfg: Any | None = None,
) -> dict[str, Any] | None:
    """
    Change-gated Trinity-Weave publish for pseudo-clock / schedule_tick.

    Skips when fingerprint unchanged. Updates schedule state on success.
    """
    vault_root = vault_root.resolve()
    merged = load_live_config(vault_root, config_path=config_path)
    wp = get_weave_publish_config(merged)
    if not wp.get("enabled", True):
        return {
            "action": "weave_public_publish",
            "skipped": True,
            "reason": "weave_publish_disabled",
            "plane": plane,
        }
    if wp.get("on_schedule_tick", True) is False:
        return {
            "action": "weave_public_publish",
            "skipped": True,
            "reason": "on_schedule_tick_disabled",
            "plane": plane,
        }

    if planes_cfg is None:
        from .schedule_config import load_schedule_planes_config

        planes_cfg = load_schedule_planes_config(vault_root)

    if not getattr(planes_cfg, "weave_publish_on_tick_enabled", True):
        return {
            "action": "weave_public_publish",
            "skipped": True,
            "reason": "weave_publish_on_tick_disabled",
            "plane": plane,
        }

    every_n = int(getattr(planes_cfg, "weave_publish_every_n_ticks", 1) or 1)
    if every_n > 0 and tick_count > 0 and tick_count % every_n != 0:
        return {
            "action": "weave_public_publish",
            "skipped": True,
            "reason": "cadence_skip",
            "every_n_ticks": every_n,
            "plane": plane,
        }

    fingerprint = compute_weave_publish_fingerprint(vault_root, cfg=wp)
    prior = str(state.get("weave_publish_fingerprint") or "")
    if prior and prior == fingerprint:
        return {
            "action": "weave_public_publish",
            "skipped": True,
            "reason": "unchanged_fingerprint",
            "fingerprint": fingerprint[:16],
            "plane": plane,
        }

    subject = weave_publish_commit_subject(tick_count=tick_count, trigger="schedule_tick")
    result = run_weave_public_sync(
        vault_root,
        config_path,
        push=bool(wp.get("push_on_sync", True)),
        summary=subject.replace("chore(weave): ", "", 1),
        use_lock=True,
    )
    payload = dict(result.payload)
    action: dict[str, Any] = {
        "action": "weave_public_publish",
        "plane": plane,
        "status": result.status,
        "exit_code": result.exit_code,
        "fingerprint": fingerprint[:16],
        "prior_fingerprint": prior[:16] if prior else None,
        "commit": payload.get("commit"),
        "pushed": payload.get("pushed"),
    }
    if result.status == "completed" and result.exit_code == 0:
        state["weave_publish_fingerprint"] = fingerprint
        state["last_weave_publish_at"] = _utc_now()
        if payload.get("commit"):
            state["last_weave_publish_commit"] = payload.get("commit")
    elif result.status == "skipped":
        action["skipped"] = True
        action["reason"] = payload.get("reason")
    else:
        action["error"] = payload.get("reason") or payload.get("error")
    return action


def scan_forbidden(paths: list[str], forbidden: list[str]) -> list[str]:
    hits: list[str] = []
    for p in paths:
        pl = p.replace("\\", "/").lstrip("./")
        for prefix in forbidden:
            if pl.startswith(prefix) or f"/{prefix}" in f"/{pl}":
                hits.append(pl)
                break
    return hits


def sync_weave_public_export(
    vault_root: Path,
    export_root: Path,
    *,
    cfg: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Copy allowlisted vault paths into export checkout (destructive clean per subtree)."""
    vault_root = vault_root.resolve()
    export_root = export_root.resolve()
    wp = cfg or {}
    forbidden = resolve_forbidden_prefixes(wp)
    sources = resolve_include_paths(wp, vault_root)

    if not sources:
        return {"ok": False, "error": "no_include_paths", "message": "allowlist resolved empty"}

    copied: list[str] = []
    import shutil

    readme_src = vault_root / "3-Resources/Second-Brain/Docs/Trinity-Weave-Export-README.md"
    if readme_src.is_file():
        export_root.mkdir(parents=True, exist_ok=True)
        shutil.copy2(readme_src, export_root / "README.md")
        copied.append("README.md")

    for src in sources:
        dest_rel = _export_map_path(src, vault_root)
        dest = export_root / dest_rel
        if src.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
        copied.append(dest_rel)

    # Prune legacy bone-pilot path (renamed to meat-suit-entry/ at repo root)
    legacy_bp = export_root / "Docs" / "bone-pilot"
    if legacy_bp.exists():
        shutil.rmtree(legacy_bp)

    # Post-sync forbidden scan on all export files
    all_paths: list[str] = []
    for root, _dirs, files in os.walk(export_root):
        for name in files:
            full = Path(root) / name
            all_paths.append(full.relative_to(export_root).as_posix())

    hits = scan_forbidden(all_paths, forbidden)
    if hits:
        return {
            "ok": False,
            "error": "forbidden_paths_detected",
            "paths_sample": hits[:30],
            "copied_before_fail": copied,
        }

    fingerprint = compute_weave_publish_fingerprint(vault_root, cfg=wp)
    from .weave_observability import write_observability_artifacts

    obs = write_observability_artifacts(
        export_root,
        vault_root,
        fingerprint=fingerprint,
    )
    copied.extend(
        [
            obs.get("observability_json", "OBSERVABILITY.json"),
            obs.get("card_index", "weave/CARD-INDEX.md"),
            "GROK-START-HERE.md",
        ]
    )

    all_paths_after: list[str] = []
    for root, _dirs, files in os.walk(export_root):
        for name in files:
            all_paths_after.append((Path(root) / name).relative_to(export_root).as_posix())

    return {
        "ok": True,
        "copied": copied,
        "file_count": len(all_paths_after),
        "fingerprint": fingerprint,
        "observability": obs,
    }


def run_weave_public_sync(
    vault_root: Path,
    config_path: Path,
    *,
    push: bool = True,
    dry_run: bool = False,
    summary: str = "",
    use_lock: bool = True,
) -> WeavePublicPublishResult:
    vault_root = vault_root.resolve()
    merged = load_live_config(vault_root, config_path=config_path)
    wp = get_weave_publish_config(merged)
    pe = get_parallel_execution_config(merged)
    gf = merged.get("gitforge") if isinstance(merged.get("gitforge"), dict) else {}

    def finish(status: str, code: int, payload: dict[str, Any], audit: list[str] | None = None) -> WeavePublicPublishResult:
        if audit:
            _append_audit(vault_root, audit)
        payload["status"] = status
        payload["exit_code"] = code
        return WeavePublicPublishResult(status=status, exit_code=code, payload=payload)

    if not wp.get("enabled", True):
        return finish(
            "skipped",
            0,
            {"reason": "weave_publish_disabled"},
            ["| result | skipped |", "| reason | weave_publish_disabled |"],
        )

    export_root_s = wp.get("export_repo_root")
    if not isinstance(export_root_s, str) or not export_root_s.strip():
        return finish("failed", 1, {"reason": "export_repo_root_missing"})

    export_root = Path(export_root_s).expanduser().resolve()
    branch = str(wp.get("branch") or "main")
    remote_url = str(wp.get("remote_url") or "https://github.com/L0RDTH0TH/Trinity-Weave.git")
    allow_push = effective_push(push, merged)

    lock_acquired = False
    if use_lock:
        timeout_s = float(lock_timeout_seconds(pe, gf if isinstance(gf, dict) else {}))
        lock_acquired = _acquire_lock_impl(vault_root, "weave_publish", timeout_s)
        if not lock_acquired:
            return finish(
                "skipped",
                0,
                {"reason": "gitforge_lock_held", "message": "weave publish skipped — lock held"},
                ["| result | skipped |", "| reason | gitforge_lock_held |"],
            )

    try:
        if not export_root.is_dir():
            export_root.mkdir(parents=True, exist_ok=True)
            git = _git_executable()
            init = _run([git, "init"], cwd=export_root, timeout=60)
            if init.returncode != 0:
                return finish("failed", 1, {"reason": "export_init_failed", "stderr": init.stderr})
            _run([git, "remote", "add", "origin", remote_url], cwd=export_root, timeout=30)
            _run([git, "checkout", "-b", branch], cwd=export_root, timeout=30)

        sync_out = sync_weave_public_export(vault_root, export_root, cfg=wp)
        if not sync_out.get("ok"):
            return finish(
                "failed",
                1,
                {"reason": sync_out.get("error", "sync_failed"), **sync_out},
                [f"| result | failed |", f"| reason | {sync_out.get('error')} |"],
            )

        if dry_run:
            return finish(
                "completed",
                0,
                {"dry_run": True, "sync": sync_out, "push": False},
                ["| result | completed |", "| mode | dry_run |"],
            )

        git = _git_executable()
        st = _run([git, "status", "--porcelain"], cwd=export_root, timeout=60)
        if st.returncode != 0:
            return finish("failed", 1, {"reason": "git_status_failed", "stderr": st.stderr})

        commit_sha: str | None = None
        if (st.stdout or "").strip():
            _run([git, "add", "-A"], cwd=export_root, timeout=120).check_returncode()
            if summary.startswith("chore(weave):"):
                msg = summary[:200]
            elif summary.startswith("schedule_tick"):
                msg = weave_publish_commit_subject(summary=summary, trigger="schedule_tick")[:200]
            else:
                msg = f"chore(weave): public sync {summary or _utc_now()}"[:200]
            c = _run([git, "commit", "-m", msg], cwd=export_root, timeout=120)
            if c.returncode != 0:
                return finish("failed", 1, {"reason": "export_commit_failed", "stderr": c.stderr})
            rev = _run([git, "rev-parse", "HEAD"], cwd=export_root, timeout=30)
            if rev.returncode == 0:
                commit_sha = (rev.stdout or "").strip()

        pushed = False
        if allow_push and commit_sha:
            pu = _run([git, "push", "-u", "origin", branch], cwd=export_root, timeout=300)
            if pu.returncode != 0:
                return finish(
                    "failed",
                    1,
                    {"reason": "export_push_failed", "stderr": pu.stderr, "commit": commit_sha},
                )
            pushed = True
        elif commit_sha and push and not allow_push:
            pass  # local commit only — master git.push_enabled false

        payload_push_meta: dict[str, Any] = {}
        if push and not allow_push:
            payload_push_meta["push_skipped_git_push_disabled"] = True

        return finish(
            "completed",
            0,
            {
                "sync": sync_out,
                "commit": commit_sha,
                "pushed": pushed,
                **payload_push_meta,
                "export_repo_root": str(export_root),
                "branch": branch,
                "remote_url": remote_url,
            },
            [
                "| result | completed |",
                f"| commit | `{commit_sha or '—'}` |",
                f"| pushed | {pushed} |",
                f"| files | {sync_out.get('file_count', '—')} |",
            ],
        )
    finally:
        if lock_acquired:
            _release_lock_impl(vault_root)
