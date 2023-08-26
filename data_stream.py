import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T

from config import configs


def extract_kafka(kafka_stream):
    df = kafka_stream.select(F.col("value").cast("string").alias("json"))
    schema = T.StructType(
        [
            T.StructField("student_id", T.StringType()),
            T.StructField("name", T.StringType()),
            T.StructField("city", T.StringType()),
        ]
    )

    processed_df = df.select(
        F.from_json(F.col("json").cast("string"), schema).alias("parsed_value")
    ).select("parsed_value.*")

    # Output the processed data to the console
    query = processed_df.writeStream.outputMode("append").format("console").start()

    # Wait for the termination of the query
    query.awaitTermination()


def write_to_database(df):
    url = configs["jdbc_url"]
    table = configs["DB_TABLE"]
    user = configs["BD_USER"]
    password = configs["DB_PASSWORD"]
    driver = configs["DB_DRIVER"]
    properties = {"user": user, "password": password, "driver": driver}
    mode = "append"

    df.write.jdbc(url, table, mode, properties)


def main():
    spark = (
        SparkSession.builder.appName("MBTA Data Streaming")
        .master("local[*]")
        .getOrCreate()
    )

    kafka_host = configs["KAFKA_HOST"]
    kafka_port = configs["KAFKA_PORT"]
    kafka_topic = configs["SCHEDULES_INPUT_TOPIC"]
    bootstrap_servers = f"{kafka_host}:{kafka_port}"

    kafka_stream = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", bootstrap_servers)
        .option("subscribe", kafka_topic)
        .option("startingOffsets", "latest")
        .load()
    )

    extract_kafka(kafka_stream)


if __name__ == "__main__":
    sys.exit(main())
