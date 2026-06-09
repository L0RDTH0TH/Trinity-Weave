"""Generate Grok-facing observability artifacts in Trinity-Weave export checkout."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WEAVE_CORE_VERSION = "2026.06.09-light"

KEY_HARNESS_COMMANDS: tuple[str, ...] = (
    "schedule_tick",
    "pseudo_clock_tick",
    "weave_public_sync",
    "trinity_weave_self_wrap",
    "trinity_touch_refresh",
    "trinity_lock_card",
    "trinity_type2_verify",
    "trinity_core_charter_audit",
    "trinity_catchup_sweep",
    "trinity_provisional_corps_sweep",
    "post_queue_gitforge",
    "post_queue_weave_publish",
)


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_card_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore[import-untyped]

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError, ImportError):
        return {}


def _summary_line(card: dict[str, Any]) -> str:
    conc = card.get("conceptual")
    if isinstance(conc, dict):
        for key in ("summary", "outcome", "primary_case"):
            val = conc.get(key)
            if isinstance(val, str) and val.strip():
                line = val.strip().split("\n", 1)[0]
                return line[:200]
    return ""


def build_card_index_rows(components_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not components_dir.is_dir():
        return rows
    for path in sorted(components_dir.glob("*.yaml")):
        if path.name.startswith("_"):
            continue
        card = _load_card_yaml(path)
        tid = str(card.get("id") or path.stem)
        meta = card.get("meta") if isinstance(card.get("meta"), dict) else {}
        rows.append(
            {
                "id": tid,
                "path": f"weave/components/{path.name}",
                "card_kind": str(meta.get("card_kind") or "component"),
                "lock_kind": str(meta.get("lock_kind") or ""),
                "summary": _summary_line(card),
            }
        )
    return rows


def render_card_index_md(rows: list[dict[str, Any]], *, generated_at: str) -> str:
    lines = [
        "# Trinity card index (auto-generated)",
        "",
        f"Generated: `{generated_at}` — do not hand-edit; regenerated on each `weave_public_sync`.",
        "",
        "| id | kind | lock | summary |",
        "|----|------|------|---------|",
    ]
    for row in rows:
        sid = row["id"].replace("|", "\\|")
        summary = str(row.get("summary") or "").replace("|", "\\|")[:120]
        lines.append(
            f"| `{sid}` | {row.get('card_kind', '')} | {row.get('lock_kind', '')} | {summary} |"
        )
    lines.extend(
        [
            "",
            "Full YAML: `weave/components/<id>.yaml`",
            "",
            "Grok: start at `GROK-START-HERE.md`.",
            "",
        ]
    )
    return "\n".join(lines)


def build_observability_payload(
    export_root: Path,
    *,
    fingerprint: str = "",
    commit_sha: str | None = None,
    vault_root: Path | None = None,
) -> dict[str, Any]:
    export_root = export_root.resolve()
    components_dir = export_root / "weave" / "components"
    rows = build_card_index_rows(components_dir)
    meta_ids = [r["id"] for r in rows if r.get("card_kind") == "meta"]
    component_ids = [r["id"] for r in rows if r.get("card_kind") != "meta"]

    return {
        "schema_version": 1,
        "repo": "Trinity-Weave",
        "remote": "https://github.com/L0RDTH0TH/Trinity-Weave",
        "branch": "main",
        "weave_core_version": WEAVE_CORE_VERSION,
        "last_publish_utc": _utc_iso(),
        "fingerprint": fingerprint,
        "last_commit": commit_sha,
        "grok_start_here": "GROK-START-HERE.md",
        "observability_doc": "Docs/GROK-OBSERVABILITY.md",
        "architecture_doc": "Docs/ARCHITECTURE-OVERVIEW.md",
        "glossary_doc": "Docs/GLOSSARY-FOR-EXTERNAL-READERS.md",
        "question_routing": {
            "weave_design": {"repo": "Trinity-Weave", "branch": "main"},
            "queue_automation": {
                "repo": "genesis-mythos-master-roadmap",
                "branch": "iteration-2-roadmap-rules",
            },
            "project_roadmap": {
                "repo": "genesis-mythos-master-roadmap",
                "branch": "godot-genesis-mythos-master",
            },
            "live_runtime": None,
        },
        "key_paths": {
            "cards": "weave/components/",
            "card_index": "weave/CARD-INDEX.md",
            "registry": "weave/trinity-partition-registry.yaml",
            "host_weld_safety": "weave/host-weld/live/safety.md",
            "harness_cli": "scripts/eat_queue_core/harness.py",
            "weave_python": "scripts/eat_queue_core/weave/",
            "constitution": "Docs/Maintenance-Trinity-Constitution.md",
            "manifest": "Docs/Weave-Core-Manifest.md",
        },
        "meta_card_ids": meta_ids,
        "component_card_ids": component_ids,
        "card_count": len(rows),
        "harness_commands_weave": list(KEY_HARNESS_COMMANDS),
        "not_in_repo": [
            "1-Projects/",
            "Roadmap/",
            "Ingest/",
            ".technical/parallel/",
            ".cursor/agents/",
            "live Watcher-Result",
        ],
        "publish_source": "private Second Brain vault (path not published)",
    }


def write_observability_artifacts(
    export_root: Path,
    vault_root: Path,
    *,
    fingerprint: str = "",
    commit_sha: str | None = None,
) -> dict[str, Any]:
    """Write OBSERVABILITY.json, weave/CARD-INDEX.md, copy GROK-START-HERE to root."""
    export_root = export_root.resolve()
    vault_root = vault_root.resolve()
    generated_at = _utc_iso()

    rows = build_card_index_rows(export_root / "weave" / "components")
    (export_root / "weave").mkdir(parents=True, exist_ok=True)
    index_path = export_root / "weave" / "CARD-INDEX.md"
    index_path.write_text(render_card_index_md(rows, generated_at=generated_at), encoding="utf-8")

    payload = build_observability_payload(
        export_root,
        fingerprint=fingerprint,
        commit_sha=commit_sha,
        vault_root=vault_root,
    )
    payload["card_index_path"] = "weave/CARD-INDEX.md"
    obs_path = export_root / "OBSERVABILITY.json"
    obs_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    grok_src = vault_root / "3-Resources/Second-Brain/Docs/GROK-START-HERE.md"
    if grok_src.is_file():
        text = grok_src.read_text(encoding="utf-8")
        # Strip YAML frontmatter for GitHub readability
        text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
        (export_root / "GROK-START-HERE.md").write_text(text.strip() + "\n", encoding="utf-8")

    return {
        "ok": True,
        "observability_json": obs_path.relative_to(export_root).as_posix(),
        "card_index": index_path.relative_to(export_root).as_posix(),
        "card_count": len(rows),
        "last_publish_utc": payload["last_publish_utc"],
    }
