import asyncio
import json
from typing import Dict, List, Union

import httpx
from httpx_sse import aconnect_sse
from kafka import KafkaProducer
from stamina import retry

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
        key_serializer=lambda k: k.encode("utf-8"),
    )


async def _send_to_kafka(
    producer: KafkaProducer, topic: str, value: Dict, key: str
) -> None:
    """
    Send a message to a Kafka topic using the provided producer.

    Parameters
    ----------
    producer : KafkaProducer
        The Kafka producer instance.
    topic : str
        The Kafka topic to send the message to.
    value : dict
        The record to push into the Kafka topic.
    key : str
        The unique key for the Kafka record
    Returns
    -------
    None
    """
    producer.send(topic=topic, value=value, key=key)


async def _send_batch_to_kafka(
    producer: KafkaProducer, topic: str, event: str, batch_data: List[Dict]
) -> None:
    """
    Send array of JSON objects to Kafka.

    Parameters
    ----------
    producer : Kafka Producer
        Kafka producer instance.
    topic : str
        Kafka topic to write to.
    event : str
        Server Sent Event. Will be one of "reset", "add", "update", "remove"
    batch_data : List[Dict]
        Array of JSON data

    Returns
    -------
    None
    """
    tasks = (
        _send_to_kafka(
            producer=producer,
            topic=topic,
            value={"event": event, "data": data},
            key=data["id"],
        )
        for data in batch_data
    )

    await asyncio.gather(*tasks)


def _iter_sse_retrying(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    headers: Union[Dict, None] = None,
    params: Union[Dict, None] = None,
):
    """
    Handle reconnections for SSE interuptions.

    Parameters
    ----------
    client : httpx.AsyncClient
        Async connection client
    method : str
        HTTP method (i.e. GET/POST)
    url : str
        API url (e.g https://mbta-v3.mbta.com/predictions)
    headers : Union[Dict, None]
        Request headers
    params : Union[Dict, None]
        Request parameters

    Notes
    -----
    See https://github.com/florimondmanca/httpx-sse#handling-reconnections
    """
    last_event_id = ""
    reconnection_delay = 0.0

    @retry(on=[httpx.ReadError, httpx.RemoteProtocolError], attempts=5)
    async def _aiter_sse():
        nonlocal last_event_id, reconnection_delay

        await asyncio.sleep(reconnection_delay)

        if last_event_id:
            headers["Last-Event-ID"] = last_event_id

        async with aconnect_sse(
            client, method, url, headers=headers, params=params
        ) as event_source:
            async for sse in event_source.aiter_sse():
                last_event_id = sse.id

                if sse.retry is not None:
                    reconnection_delay = sse.retry / 1000

                yield sse

    return _aiter_sse()


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
    async for server_sent_event in _iter_sse_retrying(
        client=client, method="GET", url=url, params=params, headers=headers
    ):
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
                value={"event": response_event, "data": response_data},
                key=response_data["id"],
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
    limits = httpx.Limits(
        max_connections=None, max_keepalive_connections=20, keepalive_expiry=None
    )

    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        producer = _create_kafka_producer()

        data_sources = (
            {
                "topic": "schedule-topic",
                "end_point": "schedules",
                "params": {
                    "filter[route]": "Red,Orange,Blue,Green-B,Green-C,Green-D,Green-E",
                },
            },
            {
                "topic": "trip-topic",
                "end_point": "trips",
                "params": {
                    "filter[route]": "Red,Orange,Blue,Green-B,Green-C,Green-D,Green-E",
                },
            },
            {
                "topic": "stop-topic",
                "end_point": "stops",
                "params": {
                    "filter[route]": "Red,Orange,Blue,Green-B,Green-C,Green-D,Green-E",
                    "include": "child_stops",
                },
            },
            {
                "topic": "shape-topic",
                "end_point": "shapes",
                "params": {
                    "filter[route]": "Red,Orange,Blue,Green-B,Green-C,Green-D,Green-E",
                },
            },
            {
                "topic": "vehicle-topic",
                "end_point": "vehicles",
                "params": {
                    "filter[route]": "Red,Orange,Blue,Green-B,Green-C,Green-D,Green-E",
                },
            },
            {
                "topic": "route-topic",
                "end_point": "routes",
            },
        )

        tasks = (
            _fetch_and_send_data(producer, client, **source) for source in data_sources
        )

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
