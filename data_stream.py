from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T

from config import configs


def main():
    spark = (
        SparkSession.builder.appName("MBTA Data Streaming")
        .master("local[*]")
        .getOrCreate()
    )

    kafka_host = configs.get("kafka", "HOST")
    kafka_port = configs.get("kafka", "PORT")
    kafka_topic = configs.get("kafka", "SCHEDULES_INPUT_TOPIC")
    bootstrap_servers = f"{kafka_host}:{kafka_port}"

    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", bootstrap_servers)
        .option("subscribe", kafka_topic)
        .option("startingOffsets", "latest")
        .load()
    )

    # Process kafka stream
    processed_df = df.selectExpr("CAST(value AS STRING) AS json")
    schema = T.StructType(
        [
            T.StructField("student_id", T.StringType()),
            T.StructField("name", T.StringType()),
            T.StructField("city", T.StringType()),
        ]
    )

    processed_df = processed_df.select(
        F.from_json(F.col("json").cast("string"), schema).alias("parsed_value")
    ).select("parsed_value.*")

    # Output the processed data to the console
    query = processed_df.writeStream.outputMode("append").format("console").start()

    # Wait for the termination of the query
    query.awaitTermination()


if __name__ == "__main__":
    main()
