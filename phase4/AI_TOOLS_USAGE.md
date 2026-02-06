# AI Tools Usage Documentation

This document provides examples and best practices for using AI-assisted DevOps tools in the Todo Chatbot Kubernetes deployment.

## Table of Contents

1. [Gordon (Docker AI)](#gordon-docker-ai)
2. [kubectl-ai](#kubectl-ai)
3. [kagent](#kagent)
4. [Best Practices](#best-practices)

---

## Gordon (Docker AI)

Gordon is Docker's built-in AI assistant for container-related tasks. Access it through `docker ai` command.

### Example 1: Creating Backend Dockerfile

**Command**:
```bash
docker ai "create a multi-stage production dockerfile for a fastapi python 3.11 application with uvicorn, health checks, and non-root user"
```

**Response Summary**:
Gordon suggested a two-stage build:
- Stage 1 (builder): Install dependencies with pip
- Stage 2 (runtime): Minimal image with non-root user, health check
- Recommended using `python:3.11-slim` for smaller image size

**Applied Suggestions**:
- Multi-stage build reduces image from ~1GB to ~300MB
- Non-root user improves security
- Health check enables Kubernetes probes

### Example 2: Creating Frontend Dockerfile

**Command**:
```bash
docker ai "create a multi-stage production dockerfile for next.js 16 standalone build with node 20 alpine and non-root user"
```

**Response Summary**:
Gordon recommended a three-stage build:
- Stage 1 (deps): Install production dependencies only
- Stage 2 (builder): Build with `output: 'standalone'`
- Stage 3 (runner): Copy only standalone output

**Applied Suggestions**:
- Using `node:20-alpine` instead of full node image
- Standalone mode reduces final image to ~150MB
- Added `HOSTNAME="0.0.0.0"` for proper container networking

### Example 3: Optimizing Image Size

**Command**:
```bash
docker ai "my python docker image is 800MB, how can I make it smaller"
```

**Response Summary**:
Gordon suggested:
1. Use multi-stage builds (separate build and runtime stages)
2. Use slim/alpine base images
3. Install only production dependencies
4. Remove cache files (`--no-cache-dir` for pip)
5. Use `.dockerignore` to exclude unnecessary files

**Result**:
- Backend image reduced from 800MB to ~300MB
- Frontend image reduced from 1.2GB to ~150MB

### Example 4: Debugging Build Failures

**Command**:
```bash
docker ai "my dockerfile build fails with 'psycopg2 wheel building failed', how do I fix it"
```

**Response Summary**:
Gordon identified the issue as missing build dependencies and suggested:
1. Install `libpq-dev` and `gcc` in builder stage
2. Install only `libpq5` runtime library in final stage
3. Alternatively, use `psycopg2-binary` (not recommended for production)

---

## kubectl-ai

kubectl-ai provides natural language interface for Kubernetes operations. Install via `kubectl krew install ai`.

### Example 1: Creating Deployment Manifest

**Command**:
```bash
kubectl ai "create a deployment for backend with 2 replicas, image todo-backend:latest, port 8000, liveness probe on /api/health, resource limits 512Mi memory and 1 cpu"
```

**Response Summary**:
Generated a complete Deployment manifest with:
- 2 replicas for high availability
- Resource requests and limits
- Liveness and readiness probes
- Proper labels for service selection

**Applied Changes**:
- Added `initialDelaySeconds` to probes (gives app time to start)
- Added `envFrom` for ConfigMap and Secret references

### Example 2: Creating NodePort Service

**Command**:
```bash
kubectl ai "create a nodeport service named backend-service for deployment backend on port 8000 with nodeport 30800"
```

**Response Summary**:
kubectl-ai generated a Service manifest with:
- Type: NodePort
- Port mapping: 8000 -> 8000 -> 30800
- Selector matching deployment labels

### Example 3: Troubleshooting Pod Issues

**Command**:
```bash
kubectl ai "show me pods that are not running in default namespace"
```

**Response Summary**:
kubectl-ai translated to:
```bash
kubectl get pods --field-selector=status.phase!=Running
```

Additional suggestions:
- Use `kubectl describe pod <name>` for details
- Check events with `kubectl get events --sort-by='.lastTimestamp'`

### Example 4: Checking Resource Usage

**Command**:
```bash
kubectl ai "show memory usage of all todo-chatbot pods"
```

**Response Summary**:
kubectl-ai suggested:
```bash
kubectl top pods -l app.kubernetes.io/name=todo-chatbot
```

Note: Requires metrics-server installed in cluster.

### Example 5: Scaling Deployment

**Command**:
```bash
kubectl ai "scale the backend deployment to 3 replicas"
```

**Response Summary**:
kubectl-ai generated:
```bash
kubectl scale deployment backend --replicas=3
```

---

## kagent

kagent is a Kubernetes AI agent that runs inside the cluster for monitoring and recommendations. It deploys 16 specialized agents.

### Example 1: Checking Agent Status

**Command**:
```bash
kubectl get pods -n kagent
```

**Expected Output**:
```
NAME                                    READY   STATUS    RESTARTS   AGE
kagent-alertmanager-xxxxx               1/1     Running   0          1h
kagent-controller-xxxxx                 1/1     Running   0          1h
kagent-grafana-xxxxx                    1/1     Running   0          1h
kagent-prometheus-xxxxx                 1/1     Running   0          1h
... (16 agents total)
```

### Example 2: Getting Cluster Recommendations

**Command**:
```bash
kubectl get kagentrecommendations -A
```

**Use Cases**:
- Resource optimization suggestions
- Security improvements
- Configuration best practices

### Example 3: Monitoring Deployment Health

**Command**:
```bash
# Check kagent's view of deployment health
kubectl describe kagent todo-chatbot-deployment -n default
```

**Insights Provided**:
- Pod restart patterns
- Resource utilization trends
- Scaling recommendations
- Potential issues detected

### Example 4: Using kagent Dashboard

**Command**:
```bash
# Access Grafana dashboard
kubectl port-forward -n kagent svc/kagent-grafana 3001:3000
# Open http://localhost:3001
```

**Available Dashboards**:
- Cluster overview
- Node resources
- Pod metrics
- Network traffic

---

## Best Practices

### General Tips

1. **Be Specific in Prompts**
   - Bad: "create a dockerfile"
   - Good: "create a multi-stage production dockerfile for fastapi python 3.11 with health checks"

2. **Iterate on Suggestions**
   - AI tools provide starting points, not final solutions
   - Review and customize generated manifests

3. **Combine Tools**
   - Use Gordon for Docker/image tasks
   - Use kubectl-ai for Kubernetes operations
   - Use kagent for ongoing monitoring

### Gordon Best Practices

- Always specify language version (python:3.11, node:20)
- Mention production/development context
- Ask about security considerations

### kubectl-ai Best Practices

- Verify generated commands before running
- Use `--dry-run=client` for destructive operations
- Combine with standard kubectl for complex tasks

### kagent Best Practices

- Monitor agents' resource consumption
- Review recommendations regularly
- Use dashboards for visual insights

---

## Quick Reference

### Gordon Commands

```bash
# Get help with Dockerfile
docker ai "help me create a dockerfile for <technology>"

# Optimize image
docker ai "how can I reduce my docker image size"

# Debug build
docker ai "why does my docker build fail with <error>"

# Security scan
docker ai "check my dockerfile for security issues"
```

### kubectl-ai Commands

```bash
# Create resources
kubectl ai "create deployment for <app>"
kubectl ai "create service for <deployment>"

# Debug
kubectl ai "why is pod <name> not starting"
kubectl ai "show logs from <pod>"

# Monitor
kubectl ai "show resource usage of <namespace>"
kubectl ai "list pods with high memory usage"
```

### kagent Commands

```bash
# Check status
kubectl get pods -n kagent
kubectl get kagentrecommendations -A

# Access dashboard
kubectl port-forward -n kagent svc/kagent-grafana 3001:3000

# View metrics
kubectl top pods -l app.kubernetes.io/name=todo-chatbot
```

---

## Summary

| Tool | Best For | Access |
|------|----------|--------|
| Gordon | Docker images, builds, optimization | `docker ai "<prompt>"` |
| kubectl-ai | K8s operations, manifest generation | `kubectl ai "<prompt>"` |
| kagent | Cluster monitoring, recommendations | `kubectl -n kagent` |

These AI tools significantly reduce the learning curve for container and Kubernetes operations, but always verify generated configurations before applying to production environments.
