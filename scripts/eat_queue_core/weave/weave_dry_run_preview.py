"""Grok E — dry-run preview bundle for trinity_weave_self_wrap (pass_gate + 10e + adequacy)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import load_trinity_config
from .corps_proof_adequacy import summarize_adequacy_from_nerves
from .trinity_provisional_corps_sweep import (
    build_corps_pass_gate,
    load_corps_nerve_map,
)


def build_weave_dry_run_preview(
    vault_root: Path,
    *,
    full_corpus: bool = True,
    regenerate_complete: bool = False,
    meta_lens_force_align: bool = False,
) -> dict[str, Any]:
    """Read-only preview: stored nerve map pass_gate, 10e dry-run, adequacy summary."""
    vault_root = vault_root.resolve()
    cfg = load_trinity_config(vault_root)
    preview: dict[str, Any] = {
        "ok": True,
        "full_corpus": full_corpus,
        "regenerate_complete_requested": regenerate_complete,
        "meta_lens_force_align_requested": meta_lens_force_align,
    }

    nmap = load_corps_nerve_map(vault_root)
    if nmap:
        nerve = {
            "ok": True,
            "counts": nmap.get("counts"),
            "tier_failures": nmap.get("tier_failures"),
            "nerves": nmap.get("nerves"),
            "tested": len(nmap.get("nerves") or []),
            "generated_at": nmap.get("generated_at"),
        }
        preview["pass_gate"] = build_corps_pass_gate(nerve, full_corpus=full_corpus)
        preview["nerve_map_age"] = nmap.get("generated_at")
        nerves = nmap.get("nerves") or []
        preview["proof_adequacy"] = summarize_adequacy_from_nerves(nerves)
        preview["red_ids_sample"] = (preview["pass_gate"].get("red_ids") or [])[:12]
    else:
        preview["pass_gate"] = {
            "ok": False,
            "reason": "no_corps_nerve_map",
            "hint": "Run trinity_provisional_corps_sweep --full-corpus first",
        }

    if regenerate_complete:
        from .corps_corpus_regenerate import run_regenerate_complete

        preview["regenerate_complete"] = run_regenerate_complete(
            vault_root,
            dry_run=True,
            cli_requested=True,
            meta_lens_force_align=bool(meta_lens_force_align),
        )
        preview["11a"] = _load_11a_status(vault_root)

    val_dir = vault_root / ".technical/weave/validation"
    if val_dir.is_dir():
        reports = sorted(val_dir.glob("trinity-weave-self-wrap-*.json"), reverse=True)
        if reports:
            try:
                last = json.loads(reports[0].read_text(encoding="utf-8"))
                preview["last_self_wrap"] = {
                    "path": str(reports[0].relative_to(vault_root)),
                    "ok": last.get("ok"),
                    "pass_gate_ok": (last.get("pass_gate") or {}).get("ok"),
                    "conduct_ok": (last.get("pass_gate") or {}).get("conduct_ok"),
                    "completed_at": last.get("completed_at"),
                }
            except (OSError, json.JSONDecodeError):
                pass

    preview["config"] = {
        "corps_regenerate_complete_enabled": cfg.corps_regenerate_complete_enabled,
        "corps_regenerate_require_11a": cfg.corps_regenerate_require_11a,
        "corps_regen_meta_lens_force_align_enabled": getattr(
            cfg, "corps_regen_meta_lens_force_align_enabled", False
        ),
        "mvl_conductor_enabled": getattr(cfg, "mvl_conductor_enabled", True),
        "corps_conduct_pending_ok": cfg.corps_conduct_pending_ok,
    }
    return preview


def _load_11a_status(vault_root: Path) -> dict[str, Any]:
    from .trinity_card_11a import load_11a_status

    return load_11a_status(vault_root)
