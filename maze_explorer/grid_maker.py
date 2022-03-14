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
        

        self.node_type_conv = {"tile":0.0, "vortex":0.5, "wall":1.0} #dic for converting to num values
        
        self.status_conv = {"occupied":1.0,
                            "undefined":0.5,
                            "not_occupied":0.0}# same dic 
        self.tile_type_conv = {"undefined":0.0, 
                                "normal": 0.1, 
                                "start": 0.2, 
                                "connection1-2": 0.3, 
                                "connection1-3":0.4, 
                                "connection2-3": 0.5, 
                                "swamp": 0.6, 
                                "hole": 0.7} #same dic

        
    
    def get_representation(self) -> list: #tipo de nodo tipo de estado  tipo de casilla 
        rep = []
        rep.append(self.node_type_conv[self.node_type])
        rep.append(self.status_conv[self.status])
        rep.append(self.tile_type_conv[self.tile_type])
        
        return rep

    def __str__(self) -> str:
        if self.status == "undefined":
            return "?"
        if self.status == "occupied":
            return "■"
        elif self.node_type == "wall":
            return "-"
        elif self.node_type == "vortex": #vertice
            return "+"
        elif self.node_type == "tile":
            return "□"

    def __repr__(self) -> str:
        if self.status == "undefined":
            return "?"
        if self.status == "occupied":
            return "■"
        elif self.node_type == "wall":
            return "-"
        elif self.node_type == "vortex":
            return "+"
        elif self.node_type == "tile":
            return "□"


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


    
