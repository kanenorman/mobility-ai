#!/bin/bash

# Fetch the service URL dynamically
URL=$(minikube service machine-learning-prediction-service --url)

# Append the endpoint path
PREDICT_URL="${URL}/predict"

echo "Sending requests to $PREDICT_URL"

# Send POST requests concurrently
curl -X POST -H "Content-Type: application/json" -d @tests/payload1.json $PREDICT_URL &
curl -X POST -H "Content-Type: application/json" -d @tests/payload2.json $PREDICT_URL &
curl -X POST -H "Content-Type: application/json" -d @tests/payload3.json $PREDICT_URL &

wait
echo "All requests sent."
