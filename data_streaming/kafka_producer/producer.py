import asyncio
import json
from typing import Dict, Union

import httpx
from httpx_sse import aconnect_sse
from kafka import KafkaProducer

from .config import configs


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


async def _send_to_kafka(producer: KafkaProducer, topic: str, message: Dict) -> None:
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


async def _send_batch_to_kafka(
    producer: KafkaProducer, topic: str, event: str, batch_data: str
) -> None:
    """
    Send array of JSON objects to Kafka.

    Parameters
    ----------
    producer
        Kafka producer instance.
    topic
        Kafka topic to write to.
    event
        Server Sent Event. Will be one of "reset", "add", "update", "remove"
    batch_data
        Array of JSON data

    Returns
    -------
    None
    """
    tasks = (
        _send_to_kafka(
            producer=producer,
            topic=topic,
            message={"event": event, "data": data},
        )
        for data in batch_data
    )

    await asyncio.gather(*tasks)


async def _fetch_and_send_data(
    producer: KafkaProducer,
    client: httpx.AsyncClient,
    topic: str,
    end_point: str,
    params: Union[Dict, None] = None,
) -> None:
    """
    Fetch API data and send to kafka producer.

    Parameters
    ----------
    producer
        Kafka producer instance.
    client
        httpx Connection Client (must be async)
    topic
        Kafka topic to write to.
    end_point
        MBTA API endpoint (e.g. alerts, schedules, etc.)
    params
        API request parameters (e.g. 'filter[route]', 'id', etc.)

    Returns
    -------
    None

    Notes
    -----
    See https://api-v3.mbta.com/docs/swagger/index.html
    for API documentation

    See https://www.mbta.com/developers/v3-api/streaming
    for streaming API documentation
    """
    url = f"https://api-v3.mbta.com/{end_point}"
    headers = {"Accept": "text/event-stream", "X-API-Key": configs.MBTA_API_KEY}
    # TODO: Find solution to fix issue with aconnect_sse.
    # see https://github.com/florimondmanca/httpx-sse/issues/4
    while True:
        async with aconnect_sse(
            client=client,
            method="GET",
            url=url,
            headers=headers,
            params=params,
        ) as event_source:
            async for server_sent_event in event_source.aiter_sse():
                response_data = json.loads(server_sent_event.data)
                response_event = server_sent_event.event

                # reset events return an array of JSON objects
                if response_event == "reset":
                    await _send_batch_to_kafka(
                        producer=producer,
                        topic=topic,
                        event=response_event,
                        batch_data=response_data,
                    )
                # other events return a single JSON object
                else:
                    await _send_to_kafka(
                        producer=producer,
                        topic=topic,
                        message={"event": response_event, "data": response_data},
                    )


async def main() -> None:
    """
    Primary function for processing schedules and alerts.

    This function fetches schedules and alerts and sends them to Kafka topics.

    Returns
    -------
    None
    """
    timeout = httpx.Timeout(connect=None, read=None, write=None, pool=None)
    limits = httpx.Limits(max_keepalive_connections=None, keepalive_expiry=None)

    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
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
                "params": {"filter[route]": "Red", "include": "child_stops"},
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
        tasks = (
            _fetch_and_send_data(producer, client, **source) for source in data_sources
        )

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
