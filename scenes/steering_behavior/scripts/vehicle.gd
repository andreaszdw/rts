class_name Vehicle
extends Area2D

var velocity: Vector2 = Vector2(0, 0)
var acceleration: Vector2 = Vector2(0,0)
var steering_force: Vector2 = Vector2(0, 0)

var slowing_distance: float = 50
var max_speed: float = 3
var max_force: float = 0.05
var desired_separation: float = 100

var _behavior: String = "idle"
var _target: Vector2 = Vector2(0, 0)
var _path: Array

var _vehicles: Array


func init(pos, vehicles):
	position = pos
	_vehicles = vehicles


func _process(delta: float) -> void:
	if _behavior == "idle":
		return
		
	steering_force = Vector2(0, 0)
	acceleration = Vector2(0, 0)
	
	#stay_within_rect(get_viewport_rect())
	
	if _behavior == "seek":
		seek()
	
	if _behavior == "flee":
		flee()
		
	if _behavior == "arrive":
		arrive()
		
	separate()


func steering(behavior, target=Vector2(0, 0), path=Array()):
	_behavior = behavior
	_target = target
	_path = path


func seek():
	var desired = (_target - position).normalized() * max_speed
	calc_steering(desired)


func flee():
	var desired = (position - _target).normalized() * max_speed
	calc_steering(desired)


func arrive():
	var target_offset = _target - position
	var distance = target_offset.length()
	var ramped_speed = max_speed * (distance / slowing_distance)
	var clipped_speed = min(ramped_speed, max_speed)
	var desired = (clipped_speed / distance) * target_offset
	calc_steering(desired)

func separate():
	var sum: Vector2 = Vector2(0, 0)
	var counter: int = 0
	for v in _vehicles:
		if v == self:
			continue
		var d = position.distance_to(v.position)
		if d > 0 && d < desired_separation:
			var diff = position - v.position
			diff.normalized()
			diff /= d
			sum += diff
			counter += 1
	if counter > 0:
		sum /= counter
		sum = sum.normalized() * max_speed
		calc_steering(sum - velocity)
		return
	
	calc_steering(sum)
	
func calc_steering(desired):
	steering_force = desired - velocity
	steering_force = steering_force.limit_length(max_force)
	acceleration += steering_force
	velocity += acceleration
	velocity = velocity.limit_length(max_speed)
	position += velocity
	rotation = velocity.angle()


func stay_within_rect(rect: Rect2):
	var desired = velocity
	
	if position.x < rect.position.x + 180:
		desired = Vector2(max_speed, velocity.y)
	if position.x > rect.end.x - 180:
		desired = Vector2(-max_speed, velocity.y)
		
	if position.y < rect.position.y + 180:
		desired = Vector2(velocity.x, max_speed)
	if position.y > rect.end.y - 180:
		desired = Vector2(velocity.x, -max_speed)
	
	calc_steering(desired)
