import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T

from config import configs


def write_to_database(batch, batch_id):
    table = configs["POSTGRES_TABLE"]
    user = configs["POSTGRES_USER"]
    host = configs["POSTGRES_HOST"]
    port = configs["POSTGRES_PORT"]
    database = configs["POSTGRES_DB"]
    password = configs["POSTGRES_PASSWORD"]
    driver = configs["POSTGRES_DRIVER"]
    url = f"jdbc:postgresql://{host}:{port}/{database}"

    (
        batch.write.format("jdbc")
        .option("driver", driver)
        .option("url", url)
        .option("dbtable", table)
        .option("user", user)
        .option("password", password)
        .save()
    )


def main():
    spark = (
        SparkSession.builder.appName("MBTA Data Streaming")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1",
        )
        .master("local[*]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    kafka_host = configs["KAFKA_HOST"]
    kafka_port = configs["KAFKA_PORT"]
    kafka_topic = configs["SCHEDULES_INPUT_TOPIC"]
    bootstrap_servers = f"{kafka_host}:{kafka_port}"

    kafka_stream = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", bootstrap_servers)
        .option("subscribe", kafka_topic)
        .load()
    )

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

    query_kafka = (
        processed_df.writeStream.trigger(processingTime="10 seconds")
        .outputMode("update")
        .foreachBatch(write_to_database)
        .start()
    )

    query_kafka.awaitTermination()

    spark.stop()


if __name__ == "__main__":
    sys.exit(main())
