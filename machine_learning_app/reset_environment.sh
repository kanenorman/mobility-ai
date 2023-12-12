#!/bin/bash

# Stop all running Docker containers if any exist
if [ $(docker ps -q | wc -l) -gt 0 ]; then
    docker stop $(docker ps -aq)
fi

# Remove all Docker containers if any exist
if [ $(docker ps -aq | wc -l) -gt 0 ]; then
    docker rm $(docker ps -aq)
fi

# Forcefully remove all Docker images if any exist
if [ $(docker images -q | wc -l) -gt 0 ]; then
    docker rmi -f $(docker images -q)
fi

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete

# Optional: Reset Minikube (removes all Minikube data and configurations)
rm -rf ~/.minikube

# Optional: Restart Docker service
sudo systemctl restart docker

echo "Environment reset complete."
