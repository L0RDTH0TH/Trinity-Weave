"""Engine-neutral Prefer probes — ops only; project nouns live in proof-catalog.yaml.

Ops: file_exists | file_contains | field_equals | command_exits_zero.
Runner does not know scenes, engines, or C# types. Never iterates the whole catalog.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .bindings import BindingMissingError, UNKNOWN_PROBE, load_family, require_project_id


@dataclass(frozen=True)
class ProbeOutcome:
    probe_id: str
    ok: bool
    detail: str


class UnknownProbeError(KeyError):
    def __init__(self, probe_id: str) -> None:
        super().__init__(probe_id)
        self.code = UNKNOWN_PROBE
        self.probe_id = probe_id


_OPS = frozenset(
    {"file_exists", "file_contains", "field_equals", "command_exits_zero"}
)


def _repo_root(vault_root: Path, project_id: str) -> Path:
    from .bindings import game_repo_path

    return vault_root.resolve() / game_repo_path(vault_root, project_id)


def _run_op(repo: Path, vault_root: Path, op: str, args: dict[str, Any]) -> tuple[bool, str]:
    if op == "file_exists":
        rel = str(args.get("path") or "").strip()
        if not rel:
            return False, "file_exists:missing_path"
        target = repo / rel
        return target.is_file() or target.is_dir(), f"file_exists:{rel}"

    if op == "file_contains":
        rel = str(args.get("path") or "").strip()
        needle = str(args.get("contains") or "")
        if not rel:
            return False, "file_contains:missing_path"
        path = repo / rel
        if not path.is_file():
            return False, f"file_contains:missing:{rel}"
        text = path.read_text(encoding="utf-8", errors="replace")
        return needle in text, f"file_contains:{rel}"

    if op == "field_equals":
        rel = str(args.get("path") or "").strip()
        key = str(args.get("key") or "").strip()
        expect = args.get("equals")
        if not rel or not key:
            return False, "field_equals:missing_path_or_key"
        path = repo / rel
        if not path.is_file():
            # Also allow vault-relative paths
            path = vault_root / rel
        if not path.is_file():
            return False, f"field_equals:missing:{rel}"
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(raw, dict):
            return False, f"field_equals:not_mapping:{rel}"
        actual = raw.get(key)
        return actual == expect, f"field_equals:{key}"

    if op == "command_exits_zero":
        argv = args.get("argv")
        if not isinstance(argv, list) or not argv:
            return False, "command_exits_zero:missing_argv"
        cmd = [str(x) for x in argv]
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(repo),
                capture_output=True,
                text=True,
                timeout=int(args.get("timeout_sec") or 120),
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return False, f"command_exits_zero:error:{exc}"
        return proc.returncode == 0, f"command_exits_zero:rc={proc.returncode}"

    return False, f"unknown_op:{op}"


def run_named_probes(
    vault_root: Path,
    project_id: str,
    probe_ids: list[str] | tuple[str, ...],
) -> list[ProbeOutcome]:
    """Run only the named probe ids from proof-catalog.yaml. Empty list → no work."""
    pid = require_project_id(project_id)
    vault_root = vault_root.resolve()
    if not probe_ids:
        return []

    try:
        catalog = load_family(vault_root, pid, "proof-catalog")
    except BindingMissingError:
        raise
    probes = catalog.get("probes")
    if not isinstance(probes, dict):
        probes = {}

    try:
        repo = _repo_root(vault_root, pid)
    except BindingMissingError as exc:
        return [
            ProbeOutcome(str(i), False, f"binding_missing:{exc.detail}")
            for i in probe_ids
        ]

    out: list[ProbeOutcome] = []
    for raw_id in probe_ids:
        cid = str(raw_id or "").strip()
        if not cid:
            continue
        if cid not in probes:
            raise UnknownProbeError(cid)
        entry = probes[cid]
        if not isinstance(entry, dict):
            out.append(ProbeOutcome(cid, False, "probe_entry_not_mapping"))
            continue
        op = str(entry.get("op") or "").strip()
        if op not in _OPS:
            out.append(ProbeOutcome(cid, False, f"unsupported_op:{op}"))
            continue
        args = entry.get("args") if isinstance(entry.get("args"), dict) else {}
        # Allow top-level keys as args shorthand
        if not args:
            args = {k: v for k, v in entry.items() if k not in ("op", "args", "id")}
        ok, detail = _run_op(repo, vault_root, op, args)
        out.append(ProbeOutcome(cid, ok, detail))
    return out
