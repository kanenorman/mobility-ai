import asyncio
import json
from typing import Callable, Dict

from config import configs
from kafka import KafkaProducer
from mbta import get_alerts, get_schedules
from sseclient import SSEClient


def _create_kafka_producer() -> KafkaProducer:
    """
    Create and return a KafkaProducer instance.

    Returns
    -------
    KafkaProducer
        The Kafka producer instance.
    """
    bootstrap_servers = [
        f"{configs.KAFKA_HOST1}:{configs.KAFKA_PORT1}",
        f"{configs.KAFKA_HOST2}:{configs.KAFKA_PORT2}",
        f"{configs.KAFKA_HOST3}:{configs.KAFKA_PORT3}",
    ]

    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


async def _send_to_kafka(producer: KafkaProducer, topic: str, message: Dict):
    """
    Send a message to a Kafka topic using the provided producer.

    Parameters
    ----------
    producer : KafkaProducer
        The Kafka producer instance.
    topic : str
        The Kafka topic to send the message to.
    message : dict
        The record to push into the Kafka topic.

    Returns
    -------
    None
    """
    producer.send(topic, message)


async def _fetch_and_send_data(
    producer: KafkaProducer, fetch_func: Callable, topic: str, **kwargs
):
    """
    Fetch data and send it to a Kafka topic.

    Parameters
    ----------
    producer : KafkaProducer
        The Kafka producer instance.
    fetch_func : Callable
        A function to fetch the data.
    topic : str
        The Kafka topic to send the data to.
    kwargs : dict
        Additional keyword arguments to pass to fetch_func.

    Returns
    -------
    None
    """
    response = fetch_func(**kwargs)
    server = SSEClient(response)

    for event in server.events():
        tasks = (
            asyncio.create_task(
                _send_to_kafka(
                    producer=producer,
                    topic=topic,
                    message={"event": event.event, "data": data},
                )
            )
            for data in json.loads(event.data)
        )

        await asyncio.gather(*tasks)


async def main() -> None:
    """
    Primary function for processing schedules and alerts.

    This function fetches schedules and alerts and sends them to Kafka topics.

    Returns
    -------
    None
    """
    producer = _create_kafka_producer()

    # Define the data sources and topics with their respective parameters
    data_sources = (
        {
            "producer": producer,
            "fetch_func": get_alerts,
            "topic": configs.ALERTS_INPUT_TOPIC,
            "params": {"filter[route]": "Red"},
        },
        {
            "producer": producer,
            "fetch_func": get_schedules,
            "topic": configs.SCHEDULES_INPUT_TOPIC,
            "params": {"filter[route]": "Red"},
        },
    )

    # Start fetching and sending data concurrently
    tasks = (_fetch_and_send_data(**source) for source in data_sources)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
