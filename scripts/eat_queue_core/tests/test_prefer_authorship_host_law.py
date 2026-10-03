"""Constitution-grade Prefer / proxy subordination / dispatch preflight tests."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

from eat_queue_core.weave.factory.drop_contract_base import (
    check_depends_on_drops,
    ensure_drop_manifest_skeleton,
    is_bootstrap_stub_manifest,
    register_lane_drop,
)
from eat_queue_core.weave.factory.factory_dispatch_preflight import (
    SHELL_ERA_CHECKLIST_IDS,
    check_armed_paths_owned,
    check_shell_era_checklist_vs_worldgen,
    extract_armed_required_paths,
    run_factory_dispatch_preflight,
)
from eat_queue_core.weave.factory.module_fit_lint import (
    count_core_touches,
    count_file_diff_lines,
    run_module_fit_pass,
)
from eat_queue_core.weave.factory.implicit_intent_bind import write_implicit_intent_bind
from eat_queue_core.weave.factory.factory_pq_stage import (
    armed_slice_authority_note,
    factory_lane_entries_from_dispatch,
)
from eat_queue_core.weave.factory.prefer_authorship_contract import (
    DUAL_VISUAL_DO_NOT_WAIVE,
    NEGATIVE_EXAMPLES,
    PRODUCT_PREFER_DO_NOT_WAIVE,
    authorship_overlay_markdown,
    dual_visual_violations_from_evidence,
    resolve_step1_lock,
    run_prefer_authorship_pass,
    scan_dual_visual_evidence,
    scan_topology_evidence,
    slice_requires_prefer_authorship,
)
from eat_queue_core.weave.user_story.product_factory_continue import (
    append_product_factory_continue,
)


def _init_git(repo: Path) -> None:
    subprocess.run(["git", "init"], cwd=repo, capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo,
        capture_output=True,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=repo,
        capture_output=True,
        check=True,
    )


def _write_cfg(vault: Path, body: str) -> None:
    cfg = vault / "3-Resources"
    cfg.mkdir(parents=True, exist_ok=True)
    (cfg / "Second-Brain-Config.md").write_text(
        f"```yaml\n{body}\n```\n",
        encoding="utf-8",
    )


class PreferAuthorshipTests(unittest.TestCase):
    def test_slice_detection(self) -> None:
        self.assertTrue(
            slice_requires_prefer_authorship("alpha0_worldgen_terrain3d_feed_r3")
        )
        self.assertTrue(
            slice_requires_prefer_authorship(
                "row_ux_world_generation_r1_d4",
                {"ask_id": "alpha0_worldgen_terrain3d_feed"},
            )
        )
        self.assertFalse(slice_requires_prefer_authorship("alpha_core_loop_v1"))

    def test_overlay_contains_durable_negatives(self) -> None:
        md = authorship_overlay_markdown(slice_id="alpha0_worldgen_dualgrid_sparky_r1")
        self.assertIn("Hot Wheels", md)
        self.assertIn("Y19Mw5YsgjI", md)
        for ex in NEGATIVE_EXAMPLES:
            self.assertIn(ex["refuse"], md)

    def test_authorship_fail_on_cam_yank_pattern(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cite = root / (
                "Ingest/Resources/"
                "Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01.md"
            )
            cite.parent.mkdir(parents=True)
            cite.write_text("# cite\n", encoding="utf-8")
            repo = root / "game"
            host = repo / "Systems/Worldgen"
            host.mkdir(parents=True)
            (host / "DualGridCraftHost.cs").write_text(
                "void TryPickCell() {\n"
                "  // place tile then yank focus\n"
                "  SetFocusWorld(pickedCell);\n"
                "}\n",
                encoding="utf-8",
            )
            result = run_prefer_authorship_pass(
                root,
                game_repo_rel="game",
                changed_paths=("Systems/Worldgen/DualGridCraftHost.cs",),
                job={
                    "slice_id": "alpha0_worldgen_terrain3d_feed_r3",
                    "prefer_proof": "layer_split",
                    "do_not_waive": ["Terrain3D_prefer_proof", "prefer_authorship_pass"],
                },
            )
            self.assertTrue(result.applicable)
            self.assertFalse(result.ok)
            self.assertTrue(
                any("craft_cam_recenter_on_place" in v for v in result.little_val.anti_pattern_violations),
                result.little_val.anti_pattern_violations,
            )

    def test_waive_cannot_silence_product_seat(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cite = root / (
                "Ingest/Resources/"
                "Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01.md"
            )
            cite.parent.mkdir(parents=True)
            cite.write_text("# cite\n", encoding="utf-8")
            (root / "game").mkdir()
            result = run_prefer_authorship_pass(
                root,
                game_repo_rel="game",
                job={
                    "slice_id": "alpha0_worldgen_dualgrid_sparky_r1",
                    "waive_shell_era_seats": True,
                    "waive_seats": ["prefer_authorship_pass"],
                    "prefer_proof": "x",
                    "do_not_waive": ["Terrain3D_prefer_proof"],
                },
            )
            self.assertFalse(result.ok)
            self.assertTrue(
                any("waive_forbidden" in v for v in result.little_val.anti_pattern_violations)
            )


SLICE_S1 = "alpha0_townscaper_tutorial_s1_occupancy_r1"
PROJECT_ID = "genesis-mythos-master"

_POINTS_ONLY_LATTICE = """\
namespace Genesis.Core.WorldGen;

