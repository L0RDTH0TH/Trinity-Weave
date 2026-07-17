"""Navigation hygiene for roadmap trees after path organize — Dataview scopes, minor fixes."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

_DATAVIEW_FROM_RE = re.compile(
    r'(```dataview\s*\nTABLE WITHOUT ID[^\n]*\nFROM )"([^"]+)"',
    re.IGNORECASE,
)
_TERTIARY_SECTION_RE = re.compile(
    r"## (Tertiary notes|Child notes)\s*\n\n```dataview",
    re.IGNORECASE,
)


def _read_fm(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    fm = yaml.safe_load(text[4:end]) or {}
    return fm if isinstance(fm, dict) else {}


def _is_secondary_roadmap(path: Path, fm: dict[str, Any]) -> bool:
    level = str(fm.get("roadmap-level") or "").lower()
    if level == "secondary":
        return True
    idx = str(fm.get("subphase-index") or "")
    return bool(re.fullmatch(r"\d+\.\d+", idx.strip().strip('"')))


def clean_roadmap_navigation(
    vault_root: Path,
    project_id: str,
    *,
    dry_run: bool = True,
) -> dict[str, Any]:
    """Fix secondary Dataview FROM scopes to own folder; add tertiary section when missing."""
    vault_root = vault_root.resolve()
    road = vault_root / "1-Projects" / project_id / "Roadmap"
    if not road.is_dir():
        return {"ok": False, "error": "roadmap_missing"}

    updated: list[str] = []

    for path in sorted(road.rglob("*.md")):
        rel = str(path.relative_to(vault_root)).replace("\\", "/")
        if any(x in rel for x in ("/Conceptual-Decision-Records/", "/User-Story/", "/Execution/")):
            continue
        if path.name in {"workflow_state.md", "roadmap-state.md", "distilled-core.md", "decisions-log.md"}:
            continue
        if "MOC" in path.name:
            continue

        fm = _read_fm(path)
        if not _is_secondary_roadmap(path, fm):
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        sec_folder_rel = str(path.parent.relative_to(vault_root)).replace("\\", "/")
        new_text = text

        if _TERTIARY_SECTION_RE.search(text):
            if f'FROM "{sec_folder_rel}"' not in text:

                def _repl(m: re.Match[str]) -> str:
                    return f'{m.group(1)}"{sec_folder_rel}"'

                new_text = _DATAVIEW_FROM_RE.sub(_repl, text, count=1)
        elif "## Tertiary notes" not in text and "## Child notes" not in text:
            block = (
                "\n## Tertiary notes\n\n"
                "```dataview\n"
                'TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", '
                'subphase-index AS "Index", status, progress AS "%"\n'
                f'FROM "{sec_folder_rel}"\n'
                'WHERE roadmap-level = "tertiary" OR roadmap-level = "task"\n'
                "SORT subphase-index ASC, file.name ASC\n"
                "```\n"
            )
            new_text = text.rstrip() + "\n" + block

        if new_text != text:
            updated.append(rel)
            if not dry_run:
                path.write_text(new_text, encoding="utf-8")

    dc = road / "distilled-core.md"
    if dc.is_file():
        text = dc.read_text(encoding="utf-8")
        fixed = re.sub(r"(tertiaries\.\n)(## Dependency)", r"\1\n\2", text)
        if fixed != text:
            updated.append(str(dc.relative_to(vault_root)))
            if not dry_run:
                dc.write_text(fixed, encoding="utf-8")

    return {
        "ok": True,
        "project_id": project_id,
        "dry_run": dry_run,
        "updated_count": len(updated),
        "updated": updated,
    }
