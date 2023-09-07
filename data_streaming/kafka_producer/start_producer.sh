#!/bin/bash

KAFKA_PORTS=("$KAFKA_PORT1" "$KAFKA_PORT2" "$KAFKA_PORT3")
KAFKA_HOST=("$KAFKA_HOST1" "$KAFKA_HOST2" "$KAFKA_HOST3")

kafka_running() {
    local result
    for index in "${!KAFKA_PORTS[@]}"; do
        port="${KAFKA_PORTS[$index]}"
        host="${KAFKA_HOST[$index]}"
        nc -z -w 5 "$host" "$port" && result="true" && break
    done
    if [[ "$result" == "true" ]]; then
        return 0
    else
        return 1
    fi
}

until kafka_running; do
    echo "Kafka is not available yet on any of the specified ports. Retrying in 3 seconds..."
    sleep 3
done

echo "Kafka is now available on at least one of the specified ports. Starting producer..."
python producer.py
echo "Done"
