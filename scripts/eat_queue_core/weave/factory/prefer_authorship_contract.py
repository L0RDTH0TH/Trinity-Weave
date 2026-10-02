"""Prefer authorship contract — durable product seats for worldgen / Terrain3D feed.

Constitution-grade Prefer law (not one-off brief text). Product Prefer seats dominate
proxy metrics (budgets, file existence, shell checklists, bootstrap stubs).

Locked step-1 law (operator 2026-10-01):
  Craft = Hot Wheels tile authorship; Terrain3D = fed car under Sparky;
  no craft-view blend; no cam recenter on place.
  Cite: https://www.youtube.com/watch?v=Y19Mw5YsgjI
  Vault: Ingest/Resources/Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01.md
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .factory_little_val import FactoryLittleValResult

YT_CANONICAL = "https://www.youtube.com/watch?v=Y19Mw5YsgjI"
VAULT_CITE = (
    "Ingest/Resources/Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01.md"
)

# Durable negative examples — Prefer must not re-blend these failure modes.
NEGATIVE_EXAMPLES: tuple[dict[str, str], ...] = (
    {
        "id": "cam_yank_on_place",
        "refuse": "craft_cam_recenter_on_place",
        "summary": "Craft place/remove recenters camera / orbit focus onto the new tile",
    },
    {
        "id": "craft_view_terrain_blend",
        "refuse": "craft_terrain_blend",
        "summary": "Craft view deforms checker/grid into Terrain3D heights (Hot Wheels≠car)",
    },
    {
        "id": "craft_phase_terrain3d_deform",
        "refuse": "craft_phase_terrain3d_deform",
        "summary": "Craft phase authors via Terrain3D sculpt instead of tile map",
    },
    {
        "id": "missing_sparky_feed_separation",
        "refuse": "unfed_terrain_under_sparky",
        "summary": "Sparky sees graybox-only; Terrain3D not fed as separate consumer layer",
    },
    {
        "id": "layer_collapse_in_craft",
        "refuse": "inspiration_shape_miss",
        "summary": "Prefer collapses Hot Wheels craft into Terrain3D under craft cam",
    },
)

WORLDGEN_SLICE_MARKERS: tuple[str, ...] = (
    "worldgen",
    "terrain3d_feed",
    "dualgrid",
    "dual_grid",
    "ux_world_generation",
)

# Patterns that indicate craft-cam recenter / focus yank on place (structural heuristics).
_CAM_RECENTER_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"SetFocusWorld\s*\(", re.I),
    re.compile(r"GlobalPosition\s*=\s*.*pick|picked|cell|place", re.I),
    re.compile(r"recenter.*(?:place|paint|cell)|(?:place|paint|cell).*recenter", re.I),
)

# Patterns that indicate craft-view Terrain3D deform (blend under craft).
_CRAFT_BLEND_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(
        r"craft.*(?:SetHeight|SetHeights|sculpt|deform).*Terrain3D|"
        r"Terrain3D.*(?:SetHeight|SetHeights|sculpt|deform).*craft",
        re.I,
    ),
    re.compile(r"ApplyTerrain(?:Under|In)Craft|BlendCraft(?:To|Into)Terrain", re.I),
)


@dataclass(frozen=True)
class PreferAuthorshipResult:
    ok: bool
    little_val: FactoryLittleValResult
    detail: str
    applicable: bool = True
    negative_examples: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "detail": self.detail,
            "applicable": self.applicable,
            "violations": list(self.little_val.anti_pattern_violations),
            "negative_examples": list(self.negative_examples),
        }


def slice_requires_prefer_authorship(slice_id: str, job: dict[str, Any] | None = None) -> bool:
    """True when slice / Prefer overlay is worldgen or Terrain3D-feed authorship."""
    blob = " ".join(
        [
            str(slice_id or ""),
            str((job or {}).get("ask_id") or ""),
            str((job or {}).get("half_b_overlay_slice_id") or ""),
            str((job or {}).get("catalog_row_id") or ""),
            str((job or {}).get("prefer_proof") or ""),
        ]
    ).lower()
    if any(m in blob for m in WORLDGEN_SLICE_MARKERS):
        return True
    armed = str((job or {}).get("armed_packet_path") or "")
    if armed and any(m in armed.lower() for m in WORLDGEN_SLICE_MARKERS):
        return True
    if (job or {}).get("step1_authorship") or (job or {}).get("prefer_authorship"):
        return True
    return False


def load_armed_packet(vault_root: Path, job: dict[str, Any] | None) -> dict[str, Any]:
    path_s = str((job or {}).get("armed_packet_path") or "").strip()
    if not path_s:
        return {}
    path = vault_root / path_s
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def authorship_overlay_markdown(*, slice_id: str = "") -> str:
    """Step-1 authorship overlay injected into producer missions / Prefer handoffs."""
    neg = "\n".join(
        f"- `{ex['refuse']}` — {ex['summary']}" for ex in NEGATIVE_EXAMPLES
    )
    return (
        "## Prefer authorship contract (host law — durable; not one-off brief text)\n\n"
        f"- **Slice:** `{slice_id or '(matching worldgen/terrain3d_feed)'}`\n"
        f"- **YT lock:** {YT_CANONICAL}\n"
        f"- **Vault cite:** `{VAULT_CITE}`\n"
        "- **Craft** = Hot Wheels tile authorship only (Townscaper dual-grid)\n"
        "- **Terrain3D** = real car / fed consumer under Sparky (or explicit feed)\n"
        "- **No** craft-view Terrain3D blend / deform\n"
        "- **No** camera recenter on place\n"
        "- **No proxy override:** host_touch_budget / shell seats / bootstrap stubs "
        "cannot pass or waive these product Prefer seats\n\n"
        "### Durable negative examples (fail closed)\n"
        f"{neg}\n"
    )


def _scan_repo_for_refuse(
    game_repo: Path,
    *,
    changed_paths: tuple[str, ...] | None,
) -> list[str]:
    """Structural heuristics over changed (or key worldgen) C# sources."""
    violations: list[str] = []
    if not game_repo.is_dir():
        return ["prefer_authorship:game_repo_missing"]

    candidates: list[Path] = []
    if changed_paths:
        for rel in changed_paths:
            fp = game_repo / rel
            if fp.is_file() and fp.suffix.lower() == ".cs":
                candidates.append(fp)
    if not candidates:
        # Prefer-scoped default surfaces when no change set (fail soft on missing).
        for rel in (
            "Systems/Worldgen/DualGridCraftHost.cs",
            "Systems/Worldgen/WorldgenCraftController.cs",
            "Core/WorldGen/DualGridCraftHost.cs",
        ):
            fp = game_repo / rel
            if fp.is_file():
                candidates.append(fp)
        # Broader scan of Systems/** craft hosts when present.
        systems = game_repo / "Systems"
        if systems.is_dir():
            for fp in systems.rglob("*Craft*.cs"):
                candidates.append(fp)
            for fp in systems.rglob("*Worldgen*.cs"):
                candidates.append(fp)

    seen: set[Path] = set()
    for fp in candidates:
        if fp in seen or not fp.is_file():
            continue
        seen.add(fp)
        text = fp.read_text(encoding="utf-8", errors="replace")
        rel = str(fp.relative_to(game_repo)).replace("\\", "/")
        # Explicit refuse tags in source / receipts count as documented bans (ok).
        refuse_documented = "refuse craft_cam_recenter_on_place" in text.lower() or (
            "craft_cam_recenter_on_place" in text and "refuse" in text.lower()
        )
        for pat in _CAM_RECENTER_PATTERNS:
            if pat.search(text) and not refuse_documented:
                # SetFocusWorld alone is not enough — require place/paint context nearby.
                if "SetFocusWorld" in pat.pattern:
                    if re.search(
                        r"(TryPick|Paint|Place|OnPrimary|OnClick).{0,400}SetFocusWorld|"
                        r"SetFocusWorld.{0,200}(Pick|Paint|Place|cell)",
                        text,
                        re.I | re.S,
                    ):
                        violations.append(f"craft_cam_recenter_on_place:{rel}")
                else:
                    violations.append(f"craft_cam_recenter_on_place:{rel}")
                break
        for pat in _CRAFT_BLEND_PATTERNS:
            if pat.search(text):
                violations.append(f"craft_terrain_blend:{rel}")
                break

    # Manifest / receipt honesty: factory Systems manifest may declare open refuse codes.
    man = game_repo / "Systems/_factory/manifest.yaml"
    if man.is_file():
        try:
            data = yaml.safe_load(man.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError):
            data = {}
        if isinstance(data, dict):
            open_fails = data.get("open_prefer_fails") or data.get("prefer_fails_open") or []
            if isinstance(open_fails, list):
                for code in open_fails:
                    c = str(code).strip()
                    if c in {ex["refuse"] for ex in NEGATIVE_EXAMPLES}:
                        violations.append(f"open_prefer_fail:{c}")

    return sorted(set(violations))


