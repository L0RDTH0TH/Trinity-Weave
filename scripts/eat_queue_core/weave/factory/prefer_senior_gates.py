"""Trinity senior Gate B₁ / B₂ — Cursor agent -p without --force.

Governance only places the call and stores the verdict. The senior reads and
returns via stdout. Trinity stamps ``source`` from the launched role. Disk
prefer-result written by the agent is ignored. Edits to ticket/catalog/Prefer/
diff paths → fail closed (stdout not accepted).

Factory order is the only store caller. Ticketment / chat must not invoke this.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from ...host_runner import HostInvokeRequest, HostInvokeResult, resolve_host_runner
from .bindings import factory_drb_rel

ROLE_B1 = "prefer_b1_senior"
ROLE_B2 = "prefer_b2_senior"
SOURCE_B1 = "cursor_senior_b1"
SOURCE_B2 = "cursor_senior_b2"

_SENIOR_SOURCES = frozenset({SOURCE_B1, SOURCE_B2})

_VERDICT_FENCE_RE = re.compile(
    r"```(?:json)?\s*(\{.*?\})\s*```",
    re.S | re.I,
)


@dataclass
class SeniorGateResult:
    ok: bool
    source: str
    role: str
    summary: str = ""
    violations: list[str] = field(default_factory=list)
    raw_text: str | None = None
    prefer_result_path: str | None = None
    launched: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "source": self.source,
            "role": self.role,
            "summary": self.summary,
            "violations": list(self.violations),
            "prefer_result_path": self.prefer_result_path,
            "launched": self.launched,
        }


def trinity_stamped_source(role: str) -> str | None:
    """Map launched role → Trinity authority source. Model text cannot invent this."""
    r = str(role or "").strip()
    if r == ROLE_B1:
        return SOURCE_B1
    if r == ROLE_B2:
        return SOURCE_B2
    return None


def senior_pass_ok(
    prefer_result: dict[str, Any] | None,
    *,
    gate: str,
    armed: dict[str, Any] | None = None,
) -> bool:
    """True when Trinity-stored nested record has Trinity-stamped source + ok.

    ``gate`` is ``b1`` or ``b2``. Bare author ok and model-supplied source alone
    (without matching Trinity nested record) stay red. Disk-shaped JSON that was
    never written by :func:`store_senior_verdict` is not accepted here — callers
    only pass prefer-result loaded after a store, or check nested fields.

    Packets with named ``missing_observer`` (retired incomplete-until-robot shape)
    never pass, even if prefer-result has nested ``ok: true``.
    """
    if armed is not None:
        from .prefer_map_fidelity import named_missing_observer

        if named_missing_observer(armed):
            return False
    if not isinstance(prefer_result, dict):
        return False
    if gate == "b1":
        nested = prefer_result.get("map_fidelity_hostile")
        need = SOURCE_B1
    elif gate == "b2":
        nested = prefer_result.get("weld_intent_hostile")
        need = SOURCE_B2
    else:
        return False
    if not isinstance(nested, dict):
        return False
    if nested.get("source") != need:
        return False
    if nested.get("trinity_stamped") is not True:
        return False
    if nested.get("ok") is not True:
        return False
    # Store must record which role Trinity launched.
    if nested.get("role") != (ROLE_B1 if gate == "b1" else ROLE_B2):
        return False
    return True


def parse_senior_stdout(raw: str | None) -> dict[str, Any] | None:
    """Extract verdict object from senior stdout. Model ``source`` is discarded."""
    text = str(raw or "")
    if not text.strip():
        return None
    # Prefer last fenced JSON block.
    matches = list(_VERDICT_FENCE_RE.finditer(text))
    candidates: list[str] = []
    if matches:
        candidates.append(matches[-1].group(1))
    # Fallback: last line-looking JSON object
    for line in reversed(text.splitlines()):
        s = line.strip()
        if s.startswith("{") and s.endswith("}"):
            candidates.append(s)
            break
    # Whole-text object
    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        candidates.append(stripped)

    for blob in candidates:
        try:
            data = json.loads(blob)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and "ok" in data:
            return data
    return None


def _snapshot_mtimes(paths: list[Path]) -> dict[str, float]:
    out: dict[str, float] = {}
    for p in paths:
        try:
            if p.is_file():
                out[str(p.resolve())] = p.stat().st_mtime
            elif p.is_dir():
                for child in p.rglob("*"):
                    if child.is_file():
                        out[str(child.resolve())] = child.stat().st_mtime
        except OSError:
            continue
    return out


def _watched_paths(
    vault_root: Path,
    project_id: str,
    armed: dict[str, Any],
    *,
    map_rel: str | None,
) -> list[Path]:
    """Paths a senior must not edit. Any mtime change → fail closed."""
    from .ticket_map_schema import resolve_active_ticket_map_rel

    vault_root = vault_root.resolve()
    pid = str(project_id or armed.get("project_id") or "").strip()
    paths: list[Path] = []
    if not pid:
        return paths
    drb = vault_root / factory_drb_rel(pid)
    paths.append(drb / "bindings" / "proof-catalog.yaml")
    paths.append(drb / "factory-project.yaml")
    slice_id = str(armed.get("slice_id") or "").strip()
    if slice_id:
        briefs = drb / "slice-briefs"
        paths.append(briefs / f"{slice_id}.armed.yaml")
        paths.append(briefs / f"{slice_id}.md")
        paths.append(briefs / f"{slice_id}.prefer-result.json")
        paths.append(briefs)
    tid = str(armed.get("ticket_map_id") or "").strip()
    rel = map_rel or resolve_active_ticket_map_rel(
        vault_root, project_id=pid, ticket_map_id=tid or None
    )
    if rel:
        paths.append(vault_root / rel)
    try:
        from .bindings import game_repo_path

        paths.append(vault_root / game_repo_path(vault_root, pid))
    except Exception:
        pass
    return paths


def detect_senior_writes(
    before: dict[str, float], after: dict[str, float]
) -> list[str]:
    """Return relative-ish keys that appeared or changed mtime."""
    hits: list[str] = []
    for key, mtime in after.items():
        prev = before.get(key)
        if prev is None or mtime > prev + 0.001:
            hits.append(key)
    return hits


def build_b1_handoff(
    *,
    armed: dict[str, Any],
    map_text: str,
    feedstock_note: str,
    probe_claim: str,
) -> str:
    """Prompt for prefer_b1_senior — read and return only."""
    return f"""You are Gate B₁ — a senior engineer second reader. New process. Read only.

