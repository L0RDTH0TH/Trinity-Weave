"""Gate B₂ — weld intent hostile (post-weld).

Prefer Success is the painting brief. LIVE mechanics must be brush strokes for
that picture — not another picture that shares labels.

Not Gate A (mechanical MAP shape). Not Gate B₁ Prefer hostile
(``map_fidelity_hostile_ok``). B₂ asks: after GREENLIGHT → weld LIVE, does
Play-path behavior keep Prefer Success + refuses?

Grok guards (binding):

1. **Logs cannot acquit.** Proof tags / factory logs / receipt KEEP headers may
   **indict** only. They must **not** pass B₂. Passing evidence = behavior.
2. **Latch sees skipped-factory welds.** Staging Success / ready-for-F5 / KEEP /
   ask_success without ``weld_intent_hostile_ok`` when LIVE weld is claimed (or
   receipt claims success / greenlit) = hard fail — including chat receipts that
   never called the pipeline. Skip only explicit ``factory_bypass`` + operator
   ack; bypass receipt must **never** say greenlit.
3. **B₂ does not edit the picture.** Validator must not rewrite Prefer Success
   to fit what shipped. Prefer-lie is an operator call.

Cite: Prefer-Authorship-Host-Law §C.3 B₂ · Prefer-Map-Fidelity-Automation-Plan.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# Claim altitudes that count as Success / ready-for-F5 / KEEP (need B₂ when welded).
_SUCCESS_CLAIM_CLASSES: frozenset[str] = frozenset(
    {
        "ask_success",
        "keep",
        "keep_real",
        "success",
        "staging",
        "staging_awaiting_f5",
        "staging_incomplete",
        "ready_for_f5",
        "",
    }
)

# Tags / log markers that indict piggyback / wording-minimal place — never pass.
PIGGYBACK_INDICT_TAGS: frozenset[str] = frozenset(
    {
        "piggyback_place_v1",
        "piggyback_place",
        "piggyback_skip_update_four",
        "update_four_false_on_lmb_place",
        "seat_polygon_as_place_success",
        "cull_mode_as_place_success",
    }
)

# PLACE-product behavior checklist keys (honest place-shaped fixture).
PLACE_BEHAVIOR_KEYS: tuple[str, ...] = (
    "same_seat_ghost_eq_commit",
    "update_four_ran",
    "coast_gate_ran",
    "full_survives_neighbor_rebuild",
    "prefer_refuses_not_violated_in_live",
)

# Evidence modes that must never count as pass.
_FORBIDDEN_PASS_MODES: frozenset[str] = frozenset(
    {
        "proof_tag",
        "proof_tags",
        "factory_log",
        "factory_logs",
        "keep_header",
        "receipt_header",
        "string_match",
        "prefer_word_method_name_match",
        "ast_match",
        "compiles",
        "gate_a",
        "verify_mcp_only",
        "mcp_only",
    }
)


@dataclass
class WeldIntentResult:
    ok: bool
    violations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    applicable: bool = False
    live_weld_claimed: bool = False
    bypass: bool = False
    evidence_pack: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "applicable": self.applicable,
            "live_weld_claimed": self.live_weld_claimed,
            "bypass": self.bypass,
            "violations": list(self.violations),
            "warnings": list(self.warnings),
            "evidence_pack": dict(self.evidence_pack) if self.evidence_pack else {},
        }


def weld_intent_hostile_ok(prefer_result: dict[str, Any] | None) -> bool:
    """True only when Gate B₂ stamped ``weld_intent_hostile_ok: true``."""
    if not isinstance(prefer_result, dict):
        return False
    if prefer_result.get("weld_intent_hostile_ok") is True:
        return True
    nested = prefer_result.get("weld_intent_hostile")
    return isinstance(nested, dict) and nested.get("ok") is True


def is_factory_bypass(armed: dict[str, Any] | None, receipt: dict[str, Any] | None = None) -> bool:
    """Explicit factory_bypass + no greenlit claim."""
    for blob in (armed, receipt):
        if isinstance(blob, dict) and blob.get("factory_bypass") is True:
            return True
    return False


def claims_factory_greenlit(
    armed: dict[str, Any] | None,
    prefer_result: dict[str, Any] | None = None,
    receipt: dict[str, Any] | None = None,
) -> bool:
    for blob in (armed, prefer_result, receipt):
        if isinstance(blob, dict) and blob.get("factory_greenlit") is True:
            return True
    return False


def live_weld_claimed(
    armed: dict[str, Any] | None,
    prefer_result: dict[str, Any] | None = None,
    receipt: dict[str, Any] | None = None,
) -> bool:
    """LIVE weld claimed — landed flag, greenlit, or receipt success after weld."""
    for blob in (armed, prefer_result, receipt):
        if not isinstance(blob, dict):
            continue
        if blob.get("live_weld_landed") is True:
            return True
        if blob.get("live_weld_greenlit") is True:
            return True
        if blob.get("weld_live") is True:
            return True
        if str(blob.get("disposition") or "").strip().lower() in {
            "welded",
            "live_welded",
            "awaiting_f5_after_weld",
            "ready_for_f5",
        }:
            return True
    # Greenlit without explicit landed still claims weld path for latch purposes.
    if claims_factory_greenlit(armed, prefer_result, receipt):
        return True
    return False


def success_altitude_claimed(
    armed: dict[str, Any] | None,
    prefer_result: dict[str, Any] | None = None,
    receipt: dict[str, Any] | None = None,
) -> bool:
    """Staging Success / ready-for-F5 / KEEP / ask_success altitude."""
    for blob in (armed, prefer_result, receipt):
        if not isinstance(blob, dict):
            continue
        claim = str(blob.get("claim_class") or "").strip().lower()
        if claim in _SUCCESS_CLAIM_CLASSES and claim != "staging_incomplete":
            # Empty claim_class alone is not enough without other success markers.
            if claim == "" and not (
                blob.get("keep")
                or blob.get("ask_success")
                or blob.get("ready_for_f5")
                or blob.get("product_success")
            ):
                continue
            if claim or blob.get("keep") or blob.get("ask_success"):
                return True
        if blob.get("keep") is True or blob.get("ask_success") is True:
            return True
        if blob.get("ready_for_f5") is True or blob.get("product_success") is True:
            return True
        disp = str(blob.get("disposition") or "").strip().lower()
        if disp in {
            "keep",
            "ask_success",
            "ready_for_f5",
            "staging_awaiting_f5",
            "success",
        }:
            return True
    return False


def requires_weld_intent_hostile(
    armed: dict[str, Any] | None,
    prefer_result: dict[str, Any] | None = None,
    receipt: dict[str, Any] | None = None,
) -> bool:
    """B₂ applies when LIVE weld / greenlit / success altitude is claimed (unless bypass)."""
    if is_factory_bypass(armed, receipt) and not claims_factory_greenlit(
        armed, prefer_result, receipt
    ):
        return False
    return live_weld_claimed(armed, prefer_result, receipt) or (
        success_altitude_claimed(armed, prefer_result, receipt)
        and (
            live_weld_claimed(armed, prefer_result, receipt)
            or claims_factory_greenlit(armed, prefer_result, receipt)
        )
    )


def build_evidence_pack(
    *,
    prefer_success: str = "",
    prefer_refuses: list[str] | None = None,
    files_touched: list[str] | None = None,
    proof_tags: list[str] | None = None,
    factory_log_excerpts: list[str] | None = None,
    keep_headers: list[str] | None = None,
    behavior: dict[str, Any] | None = None,
    pass_basis: str = "",
    string_match_hits: list[str] | None = None,
    mcp_attest_only: bool = False,
    notes: str = "",
) -> dict[str, Any]:
    """Build B₂ evidence pack. Tags/logs/KEEP headers are **indictment-only**.

    Document for operators / validators: ``tags_are_not_pass_evidence: true``.
    Passing evidence must live under ``behavior`` with ``pass_basis: behavior``.
    """
    return {
        "prefer_success": prefer_success or "",
        "prefer_refuses": list(prefer_refuses or []),
        "files_touched": list(files_touched or []),
        "indictment_only": {
            "proof_tags": list(proof_tags or []),
            "factory_log_excerpts": list(factory_log_excerpts or []),
            "keep_headers": list(keep_headers or []),
            "note": "Logs/tags/KEEP headers may indict only; they cannot pass Gate B₂.",
        },
        "tags_are_not_pass_evidence": True,
        "behavior": dict(behavior or {}),
        "pass_basis": (pass_basis or "").strip().lower(),
        "string_match_hits": list(string_match_hits or []),
        "mcp_attest_only": bool(mcp_attest_only),
        "notes": notes or "",
        "b2_must_not_rewrite_prefer_success": True,
    }


def _collect_indict_tags(pack: dict[str, Any]) -> set[str]:
    indict = pack.get("indictment_only") if isinstance(pack.get("indictment_only"), dict) else {}
    tags = indict.get("proof_tags") or pack.get("proof_tags") or []
    out: set[str] = set()
    for t in tags:
        out.add(str(t).strip().lower())
    return out


def evaluate_behavior_evidence(pack: dict[str, Any] | None) -> WeldIntentResult:
    """Mechanical fail-closed checks on an evidence pack (no Prefer rewrite).

    Honest place-shaped behavior can pass this seat; piggyback / string-match /
    tag-as-pass / MCP-only cannot. Hostile LLM (skill) still stamps
    ``weld_intent_hostile_ok`` for the full rubric.
    """
    if not isinstance(pack, dict) or not pack:
        return WeldIntentResult(
            ok=False,
            applicable=True,
            violations=["weld_intent:missing_evidence_pack"],
        )

    violations: list[str] = []
    warnings: list[str] = []

    pass_basis = str(pack.get("pass_basis") or "").strip().lower()
    if pass_basis in _FORBIDDEN_PASS_MODES:
        violations.append(f"weld_intent:forbidden_pass_basis:{pass_basis}")

    if pack.get("mcp_attest_only") is True or pass_basis in {"verify_mcp_only", "mcp_only"}:
        violations.append("weld_intent:verify_mcp_only_refuse")

    string_hits = pack.get("string_match_hits") or []
    if string_hits and pass_basis in {
        "string_match",
        "prefer_word_method_name_match",
        "ast_match",
        "",
    }:
        # Prefer-word → method-name string match as pass = B₂ fail.
        violations.append("weld_intent:string_match_as_pass")

    if pass_basis in {"", "proof_tag", "factory_log", "keep_header"} and not pack.get(
        "behavior"
    ):
        violations.append("weld_intent:no_behavior_evidence")

    tags = _collect_indict_tags(pack)
    piggy = tags & PIGGYBACK_INDICT_TAGS
    if piggy:
        # Guard 1: tag saying Success / KEEP cannot acquit — piggyback indicts.
        violations.append(
            "weld_intent:piggyback_indict:" + ",".join(sorted(piggy))
        )

    behavior = pack.get("behavior") if isinstance(pack.get("behavior"), dict) else {}
    # Piggyback-shaped LIVE: update_four / coast skipped, or ghost≠commit.
    if behavior.get("update_four_ran") is False:
        violations.append("weld_intent:update_four_skipped")
    if behavior.get("coast_gate_ran") is False:
        violations.append("weld_intent:coast_gate_skipped")
    if behavior.get("same_seat_ghost_eq_commit") is False:
        violations.append("weld_intent:ghost_seat_neq_commit")
    if behavior.get("full_survives_neighbor_rebuild") is False:
        violations.append("weld_intent:neighbor_rebuild_deletes_full")
    if behavior.get("prefer_refuses_not_violated_in_live") is False:
        violations.append("weld_intent:prefer_refuse_violated_in_live")

    # Logs claiming Success while behavior missing/false — cannot acquit.
    indict = pack.get("indictment_only") if isinstance(pack.get("indictment_only"), dict) else {}
    log_excerpts = indict.get("factory_log_excerpts") or []
    keep_headers = indict.get("keep_headers") or []
    log_claims_success = any(
        re.search(r"\b(success|keep|ask_success)\b", str(x), re.I) for x in log_excerpts
    ) or any(re.search(r"\bkeep\b", str(x), re.I) for x in keep_headers)
    if log_claims_success and (
        not behavior
        or any(behavior.get(k) is False for k in PLACE_BEHAVIOR_KEYS)
        or piggy
    ):
        violations.append("weld_intent:logs_cannot_acquit")

    # Honest place-shaped: all behavior keys true + pass_basis behavior → mechanical ok.
    if (
        not violations
        and pass_basis == "behavior"
        and behavior
        and all(behavior.get(k) is True for k in PLACE_BEHAVIOR_KEYS)
    ):
        return WeldIntentResult(
            ok=True,
            applicable=True,
            evidence_pack=pack,
            warnings=warnings,
        )

    if not violations and pass_basis == "behavior" and behavior:
        # Partial behavior without full place checklist — still need hostile stamp;
        # mechanical seat allows non-place packs when no fail codes fired.
        return WeldIntentResult(
            ok=True,
            applicable=True,
            evidence_pack=pack,
            warnings=warnings,
        )

    if not violations and not behavior:
        violations.append("weld_intent:no_behavior_evidence")

    return WeldIntentResult(
        ok=not violations,
        applicable=True,
        violations=sorted(set(violations)),
        warnings=sorted(set(warnings)),
        evidence_pack=pack,
    )


def validate_weld_intent_latch(
    armed: dict[str, Any] | None,
    *,
    prefer_result: dict[str, Any] | None = None,
    receipt: dict[str, Any] | None = None,
    evidence_pack: dict[str, Any] | None = None,
) -> WeldIntentResult:
    """Refuse Success / ready-for-F5 / KEEP / greenlit without B₂ when weld claimed.

    Bypass without greenlit is allowed (skip). Bypass + greenlit = hard fail.
    Does **not** rewrite Prefer Success fields.
    """
    bypass = is_factory_bypass(armed, receipt)
    greenlit = claims_factory_greenlit(armed, prefer_result, receipt)
    welded = live_weld_claimed(armed, prefer_result, receipt)
    success = success_altitude_claimed(armed, prefer_result, receipt)

    violations: list[str] = []
    warnings: list[str] = []

    if bypass and greenlit:
        violations.append("weld_intent:bypass_must_not_claim_greenlit")

    if bypass and not greenlit:
        return WeldIntentResult(
            ok=True,
            applicable=False,
            bypass=True,
            live_weld_claimed=welded,
            warnings=["weld_intent:factory_bypass_skips_b2"],
        )

    # Guard 2: latch only when LIVE weld or greenlit is claimed (post-weld seat).
    # Prefer draft / unwelded staging (e.g. PLACE awaiting B₁) → not applicable.
    needs = bool(welded or greenlit)
    if not needs:
        return WeldIntentResult(
            ok=True, applicable=False, live_weld_claimed=False, bypass=bypass
        )

    # Staging Success / ready-for-F5 / KEEP / greenlit without B₂ when welded.
    if (success or greenlit) and not weld_intent_hostile_ok(prefer_result):
        violations.append("weld_intent:hostile_required_before_success")
    if greenlit and not weld_intent_hostile_ok(prefer_result):
        if "weld_intent:hostile_required_before_success" not in violations:
            violations.append("weld_intent:greenlit_without_b2")
        elif "weld_intent:greenlit_without_b2" not in violations:
            # Greenlit path also tagged for scanners / Watcher join.
            violations.append("weld_intent:greenlit_without_b2")

    pack = evidence_pack
    if pack is None and isinstance(prefer_result, dict):
        pack = prefer_result.get("weld_intent_evidence")
    if isinstance(pack, dict) and pack:
        beh = evaluate_behavior_evidence(pack)
        violations.extend(beh.violations)
        warnings.extend(beh.warnings)
        pack = beh.evidence_pack or pack

    return WeldIntentResult(
        ok=not violations,
        applicable=True,
        live_weld_claimed=welded,
        bypass=bypass,
        violations=sorted(set(violations)),
        warnings=sorted(set(warnings)),
        evidence_pack=pack if isinstance(pack, dict) else {},
    )


def scan_chat_hotfix_receipt(
    receipt: dict[str, Any] | str | None,
    *,
    prefer_result: dict[str, Any] | None = None,
) -> WeldIntentResult:
    """Chat / hotfix receipt scanner — fail greenlit-without-B₂.

    Accepts a dict receipt or markdown/YAML frontmatter text.
    Bypass without greenlit → ok (not applicable). Never rewrites Prefer.
    """
    parsed: dict[str, Any] = {}
    if isinstance(receipt, dict):
        parsed = receipt
    elif isinstance(receipt, str) and receipt.strip():
        parsed = _parse_receipt_blob(receipt)
    else:
        return WeldIntentResult(
            ok=False,
            applicable=True,
            violations=["weld_intent:missing_receipt"],
        )

    return validate_weld_intent_latch(
        None, prefer_result=prefer_result, receipt=parsed
    )


_FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.S)


def _parse_receipt_blob(text: str) -> dict[str, Any]:
    """Best-effort YAML frontmatter or JSON object from receipt text."""
    raw = text or ""
    m = _FM_RE.match(raw.strip())
    if m:
        try:
            data = yaml.safe_load(m.group(1))
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    stripped = raw.strip()
    if stripped.startswith("{"):
        try:
            data = json.loads(stripped)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass
    # Loose key: value scan for common flags
    out: dict[str, Any] = {}
    for key in (
        "factory_bypass",
        "factory_greenlit",
        "live_weld_landed",
        "claim_class",
        "keep",
        "ask_success",
        "ready_for_f5",
        "proof_tag",
    ):
        mm = re.search(rf"^{key}:\s*(.+)$", raw, re.M | re.I)
        if not mm:
            continue
        val = mm.group(1).strip().strip("\"'")
        low = val.lower()
        if low in {"true", "yes"}:
            out[key] = True
        elif low in {"false", "no"}:
            out[key] = False
        else:
            out[key] = val
    if "proof_tag" in out and "proof_tags" not in out:
        out["proof_tags"] = [out["proof_tag"]]
    return out


def post_weld_keep_latch(
    armed: dict[str, Any],
    *,
    prefer_result: dict[str, Any] | None = None,
    receipt: dict[str, Any] | None = None,
    evidence_pack: dict[str, Any] | None = None,
    operator_f5_ok: bool = False,
    map_fidelity_hostile_required: bool = True,
) -> WeldIntentResult:
    """KEEP / ask_success after weld: B₁ (when required) + B₂ + operator F5.

    Does not rewrite Prefer Success. Operator F5 = feel — separate from B₂.
    """
    from .prefer_map_fidelity import _hostile_ok as map_hostile_ok

    pr = prefer_result if isinstance(prefer_result, dict) else {}
    armed_keep = dict(armed or {})
    armed_keep["claim_class"] = "ask_success"
    result = validate_weld_intent_latch(
        armed_keep,
        prefer_result=pr,
        receipt=receipt,
        evidence_pack=evidence_pack,
    )
    if map_fidelity_hostile_required and not map_hostile_ok(pr):
        result.violations.append("weld_intent:map_fidelity_hostile_required")
        result.ok = False
        result.applicable = True
    if not operator_f5_ok:
        result.violations.append("weld_intent:operator_f5_required_for_keep")
        result.ok = False
        result.applicable = True
    result.violations = sorted(set(result.violations))
    return result


def load_prefer_result(vault_root: Path, slice_id: str) -> dict[str, Any] | None:
    if not slice_id:
        return None
    candidates = [
        vault_root
        / "1-Projects/genesis-mythos-master/Factory-DRB/slice-briefs"
        / f"{slice_id}.prefer-result.json",
    ]
    for p in candidates:
        if p.is_file():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                return data if isinstance(data, dict) else None
            except (OSError, json.JSONDecodeError):
                return None
    return None


def load_armed_yaml(path: Path) -> dict[str, Any]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return raw if isinstance(raw, dict) else {}


def assert_no_prefer_rewrite(
    before_prefer_success: str,
    after_prefer_success: str,
) -> list[str]:
    """Guard 3 helper — B₂ must not mutate Prefer Success text."""
    if (before_prefer_success or "").strip() != (after_prefer_success or "").strip():
        return ["weld_intent:prefer_success_rewritten_by_b2"]
    return []
