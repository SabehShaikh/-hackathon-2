# Feature Specification: Local Kubernetes Deployment

**Feature Branch**: `001-kubernetes-deployment`
**Created**: 2025-02-04
**Status**: Draft
**Input**: User description: "Containerize Phase 3 Todo Chatbot and deploy to local Kubernetes (Minikube) using Docker, Helm, and AI-assisted DevOps tools"

---

## Overview

Containerize the Phase 3 Todo AI Chatbot application and deploy it to a local Kubernetes cluster (Minikube) using Docker, Helm, and AI-assisted DevOps tools (Gordon, kubectl-ai, kagent). This demonstrates cloud-native deployment practices without modifying the application functionality.

**Source Application**: `../phase3/` (FastAPI backend + Next.js 16 frontend)
**Target Environment**: Minikube with Docker driver
**Database**: Neon PostgreSQL (external, cloud-hosted - not containerized)

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Docker Image Creation (Priority: P1)

As a DevOps engineer, I want to create optimized Docker images for both frontend and backend so that they can run reliably in any container environment.

**Why this priority**: Foundation for all subsequent Kubernetes deployment. Without working container images, nothing else can proceed.

**Independent Test**: Build images and run them locally with `docker run`. If both containers start and respond to health checks, this story is complete.

**Acceptance Scenarios**:

1. **Given** Phase 3 backend source code at `../phase3/backend/`, **When** I run `docker build -t todo-backend:latest ./backend`, **Then** the build completes successfully with exit code 0 and image size is under 500MB.

2. **Given** Phase 3 frontend source code at `../phase3/frontend/`, **When** I run `docker build -t todo-frontend:latest ./frontend`, **Then** the build completes successfully with exit code 0 and image size is under 300MB.

3. **Given** a built backend image, **When** I run `docker run -p 8000:8000 todo-backend:latest`, **Then** the container starts and `/api/health` returns HTTP 200.

4. **Given** a built frontend image, **When** I run `docker run -p 3000:3000 todo-frontend:latest`, **Then** the container starts and responds on port 3000.

5. **Given** both Dockerfiles, **When** I inspect them, **Then** they use multi-stage builds, run as non-root user, and include health checks.

---

### User Story 2 - Kubernetes Deployment (Priority: P1)

As a DevOps engineer, I want to deploy the application to Minikube so that it runs in a production-like Kubernetes environment with high availability.

**Why this priority**: Core objective of Phase 4. Must work for the project to be considered successful.

**Independent Test**: Run `kubectl apply -f kubernetes/` and verify all pods reach Running status with `kubectl get pods`.

**Acceptance Scenarios**:

1. **Given** Docker images loaded into Minikube, **When** I apply Kubernetes manifests, **Then** backend deployment creates 2 replicas.

2. **Given** Docker images loaded into Minikube, **When** I apply Kubernetes manifests, **Then** frontend deployment creates 2 replicas.

3. **Given** deployed pods, **When** I run `kubectl get pods`, **Then** all 4 pods show status "Running" within 2 minutes.

4. **Given** running pods, **When** I wait 5 minutes, **Then** all pods remain in "Running" status (no CrashLoopBackOff).

5. **Given** a running backend pod, **When** I run `kubectl delete pod <backend-pod>`, **Then** Kubernetes automatically creates a replacement pod within 30 seconds.

---

### User Story 3 - Service Exposure (Priority: P1)

As a user, I want to access the application via web browser so that I can use the todo app locally through Kubernetes services.

**Why this priority**: User-facing requirement. Application must be accessible to demonstrate success.

**Independent Test**: Access `http://localhost:30080` in browser and see the frontend. Access `http://localhost:30800/api/health` and get JSON response.

**Acceptance Scenarios**:

1. **Given** deployed services, **When** I access `http://localhost:30080`, **Then** the frontend loads successfully (or via `minikube service frontend-service --url`).

2. **Given** deployed services, **When** I access `http://localhost:30800/api/health`, **Then** I receive a JSON health response with status "healthy".

3. **Given** frontend and backend services running, **When** frontend makes API request, **Then** backend responds correctly (CORS configured).

