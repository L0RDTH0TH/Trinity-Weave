---
title: Investigation — dual geometry rethink (face-centroid dual verts)
created: 2026-10-04
updated: 2026-10-04
project-id: genesis-mythos-master
status: investigation_complete
claim_class: investigation
factory_greenlit: false
aborts: alpha0_stalberg_dual_rebind_r1
superseded_by_ticket: alpha0_stalberg_dual_face_centroid_r1
series_id: alpha0_stalberg_grid_kernel_r1
tags: [factory, investigation, dual-grid, townscaper, feed_for_greenlit_ticket]
---

# Investigation — dual geometry rethink

**Scope:** investigation complete. Greenlit follow-on: [[alpha0_stalberg_dual_face_centroid_r1]].
**Kill:** [[alpha0_stalberg_dual_rebind_r1]] marked **aborted / superseded** — no Success.

## Operator hypothesis (accepted as investigation frame)

The second (dual) grid is a **copy of the primal grid, half-offset / scaled** so that **dual vertices sit at the centres of the main grid’s faces**. LIVE vertex-centred duals (`LocalCentre = owner.Position`, corners = edge-neighbor primal verts) cannot place second-grid vertices in the middle of main cells.

---

## 1. What LIVE / Hex19 / Townscaper actually do

### A. LIVE organic — `OrganicDualOffsetLattice` (current, after dual_rebind)

| Property | LIVE value |
|----------|------------|
| One dual tile per | Valence-4 **primal Vertex** (`owner`) |
| `LocalCentre` | `owner.Position` (primal vertex) |
| Corners | `CardinalNeighbors(owner)` — **other primal Vertices** |
| Mesh ring | `FaceCornersLocal` → those primal corner positions (not face centroids) |
| `IsHalfStepOffset` | **Requires** centre ≈ owner vertex; **refuses** corner set equal to any primal face |
| `DualCellsTouching(P)` | Duals owned by edge-neighbors of P that list P as corner |

Cite: `Core/WorldGen/OrganicDualOffsetLattice.cs` `Rebuild` (~L128–158), `IsHalfStepOffset` (~L284–298); `Systems/DualGridCraftHost.cs` `EnsureHalfStepDualCellMesh` (~L634–649).

**Verdict vs hypothesis:** FAIL. Second-grid corners live on **primal vertices**, not face centres. Centre-on-vertex matches one half of oskar’s wording (“primary vertex = dual cell centre”) but the **corner geometry is inverted** relative to Stage 6 extraction.

### B. Hex19 tutorial lattice — `Hex19DualOffsetLattice`

| Property | Hex19 value |
|----------|-------------|
| Dual cell corners | Four **occupancy / logic sites** (axial) |
| `LocalCentre` | Mean of those four sites → **half-step between logic points** |
| `IsHalfStepOffset` | **Refuses** centre coincident with any occupancy site |
| `DualCellsTouching(occupancy)` | Exactly four dual cells that list that site as a corner |

Cite: `Core/WorldGen/Hex19DualOffsetLattice.cs` L8–16, L75–108, L205–218.

On a regular square occupancy lattice, that centre **is** the unit-face centroid. Dual corners = logic verts; dual centre = face centre. This is the **opposite polarity** of LIVE organic’s `IsHalfStepOffset`.

### C. Townscaper / oskar grammar (vault cites)

**Craft grammar** ([[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]]): player edits logic points; refresh four dual quads that share that point; dual quads are “offset by half a cell.”

**Oskar concept** ([[references/oskar-procedure/01-concept]]):

> The dual grid is a copy of the grid offset by half a cell: every *vertex* of the primary grid becomes the *center* of a dual cell, and vice versa. … take a vertex, collect the **centroids of every quad touching it**, sort them by angle, and that polygon … is the dual cell.

**Oskar Stage 6** ([[references/oskar-procedure/02-grid-algorithm]] § Stage 6):

