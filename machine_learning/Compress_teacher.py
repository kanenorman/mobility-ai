"""
Compress_teacher.py: This module contains functions prune and fine tune the best
fitting base model to improve its performance and decrease model size
"""

import psutil
import ray

# Import necessary packages
import tensorflow_model_optimization
import tensorflow_model_optimization as tfmot
from tensorflow_model_optimization.python.core.sparsity.keras import pruning_schedule


## Check and configure available computational resources ##
# Define function to determine computational resources
def check_resources():
    """
    Determines the total available computational resources.

    Returns:
        num_cpus (int): The total number of CPU cores available.
        num_gpus (int): The total number of GPU cores available.
        total_memory_gb (float): The total amount of memory available (in GB).
    """
    # Determine available CPU cores
    num_cpus = psutil.cpu_count(logical=False)

    # Determine available GPUs
    num_gpus = len(ray.get_gpu_ids())

    # Determine total system memory
    total_memory_gb = psutil.virtual_memory().total / (1024**3)  # in GB

    return num_cpus, num_gpus, total_memory_gb


# Define funciton to allocate computational resource
def configure_ray_resources(num_cpus, num_gpus):
    """
    Sets the number of resources for Ray to the total available computational resources.

    Args:
        num_cpus (int): The total number of CPU cores available.
        num_gpus (int): The total number of GPU cores available.
    """
    # Initialize Ray with available resources
    ray.shutdown()
    ray.init(num_cpus=num_cpus, num_gpus=num_gpus)


# Determine computational resources
num_cpus, num_gpus, total_memory_gb = check_resources()
# Configure Ray to use all available resources
configure_ray_resources(num_cpus, num_gpus)


## Prune (Weight/Neuron level) and finetune ##
# Define function to prune and fine tune
def prune_and_fine_tune(
    best_model, data, config, pruning_params, is_neuron_pruning=False
):
    """
    Prunes and finetunes whatever model is provided, but expected use is
    for best fitting model

    Parameters:
    - best_model: Keras model object (DNN)
    - data: Dataframe
    - Model save path: File path to save model.
    - config (dict): Configuration for DNN tuning with best fitting parameters.
    - pruning_params: Dictionary containing specifications for pruning
    - is_neuron_pruning: flag which determines behavior (neuron or weight level pruning)

    Returns:
    1) Pruned Model + Reports the training results using Ray's train.report
    """
    # Initialize WandB for pruning and fine-tuning run
    wandb.init(project="mbtadnn_pruning_fine_tuning")

    # Set up Ray tracking for pruning and fine-tuning run
    ray.shutdown()
    ray.init()

    # Createcopy of the original model
    pruned_model = tf.keras.models.clone_model(best_model)

    # Define model save path for the pruned model based on flag value
    if is_neuron_pruning:
        pruning_method = "neuron"
        pruned_model_save_path = MODEL_DIR / f"pruned_neuron_model.h5"
    else:
        pruning_method = "weight"
        pruned_model_save_path = MODEL_DIR / f"pruned_weight_model.h5"

    # Define sparsity schedule based on the pruning method specified by flag
    if is_neuron_pruning:
        target_sparsity_neuron = pruning_params["target_sparsity_neuron"]
        begin_step = pruning_params["begin_step"]
        end_step = pruning_params["end_step"]
        prune_frequency = pruning_params["prune_frequency"]
        pruning_schedule = tfmot.sparsity.keras.ConstantSparsity(
            target_sparsity=target_sparsity_neuron,
            begin_step=begin_step,
            end_step=end_step,
            frequency=prune_frequency,
        )
    else:
        target_sparsity_weight = pruning_params["target_sparsity_weight"]
        begin_step = pruning_params["begin_step"]
        end_step = pruning_params["end_step"]
        pruning_schedule = tfmot.sparsity.keras.PolynomialDecay(
            initial_sparsity=0.0,
            final_sparsity=target_sparsity_weight,
            begin_step=begin_step,
            end_step=end_step,
        )

    # Apply appropriate pruning method based on pruning flag value
    if is_neuron_pruning:
        pruned_model = tfmot.sparsity.keras.prune_low_magnitude(
            pruned_model, pruning_schedule=pruning_schedule
        )
    else:
        pruned_model = tfmot.sparsity.keras.prune_low_magnitude(
            pruned_model, pruning_schedule=pruning_schedule
        )

    # Compile pruned model
    pruned_model.compile(
        loss="mean_squared_error",
        optimizer=tf.keras.optimizers.AdamW(learning_rate=config["learning_rate"]),
        metrics=[
            tf.keras.metrics.MeanAbsoluteError(),
            tf.keras.metrics.RootMeanSquaredError(),
        ],
    )

    # Split the data into train and test sets
    train_df, test_df = train_test_split(data, test_size=0.3)
    # Train data
    train_x = train_df.drop("predictor_delay_seconds", axis=1)
    train_y = train_df["predictor_delay_seconds"]
    # Test data
    test_x = test_df.drop("predictor_delay_seconds", axis=1)
    test_y = test_df["predictor_delay_seconds"]

    # Define callback to update pruning during training (was having issues without this)
    pruning_callback = tfmot.sparsity.keras.UpdatePruningStep()

    # Fine-tune pruned model with pruning callback
    fine_tuning_history = pruned_model.fit(
        train_x,
        train_y,
        epochs=config["epochs"],
        batch_size=config["batch_size"],
        validation_data=(test_x, test_y),
        verbose=2,
        callbacks=[
            DNN_early_10,
            DNN_plateau_lr,
            DNN_BestFit,
            pruning_callback,
        ],  # pruning_callback (necessary)
    )

    # Save pruned model
    pruned_model.save(pruned_model_save_path)
    print(
        f"Pruned model saved to: {pruned_model_save_path}"
    )  # Report save location for reference

    # Evaluate pruned model performance on the test set
    y_pred = pruned_model.predict(test_x)  # Make predictions
    mae = mean_absolute_error(test_y, y_pred)  # Evaluate predictions
    rmse = mean_squared_error(test_y, y_pred, squared=False)  # Evaluate predictions
    r2 = r2_score(test_y, y_pred)  # Evaluate predictions

    # Report metrics to Ray and WandB
    ray.train.report({"rmse": rmse, "mae": mae, "r2": r2})
    wandb.log({"rmse": rmse, "mae": mae, "r2": r2})

    # Shut down WandB
    wandb.finish()

    # Shut down Ray
    ray.shutdown()

    # Return the pruned and fine-tuned model
    return pruned_model


