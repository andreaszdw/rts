extends Node2D

const vehicle: PackedScene = preload("res://scenes/steering_behavior/scenes/vehicle.tscn")
var vehicles: Array


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	for i in range(10):
		var v = vehicle.instantiate()
		v.init(Vector2(100 + i * 20, 100 + i * 25), vehicles)
	
		vehicles.append(v)
		add_child(v)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	var counter: int = 0
	for v in vehicles:
		#if counter % 3 == 0:
			#v.steering("flee", get_global_mouse_position())
		#elif counter % 2 == 0:
			#v.steering("arrive", get_global_mouse_position())
		#else:
			#v.steering("seek", get_global_mouse_position())
		#counter += 1
		v.steering("arrive", get_global_mouse_position())
