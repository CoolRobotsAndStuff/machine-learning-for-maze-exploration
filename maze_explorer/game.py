import numpy as np
import numpy.ma as ma
import copy
from grid_maker import Node, make_grid
import json_loader
import os
import utils
import map_manager

""""
@grid: la grilla 
@detection_distance: distancia a la que detecta cosas
@initial_position: donde empieza el robot
@initial_orientation: donde empieza mirando 
"""
class Maze_Game():
    def __init__(self, grid:list, detection_distance:int, initial_position:tuple, initial_orientation:str="up"):
        # Distance from the center of the robot inside wich the robot will detect things
        self.detection_distance = detection_distance
        
        self.directions = {"up":[-1,0], "down":[1,0], "right":[0,1], "left":[0,-1]}
        self.time_to_move = 1
        self.time_to_turn = 1
        print("initial_position", initial_position)

        self.reset_game(grid, initial_position, initial_orientation)
    
    # Checks if a node is the start vortex
    def is_start_node(self, position):
        if self.entire_grid[position[1]][position[0]].node_type == "vortex":
            start_count = 0
            for adj in utils.get_adjacents(position, include_straight=False, include_diagonals=True):
                if self.is_in_bounds(adj):
                    if self.entire_grid[adj[0]][adj[1]].tile_type == "start":
                        start_count += 1
            return start_count == 4
        return False

    # Resets the game
    def reset_game(self, grid:list, initial_position:tuple, initial_orientation:str="up"):
       
        self.entire_grid = copy.deepcopy(grid)  # The world
        self.grid_shape = [len(self.entire_grid), len(self.entire_grid[0])]  # The shape of the world
        # The part of the world the robot has discovered so far
        self.dicovered_grid = self.create_discovered(self.entire_grid) 
        self.initial_position = initial_position # The initial position of the robot
        
        self.robot_position = self.initial_position
        self.robot_orientation = initial_orientation
        self.updateMask()  # Makes the robot discover the world aorund it
        self.reacheable = self.get_reachable_nodes()  # The tiles the robot is able to explore in the world
        self.explored = set() # The tiles the robot has explored in the world
        self.update_explored() # Add the tiles around it
        self.total_time = 0 # Total time in the run

        return self.dicovered_grid
    
    # Returns the nodes that are reachable from the robot
    def get_reachable_nodes(self):
        queue = []  # Create a queue to store nodes
        queue.append(tuple(self.robot_position))  # Add the starting node
        visited = set()  # Create a set to store visited verticies
        visited_tiles = set() # Create a set to store visited tiles around visited verticies
        # While queue is not empty
        while queue:
            # Dequeue a node from queue and add it to visited set
            current_node = queue.pop(0)
            visited.add(current_node)

            # Add the adjacent tiles of the node to the visited_tiles set
            for adj in utils.get_adjacents(current_node, include_straight=False, include_diagonals=True):
                if adj not in visited_tiles:
                    visited_tiles.add(adj)

            # Get the valid ajacent nodes
            adjacent_nodes = []
            for key, val in self.directions.items():
                adajcent = (current_node[0] + val[0]*2, current_node[1] + val[1]*2)
                if self.is_valid_move(current_node, key):
                    adjacent_nodes.append(adajcent)

            # If any adjacent node is not visited, enqueue it
            for node in adjacent_nodes:
                if node not in visited and node not in queue:
                    queue.append(node)
        return visited_tiles

    # Creates an empty grid for the robot to gradually discover
    # Only leaves the node_type, wich is already known
    def create_discovered(self, grid):
        disc_grid = []
        for row in grid:
            disc_row = []
            for value in row:
                new_value = copy.deepcopy(value)
                new_value.status = "undefined"
                new_value.tile_type = "undefined"
                disc_row.append(new_value)
            disc_grid.append(copy.deepcopy(disc_row))
        return disc_grid
            

    # Returns number of 90 deg turns to face in new orientation
    def get_change_in_orientation(self, initial_or, new_or):
        if initial_or == new_or:
            return 0

        opposites = (("up", "down"), ("left", "right"))
        for pair in opposites:
            if (initial_or, new_or) == pair or (new_or, initial_or) == pair: return 2 
        else: return 1

    # Makes the robot gradually "discover" the map
    def updateMask(self):
        #limites alrededor del robot en X
        min_x = max(self.robot_position[0] - self.detection_distance, 0)
        max_x = min(self.robot_position[0] + self.detection_distance + 1, self.grid_shape[0])
        #limites alrededor del robot en Y
        min_y = max(self.robot_position[1] - self.detection_distance, 0)
        max_y = min(self.robot_position[1] + self.detection_distance + 1, self.grid_shape[1])
        
        # añadir al mapa descubierto los nodos dentro del cuadrado
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                self.dicovered_grid[x][y].status = self.entire_grid[x][y].status
                self.dicovered_grid[x][y].tile_type = self.entire_grid[x][y].tile_type

    # Is the position in bounds of the grid
    def is_in_bounds(self, position):
        is_valid = True
        for pos, shape in zip(position, self.grid_shape[0:2]):
            if pos < 0 or pos > shape -1:
                is_valid = False
        return is_valid

    # Is a position valid?
    def is_valid_position(self, position):
        is_valid = self.is_in_bounds(position)
        # Is the position not occupied
        if is_valid:
            is_valid = self.entire_grid[position[0]][position[1]].status != "occupied"
        
        if self.entire_grid[position[0]][position[1]].tile_type == "hole":
            is_valid = False
        
        # Are the walls surrounding the position not occupied
        for adjacent in utils.get_adjacents(position):
            if self.is_in_bounds(adjacent):
                if self.entire_grid[adjacent[0]][adjacent[1]].status == "occupied":
                    is_valid = False
            else:
                is_valid = False
        
        for diag_adj in utils.get_adjacents(position, include_straight = False, include_diagonals=True):
            if self.is_in_bounds(diag_adj):
                if self.entire_grid[diag_adj[0]][diag_adj[1]].status == "occupied":
                    is_valid = False
                if self.entire_grid[diag_adj[0]][diag_adj[1]].tile_type == "hole":
                    is_valid = False
            else:
                is_valid = False

        return is_valid

    # Given the initial position and the direction of the movement, is it valid?
    def is_valid_move(self, init_pos:list, move:str):
        if move not in self.directions.keys():
            return False
        new_pos = [(pos1 + pos2*2) for pos1, pos2 in zip(init_pos, self.directions[move])]
        middle_pos = [(pos1 + pos2) for pos1, pos2 in zip(init_pos, self.directions[move])]
        if self.is_valid_position(new_pos) and self.is_valid_position(middle_pos):
            return True
        else:
            return False

    # Executes a movement. Returns if the movement was valid and the time taken to do it.
    def move(self, move:str):
        if self.is_valid_move(self.robot_position, move):
            new_pos = [(pos1 + pos2*2) for pos1, pos2 in zip(self.robot_position, self.directions[move])]
            # Change the robot position
            self.robot_position = new_pos
            # Number of turns to get to new orientation to be able to move in that direction
            n_turns = self.get_change_in_orientation(self.robot_orientation, move)
            # Set the orientation of the robot
            self.robot_orientation = move
            # Time taken to execute the movement
            time_taken = self.time_to_move + (self.time_to_turn * n_turns)

            return True, time_taken
        else:
            return False, 0
    
    # If the robot has explored the entire grid
    def finished(self):
        #print("reacheable", self.reacheable)
        #print("explored", self.explored)
        #print("left", self.reacheable - self.explored)
        return self.reacheable == self.explored
    
    # Updates the part of the map the robot can see depending on its position
    def update_explored(self):

        for adj in utils.get_adjacents(self.robot_position, include_straight=False, include_diagonals=True):
            if adj not in self.explored:
                self.explored.add(adj)
        
        for adj in utils.get_adjacents(self.robot_position, include_straight=True, include_diagonals=True):
            self.entire_grid[adj[0]][adj[1]].explored = True
        
        self.entire_grid[self.robot_position[0]][self.robot_position[1]].explored = True

    # Runs a movement, returns if it was a valid one, the discovered grid and the time taken to do the movement
    def step(self, movement):
        valid_movement, time_taken = self.move(movement)
        self.updateMask()
        self.total_time += time_taken
        self.update_explored()
        for y, row in enumerate(self.entire_grid):
            for x, node in enumerate(row):
                if [x, y] == self.robot_position:
                    node.is_robots_position = True
                else:
                    node.is_robots_position = False
                
        return valid_movement, self.dicovered_grid, self.total_time

    def print_status(self):
        print("robot_postion =", self.robot_position)
        print("robot_orientation =", self.robot_orientation)

    # prints the grid for easy visualization
    def print_grid(self):

        robot_right = [self.robot_position[0], self.robot_position[1] + 1]
        robot_left = [self.robot_position[0], self.robot_position[1] - 1]
        robot_up = [self.robot_position[0] - 1, self.robot_position[1]]
        robot_down = [self.robot_position[0] + 1, self.robot_position[1]]

        for x, row in enumerate(self.dicovered_grid):
            for y, value in enumerate(row):
                if [x, y] == self.robot_position:
                    print("ob", end="")
                elif [x, y] == robot_right:
                    print(".|", end="")
                elif [x, y] == robot_left:
                    print("|R", end="")
                elif [x, y] == robot_up:
                    print("──", end="")
                elif [x, y] == robot_down:
                    print("──", end="")
                elif y == robot_right[1] and x == robot_up[0]:
                    print("◣ ", end="")
                elif y == robot_left[1] and x == robot_up[0]:
                    print(" ◢", end="")
                elif y == robot_left[1] and x == robot_down[0]:
                    print(" ◥", end="")
                elif y == robot_right[1] and x == robot_down[0]:
                    print("◤ ", end="")
                
                else:
                    print(str(value), end="")
            print("\n", end="")
        print("")


