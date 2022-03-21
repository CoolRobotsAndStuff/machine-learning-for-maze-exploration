import string
import numpy as np
import math

"""
Requirements:

1 = Node type (tile, vortex, wall)
2 = Status (ocupied, not_occupied, undefined)
3 = Tile type (only if tile: undefined, start, normal, connection1-2, connection1-3, connection2-3, swamp, hole)

undefined = no conozco el tipo de casilla
"""

class Node():
    def __init__(self, node_type:string, status:string="undefined", tile_type:string="undefined"):
        self.node_type = node_type
        self.status = status
        self.tile_type = tile_type if node_type == "tile" else "undefined"
        

        self.valid_node_type = ("tile", 
                                "vortex",
                                "wall") #tuple with valid values for the variables of the node
        
        self.valid_status = (   "occupied",
                                "undefined",
                                "not_occupied") #same tuple

        self.tile_type_conv = ("undefined",
                                "normal",
                                "start",
                                "connection1-2",
                                "connection1-3", 
                                "connection2-3", 
                                "swamp", 
                                "hole") #same tuple

    # Returns a visual representation of the node in ASCII 
    def get_string(self):
        if self.status == "undefined":
            return "??"
        elif self.status == "occupied":
            return "\033[1;30;40m██" + "\033[0m"

        elif self.node_type == "wall":
            if self.status == "not_occupied":
                return "\033[1;37;47m██"+ "\033[0m"
            return "--"
        elif self.node_type == "vortex": #vertice
            if self.status == "not_occupied":
                return "\033[1;37;47m██"+ "\033[0m"
            
            return "<>"
        elif self.node_type == "tile":
            if self.tile_type == "start":
                return "\033[1;32;47m██"+ "\033[0m"
            if self.tile_type == "hole":
                return "\033[1;30;47m██"+ "\033[0m"
            if self.tile_type == "swamp":
                return "\033[1;33;47m██"+ "\033[0m"
            if self.tile_type == "checkpoint":
                return "\033[1;36;47m██"+ "\033[0m"
            if self.tile_type == "connection1-3":
                return "\033[1;35;47m██"+ "\033[0m"
            if self.tile_type == "connection1-2":
                return "\033[1;34;47m██"+ "\033[0m"
            if self.tile_type == "connection2-3":
                return "\033[1;31;47m██"+ "\033[0m"

            return "\033[1;37;47m██"+ "\033[0m"

        
    def __str__(self) -> str:
        return self.get_string()

    def __repr__(self) -> str:
        return self.get_string()


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

    grid[0][0].tile_type = "start"

    for row in grid:
        for val in row:
            print(val.get_representation()[2], end=" ")
        
        print("\n", end="")


    