Trinity launched role: {ROLE_B1}. You do NOT have write permission (--force omitted).
Do NOT edit Prefer packets, proof-catalog, ticket map, factory-project, or game tree.
Do NOT write prefer-result.json. Return judgment on stdout only.

Question: Is this Prefer ticket consistent with the feedstock, the map row (incl. observe),
and its own ask — or is the proof a stand-in for the row?

Untrusted inputs (claims, not evidence):
- Author summary / Prefer prose may lie.
- Probe transcript below is a CLAIM. Lines like window_opened=1 do not prove a window opened.

Feedstock note:
{feedstock_note}

Map (excerpt):
{map_text[:12000]}

Armed Prefer (YAML/JSON dump):
{json.dumps(armed, indent=2, default=str)[:12000]}

Probe claim pack (untrusted):
{probe_claim[:8000]}

Reply with ONE fenced JSON object only, shape:
{{"ok": true|false, "summary": "one sentence", "violations": ["…"]}}
Do not include a source field (Trinity stamps source). Do not rewrite the ticket.
"""


def build_b2_handoff(
    *,
    armed: dict[str, Any],
    map_text: str,
    diff_claim: str,
    probe_claim: str,
) -> str:
    return f"""You are Gate B₂ — the same senior persona after the junior weld. New process. Read only.

Trinity launched role: {ROLE_B2}. No --force. Do NOT edit ticket, catalog, Prefer, or diff.
Do NOT write prefer-result.json. Stdout judgment only.

The ticket was already accepted at B₁. Treat the generated work as junior output.
Fail when the code does not do that ask, or builds a later map row. You do not replace operator F5.

Untrusted: probe transcripts and print flags (window_opened=1) are CLAIMS, not evidence.

