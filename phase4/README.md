# Phase 4: Local Kubernetes Deployment

Deploy the Todo AI Chatbot application to a local Kubernetes cluster (Minikube) using Docker, Helm, and AI-assisted DevOps tools.

## Overview

This phase containerizes the Phase 3 Todo AI Chatbot application (FastAPI backend + Next.js frontend) and deploys it to Minikube using:

- **Docker**: Multi-stage builds for optimized container images
- **Kubernetes**: Deployments, Services, ConfigMaps, and Secrets
- **Helm**: Chart for one-command deployment and configuration
- **AI Tools**: Gordon, kubectl-ai, and kagent for assisted DevOps

## Prerequisites

Ensure the following tools are installed and configured:

| Tool | Required Version | Verify Command |
|------|-----------------|----------------|
| Docker Desktop | 29.1+ | `docker --version` |
| Minikube | 1.38+ | `minikube version` |
| kubectl | 1.34+ | `kubectl version --client` |
| Helm | 3.16+ | `helm version` |
| curl | Any | `curl --version` |

**Optional AI Tools:**
- Gordon (Docker AI) - included in Docker Desktop
- kubectl-ai - `kubectl krew install ai`
- kagent - `kagent version`

## Quick Start

### 1. Start Minikube

```bash
minikube start --driver=docker --cpus=2 --memory=4096
```

### 2. Build Docker Images

```bash
./scripts/build.sh
```

This builds both backend and frontend images and loads them into Minikube.

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values:
# - DATABASE_URL: Your Neon PostgreSQL connection string
# - GROQ_API_KEY: Your Groq AI API key
# - BETTER_AUTH_SECRET: Your JWT secret (same as Phase 3)
```

### 4. Deploy to Kubernetes

```bash
./scripts/deploy.sh
```

### 5. Verify Deployment

```bash
./scripts/test.sh
```

### 6. Access the Application

- **Frontend**: http://localhost:30080
- **Backend API**: http://localhost:30800
- **API Documentation**: http://localhost:30800/docs
- **Health Check**: http://localhost:30800/api/health

## Project Structure

```
phase4/
├── backend/                 # FastAPI backend application
│   ├── Dockerfile          # Multi-stage Docker build
│   └── .dockerignore       # Excluded files
├── frontend/               # Next.js frontend application
│   ├── Dockerfile          # Multi-stage Docker build
│   └── .dockerignore       # Excluded files
├── kubernetes/             # Raw Kubernetes manifests
│   ├── configmap.yaml      # Non-sensitive configuration
│   ├── secret.yaml.example # Secret template
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   └── frontend-service.yaml
├── helm/                   # Helm chart
│   └── todo-chatbot/
│       ├── Chart.yaml      # Chart metadata
│       ├── values.yaml     # Default values
│       └── templates/      # Kubernetes templates
├── scripts/                # Automation scripts
│   ├── build.sh           # Build Docker images
│   ├── deploy.sh          # Deploy with Helm
│   ├── cleanup.sh         # Remove deployment
│   └── test.sh            # Verify deployment
└── docs/
    ├── README.md          # This file
    ├── TROUBLESHOOTING.md # Common issues
    └── AI_TOOLS_USAGE.md  # AI tools documentation
```

## Deployment Methods

### Method 1: Using Scripts (Recommended)

```bash
# Build images
./scripts/build.sh

# Deploy
./scripts/deploy.sh

# Test
./scripts/test.sh

# Cleanup
./scripts/cleanup.sh
```

### Method 2: Using Helm Directly

```bash
# Build and load images first
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest --build-arg NEXT_PUBLIC_API_URL=http://localhost:30800 ./frontend
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# Install with Helm
helm install todo-chatbot ./helm/todo-chatbot \
  --set secrets.databaseUrl="$DATABASE_URL" \
  --set secrets.groqApiKey="$GROQ_API_KEY" \
  --set secrets.betterAuthSecret="$BETTER_AUTH_SECRET"

# Upgrade existing deployment
helm upgrade todo-chatbot ./helm/todo-chatbot --reuse-values

# Uninstall
helm uninstall todo-chatbot
```

### Method 3: Using Raw Kubernetes Manifests

```bash
# Create secret from template
kubectl apply -f kubernetes/configmap.yaml
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="$DATABASE_URL" \
  --from-literal=GROQ_API_KEY="$GROQ_API_KEY" \
  --from-literal=BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET"

