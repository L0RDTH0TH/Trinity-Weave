"""Load product BOM manifest (Factory-DRB/product-bom.yaml)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from ..factory.factory_output_gate import parse_factory_orchestrator_yaml

DEFAULT_BOM_REL = "Factory-DRB/product-bom.yaml"


def product_bom_path(vault_root: Path, project_id: str) -> Path:
    cfg = parse_factory_orchestrator_yaml(vault_root / "3-Resources/Second-Brain-Config.md")
    fb = cfg.get("factory_bom") if isinstance(cfg.get("factory_bom"), dict) else {}
    rel = str(fb.get("bom_rel") or DEFAULT_BOM_REL)
    if not rel.startswith("1-Projects/"):
        rel = f"1-Projects/{project_id}/{rel.lstrip('/')}"
    return vault_root / rel


def load_product_bom(vault_root: Path, project_id: str) -> dict[str, Any]:
    path = product_bom_path(vault_root, project_id)
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def parse_release_frontmatter(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    block = yaml.safe_load(text[4:end]) or {}
    return block if isinstance(block, dict) else {}
