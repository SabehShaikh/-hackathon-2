# Implementation Plan: Local Kubernetes Deployment

**Branch**: `001-kubernetes-deployment` | **Date**: 2025-02-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-kubernetes-deployment/spec.md`

---

## Summary

Containerize the Phase 3 Todo AI Chatbot application (FastAPI backend + Next.js frontend) and deploy to a local Minikube Kubernetes cluster using Docker multi-stage builds, Helm charts, and AI-assisted DevOps tools (Gordon, kubectl-ai, kagent). The implementation focuses on demonstrating cloud-native deployment practices while preserving all Phase 3 application functionality.

**Technical Approach**:
1. Copy Phase 3 source code to Phase 4 (backend/, frontend/ directories)
2. Create optimized multi-stage Dockerfiles using Gordon AI for guidance
3. Create Kubernetes manifests using kubectl-ai assistance
4. Package as Helm chart for one-command deployment
5. Document all AI tool usage for educational value

---

## Technical Context

**Language/Version**: Python 3.11 (backend), Node.js 20 (frontend), YAML (K8s manifests)
**Primary Dependencies**: Docker 29.1.5, Minikube 1.38.0, kubectl 1.34.1, Helm 3.16.4
**Storage**: Neon PostgreSQL (external cloud database - not containerized)
**Testing**: Manual integration testing, Helm lint, Docker health checks
**Target Platform**: Local Minikube cluster (Windows with Docker driver)
**Project Type**: Infrastructure/DevOps (containerization of existing web application)
**Performance Goals**: Pod startup < 30s, API response < 500ms, frontend load < 3s
**Constraints**: Backend image < 500MB, frontend image < 300MB, 2 CPU / 4GB RAM cluster
**Scale/Scope**: 4 pods (2 backend, 2 frontend), single namespace, local development only

---

## Constitution Check

*GATE: All principles verified before implementation.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Code Reuse Over Duplication | ✅ | Copy Phase 3 source, no modifications |
| II. AI-First DevOps Workflow | ✅ | Gordon, kubectl-ai, kagent integration planned |
| III. Spec-Driven Development | ✅ | Following constitution → spec → plan → tasks flow |
| IV. Container Best Practices | ✅ | Multi-stage, Alpine, non-root, health checks |
| V. Kubernetes Resource Design | ✅ | Separate manifests, 2 replicas, proper labels |
| VI. Helm Chart Organization | ✅ | Single chart with templated manifests |
| VII. Stateless Architecture | ✅ | External database, no PVs |
| VIII. Local Development Focus | ✅ | Minikube only, NodePort services |
| IX. Production-Ready Practices | ✅ | Health checks, resource limits, logging |
| X. Documentation | ✅ | README, Troubleshooting, AI Tools docs planned |

---

## Project Structure

### Documentation (this feature)

```text
specs/001-kubernetes-deployment/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file - implementation plan
└── tasks.md             # Task breakdown (created by /sp.tasks)
```

### Source Code (repository root)

```text
phase4/
├── CLAUDE.md                    # Agent instructions (exists)
├── .specify/                    # SpecifyPlus artifacts (exists)
│   └── memory/
│       └── constitution.md      # Project constitution (completed)
├── specs/                       # Feature specifications
│   └── 001-kubernetes-deployment/
│       ├── spec.md              # Feature spec (completed)
│       ├── plan.md              # This file
│       └── tasks.md             # Task breakdown
├── history/                     # Prompt history records
│   └── prompts/
│       ├── constitution/
│       └── 001-kubernetes-deployment/
│
├── backend/                     # Backend application (from Phase 3)
│   ├── Dockerfile               # NEW: Multi-stage Docker build
│   ├── .dockerignore            # NEW: Exclude unnecessary files
│   ├── main.py                  # FastAPI application
│   ├── agent.py                 # AI agent with MCP tools
│   ├── mcp_server.py            # MCP tool implementations
│   ├── models.py                # SQLModel entities
│   ├── database.py              # Database connection
│   ├── auth.py                  # Authentication utilities
│   ├── requirements.txt         # Python dependencies
│   ├── routes/                  # API route handlers
│   └── .env.example             # Environment template
│
├── frontend/                    # Frontend application (from Phase 3)
│   ├── Dockerfile               # NEW: Multi-stage Docker build
│   ├── .dockerignore            # NEW: Exclude unnecessary files
│   ├── next.config.ts           # Next.js configuration (modify for standalone)
│   ├── package.json             # Node dependencies
│   ├── app/                     # Next.js App Router pages
│   ├── components/              # React components
│   ├── lib/                     # Utility libraries
│   ├── providers/               # Context providers
│   └── .env.example             # Environment template
│
├── kubernetes/                  # Raw Kubernetes manifests
│   ├── namespace.yaml           # (optional) Namespace definition
│   ├── configmap.yaml           # Non-sensitive configuration
│   ├── secret.yaml.example      # Secret template (actual values not committed)
│   ├── backend-deployment.yaml  # Backend pod specification
│   ├── backend-service.yaml     # Backend NodePort service
│   ├── frontend-deployment.yaml # Frontend pod specification
│   └── frontend-service.yaml    # Frontend NodePort service
│
├── helm/                        # Helm chart package
│   └── todo-chatbot/
│       ├── Chart.yaml           # Chart metadata
│       ├── values.yaml          # Configurable values
│       ├── .helmignore          # Files to exclude from packaging
│       └── templates/
│           ├── _helpers.tpl     # Template helper functions
│           ├── configmap.yaml   # Templated ConfigMap
│           ├── secret.yaml      # Templated Secret
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── frontend-deployment.yaml
│           ├── frontend-service.yaml
│           └── NOTES.txt        # Post-install instructions
│
├── scripts/                     # Automation scripts
│   ├── build.sh                 # Build Docker images
│   ├── deploy.sh                # Deploy with Helm
│   ├── cleanup.sh               # Remove all resources
│   └── test.sh                  # Verify deployment
│
├── README.md                    # Main deployment guide
├── TROUBLESHOOTING.md           # Common issues and solutions
├── AI_TOOLS_USAGE.md            # AI tools documentation
├── .env.example                 # Root environment template
└── .gitignore                   # Git ignore patterns
```

**Structure Decision**: Hybrid structure with backend/ and frontend/ containing application code plus Dockerfiles, separate kubernetes/ for raw manifests, and helm/ for packaged chart. This supports both `kubectl apply` and `helm install` deployment methods.

---

## Architecture Decisions

### ADR-001: Multi-Stage Docker Builds

**Status**: Accepted
**Context**: Need to create production Docker images from Phase 3 source code.
**Decision**: Use multi-stage builds with separate build and runtime stages.
**Rationale**:
- Smaller final images (only runtime dependencies)
- Build tools not shipped to production (security)
- Faster pulls and deployments
- Industry best practice
**Consequences**:
- Build time slightly longer (+30s)
- More complex Dockerfiles
- Image size reduced ~50%

### ADR-002: External Database (Neon PostgreSQL)

**Status**: Accepted
**Context**: Phase 3 uses cloud-hosted Neon PostgreSQL with existing schema.
**Decision**: Keep database external; do not containerize.
**Rationale**:
- Data persistence across deployments
- Existing schema and data preserved
- Reduces Kubernetes complexity (no StatefulSets)
- Phase 3 compatibility maintained
**Consequences**:
- Requires internet connectivity
- DATABASE_URL must be in Secrets
- Cannot run completely offline

### ADR-003: NodePort Services

**Status**: Accepted
**Context**: Need to expose frontend and backend for local access.
**Decision**: Use NodePort type services (not LoadBalancer or Ingress).
**Rationale**:
- Minikube supports NodePort natively
- Direct access via localhost:PORT
- No Ingress controller setup required
- Simpler for local development
**Consequences**:
- Fixed ports (30080, 30800)
- Must check for port conflicts
- Not suitable for production without modification

### ADR-004: ConfigMap and Secret Separation

**Status**: Accepted
**Context**: Application requires both sensitive and non-sensitive configuration.
**Decision**: Store non-sensitive config in ConfigMap, sensitive data in Secret.
**Rationale**:
- Security best practice
- Secrets are base64 encoded
- Clear separation of concerns
- Different access controls possible
**Consequences**:
- Two resources to manage
- Secrets must not be committed to git
- Need .example files for templates

### ADR-005: Helm as Primary Deployment Method

**Status**: Accepted
**Context**: Need repeatable, configurable deployments.
**Decision**: Provide Helm chart as primary method; raw manifests as backup.
**Rationale**:
- One-command deployment (`helm install`)
- Easy cleanup (`helm uninstall`)
- Configurable via values.yaml
- Industry standard
- Supports upgrades and rollbacks
**Consequences**:
- Must maintain both raw manifests and Helm templates
- Learning curve for Helm
- Chart versioning to manage

### ADR-006: Two Replicas Default

**Status**: Accepted
**Context**: Need to demonstrate high availability in Kubernetes.
**Decision**: Run 2 replicas of both frontend and backend deployments.
**Rationale**:
- Demonstrates HA capabilities
- Zero-downtime rolling updates
- Pod failure recovery demo
- Production-like behavior
**Consequences**:
- Double resource usage
- Acceptable for local demo
- Can scale down if resources limited

### ADR-007: Alpine-Based Images

**Status**: Accepted
**Context**: Need minimal image sizes for faster deployments.
**Decision**: Use `node:20-alpine` for frontend, `python:3.11-slim` for backend.
**Rationale**:
- Smaller image sizes
- Faster pulls
- Reduced attack surface
- Sufficient for application needs
**Consequences**:
- Backend uses slim (not alpine) due to psycopg binary requirements
- May need additional packages for some dependencies

### ADR-008: AI Tools Documentation Requirement

**Status**: Accepted
**Context**: Hackathon requirement to demonstrate AI DevOps tools.
**Decision**: Mandatory documentation of all Gordon, kubectl-ai, and kagent usage.
**Rationale**:
- Educational value
- Reproducibility
- Hackathon scoring criteria
- Demonstrates tool integration
**Consequences**:
- Additional documentation effort
- Must track all AI interactions
- Separate AI_TOOLS_USAGE.md file

---

## Implementation Phases

### Phase 1: Setup & Preparation

**Objective**: Establish project structure and copy Phase 3 source code.

**Tasks**:
1. Create directory structure (kubernetes/, helm/, scripts/)
2. Copy backend source from ../phase3/backend/ (excluding venv, __pycache__)
3. Copy frontend source from ../phase3/frontend/ (excluding node_modules, .next)
4. Create root .gitignore
5. Create root .env.example with all required variables
6. Verify Phase 3 code runs locally (quick sanity check)

**Verification**:
- All directories exist
- Source code copied without build artifacts
- .gitignore properly excludes sensitive files

**Duration Estimate**: N/A (per constitution - no time estimates)

---

### Phase 2: Docker Images

**Objective**: Create optimized Docker images for both applications.

**Tasks**:
1. Create backend/.dockerignore
2. Create backend/Dockerfile (multi-stage, python:3.11-slim)
   - Use Gordon: `docker ai "create production dockerfile for fastapi with uvicorn"`
3. Create frontend/.dockerignore
4. Modify frontend/next.config.ts to enable standalone output
5. Create frontend/Dockerfile (multi-stage, node:20-alpine)
   - Use Gordon: `docker ai "create production dockerfile for next.js 16 standalone"`
6. Build backend image: `docker build -t todo-backend:latest ./backend`
7. Build frontend image: `docker build -t todo-frontend:latest ./frontend`
8. Verify image sizes meet requirements
9. Test images run locally with docker run
10. Document Gordon usage in AI_TOOLS_USAGE.md

**Verification**:
- `docker images | grep todo` shows both images
- Backend image < 500MB
- Frontend image < 300MB
- Backend responds to health check
- Frontend serves pages

**Gordon Commands to Document**:
```bash
# Dockerfile creation
docker ai "create a multi-stage dockerfile for a fastapi python 3.11 application"
docker ai "optimize this dockerfile for production"
docker ai "what security improvements can I make to this dockerfile"
```

---

### Phase 3: Kubernetes Manifests

**Objective**: Create raw Kubernetes manifests for direct deployment.

**Tasks**:
1. Create kubernetes/configmap.yaml
   - ALLOWED_ORIGINS: http://localhost:30080
   - NEXT_PUBLIC_API_URL: http://localhost:30800
2. Create kubernetes/secret.yaml.example (template with placeholders)
3. Create kubernetes/backend-deployment.yaml
   - Use kubectl-ai: `kubectl ai "create deployment for backend with 2 replicas"`
4. Create kubernetes/backend-service.yaml (NodePort 30800)
5. Create kubernetes/frontend-deployment.yaml
   - Use kubectl-ai: `kubectl ai "create deployment for frontend with 2 replicas"`
6. Create kubernetes/frontend-service.yaml (NodePort 30080)
7. Validate all manifests: `kubectl apply --dry-run=client -f kubernetes/`
8. Document kubectl-ai usage

**Verification**:
- All YAML files pass `kubectl apply --dry-run=client`
- Labels are consistent across resources
- Resource limits defined
- Probes configured

**kubectl-ai Commands to Document**:
```bash
# Manifest generation
kubectl ai "create a deployment yaml for a python backend with 2 replicas, health checks, and resource limits"
kubectl ai "create a nodeport service for port 8000 exposed on 30800"
kubectl ai "what's wrong with my deployment - pods not starting"
```

---

### Phase 4: Helm Chart

**Objective**: Package deployment as reusable Helm chart.

**Tasks**:
1. Create helm/todo-chatbot/Chart.yaml
2. Create helm/todo-chatbot/values.yaml with all configurable values
3. Create helm/todo-chatbot/.helmignore
4. Create helm/todo-chatbot/templates/_helpers.tpl
5. Convert kubernetes/configmap.yaml to Helm template
6. Convert kubernetes/secret.yaml to Helm template
7. Convert kubernetes/backend-deployment.yaml to Helm template
8. Convert kubernetes/backend-service.yaml to Helm template
9. Convert kubernetes/frontend-deployment.yaml to Helm template
10. Convert kubernetes/frontend-service.yaml to Helm template
11. Create helm/todo-chatbot/templates/NOTES.txt
12. Validate: `helm lint ./helm/todo-chatbot`
13. Test render: `helm template todo-chatbot ./helm/todo-chatbot`
14. Dry run: `helm install todo-chatbot ./helm/todo-chatbot --dry-run`

**Verification**:
- `helm lint` passes with no errors
- `helm template` renders valid YAML
- `helm install --dry-run` succeeds

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
    requests:
      cpu: 250m
      memory: 256Mi
    limits:
      cpu: 1000m
      memory: 512Mi
  probe:
    path: /api/health
    initialDelaySeconds: 10
    periodSeconds: 30

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
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 256Mi
  probe:
    path: /
    initialDelaySeconds: 10
    periodSeconds: 30

config:
  allowedOrigins: "http://localhost:30080"
  apiUrl: "http://localhost:30800"

secrets:
  databaseUrl: ""      # Base64 encoded
  groqApiKey: ""       # Base64 encoded
  betterAuthSecret: "" # Base64 encoded
```

