import asyncio
import json
from datetime import datetime

from kafka import KafkaProducer

from config import configs
from mbta import get_predictions, get_schedules


async def process_message(producer, message):
    schedules_topic = configs.SCHEDULES_INPUT_TOPIC
    predictions_topic = configs.PREDICTIONS_INPUT_TOPIC
    producer.send(schedules_topic, message)

    route_data = message["relationships"]["route"]["data"]
    route, trip, stop = route_data["id"], route_data["id"], route_data["id"]

    prediction_message = await get_predictions(route, trip, stop)
    producer.send(predictions_topic, prediction_message)


async def main() -> None:
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
        tasks = []
        for message in messages:
            task = asyncio.create_task(process_message(producer, message))
            tasks.append(task)

        await asyncio.gather(*tasks)

        prev_time = current_time
        print("Batch of messages sent...")
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
