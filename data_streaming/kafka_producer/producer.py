import asyncio
import json
from datetime import datetime
from typing import Dict

from config import configs
from kafka import KafkaProducer
from mbta import get_schedules


async def process_message(producer: KafkaProducer, message: Dict):
    """
    Process a message and sends to kafka topic

    Parameters
    ----------
    producer
       Kafka producer instance
    message
        Record to push into kafka topic

    Returns
    -------
        None
    """
    schedules_topic = configs.SCHEDULES_INPUT_TOPIC
    producer.send(schedules_topic, message)


async def main() -> None:
    """
    Main function for the asynchronous schedule processing.

    This function continuously fetches schedules, processes them,
    and sends them to Kafka.

    Returns
    _______
        None
    """
    kafka_host = configs.KAFKA_HOST
    kafka_port = configs.KAFKA_PORT
    bootstrap_servers = f"{kafka_host}:{kafka_port}"

    producer = KafkaProducer(
        bootstrap_servers=[bootstrap_servers],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    prev_time = datetime.now()
    while True:
        current_time = datetime.now()
        messages = get_schedules(route="Red", min_time=prev_time, max_time=current_time)

        tasks = (
            asyncio.create_task(process_message(producer, message))
            for message in messages
        )
        await asyncio.gather(*tasks)

        prev_time = current_time
        print("Batch of messages sent...")
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
