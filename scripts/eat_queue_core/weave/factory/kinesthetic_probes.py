"""Structural usability lint — code audit + optional headless smokes (proof tier: structural_lint only)."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .operator_feedback import DEFAULT_FEEDBACK_REL
from .product_kinesthetic_honesty import row_is_protected_override
from .proof_tiers import normalize_source

DEFAULT_GAME_REPO_REL = "5-Attachments/Code-Repos/genesis-mythos-alpha"
MANIFEST_REL = "1-Projects/genesis-mythos-master/Factory-DRB/Tech-Stack-Manifest-v1.yaml"

DRB_NAV = "Factory-DRB/usability-navigation-v1.md"
DRB_LAUNCH = "Factory-DRB/usability-launch-v1.md"

KINESTHETIC_IDS: tuple[str, ...] = (
    "Nav_LookWhileMove_FP",
    "Nav_LookWhileMove_DM",
    "Flow_Launch",
    "Flow_DM_Mode",
    "Flow_Ortho_Tabletop",
    "Anti_DevOnlyHUD",
    "Anti_HarnessSubstitutesPlaytest",
)


@dataclass(frozen=True)
class ProbeResult:
    checklist_id: str
    pass_: bool
    source: str
    evidence: str
    kinesthetic: bool = True

    def to_feedback_row(self) -> dict[str, Any]:
        row: dict[str, Any] = {
            "checklist_id": self.checklist_id,
            "kinesthetic": self.kinesthetic,
            "source": "structural_lint",
            "probed_at": datetime.now(timezone.utc).isoformat(),
            "notes": self.evidence[:500],
            "drb_ref": f"Factory-DRB/usability-{'launch' if self.checklist_id.startswith('Flow_') else 'navigation'}-v1.md",
        }
        if self.kinesthetic:
            # Structural lint never ships — pass stays undecided until operator/trace tier.
            row["pass"] = None
            row["structural_hint"] = self.pass_
        else:
            row["pass"] = self.pass_
        return row


def _game_repo(vault_root: Path, project_id: str | None = None) -> Path:
    from .factory_drb_paths import resolve_game_repo_path

    return vault_root / resolve_game_repo_path(vault_root, project_id)


def _read_cs(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _probe_fp_look_move(repo: Path) -> ProbeResult:
    text = _read_cs(repo / "Player/PlayerFP.cs")
    cid = "Nav_LookWhileMove_FP"
    if not text:
        return ProbeResult(cid, False, "static", "missing:Player/PlayerFP.cs")

    has_move = "GetVector(" in text and "_PhysicsProcess" in text
    has_look = "InputEventMouseMotion" in text and "_UnhandledInput" in text
    if not has_move or not has_look:
        return ProbeResult(
            cid,
            False,
            "static",
            f"parallel_paths_missing move={has_move} look={has_look}",
        )

    # Look gated on capture but move is not → effective one-at-a-time UX
    look_block = re.search(
        r"InputEventMouseMotion[\s\S]{0,400}?MouseMode\s*==\s*Input\.MouseModeEnum\.Captured",
        text,
    )
    move_block = re.search(r"_PhysicsProcess[\s\S]{0,600}?GetVector\(", text)
    move_requires_capture = bool(
        move_block and "MouseMode" in move_block.group(0) and "Captured" in move_block.group(0)
    )
    if look_block and not move_requires_capture:
        return ProbeResult(
            cid,
            False,
            "static",
            "look_requires_mouse_captured_move_does_not",
        )

    # elif chain that picks move OR look in one input handler
    if re.search(
        r"_UnhandledInput[\s\S]{0,800}if\s*\([^)]*GetVector[^)]*\)[\s\S]{0,200}else if\s*\([^)]*MouseMotion",
        text,
    ):
        return ProbeResult(cid, False, "static", "mutual_exclusion_in_single_input_handler")

    sync = _read_cs(repo / "Core/ClosedAlpha/Q3StackCameraSync.cs")
    if "player.InputEnabled = fp" in sync and "captureMouse = (fp || dm)" in sync:
        return ProbeResult(cid, True, "static", "fp_parallel_move_look_paths+camera_sync_ok")
    return ProbeResult(cid, True, "static", "fp_parallel_move_look_paths")


def _probe_dm_look_move(repo: Path) -> ProbeResult:
    text = _read_cs(repo / "Camera/SparkyDmFreeCamRig.cs")
    cid = "Nav_LookWhileMove_DM"
    if not text:
        return ProbeResult(cid, False, "static", "missing:Camera/SparkyDmFreeCamRig.cs")

    has_move = "GetVector(" in text and ("_Process" in text or "_PhysicsProcess" in text)
    has_look = "InputEventMouseMotion" in text
    if not has_move or not has_look:
        return ProbeResult(
            cid,
            False,
            "static",
            f"parallel_paths_missing move={has_move} look={has_look}",
        )

    look_requires_capture = bool(
        re.search(
            r"InputEventMouseMotion[\s\S]{0,300}?MouseMode\s*==\s*Input\.MouseModeEnum\.Captured",
            text,
        )
    )
    move_in_process = "_Process" in text and "GetVector(" in text
    look_in_unhandled = "_UnhandledInput" in text and "InputEventMouseMotion" in text

    if look_requires_capture and move_in_process and look_in_unhandled:
        return ProbeResult(
            cid,
            False,
            "static",
            "dm_look_gated_on_capture_in_UnhandledInput_move_in_Process",
        )

    return ProbeResult(cid, True, "static", "dm_parallel_move_look_paths")


def _probe_flow_launch(repo: Path) -> ProbeResult:
    cid = "Flow_Launch"
    project = repo / "project.godot"
    launch = repo / "LaunchShell.tscn"
    play = repo / "PlayRegion.tscn"
    shell_cs = _read_cs(repo / "LaunchShell.cs")

    if not project.is_file():
        return ProbeResult(cid, False, "static", "missing:project.godot")
    proj_text = project.read_text(encoding="utf-8")
    if "LaunchShell.tscn" not in proj_text:
        return ProbeResult(cid, False, "static", "main_scene_not_LaunchShell")

    if not launch.is_file() or not play.is_file():
        return ProbeResult(cid, False, "static", "missing LaunchShell or PlayRegion.tscn")

    if "PlayRegion.tscn" not in shell_cs or "ChangeSceneToFile" not in shell_cs:
        return ProbeResult(cid, False, "static", "LaunchShell missing PlayRegion scene transition")

    return ProbeResult(cid, True, "static", "LaunchShell_PlayRegion_path")


def _read_play_region(repo: Path) -> str:
    return _read_cs(repo / "PlayRegion.cs")


def _probe_flow_dm_mode(repo: Path) -> ProbeResult:
    cid = "Flow_DM_Mode"
    pr = _read_play_region(repo)
    if "Key.Tab" in pr and "TogglePerspective" in pr:
        return ProbeResult(cid, True, "static", "PlayRegion Tab→TogglePerspective")
    main = _read_cs(repo / "Main.cs")
    if "Key.Tab" in main and "TogglePerspective" in main:
        return ProbeResult(cid, True, "static", "Main Tab→TogglePerspective")
    return ProbeResult(cid, False, "static", "PlayRegion missing Tab→TogglePerspective")


def _probe_flow_ortho(repo: Path) -> ProbeResult:
    cid = "Flow_Ortho_Tabletop"
    pr = _read_play_region(repo)
    sparky = _read_cs(repo / "Camera/SparkyDmFreeCamRig.cs")
    if "Key.O" in pr and "ToggleOrthoTabletop" in pr:
        if "IsTabletopTopDown" in sparky and "TabletopPitchRadians" in sparky:
            if "-Mathf.Pi / 2f" in sparky or "-Mathf.Pi/2f" in sparky.replace(" ", ""):
                return ProbeResult(cid, True, "static", "PlayRegion ortho_top_down_tabletop_contract")
        return ProbeResult(cid, False, "static", "Sparky missing BG top-down tabletop contract")
    main = _read_cs(repo / "Main.cs")
    if "Key.O" in main and "ToggleOrthoTabletop" in main:
        if "IsTabletopTopDown" in sparky and "TabletopPitchRadians" in sparky:
            if "-Mathf.Pi / 2f" in sparky or "-Mathf.Pi/2f" in sparky.replace(" ", ""):
                return ProbeResult(cid, True, "static", "Main ortho_top_down_tabletop_contract")
    if "Key.O" not in pr and "ToggleOrthoTabletop" not in pr:
        return ProbeResult(cid, False, "static", "PlayRegion missing O→ToggleOrthoTabletop")
    return ProbeResult(cid, False, "static", "Sparky missing BG top-down tabletop contract")


def _probe_anti_dev_hud(repo: Path) -> ProbeResult:
    cid = "Anti_DevOnlyHUD"
    hud = _read_cs(repo / "UI/GameHud.cs")
    if not hud:
        return ProbeResult(cid, False, "structural_lint", "missing:UI/GameHud.cs", kinesthetic=False)
    if re.search(r"Horizon-Q3", hud, re.IGNORECASE):
        return ProbeResult(
            cid,
            False,
            "structural_lint",
            "q3_acceptance_remnant_in_GameHud",
            kinesthetic=False,
        )
    if "SetPerspectiveShellHint" in hud or "PerspectiveShellHint" in hud:
        return ProbeResult(
            cid,
            True,
            "structural_lint",
            "player_facing_hud_with_perspective_hint",
            kinesthetic=False,
        )
    return ProbeResult(cid, False, "structural_lint", "GameHud_missing_shell_hint_api", kinesthetic=False)


def _probe_anti_harness(repo: Path) -> ProbeResult:
    return ProbeResult(
        "Anti_HarnessSubstitutesPlaytest",
        True,
        "factory",
        "surface_pass_blocks_harness_only_ship",
        kinesthetic=False,
    )


def _run_godot_smoke(repo: Path, env: dict[str, str], scene: str, timeout: int = 120) -> tuple[bool, str]:
    import shutil

    godot = shutil.which("godot")
    if not godot:
        return False, "godot_not_in_path"

    try:
        proc = subprocess.run(
            [godot, "--headless", "--path", str(repo), scene],
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**dict(**__import__("os").environ), **env},
            cwd=str(repo),
        )
    except subprocess.TimeoutExpired:
        return False, "smoke_timeout"
    except OSError as exc:
        return False, f"smoke_os_error:{exc}"

    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode == 0, out[-2000:] if len(out) > 2000 else out


def _apply_smoke_overrides(repo: Path, results: dict[str, ProbeResult]) -> dict[str, ProbeResult]:
    """Refine flow probes with slice3 / ship smokes when godot is available."""
    ok3, log3 = _run_godot_smoke(
        repo,
        {"CLOSED_ALPHA_SLICE3_AUTORUN": "1"},
        "res://PlayRegion.tscn",
    )
    if ok3:
        if "toggle_dm=true" in log3 or "graybox_toggle_to_dm=true" in log3.lower():
            results["Flow_DM_Mode"] = ProbeResult(
                "Flow_DM_Mode",
                True,
                "smoke",
                "slice3_graybox_toggle_dm",
            )
        if "ortho_top_down=true" in log3.lower():
            results["Flow_Ortho_Tabletop"] = ProbeResult(
                "Flow_Ortho_Tabletop",
                True,
                "smoke",
                "slice3_ortho_top_down",
            )
    else:
        for cid in ("Flow_DM_Mode", "Flow_Ortho_Tabletop"):
            if results[cid].source == "static" and results[cid].pass_:
                results[cid] = ProbeResult(
                    cid,
                    False,
                    "smoke",
                    f"slice3_smoke_failed:{log3[:200]}",
                )

    ok_ship, log_ship = _run_godot_smoke(
        repo,
        {"CLOSED_ALPHA_SHIP_AUTORUN": "1"},
        "res://LaunchShell.tscn",
    )
    if ok_ship and "closed_alpha_ship_shell leg=true" in log_ship.lower():
        results["Flow_Launch"] = ProbeResult(
            "Flow_Launch",
            True,
            "smoke",
            "ship_shell_leg_main_exists",
        )
    elif not ok_ship and results["Flow_Launch"].pass_:
        results["Flow_Launch"] = ProbeResult(
            "Flow_Launch",
            False,
            "smoke",
            f"ship_shell_failed:{log_ship[:200]}",
        )

    return results


def run_kinesthetic_probes(
    vault_root: Path,
    *,
    run_smokes: bool = True,
    project_id: str | None = None,
    checklist_ids: tuple[str, ...] | None = None,
) -> tuple[ProbeResult, ...]:
    repo = _game_repo(vault_root, project_id)
    results: dict[str, ProbeResult] = {
        "Nav_LookWhileMove_FP": _probe_fp_look_move(repo),
        "Nav_LookWhileMove_DM": _probe_dm_look_move(repo),
        "Flow_Launch": _probe_flow_launch(repo),
        "Flow_DM_Mode": _probe_flow_dm_mode(repo),
        "Flow_Ortho_Tabletop": _probe_flow_ortho(repo),
        "Anti_DevOnlyHUD": _probe_anti_dev_hud(repo),
        "Anti_HarnessSubstitutesPlaytest": _probe_anti_harness(repo),
    }

    if run_smokes:
        results = _apply_smoke_overrides(repo, results)

    allowed = checklist_ids
    if allowed:
        allowed_set = frozenset(allowed)
        return tuple(results[cid] for cid in KINESTHETIC_IDS if cid in results and cid in allowed_set)
    return tuple(results[cid] for cid in KINESTHETIC_IDS if cid in results)


def write_operator_feedback_from_probes(
    vault_root: Path,
    probes: tuple[ProbeResult, ...],
    *,
    feedback_rel: str = DEFAULT_FEEDBACK_REL,
    respect_operator_override: bool = True,
    project_id: str | None = None,
) -> Path:
    from .factory_drb_paths import factory_drb_dir, resolve_project_id

    pid = resolve_project_id(vault_root, project_id)
    drb_rel = str(factory_drb_dir(vault_root, pid).relative_to(vault_root))
    out_path = vault_root / feedback_rel
    existing: dict[str, Any] = {}
    if out_path.is_file():
        existing = yaml.safe_load(out_path.read_text(encoding="utf-8")) or {}

    prior_rows: dict[str, dict[str, Any]] = {}
    for row in existing.get("feedback") or []:
        if isinstance(row, dict) and "checklist_id" in row:
            prior_rows[str(row["checklist_id"])] = row

    merged: list[dict[str, Any]] = []
    for probe in probes:
        prior = prior_rows.get(probe.checklist_id, {})
        prior_source = str(prior.get("source") or "")
        if respect_operator_override and row_is_protected_override(prior_source):
            if prior.get("operator_confirmed") or normalize_source(prior_source) == "operator":
                merged.append(prior)
                continue
        merged.append(probe.to_feedback_row())

    doc: dict[str, Any] = {
        "schema_version": 1,
        "project_id": pid,
        "release_tier": "closed_alpha",
        "playtest_gate": "structural_lint_and_trace",
        "last_probe_run": datetime.now(timezone.utc).isoformat(),
        "drb_refs": [
            f"{drb_rel}/{DRB_NAV}",
            f"{drb_rel}/{DRB_LAUNCH}",
        ],
        "feedback": merged,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml.dump(doc, sort_keys=False, default_flow_style=False), encoding="utf-8")
    return out_path


def run_and_sync_probes(
    vault_root: Path,
    *,
    run_smokes: bool = True,
    write_feedback: bool = True,
    project_id: str | None = None,
) -> dict[str, Any]:
    probes = run_kinesthetic_probes(vault_root, run_smokes=run_smokes, project_id=project_id)
    out_path = None
    if write_feedback:
        out_path = write_operator_feedback_from_probes(
            vault_root, probes, project_id=project_id
        )

    all_ok = all(p.pass_ for p in probes if p.kinesthetic)
    return {
        "all_ok": all_ok,
        "feedback_path": str(out_path) if out_path else None,
        "probes": [
            {
                "checklist_id": p.checklist_id,
                "pass": p.pass_,
                "source": p.source,
                "evidence": p.evidence,
                "kinesthetic": p.kinesthetic,
            }
            for p in probes
        ],
    }
