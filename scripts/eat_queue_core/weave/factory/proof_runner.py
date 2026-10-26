"""Engine-neutral Prefer probes — ops only; project nouns live in proof-catalog.yaml.

Ops: file_exists | file_contains | field_equals | command_exits_zero |
entrypoint_result_equals | point_hits_solid | window_pointer_inject.

Each run emits ``observe_class`` from the code path taken (person|record), not
from catalog labels. File/stdout/command compares are ``record``. Window +
pointer inject is ``person``. Catalog keys cannot override.

Exit code alone is not evidence. Literal ``equals`` is not behavior-key evidence.
Runner does not know scenes, engines, or C# types. Never iterates the whole catalog.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .bindings import BindingMissingError, UNKNOWN_PROBE, load_family, require_project_id
from .observe_class import (
    OBSERVE_PERSON,
    OBSERVE_RECORD,
    WINDOW_POINTER_OP,
    classify_op_path,
)

# Record-path compare ops (stdout / file / command).
BEHAVIOR_KEY_ATTEST_OP = "entrypoint_result_equals"
POINT_HITS_SOLID_OP = "point_hits_solid"
_POINT_HITS_SOLID_COSTUME = frozenset({"equals_from", "entrypoint", "selector"})


@dataclass(frozen=True)
class ProbeOutcome:
    probe_id: str
    ok: bool
    detail: str
    op: str = ""
    observed: str = ""
    observe_class: str = OBSERVE_RECORD
    window_opened: bool = False
    pointer_injected: bool = False
    files_read: tuple[str, ...] = ()
    process_started: bool = False


@dataclass
class ProbeTranscript:
    """Harness transcript for B₂ — class comes from what ran, not author booleans."""

    probe_id: str
    op: str
    observe_class: str
    ok: bool
    detail: str
    window_opened: bool = False
    pointer_injected: bool = False
    files_read: list[str] = field(default_factory=list)
    process_started: bool = False
    observed: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "probe_id": self.probe_id,
            "op": self.op,
            "observe_class": self.observe_class,
            "ok": self.ok,
            "detail": self.detail,
            "window_opened": self.window_opened,
            "pointer_injected": self.pointer_injected,
            "files_read": list(self.files_read),
            "process_started": self.process_started,
            "observed": self.observed,
        }


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
        POINT_HITS_SOLID_OP,
        WINDOW_POINTER_OP,
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
    if isinstance(point, (list, tuple)) and len(point) >= 2:
        xs, ys = str(point[0]).strip(), str(point[1]).strip()
        ban.extend([xs, ys])
        return ["--point", xs, ys], ban, ""
    if isinstance(point, dict) and "x" in point and "y" in point:
        xs, ys = str(point.get("x")).strip(), str(point.get("y")).strip()
        ban.extend([xs, ys])
        return ["--point", xs, ys], ban, ""
    return [], [], "entrypoint_result_equals:selector_not_index_or_point"


def _parse_point(raw: Any) -> tuple[float, float] | None:
    if isinstance(raw, (list, tuple)) and len(raw) >= 2:
        try:
            return float(raw[0]), float(raw[1])
        except (TypeError, ValueError):
            return None
    if isinstance(raw, dict) and "x" in raw and "y" in raw:
        try:
            return float(raw["x"]), float(raw["y"])
        except (TypeError, ValueError):
            return None
    return None


def _solid_contains(solid: dict[str, Any], x: float, y: float) -> bool:
    """Axis-aligned rect: x0,y0,x1,y1 (inclusive)."""
    try:
        x0, y0 = float(solid["x0"]), float(solid["y0"])
        x1, y1 = float(solid["x1"]), float(solid["y1"])
    except (KeyError, TypeError, ValueError):
        return False
    lo_x, hi_x = (x0, x1) if x0 <= x1 else (x1, x0)
    lo_y, hi_y = (y0, y1) if y0 <= y1 else (y1, y0)
    return lo_x <= x <= hi_x and lo_y <= y <= hi_y


def _expected_id_from_bounds(repo: Path, bounds_rel: str, x: float, y: float) -> tuple[str | None, str]:
    """Compute solid id from geometry. Does not read selection_id / commit_id / equals_from."""
    path = repo / bounds_rel
    if not path.is_file():
        return None, f"point_hits_solid:bounds_missing:{bounds_rel}"
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        return None, f"point_hits_solid:bounds_unreadable:{exc}"
    solids = raw.get("solids") if isinstance(raw, dict) else None
    if not isinstance(solids, list):
        return None, "point_hits_solid:bounds_missing_solids"
    hits: list[str] = []
    for row in solids:
        if not isinstance(row, dict):
            continue
        sid = str(row.get("id") or "").strip()
        if not sid:
            continue
        if _solid_contains(row, x, y):
            hits.append(sid)
    if not hits:
        return None, "point_hits_solid:point_outside_all_bounds"
    if len(hits) > 1:
        return None, "point_hits_solid:ambiguous_hit"
    return hits[0], "ok"


def _meta_record(
    *,
    files_read: list[str] | None = None,
    process_started: bool = False,
    observed: str = "",
) -> dict[str, Any]:
    return {
        "observe_class": OBSERVE_RECORD,
        "window_opened": False,
        "pointer_injected": False,
        "files_read": list(files_read or []),
        "process_started": process_started,
        "observed": observed,
    }


def _meta_person(
    *,
    window_opened: bool,
    pointer_injected: bool,
    process_started: bool = False,
    observed: str = "",
) -> dict[str, Any]:
    return {
        "observe_class": OBSERVE_PERSON,
        "window_opened": window_opened,
        "pointer_injected": pointer_injected,
        "files_read": [],
        "process_started": process_started,
        "observed": observed,
    }


def _run_op(
    repo: Path, vault_root: Path, op: str, args: dict[str, Any]
) -> tuple[bool, str, dict[str, Any]]:
    """Run one op. Returns (ok, detail, transcript_meta). Class from code path."""
    if op == "file_exists":
        rel = str(args.get("path") or "").strip()
        if not rel:
            return False, "file_exists:missing_path", _meta_record()
        target = repo / rel
        ok = target.is_file() or target.is_dir()
        return ok, f"file_exists:{rel}", _meta_record(files_read=[rel] if ok else [])

    if op == "file_contains":
        rel = str(args.get("path") or "").strip()
        needle = str(args.get("contains") or "")
        if not rel:
            return False, "file_contains:missing_path", _meta_record()
        path = repo / rel
        if not path.is_file():
            return False, f"file_contains:missing:{rel}", _meta_record()
        text = path.read_text(encoding="utf-8", errors="replace")
        return needle in text, f"file_contains:{rel}", _meta_record(files_read=[rel])

    if op == "field_equals":
        rel = str(args.get("path") or "").strip()
        key = str(args.get("key") or "").strip()
        expect = args.get("equals")
        if not rel or not key:
            return False, "field_equals:missing_path_or_key", _meta_record()
        path = repo / rel
        if not path.is_file():
            path = vault_root / rel
        if not path.is_file():
            return False, f"field_equals:missing:{rel}", _meta_record()
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(raw, dict):
            return False, f"field_equals:not_mapping:{rel}", _meta_record(files_read=[rel])
        actual = raw.get(key)
        return (
            actual == expect,
            f"field_equals:{key}",
            _meta_record(files_read=[rel]),
        )

    if op == "command_exits_zero":
        argv = args.get("argv")
        if not isinstance(argv, list) or not argv:
            return False, "command_exits_zero:missing_argv", _meta_record()
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
            return False, f"command_exits_zero:error:{exc}", _meta_record(process_started=True)
        return (
            proc.returncode == 0,
            f"command_exits_zero:rc={proc.returncode}",
            _meta_record(process_started=True),
        )

    if op == BEHAVIOR_KEY_ATTEST_OP:
        if "equals" in args and args.get("equals") not in (None, ""):
            return (
                False,
                "entrypoint_result_equals:literal_equals_forbidden",
                _meta_record(),
            )
        equals_from = args.get("equals_from")
        if not isinstance(equals_from, dict):
            return False, "entrypoint_result_equals:missing_equals_from", _meta_record()
        expect, err = _resolve_equals_from(repo, equals_from)
        if expect is None:
            return False, err, _meta_record(
                files_read=[str(equals_from.get("path") or "")]
            )

        argv = args.get("argv")
        if not isinstance(argv, list) or not argv:
            return False, "entrypoint_result_equals:missing_argv", _meta_record()
        sel_extra, ban_tokens, sel_err = _selector_argv(args.get("selector"))
        if sel_err:
            return False, sel_err, _meta_record()

        cmd = [str(x) for x in argv] + sel_extra
        files = [str(equals_from.get("path") or "")]
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(repo),
                capture_output=True,
                text=True,
                timeout=int(args.get("timeout_sec") or 120),
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return (
                False,
                f"entrypoint_result_equals:error:{exc}",
                _meta_record(files_read=files, process_started=True),
            )
        if proc.returncode != 0:
            return (
                False,
                f"entrypoint_result_equals:rc={proc.returncode}",
                _meta_record(files_read=files, process_started=True),
            )
        observed = (proc.stdout or "").strip()
        if observed and observed in ban_tokens:
            return (
                False,
                "entrypoint_result_equals:echoed_selector_arg",
                _meta_record(files_read=files, process_started=True, observed=observed),
            )
        ok = observed == expect
        return (
            ok,
            f"entrypoint_result_equals:observed={observed!r};expect={expect!r}",
            _meta_record(files_read=files, process_started=True, observed=observed),
        )

    if op == POINT_HITS_SOLID_OP:
        # Still a record path (stdout compare). Costume keys fail the op.
        if any(k in args for k in _POINT_HITS_SOLID_COSTUME):
            return False, "point_hits_solid:costume_forbidden", _meta_record()
        bounds_rel = str(args.get("bounds") or "").strip()
        if not bounds_rel:
            return False, "point_hits_solid:missing_bounds", _meta_record()
        parsed = _parse_point(args.get("point"))
        if parsed is None:
            return False, "point_hits_solid:missing_point", _meta_record()
        x, y = parsed
        expect, err = _expected_id_from_bounds(repo, bounds_rel, x, y)
        if expect is None:
            return False, err, _meta_record(files_read=[bounds_rel])
        argv = args.get("argv")
        if not isinstance(argv, list) or not argv:
            return False, "point_hits_solid:missing_argv", _meta_record(files_read=[bounds_rel])
        xs, ys = str(x), str(y)
        cmd = [str(a) for a in argv] + ["--point", xs, ys]
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(repo),
                capture_output=True,
                text=True,
                timeout=int(args.get("timeout_sec") or 120),
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return (
                False,
                f"point_hits_solid:error:{exc}",
                _meta_record(files_read=[bounds_rel], process_started=True),
            )
        if proc.returncode != 0:
            return (
                False,
                f"point_hits_solid:rc={proc.returncode}",
                _meta_record(files_read=[bounds_rel], process_started=True),
            )
        observed = (proc.stdout or "").strip()
        if observed in (xs, ys, f"{xs},{ys}", f"{xs} {ys}"):
            return (
                False,
                "point_hits_solid:echoed_point",
                _meta_record(
                    files_read=[bounds_rel], process_started=True, observed=observed
                ),
            )
        ok = observed == expect
        return (
            ok,
            f"point_hits_solid:observed={observed!r};expect={expect!r}",
            _meta_record(
                files_read=[bounds_rel], process_started=True, observed=observed
            ),
        )

    if op == WINDOW_POINTER_OP:
        # Person path: must open a window and inject pointer. No stdout-id compare.
        argv = args.get("argv")
        if not isinstance(argv, list) or not argv:
            return False, "window_pointer_inject:missing_argv", _meta_person(
                window_opened=False, pointer_injected=False
            )
        parsed = _parse_point(args.get("point"))
        if parsed is None:
            return False, "window_pointer_inject:missing_point", _meta_person(
                window_opened=False, pointer_injected=False
            )
        x, y = parsed
        cmd = [str(a) for a in argv] + ["--window", "--inject-pointer", str(x), str(y)]
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(repo),
                capture_output=True,
                text=True,
                timeout=int(args.get("timeout_sec") or 120),
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return (
                False,
                f"window_pointer_inject:error:{exc}",
                _meta_person(
                    window_opened=False, pointer_injected=False, process_started=True
                ),
            )
        out = (proc.stdout or "") + "\n" + (proc.stderr or "")
        window_opened = "window_opened=1" in out or "WINDOW_OPEN" in out
        pointer_injected = "pointer_injected=1" in out or "POINTER_INJECT" in out
        ok = proc.returncode == 0 and window_opened and pointer_injected
        return (
            ok,
            f"window_pointer_inject:rc={proc.returncode};window={window_opened};pointer={pointer_injected}",
            _meta_person(
                window_opened=window_opened,
                pointer_injected=pointer_injected,
                process_started=True,
                observed=(proc.stdout or "").strip(),
            ),
        )

    return False, f"unknown_op:{op}", _meta_record()


def _entry_args(entry: dict[str, Any]) -> dict[str, Any]:
    args = entry.get("args") if isinstance(entry.get("args"), dict) else {}
    if not args:
        args = {k: v for k, v in entry.items() if k not in ("op", "args", "id")}
    return args if isinstance(args, dict) else {}


def classify_catalog_probe(
    vault_root: Path, project_id: str, probe_id: str
) -> str | None:
    """Dry-classify probe observe class from runner op path. None if missing."""
    op = probe_op_for_id(vault_root, project_id, probe_id)
    if not op:
        return None
    return classify_op_path(op, None)


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
            out.append(
                ProbeOutcome(
                    cid,
                    False,
                    f"unsupported_op:{op}",
                    op=op,
                    observe_class=classify_op_path(op),
                )
            )
            continue
        args = _entry_args(entry)
        ok, detail, meta = _run_op(repo, vault_root, op, args)
        observed = str(meta.get("observed") or "")
        out.append(
            ProbeOutcome(
                cid,
                ok,
                detail,
                op=op,
                observed=observed,
                observe_class=str(meta.get("observe_class") or OBSERVE_RECORD),
                window_opened=bool(meta.get("window_opened")),
                pointer_injected=bool(meta.get("pointer_injected")),
                files_read=tuple(str(x) for x in (meta.get("files_read") or []) if x),
                process_started=bool(meta.get("process_started")),
            )
        )
    return out


def run_named_probes_with_transcript(
    vault_root: Path,
    project_id: str,
    probe_ids: list[str] | tuple[str, ...],
) -> tuple[list[ProbeOutcome], list[ProbeTranscript]]:
    """Run probes and return outcomes plus B₂ transcripts."""
    outcomes = run_named_probes(vault_root, project_id, probe_ids)
    transcripts: list[ProbeTranscript] = []
    for o in outcomes:
        transcripts.append(
            ProbeTranscript(
                probe_id=o.probe_id,
                op=o.op,
                observe_class=o.observe_class,
                ok=o.ok,
                detail=o.detail,
                window_opened=o.window_opened,
                pointer_injected=o.pointer_injected,
                files_read=list(o.files_read),
                process_started=o.process_started,
                observed=o.observed,
            )
        )
    return outcomes, transcripts


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
