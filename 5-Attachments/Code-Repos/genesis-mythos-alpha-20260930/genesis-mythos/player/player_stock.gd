extends CharacterBody3D
## Minimal stock FPS — GDScript only, no Genesis Prefer / seats / FpsLookInput.
## Purpose: A/B vs C# PlayerFp. If THIS also cannot look while WASD is held,
## the bug is OS/display (Linux key-hold starving mouse motion), not our C#.

const SPEED := 5.0
const GRAVITY := 24.0
const SENS := 0.0025
const PITCH_MIN := -1.4
const PITCH_MAX := 1.4

var _pitch := 0.0
var _cam: Camera3D
var _hud: Label
var _motion_events := 0
var _keys_held := false
var _accum := 0.0

func _ready() -> void:
	_cam = $Camera3D
	_cam.current = true
	_pitch = _cam.rotation.x
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	_ensure_move_actions()
	_make_hud()
	print("[player_stock] ready mouse_mode=", Input.mouse_mode, " display=", DisplayServer.get_name())

func _unhandled_input(event: InputEvent) -> void:
	# Esc / click — same as every tutorial
	if event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE:
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT \
			and Input.mouse_mode != Input.MOUSE_MODE_CAPTURED:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
		return

	# Look on the event itself (tutorial style). Count every motion for diagnostics.
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		_motion_events += 1
		var d: Vector2 = event.screen_relative
		if d.is_zero_approx():
			d = event.relative
		rotate_y(-d.x * SENS)
		_pitch = clampf(_pitch - d.y * SENS, PITCH_MIN, PITCH_MAX)
		_cam.rotation.x = _pitch

func _physics_process(delta: float) -> void:
	var v := velocity
	if not is_on_floor():
		v.y -= GRAVITY * delta

	# Movement is NEVER gated on mouse capture (Prefer had that bug).
	var axes := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	_keys_held = axes.length_squared() > 0.0001
	var dir := (transform.basis * Vector3(axes.x, 0.0, axes.y))
	if dir.length_squared() > 0.0001:
		dir = dir.normalized()
	else:
		dir = Vector3.ZERO
	v.x = dir.x * SPEED
	v.z = dir.z * SPEED
	velocity = v
	move_and_slide()

	_accum += delta
	if _accum >= 0.5:
		_accum = 0.0
		var line := "stock GDScript | display=%s | captured=%s | keys=%s | motion_evt/0.5s=%d | yaw=%.2f | hvel=%.2f" % [
			DisplayServer.get_name(),
			str(Input.mouse_mode == Input.MOUSE_MODE_CAPTURED),
			str(_keys_held),
			_motion_events,
			rotation.y,
			Vector3(velocity.x, 0.0, velocity.z).length(),
		]
		_hud.text = line
		print("[player_stock] ", line)
		# Smoking gun: keys held + zero motion events while trying to look = OS starvation.
		if _keys_held and _motion_events == 0:
			_hud.text += "\n★ motion starved while WASD — Linux/display, not FPS math"
		_motion_events = 0

func _ensure_move_actions() -> void:
	_bind("move_forward", KEY_W)
	_bind("move_back", KEY_S)
	_bind("move_left", KEY_A)
	_bind("move_right", KEY_D)

func _bind(action: String, key: Key) -> void:
	if not InputMap.has_action(action):
		InputMap.add_action(action, 0.2)
	for ev in InputMap.action_get_events(action):
		if ev is InputEventKey and ev.physical_keycode == key:
			return
	var e := InputEventKey.new()
	e.physical_keycode = key
	InputMap.action_add_event(action, e)

func _make_hud() -> void:
	var layer := CanvasLayer.new()
	layer.layer = 100
	_hud = Label.new()
	_hud.position = Vector2(12, 12)
	_hud.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.add_child(_hud)
	add_child(layer)
