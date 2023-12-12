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
def predict_arrival(scheduled_time, features):
    if not features or not all(features):
        return None

    feature_names = ["distance_travel_miles", "sin_time", "cos_time"]
    numpy_features = np.array([features])
    dmatrix = xgb.DMatrix(numpy_features, feature_names=feature_names)

    prediction = model.predict(dmatrix)
    delay = float(prediction[0])

    return scheduled_time + datetime.timedelta(seconds=delay)


def stream_predictor(df: DataFrame) -> StreamingQuery:
    """
    Predict the arrival time for a given vehicle at a stop using XGBoost.

    Parameters
    ----------
    df : DataFrame
        The DataFrame to perform the prediction on.
    """
    df = df.withColumn(
        "predicted_arrival", predict_arrival(F.col("scheduled_time"), F.col("features"))
    )
    df = df.drop("features")

    prediction_stream = (
        df.writeStream.queryName("model_features_stream")
        .outputMode("append")
        .format("console")
        .start()
    )

    return prediction_stream
