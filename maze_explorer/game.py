import numpy as np
import numpy.ma as ma
import copy


class Maze_game():
    def __init__(self, grid, detection_distance, initial_position=[0,0], initial_orientation="up"):

        self.raw_grid = copy.deepcopy(grid)
        
        self.detection_distance = detection_distance
        self.entire_grid = self.convert_grid(self.raw_grid)
        self.grid_shape = self.entire_grid.shape

        self.disc_mask = np.ones(self.grid_shape, dtype=np.bool_)
        print(self.disc_mask)
        self.dicovered_grid = np.zeros(self.grid_shape)

        self.valid_orientations = ("up", "down", "left", "right")
        self.valid_actions = ["up", "down", "left", "right"]
        self.actions_pos_dict = {"up":[-1,0], "down":[1,0], "right":[0,1], "left":[0,-1]}

        self.robot_position = initial_position
        self.robot_orientation = initial_orientation

        self.time_to_move = 1
        self.time_to_turn = 1
        
    
    # Pre-processes the given grid
    def convert_grid(self, raw_grid):
        return np.array(raw_grid)

    # Returns number of 90 deg turns to face in new orientation
    def get_change_in_orientation(self, or1, or2):
        opposites = (("up", "down"), ("left, right"))
        for pair in opposites:
            if (or1, or2) == pair or (or2, or1) == pair: return 2 
            else: return 1

    # Executes a movement
    def move(self, move):
        
        if move not in self.valid_actions:
            print("Invalid movement")
            return False, 0

        # Calculate the new position
        new_pos = [(pos1 + pos2) for pos1, pos2 in zip(self.robot_position, self.actions_pos_dict[move])]

        # Check if the new position is valid
        if self.is_valid_position(new_pos):

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
            is_valid = self.entire_grid[position[0]][position[1]] != 1

        return is_valid

    def step(self, movement):
        self.move(movement)
        

    def print_status(self):
        print("robot_postion =", self.robot_position)
        print("robot_orientation =", self.robot_orientation)

    def print_grid(self):
        mx = ma.fix_invalid(self.entire_grid, self.disc_mask, fill_value=3)
        final_grid = mx.filled(3)
        for x, row in enumerate(final_grid): #self.entire_grid):
            for y, value in enumerate(row):
                if [x, y] == self.robot_position:
                    print("R" + " ", end="")
                else:
                    print(str(value) + " ", end="")
            print("\n", end="")



grid = [
        [1, 0, 1, 0, 0, 0],
        [1, 0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1]
        ]

maze = Maze_game(grid, 5)
maze.print_grid()

"""
while True:
    maze.print_grid()
    move = input("move: ")
    if move == "exit": break
    maze.move(move)
"""

    