4. **Given** service manifests, **When** I inspect them, **Then** frontend uses NodePort 30080 and backend uses NodePort 30800.

---

### User Story 4 - Configuration Management (Priority: P2)

As a DevOps engineer, I want to manage configuration securely so that sensitive data is protected and configuration is externalized.

**Why this priority**: Important for security and maintainability, but can work with hardcoded values initially.

**Independent Test**: Verify ConfigMaps and Secrets exist with `kubectl get configmaps` and `kubectl get secrets`. Verify no secrets in git.

**Acceptance Scenarios**:

1. **Given** Kubernetes manifests, **When** I check for sensitive data, **Then** DATABASE_URL, GROQ_API_KEY, and BETTER_AUTH_SECRET are in Secrets (not ConfigMaps).

2. **Given** Kubernetes manifests, **When** I check for non-sensitive config, **Then** ALLOWED_ORIGINS and NEXT_PUBLIC_API_URL are in ConfigMaps.

3. **Given** the git repository, **When** I check committed files, **Then** no actual secret values are present (only `.env.example` templates).

4. **Given** deployed backend pods, **When** I check environment variables, **Then** DATABASE_URL connects successfully to Neon PostgreSQL.

---

### User Story 5 - Helm Chart Package (Priority: P2)

As a DevOps engineer, I want a Helm chart so that I can deploy, update, and delete the application with single commands.

**Why this priority**: Simplifies deployment workflow and enables repeatable deployments.

**Independent Test**: Run `helm install todo-chatbot ./helm/todo-chatbot` and verify application deploys. Run `helm uninstall todo-chatbot` and verify cleanup.

**Acceptance Scenarios**:

1. **Given** the Helm chart at `./helm/todo-chatbot/`, **When** I run `helm lint ./helm/todo-chatbot`, **Then** the chart passes validation with no errors.

2. **Given** a clean Minikube cluster, **When** I run `helm install todo-chatbot ./helm/todo-chatbot`, **Then** all resources are created and pods reach Running status.

3. **Given** an installed Helm release, **When** I run `helm uninstall todo-chatbot`, **Then** all resources are deleted and `kubectl get all` shows no todo-chatbot resources.

4. **Given** the values.yaml file, **When** I modify `backend.replicas: 3`, **Then** `helm upgrade` scales backend to 3 replicas.

---

### User Story 6 - AI Tools Integration (Priority: P3)

As a DevOps engineer, I want to use AI tools (Gordon, kubectl-ai, kagent) for assistance so that deployment follows best practices and is easier to manage.

**Why this priority**: Enhances workflow but not required for core functionality.

**Independent Test**: Document at least 3 uses of each AI tool in AI_TOOLS_USAGE.md with actual commands and outputs.

**Acceptance Scenarios**:

1. **Given** Docker Desktop with Gordon enabled, **When** I use `docker ai "optimize my backend Dockerfile"`, **Then** Gordon provides actionable suggestions (documented).

2. **Given** kubectl-ai installed, **When** I use `kubectl ai "show me pods that are not running"`, **Then** kubectl-ai generates and executes appropriate commands (documented).

3. **Given** kagent deployed in cluster, **When** I run `kubectl get pods -n kagent`, **Then** all 16 agent pods show Running status.

4. **Given** AI tool usage, **When** I check AI_TOOLS_USAGE.md, **Then** it contains at least 3 documented examples for each tool (Gordon, kubectl-ai, kagent).

---

### User Story 7 - Application Functionality (Priority: P1)

As a user, I want the todo app to work exactly like Phase 3 so that all features are available in the Kubernetes deployment.

**Why this priority**: Validates that containerization preserved functionality. Critical for success.

**Independent Test**: Complete full user journey: login → view dashboard → add task → use AI chat → logout.

**Acceptance Scenarios**:

1. **Given** deployed application, **When** I navigate to `/login` and enter valid credentials, **Then** authentication succeeds and redirects to dashboard.

2. **Given** logged-in user, **When** I view dashboard, **Then** existing tasks are displayed correctly.

3. **Given** logged-in user on dashboard, **When** I add a new task, **Then** task is created and persisted to Neon database.

4. **Given** logged-in user, **When** I navigate to `/chat` and send "show my tasks", **Then** AI responds with task list.

