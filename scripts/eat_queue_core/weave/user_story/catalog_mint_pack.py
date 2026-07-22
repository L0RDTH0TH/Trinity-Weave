"""Emit per-project catalog-mint packs onto main-visible Docs/catalog-mint/<project_id>/."""

from __future__ import annotations

import hashlib
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .catalog_io import project_root, user_story_paths

PACK_DOCS_REL = Path("3-Resources/Second-Brain/Docs/catalog-mint")
SHARED_REL = PACK_DOCS_REL / "_shared"
REQUIRED_FILES = (
    "MINT-PACK.md",
    "PACK-MANIFEST.yaml",
    "CONCEPTUAL-EXCERPT.md",
    "PIN-INDEX.md",
    "ROADMAP-RESOURCE-INDEX.yaml",
    "Tech-Stack-Excerpt.yaml",
    "Stack-Domain-Registry-Excerpt.yaml",
    "slice-catalog.yaml",
)

_ALLOWED_STACK_STATUS = frozenset({"locked", "trialing", "integrated"})
_WIKI_LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


@dataclass(frozen=True)
class CatalogMintPackResult:
    ok: bool
    project_id: str
    pack_dir: str
    synced_at: str
    missing: tuple[str, ...]
    warnings: tuple[str, ...]
    file_hashes: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "project_id": self.project_id,
            "pack_dir": self.pack_dir,
            "synced_at": self.synced_at,
            "missing": list(self.missing),
            "warnings": list(self.warnings),
            "file_hashes": dict(self.file_hashes),
        }


def pack_dir_for(vault_root: Path, project_id: str) -> Path:
    return vault_root / PACK_DOCS_REL / project_id


def active_path(vault_root: Path) -> Path:
    return vault_root / PACK_DOCS_REL / "ACTIVE.md"


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _dump_yaml(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def _find_pmg(vault_root: Path, project_id: str) -> Path | None:
    base = project_root(vault_root, project_id)
    if not base.is_dir():
        return None
    for p in sorted(base.glob("*Master*Goal*")):
        if p.is_file() and p.suffix.lower() in {".md", ""}:
            return p
    for p in sorted(base.glob("*master*goal*.md")):
        if p.is_file():
            return p
    for p in sorted(base.glob("*-goal.md")):
        if p.is_file():
            return p
    return None


def _excerpt_pmg(pmg: Path, *, max_chars: int = 6000) -> str:
    text = pmg.read_text(encoding="utf-8")
    # strip frontmatter
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4 :].lstrip("\n")
    if len(text) > max_chars:
        text = text[:max_chars].rstrip() + "\n\n…\n"
    return (
        f"# Conceptual / PMG excerpt (feedstock)\n\n"
        f"_Source: `{pmg.as_posix()}`_\n\n"
        f"{text}"
    )


def _collect_pin_titles(vault_root: Path, project_id: str) -> list[str]:
    roadmap = project_root(vault_root, project_id) / "Roadmap"
    titles: list[str] = []
    if not roadmap.is_dir():
        return titles
    for p in sorted(roadmap.rglob("*.md")):
        name = p.stem
        if "Roadmap" in name or name.startswith("Phase-"):
            titles.append(name)
    # Prefer Conceptual-Decision-Records and phase notes
    return sorted(set(titles))


def _write_pin_index(titles: list[str], project_id: str) -> str:
    lines = [
        f"# {project_id} catalog mint — live conceptual_pin titles",
        "",
        "Use ONLY these wiki-link titles (or say `needs pin`). Do not invent names.",
        "",
        f"_Count: {len(titles)}_",
        "",
    ]
    for t in titles:
        lines.append(f"- `[[{t}]]`")
    lines.append("")
    return "\n".join(lines)


