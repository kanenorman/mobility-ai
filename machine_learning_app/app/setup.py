"""setup.py: For software development in a local environment
version of software reflects Milestone number.
"""
from setuptools import setup, find_packages

setup(
    name='mbta_machine_learning',
    version='4', # Milestone 4
    packages=find_packages(),
)