5. **Given** AI chat interface, **When** I send "add task: test kubernetes deployment", **Then** AI confirms task creation and task appears in dashboard.

---

### User Story 8 - Documentation (Priority: P2)

As a developer, I want clear documentation so that I can deploy and troubleshoot the application independently.

**Why this priority**: Essential for reproducibility and handoff, but can be created after implementation.

**Independent Test**: New developer can follow README.md to deploy application from scratch without additional assistance.

**Acceptance Scenarios**:

1. **Given** README.md, **When** I follow the deployment instructions, **Then** application deploys successfully.

2. **Given** TROUBLESHOOTING.md, **When** I encounter a common error, **Then** I find the solution documented.

3. **Given** documentation, **When** I search for prerequisites, **Then** all required tools and versions are listed.

4. **Given** AI_TOOLS_USAGE.md, **When** I want to use Gordon/kubectl-ai/kagent, **Then** I find working example commands.

---

### Edge Cases

1. **Database Connection Failure**: Backend should log connection errors clearly; health check should report database status; pod should not crash but may be marked unhealthy.

2. **Missing Environment Variables**: Container should fail fast with clear error message indicating which variable is missing.

3. **Port Conflicts**: Document how to change NodePort values in values.yaml if 30080/30800 are occupied.

4. **Image Build Failures**: Dockerfile should fail with actionable error; most common issues documented in TROUBLESHOOTING.md.

5. **Minikube Resource Exhaustion**: Document minimum resource requirements (2 CPUs, 4GB RAM); include resource limits to prevent individual pods from consuming all resources.

6. **Helm Release Conflicts**: `helm install` fails if release exists; document use of `helm upgrade --install` for idempotent deployments.

7. **Network Connectivity**: Frontend must reach backend via internal Kubernetes DNS or NodePort; CORS must allow frontend origin.

---

## Requirements *(mandatory)*

### Functional Requirements

**Docker Images**:
- **FR-001**: System MUST build backend Docker image from `../phase3/backend/` source code.
- **FR-002**: System MUST build frontend Docker image from `../phase3/frontend/` source code.
- **FR-003**: Backend image MUST use multi-stage build with `python:3.11-slim` base.
- **FR-004**: Frontend image MUST use multi-stage build with `node:20-alpine` base.
- **FR-005**: Both images MUST run as non-root user for security.
- **FR-006**: Both images MUST include HEALTHCHECK instructions or rely on Kubernetes probes.
- **FR-007**: Backend image size MUST be under 500MB.
- **FR-008**: Frontend image size MUST be under 300MB.

**Kubernetes Manifests**:
- **FR-009**: System MUST create Deployment manifests for backend and frontend.
- **FR-010**: Each Deployment MUST specify 2 replicas for high availability.
- **FR-011**: System MUST create Service manifests with NodePort type.
- **FR-012**: Frontend service MUST expose NodePort 30080.
- **FR-013**: Backend service MUST expose NodePort 30800.
- **FR-014**: System MUST create ConfigMap for non-sensitive configuration.
- **FR-015**: System MUST create Secret for sensitive credentials (DATABASE_URL, GROQ_API_KEY, BETTER_AUTH_SECRET).
- **FR-016**: All Deployments MUST define resource requests and limits.
- **FR-017**: All Deployments MUST define liveness and readiness probes.

**Helm Chart**:
- **FR-018**: System MUST provide Helm chart at `helm/todo-chatbot/`.
- **FR-019**: Chart MUST include Chart.yaml with version 1.0.0.
- **FR-020**: Chart MUST include values.yaml with configurable replicas, images, and resources.
- **FR-021**: Chart MUST template all Kubernetes manifests.
- **FR-022**: Chart MUST include NOTES.txt with post-install instructions.
- **FR-023**: Chart MUST pass `helm lint` validation.

**Configuration**:
- **FR-024**: Backend MUST receive DATABASE_URL from Kubernetes Secret.
- **FR-025**: Backend MUST receive GROQ_API_KEY from Kubernetes Secret.
- **FR-026**: Backend MUST receive BETTER_AUTH_SECRET from Kubernetes Secret.
- **FR-027**: Backend MUST receive ALLOWED_ORIGINS from ConfigMap (value: `http://localhost:30080`).
- **FR-028**: Frontend MUST receive NEXT_PUBLIC_API_URL from build args or ConfigMap (value: `http://localhost:30800`).

