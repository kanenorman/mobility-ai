from typing import Iterable, List

import psycopg2
import pyspark
from psycopg2.extras import execute_values
from pyspark.sql import SparkSession

from .config import configs


def _get_postgres_connection():
    """
    Create and return a Postgres database connection using the configurations.

    Returns
    -------
    psycopg2.extensions.connection
        The PostgreSQL database connection.
    """
    return psycopg2.connect(
        host=configs.POSTGRES_HOST,
        database=configs.POSTGRES_DB,
        user=configs.POSTGRES_USER,
        password=configs.POSTGRES_PASSWORD,
    )


def _build_upsert_query(table_name: str, unique_key: str, columns: List[str]):
    """
    Build and return the upsert (INSERT ON CONFLICT) query for PostgreSQL.

    Parameters
    ----------
    table_name : str
        The name of the target table.
    unique_key : str
        The unique key for conflict resolution.
    columns : List[str]
        The list of column names to insert.

    Returns
    -------
    str
        The upsert query.
    """
    column_names = ",".join(columns)

    return f"""INSERT INTO {table_name} ({column_names}) VALUES %s
               ON CONFLICT ({unique_key}) DO NOTHING"""


def _preform_upsert(batch, query, batch_size):
    """
    Execute the upsert operation on a batch of records in PostgreSQL.

    Parameters
    ----------
    batch : Iterable
        The batch of records to upsert.
    query : str
        The upsert query.
    batch_size : int
        The batch size for upserting records.

    Returns
    -------
    None
    """
    with _get_postgres_connection() as connection:
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            execute_values(cur=cursor, sql=query, argslist=batch, page_size=batch_size)
            connection.commit()


def _prepare_upsert(
    batch_partition: Iterable,
    query: str,
    batch_size: int = 1000,
):
    """
    Prepare and execute upsert operations on a partition of data.

    Parameters
    ----------
    batch_partition : Iterable
        The partition of data to upsert.
    query : str
        The upsert query.
    batch_size : int, optional
        The batch size for upserting records, by default 1000.

    Returns
    -------
    None
    """
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

    yield None


def write_to_database(
    batch: pyspark.sql.DataFrame,
    epoch_id: int,
    table_name: str,
    unique_key: str,
    parallelism: int = 1,
) -> None:
    """
    Write a batch of data to a PostgreSQL database using upsert (INSERT ON CONFLICT).

    Parameters
    ----------
    batch : pyspark.sql.DataFrame
        The batch of data to write.
    epoch_id : int
        The current epoch ID.
    table_name : str
        The name of the target table.
    unique_key : str
        The unique key for conflict resolution.
    parallelism : int, optional
        The degree of parallelism for writing data, by default 1.

    Returns
    -------
    None
    """
    upsert_query = _build_upsert_query(
        columns=batch.schema.names, table_name=table_name, unique_key=unique_key
    )

    batch.coalesce(parallelism).rdd.mapPartitions(
        lambda dataframe_partition: _prepare_upsert(
            batch_partition=dataframe_partition,
            query=upsert_query,
            batch_size=1000,
        )
    ).collect()


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
