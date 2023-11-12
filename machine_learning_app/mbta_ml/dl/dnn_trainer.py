"""
DNN_train_base.py: This module contains functions to train, build, and save DNN models.
It also incorporates functionality to evaluate model performance using various metrics.
"""

# Import necessary packages
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import psutil
import ray
import ray.tune as tune
import tensorflow as tf
import tensorflow_addons as tfa
import wandb
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from tensorflow_addons.optimizers import AdamW

os.environ["WANDB_API_KEY"] = "610d13d9a43fffd83600c4d4e90ccaba1646acbd"


## Prepare environment to train base model ##
# Check and configure available computational resources
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

# Define file paths and directories
BASE_DIR = Path(os.getcwd())
MODEL_DIR = BASE_DIR / "models"
EXPERIMENT_DIR = BASE_DIR / "experiments" / datetime.now().strftime("%d_%m_%Y")

# Ensure directories exist
MODEL_DIR.mkdir(parents=True, exist_ok=True)
EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)

# Load WandB
wandb.login(relogin=False)

# Extract data from GCP bucket
raw_df = extract_from_gcp(verbose=False, close_connection=True)
raw_df = preprocess_data(raw_df, verbose=False)
transformed_df, le_dict = transform(raw_df)
mbta_final_df = data_checks_and_cleaning(transformed_df, verbose=False)

# Establish constants
global mbta_final_df
optimizer = AdamW(learning_rate=0.001, weight_decay=1e-4)
NUM_TRIALS = 10

# Define Model Training Callbacks
DNN_early_10 = EarlyStopping(monitor="val_loss", patience=10, mode="min")
DNN_plateau_lr = ReduceLROnPlateau(
    monitor="val_loss", factor=0.8, patience=6, verbose=1, mode="min", min_lr=0.0001
)
DNN_BestFit = ModelCheckpoint(
    filepath="DNN_best_fit.h5",
    save_best_only=True,
    save_weights_only=False,
    monitor="val_loss",
    mode="min",
)


# Define function to create a simple DNN model
def create_dnn_model(input_dim, dropout_rate):
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(128, activation="relu", input_shape=(input_dim,)),
            tf.keras.layers.BatchNormalization(),  # Batch normalization to facilitate backpropogation
            tf.keras.layers.Dropout(
                dropout_rate
            ),  # Dropout_rate to improve generalization through regularization
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.BatchNormalization(),  # Batch normalization to facilitate backpropogation
            tf.keras.layers.Dropout(
                dropout_rate
            ),  # Dropout_rate to improve generalization through regularization
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.BatchNormalization(),  # Batch normalization to facilitate backpropogation
            tf.keras.layers.Dropout(
                dropout_rate
            ),  # Dropout_rate to improve generalization through regularization
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.BatchNormalization(),  # Batch normalization to facilitate backpropogation
            tf.keras.layers.Dropout(
                dropout_rate
            ),  # Dropout_rate to improve generalization through regularization
            tf.keras.layers.Dense(1),  # Regression (linear) layer
        ]
    )
    return model


# Initialize Ray for parameter tuning
ray.shutdown()
ray.init(num_cpus=num_cpus, num_gpus=num_gpus)

# Configure hyperparameter search space for Ray
param_space = {
    "hidden_layers": [64, 32, 16],
    "learning_rate": tune.loguniform(1e-4, 1e-2),
    "batch_size": tune.choice([32, 64, 128]),
    "epochs": tune.choice([30, 50, 70]),
    "activation": "relu",
    "output_activation": "linear",
    "loss": "mean_squared_error",
    "dropout_rate": tune.uniform(0.0, 0.5),
    "early_stopping_patience": tune.choice([5, 10, 15]),
}


# Define function to train the DNN
def train_dnn(data, model_save_path, config):
    """
    Specifies training parameters for DNN model with MBTA data.

    Parameters:
    - data: Dataframe
    - Model save path: File path to save model.
    - config (dict): Configuration for DNN tuning.

    Returns:
    1) Model
    2) Reports the training results using Ray's train.report instead.
    """
    # Extract hyperparameters from configuration dictionary
    hidden_layers = config["hidden_layers"]
    learning_rate = config["learning_rate"]
    batch_size = config["batch_size"]
    epochs = config["epochs"]
    activation = config["activation"]
    output_activation = config["output_activation"]
    loss = config["loss"]
    dropout_rate = config["dropout_rate"]
    early_stopping_patience = config["early_stopping_patience"]

    # Set AdamW optimizer with the specified learning rate
    optimizer = tf.keras.optimizers.AdamW(
        learning_rate=learning_rate, weight_decay=1e-4
    )

    # Split data into train and test sets
    train_df, test_df = train_test_split(data, test_size=0.3)
    # Train data
    train_x = train_df.drop("predictor_delay_seconds", axis=1)
    train_y = train_df["predictor_delay_seconds"]
    # Test data
    test_x = test_df.drop("predictor_delay_seconds", axis=1)
    test_y = test_df["predictor_delay_seconds"]

    # Create and compile DNN model
    input_dim = train_x.shape[1]
    dnn_model = create_dnn_model(input_dim, dropout_rate)
    dnn_model.compile(
        loss="mean_squared_error",
        optimizer=optimizer,
        metrics=[
            tf.keras.metrics.MeanAbsoluteError(),
            tf.keras.metrics.RootMeanSquaredError(),
        ],
    )

    # Train DNN model (+ save fit history)
    history = dnn_model.fit(
        train_x,
        train_y,
        epochs=config["epochs"],
        batch_size=config["batch_size"],
        validation_data=(test_x, test_y),
        verbose=2,
        callbacks=[DNN_early_10, DNN_plateau_lr, DNN_BestFit],
    )

    # Save DNN model
    dnn_model.save(model_save_path)
    print(
        f"Model saved to: {model_save_path}"
    )  # Report where it is saved for reference

    # Evaluate DNN model on test set
    y_pred = dnn_model.predict(test_x)  # Make predictions
    mae = mean_absolute_error(test_y, y_pred)  # Evaluate performance
    rmse = mean_squared_error(test_y, y_pred, squared=False)  # Evaluate performance
    r2 = r2_score(test_y, y_pred)  # Evaluate performance

    # Report metrics to Ray and W&B
    train.report({"rmse": rmse, "mae": mae, "r2": r2})
    wandb.log({"rmse": rmse, "mae": mae, "r2": r2, "config": config})

    return dnn_model


