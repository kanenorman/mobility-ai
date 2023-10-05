""" gcp_dataloader.py: Functions for extracting and preprocessing transit data from GCP,
targeting machine learning & time series forecasting of bus arrivals and delays.
"""
from google.colab import auth
from google.cloud import storage
from google.cloud import bigquery
import pandas as pd
import numpy as np
import logging
from datetime import datetime


def authenticate_gcp() -> None:
    """
    Authenticates the user for Google Cloud Platform (GCP).

    Raises
    ------
    Exception
        If authentication fails.
    """
    try:
        auth.authenticate_user()
        logging.info("Successfully authenticated for GCP.")
    except Exception as e:
        logging.error("GCP Authentication failed.")
        raise e


def extract_from_gcp(
    project_id: str = "ac215-transit-prediction",
    vehicle_table: str = "`ac215-transit-prediction.vehicle.df`",
    trip_table: str = "`ac215-transit-prediction.trip.df`",
    stop_table: str = "`ac215-transit-prediction.stop.df`",
    schedule_table: str = "`ac215-transit-prediction.schedule.df`",
    verbose: bool = True,
    close_connection: bool = False,
) -> pd.DataFrame:
    """
    Extracts data from GCP Buckets based on the provided SQL query.

    Parameters
    ----------
    project_id : str, optional
        The Google Cloud Project ID where the BigQuery dataset resides.
    vehicle_table : str, optional
        The BigQuery table containing vehicle data.
    trip_table : str, optional
        The BigQuery table containing trip data.
    stop_table : str, optional
        The BigQuery table containing stop data.
    schedule_table : str, optional
        The BigQuery table containing schedule data.
    close_connection : bool, optional
        If True, will close the BigQuery client connection after extracting data.
    verbose : bool, optional
        If True, will print information about the extraction process.

    Returns
    -------
    pd.DataFrame
        Data extracted from BigQuery table.

    Notes
    -----
    Ensure you've authenticated using `authenticate_gcp()` before calling this function.
    """
    # Ensure user is authenticated
    authenticate_gcp()

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Start the timer for execution time
    start_time = datetime.now()

    # Initialize the BigQuery client
    client = bigquery.Client(project=project_id)

    if verbose:
        logging.info("Starting data extraction from BigQuery...")

    sql_query = f"""
    WITH training_data AS (
    SELECT
        v.updated_at AS time_stamp,
        v.id AS vehicle_id,
        v.current_status,
        v.latitude AS current_latitude,
        v.longitude AS current_longitude,
        stop.name AS destination,
        stop.platform_name,
        stop.latitude AS destination_latitude,
        stop.longitude AS destination_longitude,
        trip.name AS trip_name,
        schedule.departure_time AS scheduled_departure,
        schedule.arrival_time AS scheduled_arrival,
        stop.id AS stop_id,
        trip.id AS trip_id,
        CAST(schedule.stop_id AS STRING) AS sch_stop_id,
        CAST(schedule.trip_id AS STRING) AS sch_trip_id
    FROM {vehicle_table} AS v
    LEFT JOIN {trip_table} AS trip ON v.trip_id = trip.id
    LEFT JOIN {stop_table} AS stop ON v.stop_id = stop.id
    LEFT JOIN {schedule_table} AS schedule
        ON CAST(schedule.trip_id AS STRING) = CAST(v.trip_id AS STRING)
        AND CAST(schedule.stop_id AS STRING) = CAST(v.stop_id AS STRING)
    )
    SELECT *,
        MAX(CASE WHEN current_status = 'STOPPED_AT' THEN time_stamp ELSE NULL END)
        OVER(PARTITION BY sch_trip_id, sch_stop_id) AS actual_arrival_time
    FROM training_data;
    """

    query_job = client.query(sql_query)
    results = query_job.result()

    # Calculate execution time
    execution_time = datetime.now() - start_time

    # Log the details and execution time
    if verbose:
        print(f"Data successfully extracted from BigQuery.")
        print(f"Source Table: {vehicle_table}")
        print(f"Google Cloud Project ID: {project_id}")
        print(f"Service: BigQuery")
        print(f"Execution Time: {execution_time}")

    # After extracting data, close the client connection if close_connection is set to True
    if close_connection:
        client.close()
        if verbose:
            print("Closed BigQuery client connection.")

    return results.to_dataframe()


