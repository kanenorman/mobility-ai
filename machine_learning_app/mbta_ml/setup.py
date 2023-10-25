"""setup.py: For software development in a local environment
version of software reflects Milestone number.
"""
from setuptools import setup, find_packages

# Read in the requirements.txt
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name='mbta_ml',
    version='4',  # Milestone 4
    packages=find_packages(),
    install_requires=requirements,  # install from requirements.txt
)
