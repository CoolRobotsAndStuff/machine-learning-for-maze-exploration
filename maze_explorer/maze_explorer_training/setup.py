from setuptools import find_packages
from setuptools import setup
import glob

REQUIRED_PACKAGES = ["numpy", "gym", "tensorflow", "keras", "mlflow", "bresenham", "google-cloud-storage", "keras-rl2"]

setup(
    name='trainer',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    data_files=['trainer/experiment_config.json', "trainer/small_maps/"],
    description='My training application package.'
)