"""
Distill_student.py: This module contains functions to distill the knowledge obtained
by the teacher to a student smaller model
"""

import psutil  # For system resource information
import ray  # For distributed computing

# Import necessary packages
import tensorflow as tf
import wandb  # For experiment tracking
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers
from tensorflow.keras.layers import Lambda  # For custom layers in the neural network
from tensorflow.keras.losses import KLDivergence  # KL divergence loss
from tensorflow.keras.optimizers import Adam  # Adam optimizer


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


# Define function to allocate computational resources
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


# Define a function to create a simple student model
def create_student_model(input_dim, dropout_rate):
    """
    Creates a simple student model for knowledge distillation.

    Args:
        input_dim (int): Dimension of the input data.
        dropout_rate (float): Rate of dropout for regularization.

    Returns:
        model: A student model ready for distillation.
    """
    model = tf.keras.Sequential(
        [
            layers.Dense(64, activation="relu", input_shape=(input_dim,)),
            layers.BatchNormalization(),  # Batch normalization layer
            layers.Dropout(dropout_rate),  # Dropout layer with a specified dropout rate
            layers.Dense(32, activation="relu"),
            layers.BatchNormalization(),  # Batch normalization layer
            layers.Dropout(dropout_rate),  # Dropout layer with a specified dropout rate
            layers.Dense(
                1
            ),  # Regression output layer with a single neuron (for regression)
        ]
    )
    return model


# Initialize Ray
ray.shutdown()
ray.init(
    num_cpus=num_cpus, num_gpus=num_gpus
)  # Initialize Ray with the specified CPU and GPU resources


# Update the train_student_model function
def train_student_model(data, model_save_path, config, teacher_model):
    """
    Distills knowledge and trains student model based on the supplied teacher model.

    Parameters:
    - data: Dataframe
    - model_save_path: File path to save the trained student model.
    - config (dict): Configuration for DNN tuning (e.g., dropout rate).
    - teacher_model: Keras DNN that the student model attempts to emulate.

    Returns:
    - Fit metrics for the student model.
    """
    # Initialize environment for knowledge distillation
    input_dim = data.shape[1] - 1  # Determine the input dimension
    dropout_rate = config["dropout_rate"]  # Get the dropout rate from the configuration
    train_df, test_df = train_test_split(
        data, test_size=0.3
    )  # Split the data into training and testing sets

    train_x = train_df.drop("predictor_delay_seconds", axis=1)
    train_y = train_df["predictor_delay_seconds"]
    test_x = test_df.drop("predictor_delay_seconds", axis=1)
    test_y = test_df["predictor_delay_seconds"]

    student_model = create_student_model(
        input_dim, dropout_rate
    )  # Create a student model

    # Define the distillation loss using a Lambda layer
    distillation_loss = tf.keras.layers.Lambda(lambda x: KLDivergence()(x[0], x[1]))

    # Compile the student model with both mean squared error loss and distillation loss
    student_model.compile(
        loss=[
            "mean_squared_error",  # Loss for the main regression task
            distillation_loss,  # Distillation loss
        ],
        loss_weights=[
            1.0,
            config["distillation_weight"],
        ],  # Control the balance between losses
        optimizer=Adam(learning_rate=config["learning_rate"]),
    )

    # Train the student model
    history = student_model.fit(
        train_x,
        [train_y, teacher_model.predict(train_x)],
        epochs=config["epochs"],
        batch_size=config["batch_size"],
        validation_data=(test_x, [test_y, teacher_model.predict(test_x)]),
        verbose=2,
    )

    # Save the student model
    student_model.save(model_save_path)
    print(f"Student model saved to: {model_save_path}")

    # Predict with the student model
    y_pred = student_model.predict(test_x)
    if len(y_pred) == 2:
        y_pred_main_task = y_pred[0]  # Select the main task output
    else:
        y_pred_main_task = y_pred  # Assuming there's only one output

    # Ensure that y_pred_main_task and test_y have consistent dimensions
    if y_pred_main_task.shape != test_y.shape:
        # Reshape y_pred_main_task if needed
        y_pred_main_task = y_pred_main_task.reshape(test_y.shape)

    # Calculate metrics
    mae = mean_absolute_error(test_y, y_pred_main_task)
    rmse = mean_squared_error(test_y, y_pred_main_task, squared=False)
    r2 = r2_score(test_y, y_pred_main_task)

    return rmse, mae, r2  # Return the calculated metrics


# Capture metrics during training
def trainable_student(config):
    # Initialize WandB for each trial
    wandb.init(project="mbtadnn_student")

    run_id = str(wandb.run.id)  # Convert wandb.run.id to a string
    model_save_path = str(MODEL_DIR / f"student_model_{run_id}.h5")
    print(f"Student model will be saved in: {model_save_path}")  # report for reference

    # Use the trainable function to train the student model
    rmse, mae, r2 = train_student_model(
        mbta_final_df, model_save_path, config, best_trained_dnn_model
    )

    # Report metrics to Ray and WandB
    ray.train.report({"rmse": rmse, "mae": mae, "r2": r2})  # Report 'rmse' metric
    wandb.log({"rmse": rmse, "mae": mae, "r2": r2, "config": config})


# Configure hyperparameter search space for the student model
student_param_space = {
    "dropout_rate": ray.tune.uniform(0.0, 0.5),  # Adjust as needed
    "distillation_weight": ray.tune.uniform(0.0, 1.0),
    "learning_rate": ray.tune.loguniform(1e-5, 1e-2),
    "epochs": ray.tune.choice([30, 50, 70]),
    "batch_size": ray.tune.choice([32, 64, 128]),
}

# Start hyperparameter tuning experiment for the student model
student_analysis = ray.tune.run(
    trainable_student,
    config=student_param_space,
    num_samples=NUM_TRIALS,
    name="student_tuning",
    stop={"training_iteration": 5},
    local_dir=str(EXPERIMENT_DIR),  # Specify the directory to store results
    verbose=1,
    metric="rmse",
    mode="min",  # optimization goal
)

# Obtain best student hyperparameters
best_student_hyperparameters = student_analysis.best_config


# Retrain the student model with the best hyperparameters
def retrain_student_with_best_hyperparameters(
    data, best_hyperparameters, teacher_model
):
    # Model save path for the new student model
    new_model_save_path = "retrained_student_model.h5"

    # Train the student model with the best hyperparameters
    rmse, mae, r2 = train_student_model(
        data, new_model_save_path, best_hyperparameters, teacher_model
    )

    # Report metrics for the retrained student model
    print("RMSE for the retrained student model:", rmse)
    print("MAE for the retrained student model:", mae)
    print("R2 for the retrained student model:", r2)


# Use the new function to retrain the student model with the best hyperparameters
retrain_student_with_best_hyperparameters(
    mbta_final_df, best_student_hyperparameters, best_trained_dnn_model
)

# Finish the WandB run after logging is complete
wandb.finish()

# Shut down Ray
ray.shutdown()
