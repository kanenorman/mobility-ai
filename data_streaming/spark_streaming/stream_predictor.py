from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery
import pyspark.sql.types as T
import pyspark.sql.functions as F
import xgboost as xgb
import numpy as np


model_path = "./final_best_xgboost.json"
model = xgb.Booster()
model.load_model(model_path)


@F.udf(T.FloatType())
def prediction(features):
    if not features or not all(features):
        return None
    
    print(features)

    dmatrix = xgb.DMatrix(np.array([features.toArray()]))
    feature_names = ['distance_travel_miles', 'sin_time', 'cos_time']
    prediction = model.predict(dmatrix, feature_names=feature_names)
    return prediction[0]


def stream_predictor(df: DataFrame) -> StreamingQuery:
    """
    Predict the arrival time for a given vehicle at a stop using XGBoost.

    Parameters
    ----------
    df : DataFrame
        The DataFrame to perform the prediction on.
    """
    df = df.withColumn("prediction", prediction(F.col("features")))

    prediction_stream = (
        df.writeStream.queryName("model_features_stream")
        .outputMode("append")
        .format("console")
        .start()
    )

    return prediction_stream
