"""config.py: This module contains functions to distill the knowledge obtained
by a teacher into a student model.
"""
import os
from pathlib import Path
from datetime import datetime

# Define the paths
BASE_DIR = Path(os.getcwd())  # Gets the current working directory
MODEL_DIR = BASE_DIR / "models"
EXPERIMENT_DIR = BASE_DIR / "experiments" / datetime.now().strftime("%d_%m_%Y")

# Ensure the directories exist
MODEL_DIR.mkdir(parents=True, exist_ok=True)
EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)

NUM_TRIALS = 10
WANDB_API_KEY = os.environ["WANDB_API_KEY"]
