---
title: usability-navigation-v1
project-id: godot-genesis-mythos-master
factory: Presentation
seat: Surface
tier: B
human_facing: true
---

# Usability DRB — Navigation v1 (Surface seat)

**Question:** Can a human **move and look at the same time** and command the world without dev cheatsheet?

Interpretation pass does **not** satisfy this DRB.

## Checklist (machine block)

```yaml
checklist:
  - id: Nav_LookWhileMove_FP
    tier: A
    kinesthetic: true
    bar: "WASD + mouse look simultaneously in FP — point at object while moving"
  - id: Nav_LookWhileMove_DM
    tier: A
    kinesthetic: true
    bar: "Sparky DM — fly + look simultaneously — not one-at-a-time"
  - id: Flow_Ortho_Tabletop
    tier: B
    kinesthetic: true
    bar: "O key — top-down map read + WASD pan (BG-style, camera ⊥ XZ)"
  - id: Anti_DevOnlyHUD
    tier: B
    kinesthetic: false
    bar: "No dev-only success path; degraded modes visible per waiver"
  - id: Anti_HarnessSubstitutesPlaytest
    tier: A
    kinesthetic: false
    bar: "Harness green ≠ Surface pass; smokes do not waive this DRB"
```

## Evidence

- `operator_feedback` row per **kinesthetic: true** id — [[Factory-DRB/operator-feedback/godot-closed-alpha-kinesthetic.yaml]]
- Factory: `surface-pass` CLI

## Related

- [[Factory-DRB/Gate-Precedence-Conflict-Doctrine-v1]]
- [[Factory-DRB/perspective-stack-v1]]
