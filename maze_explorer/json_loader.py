import json
import os
from grid_maker import Node

# Extracts the necesary information about the wall form a cell in the dicitonary
def simplify_wall(cell_value):
    return {"node_type": "wall", "wall_status": cell_value["halfWall"]}

# Extracts the necesary information about the tile form a cell in the dicitonary
def simplify_tile(cell_value):
    dict = {}
    dict["node_type"] = "tile"
    dict["curved_walls"] = cell_value["tile"]["curve"]
    dict["in_half_walls"] = cell_value["tile"]["halfWallIn"]
    if "swamp" in cell_value["tile"]:
        dict["tile_type"] = "swamp"
    elif "checkpoint" in cell_value["tile"]:
        dict["tile_type"] = "checkpoint"
    elif "black" in cell_value["tile"]:
        dict["tile_type"] = "hole"
    elif "color" in cell_value["tile"]:
        if cell_value["tile"]["color"] == "#4d1a99":
            dict["tile_type"] = "connection1-3"
        elif cell_value["tile"]["color"] ==   "#1a1ae6":
            dict["tile_type"] = "connection1-2"
        elif cell_value["tile"]["color"] == "#e61a1a":
            dict["tile_type"] = "connection2-3"

    else:
        dict["tile_type"] = "normal"
    
    return dict

# Simplifies the given dictionary to a format that can be used to make a grid
def format_dict(dict):
    adjacents = ([0, 1], [1, 0], [0, -1], [-1, 0])

    start_tile = dict["startTile"]
    start_coords = (start_tile["x"], start_tile["y"])

    new_dict = {}

    for cell_key, cell_value in dict["cells"].items():
        coords = cell_key.split(",")
        coords = list(coords[0:2])
        coords = (int(coords[0]), int(coords[1]))

        lenght = dict["length"]
        width = dict["width"]

        if coords[1] > lenght * 2 or coords[0] > width * 2:
            continue
        if "isWall" in cell_value and not cell_value["isWall"] and cell_value["halfWall"] == 0:
            continue

        new_dict[coords] = {}

        if "isWall" in cell_value:
            new_dict[coords] = simplify_wall(cell_value)
        
        elif "isTile" in cell_value:
            new_dict[coords] = simplify_tile(cell_value)
        else:
            del new_dict[coords]
    new_dict[start_coords]["tile_type"] = "start"

    for y in range(lenght * 2 + 1):
        for x in range(width * 2 + 1):
            if is_even(y) and is_even(x):
                for adj in adjacents:
                    vortex_adj = (x + adj[0], y + adj[1])
                    if vortex_adj in new_dict:
                        if new_dict[vortex_adj]["node_type"] == "wall" and new_dict[vortex_adj]["wall_status"] == 0:
                            new_dict[(x, y)] = {"node_type":"vortex", "status":"occupied"}
    return new_dict

# A previsory node to handle curved walls
class Prev_Node(Node):
    def __init__(self, node_type: str, status: str = "undefined", tile_type: str = "undefined", curved=0):
        super().__init__(node_type, status, tile_type)
        self.curved = curved

def is_even(n):
    return n % 2 == 0

# Generates a vertical wall
def even_wall_gen(cell=None):
    if cell is not None:
        left = right = "not_occupied"
        if cell["wall_status"] == 0:
            left = right = "occupied"
        elif cell["wall_status"] == 1:
            left = "occupied"
        else:
            right = "occupied"
        final_list = [[Node("wall", left), Node("vortex", "occupied"), Node("wall", right)],]
    else:
        final_list = [[Node("wall", "not_occupied"), Node("vortex", "not_occupied"), Node("wall", "not_occupied")],]
    return final_list

# Generates a horizontal wall
def odd_wall_gen(cell=None):
    if cell is not None:
        up = down = "not_occupied"
        if cell["wall_status"] == 0:
            up = down = "occupied"
        elif cell["wall_status"] == 1:
            down = "occupied"
        else:
            up = "occupied"
        final_list = [
            [Node("wall", up), ],
            [Node("vortex", "occupied"), ],
            [Node("wall", down), ]]
    else:
        
        final_list = [
            [Node("wall", "not_occupied"), ],
            [Node("vortex", "not_occupied"), ],
            [Node("wall", "not_occupied"), ]]
    return final_list

# Gets the status of the center vortex in a tile
def get_vortex_status(cell):
    for wall in cell["in_half_walls"]:
        if wall:
            return "occupied"
    return "not_occupied"

