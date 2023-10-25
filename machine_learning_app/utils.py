"""utils.py: Utility functions for ETL & Deep & Machine Learning model 
training & inference.
"""
import numpy as np
import psutil
import ray

def check_resources():
    """Determines the total available computational resources.
    
    Returns:
        num_cpus (int): The total number of CPU cores available.
        num_gpus (int): The total number of GPU cores available.
        total_memory_gb (float): The total amount of memory available (in GB).
    """
    
    num_cpus = np.int32(psutil.cpu_count(logical=False))
    num_gpus = np.int32(len(ray.get_gpu_ids()))
    total_memory_gb = np.float32(psutil.virtual_memory().total / (1024**3))
    
    return num_cpus, num_gpus, total_memory_gb

def configure_ray_resources(num_cpus, num_gpus):
    """Sets the number of resources for Ray to the total available
    computational resources.
    
    Args:
        num_cpus (int): The total number of CPU cores available.
        num_gpus (int): The total number of GPU cores available.
    """
    
    # Initialize Ray with available resources
    ray.shutdown()
    ray.init(num_cpus=num_cpus, num_gpus=num_gpus)