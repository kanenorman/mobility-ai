import json
from typing import Dict

from config import configs
from kafka import KafkaProducer
from mbta import get_schedules
from sseclient import SSEClient


def process_message(producer: KafkaProducer, message: Dict):
    """
    Process a message and sends it to a Kafka topic.

    Parameters
    ----------
    producer : KafkaProducer
        The Kafka producer instance.
    message : dict
        The record to push into the Kafka topic.

    Returns
    -------
    None
    """
    schedules_topic = configs.SCHEDULES_INPUT_TOPIC
    producer.send(schedules_topic, message)


def main() -> None:
    """
    Primary function for the schedule processing.

    This function continuously fetches schedules
    using Server Sent Events (SSE) and sends them to the kafka topic.

    Returns
    -------
    None
    """
    bootstrap_servers = [
        f"{configs.KAFKA_HOST1}:{configs.KAFKA_PORT1}",
        f"{configs.KAFKA_HOST2}:{configs.KAFKA_PORT2}",
        f"{configs.KAFKA_HOST3}:{configs.KAFKA_PORT3}",
    ]

    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    schedules = get_schedules(route="Red")
    server = SSEClient(schedules)

    for event in server.events():
        process_message(
            producer=producer, message={"event": event.event, "data": event.data}
        )


if __name__ == "__main__":
    main()
