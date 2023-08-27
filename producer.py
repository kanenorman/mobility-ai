import json
import sys
import time

from kafka import KafkaProducer

from ..config import configs


def mock_data():
    return {"student_id": 12, "name": "Joe", "city": "New York"}


def main():
    kafka_host = configs.KAFKA_HOST
    kafka_port = configs.KAFKA_PORT
    kafka_topic = configs.SCHEDULES_INPUT_TOPIC
    bootstrap_servers = f"{kafka_host}:{kafka_port}"
    producer = KafkaProducer(
        bootstrap_servers=[bootstrap_servers],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    while True:
        data = mock_data()
        producer.send(kafka_topic, value=data)
        print("message sent...")
        time.sleep(5)


if __name__ == "__main__":
    sys.exit(main())
