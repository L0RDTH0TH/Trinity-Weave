"""Phase 10g — conduct repair pack (proof-driven test surgery hand-off).

Uses Phase 11b Pull slice as base context; overlays failing proof stderr and nerve
conduct fields. Writes markdown packs for Task/host or operator chat.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .trinity_card_paths import load_trinity_card
from .trinity_prompt_context_slice import resolve_prompt_context

PACK_DIR_REL = ".technical/weave/conduct-repair-packs"

FORBIDDEN_CONDUCT_REPAIR = (
    "weaken_asserts_to_green",
    "import_only_without_behavior",
    "delete_tests_to_skip",
    "edit_outside_contract_proof_paths",
    "patch_card_yaml_in_this_task",
)


def _failed_proofs(proof_results: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in proof_results or []:
        if row.get("ok") is False:
            out.append(row)
    return out


def _proof_paths(card: dict[str, Any]) -> list[str]:
    contract = card.get("contract") or {}
    proof = contract.get("proof") or []
    if isinstance(proof, list):
        return [str(p).strip() for p in proof if str(p).strip()]
    return []


def build_conduct_repair_pack_markdown(
    vault_root: Path,
    trinity_id: str,
    *,
    card: dict[str, Any] | None = None,
    proof_results: list[dict[str, Any]] | None = None,
    nerve_row: dict[str, Any] | None = None,
    prefer: str = "provisional",
) -> str:
    """Cursor / Task hand-off for Tier-2 conduct failures on one card."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    loaded = card
    if loaded is None:
        loaded = load_trinity_card(vault_root, tid, prefer=prefer)

    bundle = resolve_prompt_context(vault_root, tid, "conduct_repair", prefer=prefer)
    failed = _failed_proofs(proof_results)
    proof_paths = _proof_paths(loaded)
    conduct = (nerve_row or {}).get("conduct") or {}
    tier = (nerve_row or {}).get("tier") or {}

    lines = [
        f"# Conduct repair pack — `{tid}`",
        "",
        "Fix **behavior proofs only** under `contract.proof` paths. "
        "Do **not** edit card YAML, Conceptual, Touch, or Rules in this task.",
        "",
        "## Write scope (11b Pull)",
        "",
        f"- **task_kind:** `conduct_repair`",
        f"- **write_scope:** `{bundle.write_scope}`",
        f"- **tier:** `{bundle.tier}`",
        f"- **meta_prepend:** {', '.join(f'`{m}`' for m in bundle.meta_prepend)}",
        "",
        "## Forbidden (hard stop)",
        "",
    ]
    for item in list(bundle.forbidden) + list(FORBIDDEN_CONDUCT_REPAIR):
        lines.append(f"- {item}")
    lines.append("")

    lines.extend(
        [
            "## Context legs (read-only — infer intent, do not cite in comments)",
            "",
            "```yaml",
            yaml.dump(bundle.legs, default_flow_style=False).strip(),
            "```",
            "",
            "## Proof paths (editable in this task)",
            "",
        ]
    )
    if proof_paths:
        for p in proof_paths:
            lines.append(f"- `{p}`")
    else:
        lines.append("- _(none listed on contract.proof — resolve from Touch primary_paths)_")
    lines.append("")

    if tier:
        lines.extend(
            [
                "## Nerve overlay (task context)",
                "",
                "```json",
                json.dumps(
                    {
                        "tier": {
                            k: tier.get(k)
                            for k in (
                                "shape_ok",
                                "spine_ok",
                                "semantic_ok",
                                "conduct_ok",
                                "conduct_skipped",
                            )
                            if k in tier
                        },
                        "conduct_disconnects": (conduct.get("disconnects") or [])[:8],
                    },
                    indent=2,
                ),
                "```",
                "",
            ]
        )

    lines.append("## Failing proofs")
    lines.append("")
    if not failed:
        lines.append("_No failing proof rows supplied — re-run `run_card_behavior_proofs` before repair._")
        lines.append("")
    else:
        for row in failed[:8]:
            name = row.get("test_name") or row.get("signal") or "unknown"
            detail = str(row.get("detail") or row.get("stderr") or "").strip()
            lines.append(f"### `{name}`")
            if detail:
                lines.append("```text")
                lines.append(detail[:4000])
                lines.append("```")
            lines.append("")

    lines.extend(
        [
            "## Repair doctrine",
            "",
            "- Align test assertions with **Conceptual outcome** and **contract.proof** intent.",
            "- Prefer **minimal** edits: fixtures, timeouts, env stubs, or assertion messages — not broad skips.",
            "- If proof references missing modules after regen, restore imports from Touch `primary_paths`.",
            "- Re-run: `PYTHONPATH=scripts python3 -m pytest <proof_path> -q` after each edit.",
            "",
            "## Self-check before you finish",
            "",
            "- [ ] Only files under `contract.proof` changed",
            "- [ ] No weakened asserts solely to green-wash",
            "- [ ] No card YAML edits",
            "- [ ] Failing proof names from above are addressed or explicitly documented as blocked",
            "",
            "## Output",
            "",
            "Patched test file(s) on disk; optional one-line summary of what changed per proof path.",
        ]
    )
    return "\n".join(lines)


def write_conduct_repair_pack(
    vault_root: Path,
    trinity_id: str,
    markdown: str,
    *,
    timestamp: str | None = None,
) -> Path:
    """Persist pack markdown under `.technical/weave/conduct-repair-packs/`."""
    vault_root = vault_root.resolve()
    tid = str(trinity_id).strip()
    ts = timestamp or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = vault_root / PACK_DIR_REL
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{tid}-{ts}.md"
    path.write_text(markdown, encoding="utf-8")
    return path
