import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class _Config:
    KAFKA_HOST: str = os.environ["KAFKA_HOST"]
    KAFKA_PORT: str = os.environ["KAFKA_PORT"]
    SCHEDULES_INPUT_TOPIC: str = os.environ["SCHEDULES_INPUT_TOPIC"]
    MBTA_API_KEY: str = os.environ["MBTA_API_KEY"]


configs = _Config()
