import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class _Config:
    KAFKA_HOST: str = os.environ["KAFKA_HOST"]
    KAFKA_PORT: str = os.environ["KAFKA_PORT"]
    SCHEDULES_INPUT_TOPIC: str = os.environ["SCHEDULES_INPUT_TOPIC"]
    POSTGRES_PORT: str = os.environ["POSTGRES_PORT"]
    POSTGRES_DB: str = os.environ["POSTGRES_DB"]
    POSTGRES_USER: str = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_HOST: str = os.environ["POSTGRES_HOST"]
    POSTGRES_DRIVER: str = os.environ["POSTGRES_DRIVER"]
    POSTGRES_TABLE: str = os.environ["POSTGRES_TABLE"]


configs = _Config()
