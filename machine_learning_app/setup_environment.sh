#!/bin/bash

# Start Minikube with Docker driver
echo "Starting Minikube with Docker driver..."
minikube start --driver=docker

# Direct the shell to use Minikube's Docker daemon
echo "Setting up Minikube's Docker environment..."
eval $(minikube docker-env)

# Build the Docker image
echo "Building the Docker image..."
docker build -t machine_learning_app_prediction:latest -f Dockerfile.prediction .

# Deploy the application using Kubernetes
echo "Deploying the application..."
kubectl apply -f prediction-deployment.yaml

# Confirm the deployment
echo "Checking the deployment status..."
kubectl get pods
kubectl get deployments
kubectl get services

# Access the application (specific to Minikube with NodePort service)
echo "Fetching the application URL..."
minikube service machine-learning-prediction-service --url

echo "Setup complete."
