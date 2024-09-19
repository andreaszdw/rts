extends Area2D


var movement_speed: float = 30.0
var turn_speed:float = 5

var turret_speed: float = 1

var attack_radius: float = 300

var navigation_agent: NavigationAgent2D 
var movement_delta: float
var has_movement_target: bool = false

var attack_target: Vector2
var has_attack_target: bool = false


func _ready() -> void:
	navigation_agent = get_node("NavigationAgent2D")
	navigation_agent.velocity_computed.connect(Callable(_on_velocity_computed))
	
	# Enable avoidance
	NavigationServer2D.agent_set_avoidance_enabled(navigation_agent, true)
	# Create avoidance callback
	NavigationServer2D.agent_set_avoidance_callback(navigation_agent, Callable(self, "_avoidance_done"))

	# Disable avoidance
	#NavigationServer2D.agent_set_avoidance_enabled(navigation_agent, false)
	# Delete avoidance callback
	#NavigationServer2D.agent_set_avoidance_callback(navigation_agent, Callable())


func set_movement_target(movement_target: Vector2):
	has_movement_target = true
	has_attack_target = false
	navigation_agent.set_target_position(movement_target)
	

func set_attack_target(target: Vector2):
	has_attack_target = true
	attack_target = target


func _physics_process(delta):
	
	if has_movement_target:		
		# Do not query when the map has never synchronized and is empty.
		if NavigationServer2D.map_get_iteration_id(navigation_agent.get_navigation_map()) == 0:
			return
		if navigation_agent.is_navigation_finished():
			$TankBody.play("idle")
			has_movement_target = false
			return
		
		$TankBody.play("move")
		
		movement_delta = movement_speed * delta
		
		var next_path_position: Vector2 = navigation_agent.get_next_path_position()
		var new_velocity: Vector2 = global_position.direction_to(next_path_position) * movement_delta
		# rotation = lerpf(rotation, position.angle_to_point(next_path_position), delta * turn_speed)
		rotation = lerp_angle(rotation, position.angle_to_point(next_path_position), delta * turn_speed)
		if navigation_agent.avoidance_enabled:
			navigation_agent.set_velocity(new_velocity)
		else:
			_on_velocity_computed(new_velocity)

	if has_attack_target:
		$Turret.rotation = lerp_angle($Turret.rotation, position.angle_to_point(attack_target) - rotation, delta * turret_speed)
	else:
		$Turret.rotation = lerp_angle($Turret.rotation, 0, delta * turret_speed)
	
	queue_redraw()


func _on_velocity_computed(safe_velocity: Vector2) -> void:
	global_position = global_position.move_toward(global_position + safe_velocity, movement_delta)


func _draw():
	draw_arc(Vector2(0, 0), attack_radius, 0, 360, 100, Color(1, 0, 0, 1), 5)
	


func lerp_angle(from, to, weight):
	return from + short_angle_dist(from, to) * weight


func short_angle_dist(from, to):
	var max_angle = PI * 2
	var difference = fmod(to - from, max_angle)
	return fmod(2 * difference, max_angle) - difference
