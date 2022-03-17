import json
import os
from grid_maker import make_grid, Node
script_dir = os.path.dirname(__file__)
rel_path = "world1.json"
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

    return final_list



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

    if ("isWall" in cell_value and cell_value["isWall"]) or "isWall" not in cell_value:
        new_dict[coords] = {}

    
    if "isWall" in cell_value:
        print(cell_value["isWall"])
        if cell_value["isWall"]:
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

grid = []
for y in range(dict["length"]*2+1):
    half_y = int(y / 2)
    half_x = int(y / 2)
    if y % 2 == 0: #even y
        row = [[],]
    else:
        row = [[], [], []]
    for x in range(dict["width"]*2+1):
        if y % 2 == 0: #even y
            
            if x % 2 == 0: # even x
                row[0].append(Node("vortex", status="not_occupied"))
            else: #odd x
                if (x, y) in new_dict.keys():
                    wall = even_wall_gen(new_dict[(x, y)])
                    for node in wall[0]:
                        row[0].append(node)
                else:
                    wall = even_wall_gen(None)
                    for node in wall[0]:
                        row[0].append(node)
        else: #odd y
            
            if x % 2 == 0: # even x
                if (x, y) in new_dict.keys():
                    odd_wall = odd_wall_gen(new_dict[(x, y)])
                else:
                    odd_wall = odd_wall_gen(None)
                for index, a_row in enumerate(odd_wall):
                    row[index].append(a_row[0])
                
            
            else: #odd x
                tile_cell = new_dict[(x, y)]
                odd_tile = odd_tile_gen(tile_cell)

                for index_y, a_row in enumerate(odd_tile):
                    for index_x in range(len(a_row)):
                        row[index_y].append(a_row[index_x])


    for r in row:
        grid.append(r)
print("GRID:")

for row in grid:
    print(row)
        




for item in new_dict.items():
    print(item)

for row in grid:
    for val in row:
        print(val, end="")
    print()

for key, value in dict["cells"].items():
    pass


