import asyncio
import json
import os
from typing import Dict, Union

import httpx
from config import configs
from httpx_sse import aconnect_sse
from kafka import KafkaProducer


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
    producer: KafkaProducer,
    topic: str,
    end_point: str,
    params: Union[Dict, None] = None,
):
    url = f"https://api-v3.mbta.com/{end_point}"
    headers = {"Accept": "text/event-stream", "X-API-Key": os.environ["MBTA_API_KEY"]}

    async with httpx.AsyncClient() as client:
        async with aconnect_sse(
            client, "GET", url, headers=headers, params=params, timeout=None
        ) as event_source:
            async for sse in event_source.aiter_sse():
                event = {"event": sse.event, "data": sse.data}
                await _send_to_kafka(producer=producer, topic=topic, message=event)


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
            "topic": "schedules",
            "end_point": "schedules",
            "params": {"filter[route]": "Red"},
        },
        {
            "topic": "trips",
            "end_point": "trips",
            "params": {"filter[route]": "Red"},
        },
        {
            "topic": "stops",
            "end_point": "stops",
            "params": {"filter[route]": "Red"},
        },
        {
            "topic": "shapes",
            "end_point": "shapes",
            "params": {"filter[route]": "Red"},
        },
        {
            "topic": "vehicles",
            "end_point": "vehicles",
            "params": {"filter[route]": "Red"},
        },
    )

    # Start fetching and sending data concurrently
    tasks = (_fetch_and_send_data(producer, **source) for source in data_sources)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
