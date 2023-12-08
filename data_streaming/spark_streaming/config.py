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


configs = _Config()
