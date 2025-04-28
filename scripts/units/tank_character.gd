extends CharacterBody2D

@export var speed := 120
@export var separation_radius := 70.0
@export var separation_strength := 100.0

var navigation_agent : NavigationAgent2D 
var has_movement_target: bool = false

var target_position: Vector2
var moving := false
var flow_field


func _ready():
    navigation_agent = get_node("NavigationAgent2D")
    add_to_group("units")
    flow_field = FlowField


func set_movement_target(movement_target: Vector2) -> void:
    has_movement_target = true
    navigation_agent.set_target_position(movement_target)


func _physics_process(delta):
    if has_movement_target:
        print(navigation_agent.target_position)
        if NavigationServer2D.map_get_iteration_id(
            navigation_agent.get_navigation_map()) == 0:
            return
        if navigation_agent.is_navigation_finished():
            $TankBody.play("idle")
            has_movement_target = false
            return

        $TankBody.play("moving")

        var to_target = (navigation_agent.get_next_path_position() - global_position)
        if to_target.length() < 10:
            moving = false
            velocity = Vector2.ZERO
        else:
            var desired_velocity = to_target.normalized() * speed
            desired_velocity += calculate_separation()
            velocity = desired_velocity
            rotation = lerp_angle(rotation, position.angle_to_point(
                global_position + velocity), delta * 16)
            move_and_slide()


func calculate_separation() -> Vector2:
    var separation = Vector2.ZERO
    for other in get_tree().get_nodes_in_group("units"):
        if other == self:
            continue
        var offset = global_position - other.global_position
        var dist = offset.length()
        if dist < separation_radius and dist > 0:
            separation += offset.normalized() * (separation_strength / dist)
    return separation
