"""Generate PROJECT-OBSERVABILITY.json and GROK-PROJECT-START for project branches."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BRIDGE_LAYOUT_VERSION = "1"
DEFAULT_GATE_CARDS = (
    "catalog_mint_gate",
    "product_factory_pipeline",
    "ux_context_execution_gate",
    "factory_product_bom",
)


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _file_fingerprint(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        st = path.stat()
        return f"{path.resolve().as_posix()}:{st.st_mtime_ns}:{st.st_size}"
    except OSError:
        return None


def _collect_input_fingerprints(project_root: Path) -> list[str]:
    parts: list[str] = []
    candidates: list[Path] = []
    for pattern in (
        "Roadmap/**/*.md",
        "Roadmap/**/*.yaml",
        "Roadmap/**/*.json",
        f"{project_root.name}-goal.md",
        f"{project_root.name}-Roadmap-MOC.md",
        "roadmap-state.md",
        "Factory-DRB/**/*",
    ):
        if "**" in pattern:
            candidates.extend(project_root.glob(pattern))
        else:
            p = project_root / pattern
            if p.exists():
                candidates.append(p)
    for p in sorted(set(candidates), key=lambda x: x.as_posix()):
        if p.is_file():
            fp = _file_fingerprint(p)
            if fp:
                parts.append(fp)
    return parts


def compute_input_fingerprint(project_root: Path) -> str:
    parts = _collect_input_fingerprints(project_root)
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def _load_yaml(path: Path) -> Any:
    try:
        import yaml  # type: ignore[import-untyped]

        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, ImportError):
        return None


def _catalog_rows(project_root: Path) -> list[dict[str, Any]]:
    catalog = project_root / "Roadmap/User-Story/slice-catalog.yaml"
    if not catalog.is_file():
        return []
    data = _load_yaml(catalog)
    if not isinstance(data, dict):
        return []
    rows = data.get("rows")
    if not isinstance(rows, list):
        return []
    out: list[dict[str, Any]] = []
    for row in rows:
        if isinstance(row, dict) and row.get("id"):
            out.append(row)
    return out


def build_project_observability(
    vault_root: Path,
    project_id: str,
    *,
    cfg: dict[str, Any],
    tertiary_fingerprint: str = "",
) -> dict[str, Any]:
    project_root = vault_root / "1-Projects" / project_id
    branch = cfg.get("project_branch") or f"project/{project_id}"
    input_fp = compute_input_fingerprint(project_root)

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    goal = project_root / f"{project_id}-goal.md"
    moc = project_root / f"{project_id}-Roadmap-MOC.md"
    if goal.is_file():
        nodes.append({"id": "pmg", "kind": "pmg", "path": goal.name, "role": "Project master goal anchor"})
    if moc.is_file():
        nodes.append({"id": "moc", "kind": "moc", "path": moc.name, "role": "Roadmap map of content"})

    catalog_path = "Roadmap/User-Story/slice-catalog.yaml"
    if (project_root / catalog_path).is_file():
        nodes.append({"id": "slice_catalog", "kind": "catalog", "path": catalog_path, "role": "Mint / deliverable rows"})

    for row in _catalog_rows(project_root):
        rid = str(row["id"])
        nodes.append({"id": f"catalog:{rid}", "kind": "catalog_row", "path": catalog_path, "row_id": rid})
        pins = row.get("execution_pins")
        if isinstance(pins, list):
            for pin in pins:
                if isinstance(pin, str) and pin.strip():
                    edges.append({"from": f"catalog:{rid}", "to": pin, "kind": "execution_pin"})
        cpin = row.get("conceptual_pin")
        if isinstance(cpin, str) and cpin.strip():
            edges.append({"from": f"catalog:{rid}", "to": cpin, "kind": "conceptual_pin"})
        related = list(DEFAULT_GATE_CARDS)
        edges.append(
            {
                "from": f"catalog:{rid}",
                "to": related,
                "kind": "related_weave_cards",
                "note": "Gate law on main branch",
            }
        )
        scope_l5 = project_root / "Roadmap/User-Story/scopes" / rid / "L5.md"
        if scope_l5.is_file():
            rel = scope_l5.relative_to(project_root).as_posix()
            nodes.append({"id": f"l5:{rid}", "kind": "l5", "path": rel})
            edges.append({"from": f"catalog:{rid}", "to": f"l5:{rid}", "kind": "row_to_l5"})

    edges.append({"from": "half_a", "to": "half_b", "kind": "factory_handoff", "note": "Roadmap factory → implementation factory"})

    return {
        "schema_version": 1,
        "project_id": project_id,
        "last_generated_utc": _utc_iso(),
        "input_fingerprint": input_fp,
        "tertiary_index_fingerprint": tertiary_fingerprint,
        "last_publish_utc": None,
        "bridge": {
            "trinity_repo": "L0RDTH0TH/Trinity-Weave",
            "main_branch": cfg.get("main_branch") or "main",
            "project_branch": branch,
            "layout_version": BRIDGE_LAYOUT_VERSION,
        },
        "nodes": nodes,
        "edges": edges,
        "routes": {
            "weave_law": {"branch": cfg.get("main_branch") or "main", "paths": ["weave/components/", "weave/component-proposals/"]},
            "project_instances": {"branch": branch, "start": "GROK-PROJECT-START.md"},
        },
    }


def render_grok_project_start(project_id: str, branch: str) -> str:
    return f"""# Grok — project start ({project_id})