**Documentation**:
- **FR-029**: System MUST provide README.md with complete deployment instructions.
- **FR-030**: System MUST provide TROUBLESHOOTING.md with common issues and solutions.
- **FR-031**: System MUST provide AI_TOOLS_USAGE.md documenting Gordon, kubectl-ai, and kagent usage.

### Key Entities

- **Docker Image**: Container image built from application source, contains runtime and dependencies, tagged with version.
- **Deployment**: Kubernetes resource managing pod replicas, defines container spec, resources, probes.
- **Service**: Kubernetes resource exposing pods, routes traffic via NodePort to pod containers.
- **ConfigMap**: Kubernetes resource storing non-sensitive configuration as key-value pairs.
- **Secret**: Kubernetes resource storing sensitive data, base64-encoded, mounted as environment variables.
- **Helm Chart**: Package containing templated Kubernetes manifests, values file, and metadata.
- **Helm Release**: Installed instance of a Helm chart with specific values.

---

## Technical Specifications

### Docker Configuration

**Backend Dockerfile** (`backend/Dockerfile`):
```dockerfile
# Stage 1: Build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
RUN useradd -m -u 1000 appuser
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile** (`frontend/Dockerfile`):
```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ARG NEXT_PUBLIC_API_URL=http://localhost:30800
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
RUN npm run build

# Stage 3: Runtime
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
ENV PORT=3000
CMD ["node", "server.js"]
```

**Note**: Frontend requires `output: 'standalone'` in `next.config.ts` for minimal production image.

### Kubernetes Resource Specifications

**Labels** (consistent across all resources):
```yaml
labels:
  app.kubernetes.io/name: todo-chatbot
  app.kubernetes.io/component: frontend|backend
  app.kubernetes.io/version: "1.0.0"
  app.kubernetes.io/managed-by: helm
```

**Resource Limits**:
| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Backend   | 250m        | 1000m     | 256Mi          | 512Mi        |
| Frontend  | 100m        | 500m      | 128Mi          | 256Mi        |

**Probes**:
- Backend: HTTP GET `/api/health` on port 8000
- Frontend: HTTP GET `/` on port 3000
- Initial delay: 10s, Period: 30s, Timeout: 10s, Failure threshold: 3

### Helm Chart Structure

```
helm/todo-chatbot/
├── Chart.yaml              # name: todo-chatbot, version: 1.0.0, appVersion: 1.0.0
├── values.yaml             # Configurable values
├── .helmignore             # Files to exclude
└── templates/
    ├── _helpers.tpl        # Template helpers (labels, names)
    ├── backend-deployment.yaml
    ├── backend-service.yaml
    ├── frontend-deployment.yaml
    ├── frontend-service.yaml
    ├── configmap.yaml
    ├── secret.yaml
    └── NOTES.txt           # Post-install instructions
```

**values.yaml Structure**:
```yaml
backend:
  replicas: 2
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: NodePort
    port: 8000
    nodePort: 30800
  resources:
    requests: { cpu: 250m, memory: 256Mi }
    limits: { cpu: 1000m, memory: 512Mi }

frontend:
  replicas: 2
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: NodePort
    port: 3000
    nodePort: 30080
  resources:
    requests: { cpu: 100m, memory: 128Mi }
    limits: { cpu: 500m, memory: 256Mi }

config:
  allowedOrigins: "http://localhost:30080"
  apiUrl: "http://localhost:30800"

secrets:
  # Base64 encoded - DO NOT commit real values
  databaseUrl: ""
  groqApiKey: ""
  betterAuthSecret: ""
