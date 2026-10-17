# Lane receipt — alpha0_world_s0_optional_lore_r1

**claim_class:** staging · **KEEP:** false · **ask_success:** false

## Touched

- UI/WorldgenGui.cs (optional lore LineEdits after Accept scaffold; **F5-fail amend:** TextChanged lambda wrap CS0029)
- Core/WorldGen/WorldSession0IntentBoard.cs (FromOptionalLore + LoreFeedSalt)
- Core/WorldGen/WorldSession0Intent.cs (CreateAccepted)
- Core/WorldGen/GenTerrainService.cs (lore salt in DeriveSeed)
- Core/WorldGen/WorldPackageSession.cs (lore metas)
- Systems/WorldgenCraft.cs / DualGridCraftHost.cs (pass lore salt)
- LaunchShell.cs (help + open log)

## F5 FAIL amend

- Operator: It no launch (after tip 72cc1a6)
- Cause: `edit.TextChanged += onChanged` (`Action<string>` ≠ `TextChangedEventHandler`) → build fail
- Fix: `edit.TextChanged += newText => onChanged(newText);` — `dotnet build` 0 errors; LaunchShell MCP started=true

## Proofs

| Weld | LIVE |
|------|------|
| L1 | Accept scaffold → lore fields (Player/DM/Shared) |
| L2 | Open with empty fields always lawful |
| L3 | LoreFeedSalt mixed into Create World Open gen seed |
| L-fix | LineEdit TextChanged compiles — Create World / Open / Enter Craft launch again |
