"""Ingest F6 playtest session JSONL → suggest operator_feedback playtest_trace rows."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .operator_feedback import DEFAULT_FEEDBACK_REL, KINESTHETIC_CHECKLIST_IDS
from .product_kinesthetic_honesty import row_is_protected_override

DEFAULT_GAME_REPO_REL = "5-Attachments/Code-Repos/genesis-mythos-alpha"
MANIFEST_REL = "1-Projects/godot-genesis-mythos-master/Factory-DRB/Tech-Stack-Manifest-v1.yaml"
OPERATOR_VERDICTS = frozenset({"pass", "fail", "skip", "unsure"})


@dataclass(frozen=True)
class PlaytestIngestResult:
    ok: bool
    session_path: str
    rows_updated: int
    suggestions: tuple[dict[str, Any], ...]
    detail: str
    manifest: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "ok": self.ok,
            "session_path": self.session_path,
            "rows_updated": self.rows_updated,
            "suggestions": list(self.suggestions),
            "detail": self.detail,
        }
        if self.manifest is not None:
            out["manifest"] = self.manifest
        return out


def _game_repo(vault_root: Path) -> Path:
    manifest = vault_root / MANIFEST_REL
    rel = DEFAULT_GAME_REPO_REL
    if manifest.is_file():
        data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        if isinstance(data, dict) and data.get("game_repo_path"):
            rel = str(data["game_repo_path"])
    return vault_root / rel


def _latest_session(repo: Path) -> Path | None:
    sessions = repo / ".technical/playtest/sessions"
    if not sessions.is_dir():
        return None
    files = sorted(sessions.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def _load_session_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            rows.append(obj)
    return rows


def _load_session_manifest(session_path: Path) -> dict[str, Any] | None:
    manifest_path = session_path.parent / "session_manifest.json"
    if not manifest_path.is_file():
        return None
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def _is_operator_mark(row: dict[str, Any]) -> bool:
    if str(row.get("type") or "") == "operator_mark":
        return True
    verdict = str(row.get("verdict") or "").lower()
    return verdict in OPERATOR_VERDICTS


def _aggregate_by_checklist(session_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Last operator_mark per checklist_id overrides window_pass heuristics."""
    by_id: dict[str, dict[str, Any]] = {}
    operator_marks: dict[str, dict[str, Any]] = {}

    for row in session_rows:
        cid = str(row.get("checklist_id") or "")
        if not cid:
            continue

        if _is_operator_mark(row):
            verdict = str(row.get("verdict") or "").lower()
            operator_marks[cid] = {
                "checklist_id": cid,
                "verdict": verdict,
                "note": str(row.get("note") or ""),
                "hypothesis": row.get("hypothesis"),
                "last_observation": row.get("observation"),
                "source": "playtest_operator_mark",
            }
            continue

        window_pass = bool(row.get("window_pass"))
        prior = by_id.get(cid)
        if prior is None:
            by_id[cid] = {
                "checklist_id": cid,
                "window_pass": window_pass,
                "samples": 1,
                "hypothesis": row.get("hypothesis"),
                "last_observation": row.get("observation"),
                "source": "playtest_trace",
            }
        else:
            prior["samples"] += 1
            prior["window_pass"] = prior["window_pass"] and window_pass
            prior["last_observation"] = row.get("observation")

    for cid, mark in operator_marks.items():
        by_id[cid] = mark

    return by_id


