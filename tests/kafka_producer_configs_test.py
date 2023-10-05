import os
from dataclasses import FrozenInstanceError

import pytest
from hamcrest import assert_that, has_properties

from data_streaming.kafka_producer.config import configs


def test_config_initiates_with_environment_variables():
    assert_that(
        configs,
        has_properties(
            KAFKA_HOST1=os.environ["KAFKA_HOST1"],
            KAFKA_HOST2=os.environ["KAFKA_HOST2"],
            KAFKA_HOST3=os.environ["KAFKA_HOST3"],
            KAFKA_PORT1=os.environ["KAFKA_PORT1"],
            KAFKA_PORT2=os.environ["KAFKA_PORT2"],
            KAFKA_PORT3=os.environ["KAFKA_PORT3"],
            MBTA_API_KEY=os.environ["MBTA_API_KEY"],
        ),
    )


def test_config_object_is_immutable():
    with pytest.raises(FrozenInstanceError):
        configs.KAFKA_HOST1 = "new_value"


def test_config_object_does_not_allow_duck_typing():
    with pytest.raises(AttributeError):
        configs.some_attr_that_doesnt_exist = "foo"
