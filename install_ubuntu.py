import subprocess
from pathlib import Path

path = Path(".")
parent_dir = path.parent.absolute().parent.absolute()

subprocess.run(["apt-get", "update"])

subprocess.run(["apt-get", "install", "python3-pip", "-y"])

subprocess.run(["apt-get", "install", "git", "-y"])

subprocess.run(["pip", "install", "numpy", "gym", "tensorflow", "keras", "mlflow", "bresenham", "google-cloud-storage"])

subprocess.run(["git", "clone", "https://github.com/CoolRobotsAndStuff/keras-rl2-mlflow.git"], cwd=parent_dir)

subprocess.run(["pip", "install", "."], cwd=parent_dir / "keras-rl2-mlflow")





