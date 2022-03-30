import numpy as np
import numpy.ma as ma
import copy
from grid_maker import Node, make_grid
import json_loader
import os
import utils

""""
@grid: la grilla 
@detection_distance: distancia a la que detecta cosas
@initial_position: donde empieza el robot
@initial_orientation: donde empieza mirando 
"""
class Maze_Game():
    def __init__(self, grid:list, detection_distance:int, initial_position:list=[0,0], initial_orientation:str="up"):

        self.entire_grid = copy.deepcopy(grid)  # El mundo
        
        self.detection_distance = detection_distance
        self.grid_shape = [len(self.entire_grid), len(self.entire_grid[0])]


        self.dicovered_grid = self.create_discovered(self.entire_grid)

        self.directions = {"up":[-1,0], "down":[1,0], "right":[0,1], "left":[0,-1]}

        self.robot_position = initial_position
        self.robot_orientation = initial_orientation

        self.reacheable = self.get_reachable_nodes()
        self.explored = set()
        self.explored.add(tuple(self.robot_position))

        self.time_to_move = 1
        self.time_to_turn = 1

        self.total_time = 0

        self.updateMask()
    
    def reset_game(self, grid:list, initial_position:list=[0,0], initial_orientation:str="up"):
        self.entire_grid = copy.deepcopy(grid)
        self.dicovered_grid = self.create_discovered(self.entire_grid)
        self.robot_position = initial_position
        self.robot_orientation = initial_orientation
        self.updateMask()
        self.reacheable = self.get_reachable_nodes()
        self.explored = set()
        self.explored.add(tuple(self.robot_position))
        self.total_time = 0

        return self.dicovered_grid
    
    def get_reachable_nodes(self):
        # Create a queue to store nodes
        queue = []
        # Add the starting node
        queue.append(tuple(self.robot_position))
        # Create a set to store visited nodes
        visited = set()
        # While queue is not empty
        while queue:
            # Dequeue a node from queue and add it to visited set
            current_node = queue.pop(0)
            visited.add(current_node)
            adjacent_nodes = []
            for key, val in self.directions.items():
                adajcent = (current_node[0] + val[0]*2, current_node[1] + val[1]*2)
                if self.is_valid_move(key) and self.is_valid_position(adajcent):
                    adjacent_nodes.append(adajcent)
            # If any adjacent node is not visited, enqueue it
            for node in adjacent_nodes:
                if node not in visited and node not in queue:
                    queue.append(node)
        return visited


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
        
        # descubrir de la mascara todos indices dentro del cuadrado 
        #falso = ya descubierto 
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                self.dicovered_grid[x][y].status = self.entire_grid[x][y].status
                self.dicovered_grid[x][y].tile_type = self.entire_grid[x][y].tile_type

    def is_valid_move(self, move:str):
        if move not in self.directions.keys():
            return False
        new_pos = [(pos1 + pos2*2) for pos1, pos2 in zip(self.robot_position, self.directions[move])]
        middle_pos = [(pos1 + pos2) for pos1, pos2 in zip(self.robot_position, self.directions[move])]
        if self.is_valid_position(new_pos) and self.is_valid_position(middle_pos):
            return True
        else:
            return False

    # Executes a movement
    def move(self, move:str):
        if self.is_valid_move(move):
            new_pos = [(pos1 + pos2*2) for pos1, pos2 in zip(self.robot_position, self.directions[move])]
        
            # Change the robot position
            self.robot_position = new_pos

            # Number of turns to get to new orientation to be able to move in that direction
            n_turns = self.get_change_in_orientation(self.robot_orientation, move)

            # Set the orientation of the robot
            self.robot_orientation = move

            time_taken = self.time_to_move + (self.time_to_turn * n_turns)

            return True, time_taken
        else:
            return False, 0
    
    def is_in_bounds(self, position):
        is_valid = True
        # Is the position in bounds of the grid
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
        
        if self.entire_grid[position[0]][position[1]].node_type == "vortex":
            for adjacent in utils.get_adjacents(position):
                if self.is_in_bounds(adjacent):
                    if self.entire_grid[adjacent[0]][adjacent[1]].status == "occupied":
                        is_valid = False

        return is_valid
    
    def finished(self):
        #print("reacheable", self.reacheable)
        #print("explored", self.explored)
        return self.reacheable == self.explored

    # Runs a movement, returns if it was a valid one, the discovered grid and the time taken to do the movement
    def step(self, movement):
        valid_movement, time_taken = self.move(movement)
        self.updateMask()
        self.total_time += time_taken
        self.explored.add(tuple(self.robot_position))
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

    """
    # Esto crea un escenario de ejemplo

    grid = make_grid((17, 17))

    for value in grid[-1]:
        value.status = "occupied"
    
    for value in grid[0]:
        value.status = "occupied"
    
    for value in grid[12][6:16]:
        value.status = "occupied"
    
    for index, row in enumerate(grid):
        row[-1].status = "occupied"
        row[0].status = "occupied"
        if index in range(4, 9):
            row[8].status = "occupied"
    
    grid[1][1].tile_type = "start"
    grid[1][3].tile_type = "start"
    grid[3][1].tile_type = "start"
    grid[3][3].tile_type = "start"

    grid[-2][-2].tile_type = "hole"
    grid[-2][-4].tile_type = "hole"
    grid[-4][-2].tile_type = "hole"
    grid[-4][-4].tile_type = "hole"

    """
    script_dir = os.path.dirname(__file__)
    rel_path = "test1.json"
    abs_file_path = os.path.join(script_dir, rel_path)

    grid = json_loader.grid_from_json(abs_file_path)
     
    # Inicializa el juego
    maze = Maze_Game(grid, 4, initial_position=[2, 2])

    print("--------------------------------")
    print('Paramoverse ingresar "up", "down", "left" o "right".')
    print('Para salir ingresar "exit".')
    print("Agrandar la terminal si es necesario para que entre todo el mapa!")
    print('---------------------------------')
    input('Ingresar cualquier caracter para continuar: ')

    while True:
            maze.print_grid()
            move = input("move: ")
            if move == "exit": break
            valid_move, _, time_taken = maze.step(move)
            if not valid_move:
                print("invalid movement!")
            print("Time taken:", time_taken)



    

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
                
