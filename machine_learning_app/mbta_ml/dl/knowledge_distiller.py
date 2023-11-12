"""
knowledge_distillation.py: This module provides an OOP implementation to distill knowledge
from a teacher model into a student model.
"""
import ray  # For distributed computing
import tensorflow as tf
import wandb  # For experiment tracking
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Lambda
from tensorflow.keras.losses import KLDivergence
from tensorflow.keras.optimizers import Adam
from utils import check_resources, configure_ray_resources


class KnowledgeDistillation:
    """Knowledge Distillation class for training a student model.

    Attributes:
        STUDENT_PARAM_SPACE (dict): Hyperparameters search space for student model.
    """

    STUDENT_PARAM_SPACE = {
        "dropout_rate": ray.tune.uniform(0.0, 0.5),
        "distillation_weight": ray.tune.uniform(0.0, 1.0),
        "learning_rate": ray.tune.loguniform(1e-5, 1e-2),
        "epochs": ray.tune.choice([30, 50, 70]),
        "batch_size": ray.tune.choice([32, 64, 128]),
    }

    def __init__(self, teacher_model):
        """Initialize Knowledge Distillation instance with teacher model.

        Parameters:
            teacher_model (tf.keras.Model): Trained teacher model.
        """
        self.teacher_model = teacher_model

    @staticmethod
    def create_student_model(input_dim, dropout_rate):
        """Creates a student model for knowledge distillation.

        Parameters:
            input_dim (int): Input data dimension.
            dropout_rate (float): Dropout rate for regularization.

        Returns:
            tf.keras.Sequential: Student model for distillation.
        """
        model = tf.keras.Sequential(
            [
                tf.keras.layers.Dense(64, activation="relu", input_shape=(input_dim,)),
                tf.keras.layers.BatchNormalization(),
                tf.keras.layers.Dropout(dropout_rate),
                tf.keras.layers.Dense(32, activation="relu"),
                tf.keras.layers.BatchNormalization(),
                tf.keras.layers.Dropout(dropout_rate),
                tf.keras.layers.Dense(1),
            ]
        )
        return model

    def train_student_model(self, data, model_save_path, config):
        """Distills knowledge and trains a student model.

        Parameters:
            data (pd.DataFrame): Input data.
            model_save_path (str): Path to save the student model.
            config (dict): DNN tuning configuration.

        Returns:
            tuple: RMSE, MAE, and R^2 metrics of the student model.
        """
        # Initialize environment for knowledge distillation
        input_dim = data.shape[1] - 1  # Determine the input dimension
        dropout_rate = config[
            "dropout_rate"
        ]  # Get the dropout rate from the configuration
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

    def trainable_student(self, config):
        """Trains student model and logs metrics during training.

        Parameters:
            config (dict): Configuration parameters for training.

        Returns:
            None
        """
        # Initialize WandB for each trial
        wandb.init(project="mbtadnn_student")

        run_id = str(wandb.run.id)  # Convert wandb.run.id to a string
        model_save_path = str(MODEL_DIR / f"student_model_{run_id}.h5")
        print(
            f"Student model will be saved in: {model_save_path}"
        )  # report for reference

        # Use the trainable function to train the student model
        rmse, mae, r2 = train_student_model(
            mbta_final_df, model_save_path, config, best_trained_dnn_model
        )

        # Report metrics to Ray and WandB
        ray.train.report({"rmse": rmse, "mae": mae, "r2": r2})  # Report 'rmse' metric
        wandb.log({"rmse": rmse, "mae": mae, "r2": r2, "config": config})

    def retrain_student_with_best_hyperparameters(self, data, best_hyperparameters):
        """Retrains the student model with the best hyperparameters.

        Parameters:
            data (pd.DataFrame): Input data.
            best_hyperparameters (dict): Best hyperparameters for training.

        Returns:
            None
        """
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


if __name__ == "__main__":
    # Determine computational resources
    num_cpus, num_gpus, total_memory_gb = check_resources()

    # Configure Ray to utilize all available resources
    configure_ray_resources(num_cpus, num_gpus)

    # Initialize the knowledge distillation object with the teacher model
    kd = KnowledgeDistillation(best_trained_dnn_model)

    # Start hyperparameter tuning for the student model
    student_analysis = ray.tune.run(
        kd.trainable_student,  # Use the instance method as the training function
        config=kd.STUDENT_PARAM_SPACE,  # Access the parameter space via the instance
        num_samples=NUM_TRIALS,
        name="student_tuning",
        stop={"training_iteration": 5},
        local_dir=str(EXPERIMENT_DIR),
        verbose=1,
        metric="rmse",
        mode="min",
    )

    # Get best hyperparameters
    best_student_hyperparameters = student_analysis.best_config

    # Retrain with best hyperparameters using the knowledge distillation object
    kd.retrain_student_with_best_hyperparameters(
        mbta_final_df, best_student_hyperparameters
    )

    wandb.finish()
    ray.shutdown()
