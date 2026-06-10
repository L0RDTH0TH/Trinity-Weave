"""Post-MCP / post-engine-edit validation receipts → maintenance lane (Track C)."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_MAINTENANCE_RECEIPTS = Path(
    ".technical/parallel/maintenance/mcp-implementation-receipts.jsonl"
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def receipt_paths(vault_root: Path, lane: str) -> tuple[Path, Path]:
    vault_root = vault_root.resolve()
    primary = vault_root / DEFAULT_MAINTENANCE_RECEIPTS
    mirror = vault_root / ".technical" / "parallel" / lane / "mcp-validation-receipts.jsonl"
    return primary, mirror


def append_receipt(
    vault_root: Path,
    *,
    lane: str,
    project_id: str,
    engine_adapter: str,
    milestone_id: str,
    status: str,
    message: str,
    repo_root: str | None = None,
    debug_output: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Append one structured receipt to maintenance + lane mirror jsonl."""
    vault_root = vault_root.resolve()
    primary, mirror = receipt_paths(vault_root, lane)
    record: dict[str, Any] = {
        "record_type": "mcp_implementation_receipt",
        "receipt_id": f"mcp-{uuid.uuid4().hex[:12]}",
        "at": _now_iso(),
        "lane": lane,
        "project_id": project_id,
        "engine_adapter": engine_adapter,
        "milestone_id": milestone_id,
        "status": status,
        "message": message,
    }
    if repo_root:
        record["repo_root"] = repo_root
    if debug_output:
        record["debug_output"] = debug_output[:8000]
    if extra:
        record.update(extra)

    line = json.dumps(record, ensure_ascii=False) + "\n"
    for path in (primary, mirror):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            fh.write(line)

    return {
        "ok": True,
        "receipt_id": record["receipt_id"],
        "primary_path": str(primary.relative_to(vault_root)),
        "mirror_path": str(mirror.relative_to(vault_root)),
        "record": record,
    }


def run_mcp_postedit_validate(
    vault_root: Path,
    *,
    lane: str,
    project_id: str,
    engine_adapter: str,
    milestone_id: str,
    repo_root: str | None = None,
    status: str = "pass",
    message: str = "",
    debug_output: str | None = None,
    smoke: bool = False,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Harness entry — write receipt; optional M0 structural smoke checks."""
    vault_root = vault_root.resolve()
    checks: list[dict[str, str]] = []

    if smoke or milestone_id.upper() == "M0":
        repo = Path(repo_root or "5-Attachments/Code-Repos/genesis-mythos-demo")
        if not repo.is_absolute():
            repo = vault_root / repo
        pg = repo / "project.godot"
        csproj = repo / "GenesisMythosDemo.csproj"
        addon = repo / "addons" / "godot_mcp" / "plugin.cfg"
        for label, path in (
            ("project_godot", pg),
            ("csproj", csproj),
            ("mcp_plugin", addon),
        ):
            checks.append(
                {
                    "check": label,
                    "status": "pass" if path.is_file() else "fail",
                    "path": str(path.relative_to(vault_root)) if path.is_file() else str(path),
                }
            )
        failed = [c for c in checks if c["status"] != "pass"]
        if failed and status == "pass":
            status = "fail"
        if not message:
            message = (
                "M0 smoke structural checks pass"
                if not failed
                else f"M0 smoke failed: {[c['check'] for c in failed]}"
            )

    if not message:
        message = f"{milestone_id} mcp_postedit_validate receipt"

    out = append_receipt(
        vault_root,
        lane=lane,
        project_id=project_id,
        engine_adapter=engine_adapter,
        milestone_id=milestone_id,
        status=status,
        message=message,
        repo_root=repo_root,
        debug_output=debug_output,
        extra={"checks": checks, **(extra or {})} if checks or extra else extra,
    )
    out["checks"] = checks
    return out


def main() -> int:
    import argparse
    import sys

    p = argparse.ArgumentParser(description="Write MCP implementation validation receipt")
    p.add_argument("--vault-root", default=".")
    p.add_argument("--lane", required=True)
    p.add_argument("--project-id", required=True)
    p.add_argument("--engine-adapter", required=True)
    p.add_argument("--milestone-id", required=True)
    p.add_argument("--repo-root", default=None)
    p.add_argument("--status", default="pass", choices=["pass", "fail", "provisional"])
    p.add_argument("--message", default="")
    p.add_argument("--debug-output", default=None)
    p.add_argument("--smoke", action="store_true")
    args = p.parse_args()
    out = run_mcp_postedit_validate(
        Path(args.vault_root),
        lane=args.lane,
        project_id=args.project_id,
        engine_adapter=args.engine_adapter,
        milestone_id=args.milestone_id,
        repo_root=args.repo_root,
        status=args.status,
        message=args.message,
        debug_output=args.debug_output,
        smoke=args.smoke,
    )
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
