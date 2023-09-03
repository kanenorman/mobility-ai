#!/bin/bash

# Function to check if Kafka is reachable
check_kafka() {
    nc -z -w 5 kafka $KAFKA_PORT 
}

until check_kafka; do
    echo "Kafka is not available yet. Retrying in 10 seconds..."
    sleep 10
done

echo "Kafka is now available. Starting producer..."
python producer.py
echo "Done"
