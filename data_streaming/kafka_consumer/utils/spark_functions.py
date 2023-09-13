from typing import Iterable, List

import psycopg2
import pyspark
from psycopg2.extras import execute_values
from pyspark.sql import SparkSession

from .config import configs


def _get_postgres_connection():
    host = configs.POSTGRES_HOST
    database = configs.POSTGRES_DB
    user = configs.POSTGRES_USER
    password = configs.POSTGRES_PASSWORD

    return psycopg2.connect(
        **{
            "host": host,
            "database": database,
            "user": user,
            "password": password,
        }
    )


def _build_upsert_query(table_name: str, unique_key: str, columns: List[str]):
    column_names = ",".join(columns)

    return f"""INSERT INTO {table_name} ({column_names}) VALUES %s
               ON CONFLICT ({unique_key}) DO NOTHING"""


def _preform_upsert(batch, query, batch_size):
    with _get_postgres_connection() as connection:
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            execute_values(cur=cursor, sql=query, argslist=batch, page_size=batch_size)
            connection.commit()
            print("wrote to databse")


def _prepare_upsert(
    batch_partition: Iterable,
    query: str,
    batch_size: int = 1000,
):
    counter = 0
    batch = []

    for record in batch_partition:
        counter += 1
        batch.append(record)

        if counter % batch_size == 0:
            _preform_upsert(batch, query, batch_size)
            batch = []

    if len(batch) > 0:
        _preform_upsert(batch, query, batch_size)


def write_to_database(
    batch: pyspark.sql.DataFrame,
    epoch_id: int,
    table_name: str,
    unique_key: str,
    parallelism: int = 1,
) -> None:
    upsert_query = _build_upsert_query(
        columns=batch.schema.names, table_name=table_name, unique_key=unique_key
    )

    batch.coalesce(parallelism).rdd.mapPartitions(
        lambda dataframe_partition: _prepare_upsert(
            batch_partition=dataframe_partition,
            query=upsert_query,
            batch_size=1000,
        )
    )


def create_spark_session() -> pyspark.sql.SparkSession:
    """
    Create and configure a SparkSession.

    Returns
    -------
    pyspark.sql.SparkSession
        The configured SparkSession.
    """
    return (
        SparkSession.builder.appName("MBTA Data Streaming")
        .master("local[*]")
        .getOrCreate()
    )


def configure_spark_logging(spark: pyspark.sql.SparkSession) -> None:
    """
    Configure Spark logging level to ERROR.

    Parameters
    ----------
    spark : pyspark.sql.SparkSession
        The SparkSession to configure.
    """
    spark.sparkContext.setLogLevel("ERROR")
