"""authenticate.py: Authentication utility functions for ETL & Deep & Machine Learning model 
training & inference.
"""
import numpy as np
import psutil
import ray
from google.oauth2.service_account import Credentials
import wandb
from mbta_ml.config import GCP_SERVICE_ACCOUNT_FILE, WANDB_API_KEY

def check_resources():
    """ Determine the total available computational resources.

    Returns
    -------
    Tuple[int, int, float]
        A tuple containing:
        - The total number of CPU cores available.
        - The total number of GPU cores available.
        - The total amount of memory available (in GB).
    """
    
    num_cpus = np.int32(psutil.cpu_count(logical=False))
    num_gpus = np.int32(len(ray.get_gpu_ids()))
    total_memory_gb = np.float32(psutil.virtual_memory().total / (1024**3))
    
    return num_cpus, num_gpus, total_memory_gb

def configure_ray_resources(num_cpus, num_gpus):
    """ Set the number of resources for Ray to the total available
    computational resources.

    Parameters
    ----------
    num_cpus : int
        The total number of CPU cores available.
    num_gpus : int
        The total number of GPU cores available.
    """
    
    # Initialize Ray with available resources
    ray.shutdown()
    ray.init(num_cpus=num_cpus, num_gpus=num_gpus)

from google.cloud import bigquery

def authenticate_with_gcp():
    """ Authenticate with Google Cloud Platform using a service account key.

    Returns
    -------
    google.cloud.bigquery.client.Client
        The BigQuery client for GCP.
    """
    credentials = Credentials.from_service_account_file(GCP_SERVICE_ACCOUNT_FILE)
    client = bigquery.Client(credentials=credentials)
    return client


def authenticate_with_wandb():
    """ Authenticate with Weights & Biases using an API key.

    Returns
    -------
    bool
        True if the login was successful, False otherwise.
    """
    return wandb.login(key=WANDB_API_KEY)

def run_authentication_tasks():
    """
    Run authentication utility tasks.
    """
    print("Checking computational resources:")
    num_cpus, num_gpus, total_memory_gb = check_resources()
    print(f"Total CPU cores available: {num_cpus}")
    print(f"Total GPU cores available: {num_gpus}")
    print(f"Total memory available (GB): {total_memory_gb}")

    print("\nAuthenticating with Google Cloud Platform...")
    gcp_credentials = authenticate_with_gcp()
    print("Google Cloud Platform authentication successful.")

    print("\nAuthenticating with Weights & Biases...")
    wandb_login_success = authenticate_with_wandb()
    if wandb_login_success:
        print("Weights & Biases authentication successful.")
    else:
        print("Weights & Biases authentication failed.")

if __name__ == "__main__":
    run_authentication_tasks()