def run_prefer_authorship_pass(
    vault_root: Path,
    *,
    lane_id: str | None = None,
    game_repo_rel: str = "",
    changed_paths: tuple[str, ...] | None = None,
    job: dict[str, Any] | None = None,
) -> PreferAuthorshipResult:
    """
    Product Prefer seat — fail closed on layer blend / cam yank / craft Terrain3D deform
    / missing sparky-feed separation signals. Waives cannot silence this seat.
    """
    vault_root = vault_root.resolve()
    job = job if isinstance(job, dict) else {}
    slice_id = str(job.get("slice_id") or "")
    applicable = slice_requires_prefer_authorship(slice_id, job)
    if not applicable:
        lv = FactoryLittleValResult(True, [], "prefer_authorship_pass_skipped")
        return PreferAuthorshipResult(
            True, lv, "prefer_authorship_not_applicable", applicable=False
        )

    # Product Prefer seats are never waiveable — even shell-era waive flags.
    if job.get("waive_shell_era_seats") and "prefer_authorship_pass" in (
        job.get("waive_seats") or []
    ):
        lv = FactoryLittleValResult(
            False,
            ["waive_forbidden_on_product_prefer_seat:prefer_authorship_pass"],
            "prefer_authorship_pass",
        )
        return PreferAuthorshipResult(
            False,
            lv,
            "waive_forbidden_on_product_prefer_seat",
            applicable=True,
            negative_examples=tuple(ex["refuse"] for ex in NEGATIVE_EXAMPLES),
        )

    violations: list[str] = []
    cite = vault_root / VAULT_CITE
    if not cite.is_file():
        violations.append(f"missing_authorship_vault_cite:{VAULT_CITE}")

    armed = load_armed_packet(vault_root, job)
    step1 = armed.get("step1_authorship") if isinstance(armed.get("step1_authorship"), dict) else {}
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    step1_lock = (
        locks.get("step1_authorship")
        if isinstance(locks.get("step1_authorship"), dict)
        else step1
    )
    if armed and not step1_lock and not locks.get("step1_authorship"):
        # Prefer overlay armed without step1 lock → topology/authorship drift.
        if any(m in str(armed.get("slice_id") or "").lower() for m in WORLDGEN_SLICE_MARKERS):
            violations.append("armed_packet_missing_step1_authorship_lock")

    if not game_repo_rel:
        violations.append("missing_game_repo_rel")
    else:
        repo = vault_root / game_repo_rel.strip("/")
        violations.extend(
            _scan_repo_for_refuse(repo, changed_paths=changed_paths)
        )

    # do_not_waive product Prefer seats must remain listed when Prefer overlay present.
    do_not_waive = job.get("do_not_waive") or []
    if isinstance(do_not_waive, str):
        do_not_waive = [do_not_waive]
    product_codes = {
        "Terrain3D_prefer_proof",
        "prefer_authorship_pass",
        "craft_cam_recenter_on_place",
        "craft_terrain_blend",
    }
    # Soft: only require when Prefer fields present on job.
    if job.get("prefer_proof") or job.get("armed_packet_path") or job.get("half_b_brief_path"):
        if not any(str(x) in product_codes or "Terrain3D" in str(x) for x in do_not_waive):
            # Advisory → binding: Prefer overlays must declare do_not_waive product seats.
            violations.append("prefer_overlay_missing_do_not_waive_product_seats")

    ok = len(violations) == 0
    lv = FactoryLittleValResult(ok, violations, "prefer_authorship_pass")
    detail = "; ".join(violations) if violations else "prefer_authorship_pass_ok"
    return PreferAuthorshipResult(
        ok,
        lv,
        detail,
        applicable=True,
        negative_examples=tuple(ex["refuse"] for ex in NEGATIVE_EXAMPLES),
    )


def product_prefer_seats_met(lane_seats: dict[str, Any] | None) -> bool:
    """True when Prefer product seats (authorship) are ok or not applicable."""
    if not lane_seats:
        return True
    passes = lane_seats.get("passes") or {}
    authorship = passes.get("prefer_authorship_pass")
    if authorship is None:
        return True
    return bool(getattr(authorship, "ok", True) if not isinstance(authorship, dict) else authorship.get("ok"))
