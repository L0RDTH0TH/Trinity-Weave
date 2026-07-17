"""UserStory-Brief — operator handoff after beat generation (mirrors playtest_brief)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..factory.factory_output_gate import parse_factory_orchestrator_yaml
from .catalog_io import catalog_rows_by_id, load_json, load_yaml, user_story_paths
from .user_story_feedback import list_pending_user_story_confirmations, sync_feedback_from_budget


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def brief_dir(vault_root: Path, project_id: str) -> Path:
    cfg = parse_factory_orchestrator_yaml(vault_root / "3-Resources/Second-Brain-Config.md")
    rf = cfg.get("roadmap_factory") if isinstance(cfg.get("roadmap_factory"), dict) else {}
    rel = str(
        rf.get("brief_dir_rel")
        or f"1-Projects/{project_id}/Factory-DRB/operator-feedback/user-story-briefs"
    )
    if not rel.startswith("1-Projects/"):
        rel = f"1-Projects/{project_id}/{rel.lstrip('/')}"
    return vault_root / rel


@dataclass(frozen=True)
class UserStoryBriefResult:
    ok: bool
    path: str
    rollout_version: int
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "path": self.path,
            "rollout_version": self.rollout_version,
            "detail": self.detail,
        }


def write_user_story_brief(
    vault_root: Path,
    *,
    project_id: str,
) -> UserStoryBriefResult:
    """Emit operator brief listing rollout rows, beats, and confirm shortcuts."""
    vault_root = vault_root.resolve()
    paths = user_story_paths(vault_root, project_id)
    budget = load_json(paths["budget"])
    catalog = load_yaml(paths["catalog"])
    catalog_by_id = catalog_rows_by_id(catalog)
    rv = int(budget.get("rollout_version") or 1)

    sync_feedback_from_budget(vault_root, project_id)
    pending = list_pending_user_story_confirmations(vault_root, project_id)

    lines = [
        "---",
        f"brief_type: user_story",
        f"project_id: {project_id}",
        f"rollout_version: {rv}",
        f"generated_at: {datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')}",
        "---",
        "",
        f"# User Story Brief — rollout {rv}",
        "",
        "## Operator rhythm (mirror playtest)",
        "",
        "1. Read each row's beat **Experiential narrative**",
        "2. Mark pass/fail per row (CLI below)",
        "3. Run `./scripts/run-operator-user-story-session.sh` to ingest + list pending",
        "4. When all rows confirmed → factory stages via `ROADMAP_FACTORY_STAGE_FACTORY`",
        "",
        "## Active rollout rows",
        "",
    ]

    for br in budget.get("rows") or []:
        if not isinstance(br, dict):
            continue
        row_id = str(br.get("row_id") or "")
        cat = catalog_by_id.get(row_id) or {}
        lines.append(
            f"### `{row_id}` — target depth {br.get('target_depth')} "
            f"(current {br.get('current_depth', 0)})"
        )
        lines.append(f"- **Label:** {cat.get('label') or row_id}")
        lines.append(f"- **Dimension:** {cat.get('dimension') or 'general'}")
        pins = cat.get("execution_pins") or []
        if pins:
            lines.append(f"- **Execution pin:** `{pins[0]}`")
        beat_ref = cat.get("beat_ref") or ""
        if beat_ref:
            lines.append(f"- **Beat:** [[{beat_ref}]]")
        lines.append("")

    lines.extend(
        [
            "## Confirm commands",
            "",
            "```bash",
            "# Catalog sign-off (once per rollout)",
            "PYTHONPATH=scripts python3 -m eat_queue_core.weave.user_story.cli operator-user-story-confirm \\",
            f"  --vault-root . --project-id {project_id} --catalog-sign",
            "",
            "# Per-row experiential pass",
            "PYTHONPATH=scripts python3 -m eat_queue_core.weave.user_story.cli operator-user-story-confirm \\",
            f"  --vault-root . --project-id {project_id} --row-id <row_id> --pass true --confirm",
            "```",
            "",
            f"## Pending confirmations ({len(pending)})",
            "",
        ]
    )
    if pending:
        for p in pending:
            lines.append(f"- `{p['row_id']}` pass={p.get('experiential_pass')} confirmed={p.get('operator_confirmed')}")
    else:
        lines.append("- (none — ready for factory stage)")

    out_dir = brief_dir(vault_root, project_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = _utc_stamp()
    out_path = out_dir / f"user-story-brief-r{rv}-{stamp}.md"
    latest = out_dir / "latest.md"
    body = "\n".join(lines) + "\n"
    out_path.write_text(body, encoding="utf-8")
    latest.write_text(body, encoding="utf-8")

    return UserStoryBriefResult(
        ok=True,
        path=str(out_path.relative_to(vault_root)),
        rollout_version=rv,
        detail="user_story_brief_written",
    )