def preprocess_data(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Preprocess the dataframe for Machine Learning & Time Series Forecasting.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe containing transit data.
    verbose : bool, optional
        If True, will print information about the dataframe and NaN statistics,
        by default True.

    Returns
    -------
    pd.DataFrame
        Preprocessed dataframe ready for ML and Time Series Forecasting.

    Examples
    --------
    >>> df = pd.read_csv("transit_data.csv")
    >>> preprocessed_df = preprocess_data(df, verbose=True)
    """

    # Create a copy to avoid modifying the original dataframe
    df_copy = df.copy()

    # Store the initial shape of the dataframe
    initial_shape = df_copy.shape

    # Convert 'NULL' strings to actual NaNs for datetime columns
    datetime_cols = [
        "time_stamp",
        "scheduled_departure",
        "scheduled_arrival",
        "actual_arrival_time",
    ]
    for col in datetime_cols:
        df_copy[col].replace("NULL", np.nan, inplace=True)

    # Convert string timestamps to datetime objects for easy computation
    df_copy["time_stamp"] = (
        pd.to_datetime(df_copy["time_stamp"], errors="coerce")
        .dt.tz_localize(None)
        .dt.tz_localize("UTC")
        .dt.tz_convert("US/Eastern")
    )
    df_copy["scheduled_departure"] = (
        pd.to_datetime(df_copy["scheduled_departure"], errors="coerce")
        .dt.tz_localize(None)
        .dt.tz_localize("UTC")
        .dt.tz_convert("US/Eastern")
    )
    df_copy["scheduled_arrival"] = (
        pd.to_datetime(df_copy["scheduled_arrival"], errors="coerce")
        .dt.tz_localize(None)
        .dt.tz_localize("UTC")
        .dt.tz_convert("US/Eastern")
    )
    df_copy["actual_arrival_time"] = (
        pd.to_datetime(df_copy["actual_arrival_time"], errors="coerce")
        .dt.tz_localize(None)
        .dt.tz_localize("UTC")
        .dt.tz_convert("US/Eastern")
    )

    # Create delay column
    df_copy["delay"] = (
        df_copy["actual_arrival_time"] - df_copy["scheduled_arrival"]
    ).dt.total_seconds() / 60  # delay in minutes

    # Merge scheduled_departure and scheduled_arrival to form scheduled_time
    df_copy["scheduled_time"] = df_copy["scheduled_arrival"]

    # Drop scheduled_departure and scheduled_arrival
    df_copy.drop(columns=["scheduled_departure", "scheduled_arrival"], inplace=True)

    # Capture NaN statistics before changes
    nan_stats_before = df_copy.isna().sum()
    nan_percentage_before = (df_copy.isna().sum() / len(df_copy)) * 100

    # Handle NaN values
    for col in df_copy.columns:
        if df_copy[col].dtype == "object":
            mode_value = df_copy[col].mode()[0]
            df_copy[col].fillna(mode_value, inplace=True)
        else:
            mean_value = df_copy[col].mean()
            df_copy[col].fillna(mean_value, inplace=True)

    # Convert vehicle_id to a numerical representation
    df_copy["vehicle_id"] = df_copy["vehicle_id"].astype("category").cat.codes

    # Ensure data columns related to latitudes and longitudes are converted to float type
    for col in [
        "current_latitude",
        "current_longitude",
        "destination_latitude",
        "destination_longitude",
    ]:
        df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce")

    # Ensure data is ordered by time_stamp
    df_copy = df_copy.sort_values(by="time_stamp").reset_index(drop=True)

    # Capture NaN statistics after changes
    nan_stats_after = df_copy.isna().sum()

    if verbose:
        print(f"Initial shape of the dataframe: {initial_shape}")
        print("\n=== NaN Statistics (Before) ===")
        print(nan_stats_before.to_frame().to_markdown())
        print("\n=== NaN Percentage (Before) ===")
        print(nan_percentage_before.to_frame().to_markdown())
        print("\n=== NaN Statistics (After) ===")
        print(nan_stats_after.to_frame().to_markdown())
        print("\n=== Dataframe Info ===")
        print(df_copy.info())

    return df_copy
