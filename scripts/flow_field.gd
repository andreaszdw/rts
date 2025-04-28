class_name FlowField
extends Node2D

var tilemap: TileMapLayer
var distance_field = {}
var flow_field = {}

func _ready() -> void:
    z_index = 100


# Gibt zurück, ob ein Tile begehbar ist
func is_walkable(cell: Vector2i) -> bool:
    var ground = tilemap.get_cell_tile_data(cell).get_custom_data("ground")
    if ground == "water":
        return false
    else:
        return true

    #return tilemap.get_cell_source_id(0, cell) == 0  # 0 = Boden (anpassen je nach deinem TileSet)


# Generiert FlowField vom Ziel aus
func generate(target_cell: Vector2i):
    distance_field.clear()
    flow_field.clear()

    var queue = [target_cell]
    distance_field[target_cell] = 0

    while not queue.is_empty():
        var current = queue.pop_front()
        var current_dist = distance_field[current]

        for neighbor in get_neighbors(current):

            if is_walkable(neighbor) and not distance_field.has(neighbor):
                distance_field[neighbor] = current_dist + 1
                queue.append(neighbor)

    # Bestimme beste Richtung für jedes begehbare Tile
    for cell in distance_field.keys():
        var best_dir = Vector2.ZERO
        var best_dist = distance_field[cell]

        for neighbor in get_neighbors(cell):
            if distance_field.has(neighbor) and distance_field[neighbor] < best_dist:
                best_dist = distance_field[neighbor]
                best_dir = (neighbor - cell)
                best_dir = Vector2(best_dir.x, best_dir.y).normalized()

        flow_field[cell] = best_dir

# Hilfsfunktion: Gibt Nachbarn
func get_neighbors(cell: Vector2i) -> Array:
    var map_size = tilemap.get_used_rect().size
    var neighbors = []
    var directions = [
        Vector2i(1, 0),
        Vector2i(-1, 0),
        Vector2i(0, 1),
        Vector2i(0, -1)
    ]
    
    for dir in directions:
        var neighbor = cell + dir
        if neighbor.x >= 0 and neighbor.y >= 0 and neighbor.x < map_size.x and neighbor.y < map_size.y:
            neighbors.append(neighbor)
    
    return neighbors