public static class Hex19OccupancyLattice
{
	public const int PointCount = 19;
	public static readonly Vector2I[] Points = BuildRingPoints(rings: 2);
	public static bool Contains(Vector2I axial) => PointSet.Contains(axial);
}
"""

_POINTS_ONLY_HOST = """\
public partial class DualGridCraftHost : Node3D
{
	public int LatticePointCount => Hex19OccupancyLattice.PointCount;

	private void BuildHex19Visuals()
	{
		foreach (var axial in Hex19OccupancyLattice.Points)
			_gridRoot.AddChild(new MeshInstance3D { Mesh = MakeDiskMarker(0.32f) });
	}
}
"""

_LATTICE_GRAPH_LATTICE = """\
namespace Genesis.Core.WorldGen;

public static class Hex19OccupancyLattice
{
	public static readonly Vector2I[] Vertices = BuildVertices(rings: 2);
	public static readonly (Vector2I A, Vector2I B)[] NeighborEdges = BuildEdges(Vertices);
	public static readonly HexCell[] HexCells = BuildCells(Vertices, NeighborEdges);

	public static Vector3[] CellCorners(HexCell cell) => cell.CellVertices;
}
"""

_LATTICE_GRAPH_HOST = """\
public partial class DualGridCraftHost : Node3D
{
	private void BuildLatticeGraph()
	{
		foreach (var edge in Hex19OccupancyLattice.NeighborEdges)
			_lines.AddLine(edge.A, edge.B);
		foreach (var hexCell in Hex19OccupancyLattice.HexCells)
			_faces.AddFan(Hex19OccupancyLattice.CellCorners(hexCell));
	}
}
"""


def _seed_prefer_vault(root: Path, *, lattice: str, host: str) -> None:
    cite = root / (
        "Ingest/Resources/Townscaper-Dual-Grid-Authorship-YT-Y19Mw5YsgjI-2026-10-01.md"
    )
    cite.parent.mkdir(parents=True, exist_ok=True)
    cite.write_text("# cite\n", encoding="utf-8")
    repo = root / "game"
    (repo / "Core/WorldGen").mkdir(parents=True, exist_ok=True)
    (repo / "Systems").mkdir(parents=True, exist_ok=True)
    (repo / "Core/WorldGen/Hex19OccupancyLattice.cs").write_text(lattice, encoding="utf-8")
    (repo / "Systems/DualGridCraftHost.cs").write_text(host, encoding="utf-8")


def _prefer_job() -> dict:
    return {
        "slice_id": SLICE_S1,
        "project_id": PROJECT_ID,
        "prefer_proof": "layer_split",
        "do_not_waive": list(PRODUCT_PREFER_DO_NOT_WAIVE),
    }


class PreferTopologySeatTests(unittest.TestCase):
    """Phase 1 exit gate — lattice graph, not point cloud."""

    def test_1_points_only_live_scan_fails_prefer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _seed_prefer_vault(root, lattice=_POINTS_ONLY_LATTICE, host=_POINTS_ONLY_HOST)
            write_implicit_intent_bind(
                root,
                slice_id=SLICE_S1,
                project_id=PROJECT_ID,
                explicit_ask="hex-19 occupancy grid with 19 points",
            )
            result = run_prefer_authorship_pass(
                root, game_repo_rel="game", job=_prefer_job()
            )
            violations = result.little_val.anti_pattern_violations
            self.assertFalse(result.ok, result.detail)
            self.assertTrue(
                any(v.startswith("points_as_grid") for v in violations), violations
            )
            self.assertTrue(
                any(v.startswith("count_equals_topology") for v in violations), violations
            )
            self.assertTrue(
                any(v.startswith("explicit_met_implicit_miss") for v in violations),
                violations,
            )
            # Structured evidence, not a bare bool.
            ev = result.topology_evidence or {}
            self.assertTrue(ev.get("point_signals"), ev)
            self.assertFalse(ev.get("has_edges"), ev)
            self.assertFalse(ev.get("has_faces_or_cells"), ev)
            self.assertIn("Systems/DualGridCraftHost.cs", ev.get("files_scanned") or [])
            self.assertIn(
                "Core/WorldGen/Hex19OccupancyLattice.cs", ev.get("files_scanned") or []
            )
            self.assertIn("topology_evidence", result.to_dict())

    def test_2_edges_and_cells_pass_topology_axis(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _seed_prefer_vault(
                root, lattice=_LATTICE_GRAPH_LATTICE, host=_LATTICE_GRAPH_HOST
            )
            write_implicit_intent_bind(
                root,
                slice_id=SLICE_S1,
                project_id=PROJECT_ID,
                explicit_ask="hex-19 occupancy grid with 19 points",
            )
            result = run_prefer_authorship_pass(
                root, game_repo_rel="game", job=_prefer_job()
            )
            violations = result.little_val.anti_pattern_violations
            for code in ("points_as_grid", "count_equals_topology", "explicit_met_implicit_miss"):
                self.assertFalse(
                    any(v.startswith(code) for v in violations), violations
                )
            ev = result.topology_evidence or {}
            self.assertTrue(ev.get("has_edges"), ev)
            self.assertTrue(ev.get("has_faces_or_cells"), ev)
            self.assertEqual(ev.get("missing_axes"), [])
            self.assertTrue(result.ok, result.detail)

    def test_3_missing_bind_fails_prefer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _seed_prefer_vault(
                root, lattice=_LATTICE_GRAPH_LATTICE, host=_LATTICE_GRAPH_HOST
            )
            result = run_prefer_authorship_pass(
                root, game_repo_rel="game", job=_prefer_job()
            )
            violations = result.little_val.anti_pattern_violations
            self.assertFalse(result.ok, result.detail)
            self.assertTrue(
                any("implicit_bind" in v for v in violations), violations
            )
            # No bind → no topology axis claim either way.
            self.assertIsNone(result.topology_evidence)

    def test_4_staging_injects_armed_packet_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            briefs = root / f"1-Projects/{PROJECT_ID}/Factory-DRB/slice-briefs"
            briefs.mkdir(parents=True)
            brief_rel = f"1-Projects/{PROJECT_ID}/Factory-DRB/slice-briefs/{SLICE_S1}.md"
            armed = {
                "slice_id": SLICE_S1,
                "ask_id": "alpha0_townscaper_tutorial",
                "umbrella_ask_id": "alpha_architecture_half_b",
                "brief_path": brief_rel,
                "locks": {"step1_authorship": {"law": "hex19_lattice_graph"}},
            }
            (briefs / f"{SLICE_S1}.armed.yaml").write_text(
                yaml.dump(armed), encoding="utf-8"
            )
            entries = factory_lane_entries_from_dispatch(
                root,
                lane="module",
                packet={"project_id": PROJECT_ID, "planner_hints": {}},
                run_id="run-armed-1",
                jobs=[{"lane_id": "module", "game_repo_rel": "game", "factory_name": "f"}],
                slice_id=SLICE_S1,
            )
            self.assertEqual(len(entries), 1, entries)
            params = entries[0]["params"]
            self.assertEqual(
                params["armed_packet_path"],
                f"1-Projects/{PROJECT_ID}/Factory-DRB/slice-briefs/{SLICE_S1}.armed.yaml",
            )
            self.assertEqual(params["half_b_brief_path"], brief_rel)
            self.assertEqual(params["ask_id"], "alpha0_townscaper_tutorial")
            self.assertTrue(params["step1_authorship"])
            for code in ("prefer_authorship_pass", "points_as_grid", "count_equals_topology"):
                self.assertIn(code, params["do_not_waive"])

            # Armed state never blocks staging — GO is an operator chat kickoff.
            self.assertEqual(armed_slice_authority_note(armed, slice_id=SLICE_S1), "")
            self.assertEqual(
                armed_slice_authority_note(
                    {**armed, "do_not_auto_dispatch": True}, slice_id=SLICE_S1
                ),
                "",
            )
            # A divergent slice is reported for review, not refused.
            self.assertTrue(
                armed_slice_authority_note(
                    armed, slice_id="row_ux_world_generation_r1_d6"
                ).startswith("armed_slice_divergence")
            )

    def test_5_bool_step1_lock_does_not_false_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _seed_prefer_vault(
                root, lattice=_LATTICE_GRAPH_LATTICE, host=_LATTICE_GRAPH_HOST
            )
            write_implicit_intent_bind(
                root,
                slice_id=SLICE_S1,
                project_id=PROJECT_ID,
                explicit_ask="hex-19 occupancy grid with 19 points",
            )
            briefs = root / f"1-Projects/{PROJECT_ID}/Factory-DRB/slice-briefs"
            briefs.mkdir(parents=True)
            armed_rel = (
                f"1-Projects/{PROJECT_ID}/Factory-DRB/slice-briefs/{SLICE_S1}.armed.yaml"
            )
            (root / armed_rel).write_text(
                yaml.dump({"slice_id": SLICE_S1, "step1_authorship": True}),
                encoding="utf-8",
            )
            result = run_prefer_authorship_pass(
                root,
                game_repo_rel="game",
                job={**_prefer_job(), "armed_packet_path": armed_rel},
            )
            violations = result.little_val.anti_pattern_violations
            self.assertNotIn("armed_packet_missing_step1_authorship_lock", violations)
            self.assertIn("step1_authorship_bool_underspecified", result.warnings)
            self.assertTrue(result.ok, result.detail)

            # Dict shape is the preferred form — no warning.
            lock, warnings = resolve_step1_lock(
                {"locks": {"step1_authorship": {"law": "hex19_lattice_graph"}}}
            )
            self.assertTrue(lock)
            self.assertEqual(warnings, [])
            # No lock at all is still a hard fail for a worldgen armed packet.
            self.assertEqual(resolve_step1_lock({"slice_id": SLICE_S1}), ({}, []))


class ArmedPacketAuthorityTests(unittest.TestCase):
    def test_project_armed_pointer_resolves_for_other_slices(self) -> None:
        from eat_queue_core.weave.factory.factory_pq_stage import (
            resolve_authority_armed_packet,
        )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            drb = root / f"1-Projects/{PROJECT_ID}/Factory-DRB"
            (drb / "slice-briefs").mkdir(parents=True)
            armed_rel = (
                f"1-Projects/{PROJECT_ID}/Factory-DRB/slice-briefs/{SLICE_S1}.armed.yaml"
            )
            (root / armed_rel).write_text(
                yaml.dump({"slice_id": SLICE_S1}),
                encoding="utf-8",
            )
            (drb / "factory-project.yaml").write_text(
                yaml.dump({"project_id": PROJECT_ID, "armed_packet": armed_rel}),
                encoding="utf-8",
            )
            # A stale cell ticks under its own slice_id — armed law still resolves.
            rel, armed = resolve_authority_armed_packet(
                root, project_id=PROJECT_ID, slice_id="row_ux_world_generation_r1_d6"
            )
            self.assertEqual(rel, armed_rel)
            self.assertEqual(armed.get("slice_id"), SLICE_S1)
            # Divergence is advisory; it must not refuse staging.
            self.assertTrue(
                armed_slice_authority_note(
                    armed, slice_id="row_ux_world_generation_r1_d6"
                ).startswith("armed_slice_divergence")
            )


class TopologyEvidenceTests(unittest.TestCase):
    def test_required_live_files_always_scanned(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _seed_prefer_vault(root, lattice=_POINTS_ONLY_LATTICE, host=_POINTS_ONLY_HOST)
            # Change set names an unrelated file — required LIVE surfaces still scanned.
            ev = scan_topology_evidence(
                root / "game", changed_paths=("Systems/Unrelated.cs",)
            )
            self.assertEqual(ev["required_live_files_absent"], [])
            self.assertTrue(ev["points_only"])
            self.assertEqual(sorted(ev["missing_axes"]), ["edges", "faces_cells"])

    def test_comment_claims_are_not_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            claim = (
                "// This builds neighbor edges and hex cell faces.\n"
                'public static string Note = "edges and HexCells and CellCorners";\n'
                "public const int PointCount = 19;\n"
                "public static readonly Vector2I[] Points = new Vector2I[19];\n"
            )
            _seed_prefer_vault(root, lattice=claim, host=claim)
            ev = scan_topology_evidence(root / "game")
            self.assertFalse(ev["has_edges"], ev)
            self.assertFalse(ev["has_faces_or_cells"], ev)
            self.assertTrue(ev["points_only"], ev)


class DispatchPreflightTests(unittest.TestCase):
    def test_shell_era_checklist_fails_on_worldgen(self) -> None:
        v = check_shell_era_checklist_vs_worldgen(
            slice_id="alpha0_worldgen_terrain3d_feed_r3",
            job={},
            checklist_ids=["Nav_LookWhileMove_FP", "Flow_Launch", "Anti_DevOnlyHUD"],
        )
        self.assertIn("shell_era_checklist_on_worldgen_prefer:Nav_LookWhileMove_FP", v)
        self.assertIn("shell_era_checklist_on_worldgen_prefer:Flow_Launch", v)
        self.assertTrue(all("Anti_DevOnlyHUD" not in x for x in v))
        self.assertTrue(SHELL_ERA_CHECKLIST_IDS)

    def test_armed_path_unowned(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pid = "genesis-mythos-master"
            drb = root / f"1-Projects/{pid}/Factory-DRB"
            drb.mkdir(parents=True)
            (drb / "FACTORY_ZONES.yaml").write_text(
                yaml.dump(
                    {
                        "zones": {
                            "module": {"write": ["Systems/**", "Core/**"]},
                        }
                    }
                ),
                encoding="utf-8",
            )
            armed = {
                "worldgen_entry_scene": "res://scenes/WorldgenCraft.tscn",
                "terrain3d_prep": {"live_addon_present": True},
            }
            (drb / "slice-briefs").mkdir(parents=True)
            armed_path = drb / "slice-briefs/test.armed.yaml"
            armed_path.write_text(yaml.dump(armed), encoding="utf-8")
            job = {
                "slice_id": "alpha0_worldgen_dualgrid_sparky_r1",
                "armed_packet_path": str(armed_path.relative_to(root)),
                "zone_write": ["Systems/**"],
                "project_id": pid,
            }
            violations = check_armed_paths_owned(
                root, job=job, zone_write=["Systems/**"], project_id=pid
            )
            self.assertTrue(
                any("armed_path_unowned" in v for v in violations),
                violations,
            )

    def test_armed_path_owned_when_zones_cover(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pid = "genesis-mythos-master"
            drb = root / f"1-Projects/{pid}/Factory-DRB"
            drb.mkdir(parents=True)
            (drb / "FACTORY_ZONES.yaml").write_text(
                yaml.dump(
                    {
                        "zones": {
                            "module": {
                                "write": [
                                    "Systems/**",
                                    "scenes/**",
                                    "addons/terrain_3d/**",
                                ]
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            armed = {
                "worldgen_entry_scene": "res://scenes/WorldgenCraft.tscn",
                "terrain3d_prep": {"live_addon_present": True},
            }
            required = extract_armed_required_paths(armed)
            self.assertIn("scenes/WorldgenCraft.tscn", required)
            (drb / "slice-briefs").mkdir(parents=True)
            armed_path = drb / "slice-briefs/test.armed.yaml"
            armed_path.write_text(yaml.dump(armed), encoding="utf-8")
            _write_cfg(
                root,
                f"factory_orchestrator:\n  project_id: {pid}\n"
                f"  manifest_path: 1-Projects/{pid}/Factory-DRB/Tech-Stack-Manifest-v1.yaml\n",
            )
            job = {
                "slice_id": "alpha0_worldgen_dualgrid_sparky_r1",
                "armed_packet_path": str(armed_path.relative_to(root)),
                "zone_write": ["Systems/**", "scenes/**", "addons/terrain_3d/**"],
                "project_id": pid,
                "checklist_ids": ["Anti_DevOnlyHUD"],
            }
            write_implicit_intent_bind(
                root,
                slice_id=job["slice_id"],
                project_id=pid,
                explicit_ask="worldgen dualgrid sparky terrain3d feed",
            )
            result = run_factory_dispatch_preflight(
                root,
                job=job,
                project_id=pid,
                zone_write=job["zone_write"],
                checklist_ids=job["checklist_ids"],
            )
            self.assertTrue(result.ok, result.to_dict())

    def test_identity_drift_legacy_project_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_cfg(
                root,
                "factory_orchestrator:\n  project_id: genesis-mythos-master\n",
            )
            (root / "1-Projects/genesis-mythos-master/Factory-DRB").mkdir(parents=True)
            result = run_factory_dispatch_preflight(
                root,
                job={
                    "project_id": "godot-genesis-mythos-master",
                    "slice_id": "alpha_core_loop_v1",
                },
                project_id="godot-genesis-mythos-master",
            )
            self.assertFalse(result.ok)
            self.assertTrue(
                any("identity_drift" in v for v in result.violations),
                result.violations,
            )


class BudgetDiffLineTests(unittest.TestCase):
    def test_counts_diff_not_whole_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "game"
            core = repo / "Core"
            core.mkdir(parents=True)
            _init_git(repo)
            big = core / "Big.cs"
            big.write_text("line\n" * 200, encoding="utf-8")
            subprocess.run(["git", "add", "Core/Big.cs"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-m", "base"], cwd=repo, check=True)
            # Small edit
            big.write_text("line\n" * 200 + "// one more\n", encoding="utf-8")
            delta = count_file_diff_lines(repo, "Core/Big.cs")
            self.assertLess(delta, 50, f"expected small diff, got {delta}")
            self.assertEqual(count_core_touches(repo, ("Core/Big.cs",)), delta)

    def test_budget_advisory_on_prefer_product(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "game"
            core = repo / "Core"
            core.mkdir(parents=True)
            _init_git(repo)
            f = core / "X.cs"
            f.write_text("a\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-m", "base"], cwd=repo, check=True)
            f.write_text("a\n" * 600, encoding="utf-8")
            charter_dir = root / "1-Projects/genesis-mythos-master/Factory-DRB/lane-charters"
            # module_fit loads charter optionally — empty ok
            result = run_module_fit_pass(
                root,
                lane_id="module",
                game_repo_rel="game",
                changed_paths=("Core/X.cs",),
                job={
                    "slice_id": "alpha0_worldgen_terrain3d_feed_r3",
                    "host_touch_budget": 10,
                    "prefer_proof": "layer_split",
                },
            )
            self.assertTrue(result.ok, result.detail)
            self.assertTrue(result.budget_exceeded)
            self.assertTrue(result.budget_is_advisory_only)


class BootstrapDropTests(unittest.TestCase):
    def test_bootstrap_stub_not_ready(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "game"
            repo.mkdir()
            ensure_drop_manifest_skeleton(repo, "adc")
            data = yaml.safe_load(
                (repo / "assets/_factory/manifest.yaml").read_text(encoding="utf-8")
            )
            self.assertTrue(is_bootstrap_stub_manifest(data))
            ok, violations = check_depends_on_drops(repo, ["adc"])
            self.assertFalse(ok)
            self.assertTrue(
                any("bootstrap_stub_not_ready" in v for v in violations),
                violations,
            )

    def test_real_drop_satisfies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "game"
            repo.mkdir()
            out = register_lane_drop(
                repo,
                lane_id="asset",
                slice_id="s1",
                receipt_id="receipt-real-1",
                paths=["assets/foo.gltf"],
            )
            self.assertTrue(out.get("ok"))
            ok, violations = check_depends_on_drops(repo, ["adc"])
            self.assertTrue(ok, violations)


class ContinueDedupeTests(unittest.TestCase):
    def test_suppress_when_prefer_seats_unmet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle = root / ".technical/parallel/godot"
            bundle.mkdir(parents=True)
            (bundle / "prompt-queue.jsonl").write_text("", encoding="utf-8")
            # minimal product factory state
            pf_dir = root / "1-Projects/genesis-mythos-master/Roadmap"
            pf_dir.mkdir(parents=True)
            out = append_product_factory_continue(
                root,
                lane="godot",
                project_id="genesis-mythos-master",
                run_id="run-1",
                prefer_product_seats_met=False,
            )
            self.assertTrue(out.get("skipped"))
            self.assertEqual(out.get("reason"), "prefer_product_seats_unmet")

    def test_dedupe_open_continue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle = root / ".technical/parallel/godot"
            bundle.mkdir(parents=True)
            existing = {
                "id": "pfc-existing",
                "mode": "PRODUCT_FACTORY_CONTINUE",
                "params": {"product_factory_run_id": "run-dup", "project_id": "genesis-mythos-master"},
            }
            (bundle / "prompt-queue.jsonl").write_text(
                json.dumps(existing) + "\n", encoding="utf-8"
            )
            # done_when / product factory — allow continue path
            out = append_product_factory_continue(
                root,
                lane="godot",
                project_id="genesis-mythos-master",
                run_id="run-dup",
                force=True,
            )
            self.assertTrue(out.get("skipped"))
            self.assertEqual(out.get("reason"), "continue_already_queued")


class DualVisualPreferHardenTests(unittest.TestCase):
    """stretch_as_variant / over_neighbor_paint — r1 failure pattern defense."""

    _STRETCH_HOST = """
