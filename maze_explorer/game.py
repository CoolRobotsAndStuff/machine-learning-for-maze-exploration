import numpy as np
import numpy.ma as ma
import copy
import json_loader
import os
import utils
import map_manager
from bresenham import bresenham

""""
@grid: la grilla 
@initial_position: donde empieza el robot
@initial_orientation: donde empieza mirando 
"""
class Maze_Game():
    def __init__(self, grid:list, initial_position:tuple, initial_orientation:str="up"):
        # Distance from the center of the robot inside wich the robot will detect things
        self.detection_distance = 4 * 3

        # The tiles of wich the robot can see the color.
        self.color_detection_mask = np.array([
            [0, 0, 0,   0,   0, 0, 0,   0,   1, 0, 1,   0,   1, 0, 1,   0,   1, 0, 1,   0,   0, 0, 0,   0,   0, 0, 0],
            [0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0],
            [0, 0, 0,   0,   0, 0, 0,   0,   1, 0, 1,   0,   1, 0, 1,   0,   1, 0, 1,   0,   0, 0, 0,   0,   0, 0, 0],

            [0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0],

            [0, 0, 0,   0,   0, 0, 0,   0,   1, 0, 1,   0,   1, 0, 1,   0,   1, 0, 1,   0,   0, 0, 0,   0,   0, 0, 0],
            [0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0],
            [0, 0, 0,   0,   0, 0, 0,   0,   1, 0, 1,   0,   1, 0, 1,   0,   1, 0, 1,   0,   0, 0, 0,   0,   0, 0, 0],

            [0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0],

            [1, 0, 1,   0,   1, 0, 1,   0,   0, 0, 0,   0,   1, 0, 1,   0,   0, 0, 0,   0,   1, 0, 1,   0,   1, 0, 1],
            [0, 0, 0,   0,   0, 0, 1,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0],
            [1, 0, 1,   0,   1, 0, 1,   0,   0, 0, 0,   0,   1, 0, 1,   0,   0, 0, 0,   0,   1, 0, 1,   0,   1, 0, 1],

            [0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0],

            [1, 0, 1,   0,   1, 0, 1,   0,   1, 0, 1,   0,   0, 0, 0,   0,   1, 0, 1,   0,   1, 0, 1,   0,   1, 0, 1],
            [0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0],
            [1, 0, 1,   0,   1, 0, 1,   0,   1, 0, 1,   0,   0, 0, 0,   0,   1, 0, 1,   0,   1, 0, 1,   0,   1, 0, 1],

            [0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0],

            [1, 0, 1,   0,   1, 0, 1,   0,   0, 0, 0,   0,   1, 0, 1,   0,   0, 0, 0,   0,   1, 0, 1,   0,   1, 0, 1],
            [0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0],
            [1, 0, 1,   0,   1, 0, 1,   0,   0, 0, 0,   0,   1, 0, 1,   0,   0, 0, 0,   0,   1, 0, 1,   0,   1, 0, 1],

            [0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0],

            [0, 0, 0,   0,   0, 0, 0,   0,   1, 0, 1,   0,   1, 0, 1,   0,   1, 0, 1,   0,   0, 0, 0,   0,   0, 0, 0],
            [0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0],
            [0, 0, 0,   0,   0, 0, 0,   0,   1, 0, 1,   0,   1, 0, 1,   0,   1, 0, 1,   0,   0, 0, 0,   0,   0, 0, 0],

            [0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0],

            [0, 0, 0,   0,   0, 0, 0,   0,   1, 0, 1,   0,   1, 0, 1,   0,   1, 0, 1,   0,   0, 0, 0,   0,   0, 0, 0],
            [0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0,   0,   0, 0, 0],
            [0, 0, 0,   0,   0, 0, 0,   0,   1, 0, 1,   0,   1, 0, 1,   0,   1, 0, 1,   0,   0, 0, 0,   0,   0, 0, 0],

        ])

        # The directions in which the robot can move
        self.directions = {"up":[-1,0], "down":[1,0], "right":[0,1], "left":[0,-1]}

        # Abreviations for the directions
        self.abreviations= {"u":"up", "d":"down", "r":"right", "l":"left"}

        
        self.time_to_move = 0.6  # Time to move one tile in a straight line in a normal tile
        self.time_to_turn_90 = 0.928 # Time to turn 90 degrees in a normal tile
        self.time_to_turn_180 = 1.632 # Time to turn 180 degrees in a normal tile

        # Times to move in a stright line in a swamp tile
        self.swamp_times = {
            1: 0.66,
            2: 1.626,
        }

        # Times to turn in a swamp tile
        self.swamp_turn_times = {
            4: {90:1.1676, 180:2.3375},
            2: {90:(1.1676 * 0.50) + (self.time_to_turn_90 * 0.50), 180:(2.3375 * 0.50) + (self.time_to_turn_180 * 0.50)},
            1: {90:(1.1676 * 0.25) + (self.time_to_turn_90 * 0.75), 180:(2.3375 * 0.25) + (self.time_to_turn_180 * 0.75)},
            }

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
        
        final_tiles = set()
        for visited_tile in visited_tiles:
            adjacents = utils.get_adjacents(visited_tile, include_straight=True, include_diagonals=False)
            for adjacent in adjacents:
                if self.entire_grid[adjacent[0]][adjacent[1]].node_type == "wall":
                    if self.entire_grid[adjacent[0]][adjacent[1]].status == "occupied":
                        final_tiles.add(visited_tile)
                        break
            
        return final_tiles

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

        # Counts the number of swamp tiles adjacent to the actual position
        adj_tiles = utils.get_adjacents(self.robot_position, include_straight=False, include_diagonals=True)

        swamp_n = 0

        for tile in adj_tiles:
            if self.entire_grid[tile[0]][tile[1]].node_type == "tile":
                if self.entire_grid[tile[0]][tile[1]].tile_type == "swamp":
                    swamp_n += 1

        if initial_or == new_or:
            return 0

        opposites = (("up", "down"), ("left", "right"))
        for pair in opposites:
            if (initial_or, new_or) == pair or (new_or, initial_or) == pair: 
                if swamp_n == 0:
                    return self.time_to_turn_180
                else:
                    return self.swamp_turn_times[swamp_n][180]
        else:
            if swamp_n == 0:
                return self.time_to_turn_90
            else:
                return self.swamp_turn_times[swamp_n][90]

    # Checks if a position is visible from the robot using the bresenham line algorithm
    def is_visible(self, position):
        intermediate = list(bresenham(self.robot_position[0], self.robot_position[1], position[0], position[1]))
        intermediate.remove(position)
        is_valid = True
        for intermidiate_point in intermediate:
            if self.entire_grid[intermidiate_point[0]][intermidiate_point[1]].status == "occupied":
                is_valid = False
                break
        return is_valid

    # Makes the robot discover the world around it
    def updateMask(self):
        # Limits around the robot in X
        min_x = max(self.robot_position[0] - self.detection_distance, 0)
        max_x = min(self.robot_position[0] + self.detection_distance + 1, self.grid_shape[0])
        # Limits around the robot in Y
        min_y = max(self.robot_position[1] - self.detection_distance, 0)
        max_y = min(self.robot_position[1] + self.detection_distance + 1, self.grid_shape[1])
        
        # Adds the lidar detections to the discovered map
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                if utils.get_distance(self.robot_position, (x, y)) <= self.detection_distance:
                    if self.is_visible((x, y)): 
                        self.dicovered_grid[x][y].status = self.entire_grid[x][y].status

        # Adds the color detections to the discovered map
        center = (self.color_detection_mask.shape[0] // 2, self.color_detection_mask.shape[1] // 2)
        for x, row in enumerate(self.color_detection_mask):
            for y, node in enumerate(row):
                if node == 1:
                    pos = (self.robot_position[0] + x - center[0], self.robot_position[1] + y - center[1])
                    if pos[0] < 0 or pos[0] >= self.grid_shape[0] or pos[1] < 0 or pos[1] >= self.grid_shape[1]:
                        continue
                    if self.is_visible(pos):
                        self.dicovered_grid[pos[0]][pos[1]].tile_type = self.entire_grid[pos[0]][pos[1]].tile_type
                #self.dicovered_grid[x][y].status = self.entire_grid[y][x].status


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
        
        # Is the position not occupied and not a hole
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

        # If an abreviation is given, convert it to the full direction
        if move not in self.directions.keys():
            if move in self.abreviations.keys():
                move = self.abreviations[move]

        if self.is_valid_move(self.robot_position, move):
            new_pos = [(pos1 + pos2*2) for pos1, pos2 in zip(self.robot_position, self.directions[move])]
            intermediate_pos = [(pos1 + pos2) for pos1, pos2 in zip(self.robot_position, self.directions[move])]
            # Change the robot position
            self.robot_position = new_pos

            # Checks the amount of swampp tiles the robot will have to traverse
            adjacents = utils.get_adjacents(intermediate_pos)
            n_swamps = 0
            for adjacent in adjacents:
                if not self.is_in_bounds(adjacent):
                    continue
                if self.entire_grid[adjacent[0]][adjacent[1]].tile_type == "swamp":
                    n_swamps += 1

            # Time necessary to turn to get to new orientation to be able to move in that direction
            time_to_turn = self.get_change_in_orientation(self.robot_orientation, move)
            # Set the orientation of the robot
            self.robot_orientation = move
            # Time taken to execute the movement
            if n_swamps > 0:
                time_taken = self.swamp_times[n_swamps] + time_to_turn
            else:
                time_taken = self.time_to_move + time_to_turn

            return True, time_taken
        else:
            return False, 0
    
    def is_robot_in_start(self):
        adjacents = utils.get_adjacents(self.robot_position, include_straight = False, include_diagonals=True)
        for adjacent in adjacents:
            if self.entire_grid[adjacent[0]][adjacent[1]].tile_type == "start":
                return True
    
    # If the robot has explored the required part of the maze and gone back to the start
    def finished(self):
        #print("reacheable", self.reacheable)
        #print("explored", self.explored)
        #print("left", self.reacheable - self.explored)
        return self.reacheable.issubset(self.explored) and self.is_robot_in_start()
    
    # Saves the parts of the map the robot has passed trough
    def update_explored(self):

        for adj in utils.get_adjacents(self.robot_position, include_straight=False, include_diagonals=True):
            if adj not in self.explored:
                self.explored.add(adj)
        
        for adj in utils.get_adjacents(self.robot_position, include_straight=True, include_diagonals=True):
            self.entire_grid[adj[0]][adj[1]].explored = True
        
        self.entire_grid[self.robot_position[0]][self.robot_position[1]].explored = True

    # Runs a movement, returns if it was a valid one, the discovered grid, the time in the run and the time taken to do the movement
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
                
        return valid_movement, self.dicovered_grid, self.total_time, time_taken

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
                    if self.robot_orientation == "up":
                        print("↑ ", end="")
                    elif self.robot_orientation == "down":
                        print("↓ ", end="")
                    elif self.robot_orientation == "left":
                        print("<-", end="")
                    elif self.robot_orientation == "right":
                        print("->", end="")
                elif [x, y] == robot_right:
                    if self.robot_orientation == "up" or self.robot_orientation == "down":
                        print(" █", end="")
                    else:
                        print(" |", end="")
                elif [x, y] == robot_left:
                    if self.robot_orientation == "up" or self.robot_orientation == "down":
                        print("█ ", end="")
                    else:
                        print("| ", end="")
                elif [x, y] == robot_up:
                    if self.robot_orientation == "left" or self.robot_orientation == "right":
                        print("▀▀", end="")
                    else:
                        print("──", end="")
                elif [x, y] == robot_down:
                    if self.robot_orientation == "left" or self.robot_orientation == "right":
                        print("▄▄", end="")
                    else:
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
    rel_path = "test_maps/map_2.map"
    abs_file_path = os.path.join(script_dir, rel_path)

    grid, map_data = map_manager.load_map(abs_file_path) #json_loader.grid_from_json(abs_file_path)
     
    # Inicializa el juego
    maze = Maze_Game(grid, map_data["start_node"])

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

            valid_move, _, _, time_taken = maze.step(move)
            if not valid_move:
                print("invalid movement!")
            print("Time taken:", time_taken)
            maze.print_grid()

            if maze.finished():
                print("Finished!")
                break