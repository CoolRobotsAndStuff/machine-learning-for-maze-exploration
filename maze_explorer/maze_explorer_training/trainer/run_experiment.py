import os
import sys
import time
import json
from pathlib import Path
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Convolution2D, Permute
from tensorflow.keras.optimizers import Adam


from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy, SoftmaxPolicy, GreedyQPolicy, BoltzmannQPolicy, MaxBoltzmannQPolicy, BoltzmannGumbelQPolicy
from rl.memory import SequentialMemory

from trainer.environment import Maze_Environment

import mlflow
from mlflow.tracking import MlflowClient

from trainer.mlflow_logger import MlflowLogger

from trainer.logger import MultiLogger

from google.cloud import storage


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

# Path to save all artifacts
ARTIFACT_PATH = SCRIPT_DIR / Path('artifacts_files')
ARTIFACT_PATH.mkdir(parents=True, exist_ok=True)

POLICIES = {
    "LinearAnnealedPolicy": LinearAnnealedPolicy, 
    "EpsGreedyQPolicy": EpsGreedyQPolicy, 
    "SoftmaxPolicy": SoftmaxPolicy, 
    "GreedyQPolicy": GreedyQPolicy, 
    "BoltzmannQPolicy": BoltzmannQPolicy,
    "MaxBoltzmannQPolicy": MaxBoltzmannQPolicy,
    "BoltzmannGumbelQPolicy": BoltzmannGumbelQPolicy
    }

def load_config():
    config_file = os.path.join(SCRIPT_DIR, "experiment_config.json")
    with open(config_file) as f:
        config = json.load(f)
    print(config)
    return config

def get_experiment(client, config):
    try:
        experiment_id = client.create_experiment(config["name"], artifact_location=config["artifact_bucket_URI"])
    except:
        experiment = client.get_experiment_by_name(config["name"])
        experiment_id = experiment.experiment_id

    for key, value in config["tags"].items():
        client.set_experiment_tag(experiment_id, key, value)

    return experiment_id

def log_run_params(run):
    # Log all the parameters from config file
    for key, value in run.items():
        if key == "conv_layers":
            for index, conv_layer in enumerate(value):
                for key1, value1 in conv_layer.items():
                    mlflow.log_param("conv_" + str(index) + "_" +key1, value1)
        elif key == "dense_layers":
            for index, conv_layer in enumerate(value):
                for key1, value1 in conv_layer.items():
                    mlflow.log_param("dense_" + str(index) + "_" +key1, value1)
        else:
            mlflow.log_param(key, value)
            
def build_model(run, env):
    # Define model
    model = Sequential()
    nb_actions = env.action_space.n

    # Define the shape of the input (starts with 1 beacuse of the batch size)
    input_shape = np.array([1,] + list(env.observation_space.shape))

    # Create convolutional layers
    #for conv_layer in run["conv_layers"]:
    #    model.add(Convolution2D(input_shape=input_shape ,filters=conv_layer["filter_n"], kernel_size=conv_layer["size"], strides=conv_layer["strides"], activation=conv_layer["activation"]))

    # Flatten the output
    model.add(Flatten(input_shape=input_shape))

    # Create dense layers
    for dense_layer in run["dense_layers"]:
        model.add(Dense(dense_layer["units"], activation=dense_layer["activation"]))
    
    # Last layer: no. of neurons corresponds to action space
    # Linear activation
    model.add(Dense(nb_actions, activation='linear'))  
    
    print(model.summary())
    return model

def build_agent(run, env, model):
    # Define the policy
    policy = POLICIES[run["policy"]]()

    # Define the memory
    memory = SequentialMemory(limit=run["memory_limit"], window_length=run["memory_window_lenght"])
    #
    # Define the agent
    warmup_steps = run["warmup_steps"]
    target_model_update = run["target_model_update"]
    dqn = DQNAgent(model=model, nb_actions=env.action_space.n, memory=memory, nb_steps_warmup=warmup_steps,
    target_model_update=target_model_update, policy=policy)
    
    # Compile the agent
    lr = run["learning_rate"]
    metrics = ['mae']
    dqn.compile(Adam(lr=lr), metrics=metrics)

    return dqn

def save_agent(dqn):
    # Save and log model
    print("Saving model...")
    model_json = dqn.model.to_json()
    with open(os.path.join(ARTIFACT_PATH, "dqn_keras-RL2-model.json"), "w") as json_file:
        json_file.write(model_json)
    mlflow.log_artifact(os.path.join(ARTIFACT_PATH, "dqn_keras-RL2-model.json"))

    # Save and log weights
    print("Saving weights...")
    dqn.save_weights(str(ARTIFACT_PATH / 'dqn_keras-RL2-weights.hdf5'), overwrite=True)
    mlflow.log_artifact(str(ARTIFACT_PATH / 'dqn_keras-RL2-weights.hdf5'))

# Logging
# File to keep the terminal output
logs_path = str(ARTIFACT_PATH / 'logs.txt')
with open(logs_path, 'w'):
    pass

sys.stdout = MultiLogger((sys.__stdout__,), (logs_path,))
sys.stderr = MultiLogger((sys.__stderr__,), (logs_path,))


#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SCRIPT_DIR + '/composed-arch-348513-69f529adb730.json'
gclient = storage.Client()


config = load_config()

print("MLflow tracking server uri set to:", config["server_URI"])
mlflow.set_tracking_uri(config["server_URI"])
client = MlflowClient()

experiment_id = get_experiment(client, config)

for i, run in enumerate(config["runs"]):

    print("Starting run:", i, "with experiment_id:", experiment_id)
    mlflow.start_run(experiment_id=experiment_id)

    # Start terminal logging to mlflow
    sys.stdout.do_ml_flow_logging = False
    sys.stderr.do_ml_flow_logging = True

    # Log run parameters
    log_run_params(run)

    # Create environment
    env = Maze_Environment(gcloud_client=gclient, map_bucket=config["map_bucket_URI"], max_step_n=run["max_steps_in_episode"])

    # Create model
    model = build_model(run, env)

    # Create agent
    dqn = build_agent(run, env, model)
    
    # Train the agent
    history = dqn.fit(env, nb_steps=run["total_steps"], visualize=False, verbose=2, callbacks=[MlflowLogger()])

    # Save the model and weights
    save_agent(dqn)

    # Save the log of the temrminal output
    mlflow.log_artifact(str(ARTIFACT_PATH / 'logs.txt'))

    # Stop terminal logging to mlflow
    sys.stderr.do_ml_flow_logging = False

    # End the run
    mlflow.end_run()

    

