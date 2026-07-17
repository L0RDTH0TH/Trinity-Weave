"""Phase 16b — stub honesty fold: trace stubs, block completion claims (core law)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from .governance import append_metric_row, weave_dir

STUB_TRACE_REL = Path(".technical/weave/stub-trace.jsonl")
VALIDATION_ARTIFACT = Path(".technical/weave/validation/stub-honesty-audit.json")

DEFAULT_CLOSURE_ROOTS: tuple[str, ...] = (
    "scripts/eat_queue_core/weave",
)

CONDUCT_REPAIR_STUB_RE = re.compile(
    r"Minimal conduct-repair stub \(10g apply\)",
    re.IGNORECASE,
)

IMPORT_ONLY_TEST_RE = re.compile(
    r"importlib\.import_module",
    re.IGNORECASE,
)

FORBIDDEN_SUPPRESS_FLAGS = frozenset(
    {
        "suppress_stub_check",
        "stub_waived_without_trace",
        "import_only_as_conduct_complete",
    }
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stub_trace_path(vault_root: Path) -> Path:
    return vault_root.resolve() / STUB_TRACE_REL


def _iter_closure_files(vault_root: Path, roots: tuple[str, ...] | None = None) -> Iterator[Path]:
    base = vault_root.resolve()
    skip_names = frozenset({"stub_honesty.py"})
    for rel in roots or DEFAULT_CLOSURE_ROOTS:
        root = base / rel
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.py")):
            if path.name in skip_names or path.name.startswith("test_"):
                continue
            if "/tests/" in path.as_posix():
                continue
            yield path


def _classify_stub_line(line: str, *, rel: str) -> str | None:
    text = line.strip()
    if not text or text.startswith('"""') or text.startswith("'''"):
        return None
    # Skip pattern literals and registry flag definitions (not runtime stubs).
    if "re.compile" in text or text.startswith('r"') or text.startswith("r'"):
        return None
    if '"flag":' in text or "'flag':" in text:
        return None
    if text.startswith(("{", "}", "[", "]", ")")):
        return None

    if CONDUCT_REPAIR_STUB_RE.search(text) and rel.endswith("corps_conduct_repair_apply.py"):
        return "conduct_repair_stub"

    if re.search(r"#\s*STUB\s*:", text, re.IGNORECASE):
        return "marked_stub"

    if re.search(r"#.*(?:stub only|not production semantics)", text, re.IGNORECASE):
        return "silent_stub"

    if re.search(r"raise NotImplementedError", text) and not text.lstrip().startswith("#"):
        return "not_implemented"

    if re.search(r"#\s*TODO\s*:.*stub", text, re.IGNORECASE):
        return "marked_stub"

    return None


def is_import_only_conduct_stub_body(body: str) -> bool:
    """True when test body is import-only smoke (adequacy 0)."""
    if CONDUCT_REPAIR_STUB_RE.search(body):
        return True
    if IMPORT_ONLY_TEST_RE.search(body) and "assert" not in body:
        return True
    return False


def scan_closure_stubs(
    vault_root: Path,
    *,
    roots: tuple[str, ...] | None = None,
) -> list[dict[str, Any]]:
    """Read-only scan of closure paths for stub markers."""
    vault_root = vault_root.resolve()
    findings: list[dict[str, Any]] = []
    for path in _iter_closure_files(vault_root, roots=roots):
        rel = path.relative_to(vault_root).as_posix()
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for idx, line in enumerate(lines, start=1):
            kind = _classify_stub_line(line, rel=rel)
            if not kind:
                continue
            findings.append(
                {
                    "path": rel,
                    "line": idx,
                    "kind": kind,
                    "excerpt": line.strip()[:240],
                }
            )
    return findings


def load_stub_trace(vault_root: Path) -> list[dict[str, Any]]:
    path = stub_trace_path(vault_root)
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(raw, dict):
            rows.append(raw)
    return rows


