#!/bin/bash

# Function to check if Minikube is running
check_minikube_status() {
    minikube_status=$(minikube status --format "{{.Host}}")
    if [ "$minikube_status" != "Running" ]; then
        echo "Starting Minikube with Docker driver..."
        minikube start --driver=docker
    else
        echo "Minikube is already running."
    fi
}

# Function to build the Docker image
build_docker_image() {
    echo "Building the Docker image..."
    eval $(minikube docker-env)
    docker build -t machine_learning_app_prediction:latest -f Dockerfile.prediction .
}

# Function to deploy the application
deploy_application() {
    echo "Deploying the application..."
    kubectl apply -f prediction-deployment.yaml
}

# Function to wait for pods to be in the 'Running' state
wait_for_pods() {
    echo "Waiting for pods to be in the 'Running' state..."
    local retries=0
    local max_retries=12 # Waits for up to 1 minute (12 retries * 5 seconds)
    while : ; do
        pod_status=$(kubectl get pods -l app=machine-learning-prediction -o custom-columns=STATUS:.status.phase --no-headers | grep -v Running)
        if [ -z "$pod_status" ]; then
            echo "All pods are running."
            break
        else
            if [ $retries -eq $max_retries ]; then
                echo "Timeout waiting for pods to be running."
                exit 1
            fi
            echo "Waiting for pod to be running..."
            sleep 5
            ((retries++))
        fi
    done
}

# Function to fetch the application URL
fetch_application_url() {
    echo "Fetching the application URL..."
    minikube service machine-learning-prediction-service --url
}

# Function to print the status of all pods
print_pod_statuses() {
    echo "Printing status of all pods..."
    kubectl get pods -l app=machine-learning-prediction -o wide
}

# Main script execution
check_minikube_status
build_docker_image
deploy_application
wait_for_pods
print_pod_statuses
fetch_application_url

echo "Setup complete."
