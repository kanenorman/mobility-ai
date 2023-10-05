import pytest
from hamcrest import assert_that, equal_to

from data_streaming.kafka_consumer.utils import spark_functions


@pytest.mark.parametrize(
    "table_name, on_conflict_key, columns, expected_query",
    [
        (
            "table1",
            "id",
            ["col1", "col2"],
            "INSERT INTO table1 (col1,col2) VALUES %s ON CONFLICT (id) DO UPDATE SET (col1,col2) = (EXCLUDED.col1, EXCLUDED.col2);",
        ),
        (
            "table2",
            ["id", "name"],
            ["col1", "col2"],
            "INSERT INTO table2 (col1,col2) VALUES %s ON CONFLICT (id,name) DO UPDATE SET (col1,col2) = (EXCLUDED.col1, EXCLUDED.col2);",
        ),
        ("table3", None, ["col1", "col2"], "INSERT INTO table3 (col1,col2) VALUES %s;"),
    ],
)
def test_build_upsert_query(table_name, on_conflict_key, columns, expected_query):
    result = spark_functions._build_upsert_query(table_name, on_conflict_key, columns)
    assert_that(result, equal_to(expected_query))