def _stack_excerpts(vault_root: Path, project_id: str) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    warnings: list[str] = []
    base = project_root(vault_root, project_id)
    manifest_path = base / "Factory-DRB" / "Tech-Stack-Manifest-v1.yaml"
    registry_path = base / "Factory-DRB" / "Stack-Domain-Registry-v1.yaml"
    manifest = _load_yaml(manifest_path)
    registry = _load_yaml(registry_path)
    if not manifest:
        warnings.append("tech_stack_manifest_missing")
    if not registry:
        warnings.append("stack_domain_registry_missing")

    rows_out: list[dict[str, Any]] = []
    for row in manifest.get("rows") or []:
        if not isinstance(row, dict):
            continue
        status = str(row.get("status") or "").lower()
        kind = str(row.get("row_kind") or "").lower()
        if status not in _ALLOWED_STACK_STATUS and kind not in _ALLOWED_STACK_STATUS:
            continue
        rows_out.append(
            {
                "id": row.get("id"),
                "stack_domain_id": row.get("stack_domain_id"),
                "status": row.get("status"),
                "row_kind": row.get("row_kind"),
                "wrap_policy": row.get("wrap_policy"),
                "vendor_or_source": row.get("vendor_or_source"),
                "notes": row.get("notes"),
            }
        )

    domains_out: list[dict[str, Any]] = []
    for dom in registry.get("domains") or []:
        if not isinstance(dom, dict):
            continue
        domains_out.append(
            {
                "id": dom.get("id"),
                "title": dom.get("title"),
                "spine_interface": dom.get("spine_interface"),
                "description": dom.get("description"),
            }
        )

    tech_excerpt = {
        "schema_version": 1,
        "excerpt_of": "Factory-DRB/Tech-Stack-Manifest-v1.yaml",
        "project_id": project_id,
        "filter": "locked|trialing|integrated",
        "rows": rows_out,
    }
    reg_excerpt = {
        "schema_version": 1,
        "excerpt_of": "Factory-DRB/Stack-Domain-Registry-v1.yaml",
        "project_id": project_id,
        "domains": domains_out,
    }
    return tech_excerpt, reg_excerpt, warnings


def _mint_pack_md(project_id: str, synced_at: str) -> str:
    return f"""# Mint pack — `{project_id}`

**Law:** open `weave/component-proposals/catalog_mint.yaml` first (Trinity card).

**This folder** is feedstock for product `slice-catalog.yaml` rows — not CARD-INDEX.

| File | Use |
|------|-----|
| `PACK-MANIFEST.yaml` | synced_at + required files |
| `CONCEPTUAL-EXCERPT.md` | PMG / conceptual roll-up |
| `PIN-INDEX.md` | Legal conceptual_pin titles |
| `ROADMAP-RESOURCE-INDEX.yaml` | **Poll index** — roadmap notes + connected resources + tert_ids |
| `PIN-EXCERPTS/` | Optional pin body mirrors |
| `Tech-Stack-Excerpt.yaml` | Locked/trialing/integrated stack rows |
| `Stack-Domain-Registry-Excerpt.yaml` | Domain ids + spine_interface |
| `slice-catalog.yaml` | Applied rows mirror |

**When you need more info during mint:** open `ROADMAP-RESOURCE-INDEX.yaml`, find the roadmap entry, follow `wiki_links` / `linked_resources`. Bodies not in pack → ask bone pilot for fulfill (`tert_id`) or paste. Do not invent notes.

synced_at: `{synced_at}`

Connector = **main only**. Ask bone pilot to re-run `catalog_mint_pack_emit` if files are missing.
"""


def _load_tert_resolve(vault_root: Path, project_id: str) -> dict[str, str]:
    """Map vault_rel → tert_id from local resolve map (invert)."""
    path = vault_root / ".technical/grok-bridge" / project_id / "tertiary-resolve.json"
    if not path.is_file():
        return {}
    try:
        import json

        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict):
        return {}
    # resolve is tert_id → vault_rel
    return {str(v): str(k) for k, v in data.items() if k and v}


def _note_kind(rel: str, stem: str) -> str:
    low = rel.lower()
    if "conceptual-decision" in low or "/cdr" in low:
        return "cdr"
    if "roll-up" in stem.lower() or "rollup" in stem.lower():
        return "rollup"
    if stem.lower().startswith("phase-"):
        return "phase"
    if "user-story" in low:
        return "user_story"
    if "execution" in low:
        return "execution"
    return "roadmap"


