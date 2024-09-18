extends Node2D


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var new_region_rid: RID = NavigationServer2D.region_create()
	var default_map_rid: RID = get_world_2d().get_navigation_map()
	NavigationServer2D.region_set_map(new_region_rid, default_map_rid)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _input(event):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
			$TankProto.set_movement_target(get_global_mouse_position())
			$TankProto.set_attack_target(get_global_mouse_position())
