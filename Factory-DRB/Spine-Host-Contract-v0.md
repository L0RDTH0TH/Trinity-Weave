---
title: Spine-Host-Contract-v0
project-id: godot-genesis-mythos-master
status: draft
game_repo: 5-Attachments/Code-Repos/genesis-mythos-demo
---

# Spine-Host-Contract-v0

**Spine** = internal host sockets that accept **external** stack rows from [[Factory-DRB/Tech-Stack-Manifest-v1.yaml]]. Spine is not the BOM.

## Principles

1. Every `plugin_addon` row with `wrap_policy` must have a C# interface in `Gmm.Core/` (or documented namespace).
2. Gameplay code depends on **interfaces**, not vendor types.
3. Vendor code lives under `addons/vendor_*` only; wired in composition root / autoload registry.
4. Unwelded vendor usage in gameplay paths = `anti_pattern_violations: unwelded_vendor`.

## R1 sockets

| Interface | Manifest row | DRB |
|-----------|--------------|-----|
| `ICameraRig` | `addon-phantom-camera` | [[Factory-DRB/interfaces/perspective-stack-interface]] |

## Receipt flow

```
read manifest → mutate game repo → write integrate receipt → factory_little_val → Watcher/telemetry
```

Receipts: `.technical/weave/factory/receipts/<run_id>/`

## Related

- [[Factory-DRB/perspective-stack-v1]]
- [[Factory-DRB/Stack-Charter-v0]]
