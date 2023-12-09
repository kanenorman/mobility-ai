from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery
from xgboost.spark import SparkXGBRegressor


def stream_predictor(df: DataFrame):
    """
    Predict the arrival time for a given vehicle at a stop using XGBoost.

    Parameters
    ----------
    df : DataFrame
        The DataFrame to perform the prediction on.
    """
    # Load the model
    booster = SparkXGBRegressor()
    # model = booster.load("/app/data_streaming/spark_streaming/final_best_xgboost.json")

    # df = model.transform(df)

    prediction_stream: StreamingQuery = (
        df.writeStream.queryName("model_features_stream")
        .outputMode("append")
        .format("console")
        .start()
    )

    return prediction_stream
