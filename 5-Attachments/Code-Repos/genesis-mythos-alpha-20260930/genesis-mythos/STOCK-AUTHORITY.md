# Stock authority (before player/camera/look/move)

**Named:** `godot_stock_fps` · Trinity `engine_stock_authority`

**Godot-Implementation-Decision-Matrix principle:**
> Copy the masters. ClassDB / locked stack row / Host Index first. Convert Pathfinder → computer calcs; route results and relationship/history context to the correct seat (Player vs DM). Prefer stock Godot/vendor; extend only at seat/authority boundaries. Never invent a parallel physics, terrain, rules, or notify/RP channel when a master already owns the concern.

**Player move/look row Prefer:** `CharacterBody3D` + child `Camera3D` at eye height; `Input.MouseMode = Captured`; yaw on body (Y); pitch on camera (X); WASD → Velocity XZ + gravity + MoveAndSlide(); Esc → Visible.

**Never:** Free-fly Camera3D as only mover; Host methods named Move/Look/HandleInput driving the body.

**Investor surface:** `res://scenes/Main.tscn` (not FpsSanity*).  
Walk+look Done = operator F5 attest (with Wayland motion-starvation caveat on this laptop). Ban “MCP verified walk+look.”  
`dev/FpsSanity*` = diagnostics only.