def append_stub_trace(vault_root: Path, entry: dict[str, Any]) -> Path:
    path = stub_trace_path(vault_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {**entry, "recorded_at": entry.get("recorded_at") or _now_iso()}
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path


def stub_trace_entry_from_repair(
    *,
    proof_rel: str,
    trinity_id: str,
    run_id: str | None = None,
) -> dict[str, Any]:
    return {
        "id": f"conduct-repair-{proof_rel.replace('/', '-')}",
        "path": proof_rel,
        "kind": "conduct_repair_stub",
        "trinity_id": trinity_id,
        "run_id": run_id or "-",
        "status": "open",
        "obligation": "implement_real_proof",
    }


def _traced_keys(rows: list[dict[str, Any]]) -> set[tuple[str, int | None]]:
    keys: set[tuple[str, int | None]] = set()
    for row in rows:
        if str(row.get("status") or "").lower() in ("closed", "implemented"):
            continue
        path = str(row.get("path") or "")
        line = row.get("line")
        keys.add((path, int(line) if line is not None else None))
    return keys


def untraced_findings(
    vault_root: Path,
    findings: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    found = findings if findings is not None else scan_closure_stubs(vault_root)
    traced = _traced_keys(load_stub_trace(vault_root))
    out: list[dict[str, Any]] = []
    for f in found:
        key = (str(f.get("path") or ""), int(f.get("line") or 0) or None)
        path_only = (key[0], None)
        if key not in traced and path_only not in traced:
            out.append(f)
    return out


def evaluate_stub_honesty_payload(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    """Apply stub honesty rules to a receipt/outcome payload (immutable gate logic)."""
    errors: list[str] = []
    flags = set(payload.get("forbidden_flags") or [])
    for f in FORBIDDEN_SUPPRESS_FLAGS:
        if f in flags:
            errors.append(f"forbidden flag: {f}")

    if payload.get("import_only_smoke") and payload.get("claimed_structural"):
        errors.append("import-only smoke cannot claim structural conduct")

    if payload.get("conduct_repair_stub_as_complete"):
        errors.append("conduct-repair import stub cannot count as conduct complete")

    untraced = payload.get("untraced_stub_count")
    if untraced is None and payload.get("untraced_stubs"):
        untraced = len(payload.get("untraced_stubs") or [])
    if untraced is None:
        untraced = 0

    claims_complete = bool(
        payload.get("claimed_success")
        or payload.get("pass_gate_ok")
        or (
            payload.get("status") == "success"
            and payload.get("conduct_ok") is not False
            and not payload.get("provisional_success")
        )
    )
    if claims_complete and int(untraced or 0) > 0:
        errors.append(
            f"cannot claim completion with {untraced} untraced stub(s) in closure paths"
        )

    open_traces = int(payload.get("open_stub_trace_count") or 0)
    if claims_complete and open_traces > 0 and (
        payload.get("strict_stub_impl") or payload.get("full_corpus_closure")
    ):
        errors.append(
            f"cannot claim full closure with {open_traces} open stub implementation obligation(s)"
        )

    if payload.get("suppress_stub_check") and claims_complete:
        errors.append("stub honesty check cannot be suppressed on completion claims")

    return len(errors) == 0, errors


def run_stub_honesty_audit(
    vault_root: Path,
    *,
    dry_run: bool = False,
    write_artifact: bool = True,
    trace_open: bool = True,
) -> dict[str, Any]:
    """Scan closure, reconcile trace ledger, emit audit artifact."""
    vault_root = vault_root.resolve()
    findings = scan_closure_stubs(vault_root)
    untraced = untraced_findings(vault_root, findings)
    trace_rows = load_stub_trace(vault_root)

    if trace_open and not dry_run:
        for f in untraced:
            append_stub_trace(
                vault_root,
                {
                    "id": f"scan-{f['path'].replace('/', '-')}-L{f['line']}",
                    "path": f["path"],
                    "line": f["line"],
                    "kind": f.get("kind"),
                    "excerpt": f.get("excerpt"),
                    "status": "open",
                    "obligation": "implement_or_mark_explicit_stub",
                    "source": "stub_honesty_scan",
                },
            )
        trace_rows = load_stub_trace(vault_root)
        untraced = untraced_findings(vault_root, findings)

    open_trace = [r for r in trace_rows if str(r.get("status") or "open").lower() == "open"]
    ok = len(untraced) == 0

    report: dict[str, Any] = {
        "ok": ok,
        "dry_run": dry_run,
        "generated_at": _now_iso(),
        "findings_count": len(findings),
        "untraced_count": len(untraced),
        "open_trace_count": len(open_trace),
        "untraced": untraced[:32],
        "findings_sample": findings[:16],
        "trace_path": str(STUB_TRACE_REL),
        "artifact_path": str(VALIDATION_ARTIFACT),
    }

    if not dry_run and write_artifact:
        out = vault_root / VALIDATION_ARTIFACT
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["written"] = True

    append_metric_row(
        vault_root,
        {
            "metric_type": "stub_honesty_audit",
            "ok": ok,
            "findings_count": len(findings),
            "untraced_count": len(untraced),
        },
    )
    return report


def activate_stub_honesty_invariants(vault_root: Path) -> dict[str, Any]:
    """Bootstrap + counselor-activate Phase 16 stub honesty invariants."""
    from .invariant_registry import (
        activate_invariant,
        bootstrap_phase16_invariants,
    )

    boot = bootstrap_phase16_invariants(vault_root)
    activated: list[str] = []
    failed: list[dict[str, Any]] = []
    for iid in boot.get("created", []) + boot.get("skipped", []):
        if not iid:
            continue
        ent = activate_invariant(vault_root, iid, counselor_approved=True)
        if ent.get("ok"):
            if iid not in activated:
                activated.append(iid)
        elif ent.get("error") != "not_found":
            failed.append(ent)
    return {
        "ok": len(failed) == 0,
        "bootstrap": boot,
        "activated": activated,
        "failed": failed,
    }
