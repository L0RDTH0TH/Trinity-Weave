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
   never called the pipeline. Skip only explicit ``factory_bypass`` + non-empty
   operator ack quote; bypass receipt must **never** say greenlit.
3. **B₂ does not edit the picture.** Validator must not rewrite Prefer Success
   to fit what shipped. Prefer-lie is an operator call.

Stamp alone never passes: ``weld_intent_hostile_ok: true`` without a valid
behavior evidence pack (pass_basis behavior + required keys) fails closed.

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

# Non-place product Prefer — minimal behavior keys (fail-closed if class unknown).
GENERIC_PRODUCT_BEHAVIOR_KEYS: tuple[str, ...] = (
    "play_path_matches_prefer_success",
    "prefer_refuses_not_violated_in_live",
)

BEHAVIOR_KEYS_BY_CLASS: dict[str, tuple[str, ...]] = {
    "place": PLACE_BEHAVIOR_KEYS,
    "dual_place": PLACE_BEHAVIOR_KEYS,
    "place_product": PLACE_BEHAVIOR_KEYS,
    "place-product": PLACE_BEHAVIOR_KEYS,
    "owned_cell_place": PLACE_BEHAVIOR_KEYS,
    "tri_cell_place": PLACE_BEHAVIOR_KEYS,
    "place_coast": PLACE_BEHAVIOR_KEYS,
    "place_update": PLACE_BEHAVIOR_KEYS,
    "dual_coast": PLACE_BEHAVIOR_KEYS,
    "generic": GENERIC_PRODUCT_BEHAVIOR_KEYS,
    "product": GENERIC_PRODUCT_BEHAVIOR_KEYS,
    "worldgen": GENERIC_PRODUCT_BEHAVIOR_KEYS,
    "gen": GENERIC_PRODUCT_BEHAVIOR_KEYS,
    "vis": GENERIC_PRODUCT_BEHAVIOR_KEYS,
    "loop": GENERIC_PRODUCT_BEHAVIOR_KEYS,
    "pack": GENERIC_PRODUCT_BEHAVIOR_KEYS,
    "desk": GENERIC_PRODUCT_BEHAVIOR_KEYS,
}

_PLACE_INFER_MARKERS: tuple[str, ...] = (
    "place_product",
    "place-product",
    "dual_place",
    "owned_cell_place",
    "tri_cell_place",
    "place_coast",
    "place_update",
    "dual_coast",
    "place_",
    "_place",
    "-place",
    "place-",
)

_BYPASS_ACK_KEYS: tuple[str, ...] = (
    "factory_bypass_ack",
    "operator_bypass_ack",
    "operator_ack",
)