def _build_suggestion(
    cid: str,
    agg: dict[str, Any],
    session: Path,
    vault_root: Path,
    manifest: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if agg.get("source") == "playtest_operator_mark":
        verdict = str(agg.get("verdict") or "").lower()
        if verdict == "skip":
            return None
        note = str(agg.get("note") or "")
        notes = f"playtest_operator_mark verdict={verdict}"
        if note:
            notes += f" — {note}"
        notes += " — operator confirm required"
        return {
            "checklist_id": cid,
            "kinesthetic": True,
            "pass": None,
            "source": "playtest_operator_mark",
            "operator_confirmed": False,
            "operator_mark_verdict": verdict,
            "playtest_window_pass": verdict == "pass",
            "notes": notes,
            "session_path": (
                str(session.relative_to(vault_root))
                if vault_root in session.parents or session == vault_root
                else str(session)
            ),
            "ingested_at": datetime.now(timezone.utc).isoformat(),
            "slice_id": (manifest or {}).get("slice_id"),
            "session_duration_sec": _session_duration_sec(manifest),
        }

    return {
        "checklist_id": cid,
        "kinesthetic": True,
        "pass": None,
        "source": "playtest_trace",
        "operator_confirmed": False,
        "playtest_window_pass": agg["window_pass"],
        "notes": (
            f"playtest_trace suggest window_pass={agg['window_pass']} "
            f"samples={agg['samples']} — operator confirm required"
        ),
        "session_path": (
            str(session.relative_to(vault_root))
            if vault_root in session.parents or session == vault_root
            else str(session)
        ),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "slice_id": (manifest or {}).get("slice_id"),
        "session_duration_sec": _session_duration_sec(manifest),
    }


def _session_duration_sec(manifest: dict[str, Any] | None) -> int | None:
    if not manifest:
        return None
    started = manifest.get("started_at")
    ended = manifest.get("ended_at")
    if not started or not ended:
        return None
    try:
        t0 = datetime.fromisoformat(str(started).replace("Z", "+00:00"))
        t1 = datetime.fromisoformat(str(ended).replace("Z", "+00:00"))
        return max(0, int((t1 - t0).total_seconds()))
    except ValueError:
        return None


def ingest_playtest_session(
    vault_root: Path,
    *,
    session_path: Path | None = None,
    write_feedback: bool = True,
    feedback_rel: str = DEFAULT_FEEDBACK_REL,
) -> PlaytestIngestResult:
    repo = _game_repo(vault_root)
    session = session_path or _latest_session(repo)
    if session is None or not session.is_file():
        return PlaytestIngestResult(
            ok=False,
            session_path="",
            rows_updated=0,
            suggestions=(),
            detail="no_playtest_session",
        )

    session_rows = _load_session_rows(session)
    if not session_rows:
        return PlaytestIngestResult(
            ok=False,
            session_path=str(session),
            rows_updated=0,
            suggestions=(),
            detail="empty_playtest_session",
        )

    manifest = _load_session_manifest(session)
    aggregated = _aggregate_by_checklist(session_rows)
    suggestions: list[dict[str, Any]] = []
    for cid in KINESTHETIC_CHECKLIST_IDS:
        if cid not in aggregated:
            continue
        sug = _build_suggestion(cid, aggregated[cid], session, vault_root, manifest)
        if sug is not None:
            suggestions.append(sug)

    rows_updated = 0
    if write_feedback and suggestions:
        out_path = vault_root / feedback_rel
        existing: dict[str, Any] = {}
        if out_path.is_file():
            existing = yaml.safe_load(out_path.read_text(encoding="utf-8")) or {}

        merged: list[dict[str, Any]] = []
        seen: set[str] = set()
        for row in existing.get("feedback") or []:
            if not isinstance(row, dict) or "checklist_id" not in row:
                continue
            cid = str(row["checklist_id"])
            seen.add(cid)
            src = str(row.get("source") or "")
            if row_is_protected_override(src) and (
                src == "operator" or row.get("operator_confirmed")
            ):
                merged.append(row)
                continue
            if cid in aggregated:
                sug = next((s for s in suggestions if s["checklist_id"] == cid), None)
                if sug is not None:
                    merged.append({**row, **sug})
                    rows_updated += 1
                else:
                    merged.append(row)
            else:
                merged.append(row)

        for sug in suggestions:
            if sug["checklist_id"] not in seen:
                merged.append(sug)
                rows_updated += 1

        doc = dict(existing)
        doc["feedback"] = merged
        doc["last_playtest_ingest"] = datetime.now(timezone.utc).isoformat()
        doc["last_playtest_session"] = str(session)
        if manifest:
            doc["last_playtest_manifest"] = manifest
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(yaml.dump(doc, sort_keys=False, default_flow_style=False), encoding="utf-8")

    return PlaytestIngestResult(
        ok=True,
        session_path=str(session),
        rows_updated=rows_updated,
        suggestions=tuple(suggestions),
        detail="playtest_session_ingested",
        manifest=manifest,
    )
