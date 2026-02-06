# Phase 4 - Local Kubernetes Deployment Constitution

## Core Principles

### I. Code Reuse Over Duplication
Reference Phase 3 source code from `../phase3/` directory for Docker builds. Copy only essential source files (backend/, frontend/) needed for container images. Exclude: node_modules/, venv/, __pycache__/, .git/, .next/, specs/, history/, .specify/. Phase 3 artifacts remain authoritative; Phase 4 creates containerization layer only.

### II. AI-First DevOps Workflow
Leverage AI tools as primary assistants for DevOps tasks:
- **Gordon (Docker AI)**: Use `docker ai` for Dockerfile creation, optimization, and best practices guidance
- **kubectl-ai**: Use for generating Kubernetes commands from natural language
- **kagent**: Use cluster agents for monitoring, recommendations, and automated operations
Document all AI tool interactions for educational value and reproducibility.

### III. Spec-Driven Development
Follow SpecifyPlus workflow: constitution → specification → plan → tasks → implementation. All artifacts stored in specs/ and history/ directories. Use Claude Code for code generation via /sp.implement. No manual coding - everything generated through defined workflows. Document all decisions in appropriate spec files.

### IV. Container Best Practices
Enforce production-grade container standards:
- Multi-stage builds for minimal final images
- Official base images: node:20-alpine (frontend), python:3.11-slim (backend)
- Target sizes: frontend < 300MB, backend < 500MB
- Non-root user execution for security
- Health checks in all Dockerfiles
- Proper .dockerignore files
- Environment variables for all configuration (never hardcode secrets)
- Proper labeling and metadata (OCI annotations)

### V. Kubernetes Resource Design
Structure Kubernetes resources for maintainability and reliability:
- Separate manifests per resource type (deployment, service, configmap, secret)
- Deployments with 2 replicas minimum for high availability
- NodePort services for local Minikube access (frontend: 30080, backend: 30800)
- ConfigMaps for non-sensitive configuration
- Secrets for sensitive data (base64 encoded, never committed to version control)
- Resource requests and limits on all containers
- Readiness and liveness probes configured
- Consistent labels: app, component, version, managed-by

### VI. Helm Chart Organization
Package deployments as reusable Helm chart:
- Chart name: todo-chatbot
- Single chart containing frontend and backend components
- Templated manifests in templates/ directory
- Configurable values.yaml for: replicas, images, resources, environment
- Support one-command deployment: `helm install todo-chatbot ./helm/todo-chatbot`
- Support one-command cleanup: `helm uninstall todo-chatbot`
- Chart metadata and versioning in Chart.yaml
- Post-install notes in templates/NOTES.txt

### VII. Stateless Application Architecture
Design for cloud-native statelessness:
- No persistent volumes (external Neon PostgreSQL handles all state)
- Pods are ephemeral and horizontally scalable
- Configuration via environment variables only
- Secrets managed through Kubernetes Secrets
- No local file storage dependencies
- Graceful shutdown handling

### VIII. Local Development Focus
Optimize for Minikube local development:
- Deploy to Minikube only (not cloud providers)
- NodePort services (no Ingress controller needed)
- Access via `minikube service` or `kubectl port-forward`
- No TLS/HTTPS required
- Docker driver for Minikube (--driver=docker)
- Resource allocation: 2 CPUs, 4GB RAM

### IX. Production-Ready Practices
Apply production patterns even in local development:
- Proper error handling and graceful degradation
- Logging to stdout/stderr (Kubernetes log aggregation)
- Health check endpoints (/api/health for backend)
- Resource limits to prevent resource exhaustion
- Security context for non-root execution
- No secrets in version control (use .env.example templates)

### X. Documentation and Reproducibility
Ensure complete reproducibility:
- README.md with step-by-step deployment guide
- TROUBLESHOOTING.md for common issues
- AI_TOOLS_USAGE.md documenting Gordon, kubectl-ai, kagent examples
- All commands documented for easy copy-paste
- Verification steps for each deployment phase
- Clean teardown instructions

## Technology Stack

### Containerization
- Docker Desktop 29.1.5 with Gordon AI Agent (Beta features enabled)
- Multi-stage Dockerfiles with Alpine Linux base

### Orchestration
- Minikube v1.38.0 (docker driver)
- kubectl v1.34.1
- Helm v3.16.4

### AI DevOps Tools
- kubectl-ai (installed via krew) - natural language Kubernetes commands
- kagent 0.7.13 (16 agents in cluster) - AI cluster management
- Gordon (Docker Desktop) - AI-assisted Docker operations

### Application Stack (from Phase 3)
- Backend: FastAPI, Groq AI, OpenAI Agents SDK, 5 MCP tools
- Frontend: Next.js 16, ChatKit, Better Auth
- Database: Neon PostgreSQL (cloud, external to cluster)

## Deliverables

### Required Artifacts
1. **Docker Images**: frontend:latest, backend:latest (built and loaded to Minikube)
2. **Kubernetes Manifests**: kubernetes/ directory with deployment, service, configmap, secret YAMLs
3. **Helm Chart**: helm/todo-chatbot/ with Chart.yaml, values.yaml, templates/
4. **Dockerfiles**: Multi-stage builds for frontend and backend
5. **Scripts**: build.sh, deploy.sh, cleanup.sh, test.sh
6. **Documentation**: README.md, TROUBLESHOOTING.md, AI_TOOLS_USAGE.md

### Success Criteria
- Both Docker images build without errors
- All Kubernetes pods reach Running status
- Frontend accessible at localhost:30080
- Backend accessible at localhost:30800
- Frontend-backend communication works
- Database connectivity confirmed
- Authentication flow functional
- AI chat interface operational
- All 5 MCP tools functioning
- Helm chart installs/uninstalls cleanly

## Out of Scope
- Cloud deployment (AWS/GCP/Azure)
- Production TLS/HTTPS certificates
- Ingress controllers
- Persistent volumes
- StatefulSets/DaemonSets
- Monitoring stack (Prometheus/Grafana) - kagent provides this
- CI/CD pipelines
- Multiple environments (dev/staging/prod)

## Governance

This constitution supersedes all other practices for Phase 4 development. Amendments require:
1. Documentation of proposed change
2. Review of impact on existing artifacts
3. Update to dependent templates and manifests

All PRs and reviews must verify compliance with these principles. Use CLAUDE.md for runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2025-02-04 | **Last Amended**: 2025-02-04
