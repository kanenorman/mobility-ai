from typing import List
from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery
import pyspark.sql.types as T
import pyspark.sql.functions as F
import xgboost as xgb
import numpy as np
import datetime

# TODO: TRANSITION TO SPARK ML
model_path = "./final_best_xgboost.json"
model = xgb.Booster()
model.load_model(model_path)


@F.udf(T.TimestampType())
def _predict_arrival(scheduled_time: datetime.datetime, features: List[float]):
    """
    Predict the arrival time for a given vehicle at a stop using XGBoost.

    Parameters
    ----------
    scheduled_time : datetime.datetime
        Scheduled time of train arrival
    features : List[float]
        Input features for the model.

    Returns
    -------
    datetime.datetime
        Predicted arrival time.
    """
    if not features or not all(features):
        return None

    feature_names = ["distance_travel_miles", "sin_time", "cos_time"]
    numpy_features = np.array([features])
    dmatrix = xgb.DMatrix(numpy_features, feature_names=feature_names)

    prediction = model.predict(dmatrix)
    delay = float(prediction[0])

    return scheduled_time + datetime.timedelta(seconds=delay)


def stream_predictor(df: DataFrame, bootstrap_servers: str) -> StreamingQuery:
    """
    Predict the arrival time for a given vehicle at a stop using XGBoost.

    Parameters
    ----------
    df : DataFrame
        The DataFrame to perform the prediction on.
    bootstrap_servers : str
        Kafka bootstrap servers
    """
    df = df.withColumn(
        "predicted_arrival",
        _predict_arrival(F.col("scheduled_time"), F.col("features")),
    )
    df = df.drop("features")

    df = df.select(
        F.concat_ws(",", F.col("vehicle_id"), F.col("trip_id"), F.col("stop_id")).alias(
            "key"
        ),
        F.col("predicted_arrival").cast("string").alias("value"),
    )

    prediction_stream = (
        df.writeStream.format("kafka")
        .option("kafka.bootstrap.servers", bootstrap_servers)
        .option("topic", "predictions")
        .option("checkpointLocation", "/tmp/mbta/checkpoint")
        .outputMode("append")
        .start()
    )

    return prediction_stream