```

### Environment Variables

**Backend Container**:
| Variable | Source | Description |
|----------|--------|-------------|
| DATABASE_URL | Secret | Neon PostgreSQL connection string |
| GROQ_API_KEY | Secret | Groq AI API key |
| BETTER_AUTH_SECRET | Secret | JWT signing secret |
| ALLOWED_ORIGINS | ConfigMap | CORS allowed origins |

**Frontend Container**:
| Variable | Build Arg | Description |
|----------|-----------|-------------|
| NEXT_PUBLIC_API_URL | Build time | Backend API URL for client-side requests |
| BETTER_AUTH_SECRET | ConfigMap | JWT verification secret (if needed at runtime) |

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Both Docker images build successfully in under 5 minutes total.
- **SC-002**: Backend image size is under 500MB (`docker images | grep backend`).
- **SC-003**: Frontend image size is under 300MB (`docker images | grep frontend`).
- **SC-004**: All 4 pods reach Running status within 2 minutes of deployment.
- **SC-005**: Pods remain healthy (no restarts) for 5+ consecutive minutes.
- **SC-006**: Frontend loads in browser within 3 seconds of first request.
- **SC-007**: Backend API responds to health check in under 500ms.
- **SC-008**: User can complete full login → add task → AI chat flow without errors.
- **SC-009**: `helm lint` passes with no errors or warnings.
- **SC-010**: `helm install` and `helm uninstall` complete without errors.
- **SC-011**: AI_TOOLS_USAGE.md contains minimum 9 documented examples (3 per tool).
- **SC-012**: New developer can deploy application using only README.md instructions.

---

## File Structure (Deliverables)

```
phase4/
├── CLAUDE.md                    # Agent instructions
├── README.md                    # Deployment guide
├── TROUBLESHOOTING.md           # Common issues
├── AI_TOOLS_USAGE.md            # AI tools examples
├── .specify/                    # SpecifyPlus artifacts
├── specs/
│   └── 001-kubernetes-deployment/
│       ├── spec.md              # This file
│       ├── plan.md              # Implementation plan
│       └── tasks.md             # Task breakdown
├── history/
│   └── prompts/                 # PHR records
├── backend/
│   ├── Dockerfile               # Multi-stage backend build
│   └── .dockerignore            # Exclude venv, __pycache__, etc.
├── frontend/
│   ├── Dockerfile               # Multi-stage frontend build
│   └── .dockerignore            # Exclude node_modules, .next, etc.
├── kubernetes/
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── configmap.yaml
│   └── secret.yaml
├── helm/
│   └── todo-chatbot/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── .helmignore
│       └── templates/
│           ├── _helpers.tpl
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── frontend-deployment.yaml
│           ├── frontend-service.yaml
│           ├── configmap.yaml
│           ├── secret.yaml
│           └── NOTES.txt
└── scripts/
    ├── build.sh                 # Build Docker images
    ├── deploy.sh                # Deploy with Helm
    ├── cleanup.sh               # Remove deployment
    └── test.sh                  # Verify deployment
```

---

## Dependencies

### External Dependencies
- **Phase 3 Source Code**: `../phase3/backend/` and `../phase3/frontend/`
- **Neon PostgreSQL**: Cloud database with existing schema (users, tasks, conversations, messages)
- **Groq AI API**: API key for AI chat functionality

### Tool Dependencies (All Verified Installed)
- Docker Desktop 29.1.5 with Gordon AI Agent
- Minikube v1.38.0 (docker driver)
- kubectl v1.34.1
- Helm v3.16.4
- kubectl-ai (via krew)
- kagent 0.7.13

### Assumptions
- Minikube is running: `minikube status` shows Running
- Docker daemon is running: `docker ps` works
- Internet available for pulling base images
- Phase 3 code is functional (tested in HuggingFace/Vercel deployment)
- Database schema exists (created during Phase 3)

---

## Out of Scope

- Cloud deployment (AWS EKS, GCP GKE, Azure AKS)
- Production TLS/HTTPS certificates
- Ingress controllers (nginx-ingress, traefik)
- Persistent volumes (application is stateless)
- StatefulSets or DaemonSets
- Monitoring stack (Prometheus, Grafana) - kagent provides basic monitoring
- CI/CD pipelines (GitHub Actions, GitLab CI)
- Multiple environments (dev, staging, production)
- Database containerization (using external Neon)
- Application code changes (containerizing as-is)
- Auto-scaling (HPA) - manual scaling only
