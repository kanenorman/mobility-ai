import os
from abc import ABC
from dataclasses import dataclass


class _Config(ABC):
    TESTING = False
    DEBUG = False


@dataclass(frozen=True)
class _DevelopmentConfigs(_Config):
    SQLALCHEMY_DATABASE_URI = os.environ["DEV_POSTGRES_URI"]
    DEBUG = True


@dataclass(frozen=True)
class _ProductionConfigs(_Config):
    pass


@dataclass(frozen=True)
class _TestConfigs(_Config):
    TESTING = True
    DEBUG = True


config = {
    "dev": _DevelopmentConfigs,
    "prod": _ProductionConfigs,
    "test": _TestConfigs,
}