_CHAT_RECEIPT_KEYS: tuple[str, ...] = (
    "chat_hotfix_receipt",
    "hotfix_receipt",
    "factory_receipt",
    "bypass_receipt",
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
    """True when Gate B₂ stamp field is set (necessary, not sufficient)."""
    if not isinstance(prefer_result, dict):
        return False
    if prefer_result.get("weld_intent_hostile_ok") is True:
        return True
    nested = prefer_result.get("weld_intent_hostile")
    return isinstance(nested, dict) and nested.get("ok") is True


def has_factory_bypass_flag(
    armed: dict[str, Any] | None, receipt: dict[str, Any] | None = None
) -> bool:
    for blob in (armed, receipt):
        if isinstance(blob, dict) and blob.get("factory_bypass") is True:
            return True
    return False


def factory_bypass_ack_quote(
    armed: dict[str, Any] | None, receipt: dict[str, Any] | None = None
) -> str:
    """Non-empty operator ack quote required for bypass skip."""
    for blob in (armed, receipt):
        if not isinstance(blob, dict):
            continue
        for key in _BYPASS_ACK_KEYS:
            val = blob.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
    return ""


def is_factory_bypass(
    armed: dict[str, Any] | None, receipt: dict[str, Any] | None = None
) -> bool:
    """Explicit factory_bypass + non-empty operator ack quote."""
    return has_factory_bypass_flag(armed, receipt) and bool(
        factory_bypass_ack_quote(armed, receipt)
    )


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


def resolve_prefer_behavior_class(
    armed: dict[str, Any] | None = None,
    pack: dict[str, Any] | None = None,
    prefer_result: dict[str, Any] | None = None,
) -> str:
    """Return prefer behavior class: place / known class / unknown (fail-closed)."""
    for blob in (pack, armed, prefer_result):
        if not isinstance(blob, dict):
            continue
        for key in ("prefer_class", "behavior_class", "object_class"):
            raw = str(blob.get(key) or "").strip().lower()
            if not raw:
                continue
            if raw in BEHAVIOR_KEYS_BY_CLASS:
                return raw
            if "place" in raw:
                return "place"
            return raw
    hay = " ".join(
        [
            str((armed or {}).get("slice_id") or ""),
            str((armed or {}).get("ticket_map_id") or ""),
            str((armed or {}).get("ask_id") or ""),
            str((prefer_result or {}).get("slice_id") or ""),
            str((pack or {}).get("prefer_success") or ""),
        ]
    ).lower()
    if any(m in hay for m in _PLACE_INFER_MARKERS) or re.search(
        r"(?:^|[^a-z])place(?:[^a-z]|$)", hay
    ):
        return "place"
    # Ticket-map prefixes without explicit class → map to coarse class.
    tid = str((armed or {}).get("ticket_map_id") or "").strip().lower()
    for prefix, cls in (
        ("place", "place"),
        ("gen", "gen"),
        ("world", "worldgen"),
        ("vis", "vis"),
        ("loop", "loop"),
        ("pack", "pack"),
        ("desk", "desk"),
    ):
        if tid.startswith(prefix):
            return cls
    return "unknown"


def required_behavior_keys_for_class(prefer_class: str) -> tuple[str, ...] | None:
    """Keys required for class, or None when class is unknown / undefined."""
    cls = (prefer_class or "").strip().lower()
    if cls in BEHAVIOR_KEYS_BY_CLASS:
        return BEHAVIOR_KEYS_BY_CLASS[cls]
    if "place" in cls:
        return PLACE_BEHAVIOR_KEYS
    return None


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
    prefer_class: str = "",
) -> dict[str, Any]:
    """Build B₂ evidence pack. Tags/logs/KEEP headers are **indictment-only**.

    Document for operators / validators: ``tags_are_not_pass_evidence: true``.
    Passing evidence must live under ``behavior`` with ``pass_basis: behavior``.
    """
    pack: dict[str, Any] = {
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
    if prefer_class:
        pack["prefer_class"] = str(prefer_class).strip().lower()
    return pack


def _collect_indict_tags(pack: dict[str, Any]) -> set[str]:
    indict = pack.get("indictment_only") if isinstance(pack.get("indictment_only"), dict) else {}
    tags = indict.get("proof_tags") or pack.get("proof_tags") or []
    out: set[str] = set()
    for t in tags:
        out.add(str(t).strip().lower())
    return out


def _extract_evidence_pack(
    prefer_result: dict[str, Any] | None,
    evidence_pack: dict[str, Any] | None,
) -> dict[str, Any] | None:
    """Resolve structured evidence — never accept ok:true alone as the pack."""
    if isinstance(evidence_pack, dict) and evidence_pack:
        return evidence_pack
    if not isinstance(prefer_result, dict):
        return None
    direct = prefer_result.get("weld_intent_evidence")
    if isinstance(direct, dict) and direct:
        return direct
    nested = prefer_result.get("weld_intent_hostile")
    if isinstance(nested, dict):
        nested_ev = nested.get("evidence") or nested.get("weld_intent_evidence")
        if isinstance(nested_ev, dict) and nested_ev:
            return nested_ev
        behavior = nested.get("behavior")
        if isinstance(behavior, dict) and behavior:
            return build_evidence_pack(
                prefer_success=str(nested.get("prefer_success") or ""),
                behavior=behavior,
                pass_basis=str(nested.get("pass_basis") or ""),
                prefer_class=str(nested.get("prefer_class") or ""),
                proof_tags=list(nested.get("proof_tags") or []),
            )
    return None


def evaluate_behavior_evidence(
    pack: dict[str, Any] | None,
    *,
    armed: dict[str, Any] | None = None,
    prefer_result: dict[str, Any] | None = None,
) -> WeldIntentResult:
    """Mechanical fail-closed checks on an evidence pack (no Prefer rewrite).

    Honest place-shaped behavior can pass this seat; piggyback / string-match /
    tag-as-pass / MCP-only / missing required keys cannot. Hostile LLM (skill)
    still stamps ``weld_intent_hostile_ok`` for the full rubric — stamp alone
    never acquits without this pack.
    """
    if not isinstance(pack, dict) or not pack:
        return WeldIntentResult(
            ok=False,
            applicable=True,
            violations=["weld_intent:missing_evidence_pack"],
        )

    # Bare {ok: true} / stamp-shaped dict is not structured behavior evidence.
    behavior_candidate = pack.get("behavior") if isinstance(pack.get("behavior"), dict) else None
    pass_basis_candidate = str(pack.get("pass_basis") or "").strip().lower()
    stamp_only_keys = {
        "ok",
        "weld_intent_hostile_ok",
        "verdict",
        "summary",
        "map_fidelity_hostile_ok",
    }
    if set(pack.keys()) <= stamp_only_keys or (
        pack.get("ok") is True and not behavior_candidate and not pass_basis_candidate
    ):
        return WeldIntentResult(
            ok=False,
            applicable=True,
            violations=["weld_intent:stamp_alone_not_evidence"],
            evidence_pack=pack,
        )

    violations: list[str] = []
    warnings: list[str] = []

    pass_basis = pass_basis_candidate
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

    if pass_basis != "behavior":
        if pass_basis in {"", "proof_tag", "factory_log", "keep_header"}:
            violations.append("weld_intent:no_behavior_evidence")
        else:
            violations.append("weld_intent:pass_basis_must_be_behavior")

    tags = _collect_indict_tags(pack)
    piggy = tags & PIGGYBACK_INDICT_TAGS
    if piggy:
        # Guard 1: tag saying Success / KEEP cannot acquit — piggyback indicts.
        violations.append(
            "weld_intent:piggyback_indict:" + ",".join(sorted(piggy))
        )

    behavior = behavior_candidate or {}
    prefer_class = resolve_prefer_behavior_class(armed, pack, prefer_result)
    required = required_behavior_keys_for_class(prefer_class)
    if required is None:
        violations.append(f"weld_intent:unknown_prefer_class_fail_closed:{prefer_class or 'unknown'}")
    else:
        for key in required:
            if key not in behavior:
                violations.append(f"weld_intent:behavior_key_missing:{key}")
            elif behavior.get(key) is not True:
                # Missing/false both fail — place cannot omit update_four_ran.
                if behavior.get(key) is False:
                    alias = {
                        "update_four_ran": "weld_intent:update_four_skipped",
                        "coast_gate_ran": "weld_intent:coast_gate_skipped",
                        "same_seat_ghost_eq_commit": "weld_intent:ghost_seat_neq_commit",
                        "full_survives_neighbor_rebuild": "weld_intent:neighbor_rebuild_deletes_full",
                        "prefer_refuses_not_violated_in_live": "weld_intent:prefer_refuse_violated_in_live",
                        "play_path_matches_prefer_success": "weld_intent:play_path_mismatch",
                    }.get(key)
                    if alias:
                        violations.append(alias)
                    else:
                        violations.append(f"weld_intent:behavior_key_not_true:{key}")
                else:
                    violations.append(f"weld_intent:behavior_key_not_true:{key}")

    # Logs claiming Success while behavior missing/false — cannot acquit.
    indict = pack.get("indictment_only") if isinstance(pack.get("indictment_only"), dict) else {}
    log_excerpts = indict.get("factory_log_excerpts") or []
    keep_headers = indict.get("keep_headers") or []
    log_claims_success = any(
        re.search(r"\b(success|keep|ask_success)\b", str(x), re.I) for x in log_excerpts
    ) or any(re.search(r"\bkeep\b", str(x), re.I) for x in keep_headers)
    if log_claims_success and (
        not behavior
        or (required and any(behavior.get(k) is not True for k in required))
        or piggy
    ):
        violations.append("weld_intent:logs_cannot_acquit")

    return WeldIntentResult(
        ok=not violations,
        applicable=True,
        violations=sorted(set(violations)),
        warnings=sorted(set(warnings)),
        evidence_pack=pack,
    )


def extract_chat_receipt_blob(
    armed: dict[str, Any] | None = None,
    prefer_result: dict[str, Any] | None = None,
    receipt: dict[str, Any] | str | None = None,
) -> dict[str, Any] | str | None:
    """Pull embedded chat/hotfix receipt from armed / prefer_result when present."""
    if receipt is not None:
        return receipt
    for blob in (armed, prefer_result):
        if not isinstance(blob, dict):
            continue
        for key in _CHAT_RECEIPT_KEYS:
            val = blob.get(key)
            if isinstance(val, (dict, str)) and val:
                return val
    return None


def validate_weld_intent_latch(
    armed: dict[str, Any] | None,
    *,
    prefer_result: dict[str, Any] | None = None,
    receipt: dict[str, Any] | None = None,
    evidence_pack: dict[str, Any] | None = None,
) -> WeldIntentResult:
    """Refuse Success / ready-for-F5 / KEEP / greenlit without B₂ when weld claimed.

    Bypass skip only with ``factory_bypass: true`` **and** non-empty operator ack
    quote. Bypass + greenlit = hard fail. Bare ``weld_intent_hostile_ok: true``
    without a valid behavior evidence pack = hard fail.
    Does **not** rewrite Prefer Success fields.
    """
    bypass_flag = has_factory_bypass_flag(armed, receipt)
    ack = factory_bypass_ack_quote(armed, receipt)
    bypass = bypass_flag and bool(ack)
    greenlit = claims_factory_greenlit(armed, prefer_result, receipt)
    welded = live_weld_claimed(armed, prefer_result, receipt)
    success = success_altitude_claimed(armed, prefer_result, receipt)

    violations: list[str] = []
    warnings: list[str] = []

    if bypass_flag and greenlit:
        violations.append("weld_intent:bypass_must_not_claim_greenlit")

    if bypass_flag and not ack:
        violations.append("weld_intent:bypass_missing_operator_ack")

    if bypass and not greenlit and not violations:
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
        # Bypass flag without ack on non-weld path still fails closed.
        if violations:
            return WeldIntentResult(
                ok=False,
                applicable=True,
                live_weld_claimed=welded,
                bypass=False,
                violations=sorted(set(violations)),
                warnings=sorted(set(warnings)),
            )
        return WeldIntentResult(
            ok=True, applicable=False, live_weld_claimed=False, bypass=bypass
        )

    # Staging Success / ready-for-F5 / KEEP / greenlit without B₂ stamp when welded.
    if (success or greenlit) and not weld_intent_hostile_ok(prefer_result):
        violations.append("weld_intent:hostile_required_before_success")
    if greenlit and not weld_intent_hostile_ok(prefer_result):
        if "weld_intent:greenlit_without_b2" not in violations:
            violations.append("weld_intent:greenlit_without_b2")

    # Stamp alone never passes — require structured behavior evidence pack.
    pack = _extract_evidence_pack(prefer_result, evidence_pack)
    if not isinstance(pack, dict) or not pack:
        violations.append("weld_intent:missing_evidence_pack")
    else:
        beh = evaluate_behavior_evidence(
            pack, armed=armed, prefer_result=prefer_result
        )
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
    armed: dict[str, Any] | None = None,
    evidence_pack: dict[str, Any] | None = None,
) -> WeldIntentResult:
    """Chat / hotfix receipt scanner — fail greenlit-without-B₂ / bare stamps.

    Accepts a dict receipt or markdown/YAML frontmatter text.
    Bypass without greenlit → ok (not applicable) only with ack quote.
    Never rewrites Prefer.
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
        armed,
        prefer_result=prefer_result,
        receipt=parsed,
        evidence_pack=evidence_pack,
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
        "factory_bypass_ack",
        "operator_bypass_ack",
        "operator_ack",
        "factory_greenlit",
        "live_weld_landed",
        "claim_class",
        "keep",
        "ask_success",
        "ready_for_f5",
        "proof_tag",
        "weld_intent_hostile_ok",
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
    chat = extract_chat_receipt_blob(armed_keep, pr, receipt)
    receipt_dict: dict[str, Any] | None = None
    if isinstance(chat, dict):
        receipt_dict = chat
    elif isinstance(chat, str) and chat.strip():
        receipt_dict = _parse_receipt_blob(chat)
    result = validate_weld_intent_latch(
        armed_keep,
        prefer_result=pr,
        receipt=receipt_dict,
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