using Godot;
public partial class DualGridCraftHost : Node3D
{
	public enum DualVisualFamily { Empty = 0, Edge = 1, Corner = 2, Full = 3 }
	public MeshLibrary EnsureShapeDistinctDualMeshLibrary() => new MeshLibrary();
	public (bool Ok, string Summary) ProveDualVisualVariants() => (true, "ok");
	private ArrayMesh MakeShapeDistinctDualVariant(int faceIndex, DualVisualFamily family, int rot90, bool mirror)
	{
		var corners = _organicMesh.FaceCornersLocal(faceIndex);
		return CommitDualFamilyMesh(family, corners);
	}
	private ArrayMesh CommitDualFamilyMesh(DualVisualFamily family, Vector3[] c) => new ArrayMesh();
	public int UpdateFourDualSlots(Vector2I occupancy)
	{
		foreach (var fi in faces)
			EnsureOrganicDualCellMesh(fi);
		return faces.Count;
	}
}
"""

    _DISCRETE_HOST = """
using Godot;
public partial class DualGridCraftHost : Node3D
{
	public const int MaxDualCellsPerLogicFlip = 4;
	public enum DualVisualFamily { Empty = 0, Edge = 1, Corner = 2, Full = 3 }
	public MeshLibrary EnsureShapeDistinctDualMeshLibrary() => new MeshLibrary();
	public (bool Ok, string Summary) ProveDualVisualVariants() => (true, "ok");
	public (bool Ok, string Summary) ProveNeighborhoodCardinality() => (true, "ok");
	private void PlaceDiscreteDualLibraryItem(int faceIndex, DualVisualFamily family, int rot90, bool mirror)
	{
		var lib = EnsureShapeDistinctDualMeshLibrary();
		var mesh = lib.GetItemMesh((int)family);
		// discrete_meshlibrary_item place — translate + yaw only
	}
	private ArrayMesh MakeShapeDistinctDualVariant(int faceIndex, DualVisualFamily family, int rot90, bool mirror)
		=> PlaceUnitThenReturn(family);
	private ArrayMesh CommitDualFamilyMesh(DualVisualFamily family, Vector3[] c) => new ArrayMesh();
	private ArrayMesh PlaceUnitThenReturn(DualVisualFamily family) => new ArrayMesh();
	public int UpdateFourDualSlots(Vector2I occupancy)
	{
		if (faces.Count > MaxDualCellsPerLogicFlip)
			return 0; // refuse=over_neighbor_paint
		foreach (var fi in faces.Take(4))
			EnsureOrganicDualCellMesh(fi);
		return Math.Min(faces.Count, 4);
	}
}
"""

    def test_do_not_waive_includes_stretch_and_over_neighbor(self) -> None:
        for code in ("stretch_as_variant", "over_neighbor_paint", "gray_ramp_only", "inspiration_shape_miss"):
            self.assertIn(code, PRODUCT_PREFER_DO_NOT_WAIVE)
            self.assertIn(code, DUAL_VISUAL_DO_NOT_WAIVE)
        refuses = {ex["refuse"] for ex in NEGATIVE_EXAMPLES}
        self.assertIn("stretch_as_variant", refuses)
        self.assertIn("over_neighbor_paint", refuses)

    def test_stretch_host_fails_dual_visual_seat(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "game"
            (repo / "Systems").mkdir(parents=True)
            (repo / "Systems/DualGridCraftHost.cs").write_text(
                self._STRETCH_HOST, encoding="utf-8"
            )
            ev = scan_dual_visual_evidence(repo)
            self.assertTrue(ev["has_shape_distinct"], ev)
            self.assertFalse(ev["has_discrete_library_place"], ev)
            self.assertTrue(ev["stretch_as_variant"], ev)
            viols = dual_visual_violations_from_evidence(ev)
            self.assertTrue(any(v.startswith("stretch_as_variant") for v in viols), viols)
            self.assertTrue(any(v.startswith("over_neighbor_paint") for v in viols), viols)

    def test_discrete_host_passes_new_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "game"
            (repo / "Systems").mkdir(parents=True)
            (repo / "Systems/DualGridCraftHost.cs").write_text(
                self._DISCRETE_HOST, encoding="utf-8"
            )
            ev = scan_dual_visual_evidence(repo)
            self.assertTrue(ev["has_discrete_library_place"], ev)
            self.assertTrue(ev["has_neighborhood_cardinality_gate"], ev)
            self.assertFalse(ev["stretch_as_variant"], ev)
            self.assertFalse(ev["over_neighbor_paint"], ev)
            viols = dual_visual_violations_from_evidence(ev)
            self.assertFalse(any(v.startswith("stretch_as_variant") for v in viols), viols)
            self.assertFalse(any(v.startswith("over_neighbor_paint") for v in viols), viols)


class DualNeighborhoodPreferHardenTests(unittest.TestCase):
    """unstable_dual_neighborhood / stamp_as_dual — graph-before-art defense."""

    _STAMP_HOST = """
