#!/bin/bash
set -e

echo "Deploying Bot..."

git pull origin main

docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

echo "Cleaning up..."
docker image prune -f

echo "Deployment successful."