# Define pruning_params for weight pruning
weight_pruning_params = {
    "target_sparsity_weight": 0.50,
    "begin_step": 0,
    "end_step": 100,
}
# Define pruning_params for neuron pruning
neuron_pruning_params = {
    "target_sparsity_neuron": 0.50,
    "begin_step": 0,
    "end_step": 100,
    "prune_frequency": 1,
}

# Create copy of the best model for each type of pruning (was having issues without this)
best_trained_dnn_model_copy = tf.keras.models.clone_model(best_trained_dnn_model)

# Perform weight pruning
pruned_weight_model = prune_and_fine_tune(
    best_trained_dnn_model_copy,
    mbta_final_df,
    best_hyperparameters,
    weight_pruning_params,
    is_neuron_pruning=False,
)

# Create another copy of the best model for neuron pruning (best to keep separate)
best_trained_dnn_model_copy = tf.keras.models.clone_model(best_trained_dnn_model)

# Perform neuron pruning
pruned_neuron_model = prune_and_fine_tune(
    best_trained_dnn_model_copy,
    mbta_final_df,
    best_hyperparameters,
    neuron_pruning_params,
    is_neuron_pruning=True,
)

## Evaluate performance and choose best fitting pruned model ##
# Split the data into train and validation sets
train_df, validation_df = train_test_split(mbta_final_df, test_size=0.2)
validation_x = validation_df.drop("predictor_delay_seconds", axis=1)
validation_y = validation_df["predictor_delay_seconds"]

# Evaluate the performance of the weight pruned model on the validation data
rmse_weight = mean_squared_error(validation_y, y_pred_weight, squared=False)

# Evaluate the performance of the neuron pruned model on the validation data
rmse_neuron = mean_squared_error(validation_y, y_pred_neuron, squared=False)

# Choose the best pruned model for distillation based on the metric of your choice
if rmse_weight < rmse_neuron:
    best_pruned_model = pruned_weight_model
else:
    best_pruned_model = pruned_neuron_model