using Godot;
public partial class DualGridCraftHost : Node3D
{
	public const int MaxDualCellsPerLogicFlip = 4;
	public Error SetCellFill(Vector2I cell, CellFill fill)
	{
		EnsureFilledOrganicFaceMesh(cell);
		UpdateFourDualSlots(cell);
		return Error.Ok;
	}
	private void PlaceDiscreteDualLibraryItem(int faceIndex, DualVisualFamily family, int rot90, bool mirror)
	{
		var corners = _organicMesh.FaceCornersLocal(faceIndex);
		var centre = (corners[0] + corners[1] + corners[2] + corners[3]) * 0.25f;
		mi.Position = centre;
	}
	public int UpdateFourDualSlots(Vector2I occupancy)
	{
		if (faces.Count > MaxDualCellsPerLogicFlip)
		{
			AlphaFactoryLog.Emit("craft.refuse", "over_neighbor_paint", "warn");
		}
		foreach (var fi in faces.Take(MaxDualCellsPerLogicFlip))
			EnsureOrganicDualCellMesh(fi);
		return Math.Min(faces.Count, 4);
	}
	private void RefreshDebugDualCellIds(int vertexIndex) { }
}
"""

    _STABLE_HOST = """
using Godot;
public partial class DualGridCraftHost : Node3D
{
	public const int MaxDualCellsPerLogicFlip = 4;
	public (bool Ok, string Summary) ProveStableDualNeighborhood() => (true, "stable");
	private void RefreshDebugDualCellIds(int vertexIndex) { }
	public int UpdateFourDualSlots(Vector2I occupancy)
	{
		if (faces.Count > MaxDualCellsPerLogicFlip)
			return 0; // refuse=over_neighbor_paint hard
		foreach (var fi in faces.Take(4))
			EnsureOrganicDualCellMesh(fi);
		return Math.Min(faces.Count, 4);
	}
}
"""

    def test_do_not_waive_includes_neighborhood_codes(self) -> None:
        from eat_queue_core.weave.factory.prefer_authorship_contract import (
            DUAL_NEIGHBORHOOD_DO_NOT_WAIVE,
            PRODUCT_PREFER_DO_NOT_WAIVE,
            NEGATIVE_EXAMPLES,
        )

        for code in ("unstable_dual_neighborhood", "stamp_as_dual", "over_neighbor_paint"):
            self.assertIn(code, PRODUCT_PREFER_DO_NOT_WAIVE)
            self.assertIn(code, DUAL_NEIGHBORHOOD_DO_NOT_WAIVE)
        refuses = {ex["refuse"] for ex in NEGATIVE_EXAMPLES}
        self.assertIn("unstable_dual_neighborhood", refuses)
        self.assertIn("stamp_as_dual", refuses)

    def test_stamp_host_fails_neighborhood_seat(self) -> None:
        from eat_queue_core.weave.factory.prefer_authorship_contract import (
            dual_neighborhood_violations_from_evidence,
            scan_dual_neighborhood_evidence,
        )

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "game"
            (repo / "Systems").mkdir(parents=True)
            (repo / "Systems/DualGridCraftHost.cs").write_text(
                self._STAMP_HOST, encoding="utf-8"
            )
            ev = scan_dual_neighborhood_evidence(repo)
            self.assertTrue(ev["stamp_as_dual"], ev)
            self.assertTrue(ev["unstable_dual_neighborhood"], ev)
            viols = dual_neighborhood_violations_from_evidence(ev)
            self.assertTrue(any(v.startswith("stamp_as_dual") for v in viols), viols)
            self.assertTrue(
                any(v.startswith("unstable_dual_neighborhood") for v in viols), viols
            )
            self.assertTrue(any(v.startswith("over_neighbor_paint") for v in viols), viols)

    def test_stable_host_passes_neighborhood_gates(self) -> None:
        from eat_queue_core.weave.factory.prefer_authorship_contract import (
            dual_neighborhood_violations_from_evidence,
            scan_dual_neighborhood_evidence,
        )

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "game"
            (repo / "Systems").mkdir(parents=True)
            (repo / "Systems/DualGridCraftHost.cs").write_text(
                self._STABLE_HOST, encoding="utf-8"
            )
            ev = scan_dual_neighborhood_evidence(repo)
            self.assertTrue(ev["has_prove_stable_neighborhood"], ev)
            self.assertTrue(ev["has_hard_refuse_over_neighbor"], ev)
            self.assertFalse(ev["stamp_as_dual"], ev)
            viols = dual_neighborhood_violations_from_evidence(ev)
            self.assertFalse(any(v.startswith("stamp_as_dual") for v in viols), viols)
            self.assertFalse(
                any(v.startswith("unstable_dual_neighborhood") for v in viols), viols
            )
            self.assertFalse(any(v.startswith("over_neighbor_paint") for v in viols), viols)

    def test_deferred_dual_visual_does_not_arm_visual_seat(self) -> None:
        from eat_queue_core.weave.factory.prefer_authorship_contract import (
            armed_requires_dual_neighborhood,
            armed_requires_dual_visual,
        )

        armed = {
            "slice_id": "alpha0_stalberg_dual_neighborhood_r1",
            "mode": "fix_dual_neighborhood_stable_four_cell_ownership",
            "refuse_codes": [
                "unstable_dual_neighborhood",
                "over_neighbor_paint",
                "stamp_as_dual",
            ],
            "locks": {"dual_neighborhood": {"law": "stable"}, "dual_visual": {"deferred": True}},
        }
        self.assertTrue(armed_requires_dual_neighborhood(armed))
        self.assertFalse(armed_requires_dual_visual(armed))



class DualLatticePreferHardenTests(unittest.TestCase):
    """primary_face_as_dual — refuse primary-face 2×2 as dual Success."""

    _PRIMARY_FACE_HOST = """
