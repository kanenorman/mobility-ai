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
    MBTA_API_KEY: str = os.environ["MBTA_API_KEY"]


configs = _Config()
