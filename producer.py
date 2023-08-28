import json
import sys
import time
from datetime import datetime

from kafka import KafkaProducer

from config import configs
from mbta import get_schedules


def main():
    kafka_host = configs.KAFKA_HOST
    kafka_port = configs.KAFKA_PORT
    kafka_topic = configs.SCHEDULES_INPUT_TOPIC
    bootstrap_servers = f"{kafka_host}:{kafka_port}"
    producer = KafkaProducer(
        bootstrap_servers=[bootstrap_servers],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    prev_time = datetime.now()
    while True:
        current_time = datetime.now()
        messages = get_schedules("Red", min_time=prev_time, max_time=current_time)
        for message in messages:
            producer.send(kafka_topic, message["attributes"])

        prev_time = current_time
        print("message sent...")
        time.sleep(10)


if __name__ == "__main__":
    sys.exit(main())