> Extract dual cells … centroids of incident quads … that polygon is the **dual cell**.

So the precise object is:

| Dual lattice element | Geometric locus |
|----------------------|-----------------|
| **Dual vertex** (corner of a dual cell) | **Primal face centroid** |
| **Dual cell** (paintable / soft polygon) | Cycle of face centroids around one **primal vertex**; dual cell **centre** ≈ that primal vertex |
| **Vice versa** | Primal vertex ↔ dual cell centre; primal face centre ↔ dual vertex |

LIVE currently keeps centre≈vertex but sets corners to **edge-neighbor vertices** instead of **incident face centroids**. That is the core geometry bug.

---

## 2. Algorithm sketch on `OrganicMeshGraph`

Given primal `OrganicMeshGraph` with `Vertex` / `Edge` / `Face` (all-quad):

```text
# Dual vertices
for each Face F:
  DualVertex(F) = centroid(F.Corners)   # Vector2/3 on craft plane
  # identity key: face id or sorted corner vertex ids

# Dual edges (optional explicit graph)
for each primal Edge E shared by Faces F1, F2:
  connect DualVertex(F1) — DualVertex(F2)

# Dual cells (oskar Stage 6 — one per interior primal vertex)
for each Vertex V with incident Faces F0..Fk (k≥3, ideally 4):
  corners = [DualVertex(Fi) for Fi in FacesTouchingVertex(V)]
  sort corners CCW about V.Position
  DualCell(V) = polygon(corners)       # centre ≈ V
  # corners are FACE CENTROIDS — not neighbor Vertices

# Authorship
LogicPoint store stays on primal Vertex ids (corner-state).
```

**Half-offset / “copy scaled” reading:** the dual vertex set is the primal face set relocated to face centroids (classic planar dual). Dual cells are the faces of that dual graph (stars around primal verts). No requirement to literally scale a mesh copy; incidence extraction is enough.

**Varignon note:** `VarignonMidpoints` (edge midpoints of a face) is a *different* inset construction. Oskar Stage 6 wants **face centroids as dual vertices**, not edge midpoints as dual corners. Edge midpoints can still appear in subdivision (docs/02), not as the dual cell corner set.

---

## 3. Click → update-four under that model

| Role | Binding |
|------|---------|
| Logic / paint authority | Still **primal Vertex** (corner-state bit) |
| Click target | Nearest logic Vertex V |
| Dual cell of V | Polygon of **centroids of FacesTouchingVertex(V)** (≤4 on interior quads) |
| MeshLibrary / corner-typed tile (Hex19-style) | Typically one visual tile per **primal Face** (or per dual unit whose four corners are that face’s logic verts); centre = face centroid; corners sample the four Vertex states |

**Update-four:**

1. Flip `corner_state[V]`.
2. Refresh every **visual dual tile that samples V as a corner** → on an all-quad mesh that is exactly `FacesTouchingVertex(V)` (≤4).
3. Optionally refresh the **Stage-6 dual cell polygon** for V (paint/ghost silhouette).

So the *cardinality* of update-four still looks like “four cells around a point.” The difference vs wrong altitudes is **object identity**: those cells must be dual tiles whose **vertices sit at face centroids** (or Hex19 half-step centres), not primary yellow-wire face fills and not vertex-neighbour star quads.

---

## 4. Why both prior Success shapes fail this criterion

### Face-block / `primary_face_as_dual` (neighborhood r1 → early dual_lattice)

- Cyan / ownership keyed to **primal Face** indices or primary face mesh fills.
- Even when count ≤4 and set = faces around V (correct *incidence*), there is **no second lattice** whose vertices are face centroids — Success sold the underlay faces.
- Refuse remains valid as **proxy / wrong object**, not as “≤4 around a vertex is always wrong.”

### Vertex-centred dual_rebind (aborted)

