"""Factory output conduct — product track honesty on LaunchShell → PlayRegion (warn → block ladder)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from ...config_loader import resolve_config_path
from ..trinity_align import check as trinity_align_check
from ..trinity_behavior_proof import run_card_behavior_proofs
from ..trinity_touch_refresh import load_trinity_card

EnforcementMode = Literal["off", "warn", "block"]
CARD_ID = "factory_output_conduct"
VALID_MODES: frozenset[str] = frozenset({"off", "warn", "block"})

CORE_NARRATIVE_DRIFT_PATTERNS: tuple[tuple[str, str], ...] = (
    ("Post-R1", "post_r1_deferral"),
    ("do not implement", "do_not_implement_yet"),
    ("stack proof only", "stack_proof_only"),
    ("until then", "until_then_loophole"),
    ("stack-only proof", "stack_only_proof"),
)


@dataclass(frozen=True)
class NarrativeDriftHit:
    path: str
    line: int
    pattern: str
    kind: str
    excerpt: str

    def to_dict(self) -> dict[str, str | int]:
        return {
            "path": self.path,
            "line": self.line,
            "pattern": self.pattern,
            "kind": self.kind,
            "excerpt": self.excerpt,
        }


@dataclass
class FactoryOutputGateResult:
    mode: EnforcementMode
    ok: bool
    conduct_ok: bool = True
    align_ok: bool = True
    narrative_ok: bool = True
    warnings: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)
    narrative_hits: list[NarrativeDriftHit] = field(default_factory=list)
    behavior_proofs: list[dict[str, Any]] = field(default_factory=list)
    align: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "ok": self.ok,
            "conduct_ok": self.conduct_ok,
            "align_ok": self.align_ok,
            "narrative_ok": self.narrative_ok,
            "warnings": list(self.warnings),
            "failures": list(self.failures),
            "narrative_hits": [h.to_dict() for h in self.narrative_hits],
            "behavior_proofs": list(self.behavior_proofs),
            "align": self.align,
        }


def parse_factory_orchestrator_yaml(config_path: Path) -> dict[str, Any]:
    """Load ``factory_orchestrator:`` mapping from Second-Brain-Config.md."""
    if not config_path.is_file():
        return {}
    text = config_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    start_idx: int | None = None
    for i, line in enumerate(lines):
        if len(line) - len(line.lstrip()) != 0:
            continue
        stripped = line.strip()
        if stripped == "factory_orchestrator:" or stripped.startswith("factory_orchestrator:"):
            start_idx = i
            break
    if start_idx is None:
        return {}
    block_lines: list[str] = []
    for j in range(start_idx, len(lines)):
        line = lines[j]
        stripped = line.strip()
        if j > start_idx and stripped and not stripped.startswith("#"):
            cur_col = len(line) - len(line.lstrip())
            if cur_col <= 0 and not line.lstrip().startswith("#"):
                break
        block_lines.append(line)
    blob = "\n".join(block_lines)
    try:
        import yaml  # type: ignore[import-untyped]

        data = yaml.safe_load(blob)
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    inner = data.get("factory_orchestrator")
    return inner if isinstance(inner, dict) else {}


def load_factory_output_enforcement_mode(vault_root: Path) -> EnforcementMode:
    cfg_path = resolve_config_path(vault_root, None)
    raw = parse_factory_orchestrator_yaml(cfg_path)
    mode = str(raw.get("factory_output_trinity_gate") or "warn").strip().lower()
    if mode not in VALID_MODES:
        return "warn"
    return mode  # type: ignore[return-value]


def scan_core_narrative_drift(vault_root: Path, *, game_repo_rel: str | None = None) -> list[NarrativeDriftHit]:
    """Lightweight error_narrative_drift scan on demo Core/ (factory mutable band)."""
    vault_root = vault_root.resolve()
    if game_repo_rel:
        core = vault_root / game_repo_rel.strip("/") / "Core"
    else:
        core = vault_root / "5-Attachments/Code-Repos/genesis-mythos-alpha/Core"
    if not core.is_dir():
        return []
    hits: list[NarrativeDriftHit] = []
    for py_path in sorted(core.rglob("*.cs")):
        try:
            text = py_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = str(py_path.relative_to(vault_root))
        for line_no, line in enumerate(text.splitlines(), start=1):
            lower = line.lower()
            for needle, kind in CORE_NARRATIVE_DRIFT_PATTERNS:
                if needle.lower() in lower:
                    hits.append(
                        NarrativeDriftHit(
                            path=rel,
                            line=line_no,
                            pattern=needle,
                            kind=kind,
                            excerpt=line.strip()[:160],
                        )
                    )
    return hits


def run_factory_output_conduct_proofs(vault_root: Path) -> tuple[bool, list[dict[str, Any]]]:
    """Run touch.behavior_signals for factory_output_conduct card."""
    vault_root = vault_root.resolve()
    try:
        card = load_trinity_card(vault_root, CARD_ID)
    except (FileNotFoundError, OSError, KeyError):
        return False, [{"test_name": CARD_ID, "ok": False, "detail": "card_missing"}]
    results = run_card_behavior_proofs(vault_root, card)
    payload = [r.to_dict() for r in results]
    ok = bool(results) and all(r.ok for r in results)
    return ok, payload


def run_factory_output_gate(
    vault_root: Path,
    *,
    mode: EnforcementMode | None = None,
    run_align: bool = True,
    scan_narrative: bool = True,
    game_repo_rel: str | None = None,
) -> FactoryOutputGateResult:
    """Evaluate factory output conduct. ``block`` fails closed; ``warn`` emits warnings only."""
    vault_root = vault_root.resolve()
    effective = mode or load_factory_output_enforcement_mode(vault_root)
    if effective not in VALID_MODES:
        effective = "warn"

    out = FactoryOutputGateResult(mode=effective, ok=True)

    if effective == "off":
        out.warnings.append("factory_output_trinity_gate=off — conduct skipped")
        return out

    conduct_ok, proofs = run_factory_output_conduct_proofs(vault_root)
    out.conduct_ok = conduct_ok
    out.behavior_proofs = proofs
    if not conduct_ok:
        msg = f"factory_output_conduct behavior proofs failed ({len([p for p in proofs if not p.get('ok')])} failing)"
        out.failures.append(msg)

    if scan_narrative:
        hits = scan_core_narrative_drift(vault_root, game_repo_rel=game_repo_rel)
        out.narrative_hits = hits
        out.narrative_ok = len(hits) == 0
        if hits:
            out.failures.append(f"core narrative drift ({len(hits)} hit(s))")

    if run_align:
        align = trinity_align_check(vault_root, CARD_ID, run_behavior_proofs=True)
        out.align = align.to_dict()
        out.align_ok = bool(align.ok)
        if not align.ok:
            disc = ", ".join(d.kind for d in align.disconnects[:4]) or "misalign"
            out.failures.append(f"trinity_align/{CARD_ID}: {disc}")

    if effective == "warn":
        out.warnings.extend(out.failures)
        out.failures = []
        out.ok = True
    else:
        out.ok = conduct_ok and out.narrative_ok and out.align_ok

    return out


def apply_factory_output_gate_to_trace(
    vault_root: Path,
    trace: dict[str, Any] | None = None,
    *,
    mode: EnforcementMode | None = None,
) -> tuple[FactoryOutputGateResult, dict[str, Any]]:
    """Run gate and merge parse-safe fragments into a trace dict (Layer 1 / harness)."""
    result = run_factory_output_gate(vault_root, mode=mode)
    merged = dict(trace or {})
    merged["factory_output_trinity_gate"] = result.mode
    merged["factory_output_conduct_ok"] = result.conduct_ok
    if result.warnings:
        merged["factory_output_warnings"] = result.warnings[:8]
    if result.failures:
        merged["factory_output_failures"] = result.failures[:8]
    if result.narrative_hits:
        merged["factory_output_narrative_hits"] = [h.to_dict() for h in result.narrative_hits[:6]]
    return result, merged
