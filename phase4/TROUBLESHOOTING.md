# Troubleshooting Guide

This guide covers common issues when deploying the Todo AI Chatbot to Kubernetes.

## Table of Contents

1. [Pod Issues](#pod-issues)
2. [Image Build Issues](#image-build-issues)
3. [Network Issues](#network-issues)
4. [Database Issues](#database-issues)
5. [Helm Issues](#helm-issues)
6. [Debugging Commands](#debugging-commands)

---

## Pod Issues

### CrashLoopBackOff

**Symptoms**: Pods repeatedly crash and restart.

**Diagnosis**:
```bash
kubectl logs -l app.kubernetes.io/component=backend --previous
kubectl describe pod -l app.kubernetes.io/component=backend
```

**Common Causes & Solutions**:

1. **Missing Environment Variables**
   ```bash
   # Check if secrets are set
   kubectl get secret todo-chatbot-secrets -o yaml

   # Verify deployment has envFrom
   kubectl describe deployment todo-chatbot-backend | grep -A5 "Environment"
   ```

2. **Database Connection Failure**
   - Verify DATABASE_URL is correct
   - Check network connectivity to Neon
   - Ensure database exists and user has permissions

3. **Application Error**
   ```bash
   # View application logs
   kubectl logs -l app.kubernetes.io/component=backend -f
   ```

### ImagePullBackOff

**Symptoms**: Pods stuck in ImagePullBackOff or ErrImagePull.

**Diagnosis**:
```bash
kubectl describe pod -l app.kubernetes.io/component=backend | grep -A10 "Events"
```

**Solutions**:

1. **Image Not Loaded into Minikube**
   ```bash
   # Check images in Minikube
   minikube image ls | grep todo

   # Load images
   minikube image load todo-backend:latest
   minikube image load todo-frontend:latest
   ```

2. **Wrong Image Tag**
   ```bash
   # Verify deployment uses correct tag
   kubectl get deployment todo-chatbot-backend -o jsonpath='{.spec.template.spec.containers[0].image}'
   ```

3. **imagePullPolicy Issue**
   ```bash
   # Should be IfNotPresent for local images
   kubectl get deployment todo-chatbot-backend -o jsonpath='{.spec.template.spec.containers[0].imagePullPolicy}'
   ```

### Pending Pods

**Symptoms**: Pods stuck in Pending state.

**Diagnosis**:
```bash
kubectl describe pod -l app.kubernetes.io/name=todo-chatbot | grep -A10 "Events"
```

**Solutions**:

1. **Insufficient Resources**
   ```bash
   # Check node resources
   kubectl describe node | grep -A10 "Allocated resources"

   # Reduce resource requests in values.yaml
   helm upgrade todo-chatbot ./helm/todo-chatbot \
     --set backend.resources.requests.memory=128Mi \
     --set frontend.resources.requests.memory=64Mi
   ```

2. **Node Not Ready**
   ```bash
   kubectl get nodes
   minikube status
   ```

---

## Image Build Issues

### Docker Daemon Not Running

**Symptoms**: `Cannot connect to the Docker daemon`

**Solutions**:
```bash
# Start Docker Desktop
# On Windows: Open Docker Desktop application
# On Linux:
sudo systemctl start docker
```

### Build Fails - Dependencies

**Backend Build Fails**:
```bash
# Clear Docker cache
docker builder prune -f

# Rebuild without cache
docker build --no-cache -t todo-backend:latest ./backend
```

**Frontend Build Fails**:
```bash
# Check node_modules isn't copied (should be in .dockerignore)
cat frontend/.dockerignore

# Verify standalone output is enabled
grep -r "standalone" frontend/next.config.ts
```

### Image Too Large

**Diagnosis**:
```bash
docker images | grep todo
```

**Solutions**:

1. **Multi-stage Build**
   - Ensure Dockerfile uses multi-stage build
   - Only copy production artifacts

2. **Check .dockerignore**
   ```bash
   # Ensure development files excluded
   cat backend/.dockerignore
   cat frontend/.dockerignore
   ```

3. **Use Smaller Base Images**
   - Backend: `python:3.11-slim` instead of `python:3.11`
   - Frontend: `node:20-alpine` instead of `node:20`

---

## Network Issues

### Cannot Access NodePort

**Symptoms**: http://localhost:30080 doesn't respond

**Diagnosis**:
```bash
# Check service exists
kubectl get svc -l app.kubernetes.io/name=todo-chatbot

# Check NodePort
kubectl get svc todo-chatbot-frontend -o jsonpath='{.spec.ports[0].nodePort}'
```

**Solutions**:

1. **Minikube Tunnel Required** (some configurations)
   ```bash
   # Run in separate terminal
   minikube tunnel
   ```

2. **Use Minikube Service Command**
   ```bash
   minikube service todo-chatbot-frontend --url
   minikube service todo-chatbot-backend --url
   ```

3. **Port Forwarding**
   ```bash
   kubectl port-forward svc/todo-chatbot-frontend 3000:3000 &
   kubectl port-forward svc/todo-chatbot-backend 8000:8000 &
   ```

### CORS Errors

**Symptoms**: Browser console shows CORS errors

**Diagnosis**:
```bash
# Check ALLOWED_ORIGINS
kubectl get configmap todo-chatbot-config -o yaml
```

**Solutions**:

1. **Update ConfigMap**
   ```bash
   helm upgrade todo-chatbot ./helm/todo-chatbot \
     --set config.allowedOrigins="http://localhost:30080,http://127.0.0.1:30080"
   ```

2. **Verify Frontend URL**
   - Ensure you're accessing from the URL in ALLOWED_ORIGINS
   - Don't use IP if only hostname is allowed

### Connection Refused

**Symptoms**: `curl: (7) Failed to connect`

**Diagnosis**:
```bash
# Check pods are running
kubectl get pods -l app.kubernetes.io/name=todo-chatbot

# Check endpoints
kubectl get endpoints
```

**Solutions**:

1. **Wait for Pods to be Ready**
   ```bash
   kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-chatbot --timeout=120s
   ```

2. **Check Readiness Probe**
   ```bash
   kubectl describe pod -l app.kubernetes.io/component=backend | grep -A10 "Readiness"
   ```

---

## Database Issues

### Connection Timeout

**Symptoms**: Backend fails with database connection timeout

**Diagnosis**:
```bash
kubectl logs -l app.kubernetes.io/component=backend | grep -i database
```

**Solutions**:

1. **Verify DATABASE_URL**
   ```bash
   # Check secret exists
   kubectl get secret todo-chatbot-secrets

   # Test connection from pod
   kubectl exec -it $(kubectl get pod -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}') -- python -c "
   import os
   from sqlalchemy import create_engine
   engine = create_engine(os.environ['DATABASE_URL'])
   conn = engine.connect()
   print('Connection successful')
   conn.close()
   "
   ```

2. **Network Policy** (if applicable)
   - Ensure outbound traffic to Neon is allowed

### Authentication Failed

**Symptoms**: `FATAL: password authentication failed`

**Solutions**:

1. **Verify Credentials**
   - Check DATABASE_URL has correct username/password
   - Ensure user exists in Neon database

2. **Re-create Secret**
   ```bash
   helm upgrade todo-chatbot ./helm/todo-chatbot \
     --set secrets.databaseUrl="postgresql://user:pass@host:5432/db"
   ```

---

## Helm Issues

### Release Already Exists

**Symptoms**: `Error: cannot re-use a name that is still in use`

**Solutions**:
```bash
# List releases
helm list

# Uninstall existing
helm uninstall todo-chatbot

# Or use upgrade --install
helm upgrade --install todo-chatbot ./helm/todo-chatbot
```

### Template Rendering Errors

**Symptoms**: Helm install fails with template error

**Diagnosis**:
```bash
# Test template rendering
helm template todo-chatbot ./helm/todo-chatbot --debug
```

**Solutions**:

1. **Validate Chart**
   ```bash
   helm lint ./helm/todo-chatbot
   ```

2. **Check Values**
   ```bash
   # Show computed values
   helm get values todo-chatbot
   ```

### Values Not Applied

**Symptoms**: Deployment doesn't reflect values.yaml changes

**Solutions**:
```bash
# Force upgrade
helm upgrade todo-chatbot ./helm/todo-chatbot --force

# Or delete and reinstall
helm uninstall todo-chatbot
helm install todo-chatbot ./helm/todo-chatbot
```

---

## Debugging Commands

### Quick Status Check

```bash
# Everything at once
kubectl get all -l app.kubernetes.io/name=todo-chatbot
```

### Logs

```bash
# Backend logs
kubectl logs -l app.kubernetes.io/component=backend -f

# Frontend logs
kubectl logs -l app.kubernetes.io/component=frontend -f

# Previous container logs (after crash)
kubectl logs -l app.kubernetes.io/component=backend --previous
```

### Events

```bash
# Cluster events
kubectl get events --sort-by='.lastTimestamp'

# Pod events
kubectl describe pod -l app.kubernetes.io/component=backend | tail -20
```

### Resource Usage

```bash
# Pod resource usage (requires metrics-server)
kubectl top pods -l app.kubernetes.io/name=todo-chatbot

# Node resource usage
kubectl top nodes
```

### Shell Access

```bash
# Backend (bash)
kubectl exec -it $(kubectl get pod -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}') -- /bin/bash

# Frontend (sh - Alpine)
kubectl exec -it $(kubectl get pod -l app.kubernetes.io/component=frontend -o jsonpath='{.items[0].metadata.name}') -- /bin/sh
```

### Network Testing

```bash
# From inside a pod
kubectl exec -it $(kubectl get pod -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}') -- curl -v http://localhost:8000/api/health

# Test service DNS
kubectl exec -it $(kubectl get pod -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}') -- nslookup todo-chatbot-frontend
```

### Helm Debugging

```bash
# Show release info
helm status todo-chatbot

# Show release history
helm history todo-chatbot

# Get rendered templates
helm get manifest todo-chatbot

# Debug template rendering
helm template todo-chatbot ./helm/todo-chatbot --debug
```

---

## Getting Help

If you're still stuck:

1. Check the [README.md](README.md) for setup instructions
2. Review [AI_TOOLS_USAGE.md](AI_TOOLS_USAGE.md) for AI-assisted debugging
3. Use kubectl-ai for natural language troubleshooting:
   ```bash
   kubectl ai "why is my backend pod not starting"
   ```