def _build_roadmap_resource_index(
    vault_root: Path, project_id: str
) -> tuple[dict[str, Any], list[str]]:
    """Index Roadmap notes + outbound wiki-links for Grok poll during mint."""
    warnings: list[str] = []
    base = project_root(vault_root, project_id)
    roadmap = base / "Roadmap"
    rel_to_tert = _load_tert_resolve(vault_root, project_id)
    if not rel_to_tert:
        warnings.append("tertiary_resolve_missing")

    roadmap_notes: list[dict[str, Any]] = []
    resource_hits: dict[str, dict[str, Any]] = {}

    if not roadmap.is_dir():
        warnings.append("roadmap_dir_missing")
        return (
            {
                "schema_version": 1,
                "project_id": project_id,
                "poll_protocol": (
                    "During mint, poll this index for roadmap context and connected "
                    "resources. Request fulfill by tert_id when body is not in PIN-EXCERPTS."
                ),
                "roadmap_notes": [],
                "resources": [],
            },
            warnings,
        )

    for path in sorted(roadmap.rglob("*.md")):
        if not path.is_file():
            continue
        try:
            rel_proj = path.relative_to(base).as_posix()
            vault_rel = path.resolve().relative_to(vault_root.resolve()).as_posix()
        except ValueError:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        links = [m.group(1).strip() for m in _WIKI_LINK_RE.finditer(text)]
        # de-dupe preserve order
        seen: set[str] = set()
        wiki_links: list[str] = []
        for link in links:
            if link not in seen:
                seen.add(link)
                wiki_links.append(link)

        linked_resources: list[str] = []
        for link in wiki_links:
            if (
                link.startswith("3-Resources/")
                or "resource" in link.lower()
                or link.startswith("5-Attachments/")
            ):
                linked_resources.append(link)
                entry = resource_hits.setdefault(
                    link,
                    {
                        "title": link.split("/")[-1],
                        "ref": link,
                        "tert_id": rel_to_tert.get(link),
                        "linked_from": [],
                    },
                )
                if path.stem not in entry["linked_from"]:
                    entry["linked_from"].append(path.stem)

        roadmap_notes.append(
            {
                "title": path.stem,
                "wiki": f"[[{path.stem}]]",
                "rel_under_project": rel_proj,
                "kind": _note_kind(rel_proj, path.stem),
                "wiki_links": wiki_links[:40],
                "linked_resources": linked_resources[:20],
                "tert_id": rel_to_tert.get(vault_rel),
                "pin_excerpt_available": False,  # filled by caller if needed
            }
        )

    index = {
        "schema_version": 1,
        "project_id": project_id,
        "poll_protocol": (
            "When minting and you need more information: (1) find the roadmap note by "
            "title/wiki in roadmap_notes; (2) follow wiki_links and linked_resources; "
            "(3) if PIN-EXCERPTS lacks the body, ask bone pilot for Tier C fulfill using "
            "tert_id (or a paste). Do not invent titles or open vault 1-Projects/ paths. "
            "Legal conceptual_pin values still come only from PIN-INDEX.md."
        ),
        "roadmap_note_count": len(roadmap_notes),
        "resource_count": len(resource_hits),
        "roadmap_notes": roadmap_notes,
        "resources": sorted(resource_hits.values(), key=lambda r: str(r.get("ref") or "")),
    }
    return index, warnings


def _ensure_shared(vault_root: Path) -> None:
    shared = vault_root / SHARED_REL
    shared.mkdir(parents=True, exist_ok=True)
    good = shared / "WHAT-GOOD-LOOKS-LIKE.md"
    if not good.is_file():
        good.write_text(
            "# What a good catalog mint looks like\n\n"
            "See Trinity card `catalog_mint` rules leg + receipt fixture.\n",
            encoding="utf-8",
        )


