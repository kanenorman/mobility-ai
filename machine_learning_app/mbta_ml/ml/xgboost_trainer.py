""" xgboost_trainer.py: This module contains functions to train, build, and save ML models.
It also incorporates functionality to evaluate model performance using various regression metrics.
"""
import os
from datetime import datetime
from pathlib import Path
from typing import Tuple
from mbta_ml.config import (
    TUNING_NUM_TRIALS_CONFIG,
    BASE_DIR,
    MODEL_DIR,
    EXPERIMENT_DIR,
    WANDB_API_KEY,
    GCP_SERVICE_ACCOUNT_FILE
)
import mbta_ml.authenticate as auth
import pandas as pd
import sklearn.datasets
import sklearn.metrics
import wandb
import xgboost as xgb
from permetrics import RegressionMetric
from ray import train, tune
from ray.air.integrations.wandb import WandbLoggerCallback
from sktime.forecasting.model_selection import temporal_train_test_split
from mbta_ml.etl.delay_etl import data_checks_and_cleaning, transform
from mbta_ml.etl.gcp_dataloader import extract_from_gcp, preprocess_data

# Set global variables
TUNING_NUM_TRIALS = TUNING_NUM_TRIALS_CONFIG["xgboost"]
global mbta_final_df

def compute_metrics_table(forecasts_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute metrics table for regression modeling.

    Parameters
    ----------
    forecasts_df : pd.DataFrame
        DataFrame containing "algorithm", "y_pred", and "y_true" columns.

    Returns
    -------
    pd.DataFrame
        A table containing the evaluation metrics for each algorithm.
    """

    final_results = {}
    unique_algorithms = forecasts_df["algorithm"].unique()

    for algorithm in unique_algorithms:
        y_true = forecasts_df[forecasts_df["algorithm"] == algorithm]["y_true"].values
        y_pred = forecasts_df[forecasts_df["algorithm"] == algorithm]["y_pred"].values

        evaluator = RegressionMetric()
        evaluators = {
            "MAE": evaluator.MAE,
            "RMSE": evaluator.RMSE,
            "SMAPE": evaluator.SMAPE,
            "ME": evaluator.ME,
            "MedAE": evaluator.MedAE,
        }

        model_results = {}
        for metric, evaluator_function in evaluators.items():
            score = evaluator_function(y_true, y_pred, decimal=4)
            model_results[metric] = score

        final_results[algorithm] = model_results

    results_df = pd.DataFrame(final_results).transpose()

    return results_df


def retrain_best_xgboost(
    data: pd.DataFrame, config: dict, model_save_path: Path, test_size: float = 0.25
) -> Tuple[xgb.Booster, pd.DataFrame]:
    """
    Retrain XGBoost model with the best hyperparameters from tuning.

    Parameters:
    -----------
    data : pd.DataFrame
        The dataframe containing the data to train the model on.

    config : dict
        Dictionary containing the best hyperparameters from tuning.

    model_save_path : Path
        Path object representing where the model will be saved.

    test_size : float, optional
        Proportion of the dataset to include in the test split. Default is 0.25.

    Returns:
    --------
    Tuple[xgb.Booster, pd.DataFrame]
        The trained XGBoost model and a table containing the evaluation metrics for the retrained model.
    """
    print(f"Model will be saved in: {model_save_path}")

    # Split the data temporally
    train_df, test_df = temporal_train_test_split(data, test_size=test_size)

    train_x = train_df.drop("predictor_delay_seconds", axis=1)
    train_y = train_df["predictor_delay_seconds"]

    test_x = test_df.drop("predictor_delay_seconds", axis=1)
    test_y = test_df["predictor_delay_seconds"]

    # Convert data to DMatrix format for xgboost
    train_set = xgb.DMatrix(train_x, label=train_y)
    test_set = xgb.DMatrix(test_x, label=test_y)

    # Train the regressor using best hyperparameters
    bst = xgb.train(config, train_set, evals=[(test_set, "eval")], verbose_eval=False)

    # Save the model
    bst.save_model(str(model_save_path))
    print(f"Model saved to: {model_save_path}")

    # Predict on the test set
    y_pred = bst.predict(test_set)

    # Create a dataframe for metric computation
    forecasts_df = pd.DataFrame(
        {
            "algorithm": ["xgboost_best"] * len(y_pred),
            "y_pred": y_pred,
            "y_true": test_y,
        }
    )

    # Compute the metrics table
    metrics_table = compute_metrics_table(forecasts_df)
    return bst, metrics_table


def retrain_model_with_best_config(
    tuner, data: pd.DataFrame, model_save_path: str
) -> Tuple[object, pd.DataFrame]:
    """
    Retrieve the best configuration from a completed Ray Tune experiment
    and retrain the model with this configuration.

    Parameters
    ----------
    tuner : object
        The completed Ray Tune experiment.
    data : pd.DataFrame
        The dataset used for retraining.
    model_save_path : str
        Path to save the retrained model.

    Returns
    -------
    best_model : object
        The retrained model.
    performance_table : pd.DataFrame
        Table describing the model's performance.

    """

    # Get all results from the tuner
    print("Retrieving best configuration from tuner results...")
    results = tuner.get_results()

    # Extract the best result based on RMSE
    best_result = min(results, key=lambda x: x.metrics["rmse"])
    best_config = best_result.config

    # Print best config for clarity
    print(f"Best configuration found:\n{best_config}")

    # Retrain and save the model with the best hyperparameters
    print("Retraining model with the best configuration...")
    best_model, performance_table = retrain_best_xgboost(
        data=data, config=best_config, model_save_path=model_save_path
    )

    # Print performance table
    print("Performance of the retrained model:")
    print(performance_table)

    return best_model, performance_table


def train_mbta(config):
    """
    Train an XGBoost model on MBTA data.

    Parameters:
    - config (dict): Configuration for XGBoost training.

    Returns:
    None. Reports the training results using Ray's train.report.
    """
    wandb.init(project="ac215_harvard_mobility_ai")

    train_df, test_df = temporal_train_test_split(mbta_final_df, test_size=0.25)

    train_x = train_df.drop("predictor_delay_seconds", axis=1)
    train_y = train_df["predictor_delay_seconds"]

    test_x = test_df.drop("predictor_delay_seconds", axis=1)
    test_y = test_df["predictor_delay_seconds"]

    # Convert data to DMatrix format for xgboost
    train_set = xgb.DMatrix(train_x, label=train_y)
    test_set = xgb.DMatrix(test_x, label=test_y)

    # Train the regressor
    results = {}
    bst = xgb.train(
        config,
        train_set,
        evals=[(test_set, "eval")],
        evals_result=results,
        verbose_eval=False,
    )

    # Calculate metrics
    y_pred = bst.predict(test_set)
    rmse = sklearn.metrics.mean_squared_error(test_y, y_pred, squared=False)
    mae = sklearn.metrics.mean_absolute_error(test_y, y_pred)
    r2 = sklearn.metrics.r2_score(test_y, y_pred)

    # Report metrics to Ray and W&B
    train.report({"rmse": rmse, "mae": mae, "r2": r2})
    wandb.log({"rmse": rmse, "mae": mae, "r2": r2, "config": config})


if __name__ == "__main__":
    print(f"Model will be saved in: {MODEL_DIR}")
    print(f"Experiments will be stored in: {EXPERIMENT_DIR}")
    print(f"Running for number of trials: {TUNING_NUM_TRIALS}")
    

    # Authenticate with Google Cloud Platform
    auth.authenticate_with_gcp()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCP_SERVICE_ACCOUNT_FILE

    # Authenticate and initialize W&B
    auth.authenticate_with_wandb()

    # Extract data
    raw_df = extract_from_gcp(verbose=False, close_connection=True)
    raw_df = preprocess_data(raw_df, verbose=False)
    transformed_df, le_dict = transform(raw_df)
    mbta_final_df = data_checks_and_cleaning(transformed_df, verbose=False)
    
    # Define tuner and start tuning
    tuner = tune.Tuner(
        train_mbta,
        tune_config=tune.TuneConfig(
            metric="rmse",
            mode="min",
            num_samples=NUM_TRIALS,  # specify number of experiments
        ),
        run_config=train.RunConfig(
            callbacks=[WandbLoggerCallback(project="ac215_harvard_mobility_ai")]
        ),
        param_space={
            "objective": "reg:squarederror",
            "eval_metric": ["rmse"],
            "max_depth": tune.randint(1, 15),
            "min_child_weight": tune.choice([1, 2, 3, 4, 5]),
            "subsample": tune.uniform(0.4, 1.0),
            "eta": tune.loguniform(1e-4, 1e-1),
            "n_estimators": tune.randint(50, 500),
            "colsample_bytree": tune.uniform(0.4, 1.0),
        },
    )
    tuner.fit()

    # Get all results
    results = tuner.get_results()

    # Extract the best result based on RMSE
    best_result = min(results, key=lambda x: x.metrics["rmse"])
    best_config = best_result.config

    # Retrain and save the model with the best hyperparameters
    best_model, performance_table = retrain_model_with_best_config(
        tuner=tuner,
        data=mbta_final_df,
        model_save_path=str(MODEL_DIR / "final_best_xgboost.json"),
    )
