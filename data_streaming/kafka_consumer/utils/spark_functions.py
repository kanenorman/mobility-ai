import psycopg2
import pyspark
from pyspark.sql import SparkSession

from .config import configs


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


def write_to_database(batch: pyspark.sql.DataFrame, _: int) -> None:
    """
    Write batch data to a PostgreSQL database.

    Writes the given batch of data to a PostgreSQL database using JDBC.
    Spark JDBC insert does not have native support for INSERT IGNORE/REPLACE type
    operations. As a workaround, this function first inserts the batch into
    a temporary (staging) table. The staging table is then UPSERTED into
    the final production table using postgres ON CONFLICT.

    We are working under budget and time constraints for this project.
    We consider this an acceptable solution given the circumstance.

    Parameters
    ----------
    batch : pyspark.sql.DataFrame
        The batch of data to be written to the database.
    _ : int
        The ID of the current batch (unused in this function).
    """
    # Database configuration
    host = configs.POSTGRES_HOST
    port = configs.POSTGRES_PORT
    database = configs.POSTGRES_DB
    url = f"jdbc:postgresql://{host}:{port}/{database}"
    user = configs.POSTGRES_USER
    password = configs.POSTGRES_PASSWORD
    driver = configs.POSTGRES_DRIVER
    table_name = configs.POSTGRES_TABLE
    temp_table_name = f"temp_{table_name}"

    # Create a JDBC connection
    connection = psycopg2.connect(
        **{"host": host, "database": database, "user": user, "password": password}
    )
    cursor = connection.cursor()

    try:
        # Create the temporary table matching the schema of the production table
        cursor.execute(
            f"""
            CREATE TEMPORARY TABLE IF NOT EXISTS {temp_table_name}
            (LIKE {table_name} INCLUDING CONSTRAINTS);
            """
        )

        # Write data from 'batch' into the temporary table
        (
            batch.write.format("jdbc")
            .option("driver", driver)
            .option("url", url)
            .option("dbtable", temp_table_name)
            .option("user", user)
            .option("password", password)
            .mode("append")
            .save()
        )

        # Perform upsert from temporary table to production
        cursor.execute(
            f"""
            INSERT INTO {table_name}
            SELECT * FROM {temp_table_name}
            ON CONFLICT (id) DO NOTHING;
            """
        )

        # Remove temporary table
        cursor.execute(f"DROP TABLE IF EXISTS {temp_table_name};")
        connection.commit()
        print("wrote to database")
    finally:
        connection.close()
        cursor.close()
