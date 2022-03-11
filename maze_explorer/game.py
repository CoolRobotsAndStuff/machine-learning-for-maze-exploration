import string
from typing import List
import numpy as np
import numpy.ma as ma
import copy
from grid_maker import Node, make_grid
""""
@grid: la grilla 
@detection_distance: distancia a la que detecta cosas
@initial_position: donde empieza el robot
@initial_orientation: donde empieza mirando 
"""
class Maze_game():
    def __init__(self, grid:list, detection_distance:int, initial_position:list=[0,0], initial_orientation:string="up"):

        self.raw_grid = copy.deepcopy(grid) 
        
        self.detection_distance = detection_distance
        self.entire_grid = self.convert_grid(self.raw_grid) #el mundo
        self.grid_shape = self.entire_grid.shape

        self.disc_mask = np.ones(self.grid_shape, dtype=np.bool_)
        self.disc_mask[0:-1, 0:-1, 0] = False #oculta todo menos tipo de nodo
        print(self.disc_mask) 
        self.dicovered_grid = np.zeros(self.grid_shape) #!TODO REFACTOR
        #!REFACTOR MAYBE
        self.valid_orientations = ("up", "down", "left", "right")
        self.valid_actions = ["up", "down", "left", "right"]
        self.actions_pos_dict = {"up":[-1,0], "down":[1,0], "right":[0,1], "left":[0,-1]}

        self.robot_position = initial_position
        self.robot_orientation = initial_orientation

        self.time_to_move = 1
        self.time_to_turn = 1

        self.updateMask()
    
    # Pre-processes the given grid
    def convert_grid(self, raw_grid): #Convert nodes to numbers
        final_list = []
        for column in raw_grid:
            f_col = []
            for value in column:
                f_col.append(value.get_representation())
            final_list.append(f_col)


        return np.array(final_list)

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
        self.disc_mask[min_x:max_x, min_y:max_y, 1:-1] = False

    # Executes a movement
    def move(self, move:string):
        if move not in self.valid_actions:
            return False, 0 # no logro moverse, tardo 0ut

        # Calculate the new position
        new_pos = [(pos1 + pos2*2) for pos1, pos2 in zip(self.robot_position, self.actions_pos_dict[move])]
        #calcula la posicion por la que paso para llegar a new_pos
        middle_pos = [(pos1 + pos2) for pos1, pos2 in zip(self.robot_position, self.actions_pos_dict[move])]

        # Check if the new position is valid
        if self.is_valid_position(new_pos) and self.is_valid_position(middle_pos):

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
    
    # Is a position valid?
    def is_valid_position(self, position):
        is_valid = True

        # Is the position in bounds of the grid
        for pos, shape in zip(position, self.grid_shape[0:2]):
            if pos < 0 or pos > shape -1:
                is_valid = False

        # Is the position not occupied
        if is_valid:
            #1 = esta ocupado
            is_valid = self.entire_grid[position[0]][position[1]][1] != 1

        return is_valid

    # Runs a movement, returns if it was a valid one, the discovered grid and the time taken
    # to do the movement
    def step(self, movement):
        valid_movement, time_taken = self.move(movement)
        self.updateMask()
        return valid_movement, self.get_grid(), time_taken
        

    def print_status(self):
        print("robot_postion =", self.robot_position)
        print("robot_orientation =", self.robot_orientation)

    # prints the grid for easy visualization
    def print_grid(self):
        mx = ma.fix_invalid(self.entire_grid, self.disc_mask, fill_value=0.5)
        final_grid = mx.filled(0.5)
        for x, row in enumerate(final_grid): #self.entire_grid):
            for y, value in enumerate(row):
                if [x, y] == self.robot_position:
                    print("Rob" + " ", end="")
                else:
                    print(str(value[0]) + " ", end="")
            print("\n", end="")

        print("")

    def get_grid(self):
        #check this
        mx = ma.fix_invalid(self.entire_grid, self.disc_mask, fill_value=0.5)
        final_grid = mx.filled(0.5)

        return final_grid

if __name__ == "__main__":
    grid = make_grid((7, 7))
    maze = Maze_game(grid, 1, initial_position=[0, 0])
    maze.print_grid()
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
                