# Define function for hyperparameter tuning
def trainable(config):
    """
    Trains DNN model on MBTA data.

    Parameters:
    - config (dict): Configuration for DNN tuning.

    Returns:
    None.
    """
    # Initialize W&B for each model configuration
    wandb.init(project="mbtadnn")
    run_id = str(wandb.run.id)  # Convert wandb.run.id to a string
    model_save_path = str(MODEL_DIR / f"dnn_model_{run_id}.h5")
    print(f"Model will be saved in: {model_save_path}")

    # Train DNN model
    dnn_model = train_dnn(mbta_final_df, model_save_path, config)


# Start hyperparameter tuning experiment
analysis = tune.run(
    trainable,
    config=param_space,
    num_samples=NUM_TRIALS,
    name="dnn_tuning",
    stop={
        "training_iteration": 5
    },  # Change 1 to the number of desired training iterations
    local_dir=str(EXPERIMENT_DIR),  # Specify the directory to store results
    verbose=1,  # Increase the verbosity for logging
    metric="rmse",  # Specify the metric you want to optimize (e.g., "rmse")
    mode="min",  # Specify the mode, which can be "min" or "max" depending on the optimization goal
)

# Report best hyperparameters and metrics
print("Best hyperparameters:", analysis.best_config)
print("Best RMSE:", analysis.best_result["rmse"])

# Close W&B after logging completes
wandb.finish()

# Define the best hyperparameters
best_hyperparameters = analysis.best_config


## Train DNN with best fitting hyperparameters ##
def train_best_dnn(data, model_save_path, best_hyperparameters):
    """
    Train a DNN model on MBTA data using the best hyperparameters found during tuning.

    Parameters:
    - data: dataframe
    - Model save path: file path to where the model will be saved
    - best_hyperparameters: dict with best hyperparameters from tuning.

    Returns:
    Best fitting model + reports the training results using Ray's train.report.
    """
    wandb.init(project="mbtadnn")
    print(f"Model will be saved in: {model_save_path}")

    # Extract best hyperparameters
    hidden_layers = best_hyperparameters["hidden_layers"]
    learning_rate = best_hyperparameters["learning_rate"]
    batch_size = best_hyperparameters["batch_size"]
    epochs = best_hyperparameters["epochs"]
    activation = best_hyperparameters["activation"]
    output_activation = best_hyperparameters["output_activation"]
    loss = best_hyperparameters["loss"]
    dropout_rate = best_hyperparameters["dropout_rate"]
    early_stopping_patience = best_hyperparameters["early_stopping_patience"]

    # Initialize AdamW optimizer with the best learning rate
    optimizer = tf.keras.optimizers.AdamW(
        learning_rate=learning_rate, weight_decay=1e-4
    )

    # Split the data into train and test sets
    train_df, test_df = train_test_split(data, test_size=0.3)
    # Train data
    train_x = train_df.drop("predictor_delay_seconds", axis=1)
    train_y = train_df["predictor_delay_seconds"]
    # Test data
    test_x = test_df.drop("predictor_delay_seconds", axis=1)
    test_y = test_df["predictor_delay_seconds"]

    # Create and compile the DNN model with the best hyperparameters
    input_dim = train_x.shape[1]
    dnn_model = create_dnn_model(input_dim, dropout_rate)
    dnn_model.compile(
        loss="mean_squared_error",
        optimizer=optimizer,
        metrics=[
            tf.keras.metrics.MeanAbsoluteError(),
            tf.keras.metrics.RootMeanSquaredError(),
        ],
    )

    # Train best fitting DNN model
    history = dnn_model.fit(
        train_x,
        train_y,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(test_x, test_y),
        verbose=2,
        callbacks=[DNN_early_10, DNN_plateau_lr, DNN_BestFit],
    )

    # Save best fitting DNN model
    dnn_model.save(model_save_path)
    print(f"Model saved to: {model_save_path}")

    # Evaluate best fitting DNN model on the test set
    y_pred = dnn_model.predict(test_x)
    mae = mean_absolute_error(test_y, y_pred)
    rmse = mean_squared_error(test_y, y_pred, squared=False)
    r2 = r2_score(test_y, y_pred)

    # Report metrics to Ray and W&B
    train.report({"rmse": rmse, "mae": mae, "r2": r2})
    wandb.log({"rmse": rmse, "mae": mae, "r2": r2, "config": best_hyperparameters})

    return dnn_model


# Train the DNN model with the best hyperparameters
best_model_save_path = MODEL_DIR / "best_dnn_model.h5"
best_trained_dnn_model = train_best_dnn(
    mbta_final_df, best_model_save_path, best_hyperparameters
)

# Shut down Ray
ray.shutdown()
