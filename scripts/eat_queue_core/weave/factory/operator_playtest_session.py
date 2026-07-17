"""Post-F6 operator session — ingest capture + optional surface check (not overnight)."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .factory_output_gate import parse_factory_orchestrator_yaml
from .operator_confirm import list_pending_confirmations
from .playtest_brief import BRIEF_DIR_REL
from .playtest_session_ingest import ingest_playtest_session
from .surface_pass import run_surface_pass

MANIFEST_REL = "1-Projects/godot-genesis-mythos-master/Factory-DRB/Tech-Stack-Manifest-v1.yaml"


@dataclass(frozen=True)
class OperatorPlaytestSessionResult:
    ok: bool
    ingest: dict[str, Any]
    pending: list[dict[str, Any]]
    surface_ok: bool | None
    latest_brief: str | None
    detail: str
    lifecycle: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        out = {
            "ok": self.ok,
            "ingest": self.ingest,
            "pending": self.pending,
            "surface_ok": self.surface_ok,
            "latest_brief": self.latest_brief,
            "detail": self.detail,
        }
        if self.lifecycle is not None:
            out["lifecycle"] = self.lifecycle
        return out


def _config_path(vault_root: Path) -> Path:
    from ...config_loader import resolve_config_path

    return resolve_config_path(vault_root, None)


def _feedback_rel(vault_root: Path) -> str:
    raw = parse_factory_orchestrator_yaml(_config_path(vault_root))
    return str(raw.get("operator_feedback_path") or "").strip() or (
        "1-Projects/godot-genesis-mythos-master/Factory-DRB/operator-feedback/"
        "godot-closed-alpha-kinesthetic.yaml"
    )


def run_operator_playtest_session(
    vault_root: Path,
    *,
    session_path: Path | None = None,
    run_surface_pass: bool = False,
    write_feedback: bool = True,
) -> OperatorPlaytestSessionResult:
    """
    Operator-session hook after F6 playtest — ingest only, never an overnight gate.

    Call manually or from scripts/run-operator-playtest-session.sh after human playtest.
    """
    vault_root = vault_root.resolve()
    feedback_rel = _feedback_rel(vault_root)

    ingest = ingest_playtest_session(
        vault_root,
        session_path=session_path,
        write_feedback=write_feedback,
        feedback_rel=feedback_rel,
    )
    ingest_dict = ingest.to_dict()

    pending = list_pending_confirmations(vault_root, feedback_rel=feedback_rel)

    lifecycle: dict[str, Any] | None = None
    if write_feedback and ingest.ok and not pending:
        from ...goal_authority_io import load_goal_authority
        from .operator_playtest_lifecycle import record_playtest_pass

        packet = load_goal_authority(vault_root, "godot", require_confirmed=False) or {}
        pid = str(packet.get("project_id") or "godot-genesis-mythos-master")
        lifecycle = record_playtest_pass(
            vault_root,
            pid,
            "godot",
            notes="operator_playtest_session_all_confirmed",
        )
    elif write_feedback and ingest.ok and pending:
        lifecycle = {
            "skipped": True,
            "reason": "feedback_still_pending",
            "pending_count": len(pending),
        }

    surface_ok: bool | None = None
    if run_surface_pass:
        surface_ok = run_surface_pass(vault_root, run_probes=False).ok

    brief_path = vault_root / BRIEF_DIR_REL / "latest.md"
    latest_brief = str(brief_path.relative_to(vault_root)) if brief_path.is_file() else None

    ok = ingest.ok or ingest.detail == "no_playtest_session"
    detail = "operator_playtest_session_complete"
    if ingest.detail == "no_playtest_session":
        detail = "no_session_run_f6_first"

    return OperatorPlaytestSessionResult(
        ok=ok,
        ingest=ingest_dict,
        pending=pending,
        surface_ok=surface_ok,
        latest_brief=latest_brief,
        detail=detail,
        lifecycle=lifecycle,
    )


def run_f6_capture_subprocess(vault_root: Path, *, godot_bin: str | None = None) -> dict[str, Any]:
    """Optional helper — launch game repo run-f6-playtest.sh (blocking, operator terminal)."""
    vault_root = vault_root.resolve()
    manifest = vault_root / MANIFEST_REL
    rel = "5-Attachments/Code-Repos/genesis-mythos-alpha"
    if manifest.is_file():
        data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        if isinstance(data, dict) and data.get("game_repo_path"):
            rel = str(data["game_repo_path"]).strip("/")

    script = vault_root / rel / "scripts/run-f6-playtest.sh"
    if not script.is_file():
        return {"ok": False, "error": "missing_run_f6_script", "path": str(script)}

    env = None
    if godot_bin:
        import os

        env = os.environ.copy()
        env["GODOT"] = godot_bin

    try:
        proc = subprocess.run(
            [str(script)],
            cwd=script.parent.parent,
            capture_output=True,
            text=True,
            timeout=3600,
            env=env,
        )
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout[-2000:] if proc.stdout else "",
            "stderr": proc.stderr[-2000:] if proc.stderr else "",
        }
    except (subprocess.TimeoutExpired, OSError) as e:
        return {"ok": False, "error": str(e)}
