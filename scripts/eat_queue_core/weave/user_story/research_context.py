"""Read-only research context pack for product-factory RESUME (Half A)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ...research_consumption import read_pending_injection
from .catalog_io import user_story_paths
from .catalog_mint_propose import _find_pmg_path

_WIKI = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


def _influence_deck_path(vault_root: Path, project_id: str) -> Path:
    return user_story_paths(vault_root, project_id)["influence"]


def _touchstone_snippets(vault_root: Path, pmg_text: str, *, max_chars: int = 1200) -> list[dict[str, str]]:
    snippets: list[dict[str, str]] = []
    for m in _WIKI.finditer(pmg_text):
        ref = m.group(1).strip()
        if ref.startswith("http"):
            continue
        p = vault_root / ref
        if not p.is_file() and not (vault_root / f"{ref}.md").is_file():
            p = vault_root / f"{ref}.md"
        if not p.is_file():
            continue
        body = p.read_text(encoding="utf-8", errors="replace")[:max_chars]
        snippets.append({"path": str(p.relative_to(vault_root)), "excerpt": body.strip()})
    return snippets


def _scoped_resources_section(pmg_text: str) -> str:
    if "## Scoped Resources" not in pmg_text:
        return ""
    idx = pmg_text.find("## Scoped Resources")
    rest = pmg_text[idx:]
    nxt = rest.find("\n## ", 4)
    return rest[:nxt] if nxt > 0 else rest


def build_research_context(vault_root: Path, *, project_id: str) -> dict[str, Any]:
    """Thin wrapper: influence deck, PMG scoped resources, pending workflow injection."""
    vault_root = vault_root.resolve()
    pmg = _find_pmg_path(vault_root, project_id)
    pmg_text = pmg.read_text(encoding="utf-8", errors="replace") if pmg and pmg.is_file() else ""

    wf_path = vault_root / f"1-Projects/{project_id}/workflow_state.md"
    pending = read_pending_injection(wf_path)

    deck = _influence_deck_path(vault_root, project_id)
    deck_text = deck.read_text(encoding="utf-8", errors="replace") if deck.is_file() else ""

    return {
        "influence_deck_path": str(deck.relative_to(vault_root)) if deck.is_file() else "",
        "influence_deck_chars": len(deck_text.strip()),
        "scoped_resources_markdown": _scoped_resources_section(pmg_text),
        "touchstone_snippets": _touchstone_snippets(vault_root, pmg_text),
        "injected_research_paths": list(pending.get("paths") or []),
        "injected_research_summary": str(pending.get("summary") or ""),
    }


def influence_deck_needs_research(vault_root: Path, *, project_id: str, min_chars: int = 200) -> bool:
    deck = _influence_deck_path(vault_root, project_id)
    if not deck.is_file():
        return True
    return len(deck.read_text(encoding="utf-8", errors="replace").strip()) < min_chars


def format_research_context_block(ctx: dict[str, Any]) -> str:
    lines = ["## Research context (read-only)", ""]
    if ctx.get("scoped_resources_markdown"):
        lines.append(str(ctx["scoped_resources_markdown"]))
        lines.append("")
    paths = ctx.get("injected_research_paths") or []
    if paths:
        lines.append("### Pending injected research")
        for p in paths:
            lines.append(f"- [[{p}]]")
        lines.append("")
    snippets = ctx.get("touchstone_snippets") or []
    if snippets:
        lines.append("### Touchstone excerpts")
        for s in snippets[:5]:
            lines.append(f"- `{s.get('path')}`")
        lines.append("")
    return "\n".join(lines).strip() + "\n"
