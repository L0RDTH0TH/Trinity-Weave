"""One implementation milestone — vault doc, agent loop, verify, receipt."""

from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..agent_cli import find_agent_cli
from ..goal_authority_io import goal_authority_path_for_lane, load_goal_authority
from ..pseudo_clock import load_knobs
from .engine_preflight import resolve_godot_binary, run_engine_preflight
from .implementation_handoff import build_implementation_handoff
from .mcp_postedit_validate import run_mcp_postedit_validate
from .milestone_charter import get_milestone_spec, next_milestone_id


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _repo_commit(repo: Path) -> str:
    if not (repo / ".git").is_dir():
        return "vault-local"
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=repo,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if r.returncode == 0:
            return r.stdout.strip()
    except (subprocess.TimeoutExpired, OSError):
        pass
    return "unknown"


def advance_goal_milestone(vault_root: Path, lane: str, completed_id: str) -> dict[str, Any]:
    path = goal_authority_path_for_lane(vault_root, lane)
    if not path.is_file():
        return {"ok": False, "reason": "no_goal_authority"}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"ok": False, "reason": "goal_authority_read_failed"}
    hints = data.setdefault("planner_hints", {})
    nxt = next_milestone_id(completed_id)
    if completed_id.upper() == "M0":
        hints["m0_status"] = "complete"
    if nxt:
        hints["current_milestone"] = nxt
    else:
        hints["current_milestone"] = completed_id.upper()
        hints["implementation_complete"] = True
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"ok": True, "completed": completed_id.upper(), "next_milestone": nxt}


