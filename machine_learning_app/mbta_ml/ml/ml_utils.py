""" ml_utils.py: This module contains functions to train, build, and save ML models.
"""
import pandas as pd
from permetrics import RegressionMetric


def compute_metrics_table(forecasts_df: pd.DataFrame) -> pd.DataFrame:
    """Compute metrics table for regression modeling.

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
