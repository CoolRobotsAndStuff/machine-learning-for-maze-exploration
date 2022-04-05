import numpy as np
import os
import gym
from game import Maze_Game
import json_loader

from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

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
    return np.array(one_hot_grid, dtype=np.float32)

class Maze_Environment(Maze_Game, gym.Env):
    def __init__(self, grid: list, detection_distance: int, initial_orientation: str = "up"):
        super().__init__(grid, detection_distance, initial_orientation)
        self.grid = grid
        self.initial_orientation = initial_orientation

        # Action space
        self.action_space = gym.spaces.Discrete(4)
        # Observation space
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(len(self.entire_grid), len(self.entire_grid[0]), 17), dtype=np.float32)

        # Converts the output if the model to an action for the game
        self.action_to_str = {
            0: "up",
            1: "down",
            2: "left",
            3: "right"
        }
        self.done_1 = False

    def step(self, action):
        valid_movement, discovered_grid, actual_time = super().step(self.action_to_str[action])
        state = grid_to_one_hot(discovered_grid)

        # TODO take map size into account when calculating reward
        # TODO take distance to start into account when calculating reward
        ther_reward = 1  * (0.999 ** actual_time)
        if self.finished() and not self.done_1:
            reward = ther_reward
        elif not valid_movement:
            reward = -1
        else:
            reward = 0
        
        self.done_1 = self.finished()

        done = False #self.finished()

        #print("actual time:", actual_time)
        #print("Theoretical reward: {}".format(ther_reward))

        return state, reward, done, {}
    
    def reset(self):
        discovered_grid = self.reset_game(self.grid, self.initial_orientation)
        return grid_to_one_hot(discovered_grid)
    
    def render(self):
        self.print_grid()


def main():
    script_dir = os.path.dirname(__file__)
    rel_path = "test1.json"
    abs_file_path = os.path.join(script_dir, rel_path)

    grid = json_loader.grid_from_json(abs_file_path)
    # Initialize the environment
    env = Maze_Environment(grid, 4, "up")
    check_env(env)

    # Train
    model = PPO('MlpPolicy', env, n_steps=100000, verbose=1)

    
    model.learn(total_timesteps= 1000* 100000)

    model.save("my_model")

    obs = env.reset()
    for _ in range(1000):
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        print(obs, reward, done, info)
        if done:
            print("DID IT")
            break

    """
    for _ in range(10000):
        state, reward, done, _ = env.step(env.action_space.sample()) # take a random action
        env.render()
        if done:
            print("Explored the entire maze!")
            break
    """
    
if __name__ == '__main__':
    main()

