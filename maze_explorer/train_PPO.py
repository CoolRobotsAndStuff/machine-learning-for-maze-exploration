from environment import Maze_Environment
import json_loader
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
import os

def main():
    script_dir = os.path.dirname(__file__)
    rel_path = "3by3.json"
    abs_file_path = os.path.join(script_dir, rel_path)

    grid = json_loader.grid_from_json(abs_file_path)
    # Initialize the environment
    env = Maze_Environment(grid, 4, "up")
    check_env(env)

    # Train
    model = PPO('MlpPolicy', env, n_steps=1000, verbose=1)

    
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