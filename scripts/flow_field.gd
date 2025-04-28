class_name FlowField
extends Node2D

@export var grid_size := 32
var flow_field = {}
var distance_field = {}

var walls_tilemap: TileMap

func _ready():
    walls_tilemap = $"Walls"

func world_to_cell(world_pos: Vector2) -> Vector2i:
    return Vector2i(floor(world_pos.x / grid_size), floor(world_pos.y / grid_size))

func cell_to_world(cell_pos: Vector2i) -> Vector2:
    return Vector2(cell_pos.x * grid_size + grid_size * 0.5, cell_pos.y * grid_size + grid_size * 0.5)

func get_neighbors(cell: Vector2i) -> Array:
    return [
        cell + Vector2i(1, 0),
        cell + Vector2i(-1, 0),
        cell + Vector2i(0, 1),
        cell + Vector2i(0, -1)
    ]

func is_walkable(cell: Vector2i) -> bool:
    return walls_tilemap.get_cell_tile_data(0, cell) == null

func generate(target_position: Vector2):
    var target_cell = world_to_cell(target_position)
    var queue = [target_cell]
    distance_field.clear()
    distance_field[target_cell] = 0

    while queue.size() > 0:
        var current = queue.pop_front()
        var current_distance = distance_field[current]

        for neighbor in get_neighbors(current):
            if not distance_field.has(neighbor) and is_walkable(neighbor):
                distance_field[neighbor] = current_distance + 1
                queue.append(neighbor)

    flow_field.clear()
    for cell in distance_field.keys():
        var best_neighbor = cell
        var best_distance = distance_field[cell]

        for neighbor in get_neighbors(cell):
            if distance_field.has(neighbor) and distance_field[neighbor] < best_distance:
                best_distance = distance_field[neighbor]
                best_neighbor = neighbor

        flow_field[cell] = (cell_to_world(best_neighbor) - cell_to_world(cell)).normalized()

func _draw():
    for cell in flow_field.keys():
        var world_pos = cell_to_world(cell)
        var direction = flow_field[cell]
        draw_line(world_pos, world_pos + direction * (grid_size * 0.4), Color.CYAN, 2)

func _process(delta):
    queue_redraw()
