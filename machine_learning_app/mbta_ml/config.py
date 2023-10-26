"""config.py: Configuration module containing paths, hyperparameters, and other settings."""
import os
from pathlib import Path
from datetime import datetime

# Define the paths
BASE_DIR = Path(__file__).parent
MODEL_DIR = BASE_DIR / "models"
EXPERIMENT_DIR = BASE_DIR / "experiments" / datetime.now().strftime("%d_%m_%Y")
APP_DATA_DIR = BASE_DIR / "data" 
PROD_MODELS_DIR = BASE_DIR / "production_models" 

# Ensure the directories exist
MODEL_DIR.mkdir(parents=True, exist_ok=True)
APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)
PROD_MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Configuration for tuning trials
TUNING_NUM_TRIALS_CONFIG = {
    "xgboost": 10
}

# API Key for Weights and Biases (wandb)
WANDB_API_KEY = os.environ.get("WANDB_API_KEY")

# API key for service account file
GCP_SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