- `LocalCentre = owner.Position` with corners = **edge-neighbor Vertices**.
- Dual corners sit on the **primal 1-skeleton**, never at face centres → cannot be “dual verts in the middle of main cells.”
- LIVE `IsHalfStepOffset` **inverts** Hex19: requires coincidence with a logic vertex; Hex19 refuses that.
- Cardinal N/E/S/W duals-of-neighbors is a different neighborhood shape than Stage-6 face-centroid polygons / Hex19 update-four.

**Both fail** for different reasons: face-block fails object identity; vertex-centred fails dual-vertex locus.

---

## 5. Follow-on ticket (GREENLIT)

| Field | Value |
|-------|--------|
| Id | [[alpha0_stalberg_dual_face_centroid_r1]] |
| Role | Rebuild organic dual lattice to oskar Stage 6 / Hex19 polarity |
| `success_object` | `dual_offset_cells` (Prefer-aligned; face-centroid geometry in Prefer text) |
| Structural Success | Dual verts = primal face centroids; DualCellsTouching(V) = ≤4 face-centroid duals sampling V; MeshGraph Vertex corner-state preserved; rings=2 spacing=3.0 |
| Refuse | `vertex_neighbor_as_dual_corner` · `primary_face_as_dual` · `dual_centre_on_logic_as_half_step_proof` · `dual_rebind_cardinal_wrong_locus` |
| Path | aborted dual_rebind → **greenlit face_centroid_r1** → dual_visual_r3 after F5 |

Greenlight + IMPLEMENT_SLICE live on [[alpha0_stalberg_dual_face_centroid_r1]] — not this investigation note.

---

## 6. Prefer / intent language — contradiction

### Current dual_rebind invariant (abort)

> … dual cells are the half-offset quads whose corners are those shared Vertex refs — cardinal (N/E/S/W) around the point, never a primary-face 2×2 block.

**Problems under rethink:**

1. “Corners are shared **Vertex** refs” describes **logic corners of a Hex19-style tile** (occupancy at corners) **or** LIVE vertex-neighbour stars — it does **not** name **face-centroid dual vertices**.
2. “Never a primary-face 2×2” over-refuses the **correct update-four incidence** (faces around V) if read as neighborhood shape; the real refuse is **proxy** (primary fill / face index as Success without dual lattice).
3. LIVE organic `IsHalfStepOffset` wording (“half-step vs primary faces” = centre on vertex) **contradicts** Hex19 half-step (centre off occupancy / at face centre).

### Suggested invariant direction (for next ticket draft only)

> Player edits logic points (primal Vertices). The dual lattice is the half-offset copy of the primal: **dual vertices sit at primal face centroids**; each dual cell around a logic point is the ordered polygon of those centroids (oskar Stage 6). Visual dual tiles that sample a logic point as a corner refresh on click (≤4). Refuse selling primary underlay faces or vertex-neighbour star quads as that dual object.

Craft grammar line “logic point at centre of visual cell” aligns with **Stage-6 dual cell centre = primal vertex**. Hex19’s “logic at corners, centre half-step” aligns with **MeshLibrary tile per face**. Next Prefer text should name **both layers** explicitly so they stop fighting.

---

## Disposition

| Item | State |
|------|--------|
| `alpha0_stalberg_dual_rebind_r1` | **aborted_superseded_by_geometry_rethink** — no Success |
| Prefer / Trinity for dual_rebind | **Stopped** — do not claim |
| This note | Investigation only — no weld |

## Related

- Aborted [[alpha0_stalberg_dual_rebind_r1]] · Prior [[alpha0_stalberg_dual_lattice_r2]] · [[alpha0_stalberg_primal_graph_r1]]
- [[Townscaper-Dual-Grid-Craft-Grammar-Y19Mw5YsgjI]] · [[Grid-Topology-Host-Law]] · [[references/oskar-procedure/01-concept]] · [[references/oskar-procedure/02-grid-algorithm]]
