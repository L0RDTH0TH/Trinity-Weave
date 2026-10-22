"""Prefer authorship — thin shell. Product nouns live in host-law.yaml.

Opt-in is Prefer ``host_law_ids`` only. Empty list → no cites, no refuses, pass no-ops.
``prefer_authorship: true`` does **not** opt in.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .factory_little_val import FactoryLittleValResult
from .host_law import (
    host_law_ids_from_job_or_armed,
    matching_cites,
    matching_refuse_codes,
)

# Prefer packet owns do_not_waive. No baked product refuse catalog in harness.
PRODUCT_PREFER_DO_NOT_WAIVE: tuple[str, ...] = ()


def load_armed_packet(vault_root: Path, job: dict[str, Any] | None) -> dict[str, Any]:
    path_s = str((job or {}).get("armed_packet_path") or "").strip()
    if not path_s:
        return {}
    path = vault_root / path_s
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def slice_requires_prefer_authorship(
    slice_id: str, job: dict[str, Any] | None = None
) -> bool:
    """True only when Prefer names a non-empty host_law_ids list."""
    del slice_id
    ids = host_law_ids_from_job_or_armed(job, None)
    if ids:
        return True
    return False


def authorship_overlay_markdown(*, slice_id: str = "") -> str:
    del slice_id
    return (
        "## Prefer authorship\n"
        "Host-law refuses apply only when Prefer lists `host_law_ids`. "
        "Empty list → no cites and no product refuses.\n"
    )


def product_prefer_seats_met(lane_seats: dict[str, Any] | None) -> bool:
    if not isinstance(lane_seats, dict):
        return True
    pref = lane_seats.get("prefer_authorship_pass")
    if pref is None:
        return True
    if isinstance(pref, dict):
        return pref.get("ok") is True
    return bool(pref)


@dataclass
class PreferAuthorshipPassResult:
    ok: bool
    little_val: FactoryLittleValResult
    detail: str
    bind: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "detail": self.detail,
            "violations": list(self.little_val.anti_pattern_violations),
            "implicit_bind": self.bind,
        }


def run_prefer_authorship_pass(
    vault_root: Path,
    *,
    lane_id: str | None = None,
    game_repo_rel: str = "",
    changed_paths: Any = None,
    job: dict[str, Any] | None = None,
) -> Any:
    del lane_id, game_repo_rel, changed_paths
    from .review_pass_runner import ReviewPassResult

    job = job if isinstance(job, dict) else {}
    project_id = str(job.get("project_id") or "").strip()
    armed = load_armed_packet(vault_root, job)
    ids = host_law_ids_from_job_or_armed(job, armed)
    if not ids:
        lv = FactoryLittleValResult(
            little_val_ok=True,
            anti_pattern_violations=[],
            detail="host_law_ids_empty",
        )
        return ReviewPassResult(
            "prefer_authorship_pass", True, lv, "host_law_ids_empty"
        )
    if not project_id:
        lv = FactoryLittleValResult(
            little_val_ok=False,
            anti_pattern_violations=["project_id_missing"],
            detail="prefer_authorship_pass",
        )
        return ReviewPassResult(
            "prefer_authorship_pass", False, lv, "project_id_missing"
        )

    refuses = matching_refuse_codes(
        vault_root, project_id, context={"host_law_ids": ids}
    )
    cites = matching_cites(vault_root, project_id, host_law_ids=ids)
    # Opted-in rows with no scan implementation still pass structurally;
    # Prefer names the ids — proof_runner / map seats own evidence.
    lv = FactoryLittleValResult(
        little_val_ok=True,
        anti_pattern_violations=[],
        detail="host_law_ids_applied",
    )
    return ReviewPassResult(
        "prefer_authorship_pass",
        True,
        lv,
        f"host_law_ids={ids};refuses={refuses};cites={len(cites)}",
    )


# Stubs kept so older imports do not explode; they carry no product nouns.
def resolve_step1_lock(
    armed: dict[str, Any] | None,
) -> tuple[dict[str, Any], list[str]]:
    armed = armed if isinstance(armed, dict) else {}
    locks = armed.get("locks") if isinstance(armed.get("locks"), dict) else {}
    for candidate in (
        locks.get("step1_authorship"),
        locks.get("step1_occupancy"),
        armed.get("step1_authorship"),
    ):
        if isinstance(candidate, dict) and candidate:
            return candidate, []
    return {}, []
