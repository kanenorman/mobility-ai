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

    Notes
    -----
    Mimics the following Postgres command:

        INSERT INTO <table_name> (<column1>, <column2>)
        VALUES
            (<value1_1>, <value1_2>),
            (<value2_1>, <value2_2>),
            (<value3_1>, <value3_2>)
        ON CONFLICT (<conflict_column>) DO UPDATE
        SET <update_column> = EXCLUDED.<update_column>;
    """
    column_names = ",".join(columns)
    columns_with_excluded_markers = [f"EXCLUDED.{column}" for column in columns]
    excluded_columns = ", ".join(columns_with_excluded_markers)

    insert_query = """ INSERT INTO %s (%s) VALUES %%s """ % (table_name, column_names)
    on_conflict_clause = """ ON CONFLICT (%s) DO UPDATE SET (%s) = (%s) ;""" % (
        unique_key,
        column_names,
        excluded_columns,
    )

    return insert_query + on_conflict_clause


def _build_delete_query(table_name: str, unique_key: str):
    """
    Build and return the delete query for PostgreSQL.

    Parameters
    ----------
    table_name : str
        The name of the target table from which to delete records.
    unique_key : str
        The column name used as a unique key to specify which records to delete.

    Returns
    -------
    str
        The delete query.

    Examples
    --------
    >>> _build_delete_query("my_table", "id")
    'DELETE FROM my_table WHERE id = %s'

    Notes
    -----
    Mimics the following Postgres command:

        DELETE FROM <table_name> WHERE <key> = <value>;
    """
    return """DELETE FROM %s WHERE %s = %%s""" % (table_name, unique_key)


def _preform_deletion(deletion_query: str, value: str):
    """
    Execute the deletion operation on a single Postgres record.

    Parameters
    ----------
    deletion_query
        the deletion query.
    value
        the value to match against the key for deletion.
    """
    with _get_postgres_connection() as connection:
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            execute_values(cur=cursor, sql=deletion_query, argslist=value)
            connection.commit()


def _preform_upsert(batch: List[pyspark.sql.Row], query: str, batch_size: int):
    """
    Execute the upsert operation on a batch of records in PostgreSQL.

    Parameters
    ----------
    batch : List[pyspark.sql.Row]
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
    upsert_query: str,
    deletion_query: str,
    batch_size: int = 1000,
):
    """
    Prepare and execute upsert operations on a partition of data.

    Parameters
    ----------
    batch_partition : Iterable
        The partition of data to upsert.
    upsert_query : str
        The upsert query.
    deletion_query : str
        The deletion query.
    batch_size : int, optional
        The batch size for upserting records, by default 1000.

    Returns
    -------
    None
    """
    # The logic is as follows:
    # Iterate through each record in the batch_partition
    # If the record indicates a "remove" operation, we:
    # 1. Upsert the current batch (if it contains any records).
    # 2. Perform the deletion operation specified by deletion_query.
    # Otherwise, we:
    # 1. Increment the counter.
    # 2. Add the record to the batch for upsert.
    # After adding a record, if the batch size exceeds batch_size, we upsert the batch
    # After processing all records, upsert any remaining records in the batch.

    counter: int = 0
    batch: List[pyspark.sql.Row] = []

    for record in batch_partition:
        if record.event == "remove":
            if len(batch) > 0:
                _preform_upsert(batch, upsert_query, batch_size)
                batch = []
            _preform_deletion(deletion_query, record.id)
        else:
            counter += 1
            batch.append(record)

        if counter % batch_size == 0:
            _preform_upsert(batch, upsert_query, batch_size)
            batch = []

    if len(batch) > 0:
        _preform_upsert(batch, upsert_query, batch_size)

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

    deletion_query = _build_delete_query(table_name=table_name, unique_key=unique_key)

    batch.coalesce(parallelism).rdd.mapPartitions(
        lambda dataframe_partition: _prepare_upsert(
            batch_partition=dataframe_partition,
            upsert_query=upsert_query,
            deletion_query=deletion_query,
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
