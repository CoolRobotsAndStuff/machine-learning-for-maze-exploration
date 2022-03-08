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
        self.actions_pos_dict = {"up":[-2,0], "down":[2,0], "right":[0,2], "left":[0,-2]}

        self.robot_position = initial_position
        self.robot_orientation = initial_orientation

        self.time_to_move = 1
        self.time_to_turn = 1

        self.updateMask()
    
    # Pre-processes the given grid
    def convert_grid(self, raw_grid):
        return np.array(raw_grid)

    # Returns number of 90 deg turns to face in new orientation
    def get_change_in_orientation(self, or1, or2):
        opposites = (("up", "down"), ("left, right"))
        for pair in opposites:
            if (or1, or2) == pair or (or2, or1) == pair: return 2 
            else: return 1

    # Makes the robot gradually "discover" the map
    def updateMask(self):

        min_x = max(self.robot_position[0] - self.detection_distance, 0)
        max_x = min(self.robot_position[0] + self.detection_distance + 1, self.grid_shape[0])

        min_y = max(self.robot_position[1] - self.detection_distance, 0)
        max_y = min(self.robot_position[1] + self.detection_distance + 1, self.grid_shape[1])
        
        self.disc_mask[min_x:max_x, min_y:max_y] = False
        
        # Just ignore this v
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

    # Runs a movement, returns if it was a valid one, the deicovered grid and the time taken
    # to do the movement
    def step(self, movement):
        valid_movement, time_taken = self.move(movement)
        self.updateMask()
        return valid_movement, self.get_grid(), self.time_taken
        

    def print_status(self):
        print("robot_postion =", self.robot_position)
        print("robot_orientation =", self.robot_orientation)

    # prints the grid for easy visualization
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

        print("")

    def get_grid(self):
        mx = ma.fix_invalid(self.entire_grid, self.disc_mask, fill_value=3)
        final_grid = mx.filled(3)

        return final_grid




grid = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 1, 1],
        [0, 1, 0, 0, 1, 1],
        [0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0]
        ]

def main():
    maze = Maze_game(grid, 3, initial_position=[2, 2])
    maze.print_grid()


    while True:
        maze.print_grid()
        move = input("move: ")
        if move == "exit": break
        maze.step(move)


    