# Apply deployments and services
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-service.yaml
kubectl apply -f kubernetes/frontend-deployment.yaml
kubectl apply -f kubernetes/frontend-service.yaml
```

## Configuration

### Environment Variables

| Variable | Description | Source |
|----------|-------------|--------|
| DATABASE_URL | Neon PostgreSQL connection string | Secret |
| GROQ_API_KEY | Groq AI API key | Secret |
| BETTER_AUTH_SECRET | JWT signing secret | Secret |
| ALLOWED_ORIGINS | CORS allowed origins | ConfigMap |
| NEXT_PUBLIC_API_URL | Backend API URL for frontend | ConfigMap |

### Helm Values

Customize deployment in `helm/todo-chatbot/values.yaml`:

```yaml
backend:
  replicas: 2           # Number of backend pods
  resources:
    limits:
      cpu: 1000m
      memory: 512Mi

frontend:
  replicas: 2           # Number of frontend pods
  resources:
    limits:
      cpu: 500m
      memory: 256Mi
```

### Scaling

```bash
# Scale backend
kubectl scale deployment todo-chatbot-backend --replicas=3

# Scale frontend
kubectl scale deployment todo-chatbot-frontend --replicas=3

# Or modify values.yaml and upgrade
helm upgrade todo-chatbot ./helm/todo-chatbot --set backend.replicas=3
```

## Monitoring and Debugging

### Check Pod Status

```bash
kubectl get pods -l app.kubernetes.io/name=todo-chatbot
```

### View Logs

```bash
# Backend logs
kubectl logs -l app.kubernetes.io/component=backend -f

# Frontend logs
kubectl logs -l app.kubernetes.io/component=frontend -f
```

### Describe Resources

```bash
# Check deployment details
kubectl describe deployment todo-chatbot-backend
kubectl describe deployment todo-chatbot-frontend

# Check service details
kubectl describe service todo-chatbot-backend
kubectl describe service todo-chatbot-frontend
```

### Access Pod Shell

```bash
# Backend
kubectl exec -it $(kubectl get pod -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}') -- /bin/bash

# Frontend
kubectl exec -it $(kubectl get pod -l app.kubernetes.io/component=frontend -o jsonpath='{.items[0].metadata.name}') -- /bin/sh
```

## AI Tools Integration

See [AI_TOOLS_USAGE.md](AI_TOOLS_USAGE.md) for detailed examples of:

- **Gordon** (Docker AI): Dockerfile optimization and debugging
- **kubectl-ai**: Natural language Kubernetes commands
- **kagent**: Cluster monitoring and recommendations

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common issues:

- Pod not starting (CrashLoopBackOff)
- Image pull errors
- Network connectivity issues
- Database connection problems

## Cleanup

```bash
# Using script
./scripts/cleanup.sh

# Manual cleanup
helm uninstall todo-chatbot
kubectl delete configmap todo-config
kubectl delete secret todo-secrets
```

## Success Criteria

- [ ] Docker images build successfully (< 5 minutes)
- [ ] Backend image < 500MB, Frontend image < 300MB
- [ ] All 4 pods reach Running status (< 2 minutes)
- [ ] Pods stable for 5+ minutes (no restarts)
- [ ] Frontend loads in < 3 seconds
- [ ] Backend health check responds in < 500ms
- [ ] Full user journey works (login -> tasks -> AI chat)
- [ ] `helm lint` passes
- [ ] `helm install/uninstall` clean
- [ ] 9+ AI tool examples documented

## Architecture

```
                    ┌─────────────────────────────────────┐
                    │           Minikube Cluster          │
                    │                                     │
User ───────────────┤  ┌───────────────────────────────┐  │
http://localhost:   │  │     Frontend (NodePort:30080) │  │
    30080           │  │  ┌─────────┐   ┌─────────┐    │  │
                    │  │  │ Pod 1   │   │ Pod 2   │    │  │
                    │  │  │ Next.js │   │ Next.js │    │  │
                    │  │  └────┬────┘   └────┬────┘    │  │
                    │  └───────┼─────────────┼─────────┘  │
                    │          │             │            │
                    │  ┌───────┼─────────────┼─────────┐  │
                    │  │     Backend (NodePort:30800)  │  │
User ───────────────┤  │  ┌────▼────┐   ┌────▼────┐    │  │
http://localhost:   │  │  │ Pod 1   │   │ Pod 2   │    │  │
    30800           │  │  │ FastAPI │   │ FastAPI │    │  │
                    │  │  └────┬────┘   └────┬────┘    │  │
                    │  └───────┼─────────────┼─────────┘  │
                    │          │             │            │
                    └──────────┼─────────────┼────────────┘
                               │             │
                               └──────┬──────┘
                                      │
                               ┌──────▼──────┐
                               │    Neon     │
                               │ PostgreSQL  │
                               │   (Cloud)   │
                               └─────────────┘
```

## License

Part of the Q4 Gemini CLI Hackathon Phase 4 project.
