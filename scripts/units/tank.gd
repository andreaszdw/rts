extends Area2D

var movement_speed: float = 130.0
var turn_speed: float = 5

var turret_speed: float = 1

var attack_radius: float = 300

var navigation_agent : NavigationAgent2D 
var movement_delta: float
var has_movement_target: bool = false

var attack_target: Vector2
var has_attack_target: bool = false

var path: Array

var mouse_over: bool = false

var velocity_computed: Vector2

var root: Node2D


func _ready() -> void:
	navigation_agent = get_node("NavigationAgent2D")
	root = get_tree().get_current_scene()


func set_movement_target(movement_target: Vector2) -> void:
	has_movement_target = true
	has_attack_target = false
	navigation_agent.set_target_position(movement_target)
	

func set_attack_target(target: Vector2) -> void:
	has_attack_target = true
	attack_target = target


func _physics_process(delta):	
	if has_movement_target:	
		# Do not query when the map has never synchronized and is empty.
		if NavigationServer2D.map_get_iteration_id(
			navigation_agent.get_navigation_map()) == 0:
			return
		if navigation_agent.is_navigation_finished():
			$TankBody.play("idle")
			has_movement_target = false
			return
					
		$TankBody.play("move")
		
		movement_delta = movement_speed * delta
		
		var next_path_position: Vector2 = navigation_agent.get_next_path_position()
		check_move_target()
		var new_velocity: Vector2 = global_position.direction_to(next_path_position)  * movement_delta
		new_velocity += velocity_computed * movement_delta
		rotation = lerp_angle(rotation, position.angle_to_point(
			global_position + new_velocity), movement_delta / movement_speed * turn_speed)
		position += new_velocity
		
	#if has_attack_target:
		#$Turret.rotation = lerp_angle(
			#$Turret.rotation, position.angle_to_point(attack_target) - 
			#rotation, delta * turret_speed)
	#else:
		#$Turret.rotation = lerp_angle($Turret.rotation, 0, delta * turret_speed)
	
	#queue_redraw()


func check_move_target():
	var space_state = get_world_2d().direct_space_state
	var target_position = navigation_agent.get_next_path_position()
	var query = PhysicsRayQueryParameters2D.create(position, target_position, collision_mask) #, [self])
	query.collide_with_areas = true
	var result = space_state.intersect_ray(query)
	print(result)
	

func _draw() -> void:
	#draw_circle(Vector2(0, 0), attack_radius, Color(1, 0, 0, 0.2))
	pass


func lerp_angle(from, to, weight):
	return from + short_angle_dist(from, to) * weight


func short_angle_dist(from, to):
	var max_angle = PI * 2
	var difference = fmod(to - from, max_angle)
	return fmod(2 * difference, max_angle) - difference


func _on_mouse_entered() -> void:
	mouse_over = true


func _on_mouse_exited() -> void:
	mouse_over = false


func _on_velocity_computed(safe_velocity: Vector2) -> void:
	velocity_computed = safe_velocity.normalized()
