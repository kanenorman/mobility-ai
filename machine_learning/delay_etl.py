"""  delay_etl.py: Provides functions to preprocess transit data for ML-driven
bus delay prediction.

Explanation of modelling approach:

1. Prediction Target:
We aim to estimate E[time of arrival | various features], indicating the
expected bus arrival time given specific conditions like weather and
date-based features.

2. Complexity with `actual_arrival_time`:
Predicting exact datetimes, such as bus arrival times, poses challenges due
to the granularity of potential outcomes. For instance, predicting the exact
second of arrival (e.g., 3:05:23 PM vs. 3:05:24 PM) introduces considerable
variance.

3. Problem Simplification:
Instead of precise arrival times, we predict delay durations. This offers a
more tractable modeling task: a 5-minute predicted delay can be added to the
scheduled time, while negligible delays suggest on-time arrivals.
"""
import h3
from haversine import haversine, Unit
from sklearn.preprocessing import LabelEncoder
import numpy as np
from typing import Tuple, Dict
import pandas as pd

def create_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract date features from scheduled_time column.

    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame containing `scheduled_time` column.

    Returns:
    --------
    df : pd.DataFrame
        DataFrame with additional date features.
    """
    # Convert the scheduled_time into a datetime object
    df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])

    # Extract date features
    df['month'] = df['scheduled_time'].dt.month
    df['day_of_week'] = df['scheduled_time'].dt.dayofweek
    df['day_of_year'] = df['scheduled_time'].dt.dayofyear

    # Create sin/cos encoding for time
    seconds_in_day = 24*60*60
    df['sin_time'] = np.sin(2*np.pi*df['scheduled_time'].dt.second/seconds_in_day)
    df['cos_time'] = np.cos(2*np.pi*df['scheduled_time'].dt.second/seconds_in_day)

    # Determine season based on month
    df['season'] = df['month'].apply(lambda x: (x%12 + 3)//3)

    return df


def transform(data_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, LabelEncoder]]:
    """
    Transform MBTA data for ML tasks on transport times & distances.

    The key column is "predictor_delay_seconds", a numerical value
    representing delay (or being ahead) in seconds. Positive values
    indicate delays, while negative values mean arriving early. All
    other columns are features for ML to predict this delay.

    Parameters:
    -----------
    data_df : pd.DataFrame
        DataFrame after preprocessing MBTA data.

    Returns:
    --------
    transformed_df : pd.DataFrame
        DataFrame with features for ML tasks.
    le_dict : Dict[str, LabelEncoder]
        Mappings used for transformation.
    """
    # Convert "scheduled_time" and "actual_arrival_time" to datetime format
    data_df["scheduled_time"] = pd.to_datetime(data_df["scheduled_time"])
    data_df["actual_arrival_time"] = pd.to_datetime(data_df["actual_arrival_time"])

    # Compute "predictor_delay_seconds" in seconds
    data_df["predictor_delay_seconds"] = (data_df["actual_arrival_time"] - data_df["scheduled_time"]).dt.total_seconds()

    # Compute the hex values for locations
    resolution = 9  # you can adjust the resolution as required
    data_df['current_location_hex'] = data_df.apply(lambda row: h3.geo_to_h3(row['current_latitude'], row['current_longitude'], resolution), axis=1)
    data_df['destination_location_hex'] = data_df.apply(lambda row: h3.geo_to_h3(row['destination_latitude'], row['destination_longitude'], resolution), axis=1)

    # Encode categorical columns
    le_dict = {}
    for col in ["vehicle_id", "destination", "platform_name", "current_location_hex", "destination_location_hex"]:
        le = LabelEncoder()
        data_df[col] = le.fit_transform(data_df[col])
        le_dict[col] = le

    # Compute distance of travel using haversine package and name it as "distance_travel_miles"
    data_df["distance_travel_miles"] = data_df.apply(
        lambda x: haversine(
            (x['current_latitude'], x['current_longitude']),
            (x['destination_latitude'], x['destination_longitude']),
            unit=Unit.MILES
        ),
        axis=1
    )

    # Extract date-based features
    data_df = create_date_features(data_df)

    # Drop unnecessary columns
    cols_to_drop = ['time_stamp', 'current_status', 'trip_name', 'stop_id', 'trip_id', 'sch_stop_id', 'sch_trip_id',
                    'actual_arrival_time', 'scheduled_time', 'current_latitude', 'current_longitude',
                    'destination_latitude', 'destination_longitude', 'delay', 'distance_travel', 'predictor_delay_time']
    transformed_df = data_df.drop(columns=cols_to_drop, errors='ignore')  # Added errors='ignore' to ensure it doesn't fail if a column is missing

    return transformed_df, le_dict

def data_checks_and_cleaning(df: pd.DataFrame, verbose: bool=True) -> pd.DataFrame:
    """
    Process the MBTA DataFrame to:
    1. Report and flag any erroneous data.
    2. Drop duplicates and columns with low variance.
    3. Return a dataset ready for ML modeling.

    Parameters:
    -----------
    df : pd.DataFrame
        The MBTA DataFrame to process.
    verbose : bool, optional
        Whether or not to print out the processing steps. Default is True.

    Returns:
    --------
    pd.DataFrame
        The processed DataFrame ready for ML modeling.
    """

    if verbose:
        # Print shape before processing
        print(f"Initial DataFrame shape: {df.shape}")

        # Basic statistics
        print("\nBasic Descriptive Statistics:")
        print(df.describe().to_markdown())

    # Check for NaN values
    nan_count = df.isna().sum().sum()
    if verbose:
        print(f"\nTotal NaN values in the dataset: {nan_count}")

    # Check for duplicates
    duplicate_count = df.duplicated().sum()
    df = df.drop_duplicates()
    if verbose:
        print(f"\nTotal duplicate rows in the dataset: {duplicate_count}")

    # Derive the number of seconds in 24 hours
    seconds_in_24_hours = 24 * 60 * 60
    # Check if 'predictor_delay_seconds' has extremely large values (more than 24 hours)
    extreme_delay_count = (abs(df['predictor_delay_seconds']) > seconds_in_24_hours).sum()
    if verbose:
        print(f"\nRows with delay exceeding 24 hours: {extreme_delay_count}")

    # Checking range of sin_time and cos_time values
    sin_out_of_range = ((df['sin_time'] < -1) | (df['sin_time'] > 1)).sum()
    cos_out_of_range = ((df['cos_time'] < -1) | (df['cos_time'] > 1)).sum()
    if verbose:
        print(f"\nRows with sin_time out of [-1,1] range: {sin_out_of_range}")
        print(f"Rows with cos_time out of [-1,1] range: {cos_out_of_range}")

    # Check for negative values in columns where they don't make sense
    negative_distance_count = (df['distance_travel_miles'] < 0).sum()
    if verbose:
        print(f"\nRows with negative distance values: {negative_distance_count}")

    # Drop columns with zero variance
    zero_variance_cols = df.columns[df.std() == 0]
    if len(zero_variance_cols) > 0:
        df = df.drop(columns=zero_variance_cols)
        if verbose:
            print(f"\nDropping columns with zero variance: {', '.join(zero_variance_cols)}")

    if verbose:
        # Print shape after processing
        print(f"\nDataFrame shape after processing: {df.shape}")

    return df
