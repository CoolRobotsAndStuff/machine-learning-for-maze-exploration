import json
import os
from grid_maker import make_grid, Node
script_dir = os.path.dirname(__file__)
rel_path = "test.json"
abs_file_path = os.path.join(script_dir, rel_path)


with open(abs_file_path) as file:
    dict = json.load(file)


def even_wall_gen(cell=None):
    if cell is not None:
        final_list = [[Node("wall", "occupied"), Node("vortex", "occupied"), Node("wall", "occupied")],]
    else:
        final_list = [[Node("wall", "not_occupied"), Node("vortex", "not_occupied"), Node("wall", "not_occupied")],]
    
    return final_list

def odd_wall_gen(cell=None):
    if cell is not None:
        final_list = [
            [Node("wall", "occupied"),],
            [Node("vortex", "occupied"),],
            [Node("wall", "occupied"),],
            ]
    else:
        final_list = [
            [Node("wall", "not_occupied"),],
            [Node("vortex", "not_occupied"),],
            [Node("wall", "not_occupied"),],
            ]
    return final_list

def odd_tile_gen(cell=None):
    left_half_w = "occupied" if cell["in_half_walls"][3] else "not_occupied"
    right_half_w = "occupied" if cell["in_half_walls"][1] else "not_occupied"
    down_half_w = "occupied" if cell["in_half_walls"][2] else "not_occupied"
    up_half_w = "occupied" if cell["in_half_walls"][0] else "not_occupied"
    vortex = "not_occupied"

    for wall in cell["in_half_walls"]:
        if wall:
            vortex = "occupied"

    tile_type = cell["tile_type"]
    final_list = [
        [Node("tile", "not_occupied", tile_type),   Node("wall", up_half_w),    Node("tile", "not_occupied", tile_type)],
        [Node("wall", left_half_w),                 Node("vortex", vortex),     Node("wall", right_half_w)],
        [Node("tile", "not_occupied", tile_type),   Node("wall", down_half_w),  Node("tile", "not_occupied", tile_type)]
    ]



for cell in dict["cells"].values():
    #del cell["virtualWall"]
    #del cell["explored"]
    #del cell["isLinear"]

    """
    if "halfWall" in cell:
        del cell["halfWall"]
    """
 
    if "tile" in cell:
        del cell["tile"]["changeFloorTo"]
    
    print(cell)

"""

grid = [["nn", "nn", "nn", "nn", "nn", "nn", "nn", "nn"],
        ["nn", "nn", "nn", "nn", "nn", "nn", "nn", "nn"],
        ["nn", "nn", "nn", "nn", "nn", "nn", "nn", "nn"],
        ["nn", "nn", "nn", "nn", "nn", "nn", "nn", "nn"],
        ["nn", "nn", "nn", "nn", "nn", "nn", "nn", "nn"],
        ["nn", "nn", "nn", "nn", "nn", "nn", "nn", "nn"],
        ["nn", "nn", "nn", "nn", "nn", "nn", "nn", "nn"],
        ["nn", "nn", "nn", "nn", "nn", "nn", "nn", "nn"]]
"""

grid = make_grid([16, 16])

start_tile = dict["startTile"]
start_coords = (start_tile["x"], start_tile["y"])


new_dict = {}

for cell_key, cell_value in dict["cells"].items() :
    coords = list(cell_key)
    coords = (int(coords[0]), int(coords[2]))
    if coords[0] > dict["length"]*2  or coords[1] > dict["width"]*2:
        continue
    #print(coords)

    new_dict[coords] = {}


    if "isWall" in cell_value:
        new_dict[coords]["node_type"] = "wall"
        new_dict[coords]["status"] = "occupied"
    
    elif "isTile" in cell_value:
        new_dict[coords]["node_type"] = "tile"
        new_dict[coords]["curved_walls"] = cell_value["tile"]["curve"]
        new_dict[coords]["in_half_walls"]=cell_value["tile"]["halfWallIn"]
        if "swamp" in cell_value["tile"]:
            new_dict[coords]["tile_type"] = "swamp"
        elif "checkpoint" in cell_value["tile"]:
            new_dict[coords]["tile_type"] = "checkpoint"
        
        else:
            new_dict[coords]["tile_type"] = "normal"
        


new_dict[start_coords]["tile_type"] = "start"

for item in new_dict.items():
    print(item)

for row in grid:
    for val in row:
        print(val, end="")
    print()

for key, value in dict["cells"].items():
    pass


