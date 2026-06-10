"""Scoped Cursor agent handoff for one implementation milestone."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def build_implementation_handoff(
    vault_root: Path,
    *,
    lane: str,
    entry: dict[str, Any],
    charter: dict[str, Any],
    goal_packet: dict[str, Any] | None,
) -> str:
    vault_root = vault_root.resolve()
    params = entry.get("params") if isinstance(entry.get("params"), dict) else {}
    milestone_id = str(params.get("milestone_id") or charter.get("milestone_id") or "").upper()
    repo_rel = str(
        params.get("repo_path")
        or (goal_packet or {}).get("planner_hints", {}).get("repo_path")
        or "5-Attachments/Code-Repos/genesis-mythos-demo/"
    ).rstrip("/")
    repo_abs = vault_root / repo_rel
    spec_ref = str(
        params.get("demo_spec_ref")
        or (goal_packet or {}).get("planner_hints", {}).get("demo_spec_ref")
        or "1-Projects/godot-genesis-mythos-master/Horizon-Q3-Demo-Spec.md"
    )
    guidance = str(params.get("user_guidance") or charter.get("done_when") or "")
    targets = charter.get("target_files") or []
    target_block = "\n".join(f"- `{repo_rel}/{t}`" for t in targets) if targets else "- (see demo spec scenes)"

    return (
        f"You are the **Implementation Factory** agent for Track C (Horizon-Q3 Demo v1).\n\n"
        f"Vault root: `{vault_root}`\n"
        f"Lane: `{lane}`\n"
        f"Milestone: **{milestone_id}** (`IMPLEMENT_SLICE`)\n"
        f"Repo (edit in-vault): `{repo_rel}/`\n"
        f"Demo spec: `{spec_ref}`\n\n"
        f"## Objective\n{guidance}\n\n"
        f"## Acceptance ({milestone_id})\n{charter.get('done_when', '')}\n\n"
        f"## Target artifacts\n{target_block}\n\n"
        f"## Constraints\n"
        f"- Godot **4.6.3 .NET**, C# primary, Linux\n"
        f"- Edit files under `{repo_rel}/` only for engine work\n"
        f"- Do **not** run RESUME_ROADMAP, roadmap deepen, or sandbox lane work\n"
        f"- Do **not** edit `.cursor/rules/**`\n"
        f"- When done: ensure `dotnet build` passes in `{repo_rel}/`\n"
        f"- Append a one-line receipt stub to "
        f"`1-Projects/godot-genesis-mythos-master/GMM-Godot-Prototype-History.md` "
        f"under a `## {milestone_id} harness receipt` heading\n\n"
        f"## Finish\n"
        f"Implement **only** {milestone_id}. Do not start later milestones. "
        f"Report files created/changed and build result."
    )
