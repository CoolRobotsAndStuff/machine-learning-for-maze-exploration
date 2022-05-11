import os
import time

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from tensorflow.keras.optimizers import Adam
from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

from map_manager import load_map
from environment import Maze_Environment

import mlflow
from mlflow.tracking import MlflowClient

from google.cloud import storage


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'composed-arch-348513-69f529adb730.json'


client = storage.Client()


from pathlib import Path

srcipt_dir = os.path.dirname(os.path.realpath(__file__))

ip_file_dir = os.path.join(srcipt_dir, 'tracking_uri_IP.txt')
with open(ip_file_dir, "r") as f:
    tracking_uri = f.read()
    print("MLflow tracking server uri set to:", tracking_uri)
    mlflow.set_tracking_uri(tracking_uri)

# Create an experiment with a name that is unique and case sensitive.
client = MlflowClient()
experiment_id = client.create_experiment("Artifact Storage Test", artifact_location="gs://machine_learning_for_maze_exploration_models")
client.set_experiment_tag(experiment_id, "test", "q-learning")

with mlflow.start_run(experiment_id=experiment_id):
    

    maps_dir = os.path.join(srcipt_dir, 'test_maps')

    env = Maze_Environment(maps_dir, "up", 50)

    nb_actions = env.action_space.n

    dense_layers = [{"size":16, "activation":"relu"}, {"size":nb_actions, "activation":"linear"}]

    model = Sequential()
    model.add(Flatten(input_shape=(1,) + env.observation_space.shape))

    for layer in dense_layers:
        model.add(Dense(layer["size"]))
        model.add(Activation(layer["activation"]))

    mlflow.log_param("layers", dense_layers)

    """
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))
    """
    print(model.summary())

    

    policy = EpsGreedyQPolicy()
    mlflow.log_param("policy", "EpsGreedyQPolicy")
    
    limit = 50000
    window_length = 1
    memory = SequentialMemory(limit=limit, window_length=window_length)
    mlflow.log_params({
        "memory": "SequentialMemory", 
        "memory_limit":limit, 
        "memory_window_lenght":window_length
        })


    warmup_steps = 10
    mlflow.log_param("warmup_steps", warmup_steps)

    target_model_update = 1e-2
    mlflow.log_param("target_model_update", target_model_update)

    dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=warmup_steps,
    target_model_update=target_model_update, policy=policy)

    mlflow.log_param("agent", "DQNAgent")
    
    lr = 1e-3
    mlflow.log_param("learning_rate", lr)
    metrics = ['mae']
    mlflow.log_param("metrics", metrics)
    dqn.compile(Adam(lr=lr), metrics=metrics)

    # Okay, now it's time to learn something! We visualize the training here for show, but this slows down training quite a lot. 
    history = dqn.fit(env, nb_steps=1000, visualize=False, verbose=2)

    weight_path = Path('saved_agents')
    weight_path.mkdir(parents=True, exist_ok=True)
    
    model_json = dqn.model.to_json()
    with open(os.path.join(weight_path, "dqn_keras-RL2-model.json"), "w") as json_file:
        json_file.write(model_json)
    mlflow.log_artifact(os.path.join(weight_path, "dqn_keras-RL2-model.json"))
    
    dqn.save_weights(str(weight_path / 'dqn_keras-RL2-weights.hdf5'), overwrite=True)
    mlflow.log_artifact(str(weight_path / 'dqn_keras-RL2-weights.hdf5'))

    mlflow.end_run()
#dqn.test(env, nb_episodes=5, visualize=True)