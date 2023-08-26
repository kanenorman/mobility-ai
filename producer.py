import json
import sys
import time

from kafka import KafkaProducer

from config import configs


def mock_data():
    return {"student_id": 12, "name": "Joe", "city": "New York"}


def main():
    kafka_host = configs.get("kafka", "HOST")
    kafka_port = configs.get("kafka", "PORT")
    kafka_topic = configs.get("kafka", "SCHEDULES_INPUT_TOPIC")
    bootstrap_servers = f"{kafka_host}:{kafka_port}"

    while True:
        producer = KafkaProducer(
            bootstrap_servers=[bootstrap_servers],
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

        data = mock_data()
        producer.send(kafka_topic, value=data)
        print("message sent...")
        time.sleep(5)


if __name__ == "__main__":
    sys.exit(main())
