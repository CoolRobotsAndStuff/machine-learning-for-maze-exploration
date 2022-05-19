import string
import numpy as np
import math
from grid_node import Node

def make_grid(dimensions) -> list:
    grid = list()
    for y in range(dimensions[0]):
        row = list()
        if y % 2 == 0:
            for x in range(dimensions[1]):
                if x % 2 == 0:
                    row.append(Node("vortex", status="not_occupied"))
                else:
                    row.append(Node("wall", status="not_occupied"))
        else:
            for x in range(dimensions[1]):
                if x % 2 == 0:
                    row.append(Node("wall", status="not_occupied"))
                else:
                    row.append(Node("tile", status="not_occupied"))
        grid.append(row)
    return grid

#!!---------
if __name__ == "__main__":

    grid = make_grid((11, 11))

    grid[1][1].tile_type = "swamp"

    for row in grid:
        for val in row:
            print(val, end="")
        
        print("\n", end="")


    
