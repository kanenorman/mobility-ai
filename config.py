import os
from collections import namedtuple

from dotenv import load_dotenv

load_dotenv()

_Config = namedtuple(
    "Config",
    [
        "KAFKA_HOST",
        "KAFKA_PORT",
        "SCHEDULES_INPUT_TOPIC",
        "MBTA_API_KEY",
        "POSTGRES_PORT",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_HOST",
        "POSTGRES_DRIVER",
        "POSTGRES_TABLE",
    ],
)

configs = _Config(
    KAFKA_HOST=os.environ["KAFKA_HOST"],
    KAFKA_PORT=os.environ["KAFKA_PORT"],
    SCHEDULES_INPUT_TOPIC=os.environ["SCHEDULES_INPUT_TOPIC"],
    MBTA_API_KEY=os.environ["MBTA_API_KEY"],
    POSTGRES_PORT=os.environ["POSTGRES_PORT"],
    POSTGRES_DB=os.environ["POSTGRES_DB"],
    POSTGRES_USER=os.environ["POSTGRES_USER"],
    POSTGRES_PASSWORD=os.environ["POSTGRES_PASSWORD"],
    POSTGRES_HOST=os.environ["POSTGRES_HOST"],
    POSTGRES_DRIVER=os.environ["POSTGRES_DRIVER"],
    POSTGRES_TABLE=os.environ["POSTGRES_TABLE"],
)
