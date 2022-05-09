import numpy as np
import os
import gym
from game import Maze_Game
import json_loader
from map_manager import load_map
import mlflow

one_hot_node_type_encoder = {
    "undefined": np.array([0, 0, 0]),
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
    arr = np.concatenate((one_hot_node_type_encoder[node.node_type], one_hot_status_encoder[node.status], one_hot_tile_type_encoder[node.tile_type]))
    arr1 = np.array([int(node.is_robots_position), int(node.explored)])
    arr = np.concatenate((arr, arr1))
    return arr

# Encodes the entire grid and returns it as a numpy array
def grid_to_one_hot(grid):
    one_hot_grid = list()
    for row in grid:
        one_hot_row = list()
        for node in row:
            one_hot_row.append(get_one_hot_form_node(node))
        one_hot_grid.append(one_hot_row)
    return np.array(one_hot_grid, dtype=bool)

class Maze_Environment(Maze_Game, gym.Env):
    def __init__(self, maps_dir:str, initial_orientation: str = "up", max_step_n: int = 1000):
        self.max_step_n = max_step_n
        self.maps_dir = maps_dir
        self.map_count = len(os.listdir(maps_dir))
        self.current_map_number = 0
        self.current_step_n = 0
        self.reward_factor = 10

        self.cummulative_reward = 0
        
        self.grid, map_data = self.get_current_map()
        self.final_reward = map_data["accesible_vortex_n"] * self.reward_factor
        super().__init__(self.grid, map_data["start_node"], initial_orientation)

        self.initial_orientation = initial_orientation

        # Action space
        self.action_space = gym.spaces.Discrete(4)
        # Observation space
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(len(self.entire_grid), len(self.entire_grid[0]), 17), dtype=bool)

        # Converts the output if the model to an action for the game
        self.action_to_str = {
            0: "up",
            1: "down",
            2: "left",
            3: "right"
        }

    def get_current_map(self):
        return load_map(os.path.join(self.maps_dir, "map_" + str(self.current_map_number) + ".map"))

    def step(self, action):
        self.current_step_n += 1
        valid_movement, discovered_grid, actual_time, time_taken = super().step(self.action_to_str[action])
        state = grid_to_one_hot(discovered_grid)
        # TODO take distance to start into account when calculating reward
        
        if self.finished():
            reward = self.final_reward
        elif not valid_movement:
            reward = -10
        else:
            reward = -1
        
        self.cummulative_reward += reward

        done = self.finished() or self.current_step_n >= self.max_step_n

        return state, reward, done, {}
    
    def reset(self):
        self.current_step_n = 0
        self.cummulative_reward = 0

        if self.current_map_number >= self.map_count:
            self.current_map_number = 0
        self.current_map_number += 1
        self.grid, map_data = self.get_current_map()
        self.final_reward = map_data["accesible_vortex_n"] * self.reward_factor
        discovered_grid = self.reset_game(self.grid, map_data["start_node"], self.initial_orientation)

        return grid_to_one_hot(discovered_grid)
    
    def clear(self):
        if os.name == "nt":
            _ = os.system('cls')
        else:
            _ = os.system('clear')

    def render(self, mode='human'):
        self.clear()
        self.print_grid()



def main():
    script_dir = os.path.dirname(__file__)
    maps_dir = os.path.join(script_dir, "test_maps")
    # Initialize the environment
    env = Maze_Environment(maps_dir, "up")

    
    for _ in range(10000):
        state, reward, done, _ = env.step(env.action_space.sample()) # take a random action
        env.render()
        if done:
            print("Explored the entire maze or reached the maximum number of steps")
            break
    
    
if __name__ == '__main__':
    main()