---

### Phase 5: Automation Scripts

**Objective**: Create shell scripts for common operations.

**Tasks**:
1. Create scripts/build.sh
   - Build backend and frontend images
   - Load images into Minikube
   - Verify image availability
2. Create scripts/deploy.sh
   - Check Minikube status
   - Create secret from .env file
   - Install/upgrade Helm chart
   - Wait for pods to be ready
3. Create scripts/cleanup.sh
   - Uninstall Helm release
   - Delete secrets
   - Optionally remove images
4. Create scripts/test.sh
   - Check pod status
   - Test health endpoints
   - Verify service connectivity
5. Make all scripts executable

**Verification**:
- Scripts run without syntax errors
- Scripts are idempotent (safe to run multiple times)
- Scripts provide helpful output

**build.sh Example**:
```bash
#!/bin/bash
set -e

echo "Building backend image..."
docker build -t todo-backend:latest ./backend

echo "Building frontend image..."
docker build -t todo-frontend:latest ./frontend

echo "Loading images into Minikube..."
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

echo "Verifying images..."
minikube image ls | grep todo

echo "Build complete!"
```

---

### Phase 6: Documentation

**Objective**: Create comprehensive documentation for deployment and troubleshooting.

**Tasks**:
1. Create README.md with:
   - Project overview
   - Prerequisites
   - Quick start guide
   - Step-by-step deployment
   - Verification steps
   - Scaling and management
   - Cleanup instructions
