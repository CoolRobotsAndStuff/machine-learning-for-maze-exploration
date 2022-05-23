from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ["numpy", "gym", "tensorflow", "keras", "mlflow", "bresenham", "google-cloud-storage", "keras-rl2"]

setup(
    name='maze_explorer_training',
    version='0.1',
    author = 'IITA',
    author_email = 'aledeum.saf@gmail.com',
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES,
    description='An example package for training on Cloud ML Engine.')