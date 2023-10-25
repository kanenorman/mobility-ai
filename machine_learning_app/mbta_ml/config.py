"""config.py: Configuration module containing paths, hyperparameters, and other settings."""
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

# Configuration for tuning trials
TUNING_NUM_TRIALS_CONFIG = {
    "xgboost": 10
}

# API Key for Weights and Biases (wandb)
WANDB_API_KEY = os.environ.get("WANDB_API_KEY")
