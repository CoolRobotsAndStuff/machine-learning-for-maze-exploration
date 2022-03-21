import json
import os
from grid_maker import Node
script_dir = os.path.dirname(__file__)
rel_path = "world1.json"
abs_file_path = os.path.join(script_dir, rel_path)


with open(abs_file_path) as file:
    dict = json.load(file)


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

def odd_tile_gen(cell=None):
    walls = []
    walls.append(bool_to_status(cell["in_half_walls"][0]))
    walls.append(bool_to_status(cell["in_half_walls"][1]))
    walls.append(bool_to_status(cell["in_half_walls"][2]))
    walls.append(bool_to_status(cell["in_half_walls"][3]))
    
    
    vortex = get_vortex_status(cell)
    

    tile_type = cell["tile_type"]
    final_list = [
        [Node("tile", "not_occupied", tile_type), Node("wall", walls[0]), Node("tile", "not_occupied", tile_type)],
        [Node("wall", walls[3]), Node("vortex", vortex), Node("wall", walls[1])],
        [Node("tile", "not_occupied", tile_type), Node("wall", walls[2]), Node("tile", "not_occupied", tile_type)]
    ]

    return final_list

def simplify_wall(cell_value):
    return {"node_type": "wall", "wall_status": cell_value["halfWall"]}

def simplify_tile(cell_value):
    dict = {}
    dict["node_type"] = "tile"
    dict["curved_walls"] = cell_value["tile"]["curve"]
    dict["in_half_walls"] = cell_value["tile"]["halfWallIn"]
    if "swamp" in cell_value["tile"]:
        dict["tile_type"] = "swamp"
    elif "checkpoint" in cell_value["tile"]:
        dict["tile_type"] = "checkpoint"
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


def format_dict(dict):
    adjacents = ([0, 1], [1, 0], [0, -1], [-1, 0])

    start_tile = dict["startTile"]
    start_coords = (start_tile["x"], start_tile["y"])

    new_dict = {}

    for cell_key, cell_value in dict["cells"].items():
        coords = list(cell_key)
        coords = (int(coords[0]), int(coords[2]))

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
    new_dict[start_coords]["tile_type"] = "start"

    for y in range(lenght * 2 + 1):
        if is_even(y):
            row = [[], ]
        else:
            row = [[], [], []]
        for x in range(width * 2 + 1):
            if is_even(y):  # even y
                if is_even(x):  # even x
                    for vortex_adj in [(x + adj[0], y + adj[1]) for adj in adjacents]:
                        if vortex_adj in new_dict:
                             if new_dict[vortex_adj]["node_type"] == "wall" and new_dict[vortex_adj]["wall_status"] == 0:
                                    new_dict[(x, y)] = {"node_type":"vortex", "status":"occupied"}


                else:  # odd x
                    if (x, y) in new_dict.keys():
                        pass
            else:  # odd y
                if is_even(x):  # even x
                    if (x, y) in new_dict.keys():
                        pass
                    else:
                        pass
                else:  # odd x
                    pass

    return new_dict

def is_even(n):
    return n % 2 == 0

def vortex_gen(cell):
    if cell is None:
        return [[Node("vortex", status="not_occupied"), ], ]
    else:
        return [[Node("vortex", status=cell["status"]), ], ]

def add_node(row, node):
    for index_y, a_row in enumerate(node):
        for index_x in range(len(a_row)):
            row[index_y].append(a_row[index_x])
    return row


def make_grid(lenght, width, cell_dict):
    grid = []
    for y in range(lenght * 2 + 1):
        if is_even(y):
            row = [[], ]
        else:
            row = [[], [], []]
        for x in range(width * 2 + 1):
            if is_even(y):  # even y
                if is_even(x):  # even x
                    if (x, y) in cell_dict.keys():
                        cell = cell_dict[(x, y)]
                    else:
                        cell = None
                    node = vortex_gen(cell)
                else:  # odd x
                    if (x, y) in cell_dict.keys():
                        cell = cell_dict[(x, y)]
                    else:
                        cell = None
                    node = even_wall_gen(cell)
            else:  # odd y
                if is_even(x):  # even x
                    if (x, y) in cell_dict.keys():
                        node = odd_wall_gen(cell_dict[(x, y)])
                    else:
                        node = odd_wall_gen(None)
                else:  # odd x
                    tile_cell = cell_dict[(x, y)]
                    node = odd_tile_gen(tile_cell)

            row = add_node(row, node)
        for r in row:
            grid.append(r)

    return grid

formatted_dict = format_dict(dict)
print("FORMAT DICT")
for item in formatted_dict.items():
    print(item)
grid = make_grid(dict["length"], dict["width"], cell_dict=formatted_dict)
        
for item in formatted_dict.items():
    print(item)

for row in grid:
    for val in row:
        print(val, end="")
    print()
