#!/bin/bash
# Phase 4: Cleanup Todo Chatbot Deployment
# Removes all deployed resources

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=============================================="
echo "Cleaning up Todo Chatbot Deployment"
echo "=============================================="

cd "$PROJECT_ROOT"

# Uninstall Helm release
echo ""
echo "1. Uninstalling Helm release..."
if helm list | grep -q todo-chatbot; then
  helm uninstall todo-chatbot
  echo "   Helm release uninstalled"
else
  echo "   No Helm release found"
fi

# Verify cleanup
echo ""
echo "2. Verifying cleanup..."
kubectl get all -l app.kubernetes.io/name=todo-chatbot 2>/dev/null || echo "   All resources removed"

# Ask about removing Docker images
echo ""
echo "=============================================="
echo "Docker Images"
echo "=============================================="
docker images | grep -E "REPOSITORY|todo-" || true

echo ""
read -p "Remove Docker images? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "3. Removing Docker images..."
  docker rmi todo-backend:latest 2>/dev/null || echo "   Backend image not found"
  docker rmi todo-frontend:latest 2>/dev/null || echo "   Frontend image not found"
  echo "   Docker images removed"
else
  echo "   Keeping Docker images"
fi

echo ""
echo "=============================================="
echo "Cleanup Complete!"
echo "=============================================="
