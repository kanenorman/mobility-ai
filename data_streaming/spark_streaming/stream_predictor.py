from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
from xgboost.spark import SparkXGBRegressor


def stream_predictor(df: DataFrame) -> StreamingQuery:
    """
    Predict the arrival time for a given vehicle at a stop using SparkXGBRegressor.

    Parameters
    ----------
    df : DataFrame
        The DataFrame to perform the prediction on.

    Returns
    -------
    StreamingQuery
    """
    # Create a VectorAssembler for feature transformation
    assembler = VectorAssembler(
        inputCols=["distance_travel_miles", "sin_time", "cos_time"],
        outputCol="features",
    )

    # Initialize SparkXGBRegressor
    xgb_model = SparkXGBRegressor(
        featuresCol="features",
        predictionCol="xgboost_predictions",
        modelPath="./final_best_xgboost.json"
    )

    # Set up the ML pipeline
    pipeline = Pipeline(stages=[assembler, xgb_model])

    # Transform the data
    prediction_model = pipeline.fit(df)
    df_transformed = prediction_model.transform(df)

    # Set up streaming query
    prediction_stream: StreamingQuery = (
        df_transformed.writeStream.queryName("model_features_stream")
        .outputMode("append")
        .format("console")
        .start()
    )

    return prediction_stream