using Godot;
public partial class DualGridCraftHost : Node3D
{
	public const int MaxDualCellsPerLogicFlip = 4;
	private readonly Dictionary<int, List<int>> _vertexToFaces = new();
	public (bool Ok, string Summary) ProveStableDualNeighborhood() => (true, "stable");
	private void RefreshDebugDualCellIds(int vertexIndex) { }
	public IReadOnlyList<int> OwnedDualFaceIndices(int vertexIndex)
	{
		return _vertexToFaces[vertexIndex];
	}
	private void EnsureOrganicDualCellMesh(int faceIndex)
	{
		var key = $"org_{faceIndex}";
		mi.Name = $"DualCell_{key}_owned";
	}
	public int UpdateFourDualSlots(Vector2I occupancy)
	{
		if (faces.Count > MaxDualCellsPerLogicFlip)
			return 0;
		foreach (var fi in faces)
			EnsureOrganicDualCellMesh(fi);
		return faces.Count;
	}
}
"""

    _LATTICE_HOST = """
using Godot;
using Genesis.Core.WorldGen;
public partial class DualGridCraftHost : Node3D
{
	public const int MaxDualCellsPerLogicFlip = 4;
	private OrganicDualOffsetLattice? _dualLattice;
	public (bool Ok, string Summary) ProveStableDualNeighborhood() => (true, "stable_dual_lattice");
	private void RefreshDebugDualCellIds(int vertexIndex) { }
	public IReadOnlyList<string> OwnedDualCellKeys(int vertexIndex)
	{
		return OrganicDualOffsetLattice.DualCellsTouching(vertexIndex, _dualLattice)
			.Select(c => c.Key).ToList();
	}
	public string LastOwnedDualCellsCsv { get; private set; } = "";
	public int UpdateFourDualSlots(Vector2I occupancy)
	{
		var cells = OrganicDualOffsetLattice.DualCellsTouching(occupancy.X, _dualLattice);
		if (cells.Count > MaxDualCellsPerLogicFlip)
			return 0;
		foreach (var cell in cells)
			EnsureHalfStepDualCellMesh(cell);
		return cells.Count;
	}
	private void EnsureHalfStepDualCellMesh(OrganicDualOffsetLattice.DualCell cell)
	{
		mi.Mesh = MakeHalfStepDualCellMesh(cell);
		mi.Name = $"DualCell_{cell.Key}";
	}
}
"""

    _LATTICE_TYPE = """
