# Genesis Mythos — Alpha 0 table (offline)

Open-source modular first-person 3D VTT **table**: host → pick a module cartridge → play offline with Player/DM seats.

**Product = the table.** Modules are cartridges. The included `example_goblin_oneshot` is an **example cartridge** (original placeholder content) — not a campaign ship and not a licensed adventure dump.

## Play (F5)

1. Open `project.godot` in Godot 4.6.3 .NET
2. Run main scene (`scenes/Main.tscn`)
3. **Front door:** Host table → select **Example Goblin Oneshot** (`example_goblin_oneshot`) → **Enter play**
4. **Session roles:** choose Player or DM seat + a pregen → **Continue into site**
5. **Play:** WASD + mouse look in the site; **Skill check** (or **C**) → **Start skirmish** (or **V**) → **Attack** (or **B**)
6. **Seats:** Seat: Player / Seat: DM · **DM rail view** or **Tab** (Player seat → on-screen **Unauthorized**)
7. **Esc** quits · **Front door** returns to module pick · **Enter** advances front door / roles when focused

## Example pack (`content/packs/example_goblin_oneshot/`)

| File | Contents |
|------|----------|
| `pack.json` | Stable `pack_id`, honesty banner, rules bind |
| `pregens.json` | 4 example goblin PCs (name, HP, attack, skills) |
| `sites.json` | Cave Mouth Path + Scrap Clearing |
| `beats.json` | Stealth DC 12 check + short scrap vs placeholder mongrel |

## Honesty

- Placeholder art
- NOT campaign ship / NOT full Genesis campaign
- No LAN (`lan_listen_server` is Alpha 1)
- Factory overnight / full BOM path is **not** required for Alpha 0
- `CampaignCapableDoDGate` still refuses loop-alone (legacy host remains; Alpha 0 does not claim CampaignCapable)

## Hosts reused

`IPlayRegionHost`, `IUiHost`, `ICameraRig`, `IAgencyEnvelope`, `IDiceRoller`, `IRulesPluginHost`, seams. No Demo* parallel ports for authority.
