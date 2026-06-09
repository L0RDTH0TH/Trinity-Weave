"""Conceptual-leg authoring doctrine — experiential voice, anti-meta guard.

Synthesis infers human purpose from Touch/Rules internally but must **not**
name them in outcome/summary/primary_case. Gold style: harness_headless_eat,
harness_snapshot (user-centered, vivid, no Trinity-framework commentary).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .trinity_card import get_conceptual
from .trinity_harness_backfill import _module_docstring, _read_text

# Experiential gold first (manual validations); governance/meta cards last.
DEFAULT_GOLD_EXAMPLE_IDS: tuple[str, ...] = (
    "harness_headless_eat",
    "harness_snapshot",
    "little_val_structural",
    "weave_governance",
    "skill_gap",
)

STYLE_GUIDE_LOCKED_REL = ".technical/weave/components/conceptual_style_guide.yaml"
STYLE_GUIDE_STUB_REL = (
    ".technical/weave/proposals/governance-set-v1/stubs/conceptual_style_guide.yaml"
)
AUTHORING_STUB_REL = (
    ".technical/weave/proposals/governance-set-v1/stubs/trinity_card_authoring.yaml"
)

# Machine / pipeline voice.
FORBIDDEN_MACHINE_PHRASES: tuple[str, ...] = (
    "Backward extrapolation",
    "backward extrapolation",
    "spine cascade",
    "Conceptual spine cascade",
    "validated corpus",
    "harness backfill",
    "trinity_spine_cascade",
    "trinity_conceptual_regen",
    "forward-grow conceptual",
    "stub_pass first",
)

# Meta-governance voice (framework explains itself instead of human story).
FORBIDDEN_META_TERMS: tuple[str, ...] = (
    "touch",
    "rules",
    "trinity",
    "blast radius",
    "blast-radius",
    "weave segment",
    "this card",
    "the card",
    "llm",
    "primary path",
    "primary paths",
    "conceptual section",
    "conceptual leg",
    "non-technical reviewer",
    "human-facing story",
    "doctrinal",
    "meta.source",
    "pairs_with",
    "forbidden list",
    "inbound",
    "outbound",
    "behavior_signals",
)

_META_TERM_RE = re.compile(
    r"\b(" + "|".join(re.escape(t) for t in FORBIDDEN_META_TERMS) + r")\b",
    re.IGNORECASE,
)

_MACHINE_RE = re.compile(
    r"(" + "|".join(re.escape(p) for p in FORBIDDEN_MACHINE_PHRASES) + r")",
    re.IGNORECASE,
)


def _conceptual_blob(card: dict[str, Any], *, fields: tuple[str, ...] = ("outcome", "summary", "primary_case")) -> str:
    conceptual = get_conceptual(card)
    return " ".join(str(conceptual.get(k) or "") for k in fields)


def conceptual_has_machine_voice(card: dict[str, Any]) -> bool:
    return bool(_MACHINE_RE.search(_conceptual_blob(card)))


def conceptual_has_meta_contamination(card: dict[str, Any]) -> bool:
    """Meta-governance tone in the human narrative fields."""
    return bool(_META_TERM_RE.search(_conceptual_blob(card)))


def conceptual_needs_experiential_rewrite(card: dict[str, Any]) -> bool:
    return conceptual_has_machine_voice(card) or conceptual_has_meta_contamination(card)


def pick_gold_examples(
    corpus: dict[str, dict[str, Any]],
    *,
    prefer_ids: tuple[str, ...] = DEFAULT_GOLD_EXAMPLE_IDS,
    limit: int = 5,
) -> list[tuple[str, dict[str, Any]]]:
    out: list[tuple[str, dict[str, Any]]] = []
    for tid in prefer_ids:
        if tid in corpus:
            out.append((tid, corpus[tid]))
    if len(out) >= limit:
        return out[:limit]
    for tid in sorted(corpus.keys()):
        if tid in {x[0] for x in out}:
            continue
        c = corpus[tid]
        if c.get("outcome") and c.get("summary") and len(str(c.get("summary"))) > 60:
            if not _META_TERM_RE.search(
                " ".join(str(c.get(k) or "") for k in ("outcome", "summary", "primary_case"))
            ):
                out.append((tid, c))
        if len(out) >= limit:
            break
    return out[:limit]


def _readable_name(trinity_id: str) -> str:
    s = trinity_id.replace("harness_", "").replace("_", " ").strip()
    return s or trinity_id


def _touch_rules_context(card: dict[str, Any]) -> dict[str, Any]:
    """Internal inference only — never echoed into conceptual prose."""
    touch = card.get("touch") if isinstance(card.get("touch"), dict) else {}
    rules = card.get("rules") if isinstance(card.get("rules"), dict) else {}
    primary = touch.get("primary_paths") if isinstance(touch.get("primary_paths"), list) else []
    qmodes = touch.get("queue_modes") if isinstance(touch.get("queue_modes"), list) else []
    forbidden = rules.get("forbidden") if isinstance(rules.get("forbidden"), list) else []
    return {
        "has_paths": bool(primary),
        "queue_modes": [str(m).strip() for m in qmodes if str(m).strip()][:4],
        "forbidden_count": len(forbidden),
        "is_harness": str(card.get("id") or "").startswith("harness_"),
        "is_lane": any(x in str(card.get("id") or "") for x in ("lane", "board", "registry")),
        "is_snapshot": "snapshot" in str(card.get("id") or ""),
        "is_governance": any(x in str(card.get("id") or "") for x in ("governance", "invariant", "policy")),
        "is_ghost_skill": any(x in str(card.get("id") or "") for x in ("ghost", "skill_gap")),
        "is_repair": any(x in str(card.get("id") or "") for x in ("heal", "repair", "recover")),
    }


def _module_grounding(vault_root: Path, primary_paths: list[Any]) -> str:
    for raw in primary_paths:
        rel = str(raw).strip().split("#")[0]
        if not rel.endswith(".py"):
            continue
        full = vault_root / rel
        if not full.is_file():
            continue
        doc = _module_docstring(_read_text(full))
        if doc:
            return doc[:200].rstrip(".")
    return ""


def _story_beats(trinity_id: str, ctx: dict[str, Any], ground: str) -> dict[str, str]:
    """Human story beats — no framework vocabulary."""
    name = _readable_name(trinity_id)

    if trinity_id == "harness_headless_eat" or (ctx["is_harness"] and "eat" in trinity_id):
        return {
            "outcome": (
                "Pipeline work on one lane can run while you stay free — other chats, other tasks — "
                "without one long batch holding your attention hostage."
            ),
            "summary": (
                f"{name.title()} is delegation: you line up work, start background execution for that lane, "
                "and walk away. The vault keeps cooking; you check receipts when you care, not by blocking in one chat until everything finishes."
            ),
            "primary_case": (
                "You have ingest, roadmap, or distill work queued on a lane. You kick off background processing "
                "for that lane only and keep designing, crafting prompts, or operating elsewhere."
            ),
        }

    if ctx["is_snapshot"] or trinity_id == "harness_snapshot":
        return {
            "outcome": (
                "Before anything important changes on disk, you get a deterministic before picture — "
                "so recovery is evidence, not guesswork."
            ),
            "summary": (
                f"{name.title()} is the save point right before risky work: what the bytes looked like, "
                "hashed and recorded. Not only for queues — any file you are about to rewrite deserves that receipt first. "
                "If power dies, sync fights, or a write stops halfway, you still know what 'before' was."
            ),
            "primary_case": (
                "A pass is about to rewrite or append files. You capture each target first. "
                "Mid-pass something fails — crash, I/O, another actor touched the same path. "
                "You realign from the before receipt instead of debating what might have been there."
            ),
        }

    if ctx["is_harness"]:
        step = name
        return {
            "outcome": (
                f"When {step} runs, you get a clear receipt of what happened — "
                f"so you are not left wondering whether the vault actually did the step."
            ),
            "summary": (
                f"This harness step is part of unattended maintenance: it runs in the background, "
                f"logs what it touched, and lets you verify later instead of watching every line scroll by."
            ),
            "primary_case": (
                f"You triggered or scheduled {step} on a lane. You move on; when you return, "
                f"the receipt tells you success, skip, or failure without re-running the whole pass."
            ),
        }

    if ctx["is_lane"]:
        return {
            "outcome": (
                "You see what each lane is actually doing — not a story invented from stale files or hopeful inference."
            ),
            "summary": (
                f"{name.title()} keeps lane truth on the board: activity, receipts, and status that match reality. "
                "When something looks green, it earned green; when it stalled, you see stall — not a silent lie."
            ),
            "primary_case": (
                "You open the maintenance board before deciding what to queue next. "
                "Lane rows match what last ran and what is still waiting — you trust the picture enough to act."
            ),
        }

    if ctx["is_governance"]:
        return {
            "outcome": (
                "Decisions and board context from last time are still there when you come back — "
                "so the next pass does not start from amnesia."
            ),
            "summary": (
                f"{name.title()} is operational memory: what was reviewed, what the board showed, "
                "what signals fired. It is not the repair engine itself — it is continuity so your next move "
                "builds on what actually happened."
            ),
            "primary_case": (
                "A maintenance or recovery cycle just finished. The record is durable. "
                "The next person (or next night's run) reads it before acting — anchored to facts, not vibes."
            ),
        }

    if ctx["is_ghost_skill"]:
        return {
            "outcome": (
                "Repeating gaps become a reusable overnight recipe — without mixing up "
                "'propose a fix' and 'audit whether the fix is safe'."
            ),
            "summary": (
                f"{name.title()} handles the propose side: scan what keeps failing, draft a small skill-shaped recipe, "
                "park it for review. Production skills stay yours to promote; unattended runs get stability, not surprise writes."
            ),
            "primary_case": (
                "You are away from the keyboard. A gap line appears again in lane memory. "
                "A proposal stub lands in the proposals folder — ready for audit and promotion when you return."
            ),
        }

    if ctx["is_repair"]:
        return {
            "outcome": (
                "When something breaks mid-pass, recovery has a playbook — "
                "you are not improvising under pressure with half the context."
            ),
            "summary": (
                f"{name.title()} is the cool-headed path after failure: what to retry, what to skip, "
                "what must never be auto-fixed. You get structure instead of a louder error message."
            ),
            "primary_case": (
                "A lane run failed or partially applied. You open the recovery flow — "
                "it tells you what is safe to retry and what needs your eyes first."
            ),
        }

    # Generic — still experiential; ground informs subject not vocabulary.
    subject = ground.split(".")[0][:100] if ground else name
    pain = "guessing from logs alone"
    if ctx["forbidden_count"] > 3:
        pain = "silent corruption or over-eager auto-fixes"
    elif ctx["queue_modes"]:
        pain = "queueing work you cannot explain to a teammate"

    return {
        "outcome": (
            f"You get a dependable outcome from {subject.lower()} — without {pain}."
        ),
        "summary": (
            f"{name.title()} exists so everyday operation stays understandable: what it protects, "
            f"when it runs, and what 'done' feels like for someone who does not read the implementation. "
            f"{subject.rstrip('.')}."
        ),
        "primary_case": (
            f"You are about to rely on {name}. You should know within a minute why it matters, "
            f"what good looks like, and what would be a dangerous misunderstanding — in plain language."
        ),
    }


def _sanitize_prose(text: str) -> str:
    """Strip accidental framework words from narrative fields."""
    out = text
    for term in FORBIDDEN_META_TERMS:
        out = re.sub(rf"\b{re.escape(term)}\b", "", out, flags=re.IGNORECASE)
    out = re.sub(r"\s{2,}", " ", out)
    out = re.sub(r"\s+([,.])", r"\1", out)
    return out.strip()


def _dedupe_str_list(items: list[str], *, limit: int = 8) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        s = str(item).strip()
        if not s or s in seen:
            continue
        seen.add(s)
        out.append(s)
        if len(out) >= limit:
            break
    return out


def _default_edge_cases(trinity_id: str) -> list[str]:
    return _dedupe_str_list(
        [
            "Session or plan id pasted into narrative — must stand alone for batch generation.",
            "Outcome reads like a module docstring — busy operators skim past it.",
            f"Treating { _readable_name(trinity_id) } as optional when the maintenance board says it is due.",
        ],
        limit=5,
    )


def _default_misread_risks() -> list[str]:
    return _dedupe_str_list(
        [
            "Writing about the documentation system instead of what the person gains.",
            "Copying implementation vocabulary into the outcome line.",
            "Locking narrative before a human read-through — story drifts from reality.",
        ],
        limit=6,
    )


def synthesize_conceptual_human_vantage(
    vault_root: Path,
    trinity_id: str,
    card: dict[str, Any],
    neighbor_ids: list[str],
    corpus: dict[str, dict[str, Any]],
    *,
    gold_examples: list[tuple[str, dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """Experiential Conceptual — infer from Touch/Rules internally; never name them in prose."""
    old = get_conceptual(card)
    touch = card.get("touch") if isinstance(card.get("touch"), dict) else {}
    primary_paths = touch.get("primary_paths") if isinstance(touch.get("primary_paths"), list) else []
    ctx = _touch_rules_context(card)
    ground = _module_grounding(vault_root, primary_paths)

    beats = _story_beats(trinity_id, ctx, ground)
    outcome = _sanitize_prose(beats["outcome"])[:500]
    summary = _sanitize_prose(beats["summary"])[:950]
    primary_case = _sanitize_prose(beats["primary_case"])[:900]

    polar = str(old.get("polar_pair") or "").strip()
    pairs_raw = old.get("pairs_with")
    pairs: list[str] = []
    if isinstance(pairs_raw, list):
        for item in pairs_raw:
            s = str(item).strip()
            if not s:
                continue
            token = re.split(r"\s+[—–-]\s+", s, maxsplit=1)[0].strip()
            if token:
                pairs.append(token)

    edge_cases: list[str] = list(_default_edge_cases(trinity_id))
    for nid in neighbor_ids[:2]:
        n = corpus.get(nid) or {}
        for ec in n.get("edge_cases") or []:
            if isinstance(ec, str) and not _META_TERM_RE.search(ec):
                edge_cases.append(ec)
    edge_cases = _dedupe_str_list(edge_cases, limit=6)

    misread_risks: list[str] = list(_default_misread_risks())
    for nid in neighbor_ids[:2]:
        n = corpus.get(nid) or {}
        for mr in n.get("misread_risks") or []:
            if isinstance(mr, str) and not _META_TERM_RE.search(mr):
                misread_risks.append(mr)
    misread_risks = _dedupe_str_list(misread_risks, limit=8)

    new_conceptual: dict[str, Any] = dict(old)
    new_conceptual["outcome"] = outcome
    new_conceptual["summary"] = summary
    new_conceptual["primary_case"] = primary_case
    new_conceptual["edge_cases"] = edge_cases
    new_conceptual["misread_risks"] = misread_risks
    if pairs:
        new_conceptual["pairs_with"] = pairs
    if polar:
        new_conceptual["polar_pair"] = polar
    for key in ("spine_ordinal", "set", "operator_memory_hook", "refs"):
        if old.get(key) is not None:
            new_conceptual[key] = old[key]
    return new_conceptual


def build_conceptual_regen_pack_markdown(
    vault_root: Path,
    trinity_id: str,
    card: dict[str, Any],
    neighbor_ids: list[str],
    corpus: dict[str, dict[str, Any]],
    *,
    gold_examples: list[tuple[str, dict[str, Any]]] | None = None,
) -> str:
    """Cursor hand-off — strict anti-meta prompt + full gold excerpts."""
    import yaml

    gold = gold_examples or pick_gold_examples(corpus)
    lines = [
        f"# Conceptual regen pack — `{trinity_id}`",
        "",
        "Write **only** the `conceptual:` block (`outcome`, `summary`, `primary_case`, "
        "optional `frame_anchor` per style guide, `edge_cases`, `misread_risks`). "
        "Do **not** change Touch or Rules.",
        "",
        "## STRICT STYLE (do not break)",
        "",
        "- **outcome:** one-line **claim** only (human problem solved; \"so that …\" OK) — **no story**, no scene.",
        "- **summary:** **principle + constraints** only (1–2 tight paragraphs) — **no user vignette**, no walkthrough.",
        "- **primary_case:** **only** field with user story / skim test — warm second-person or short scenario OK here.",
        "- **frame_anchor** (optional): one-line lens per `conceptual_style_guide` — meta/bridge may use; component cards usually omit.",
        "- **Never** in outcome/summary/primary_case: Touch, Rules, Trinity, weave segment, card, LLM, agent, blast radius, primary paths, Conceptual leg, inbound/outbound.",
        "- **Never** explain the card system, documentation framework, or what a \"segment\" is.",
        "- Infer purpose from Touch/Rules below — **do not reference them in your writing**.",
        "- Locked `conceptual_style_guide` field_contract governs; see anti_meta + field_contract on that card.",
        "",
        "## Gold manual examples (match tone — do not copy verbatim)",
        "",
    ]
    for gid, gcon in gold[:5]:
        lines.append(f"### `{gid}`")
        for field in ("outcome", "summary", "primary_case"):
            val = str(gcon.get(field) or "").strip()
            if val:
                lines.append(f"**{field}:** {val[:600]}")
        lines.append("")

    from .trinity_prompt_context_slice import resolve_prompt_context

    pull = resolve_prompt_context(
        vault_root, trinity_id, "conceptual_regen", prefer="provisional"
    )
    lines.extend(
        [
            "## Pull context (11b — read-only; infer purpose, do not cite)",
            f"- **write_scope:** `{pull.write_scope}`",
            f"- **meta_prepend:** {', '.join(f'`{m}`' for m in pull.meta_prepend)}",
            "```yaml",
            yaml.dump(pull.legs, default_flow_style=False).strip(),
            "```",
            "",
            "## Draft to replace",
            "```yaml",
            yaml.dump(get_conceptual(card), default_flow_style=False).strip(),
            "```",
            "",
            "## Self-check before you finish",
            "- [ ] Zero meta-framework words in outcome/summary/primary_case",
            "- [ ] Would a busy operator understand why this exists?",
            "- [ ] Could you read outcome aloud without sounding like internal docs?",
            "",
            "## Output",
            "YAML mapping for `conceptual:` only.",
        ]
    )
    return "\n".join(lines)


def load_style_guide(vault_root: Path) -> dict[str, Any] | None:
    """Locked components card first, then governance stub fallback."""
    import yaml

    for rel in (STYLE_GUIDE_LOCKED_REL, STYLE_GUIDE_STUB_REL):
        path = vault_root / rel
        if not path.is_file():
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except (OSError, ValueError, yaml.YAMLError):
            continue
    try:
        from .trinity_card import load_trinity_card

        return load_trinity_card(vault_root, "conceptual_style_guide", prefer="locked")
    except (FileNotFoundError, OSError, ValueError, yaml.YAMLError):
        return None