def bool_to_status(bool_value):
    if bool_value:
        return "occupied"
    else:
        return "not_occupied"

# Generates a tile
def odd_tile_gen(cell=None):
    walls = []
    walls.append(bool_to_status(cell["in_half_walls"][0]))
    walls.append(bool_to_status(cell["in_half_walls"][1]))
    walls.append(bool_to_status(cell["in_half_walls"][2]))
    walls.append(bool_to_status(cell["in_half_walls"][3]))
    
    vortex = get_vortex_status(cell)
    curved = cell["curved_walls"]

    tile_type = cell["tile_type"]
    final_list = [
        [Prev_Node("tile", "not_occupied", tile_type, curved[0]), Node("wall", walls[0]), Prev_Node("tile", "not_occupied", tile_type, curved[1])],
        [Node("wall", walls[3]), Node("vortex", vortex), Node("wall", walls[1])],
        [Prev_Node("tile", "not_occupied", tile_type, curved[2]), Node("wall", walls[2]), Prev_Node("tile", "not_occupied", tile_type, curved[3])]
    ]

    return final_list

# Generates a vortex
def vortex_gen(cell):
    if cell is None:
        return [[Node("vortex", status="not_occupied"), ], ]
    else:
        return [[Node("vortex", status=cell["status"]), ], ]

# Adds a node to the grid
def add_node(row, node):
    for index_y, a_row in enumerate(node):
        for index_x in range(len(a_row)):
            row[index_y].append(a_row[index_x])
    return row

# Makes a grid form the formatted dicitonary
def make_grid(lenght, width, cell_dict):
    adjacents = ([0, 1], [1, 0], [0, -1], [-1, 0])
    curved_verticies = {
        1:[1, -1],
        2:[1, 1],
        3:[-1, 1],
        4:[-1, -1],
    }
    # Creates the grid adding different types of nodes depending on the index of the cell
    grid = []
    for y in range(lenght * 2 + 1):
        if is_even(y):
            row = [[], ]
        else:
            row = [[], [], []]
        for x in range(width * 2 + 1):
            if is_even(y) and is_even(x):
                if (x, y) in cell_dict.keys():
                    cell = cell_dict[(x, y)]
                else:
                    cell = None
                node = vortex_gen(cell)

            elif is_even(y) and not is_even(x):
                if (x, y) in cell_dict.keys():
                    cell = cell_dict[(x, y)]
                else:
                    cell = None
                node = even_wall_gen(cell)

            elif not is_even(y) and is_even(x):
                if (x, y) in cell_dict.keys():
                    node = odd_wall_gen(cell_dict[(x, y)])
                else:
                    node = odd_wall_gen(None)

            elif not is_even(y) and not is_even(x):
                tile_cell = cell_dict[(x, y)]
                node = odd_tile_gen(tile_cell)

            row = add_node(row, node)
        for r in row:
            grid.append(r)

    # Adds verticies in the middle and a the end of walls
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value.node_type == "vortex":
                for adj in adjacents:
                    adj_x = x + adj[0]
                    adj_y = y + adj[1]

                    if -1 < adj_y < len(grid) and -1 < adj_x < len(row):
                        if grid[adj_y][adj_x].status == "occupied":
                            value.status = "occupied"

    # Adds curved walls
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value.node_type == "tile":
                if value.curved != 0:
                    adj_x = x + curved_verticies[value.curved][0]
                    adj_y = y + curved_verticies[value.curved][1]
                    
                    grid[y][adj_x].status = "occupied"
                    grid[adj_y][x].status = "occupied"

                    adj1_x = x + curved_verticies[value.curved][0] * -1
                    adj1_y = y + curved_verticies[value.curved][1] * -1

                    grid[adj_y][adj1_x].status = "occupied"
                    grid[adj1_y][adj_x].status = "occupied"

    return grid

# Takes a json file from the maze customizer and returns a grid
def grid_from_json(json_path):
    # Opens the file
    with open(json_path) as file:
        dict = json.load(file)
    # Simplifies the json
    formatted_dict = format_dict(dict)
    # Generates the grid
    grid = make_grid(dict["length"], dict["width"], cell_dict=formatted_dict)

    return grid

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    rel_path = "test1.json"
    abs_file_path = os.path.join(script_dir, rel_path)

    grid = grid_from_json(abs_file_path)

    # Prints the grid
    for row in grid:
        for val in row:
            print(val, end="")
        print()
