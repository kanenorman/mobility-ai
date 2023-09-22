import os
from abc import ABC
from dataclasses import dataclass


class _Config(ABC):
    TESTING = False


@dataclass(frozen=True)
class _DevelopmentConfigs(_Config):
    SQLALCHEMY_DATABASE_URI = os.environ["DEV_POSTGRES_URI"]


@dataclass(frozen=True)
class _ProductionConfigs(_Config):
    pass


@dataclass(frozen=True)
class _TestConfigs(_Config):
    TESTING = True


config = {
    "dev": _DevelopmentConfigs,
    "prod": _ProductionConfigs,
    "test": _TestConfigs,
}