def emit_catalog_mint_pack(
    vault_root: Path,
    *,
    project_id: str,
    set_active: bool = True,
    copy_pin_excerpts_from: Path | None = None,
) -> CatalogMintPackResult:
    """Write Docs/catalog-mint/<project_id>/ from vault project surfaces."""
    vault_root = vault_root.resolve()
    pid = str(project_id or "").strip()
    if not pid:
        raise ValueError("project_id required")

    _ensure_shared(vault_root)
    out_dir = pack_dir_for(vault_root, pid)
    out_dir.mkdir(parents=True, exist_ok=True)
    warnings: list[str] = []
    synced_at = _utc_now()
    hashes: dict[str, str] = {}

    # Conceptual
    pmg = _find_pmg(vault_root, pid)
    if pmg and pmg.is_file():
        conceptual = _excerpt_pmg(pmg)
    else:
        conceptual = (
            f"# Conceptual / PMG excerpt\n\n"
            f"_Missing PMG for `{pid}` — bone pilot must supply feedstock._\n"
        )
        warnings.append("pmg_missing")
    (out_dir / "CONCEPTUAL-EXCERPT.md").write_text(conceptual, encoding="utf-8")
    hashes["CONCEPTUAL-EXCERPT.md"] = _sha256_text(conceptual)

    # Pins
    titles = _collect_pin_titles(vault_root, pid)
    pin_index = _write_pin_index(titles, pid)
    if not titles:
        warnings.append("pin_index_empty")
    (out_dir / "PIN-INDEX.md").write_text(pin_index, encoding="utf-8")
    hashes["PIN-INDEX.md"] = _sha256_text(pin_index)

    # Roadmap + connected resources poll index (built after pin excerpts for flags)
    rri, rri_warn = _build_roadmap_resource_index(vault_root, pid)
    warnings.extend(rri_warn)

    # Pin excerpts
    excerpts_dir = out_dir / "PIN-EXCERPTS"
    excerpts_dir.mkdir(exist_ok=True)
    if copy_pin_excerpts_from and copy_pin_excerpts_from.is_dir():
        for p in copy_pin_excerpts_from.glob("*.md"):
            shutil.copy2(p, excerpts_dir / p.name)

    excerpts_names = {p.stem for p in excerpts_dir.glob("*.md")}
    for note in rri.get("roadmap_notes") or []:
        if isinstance(note, dict):
            stem = str(note.get("title") or "")
            note["pin_excerpt_available"] = any(
                stem in name or name in stem for name in excerpts_names
            )

    rri_text = _dump_yaml(rri)
    (out_dir / "ROADMAP-RESOURCE-INDEX.yaml").write_text(rri_text, encoding="utf-8")
    hashes["ROADMAP-RESOURCE-INDEX.yaml"] = _sha256_text(rri_text)

    # Stack
    tech, reg, stack_warn = _stack_excerpts(vault_root, pid)
    warnings.extend(stack_warn)
    tech_text = _dump_yaml(tech)
    reg_text = _dump_yaml(reg)
    (out_dir / "Tech-Stack-Excerpt.yaml").write_text(tech_text, encoding="utf-8")
    (out_dir / "Stack-Domain-Registry-Excerpt.yaml").write_text(reg_text, encoding="utf-8")
    hashes["Tech-Stack-Excerpt.yaml"] = _sha256_text(tech_text)
    hashes["Stack-Domain-Registry-Excerpt.yaml"] = _sha256_text(reg_text)

    # Catalog mirror
    paths = user_story_paths(vault_root, pid)
    cat_path = paths["catalog"]
    if cat_path.is_file():
        cat_text = cat_path.read_text(encoding="utf-8")
    else:
        cat_text = _dump_yaml(
            {
                "schema_version": 1,
                "project_id": pid,
                "rows": [],
            }
        )
        warnings.append("catalog_missing_seeded_empty")
    (out_dir / "slice-catalog.yaml").write_text(cat_text, encoding="utf-8")
    hashes["slice-catalog.yaml"] = _sha256_text(cat_text)

    mint_pack = _mint_pack_md(pid, synced_at)
    (out_dir / "MINT-PACK.md").write_text(mint_pack, encoding="utf-8")
    hashes["MINT-PACK.md"] = _sha256_text(mint_pack)

    # Copy shared good-looks into pack for convenience (optional mirror)
    shared_good = vault_root / SHARED_REL / "WHAT-GOOD-LOOKS-LIKE.md"
    if shared_good.is_file():
        shutil.copy2(shared_good, out_dir / "WHAT-GOOD-LOOKS-LIKE.md")

    manifest = {
        "schema_version": 1,
        "project_id": pid,
        "synced_at": synced_at,
        "card": "catalog_mint",
        "card_path_on_main": "weave/component-proposals/catalog_mint.yaml",
        "pack_path_on_main": f"Docs/catalog-mint/{pid}/",
        "required_files": list(REQUIRED_FILES),
        "file_hashes": hashes,
        "warnings": warnings,
    }
    man_text = _dump_yaml(manifest)
    (out_dir / "PACK-MANIFEST.yaml").write_text(man_text, encoding="utf-8")

    if set_active:
        active_path(vault_root).parent.mkdir(parents=True, exist_ok=True)
        active_path(vault_root).write_text(
            f"# Active catalog-mint project\n\n"
            f"active_project_id: {pid}\n\n"
            f"synced_at: {synced_at}\n"
            f"card: weave/component-proposals/catalog_mint.yaml\n"
            f"pack: Docs/catalog-mint/{pid}/\n",
            encoding="utf-8",
        )

    missing = [name for name in REQUIRED_FILES if not (out_dir / name).is_file()]
    ok = len(missing) == 0 and "pmg_missing" not in warnings
    # Allow ok with warnings if files present (pmg_missing still marks not ok)
    if missing:
        ok = False
    elif "tech_stack_manifest_missing" in warnings and "stack_domain_registry_missing" in warnings:
        ok = False

    return CatalogMintPackResult(
        ok=ok,
        project_id=pid,
        pack_dir=str(out_dir.relative_to(vault_root)),
        synced_at=synced_at,
        missing=tuple(missing),
        warnings=tuple(warnings),
        file_hashes=hashes,
    )


def list_pack_project_ids(vault_root: Path) -> list[str]:
    root = vault_root / PACK_DOCS_REL
    if not root.is_dir():
        return []
    out: list[str] = []
    for p in sorted(root.iterdir()):
        if p.is_dir() and p.name not in {"_shared"} and not p.name.startswith("."):
            out.append(p.name)
    return out


_WIKI_RE = re.compile(r"\[\[([^\]]+)\]\]")


def pin_titles_from_index(text: str) -> set[str]:
    return {m.group(1).strip() for m in _WIKI_RE.finditer(text)}
