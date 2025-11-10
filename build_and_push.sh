#!/bin/bash

# This script assumes it is run on the host machine where the docker command works
DOCKER_HUB_ID="$1"
IMAGE_NAME="$2"
IMAGE_TAG="$3"
DOCKER_USER="$4"
DOCKER_PASSWORD="$5"

# 1. Build and Tag
echo "Building final Docker image: ${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG}"
docker build -t "${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG}" .
docker tag "${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG}" "${DOCKER_HUB_ID}/${IMAGE_NAME}:latest"

# 2. Log in and Push
echo "Pushing image to Docker Hub..."
echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USER}" --password-stdin

docker push "${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG}"
docker push "${DOCKER_HUB_ID}/${IMAGE_NAME}:latest"

# 3. Deployment (Assumes kubectl is also on the host)
echo "Applying Kubernetes deployment..."
sed -i "s|LATEST_TAG_TO_BE_REPLACED|${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG}|g" k8s/deployment.yaml

kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/deployment.yaml

sed -i "s|${DOCKER_HUB_ID}/${IMAGE_NAME}:${IMAGE_TAG}|LATEST_TAG_TO_BE_REPLACED|g" k8s/deployment.yaml

echo "Deployment complete."