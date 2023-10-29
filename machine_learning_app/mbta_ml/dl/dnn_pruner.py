"""deep_learning_pruner.py: This module contains a class to prune and fine-tune the best
fitting base model to improve its performance and decrease model size.
"""
from pathlib import Path

import ray
import tensorflow_model_optimization as tfmot
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sktime.forecasting.model_selection import temporal_train_test_split
from utils import check_resources, configure_ray_resources


class DLModelPruner:
    """A class used to prune and fine-tune deep learning models.

    Attributes
    ----------
    model_dir : pathlib.Path
        Directory where the models will be saved.
    WEIGHT_PRUNING_PARAMS : dict
        Dictionary containing specifications for weight pruning.
    NEURON_PRUNING_PARAMS : dict
        Dictionary containing specifications for neuron pruning.

    Methods
    -------
    prune_and_fine_tune(best_model, data, config, pruning_params, is_neuron_pruning=False):
        Prunes and fine-tunes the provided model based on the given parameters.
    """

    def __init__(self, model_dir=Path("../models")):
        """
        Parameters
        ----------
        model_dir : pathlib.Path, optional
            Directory where the models will be saved (default is "../models").
        """
        self.model_dir = model_dir
        self.model_dir.mkdir(parents=True, exist_ok=True)

        # Define pruning_params for weight pruning
        self.WEIGHT_PRUNING_PARAMS = {
            "target_sparsity_weight": 0.50,
            "begin_step": 0,
            "end_step": 100,
        }

        # Define pruning_params for neuron pruning
        self.NEURON_PRUNING_PARAMS = {
            "target_sparsity_neuron": 0.50,
            "begin_step": 0,
            "end_step": 100,
            "prune_frequency": 1,
        }

    def prune_and_fine_tune(
        self, best_model, data, config, pruning_params, is_neuron_pruning=False
    ):
        """
        Prunes and fine-tunes the provided model based on the given parameters.

        Parameters
        ----------
        best_model : keras.Model
            Keras model object (DNN).
        data : pd.DataFrame
            DataFrame containing the data.
        config : dict
            Configuration for DNN tuning with best fitting parameters.
        pruning_params : dict
            Dictionary containing specifications for pruning.
        is_neuron_pruning : bool, optional
            Determines behavior (neuron or weight level pruning). Defaults to False.

        Returns
        -------
        keras.Model
            Pruned Model. Reports the training results using Ray's train.report.
        """
        # Create a copy of the original model
        pruned_model = tf.keras.models.clone_model(best_model)

        # Define model save path for the pruned model based on flag value
        if is_neuron_pruning:
            pruning_method = "neuron"
            pruned_model_save_path = model_dir / f"pruned_neuron_model.h5"
        else:
            pruning_method = "weight"
            pruned_model_save_path = model_dir / f"pruned_weight_model.h5"

        # Initialize WandB for pruning and fine-tuning run
        wandb.init(project="mbtadnn_pruning_fine_tuning")

        # Set up Ray tracking for pruning and fine-tuning run
        ray.shutdown()
        ray.init()

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

        # Temporal train-test split
        train_df, test_df = temporal_train_test_split(data, test_size=test_size)
        train_x = train_df.drop("predictor_delay_seconds", axis=1)
        train_y = train_df["predictor_delay_seconds"]
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
        print(f"Pruned model saved to: {pruned_model_save_path}")

        # Evaluate pruned model performance on the test set
        y_pred = pruned_model.predict(test_x)  # Make predictions
        mae = mean_absolute_error(test_y, y_pred)  # Evaluate predictions
        rmse = mean_squared_error(test_y, y_pred, squared=False)  # Evaluate predictions
        r2 = r2_score(test_y, y_pred)  # Evaluate predictions

        # Report metrics to Ray and WandB
        ray.train.report({"rmse": rmse, "mae": mae, "r2": r2})
        wandb.log({"rmse": rmse, "mae": mae, "r2": r2})

        # Return the pruned and fine-tuned model
        return pruned_model


if __name__ == "__main__":
    num_cpus, num_gpus, total_memory_gb = check_resources()
    configure_ray_resources(num_cpus, num_gpus)
    pruner = DLModelPruner()

    best_trained_dnn_model_copy = tf.keras.models.clone_model(best_trained_dnn_model)
    wandb.init(project="mbtadnn_pruning_fine_tuning")
    ray.init()

    pruned_weight_model = pruner.prune_and_fine_tune(
        best_trained_dnn_model_copy,
        mbta_final_df,
        best_hyperparameters,
        pruner.WEIGHT_PRUNING_PARAMS,
        is_neuron_pruning=False,
    )

    best_trained_dnn_model_copy = tf.keras.models.clone_model(best_trained_dnn_model)

    pruned_neuron_model = pruner.prune_and_fine_tune(
        best_trained_dnn_model_copy,
        mbta_final_df,
        best_hyperparameters,
        pruner.NEURON_PRUNING_PARAMS,
        is_neuron_pruning=True,
    )

    wandb.finish()
    ray.shutdown()
