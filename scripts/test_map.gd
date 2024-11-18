extends Node2D

var shift_pressed: bool = false

var selected_units: Array
var units: Array


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var new_region_rid: RID = NavigationServer2D.region_create()
	var default_map_rid: RID = get_world_2d().get_navigation_map()
	NavigationServer2D.region_set_map(new_region_rid, default_map_rid)
	units.append($TankProto)
	units.append($TankProto2)
	units.append($TankProto3)
	units.append($TankProto4)
	units.append($Tank)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _input(event):
	if event is InputEventKey:
		if event.is_pressed():
			if event.keycode == KEY_SHIFT:
				shift_pressed = true
		if event.is_released():
			if event.keycode == KEY_SHIFT:
				shift_pressed = false
		
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
			if shift_pressed:
				for u in units:
					if u.mouse_over:
						if not selected_units.has(u):
							selected_units.append(u)
			
			else:
				selected_units.clear()
				for u in units:
					if u.mouse_over:
						selected_units.append(u)

		if event.button_index == MOUSE_BUTTON_RIGHT and event.pressed:
			var counter = 0
			for su in selected_units:
				su.set_attack_target(get_global_mouse_position())
				var offset = su.get_avoidance_radius() * counter
				print(get_global_mouse_position(), offset)
				su.set_movement_target(get_global_mouse_position() + Vector2(offset, offset))
				counter +=1