2. Create TROUBLESHOOTING.md with:
   - Common errors and solutions
   - Pod troubleshooting
   - Network issues
   - Image build problems
   - Database connectivity
3. Create AI_TOOLS_USAGE.md with:
   - Gordon examples (minimum 3)
   - kubectl-ai examples (minimum 3)
   - kagent monitoring (minimum 3)
   - Tips and best practices
4. Update .env.example with all variables

**Verification**:
- New developer can deploy using only README
- All documented commands work
- Troubleshooting covers observed issues

---

### Phase 7: Integration Testing

**Objective**: Deploy and verify complete system functionality.

**Tasks**:
1. Start fresh Minikube cluster: `minikube start`
2. Run build script: `./scripts/build.sh`
3. Create secret with real values
4. Run deploy script: `./scripts/deploy.sh`
5. Wait for all pods Running: `kubectl get pods -w`
6. Access frontend via NodePort
7. Test user journey:
   - Login with test account
   - View dashboard
   - Add new task
   - Navigate to /chat
   - Send AI command: "show my tasks"
   - Send AI command: "add task: test kubernetes"
   - Verify task appears in dashboard
8. Test pod recovery: delete a pod, verify recreation
9. Test scaling: `kubectl scale deployment backend --replicas=3`
10. Check kagent agents: `kubectl get pods -n kagent`
11. Document any kagent recommendations

