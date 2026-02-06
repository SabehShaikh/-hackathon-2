#!/bin/bash
# Phase 4: Deploy Todo Chatbot to Minikube
# Deploys the application using Helm

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=============================================="
echo "Deploying Todo Chatbot to Minikube"
echo "=============================================="

cd "$PROJECT_ROOT"

# Check Minikube status
echo ""
echo "1. Checking Minikube status..."
if ! minikube status | grep -q "Running"; then
  echo "ERROR: Minikube is not running."
  echo "   Start with: minikube start --driver=docker --cpus=2 --memory=4096"
  exit 1
fi
echo "   Minikube is running"

# Check for .env file
echo ""
echo "2. Checking environment configuration..."
if [ ! -f .env ]; then
  echo "ERROR: .env file not found."
  echo "   Copy .env.example to .env and fill in your values:"
  echo "     cp .env.example .env"
  echo "   Required variables: DATABASE_URL, GROQ_API_KEY, BETTER_AUTH_SECRET"
  exit 1
fi
echo "   .env file found"

# Load environment variables
source .env

# Validate required variables
if [ -z "$DATABASE_URL" ] || [ -z "$GROQ_API_KEY" ] || [ -z "$BETTER_AUTH_SECRET" ]; then
  echo "ERROR: Missing required environment variables."
  echo "   Ensure DATABASE_URL, GROQ_API_KEY, and BETTER_AUTH_SECRET are set in .env"
  exit 1
fi
echo "   Environment variables loaded"

# Install/upgrade with Helm
echo ""
echo "3. Installing with Helm..."
helm upgrade --install todo-chatbot ./helm/todo-chatbot \
  --set secrets.databaseUrl="$DATABASE_URL" \
  --set secrets.groqApiKey="$GROQ_API_KEY" \
  --set secrets.betterAuthSecret="$BETTER_AUTH_SECRET"

# Wait for pods to be ready
echo ""
echo "4. Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod \
  -l app.kubernetes.io/name=todo-chatbot \
  --timeout=120s || {
    echo "WARNING: Some pods may not be ready yet."
    echo "   Check status with: kubectl get pods -l app.kubernetes.io/name=todo-chatbot"
  }

# Show deployment status
echo ""
echo "=============================================="
echo "Deployment Status"
echo "=============================================="
kubectl get pods -l app.kubernetes.io/name=todo-chatbot
echo ""
kubectl get services -l app.kubernetes.io/name=todo-chatbot

echo ""
echo "=============================================="
echo "Deployment Complete!"
echo "=============================================="
echo ""
echo "Access the application:"
echo "  Frontend: http://localhost:30080"
echo "  Backend:  http://localhost:30800"
echo "  Health:   http://localhost:30800/api/health"
echo "  API Docs: http://localhost:30800/docs"
