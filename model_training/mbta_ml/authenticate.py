"""authenticate.py: Authentication utility functions for ETL & Deep & Machine Learning model
training & inference.
"""
import argparse

import numpy as np
import psutil
import ray
import wandb
from google.cloud import bigquery, storage
from google.oauth2.service_account import Credentials
from mbta_ml.config import GCP_SERVICE_ACCOUNT_FILE, WANDB_API_KEY


def authenticate_gcp_storage_implicit(project_id="ac215-transit-prediction"):
    """Authenticate with Google Cloud Storage using Application Default Credentials (ADC).

    This method leverages implicit authentication provided by the `gcloud` CLI.
    It's primarily useful for GCS operations like listing buckets or uploading/downloading files.

    Note:
    Before using this method, set up ADC as described in:
    https://cloud.google.com/docs/authentication/external/set-up-adc

    Ensure the authenticated account has "storage.buckets.list" permission for listing buckets.

    Parameters
    ----------
    project_id : str, optional
        Google Cloud Project ID. If not provided, the default from ADC is used.

    Returns
    -------
    google.cloud.storage.client.Client
        Authenticated client for Google Cloud Storage.
    """
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()

    print("GCS Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")
    return storage_client


def authenticate_gcp_bigquery_implicit(project_id="ac215-transit-prediction"):
    """Authenticate with Google BigQuery using Application Default Credentials (ADC).

    This method leverages implicit authentication provided by the `gcloud` CLI.
    It's primarily useful for BigQuery operations like running SQL queries and accessing datasets.

    Note:
    Before using this method, set up ADC as described in:
    https://cloud.google.com/docs/authentication/external/set-up-adc

    Ensure the authenticated account has appropriate BigQuery permissions for the desired operations.

    Parameters
    ----------
    project_id : str, optional
        Google Cloud Project ID where the BigQuery dataset resides. If not provided,
        the default from ADC is used.

    Returns
    -------
    google.cloud.bigquery.client.Client
        Authenticated client for Google BigQuery.
    """
    bigquery_client = bigquery.Client(project=project_id)
    print("Authenticated with BigQuery.")
    return bigquery_client


def authenticate_gcp_bigquery_explicit(project_id=None):
    """Authenticate with Google Cloud Platform's BigQuery service using a service account key with
    explicit authentication & local environment variables.

    This method uses explicit service account credentials.
    It's useful when running in environments without the `gcloud` CLI or ADC setup.

    Parameters
    ----------
    project_id : str, optional
        Google Cloud Project ID where the BigQuery dataset resides. If not provided,
        the default project from the service account credentials is used.

    Returns
    -------
    google.cloud.bigquery.client.Client
        Authenticated client for Google BigQuery.
    """
    credentials = Credentials.from_service_account_file(GCP_SERVICE_ACCOUNT_FILE)
    bigquery_client = bigquery.Client(credentials=credentials, project=project_id)
    print("Authenticated with BigQuery using explicit credentials.")
    return bigquery_client


def authenticate_with_wandb():
    """Authenticate with Weights & Biases using an API key.

    Returns
    -------
    bool
        True if the login was successful, False otherwise.
    """
    return wandb.login(key=WANDB_API_KEY)


def check_resources():
    """Determine the total available computational resources.

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
    """Set the number of resources for Ray to the total available
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
    gcp_client = authenticate_gcp_storage_implicit()
    print("Google Cloud Platform authentication successful.")
    print(f"GCP client: {gcp_client}")
    print(f"GCP client type: {type(gcp_client)}")

    print("\nAuthenticating with Weights & Biases...")
    wandb_login_success = authenticate_with_wandb()
    if wandb_login_success:
        print("Weights & Biases authentication successful.")
    else:
        print("Weights & Biases authentication failed.")


def main():
    parser = argparse.ArgumentParser(
        description="Authentication Utility with Optional Ray Configuration"
    )
    parser.add_argument(
        "--ray", "-r", action="store_true", help="Run configure_ray_resources"
    )

    args = parser.parse_args()

    run_authentication_tasks()

    if args.ray:
        num_cpus, num_gpus, total_memory_gb = check_resources()
        configure_ray_resources(num_cpus, num_gpus)


if __name__ == "__main__":
    main()
