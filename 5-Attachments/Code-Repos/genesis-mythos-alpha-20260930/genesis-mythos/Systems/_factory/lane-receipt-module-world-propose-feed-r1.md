---
slice_id: alpha0_world_propose_feed_r1
lane: presentation
ticket_map: WORLD-propose
written: 2026-10-16
claim_class: staging
---

# Lane receipt — WORLD-propose feed r1

Presentation / gen apply touched:

- Core/WorldGen/WorldProposeFeedContract.cs (new)
- Core/WorldGen/WorldScaffoldProposal.cs (GenFeedSalt / coast / ridge; Reject clears)
- Core/WorldGen/GenTerrainService.cs (mix salt+axes into pass)
- Core/WorldGen/WorldPackageSession.cs (feed metas)
- Systems/DualGridCraftHost.cs (ApplyGenTerrainPass scaffold arg)
- Systems/WorldgenCraft.cs (pass package.Scaffold; Generate button stays absent)
- UI/WorldgenGui.cs (propose chrome copy)

Refuse: menu-only Accept · Generate button re-add · KEEP without F5 · forward MAP arm.
