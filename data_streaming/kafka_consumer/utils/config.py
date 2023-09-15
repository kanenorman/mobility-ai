import os
from dataclasses import dataclass


@dataclass(frozen=True)
class _Config:
    KAFKA_HOST1: str = os.environ["KAFKA_HOST1"]
    KAFKA_PORT1: str = os.environ["KAFKA_PORT1"]
    KAFKA_HOST2: str = os.environ["KAFKA_HOST2"]
    KAFKA_PORT2: str = os.environ["KAFKA_PORT2"]
    KAFKA_HOST3: str = os.environ["KAFKA_HOST3"]
    KAFKA_PORT3: str = os.environ["KAFKA_PORT3"]
    SCHEDULES_INPUT_TOPIC: str = os.environ["SCHEDULES_INPUT_TOPIC"]
    POSTGRES_PORT: str = os.environ["POSTGRES_PORT"]
    POSTGRES_DB: str = os.environ["POSTGRES_DB"]
    POSTGRES_USER: str = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_HOST: str = os.environ["POSTGRES_HOST"]
    POSTGRES_DRIVER: str = os.environ["POSTGRES_DRIVER"]
    POSTGRES_TABLE: str = os.environ["POSTGRES_TABLE"]


configs = _Config()