**Branch:** `{branch}` (branch name — artifacts at **branch root**, not nested under `project/`)

## If the task is catalog mint

**STOP — this is not `weave/CARD-INDEX` / OBSERVABILITY / harness mint.**

1. `Roadmap/User-Story/CATALOG-MINT-BLANK.md` — **dialogue contract** (one row per turn)
2. `{project_id}-goal.md` — PMG feedstock
3. Live `Roadmap/Phase-*/…` notes — real `conceptual_pin` titles
4. `Roadmap/User-Story/slice-catalog.yaml` — what is already applied
5. `Roadmap/User-Story/MINT-EPOCH.md` — poison guard (ignore archives)

Then: propose **exactly one** product deliverable row → await bone-pilot `approve` / `edit` / `reject` → next.
Do **not** invent wiki-links. Do **not** dump a batch of rows. Do **not** talk about spine/corps/self-wrap.

## General read order (non-mint)

1. `PROJECT-OBSERVABILITY.json` — nodes, edges, fingerprints
2. `TERTIARY-INDEX.json` — metadata-only tertiary pointers (bodies via fulfill packs)
3. `{project_id}-goal.md` / `{project_id}-Roadmap-MOC.md`
4. `Roadmap/` — conceptual, Execution, User-Story (catalog + scopes)

## Locked branch root layout

```text
{branch}/   ← git branch name
├── GROK-PROJECT-START.md
├── PROJECT-OBSERVABILITY.json
├── TERTIARY-INDEX.json
├── {project_id}-goal.md
├── {project_id}-Roadmap-MOC.md
└── Roadmap/
    ├── Execution/
    └── User-Story/
        ├── CATALOG-MINT-BLANK.md   ← mint dialogue contract
        ├── MINT-EPOCH.md
        ├── slice-catalog.yaml
        └── scopes/<row_id>/L5.md …
```

## Weave law (not on this branch)

Gate cards (`catalog_mint_gate`, etc.) live on **`main`**: `weave/component-proposals/` and `weave/components/`.
They explain **how** mint works — they are **not** the product catalog you fill.

## Hard limits

- No live vault access from GitHub — stale remote possible; check `bridge` fingerprints
- Tertiary bodies only via mediated fulfill packs (bone pilot + Cursor gate)
"""


def write_project_observability_artifacts(
    vault_root: Path,
    project_id: str,
    *,
    cfg: dict[str, Any],
    tertiary_fingerprint: str = "",
) -> dict[str, Any]:
    project_root = vault_root / "1-Projects" / project_id
    project_root.mkdir(parents=True, exist_ok=True)

    payload = build_project_observability(
        vault_root,
        project_id,
        cfg=cfg,
        tertiary_fingerprint=tertiary_fingerprint,
    )
    obs_path = project_root / "PROJECT-OBSERVABILITY.json"
    obs_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    start_path = project_root / "GROK-PROJECT-START.md"
    branch = payload["bridge"]["project_branch"]
    start_path.write_text(render_grok_project_start(project_id, branch), encoding="utf-8")

    return {
        "ok": True,
        "project_id": project_id,
        "observability_path": obs_path.relative_to(vault_root).as_posix(),
        "input_fingerprint": payload["input_fingerprint"],
        "node_count": len(payload.get("nodes") or []),
    }
