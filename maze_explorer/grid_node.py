"""
Requirements:

1 = Node type (tile, vortex, wall)
2 = Status (ocupied, not_occupied, undefined)
3 = Tile type (only if tile: undefined, start, normal, connection1-2, connection1-3, connection2-3, swamp, hole)

undefined = no conozco el tipo de casilla
"""

class Node():
    def __init__(self, node_type:str, status:str="undefined", tile_type:str="undefined", curved:int=0, explored:bool=False, is_robots_position:bool=False):
        self.node_type = node_type
        self.status = status
        self.tile_type = tile_type if node_type == "tile" else "undefined"
        self.explored = explored
        self.is_robots_position = is_robots_position
        

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
            if not(self.node_type == "tile" and self.tile_type != "undefined"):    
                return "??"

        if self.status == "occupied":
            return "\033[1;30;40m██" + "\033[0m"

        elif self.node_type == "wall":
            """
            if self.status == "not_occupied":
                return "\033[1;37;47m██"+ "\033[0m"
            """
            return "\033[1;30;47m||"+ "\033[0m"
        elif self.node_type == "vortex": #vertice
            """
            if self.status == "not_occupied":
                return "\033[1;37;47m██"+ "\033[0m"
            """
            return "\033[1;30;47m<>"+ "\033[0m"
        elif self.node_type == "tile":
            if self.tile_type == "start":
                return "\033[1;32;47m██"+ "\033[0m"
            if self.tile_type == "hole":
                return "\033[0m  "+ "\033[0m"
            if self.tile_type == "swamp":
                return "\033[1;33;40m██"+ "\033[0m"
            if self.tile_type == "checkpoint":
                return "\033[0m██"+ "\033[0m"
            if self.tile_type == "connection1-3":
                return "\033[1;35;47m██"+ "\033[0m"
            if self.tile_type == "connection1-2":
                return "\033[1;34;47m██"+ "\033[0m"
            if self.tile_type == "connection2-3":
                return "\033[1;31;47m██"+ "\033[0m"
            if self.tile_type == "normal":
                return "\033[1;37;47m██"+ "\033[0m"

            return "\033[1;30;47m??"+ "\033[0m"

        
    def __str__(self) -> str:
        return self.get_string()

    def __repr__(self) -> str:
        return self.get_string()
