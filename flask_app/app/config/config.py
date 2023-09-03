import os
from dataclasses import dataclass


@dataclass(frozen=True)
class _DevelopmentConfigs:
    SQLALCHEMY_DATABASE_URI = os.environ["DEV_POSTGRES_URI"]


@dataclass(frozen=True)
class _ProductionConfigs:
    pass


@dataclass(frozen=True)
class _TestConfigs:
    pass


config = {"dev": _DevelopmentConfigs, "prod": _ProductionConfigs, "test": _TestConfigs}
