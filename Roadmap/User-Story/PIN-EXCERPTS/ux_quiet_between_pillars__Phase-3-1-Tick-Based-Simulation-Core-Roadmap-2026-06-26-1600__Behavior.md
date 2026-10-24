# PIN-EXCERPT — `ux_quiet_between_pillars` → [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]

- heading: ## Behavior
- role: primary
- excerpt_note: In-adventure quiet via tick pipeline / continuous low-intensity sim
- source: `1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Core/Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600.md`
- weld_rule: excerpt text is the weld; heading is the locator

---

DMPauseGate → clock step → subsystem pass → ConsequenceResolver + tone weights → WorldStateCommitter → WorldEventLog → `sim.tick_committed` (non-blocking for Presentation).
