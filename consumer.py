import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T

from config import configs


def write_to_database(batch, batch_id):
    host = configs.POSTGRES_HOST
    port = configs.POSTGRES_PORT
    database = configs.POSTGRES_DB
    url = f"jdbc:postgresql://{host}:{port}/{database}"

    (
        batch.write.format("jdbc")
        .option("driver", configs.POSTGRES_DRIVER)
        .option("url", url)
        .option("dbtable", configs.POSTGRES_TABLE)
        .option("user", configs.POSTGRES_USER)
        .option("password", configs.POSTGRES_PASSWORD)
        .mode("append")
        .save()
    )


def process_kafka_stream(kafka_stream):
    schema = T.StructType(
        [
            T.StructField("timepoint", T.BooleanType()),
            T.StructField("stop_sequence", T.IntegerType()),
            T.StructField("stop_headsign", T.StringType()),
            T.StructField("pickup_type", T.IntegerType()),
            T.StructField("drop_off_type", T.IntegerType()),
            T.StructField("direction_id", T.IntegerType()),
            T.StructField("departure_time", T.TimestampType()),
            T.StructField("arrival_time", T.TimestampType()),
        ]
    )
    kafka_df = kafka_stream.withColumn("value", F.col("value").cast("string"))
    processed_df = kafka_df.withColumn("json", F.from_json(F.col("value"), schema))

    return processed_df.select("json.*")


def main():
    spark = (
        SparkSession.builder.appName("MBTA Data Streaming")
        .master("local[*]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    kafka_host = configs.KAFKA_HOST
    kafka_port = configs.KAFKA_PORT
    kafka_topic = configs.SCHEDULES_INPUT_TOPIC
    bootstrap_servers = f"{kafka_host}:{kafka_port}"

    kafka_stream = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", bootstrap_servers)
        .option("subscribe", kafka_topic)
        .load()
    )

    processed_df = process_kafka_stream(kafka_stream)

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
