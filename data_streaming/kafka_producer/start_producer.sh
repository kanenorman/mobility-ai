#!/bin/bash

kafka_running() {
    nc -z -w 5 kafka $KAFKA_PORT 
}

until kafka_running; do
    echo "Kafka is not available yet. Retrying in 10 seconds..."
    sleep 10
done

echo "Kafka is now available. Starting producer..."
python producer.py
echo "Done"
