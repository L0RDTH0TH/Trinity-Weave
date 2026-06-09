"""Phase 17 graduation plane — evidence-gated trial→global and bounded config promotion."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..schedule_config import GraduationPromotion, SchedulePlanesConfig
from .trinity_core_charter_audit import ARTIFACT_DIR as CHARTER_ARTIFACT_DIR
from .trinity_llm_repair_trial_gate import evaluate_trial_cutover_gates
from .trinity_type2_verify import ARTIFACT_DIR as TYPE2_ARTIFACT_DIR

GRADUATION_RECEIPTS = Path(".technical/parallel/institute/graduation-receipts.jsonl")
GRADUATION_OVERRIDES = Path(".technical/parallel/institute/graduation-overrides.yaml")


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _latest_artifact(vault_root: Path, pattern: str) -> dict[str, Any] | None:
    val_dir = vault_root / TYPE2_ARTIFACT_DIR
    if not val_dir.is_dir():
        return None
    files = sorted(val_dir.glob(pattern), reverse=True)
    if not files:
        return None
    try:
        return json.loads(files[0].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _latest_type2(vault_root: Path) -> dict[str, Any] | None:
    return _latest_artifact(vault_root, "type2-verify-*.json")


def _latest_charter(vault_root: Path) -> dict[str, Any] | None:
    val_dir = vault_root / CHARTER_ARTIFACT_DIR
    if not val_dir.is_dir():
        return None
    files = sorted(val_dir.glob("core-charter-audit-*.json"), reverse=True)
    if not files:
        return None
    try:
        return json.loads(files[0].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _signal_context(
    vault_root: Path,
    *,
    maintain_wrap_streak: int,
    maintain_wrap_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    trial = evaluate_trial_cutover_gates(vault_root)
    type2 = _latest_type2(vault_root)
    charter = _latest_charter(vault_root)
    if maintain_wrap_result is not None:
        type2_ok = bool(maintain_wrap_result.get("type2_ok"))
        charter_ok = bool(maintain_wrap_result.get("charter_ok"))
    else:
        type2_ok = bool(type2 and type2.get("pass_gate_ok"))
        charter_ok = bool(charter and charter.get("charter_aligned"))
    recommend = trial.get("recommend_global_flip")
    trial_flip = recommend is True or recommend == "operator_manual_only"
    return {
        "trial_gate": {
            "recommend_global_flip": trial_flip,
            "all_gates_ok": bool(trial.get("ok")),
            "cutover_gates": trial.get("cutover_gates"),
        },
        "type2": {
            "pass_gate_ok": type2_ok,
            "artifact": (type2 or {}).get("report_path"),
        },
        "charter": {
            "charter_aligned": charter_ok,
            "artifact": (charter or {}).get("report_path"),
        },
        "maintain_wrap_streak": maintain_wrap_streak,
    }


def _check_requires(requires: dict[str, Any], ctx: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    ok = True
    for key, expected in requires.items():
        if key == "maintain_wrap_streak_min":
            streak = int(ctx.get("maintain_wrap_streak") or 0)
            if streak < int(expected):
                ok = False
                reasons.append(f"maintain_wrap_streak {streak} < {expected}")
            continue
        if "." in key:
            section, field = key.split(".", 1)
            block = ctx.get(section) if isinstance(ctx.get(section), dict) else {}
            actual = block.get(field)
        else:
            actual = ctx.get(key)
        if actual != expected:
            ok = False
            reasons.append(f"{key}: want {expected!r} got {actual!r}")
    return ok, reasons


def _check_rollback(rollback_on: dict[str, Any], ctx: dict[str, Any]) -> bool:
    for key, bad_val in rollback_on.items():
        if "." in key:
            section, field = key.split(".", 1)
            block = ctx.get(section) if isinstance(ctx.get(section), dict) else {}
            actual = block.get(field)
        else:
            actual = ctx.get(key)
        if actual == bad_val:
            return True
    return False


def _append_receipt(vault_root: Path, row: dict[str, Any]) -> None:
    path = vault_root / GRADUATION_RECEIPTS
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _write_overrides_yaml(vault_root: Path, sets: dict[str, Any]) -> Path:
    path = vault_root / GRADUATION_OVERRIDES
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Auto-written by graduation plane — merged at trinity config read time", ""]
    for key, val in sorted(sets.items()):
        if isinstance(val, bool):
            lines.append(f"{key}: {'true' if val else 'false'}")
        else:
            lines.append(f"{key}: {val}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def load_graduation_overrides(vault_root: Path) -> dict[str, Any]:
    path = vault_root / GRADUATION_OVERRIDES
    if not path.is_file():
        return {}
    out: dict[str, Any] = {}
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.lower() in ("true", "false"):
            out[key] = val.lower() == "true"
        else:
            try:
                out[key] = int(val)
            except ValueError:
                out[key] = val.strip('"').strip("'")
    return out


def clear_graduation_overrides(vault_root: Path) -> None:
    path = vault_root / GRADUATION_OVERRIDES
    if path.is_file():
        path.unlink()


def evaluate_promotion(
    vault_root: Path,
    promo: GraduationPromotion,
    ctx: dict[str, Any],
) -> dict[str, Any]:
    ok, reasons = _check_requires(promo.requires, ctx)
    rollback = _check_rollback(promo.rollback_on, ctx)
    return {
        "promotion": promo.name,
        "eligible": ok and not rollback,
        "requires_ok": ok,
        "rollback_triggered": rollback,
        "reasons": reasons,
        "would_set": dict(promo.sets) if ok and not rollback else {},
    }


def run_graduation_evaluator(
    vault_root: Path,
    cfg: SchedulePlanesConfig,
    *,
    maintain_wrap_streak: int = 0,
    maintain_wrap_result: dict[str, Any] | None = None,
    apply: bool | None = None,
) -> dict[str, Any]:
    vault_root = vault_root.resolve()
    ctx = _signal_context(
        vault_root,
        maintain_wrap_streak=maintain_wrap_streak,
        maintain_wrap_result=maintain_wrap_result,
    )

    for promo in cfg.graduation_promotions:
        if promo.rollback_on and _check_rollback(promo.rollback_on, ctx):
                clear_graduation_overrides(vault_root)
                _append_receipt(
                    vault_root,
                    {
                        "ts": _now_iso(),
                        "event": "graduation_rollback",
                        "promotion": promo.name,
                        "context": ctx,
                    },
                )
                return {
                    "ok": True,
                    "skipped": False,
                    "action": "graduation_rollback",
                    "context": ctx,
                }

    evaluations = [
        evaluate_promotion(vault_root, promo, ctx) for promo in cfg.graduation_promotions
    ]
    eligible = [e for e in evaluations if e.get("eligible")]

    do_apply = apply if apply is not None else cfg.graduation_apply_enabled
    applied: list[dict[str, Any]] = []
    if cfg.graduation_enabled and eligible and do_apply:
        merged_sets: dict[str, Any] = {}
        for ev in eligible:
            merged_sets.update(ev.get("would_set") or {})
        if merged_sets:
            overrides_path = _write_overrides_yaml(vault_root, merged_sets)
            applied.append({"path": str(overrides_path.relative_to(vault_root)), "keys": list(merged_sets)})
            _append_receipt(
                vault_root,
                {
                    "ts": _now_iso(),
                    "event": "graduation_apply",
                    "promotions": [e["promotion"] for e in eligible],
                    "sets": merged_sets,
                    "context": ctx,
                },
            )

    return {
        "ok": True,
        "action": "graduation_evaluator",
        "graduation_enabled": cfg.graduation_enabled,
        "apply": do_apply,
        "context": ctx,
        "evaluations": evaluations,
        "eligible": [e["promotion"] for e in eligible],
        "applied": applied,
    }