namespace Genesis.Core.WorldGen;
public static class OrganicDualOffsetLattice
{
	public readonly struct DualCell
	{
		public string Key => "d_0";
		public Vector3 LocalCentre;
	}
	public static bool IsHalfStepOffset(DualCell cell) => true;
	public static List<DualCell> DualCellsTouching(int vertex, object lattice) => new();
	public static Vector3[] VarignonMidpoints(Vector3[] corners) => corners;
}
"""

    def test_do_not_waive_includes_primary_face_as_dual(self) -> None:
        from eat_queue_core.weave.factory.prefer_authorship_contract import (
            DUAL_LATTICE_DO_NOT_WAIVE,
            DUAL_NEIGHBORHOOD_DO_NOT_WAIVE,
            PRODUCT_PREFER_DO_NOT_WAIVE,
            NEGATIVE_EXAMPLES,
        )

        self.assertIn("primary_face_as_dual", PRODUCT_PREFER_DO_NOT_WAIVE)
        self.assertIn("primary_face_as_dual", DUAL_NEIGHBORHOOD_DO_NOT_WAIVE)
        self.assertIn("primary_face_as_dual", DUAL_LATTICE_DO_NOT_WAIVE)
        refuses = {ex["refuse"] for ex in NEGATIVE_EXAMPLES}
        self.assertIn("primary_face_as_dual", refuses)

    def test_primary_face_host_fails_when_lattice_required(self) -> None:
        from eat_queue_core.weave.factory.prefer_authorship_contract import (
            dual_neighborhood_violations_from_evidence,
            scan_dual_neighborhood_evidence,
        )

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "game"
            (repo / "Systems").mkdir(parents=True)
            (repo / "Systems/DualGridCraftHost.cs").write_text(
                self._PRIMARY_FACE_HOST, encoding="utf-8"
            )
            ev = scan_dual_neighborhood_evidence(repo)
            self.assertTrue(ev["primary_face_as_dual"], ev)
            viols = dual_neighborhood_violations_from_evidence(
                ev, require_dual_lattice=True
            )
            self.assertTrue(any(v.startswith("primary_face_as_dual") for v in viols), viols)

    def test_lattice_host_passes_primary_face_gate(self) -> None:
        from eat_queue_core.weave.factory.prefer_authorship_contract import (
            dual_neighborhood_violations_from_evidence,
            scan_dual_neighborhood_evidence,
            armed_requires_dual_lattice,
        )

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "game"
            (repo / "Systems").mkdir(parents=True)
            (repo / "Core/WorldGen").mkdir(parents=True)
            (repo / "Systems/DualGridCraftHost.cs").write_text(
                self._LATTICE_HOST, encoding="utf-8"
            )
            (repo / "Core/WorldGen/OrganicDualOffsetLattice.cs").write_text(
                self._LATTICE_TYPE, encoding="utf-8"
            )
            ev = scan_dual_neighborhood_evidence(repo)
            self.assertTrue(ev["has_organic_dual_offset_lattice"], ev)
            self.assertTrue(ev["has_dual_cells_touching"], ev)
            self.assertTrue(ev["has_half_step_offset_proof"], ev)
            self.assertFalse(ev["primary_face_as_dual"], ev)
            viols = dual_neighborhood_violations_from_evidence(
                ev, require_dual_lattice=True
            )
            self.assertFalse(any(v.startswith("primary_face_as_dual") for v in viols), viols)

        armed = {
            "slice_id": "alpha0_stalberg_dual_lattice_r1",
            "mode": "fix_dual_lattice_half_step_offset_ownership",
            "refuse_codes": ["primary_face_as_dual", "unstable_dual_neighborhood"],
            "locks": {"dual_lattice": {"law": "half_step"}, "dual_visual": {"deferred": True}},
        }
        self.assertTrue(armed_requires_dual_lattice(armed))

class EatLivenessHelperTests(unittest.TestCase):
    def test_escalation_requires_exit(self) -> None:
        from eat_queue_core.weave.factory.factory_lane_runner import (
            _escalation_requires_eat_exit,
        )

        esc = {
            "escalated": True,
            "heals": [
                {
                    "tier": "L2",
                    "healed": False,
                    "action": "escalate_review_seat",
                }
            ],
        }
        self.assertTrue(_escalation_requires_eat_exit(esc))
        self.assertFalse(_escalation_requires_eat_exit({"escalated": False, "heals": []}))


if __name__ == "__main__":
    unittest.main()