**Verification**:
- All 4 pods Running
- Frontend accessible at localhost:30080
- Backend accessible at localhost:30800
- Full user journey completes
- AI chat responds correctly

---

### Phase 8: Final Validation

**Objective**: Verify all success criteria and prepare for demo.

**Tasks**:
1. Run cleanup: `./scripts/cleanup.sh`
2. Run fresh deployment from scratch
3. Verify all success criteria:
   - [ ] SC-001: Images build in < 5 minutes
   - [ ] SC-002: Backend image < 500MB
   - [ ] SC-003: Frontend image < 300MB
   - [ ] SC-004: Pods Running in < 2 minutes
   - [ ] SC-005: Pods stable for 5+ minutes
   - [ ] SC-006: Frontend loads in < 3 seconds
   - [ ] SC-007: Backend health check < 500ms
   - [ ] SC-008: Full user journey works
   - [ ] SC-009: helm lint passes
   - [ ] SC-010: helm install/uninstall clean
   - [ ] SC-011: 9+ AI tool examples documented
   - [ ] SC-012: README enables fresh deployment
4. Final documentation review
5. Create demo script/checklist
6. Commit all changes

**Verification**:
- All 12 success criteria pass
- Demo ready to present
- All files committed (no secrets)

---

## Deployment Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     DEPLOYMENT WORKFLOW                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────┐     ┌─────────────┐     ┌─────────────────────────┐
│  Phase 3    │     │   Docker    │     │      Minikube           │
│  Source     │────▶│   Build     │────▶│      Cluster            │
│  Code       │     │             │     │                         │
└─────────────┘     └─────────────┘     └─────────────────────────┘
      │                   │                        │
      │                   │                        │
      ▼                   ▼                        ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────────────────┐
