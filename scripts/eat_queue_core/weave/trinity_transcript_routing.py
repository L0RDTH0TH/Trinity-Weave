"""Trinity transcript routing — plan index + agent-transcript scout.

Uses vault `.cursor/plans/**` to build search phrases per trinity_id, then ranks
parent chat transcripts under Cursor's agent-transcripts store.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .trinity_card_generate import _is_locked
from .trinity_touch_refresh import components_dir, load_trinity_card

PLANS_GLOB = ".cursor/plans"

# Pilot cohorts (operator-validated anchors)
HARNESS_SPINE_IDS: tuple[str, ...] = (
    "harness_headless_eat",
    "harness_rewrite_consumed",
    "harness_append_entries",
    "harness_pseudo_clock_tick",
    "harness_post_queue_memory_pass",
    "harness_headless_architect",
    "harness_post_queue_gitforge",
    "harness_snapshot",
    "harness_verify",
    "harness_lane_recovery_retry",
)

GOVERNANCE_SET2_LOCKED_IDS: tuple[str, ...] = (
    "invariant_registry",
    "l2_symbolic_conflict",
    "l2_predictive_maintenance",
    "weave_governance",
    "operator_surface_verifier",
    "little_val_structural",
    "l4_adaptive_policy",
    "ghost_skill_audit",
    "skill_gap",
)

TRANSCRIPT_ROOT_DEFAULT = Path.home() / ".cursor/projects/home-darth-Documents-Second-Brain/agent-transcripts"

NAME_RE = re.compile(r"^name:\s*(.+?)\s*$", re.MULTILINE)
OVERVIEW_RE = re.compile(r"^overview:\s*(.+?)\s*$", re.MULTILINE)
PATH_RE = re.compile(
    r"`((?:scripts/eat_queue_core|\.cursor/skills)[^`]+)`|"
    r"(scripts/eat_queue_core/[\w./-]+\.py)",
)


@dataclass
class TranscriptHit:
    chat_id: str
    transcript_path: str
    score: int
    matched_terms: list[str]
    plan_overlap: list[str]
    mtime_iso: str


@dataclass
class TrinityRoute:
    trinity_id: str
    plans: list[str]
    search_phrases: list[str]
    top_transcripts: list[TranscriptHit]
    notes: str = ""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _slug_phrases(trinity_id: str) -> list[str]:
    base = [trinity_id, trinity_id.replace("_", " ")]
    if trinity_id.startswith("harness_"):
        cmd = trinity_id.removeprefix("harness_")
        base.extend([f"cmd_{cmd}", cmd, f"harness {cmd.replace('_', ' ')}"])
    if trinity_id.startswith("skill_"):
        slug = trinity_id.removeprefix("skill_")
        base.append(f".cursor/skills/{slug}")
    mod = f"scripts/eat_queue_core/weave/{trinity_id}.py"
    if trinity_id.startswith("harness_"):
        cmd = trinity_id.removeprefix("harness_")
        mod = f"scripts/eat_queue_core/{cmd}.py"
        if cmd == "pseudo_clock_tick":
            mod = "scripts/eat_queue_core/pseudo_clock.py"
    base.append(mod)
    return list(dict.fromkeys(p for p in base if len(p) >= 4))


def _extract_plan_meta(text: str) -> tuple[str, str]:
    name_m = NAME_RE.search(text)
    overview_m = OVERVIEW_RE.search(text)
    name = name_m.group(1).strip() if name_m else ""
    overview = overview_m.group(1).strip() if overview_m else ""
    return name, overview


def _phrases_from_plan_snippet(trinity_id: str, text: str, limit: int = 8) -> list[str]:
    """Pull short distinctive lines from a plan that mention this id."""
    phrases: list[str] = []
    slug = trinity_id.replace("_", " ")
    for line in text.splitlines():
        low = line.lower()
        if trinity_id not in line and slug not in low:
            continue
        clean = line.strip().lstrip("#").strip("| ").strip()
        if 20 <= len(clean) <= 200 and clean not in phrases:
            phrases.append(clean)
        if len(phrases) >= limit:
            break
    return phrases


def build_plan_index(vault_root: Path) -> dict[str, Any]:
    """Scan all vault plans; map trinity_id -> plans, paths, phrases."""
    plans_dir = vault_root / PLANS_GLOB.replace("/**", "").rstrip("/")
    if not plans_dir.is_dir():
        plans_dir = vault_root / ".cursor" / "plans"

    all_plans: list[dict[str, Any]] = []
    by_trinity: dict[str, dict[str, Any]] = {}

    for plan_path in sorted(plans_dir.rglob("*.plan.md")):
        rel = plan_path.relative_to(vault_root).as_posix()
        text = _read_text(plan_path)
        if not text:
            continue
        name, overview = _extract_plan_meta(text)
        paths = sorted(set(PATH_RE.findall(text)))
        flat_paths = [p[0] or p[1] for p in paths if p[0] or p[1]]
        entry = {
            "path": rel,
            "name": name,
            "overview": overview[:300],
            "mtime_iso": datetime.fromtimestamp(plan_path.stat().st_mtime, tz=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "paths_mentioned": flat_paths[:40],
        }
        all_plans.append(entry)

        text_low = text.lower()
        ids_found: set[str] = set()
        for m in re.finditer(r"\b([a-z][a-z0-9_]{4,})\b", text_low):
            token = m.group(1)
            if token.startswith(("harness_", "skill_", "l2_", "l3_", "l4_", "weave_", "ghost_", "invariant_", "operator_", "little_")):
                ids_found.add(token)
        for tid in ids_found:
            bucket = by_trinity.setdefault(
                tid,
                {"plans": [], "search_phrases": [], "plan_phrases": []},
            )
            if rel not in bucket["plans"]:
                bucket["plans"].append(rel)
            for phrase in _phrases_from_plan_snippet(tid, text, limit=3):
                if phrase not in bucket["plan_phrases"]:
                    bucket["plan_phrases"].append(phrase)

    # Enrich pilot ids with slug phrases even if no plan hit
    for tid in set(HARNESS_SPINE_IDS) | set(GOVERNANCE_SET2_LOCKED_IDS):
        bucket = by_trinity.setdefault(
            tid,
            {"plans": [], "search_phrases": [], "plan_phrases": []},
        )
        for p in _slug_phrases(tid):
            if p not in bucket["search_phrases"]:
                bucket["search_phrases"].append(p)
        bucket["search_phrases"].extend(bucket.pop("plan_phrases", []))
        bucket["search_phrases"] = list(dict.fromkeys(bucket["search_phrases"]))[:24]

    return {
        "built_at": _now_iso(),
        "plan_count": len(all_plans),
        "plans": all_plans,
        "by_trinity_id": by_trinity,
    }


def _parent_transcript_files(transcript_root: Path) -> list[Path]:
    out: list[Path] = []
    if not transcript_root.is_dir():
        return out
    for child in transcript_root.iterdir():
        if not child.is_dir() or child.name == "subagents":
            continue
        cand = child / f"{child.name}.jsonl"
        if cand.is_file():
            out.append(cand)
    return out


def _score_transcript(
    text: str,
    phrases: list[str],
    plan_paths: list[str],
) -> tuple[int, list[str]]:
    text_low = text.lower()
    matched: list[str] = []
    score = 0
    for phrase in phrases:
        p = phrase.strip()
        if len(p) < 4:
            continue
        pl = p.lower()
        if pl in text_low:
            matched.append(p)
            score += 3 if len(pl) > 20 else 1
    for plan in plan_paths:
        stem = Path(plan).stem.replace(".plan", "")
        if stem.lower() in text_low:
            matched.append(f"plan:{stem}")
            score += 2
    return score, list(dict.fromkeys(matched))


def route_trinity_id(
    trinity_id: str,
    index: dict[str, Any],
    transcript_root: Path,
    *,
    top_k: int = 5,
) -> TrinityRoute:
    bucket = (index.get("by_trinity_id") or {}).get(trinity_id) or {}
    plans = bucket.get("plans") or []
    phrases = list(dict.fromkeys(_slug_phrases(trinity_id) + (bucket.get("search_phrases") or [])))[:28]

    hits: list[TranscriptHit] = []
    for tpath in _parent_transcript_files(transcript_root):
        text = _read_text(tpath)
        if not text:
            continue
        score, matched = _score_transcript(text, phrases, plans)
        if score <= 0:
            continue
        chat_id = tpath.parent.name
        mtime = datetime.fromtimestamp(tpath.stat().st_mtime, tz=timezone.utc).isoformat().replace(
            "+00:00", "Z"
        )
        plan_overlap = [p for p in plans if Path(p).stem.lower() in text.lower()]
        hits.append(
            TranscriptHit(
                chat_id=chat_id,
                transcript_path=str(tpath),
                score=score,
                matched_terms=matched[:12],
                plan_overlap=plan_overlap[:5],
                mtime_iso=mtime,
            )
        )

    hits.sort(key=lambda h: (-h.score, h.mtime_iso), reverse=False)
    notes = ""
    if not hits:
        notes = "no parent transcript matches — try manual uuid or adjacent plan chats"
    elif hits[0].score < 3:
        notes = "weak matches — review top 2–3 by hand"

    return TrinityRoute(
        trinity_id=trinity_id,
        plans=plans,
        search_phrases=phrases[:16],
        top_transcripts=hits[:top_k],
        notes=notes,
    )


def run_transcript_routing_pilot(
    vault_root: Path,
    *,
    trinity_ids: list[str] | None = None,
    transcript_root: Path | None = None,
    rebuild_index: bool = True,
    index_path: Path | None = None,
) -> dict[str, Any]:
    vault_root = Path(vault_root)
    out_dir = vault_root / ".technical/weave/transcript-routing"
    out_dir.mkdir(parents=True, exist_ok=True)

    idx_path = index_path or (out_dir / "plan-index.json")
    if rebuild_index or not idx_path.is_file():
        index = build_plan_index(vault_root)
        idx_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    else:
        index = json.loads(idx_path.read_text(encoding="utf-8"))

    troot = transcript_root or TRANSCRIPT_ROOT_DEFAULT
    ids = trinity_ids or list(HARNESS_SPINE_IDS) + list(GOVERNANCE_SET2_LOCKED_IDS)

    routes = [route_trinity_id(tid, index, troot) for tid in ids]

    # Known anchor chat from governance/trinity work (operator session)
    anchor_chat = "86623fcd-58ef-4444-ac8e-0d0d805bb4b0"

    lines = [
        "# Transcript routing pilot — harness spine + governance set 2",
        "",
        f"Built: {_now_iso()}",
        f"Plan index: `{idx_path.relative_to(vault_root).as_posix()}` ({index.get('plan_count', 0)} plans)",
        f"Transcript root: `{troot}`",
        "",
        f"**Anchor session (this Trinity push):** [{anchor_chat}]({anchor_chat})",
        "",
        "Compare top `chat_id` per row to where you remember locking each card.",
        "",
        "| trinity_id | plans | top transcript | score | notes |",
        "|-----------|------:|------------------|------:|-------|",
    ]
    for r in routes:
        top = r.top_transcripts[0] if r.top_transcripts else None
        cid = f"`{top.chat_id[:8]}…`" if top else "—"
        sc = str(top.score) if top else "0"
        pl = len(r.plans)
        note = r.notes or (top.matched_terms[0][:40] if top and top.matched_terms else "")
        lines.append(f"| `{r.trinity_id}` | {pl} | {cid} | {sc} | {note} |")

    lines.extend(["", "## Per-card detail", ""])
    for r in routes:
        lines.append(f"### `{r.trinity_id}`")
        lines.append("")
        if r.plans:
            lines.append("**Plans:**")
            for p in r.plans[:8]:
                lines.append(f"- `{p}`")
            if len(r.plans) > 8:
                lines.append(f"- … +{len(r.plans) - 8} more")
        else:
            lines.append("**Plans:** none indexed")
        lines.append("")
        lines.append("**Search phrases (sample):** " + ", ".join(f"`{p}`" for p in r.search_phrases[:6]))
        lines.append("")
        if not r.top_transcripts:
            lines.append("_No transcript hits._")
        else:
            lines.append("| rank | chat_id | score | matched |")
            lines.append("|------|---------|------:|---------|")
            for i, h in enumerate(r.top_transcripts, 1):
                terms = ", ".join(h.matched_terms[:4])
                lines.append(f"| {i} | `{h.chat_id}` | {h.score} | {terms} |")
        lines.append("")

    report_path = out_dir / "pilot-harness-governance.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    routes_json = {
        "built_at": _now_iso(),
        "cohorts": {
            "harness_spine": list(HARNESS_SPINE_IDS),
            "governance_set2_locked": list(GOVERNANCE_SET2_LOCKED_IDS),
        },
        "anchor_chat_id": anchor_chat,
        "routes": [
            {
                **asdict(r),
                "top_transcripts": [asdict(h) for h in r.top_transcripts],
            }
            for r in routes
        ],
    }
    routes_path = out_dir / "pilot-routes.json"
    routes_path.write_text(json.dumps(routes_json, indent=2) + "\n", encoding="utf-8")

    return {
        "ok": True,
        "plan_index_path": idx_path.relative_to(vault_root).as_posix(),
        "report_path": report_path.relative_to(vault_root).as_posix(),
        "routes_path": routes_path.relative_to(vault_root).as_posix(),
        "plan_count": index.get("plan_count"),
        "routed": len(routes),
        "transcript_root": str(troot),
    }
