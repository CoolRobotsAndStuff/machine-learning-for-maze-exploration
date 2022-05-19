from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ["numpy", "gym", "tensorflow", "keras", "mlflow", "bresenham", "google-cloud-storage", "keras-rl2"]

setup(
  name='my-package',
  version='0.1',
  author = 'Chris Rawles',
  author_email = 'chris.rawles@some-domain.com',
  install_requires=REQUIRED_PACKAGES,
  packages=find_packages(),
  description='An example package for training on Cloud ML Engine.')