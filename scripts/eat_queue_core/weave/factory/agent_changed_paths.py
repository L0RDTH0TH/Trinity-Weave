"""Extract repo-relative changed paths from factory lane agent output."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

from .structure_lint import filter_paths_to_zone_write

_PATH_RE = re.compile(
    r"(?:(?:[\w.-]+/)+[\w.-]+\.(?:cs|tscn|csproj|yaml|yml|md|gd|shader|tres|import|json))|"
    r"(?:UI|assets|content|audio|Core|Systems|Camera|Player)/[\w./-]+"
)

_VAULT_PATH_PREFIXES = ("1-Projects/", "3-Resources/", "Ingest/", "4-Archives/")


def _normalize_rel(path: str) -> str:
    return path.strip().lstrip("./").replace("\\", "/")


def extract_paths_from_log_text(text: str) -> set[str]:
    """Parse repo-like paths mentioned in agent log prose."""
    found: set[str] = set()
    for match in _PATH_RE.findall(text):
        p = _normalize_rel(match)
        if p:
            found.add(p)
    return found


def collect_git_artifact_paths(repo: Path) -> set[str]:
    """Repo-relative paths from git diff + untracked (empty when not a git repo)."""
    repo = repo.resolve()
    found: set[str] = set()
    if not (repo / ".git").is_dir():
        return found
    try:
        r = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=repo,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if r.returncode == 0:
            for line in r.stdout.splitlines():
                p = _normalize_rel(line)
                if p:
                    found.add(p)
        r2 = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=repo,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if r2.returncode == 0:
            for line in r2.stdout.splitlines():
                p = _normalize_rel(line)
                if p:
                    found.add(p)
    except (subprocess.TimeoutExpired, OSError):
        pass
    return found


def is_vault_handoff_path(rel_posix: str) -> bool:
    """Paths under vault PARA/DRB trees are handoff references, not game-repo artifacts."""
    norm = _normalize_rel(rel_posix)
    return norm.startswith(_VAULT_PATH_PREFIXES)


def extract_changed_paths_from_agent(
    vault_root: Path,
    agent_out: dict[str, Any],
    repo_rel: str,
    *,
    zone_write: list[str] | None = None,
) -> tuple[str, ...]:
    """
    Best-effort paths for structure_pass zone lint.

    When zone_write is set (lane-scoped lint), evidence is git artifacts filtered to
    the lane zone; log grep is only used as fallback when git is unavailable, and
    still filtered to zone_write. Handoff-mentioned paths outside git are excluded
    (lint_evidence_overreach fix).
    """
    vault_root = vault_root.resolve()
    repo_rel = repo_rel.strip("/").rstrip("/") + "/"
    repo = vault_root / repo_rel.strip("/")

    git_paths = collect_git_artifact_paths(repo)
    log_paths: set[str] = set()
    log_rel = agent_out.get("log_path")
    if log_rel:
        log_path = vault_root / str(log_rel)
        if log_path.is_file():
            log_paths = extract_paths_from_log_text(
                log_path.read_text(encoding="utf-8", errors="replace")
            )

    if zone_write:
        if git_paths:
            return filter_paths_to_zone_write(git_paths, zone_write)
        return filter_paths_to_zone_write(log_paths, zone_write)

    found = set(git_paths) | set(log_paths)
    return tuple(sorted(found))
