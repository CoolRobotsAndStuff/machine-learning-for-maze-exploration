import numpy as np
import os
import gym
from game import Maze_Game
import json_loader

one_hot_node_type_encoder = {
    "tile": np.array([1, 0, 0]),
    "vortex": np.array([0, 1, 0]),
    "wall": np.array([0, 0, 1])
}

one_hot_tile_type_encoder = {
    "undefined": np.array([1, 0, 0, 0, 0, 0, 0, 0, 0]),
    "normal": np.array([0, 1, 0, 0, 0, 0, 0, 0, 0]),
    "start": np.array([0, 0, 1, 0, 0, 0, 0, 0, 0]),
    "connection1-2": np.array([0, 0, 0, 1, 0, 0, 0, 0, 0]),
    "connection1-3": np.array([0, 0, 0, 0, 1, 0, 0, 0, 0]),
    "connection2-3": np.array([0, 0, 0, 0, 0, 1, 0, 0, 0]),
    "swamp": np.array([0, 0, 0, 0, 0, 0, 1, 0, 0]),
    "hole": np.array([0, 0, 0, 0, 0, 0, 0, 1, 0]),
    "checkpoint": np.array([0, 0, 0, 0, 0, 0, 0, 0, 1])
}

one_hot_status_encoder = {
    "occupied": np.array([1, 0, 0]),
    "undefined": np.array([0, 1, 0]),
    "not_occupied": np.array([0, 0, 1])
}

# Encodes a single node
def get_one_hot_form_node(node):
    return np.concatenate((one_hot_node_type_encoder[node.node_type], one_hot_status_encoder[node.status], one_hot_tile_type_encoder[node.tile_type]))

# Encodes the entire grid and returns it as a numpy array
def grid_to_one_hot(grid):
    one_hot_grid = list()
    for row in grid:
        one_hot_row = list()
        for node in row:
            one_hot_row.append(get_one_hot_form_node(node))
        one_hot_grid.append(one_hot_row)
    return np.array(one_hot_grid)

class Maze_Environment(Maze_Game, gym.Env):
    def __init__(self, grid: list, detection_distance: int, initial_orientation: str = "up"):
        super().__init__(grid, detection_distance, initial_orientation)
        self.grid = grid
        self.initial_orientation = initial_orientation

        # Action space
        self.action_space = gym.spaces.Discrete(4)
        # Observation space
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(len(self.entire_grid), len(self.entire_grid[0]), 15), dtype=np.float32)

        # Converts the output if the model to an action for the game
        self.action_to_str = {
            0: "up",
            1: "down",
            2: "left",
            3: "right"
        }

    def step(self, action):
        valid_movement, discovered_grid, actual_time = super().step(self.action_to_str[action])
        state = grid_to_one_hot(discovered_grid)

        # TODO take map size into account when calculating reward
        # TODO take distance to start into account when calculating reward
        ther_reward = 1  * (0.999 ** actual_time)
        if self.finished():
            reward = ther_reward
        elif not valid_movement:
            reward = -1
        else:
            reward = 0

        done = self.finished()

        print("actual time:", actual_time)
        print("Theoretical reward: {}".format(ther_reward))

        return state, reward, done, {}
    
    def reset(self):
        discovered_grid = self.reset_game(self.grid, self.initial_orientation)
        return grid_to_one_hot(discovered_grid)
    
    def render(self):
        self.print_grid()


def main():
    script_dir = os.path.dirname(__file__)
    rel_path = "3by3.json"
    abs_file_path = os.path.join(script_dir, rel_path)

    grid = json_loader.grid_from_json(abs_file_path)
    # Initialize the environment
    env = Maze_Environment(grid, 4, "up")
    env.reset()


    for _ in range(10):
        state, reward, done, _ = env.step(env.action_space.sample()) # take a random action
        env.render()
        if done:
            print("Finished")
            break
    
if __name__ == '__main__':
    main()