│ backend/    │     │ todo-       │     │ ┌───────────────────┐   │
│ frontend/   │     │ backend:    │     │ │  ConfigMap        │   │
│             │     │ latest      │     │ │  - ALLOWED_ORIGINS│   │
│             │     │             │     │ │  - API_URL        │   │
│             │     │ todo-       │     │ └───────────────────┘   │
│             │     │ frontend:   │     │                         │
│             │     │ latest      │     │ ┌───────────────────┐   │
│             │     │             │     │ │  Secret           │   │
│             │     │             │     │ │  - DATABASE_URL   │   │
│             │     │             │     │ │  - GROQ_API_KEY   │   │
│             │     │             │     │ │  - AUTH_SECRET    │   │
└─────────────┘     └─────────────┘     │ └───────────────────┘   │
                                        │                         │
                                        │ ┌───────────────────┐   │
                                        │ │ Backend Deployment│   │
                                        │ │ - 2 replicas      │   │
                                        │ │ - Port: 8000      │   │
                                        │ │ - Health: /api/   │   │
                                        │ │   health          │   │
                                        │ └─────────┬─────────┘   │
                                        │           │             │
                                        │ ┌─────────▼─────────┐   │
                                        │ │ Backend Service   │   │
                                        │ │ - NodePort: 30800 │   │
                                        │ └───────────────────┘   │
                                        │                         │
                                        │ ┌───────────────────┐   │
                                        │ │Frontend Deployment│   │
                                        │ │ - 2 replicas      │   │
                                        │ │ - Port: 3000      │   │
                                        │ │ - Health: /       │   │
                                        │ └─────────┬─────────┘   │
                                        │           │             │
                                        │ ┌─────────▼─────────┐   │
                                        │ │ Frontend Service  │   │
                                        │ │ - NodePort: 30080 │   │
                                        │ └───────────────────┘   │
                                        └─────────────────────────┘
                                                    │
                                                    ▼
                                        ┌─────────────────────────┐
                                        │   User Access           │
                                        │   http://localhost:30080│
                                        └─────────────────────────┘
                                                    │
                                                    ▼
                                        ┌─────────────────────────┐
                                        │   Neon PostgreSQL       │
                                        │   (Cloud Database)      │
                                        └─────────────────────────┘