def run_milestone_verify(
    vault_root: Path,
    repo_rel: str,
    charter: dict[str, Any],
    *,
    godot_binary: str | None = None,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    repo = vault_root / repo_rel.strip("/")
    checks: list[dict[str, Any]] = []
    for step in charter.get("verify") or []:
        step_s = str(step)
        if step_s == "dotnet_build":
            dotnet = os.environ.get("DOTNET_ROOT", str(Path.home() / ".dotnet"))
            dotnet_bin = Path(dotnet) / "dotnet" if Path(dotnet).is_dir() else "dotnet"
            try:
                r = subprocess.run(
                    [str(dotnet_bin), "build", str(repo / "GenesisMythosDemo.csproj")],
                    cwd=repo,
                    capture_output=True,
                    text=True,
                    timeout=180,
                )
                checks.append(
                    {
                        "check": "dotnet_build",
                        "status": "pass" if r.returncode == 0 else "fail",
                        "exit_code": r.returncode,
                    }
                )
            except (subprocess.TimeoutExpired, OSError) as e:
                checks.append({"check": "dotnet_build", "status": "fail", "error": str(e)})
        elif step_s.startswith("file_exists:"):
            rel = step_s.split(":", 1)[1]
            fp = repo / rel
            checks.append(
                {
                    "check": f"file_exists:{rel}",
                    "status": "pass" if fp.is_file() else "fail",
                    "path": str(fp),
                }
            )
        elif step_s == "godot_headless_smoke":
            godot = godot_binary or resolve_godot_binary()
            if not godot:
                checks.append({"check": "godot_headless_smoke", "status": "warn", "detail": "no godot"})
            else:
                try:
                    r = subprocess.run(
                        [godot, "--headless", "--path", str(repo), "--quit-after", "1"],
                        capture_output=True,
                        text=True,
                        timeout=120,
                    )
                    checks.append(
                        {
                            "check": "godot_headless_smoke",
                            "status": "pass" if r.returncode == 0 else "fail",
                            "exit_code": r.returncode,
                        }
                    )
                except (subprocess.TimeoutExpired, OSError) as e:
                    checks.append({"check": "godot_headless_smoke", "status": "fail", "error": str(e)})

    failed = [c for c in checks if c.get("status") == "fail"]
    return {"ok": len(failed) == 0, "checks": checks}


def run_m1_vault_doc(
    vault_root: Path,
    *,
    repo_rel: str,
    spec_ref: str,
    history_ref: str = "1-Projects/godot-genesis-mythos-master/GMM-Godot-Prototype-History.md",
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    repo = vault_root / repo_rel.strip("/")
    spec_path = vault_root / spec_ref
    history_path = vault_root / history_ref
    commit = _repo_commit(repo)
    repo_display = repo_rel.strip("/")

    if spec_path.is_file():
        text = spec_path.read_text(encoding="utf-8")
        new_row = (
            f"| **M1** | Repo link | Authoritative stub `{repo_display}/` "
            f"(vault-local; commit `{commit}` at receipt time) |"
        )
        text = re.sub(
            r"\| \*\*M1\*\* \| Repo link \|[^\n]+\|",
            new_row,
            text,
            count=1,
        )
        spec_path.write_text(text, encoding="utf-8")

    stamp = _utc_iso()
    receipt = (
        f"\n## M1 harness receipt — {stamp}\n\n"
        f"| Field | Value |\n|-------|-------|\n"
        f"| **Repo** | `{repo_display}/` |\n"
        f"| **Commit** | `{commit}` |\n"
        f"| **Dispatch** | `IMPLEMENT_SLICE` vault_doc |\n"
    )
    if history_path.is_file():
        hist = history_path.read_text(encoding="utf-8")
        if "## M1 harness receipt" not in hist:
            history_path.write_text(hist.rstrip() + "\n" + receipt + "\n", encoding="utf-8")

    return {
        "ok": True,
        "milestone_id": "M1",
        "kind": "vault_doc",
        "repo": repo_display,
        "commit": commit,
    }


def run_implementation_agent(
    vault_root: Path,
    handoff: str,
    *,
    dry_run: bool = False,
    timeout: int = 3600,
    log_path: Path | None = None,
) -> dict[str, Any]:
    cli = find_agent_cli()
    if not cli:
        return {"ok": False, "error": "cursor_or_agent_cli_not_found"}
    if dry_run:
        return {"ok": True, "dry_run": True, "handoff_preview": handoff[:600]}

    knobs = load_knobs(vault_root)
    model = str(knobs.get("headless_agent_model") or "auto").strip()
    cmd = [*cli, "-p", "--force", "--model", model, handoff]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(vault_root / "scripts")

    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("w", encoding="utf-8") as logf:
            logf.write(f"# implement_slice agent\n# cmd: {' '.join(cmd)}\n\n")
            r = subprocess.run(
                cmd,
                cwd=vault_root,
                stdout=logf,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=timeout,
                env=env,
            )
    else:
        r = subprocess.run(
            cmd,
            cwd=vault_root,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )

    return {
        "ok": r.returncode == 0,
        "exit_code": r.returncode,
        "log_path": str(log_path.relative_to(vault_root)) if log_path else None,
    }


def run_implement_slice(
    vault_root: Path,
    lane: str,
    entry: dict[str, Any],
    *,
    dry_run: bool = False,
    parent_run_id: str | None = None,
    skip_agent: bool = False,
    skip_preflight: bool = False,
) -> dict[str, Any]:
    """Execute one IMPLEMENT_SLICE for an implementation_milestone queue entry."""
    vault_root = vault_root.resolve()
    lane = lane.strip().lower()
    eid = str(entry.get("id") or "")
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    milestone_id = str(params.get("milestone_id") or "").upper()
    project_id = str(entry.get("project_id") or params.get("project_id") or "godot-genesis-mythos-master")
    engine_adapter = str(params.get("engine_adapter") or "godot_4_6_3_dotnet")
    repo_rel = str(params.get("repo_path") or "5-Attachments/Code-Repos/genesis-mythos-demo/").rstrip("/") + "/"

    packet = load_goal_authority(vault_root, lane, require_confirmed=False)
    hints = (packet or {}).get("planner_hints") or {}
    current = str(hints.get("current_milestone") or "M1").upper()
    if milestone_id and milestone_id != current:
        return {
            "ok": False,
            "id": eid,
            "error": "milestone_out_of_order",
            "expected": current,
            "got": milestone_id,
            "segment": "IMPLEMENT_SLICE",
        }

    charter = get_milestone_spec(vault_root, lane, milestone_id)
    if not charter:
        return {"ok": False, "id": eid, "error": "unknown_milestone", "milestone_id": milestone_id}

    kind = str(charter.get("kind") or "repo_build")
    requires_mcp = bool(charter.get("requires_mcp"))
    requires_agent = bool(charter.get("requires_agent"))

    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "id": eid,
            "milestone_id": milestone_id,
            "kind": kind,
            "segment": "IMPLEMENT_SLICE",
            "would_run_agent": requires_agent and kind != "vault_doc",
        }

    preflight: dict[str, Any] | None = None
    if kind != "vault_doc" and not skip_preflight:
        preflight = run_engine_preflight(
            vault_root,
            repo_rel,
            requires_mcp=requires_mcp,
            run_dotnet_build=True,
        )
        if not preflight.get("ok"):
            return {
                "ok": False,
                "id": eid,
                "milestone_id": milestone_id,
                "error": "engine_preflight_failed",
                "preflight": preflight,
                "segment": "IMPLEMENT_SLICE",
            }

    slice_out: dict[str, Any]
    if kind == "vault_doc":
        slice_out = run_m1_vault_doc(
            vault_root,
            repo_rel=repo_rel,
            spec_ref=str(params.get("demo_spec_ref") or hints.get("demo_spec_ref") or ""),
            history_ref=str(
                hints.get("prototype_history_ref")
                or "1-Projects/godot-genesis-mythos-master/GMM-Godot-Prototype-History.md"
            ),
        )
    else:
        handoff = build_implementation_handoff(
            vault_root,
            lane=lane,
            entry=entry,
            charter=charter,
            goal_packet=packet,
        )
        agent_out: dict[str, Any] = {"ok": True, "skipped": True}
        if requires_agent and not skip_agent:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            log_path = (
                vault_root
                / ".technical"
                / "Run-Telemetry"
                / lane
                / f"implement-slice-{milestone_id.lower()}-{stamp}.log"
            )
            agent_out = run_implementation_agent(
                vault_root, handoff, dry_run=False, log_path=log_path
            )
        if not agent_out.get("ok"):
            return {
                "ok": False,
                "id": eid,
                "milestone_id": milestone_id,
                "error": "agent_run_failed",
                "agent": agent_out,
                "segment": "IMPLEMENT_SLICE",
            }
        verify = run_milestone_verify(
            vault_root,
            repo_rel,
            charter,
            godot_binary=(preflight or {}).get("godot_binary"),
        )
        if not verify.get("ok"):
            return {
                "ok": False,
                "id": eid,
                "milestone_id": milestone_id,
                "error": "milestone_verify_failed",
                "verify": verify,
                "agent": agent_out,
                "segment": "IMPLEMENT_SLICE",
            }
        slice_out = {"ok": True, "agent": agent_out, "verify": verify}

    if not slice_out.get("ok"):
        return {**slice_out, "id": eid, "segment": "IMPLEMENT_SLICE"}

    receipt = run_mcp_postedit_validate(
        vault_root,
        lane=lane,
        project_id=project_id,
        engine_adapter=engine_adapter,
        milestone_id=milestone_id,
        repo_root=repo_rel.rstrip("/"),
        status="pass",
        message=f"{milestone_id} IMPLEMENT_SLICE complete",
        smoke=milestone_id == "M0",
        extra={
            "dispatch": "IMPLEMENT_SLICE",
            "parent_run_id": parent_run_id,
            "entry_id": eid,
        },
    )

    advance = advance_goal_milestone(vault_root, lane, milestone_id)

    return {
        "ok": True,
        "id": eid,
        "milestone_id": milestone_id,
        "kind": kind,
        "segment": "IMPLEMENT_SLICE",
        "slice": slice_out,
        "receipt": receipt,
        "advance": advance,
        "preflight": preflight,
        "message": f"IMPLEMENT_SLICE {milestone_id} complete → next {advance.get('next_milestone')}",
    }
