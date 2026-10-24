"""Engine-neutral Prefer probes — ops only; project nouns live in proof-catalog.yaml.

Ops: file_exists | file_contains | field_equals | command_exits_zero |
entrypoint_result_equals.

Behavior-key Success uses entrypoint_result_equals only: runner reads expected id
from write-target state (``equals_from``), invokes Prefer-named entrypoint with a
selector (index/point — never the id), and compares stdout to that id.
Catalog must not store expected stdout. Exit code alone is not evidence.
Literal ``equals`` is not behavior-key evidence.
Runner does not know scenes, engines, or C# types. Never iterates the whole catalog.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .bindings import BindingMissingError, UNKNOWN_PROBE, load_family, require_project_id

# Sole op that may attest Prefer behavior_keys (operation + compared value).
BEHAVIOR_KEY_ATTEST_OP = "entrypoint_result_equals"


@dataclass(frozen=True)
class ProbeOutcome:
    probe_id: str
    ok: bool
    detail: str
    op: str = ""
    observed: str = ""


class UnknownProbeError(KeyError):
    def __init__(self, probe_id: str) -> None:
        super().__init__(probe_id)
        self.code = UNKNOWN_PROBE
        self.probe_id = probe_id


_OPS = frozenset(
    {
        "file_exists",
        "file_contains",
        "field_equals",
        "command_exits_zero",
        BEHAVIOR_KEY_ATTEST_OP,
    }
)


def _repo_root(vault_root: Path, project_id: str) -> Path:
    from .bindings import game_repo_path

    return vault_root.resolve() / game_repo_path(vault_root, project_id)


def _dotted_get(data: Any, dotted: str) -> Any:
    cur: Any = data
    for part in str(dotted or "").split("."):
        if not part:
            continue
        if isinstance(cur, list) and part.isdigit():
            idx = int(part)
            if idx < 0 or idx >= len(cur):
                return None
            cur = cur[idx]
        elif isinstance(cur, dict):
            if part not in cur:
                return None
            cur = cur[part]
        else:
            return None
    return cur


def _resolve_equals_from(repo: Path, equals_from: dict[str, Any]) -> tuple[str | None, str]:
    """Load expected compare value from write-target state. Not from catalog literal."""
    rel = str(equals_from.get("path") or "").strip()
    key = str(equals_from.get("key") or "").strip()
    if not rel or not key:
        return None, "entrypoint_result_equals:equals_from_missing_path_or_key"
    path = repo / rel
    if not path.is_file():
        return None, f"entrypoint_result_equals:state_missing:{rel}"
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        return None, f"entrypoint_result_equals:state_unreadable:{exc}"
    val = _dotted_get(raw, key)
    if val is None or val is False:
        # Allow 0 / empty string? empty string is invalid id; 0 might be ok as int
        if val == 0:
            return "0", "ok"
        return None, f"entrypoint_result_equals:state_key_missing:{key}"
    return str(val).strip(), "ok"


def _selector_argv(selector: Any) -> tuple[list[str], list[str], str]:
    """Build argv extras for selector. Returns (extra_argv, echo_ban_tokens, error).

    Selector is index or point — never the solid id.
    """
    if not isinstance(selector, dict) or not selector:
        return [], [], "entrypoint_result_equals:selector_missing"
    ban: list[str] = []
    if "index" in selector and selector.get("index") is not None:
        idx = str(selector.get("index")).strip()
        ban.append(idx)
        return ["--index", idx], ban, ""
    point = selector.get("point")
    if isinstance(point, dict) and "x" in point and "y" in point:
        xs, ys = str(point.get("x")).strip(), str(point.get("y")).strip()
        ban.extend([xs, ys])
        return ["--point", xs, ys], ban, ""
    return [], [], "entrypoint_result_equals:selector_not_index_or_point"


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

    if op == BEHAVIOR_KEY_ATTEST_OP:
        # Expected value from write-target state at probe time — not catalog stdout.
        # Literal catalog ``equals`` is a stamp — refuse.
        if "equals" in args and args.get("equals") not in (None, ""):
            return False, "entrypoint_result_equals:literal_equals_forbidden"
        equals_from = args.get("equals_from")
        if not isinstance(equals_from, dict):
            return False, "entrypoint_result_equals:missing_equals_from"
        expect, err = _resolve_equals_from(repo, equals_from)
        if expect is None:
            return False, err

        argv = args.get("argv")
        if not isinstance(argv, list) or not argv:
            return False, "entrypoint_result_equals:missing_argv"
        sel_extra, ban_tokens, sel_err = _selector_argv(args.get("selector"))
        if sel_err:
            return False, sel_err

        cmd = [str(x) for x in argv] + sel_extra
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(repo),
                capture_output=True,
                text=True,
                timeout=int(args.get("timeout_sec") or 120),
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return False, f"entrypoint_result_equals:error:{exc}"
        if proc.returncode != 0:
            return False, f"entrypoint_result_equals:rc={proc.returncode}"
        observed = (proc.stdout or "").strip()
        # Echoing selector args is not identity.
        if observed and observed in ban_tokens:
            return False, "entrypoint_result_equals:echoed_selector_arg"
        ok = observed == expect
        return ok, f"entrypoint_result_equals:observed={observed!r};expect={expect!r}"

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
        observed = ""
        if detail.startswith("entrypoint_result_equals:observed="):
            # detail carries observed for audit; ProbeOutcome.observed is the raw compare side
            observed = detail.split("observed=", 1)[-1].strip().strip("'\"")
        out.append(ProbeOutcome(cid, ok, detail, op=op, observed=observed))
    return out


def probe_op_for_id(
    vault_root: Path, project_id: str, probe_id: str
) -> str | None:
    """Return catalog op for probe_id, or None if missing."""
    pid = require_project_id(project_id)
    try:
        catalog = load_family(vault_root, pid, "proof-catalog")
    except BindingMissingError:
        return None
    probes = catalog.get("probes")
    if not isinstance(probes, dict):
        return None
    entry = probes.get(str(probe_id or "").strip())
    if not isinstance(entry, dict):
        return None
    return str(entry.get("op") or "").strip() or None
