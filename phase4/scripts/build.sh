#!/bin/bash
# Phase 4: Build Docker Images
# Builds backend and frontend images and loads them into Minikube

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=============================================="
echo "Building Todo Chatbot Docker Images"
echo "=============================================="

cd "$PROJECT_ROOT"

# Build backend image
echo ""
echo "1. Building backend image..."
docker build -t todo-backend:latest ./backend
echo "   Backend image built successfully"

# Build frontend image
echo ""
echo "2. Building frontend image..."
docker build -t todo-frontend:latest \
  --build-arg NEXT_PUBLIC_API_URL=http://localhost:30800 \
  ./frontend
echo "   Frontend image built successfully"

# Display image sizes
echo ""
echo "=============================================="
echo "Image Sizes"
echo "=============================================="
docker images | grep -E "REPOSITORY|todo-"

# Check if Minikube is running
echo ""
echo "=============================================="
echo "Loading Images into Minikube"
echo "=============================================="

if minikube status | grep -q "Running"; then
  echo "3. Loading backend image into Minikube..."
  minikube image load todo-backend:latest
  echo "   Backend image loaded"

  echo ""
  echo "4. Loading frontend image into Minikube..."
  minikube image load todo-frontend:latest
  echo "   Frontend image loaded"

  echo ""
  echo "Verifying images in Minikube..."
  minikube image ls | grep todo || echo "   Images loaded successfully"
else
  echo "WARNING: Minikube is not running."
  echo "   Start Minikube with: minikube start"
  echo "   Then load images with:"
  echo "     minikube image load todo-backend:latest"
  echo "     minikube image load todo-frontend:latest"
fi

echo ""
echo "=============================================="
echo "Build Complete!"
echo "=============================================="