```

---

## Risk Analysis

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Docker build fails | High | Medium | Use Gordon for guidance, test incrementally |
| Image too large | Medium | Low | Multi-stage builds, Alpine base |
| Pod CrashLoopBackOff | High | Medium | Check logs, verify env vars, test locally first |
| Database connection fails | High | Medium | Verify DATABASE_URL, test connectivity |
| Port conflicts | Medium | Low | Document port changes in values.yaml |
| Minikube resource exhaustion | Medium | Medium | Set resource limits, reduce replicas if needed |
| CORS errors | High | Medium | Verify ALLOWED_ORIGINS matches frontend URL |
| Helm lint failures | Low | Low | Validate templates incrementally |

---

## Dependencies

### External
- Neon PostgreSQL (cloud) - existing from Phase 3
- Groq AI API - existing API key from Phase 3
- Docker Hub - for pulling base images

### Internal
- Phase 3 source code at ../phase3/
- Minikube running with docker driver
- kagent deployed in kagent namespace

### Blocking Dependencies by Phase
- Phase 2 (Docker) blocks Phase 3 (K8s) blocks Phase 4 (Helm)
- Phase 5 (Scripts) can run in parallel with Phase 6 (Docs)
- Phase 7 (Testing) requires all other phases complete
- Phase 8 (Validation) requires Phase 7 complete

---

## Next Steps

Run `/sp.tasks` to generate the detailed task breakdown with:
- Individual tasks for each phase
- Specific commands and expected outputs
- Dependencies between tasks
- Acceptance criteria for each task