if __name__ == "__main__":
    # Loads a map
    script_dir = os.path.dirname(__file__)
    rel_path = "test_maps/map_1.map"
    abs_file_path = os.path.join(script_dir, rel_path)

    grid, map_data = map_manager.load_map(abs_file_path) #json_loader.grid_from_json(abs_file_path)
     
    # Inicializa el juego
    maze = Maze_Game(grid, 4, map_data["start_node"])

    print("--------------------------------")
    print('Paramoverse ingresar "up", "down", "left" o "right".')
    print('Para salir ingresar "exit".')
    print("Agrandar la terminal si es necesario para que entre todo el mapa!")
    print('---------------------------------')
    input('Ingresar cualquier caracter para continuar: ')
    maze.print_grid()

    while True:
            move = input("move: ")
            if move == "exit": break

            valid_move, _, time_taken = maze.step(move)
            if not valid_move:
                print("invalid movement!")
            print("Time in run:", time_taken)
            maze.print_grid()

            if maze.finished():
                print("Finished!")
                break



    

        # Just ignore this used for lidar
"""
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                self.disc_mask[x, y] = False

        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                diff_x = self.robot_position[0] - x
                diff_y = self.robot_position[1] - y

                if diff_x == 0 and diff_y == 0:
                    self.disc_mask[x, y] = False
                
                pos_diff_x = diff_x * -1 if diff_x < 0 else  diff_x
                pos_diff_y = diff_y * -1 if diff_y < 0 else  diff_y
                
                if pos_diff_y < pos_diff_x:
                    #print(diff_x)
                    if diff_x <= 0:
                        for x1 in range(x, self.robot_position[0], -1):
                            print((x1, y))
                            self.disc_mask[x1, y] = True
                            if self.entire_grid[x1, y] == 1:
                                break
                              
                    else:
                        for x1 in range(x, self.robot_position[0]):
                            self.disc_mask[x1, y] = True
                            if self.entire_grid[x1, y] == 1:
                                break
                            
                else:
                    if diff_y <= 0:
                        for y1 in range(y, self.robot_position[1], -1):
                            print((x, y1))
                            self.disc_mask[x, y1] = True
                            if self.entire_grid[x, y1] == 1:
                                break
                            
                    else:
                        for y1 in range(y, self.robot_position[1]):
                            self.disc_mask[x, y1] = True
                            if self.entire_grid[x, y1] == 1:
                                break
        """
                
