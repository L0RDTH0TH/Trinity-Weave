"""Fail-closed validation for a single Grok/Cursor catalog mint YAML receipt."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .catalog_mint_pack import pack_dir_for, pin_titles_from_index

FORBIDDEN_KEYS = frozenset(
    {
        "trinity_id",
        "progress",
        "priority",
        "pass_gate",
        "CARD-INDEX-update",
        "catalog_signed_at",
    }
)

ALLOWED_DIMENSIONS = frozenset(
    {
        "ui_surface",
        "sim_system",
        "world_gen",
        "dm_rail",
        "player_rail",
        "rules",
        "session_bootstrap",
        "platform",
        "other",
    }
)


@dataclass(frozen=True)
class CatalogMintReceiptResult:
    ok: bool
    violations: tuple[str, ...]
    row: dict[str, Any] | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "violations": list(self.violations),
            "row": self.row,
        }


def _parse_receipt(raw: str | dict[str, Any] | list[Any]) -> list[dict[str, Any]]:
    if isinstance(raw, dict):
        if "rows" in raw and isinstance(raw["rows"], list):
            return [r for r in raw["rows"] if isinstance(r, dict)]
        return [raw]
    if isinstance(raw, list):
        return [r for r in raw if isinstance(r, dict)]
    text = str(raw).strip()
    if not text:
        return []
    # Strip markdown fences
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    data = yaml.safe_load(text)
    return _parse_receipt(data) if data is not None else []


def _domain_ids_from_pack(pack: Path) -> set[str]:
    ids: set[str] = set()
    for name in ("Tech-Stack-Excerpt.yaml", "Stack-Domain-Registry-Excerpt.yaml"):
        p = pack / name
        if not p.is_file():
            continue
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        for row in data.get("rows") or []:
            if isinstance(row, dict) and row.get("stack_domain_id"):
                ids.add(str(row["stack_domain_id"]))
        for dom in data.get("domains") or []:
            if isinstance(dom, dict) and dom.get("id"):
                ids.add(str(dom["id"]))
    return ids


def validate_catalog_mint_receipt(
    vault_root: Path,
    *,
    project_id: str,
    receipt: str | dict[str, Any] | list[Any],
    require_pack: bool = True,
) -> CatalogMintReceiptResult:
    """Validate one proposed row against pack PIN-INDEX and stack excerpts."""
    violations: list[str] = []
    rows = _parse_receipt(receipt)
    if not rows:
        return CatalogMintReceiptResult(ok=False, violations=("receipt_empty",), row=None)
    if len(rows) != 1:
        violations.append(f"receipt_row_count:{len(rows)}")

    row = rows[0]
    for key in FORBIDDEN_KEYS:
        if key in row:
            violations.append(f"forbidden_key:{key}")

    rid = str(row.get("id") or "").strip()
    if not rid:
        violations.append("missing_id")
    elif " " in rid or rid != rid.lower():
        violations.append("id_not_snake_case")

    dim = str(row.get("dimension") or "").strip()
    if dim not in ALLOWED_DIMENSIONS:
        violations.append(f"bad_dimension:{dim or 'missing'}")

    if row.get("mint_status") != "proposed":
        violations.append("mint_status_not_proposed")

    if row.get("planned") is not True:
        violations.append("planned_not_true")

    pack = pack_dir_for(vault_root, project_id)
    pin_index = pack / "PIN-INDEX.md"
    if require_pack and not pack.is_dir():
        violations.append("pack_missing")
    elif require_pack and not (pack / "PACK-MANIFEST.yaml").is_file():
        violations.append("pack_manifest_missing")

    pin = str(row.get("conceptual_pin") or "").strip()
    if pin and pin.lower() not in {"needs pin", "needs_pin"}:
        titles = pin_titles_from_index(pin_index.read_text(encoding="utf-8")) if pin_index.is_file() else set()
        # normalize [[Title]] vs Title
        inner = pin
        if inner.startswith("[[") and inner.endswith("]]"):
            inner = inner[2:-2].strip()
        if titles and inner not in titles and f"[[{inner}]]" not in {f"[[{t}]]" for t in titles}:
            if inner not in titles:
                violations.append(f"pin_not_in_index:{inner}")
    elif not pin:
        violations.append("missing_conceptual_pin")

    domains = row.get("stack_domain_ids")
    if domains is None:
        pass
    elif not isinstance(domains, list):
        violations.append("stack_domain_ids_not_list")
    elif domains:
        allowed = _domain_ids_from_pack(pack) if pack.is_dir() else set()
        if allowed:
            for d in domains:
                if str(d) not in allowed:
                    violations.append(f"stack_domain_not_in_excerpt:{d}")

    ok = len(violations) == 0
    return CatalogMintReceiptResult(ok=ok, violations=tuple(violations), row=row if ok else row)
