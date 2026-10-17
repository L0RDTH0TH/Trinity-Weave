---
slice_id: alpha0_pack_save_load_r1
lane: presentation
ticket_map: PACK-save-load
written: 2026-10-16
amended: 2026-10-16
claim_class: staging
f5_fail_fix: organic_seed_persist_restore
---

# Lane receipt — PACK-save-load r1 (organic-seed fix)

Presentation / pack persist touched:

- Core/WorldGen/PackSaveLoadContract.cs (PACK-save-load law)
- Core/WorldGen/WorldPackage.cs (active slice → PackSaveLoadContract; schema 10; FromPersisted)
- Core/WorldGen/WorldPackageSession.cs (BindFromPersisted; MetaPackLoadedFromPersist sticky; IsCreateWorldOpenPath false on Load)
- Core/WorldGen/GenToneContract.cs (feedstock note; successor = PACK)
- Systems/DualGridCraftHost.cs (Persist/Load `organic_seed` + `seed_spacing`; remesh-with-seed before board facts)
- Systems/WorldgenCraft.cs (F5 pack save; RestorePackBoard; AutoGen refuses LoadedFromPack)
- LaunchShell.cs / LaunchShell.tscn (Load World; Enter Craft clears pack sticky)

**F5 FAIL root:** Load remeshed organic board with new random seed → corner indices mapped wrong (looked regened).

**Fix proof:** pack writes `organic_seed`; Load remeshes with that seed; AutoGen barred on pack lane.

Retained: Create World Open auto-gen, Enter Craft empty, no Generate button, GEN-tone BiasLandform.
Nursery salt stubs stay parked. 1e Import parked. GEN-biomes unarmed.

Refuse: blank amber after load · lost world · fake toast · seedless remesh-as-restore · KEEP without F5 · GEN-biomes.