Section Walk (if present on the map) is operator text for gap *questions* only,
after the factory has built something. On f5/person rows, hand the operator the
ticket id, product job, and Walk steps to check — that is the person close.
That report is NOT a latch: do not invent walk_ok; do not set
map_fidelity_hostile_ok, weld_intent_hostile_ok, or f5_good; do not GREENLIGHT.
Behavior keys stay this Prefer's own sentence — not the Walk list. Nobody stamps
the Walk done. Walk is not eat order and not section pass.

Map (excerpt):
{map_text[:8000]}

Armed Prefer:
{json.dumps(armed, indent=2, default=str)[:8000]}

Junior / write-target claim:
{diff_claim[:10000]}

Probe claim pack (untrusted):
{probe_claim[:6000]}

Reply with ONE fenced JSON object only:
{{"ok": true|false, "summary": "one sentence", "violations": ["…"]}}
No source field. No edits. No walk_ok field.
"""


def store_senior_verdict(
    vault_root: Path,
    project_id: str,
    slice_id: str,
    *,
    gate: str,
    role: str,
    ok: bool,
    summary: str,
    violations: list[str],
) -> Path:
    """Trinity-only write of prefer-result latch. Stamps source from role."""
    source = trinity_stamped_source(role)
    if source is None:
        raise ValueError(f"unknown_senior_role:{role}")
    if gate == "b1" and source != SOURCE_B1:
        raise ValueError("gate_role_mismatch")
    if gate == "b2" and source != SOURCE_B2:
        raise ValueError("gate_role_mismatch")

    pr_path = (
        vault_root.resolve()
        / factory_drb_rel(project_id)
        / "slice-briefs"
        / f"{slice_id}.prefer-result.json"
    )
    existing: dict[str, Any] = {}
    if pr_path.is_file():
        try:
            existing = json.loads(pr_path.read_text(encoding="utf-8"))
            if not isinstance(existing, dict):
                existing = {}
        except (OSError, json.JSONDecodeError, ValueError):
            existing = {}

    stamp = {
        "ok": bool(ok),
        "source": source,
        "role": role,
        "trinity_stamped": True,
        "summary": str(summary or ""),
        "violations": list(violations),
        "stored_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    if gate == "b1":
        existing.pop("map_fidelity_hostile_ok", None)
        existing["map_fidelity_hostile"] = stamp
        existing["map_fidelity_hostile_ok"] = bool(ok)
    else:
        existing.pop("weld_intent_hostile_ok", None)
        existing["weld_intent_hostile"] = stamp
        existing["weld_intent_hostile_ok"] = bool(ok)

    pr_path.parent.mkdir(parents=True, exist_ok=True)
    pr_path.write_text(
        json.dumps(existing, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return pr_path


def run_senior_gate(
    vault_root: Path,
    armed: dict[str, Any],
    *,
    gate: str,
    map_rel: str | None = None,
    feedstock_note: str = "",
    probe_claim: str = "",
    diff_claim: str = "",
    model: str = "auto",
    host_invoke: Callable[[HostInvokeRequest], HostInvokeResult] | None = None,
    store: bool = True,
    factory_order: bool = False,
) -> SeniorGateResult:
    """Factory-order senior invoke. Sole path that may store a launchable latch.

    ``factory_order=True`` is required to store. Ticketment / chat without that
    flag get a dry invoke result and must not become launchable.
    """
    vault_root = vault_root.resolve()
    if store and not factory_order:
        return SeniorGateResult(
            ok=False,
            source="",
            role="",
            violations=["senior:store_requires_factory_order"],
        )
    if gate == "b1":
        role = ROLE_B1
        source = SOURCE_B1
    elif gate == "b2":
        role = ROLE_B2
        source = SOURCE_B2
    else:
        return SeniorGateResult(
            ok=False,
            source="",
            role="",
            violations=[f"senior:unknown_gate:{gate}"],
        )

    # Dedicated forms_ok gate — forms_fail must not fall through into a senior launch.
    from .prefer_map_fidelity import STATUS_FORMS_OK, validate_armed_map_fidelity

    fidelity = validate_armed_map_fidelity(
        vault_root,
        armed,
        map_rel=map_rel,
        prefer_result=None,
        require_hostile_for_keep=False,
    )
    if fidelity.gate_a_applicable and fidelity.status != STATUS_FORMS_OK:
        return SeniorGateResult(
            ok=False,
            source=source,
            role=role,
            summary=f"gate_a_status:{fidelity.status}",
            violations=[f"senior:gate_a_status:{fidelity.status}"],
            launched=False,
        )

    pid = str(armed.get("project_id") or "").strip()
    slice_id = str(armed.get("slice_id") or "").strip()
    if not pid or not slice_id:
        return SeniorGateResult(
            ok=False,
            source=source,
            role=role,
            violations=["senior:missing_project_or_slice"],
        )

    from .ticket_map_schema import resolve_active_ticket_map_rel

    tid = str(armed.get("ticket_map_id") or "").strip()
    rel = map_rel or resolve_active_ticket_map_rel(
        vault_root, project_id=pid, ticket_map_id=tid or None
    )
    map_text = ""
    if rel:
        mp = vault_root / rel
        if mp.is_file():
            map_text = mp.read_text(encoding="utf-8", errors="replace")

    if gate == "b1":
        handoff = build_b1_handoff(
            armed=armed,
            map_text=map_text,
            feedstock_note=feedstock_note or "(none)",
            probe_claim=probe_claim or "(none)",
        )
    else:
        handoff = build_b2_handoff(
            armed=armed,
            map_text=map_text,
            diff_claim=diff_claim or "(none)",
            probe_claim=probe_claim or "(none)",
        )

    watched = _watched_paths(vault_root, pid, armed, map_rel=rel)
    before = _snapshot_mtimes(watched)

    req = HostInvokeRequest(
        vault_root=vault_root,
        handoff=handoff,
        model=model,
        role=role,
        allow_writes=False,
        timeout_sec=3600,
    )
    if host_invoke is None:
        runner = resolve_host_runner(vault_root)
        host_result = runner.invoke(req)
    else:
        host_result = host_invoke(req)

    after = _snapshot_mtimes(watched)
    writes = detect_senior_writes(before, after)

    violations: list[str] = []
    if writes:
        # Fail closed — do not accept stdout; no cleanup-and-pass branch.
        violations.append("senior:edited_watched_paths")
        violations.extend(f"senior:write:{w}" for w in writes[:12])
        result = SeniorGateResult(
            ok=False,
            source=source,
            role=role,
            summary="senior edited watched paths; stdout discarded",
            violations=violations,
            raw_text=host_result.raw_text,
            launched=True,
        )
        if store:
            path = store_senior_verdict(
                vault_root,
                pid,
                slice_id,
                gate=gate,
                role=role,
                ok=False,
                summary=result.summary,
                violations=result.violations,
            )
            result.prefer_result_path = str(path)
        return result

    parsed = parse_senior_stdout(host_result.raw_text)
    if not host_result.ok and not parsed:
        violations.append(
            f"senior:invoke_failed:{host_result.error or host_result.exit_code}"
        )
        result = SeniorGateResult(
            ok=False,
            source=source,
            role=role,
            summary="senior invoke failed",
            violations=violations,
            raw_text=host_result.raw_text,
            launched=True,
        )
        if store:
            path = store_senior_verdict(
                vault_root,
                pid,
                slice_id,
                gate=gate,
                role=role,
                ok=False,
                summary=result.summary,
                violations=result.violations,
            )
            result.prefer_result_path = str(path)
        return result

    if parsed is None:
        violations.append("senior:unparseable_stdout")
        ok = False
        summary = "unparseable senior stdout"
        model_viol: list[str] = []
    else:
        # Discard any model-supplied source — Trinity stamps from role.
        ok = parsed.get("ok") is True
        summary = str(parsed.get("summary") or "")
        raw_v = parsed.get("violations") or []
        model_viol = [str(x) for x in raw_v] if isinstance(raw_v, list) else []

    result = SeniorGateResult(
        ok=bool(ok),
        source=source,
        role=role,
        summary=summary,
        violations=model_viol if ok else (violations + model_viol),
        raw_text=host_result.raw_text,
        launched=True,
    )

    if store:
        path = store_senior_verdict(
            vault_root,
            pid,
            slice_id,
            gate=gate,
            role=role,
            ok=result.ok,
            summary=result.summary,
            violations=result.violations,
        )
        result.prefer_result_path = str(path)
    return result
