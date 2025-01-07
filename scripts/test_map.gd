extends Node2D

var shift_pressed: bool = false

var selected_units: Array
var units: Array


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var new_region_rid: RID = NavigationServer2D.region_create()
	var default_map_rid: RID = get_world_2d().get_navigation_map()
	NavigationServer2D.region_set_map(new_region_rid, default_map_rid)
	units.append($Tank)
	units.append($Tank2)
	units.append($Tank3)
	units.append($Tank4)
	units.append($Tank5)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
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
			squareFormation(selected_units, get_global_mouse_position())
			#var counter = 0
			#for su in selected_units:
				#su.set_attack_target(get_global_mouse_position())
				#var offset = su.get_avoidance_radius() * counter
				#print(get_global_mouse_position(), offset)
				#su.set_movement_target(get_global_mouse_position() + Vector2(offset, offset))
				#counter +=1

func squareFormation(unit_array, mousepos):
	var counter = 0	
	var number_of_unit = unit_array.size()
	var square_side_size = round(sqrt(number_of_unit))
	var space_between_units = 100
	var unit_pos = mousepos - (space_between_units * Vector2(square_side_size/2,square_side_size/2)) * counter
	for x in unit_array:
		x.set_movement_target(unit_pos)
		unit_pos.x += space_between_units
		if unit_pos.x > (mousepos.x + square_side_size * space_between_units / 2):
			unit_pos.y += space_between_units * counter
			unit_pos.x = mousepos.x - (space_between_units * square_side_size/2) * counter
		counter += 1

func circleFormation(unit_array, mousepos):
	var unit_pos = mousepos
	var space_between_units = 100
	var circle_size = 0
	var unit_total_count_in_circle = 6 * circle_size
	var unit_count_in_circle = 0
	var current_angle = 0
	for x in unit_array:
		x.set_movement_target(unit_pos)
		unit_count_in_circle += 1
		if unit_count_in_circle >= unit_total_count_in_circle:
			unit_count_in_circle = 0
			current_angle = 0
			circle_size += 1
			unit_total_count_in_circle = 6 * circle_size
			unit_pos.x = mousepos.x + space_between_units * circle_size
			unit_pos.y = mousepos.y
		else:
			current_angle += (PI/3) / circle_size
			unit_pos.x = mousepos.x + (space_between_units * circle_size) * cos(current_angle)
			unit_pos.y = mousepos.y + (space_between_units * circle_size) * sin(current_angle)
