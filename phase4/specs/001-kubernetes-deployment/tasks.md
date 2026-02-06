# Tasks: Local Kubernetes Deployment

**Input**: Design documents from `/specs/001-kubernetes-deployment/`
**Prerequisites**: plan.md ✅, spec.md ✅

**Organization**: Tasks are organized by implementation phase, mapping to user stories:
- Phase 1 (Setup) → Foundation for all stories
- Phase 2 (Docker) → US1: Docker Image Creation
- Phase 3 (K8s Manifests) → US2: Kubernetes Deployment, US3: Service Exposure, US4: Configuration
- Phase 4 (Helm) → US5: Helm Chart Package
- Phase 5 (Scripts) → US2, US5: Automation support
- Phase 6 (Docs) → US6: AI Tools, US8: Documentation
- Phase 7 (Testing) → US7: Application Functionality
- Phase 8 (Validation) → All success criteria

## Format: `[ID] [P?] [US#] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[US#]**: Which user story this task belongs to

---

## Phase 1: Setup & Preparation

**Purpose**: Establish project structure and copy Phase 3 source code
**Goal**: All directories created, source code ready for containerization
**Independent Test**: `ls -la` shows all expected directories; source files present

### Tasks

- [X] **T001** [US1] Create root project directories
  ```bash
  mkdir -p kubernetes helm/todo-chatbot/templates scripts
  ```
  **Expected**: Directories exist
  **Dependencies**: None

- [X] **T002** [P] [US1] Create root .gitignore file at `phase4/.gitignore`
  **Content**: Exclude .env, node_modules, venv, __pycache__, .next, *.pyc, .DS_Store
  **Expected**: File exists with proper patterns
  **Dependencies**: None

- [X] **T003** [P] [US4] Create root .env.example at `phase4/.env.example`
  **Content**: Template with DATABASE_URL, GROQ_API_KEY, BETTER_AUTH_SECRET placeholders
  **Expected**: File shows all required environment variables
  **Dependencies**: None

- [X] **T004** [US1] Copy backend source from Phase 3
  ```bash
  # Copy backend excluding venv, __pycache__, .git
  cp -r ../phase3/backend ./backend
  rm -rf ./backend/venv ./backend/__pycache__ ./backend/.git
  ```
  **Expected**: backend/ contains main.py, agent.py, requirements.txt, routes/, etc.
  **Dependencies**: T001
  **Manual**: Verify files copied correctly

- [X] **T005** [US1] Copy frontend source from Phase 3
  ```bash
  # Copy frontend excluding node_modules, .next, .git
  cp -r ../phase3/frontend ./frontend
  rm -rf ./frontend/node_modules ./frontend/.next ./frontend/.git
  ```
  **Expected**: frontend/ contains package.json, app/, components/, etc.
  **Dependencies**: T001
  **Manual**: Verify files copied correctly

- [X] **T006** [US1] Verify Phase 3 code structure
  ```bash
  ls -la backend/
  ls -la frontend/
  ```
  **Expected**: All source files present, no build artifacts
  **Dependencies**: T004, T005

**Checkpoint**: Project structure ready, Phase 3 code available for containerization

---

## Phase 2: Docker Images (US1: Docker Image Creation)

**Purpose**: Create optimized Docker images for backend and frontend
**Goal**: Both images build successfully, meet size requirements, run correctly
**Independent Test**: `docker run` both images, verify health checks respond

### Backend Docker Tasks

- [X] **T007** [P] [US1] Create backend/.dockerignore
  ```
  venv/
  __pycache__/
  *.pyc
  *.pyo
  .git/
  .env
  .env.*
  *.md
  tests/
  .pytest_cache/
  ```
  **Expected**: File excludes build artifacts and sensitive files
  **Dependencies**: T004

- [X] **T008** [US1] Create backend/Dockerfile (multi-stage)
  **AI Tool**: Gordon
  ```bash
  docker ai "create a multi-stage production dockerfile for a fastapi python 3.11 application with uvicorn, health checks, and non-root user"
  ```
  **Content Requirements** (FR-001, FR-003, FR-005, FR-006):
  - Stage 1: python:3.11-slim as builder, install dependencies
  - Stage 2: python:3.11-slim as runtime, copy deps, create non-root user
  - WORKDIR /app
  - EXPOSE 8000
  - HEALTHCHECK instruction
  - USER appuser
  - CMD uvicorn
  **Expected**: Dockerfile with multi-stage build, non-root user, health check
  **Dependencies**: T004, T007

- [ ] **T009** [US1] Build backend Docker image
  ```bash
  docker build -t todo-backend:latest ./backend
  ```
  **Expected**: Build completes successfully, image created
  **Dependencies**: T008

- [ ] **T010** [US1] Verify backend image size (FR-007)
  ```bash
  docker images todo-backend:latest --format "{{.Size}}"
  ```
  **Expected**: Size < 500MB
  **Dependencies**: T009

- [ ] **T011** [US1] Test backend image runs locally
  ```bash
  docker run -d --name test-backend -p 8000:8000 \
    -e DATABASE_URL="postgresql://test:test@localhost:5432/test" \
    -e GROQ_API_KEY="test" \
    -e BETTER_AUTH_SECRET="test" \
    -e ALLOWED_ORIGINS="*" \
    todo-backend:latest
  # Wait for startup
  sleep 5
  curl http://localhost:8000/api/health
  docker stop test-backend && docker rm test-backend
  ```
  **Expected**: Health check returns JSON with status "healthy"
  **Dependencies**: T009
  **Note**: Will show database error (expected without real DB)

### Frontend Docker Tasks

- [X] **T012** [P] [US1] Create frontend/.dockerignore
  ```
  node_modules/
  .next/
  .git/
  .env
  .env.*
  *.md
  coverage/
  .nyc_output/
  ```
  **Expected**: File excludes build artifacts and dependencies
  **Dependencies**: T005

- [X] **T013** [US1] Modify frontend/next.config.ts for standalone output
  **Change**: Add `output: 'standalone'` to Next.js config
  ```typescript
  const nextConfig = {
    output: 'standalone',
    // ... existing config
  };
  ```
  **Expected**: Config enables standalone build output
  **Dependencies**: T005
  **Required for**: Minimal Docker image

- [X] **T014** [US1] Create frontend/Dockerfile (multi-stage)
  **AI Tool**: Gordon
  ```bash
  docker ai "create a multi-stage production dockerfile for next.js 16 standalone build with node 20 alpine and non-root user"
  ```
  **Content Requirements** (FR-002, FR-004, FR-005, FR-006):
  - Stage 1 (deps): node:20-alpine, install dependencies
  - Stage 2 (builder): copy deps, build with NEXT_PUBLIC_API_URL arg
  - Stage 3 (runner): node:20-alpine, copy standalone output, non-root user
  - WORKDIR /app
  - EXPOSE 3000
  - USER nextjs
  - CMD node server.js
  **Expected**: Dockerfile with 3-stage build, non-root user
  **Dependencies**: T005, T012, T013

- [ ] **T015** [US1] Build frontend Docker image
  ```bash
  docker build -t todo-frontend:latest \
    --build-arg NEXT_PUBLIC_API_URL=http://localhost:30800 \
    ./frontend
  ```
  **Expected**: Build completes successfully, image created
  **Dependencies**: T014

- [ ] **T016** [US1] Verify frontend image size (FR-008)
  ```bash
  docker images todo-frontend:latest --format "{{.Size}}"
  ```
  **Expected**: Size < 300MB
  **Dependencies**: T015

- [ ] **T017** [US1] Test frontend image runs locally
  ```bash
  docker run -d --name test-frontend -p 3000:3000 todo-frontend:latest
  sleep 5
  curl http://localhost:3000
  docker stop test-frontend && docker rm test-frontend
  ```
  **Expected**: Returns HTML content
  **Dependencies**: T015

### Gordon Documentation Task

- [ ] **T018** [US6] Document Gordon usage for Dockerfiles
  **File**: AI_TOOLS_USAGE.md (create initial content)
  **Content**:
  - Commands used for backend Dockerfile
  - Commands used for frontend Dockerfile
  - Gordon's optimization suggestions
  - Screenshots or output logs
  **Expected**: At least 3 Gordon examples documented
  **Dependencies**: T008, T014
  **AI Tool**: Gordon (documentation of usage)

**Checkpoint**: Both Docker images built, tested locally, sizes verified, Gordon usage documented

---

## Phase 3: Kubernetes Manifests (US2, US3, US4)

**Purpose**: Create raw Kubernetes manifests for deployment
**Goal**: All manifests valid, can deploy with kubectl apply
**Independent Test**: `kubectl apply --dry-run=client -f kubernetes/` succeeds

### Configuration Tasks (US4: Configuration Management)

- [X] **T019** [P] [US4] Create kubernetes/configmap.yaml (FR-014, FR-027, FR-028)
  **AI Tool**: kubectl-ai
  ```bash
  kubectl ai "create a configmap named todo-config with ALLOWED_ORIGINS=http://localhost:30080"
  ```
  **Content**:
  ```yaml
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: todo-config
    labels:
      app.kubernetes.io/name: todo-chatbot
      app.kubernetes.io/managed-by: kubectl
  data:
    ALLOWED_ORIGINS: "http://localhost:30080"
    NEXT_PUBLIC_API_URL: "http://localhost:30800"
  ```
  **Expected**: ConfigMap with non-sensitive configuration
  **Dependencies**: T001

- [X] **T020** [P] [US4] Create kubernetes/secret.yaml.example (FR-015, FR-024, FR-025, FR-026)
  **Content** (template with placeholders - NOT real values):
  ```yaml
  apiVersion: v1
  kind: Secret
  metadata:
    name: todo-secrets
    labels:
      app.kubernetes.io/name: todo-chatbot
  type: Opaque
  data:
    DATABASE_URL: <base64-encoded-value>
    GROQ_API_KEY: <base64-encoded-value>
    BETTER_AUTH_SECRET: <base64-encoded-value>
  ```
  **Expected**: Secret template, NOT committed with real values
  **Dependencies**: T001
  **Manual**: User must create actual secret with real values

### Backend Deployment Tasks (US2: Kubernetes Deployment)

- [X] **T021** [US2] Create kubernetes/backend-deployment.yaml (FR-009, FR-010, FR-016, FR-017)
  **AI Tool**: kubectl-ai
  ```bash
  kubectl ai "create a deployment named backend with 2 replicas, image todo-backend:latest, port 8000, liveness probe on /api/health, resource limits 512Mi memory and 1 cpu"
  ```
  **Content Requirements**:
  - apiVersion: apps/v1
  - 2 replicas (FR-010)
  - Image: todo-backend:latest
  - imagePullPolicy: IfNotPresent
  - Container port: 8000
  - envFrom: configMapRef (todo-config), secretRef (todo-secrets)
  - Resources: requests (256Mi, 250m), limits (512Mi, 1000m) (FR-016)
  - livenessProbe: httpGet /api/health, initialDelaySeconds: 10 (FR-017)
  - readinessProbe: httpGet /api/health, initialDelaySeconds: 5 (FR-017)
  - Labels: app.kubernetes.io/name: todo-chatbot, app.kubernetes.io/component: backend
  **Expected**: Valid Deployment manifest
  **Dependencies**: T019, T020

- [X] **T022** [US3] Create kubernetes/backend-service.yaml (FR-011, FR-013)
  **AI Tool**: kubectl-ai
  ```bash
  kubectl ai "create a nodeport service named backend-service for deployment backend on port 8000 with nodeport 30800"
  ```
  **Content**:
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: backend-service
    labels:
      app.kubernetes.io/name: todo-chatbot
      app.kubernetes.io/component: backend
  spec:
    type: NodePort
    selector:
      app.kubernetes.io/component: backend
    ports:
      - port: 8000
        targetPort: 8000
        nodePort: 30800
        protocol: TCP
  ```
  **Expected**: NodePort service on 30800 (FR-013)
  **Dependencies**: T021

### Frontend Deployment Tasks (US2, US3)

- [X] **T023** [US2] Create kubernetes/frontend-deployment.yaml (FR-009, FR-010, FR-016, FR-017)
  **AI Tool**: kubectl-ai
  ```bash
  kubectl ai "create a deployment named frontend with 2 replicas, image todo-frontend:latest, port 3000, liveness probe on /, resource limits 256Mi memory"
  ```
  **Content Requirements**:
  - apiVersion: apps/v1
  - 2 replicas (FR-010)
  - Image: todo-frontend:latest
  - imagePullPolicy: IfNotPresent
  - Container port: 3000
  - Resources: requests (128Mi, 100m), limits (256Mi, 500m) (FR-016)
  - livenessProbe: httpGet /, initialDelaySeconds: 10 (FR-017)
  - readinessProbe: httpGet /, initialDelaySeconds: 5 (FR-017)
  - Labels: app.kubernetes.io/name: todo-chatbot, app.kubernetes.io/component: frontend
  **Expected**: Valid Deployment manifest
  **Dependencies**: T019

- [X] **T024** [US3] Create kubernetes/frontend-service.yaml (FR-011, FR-012)
  **Content**:
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: frontend-service
    labels:
      app.kubernetes.io/name: todo-chatbot
      app.kubernetes.io/component: frontend
  spec:
    type: NodePort
    selector:
      app.kubernetes.io/component: frontend
    ports:
      - port: 3000
        targetPort: 3000
        nodePort: 30080
        protocol: TCP
  ```
  **Expected**: NodePort service on 30080 (FR-012)
  **Dependencies**: T023

### Validation Tasks

- [X] **T025** [US2] Validate all Kubernetes manifests
  ```bash
  kubectl apply --dry-run=client -f kubernetes/configmap.yaml
  kubectl apply --dry-run=client -f kubernetes/backend-deployment.yaml
  kubectl apply --dry-run=client -f kubernetes/backend-service.yaml
  kubectl apply --dry-run=client -f kubernetes/frontend-deployment.yaml
  kubectl apply --dry-run=client -f kubernetes/frontend-service.yaml
  ```
  **Expected**: All manifests pass validation
  **Dependencies**: T019-T024

- [ ] **T026** [US6] Document kubectl-ai usage for manifests
  **File**: AI_TOOLS_USAGE.md (append content)
  **Content**:
  - Commands used for each manifest
  - kubectl-ai suggestions received
  - Troubleshooting commands tried
  **Expected**: At least 3 kubectl-ai examples documented
  **Dependencies**: T021, T022, T023
  **AI Tool**: kubectl-ai (documentation of usage)

**Checkpoint**: All K8s manifests created and validated, kubectl-ai usage documented

---

## Phase 4: Helm Chart (US5: Helm Chart Package)

**Purpose**: Package deployment as reusable Helm chart
**Goal**: helm lint passes, helm install works
**Independent Test**: `helm lint ./helm/todo-chatbot` succeeds

### Chart Setup Tasks

- [X] **T027** [US5] Create helm/todo-chatbot/Chart.yaml (FR-018, FR-019)
  **Content**:
  ```yaml
  apiVersion: v2
  name: todo-chatbot
  description: Todo AI Chatbot - Phase 4 Kubernetes Deployment
  type: application
  version: 1.0.0
  appVersion: "1.0.0"
  keywords:
    - todo
    - chatbot
    - kubernetes
    - fastapi
    - nextjs
  maintainers:
    - name: Phase 4 Team
  ```
  **Expected**: Valid Chart.yaml with version 1.0.0 (FR-019)
  **Dependencies**: T001

- [X] **T028** [US5] Create helm/todo-chatbot/values.yaml (FR-020)
  **Content**:
  ```yaml
  # Backend configuration
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
      timeoutSeconds: 10

  # Frontend configuration
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
      timeoutSeconds: 10

  # Configuration
  config:
    allowedOrigins: "http://localhost:30080"
    apiUrl: "http://localhost:30800"

  # Secrets (base64 encoded - set during install)
  secrets:
    databaseUrl: ""
    groqApiKey: ""
    betterAuthSecret: ""
  ```
  **Expected**: Configurable values for all components
  **Dependencies**: T027

- [X] **T029** [P] [US5] Create helm/todo-chatbot/.helmignore
  **Content**:
  ```
  .git/
  .gitignore
  *.md
  .DS_Store
  ```
  **Expected**: Excludes unnecessary files from chart package
  **Dependencies**: T027

### Template Tasks

- [X] **T030** [US5] Create helm/todo-chatbot/templates/_helpers.tpl (FR-021)
  **Content**:
  ```
  {{/*
  Expand the name of the chart.
  */}}
  {{- define "todo-chatbot.name" -}}
  {{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
  {{- end }}

  {{/*
  Create chart name and version as used by the chart label.
  */}}
  {{- define "todo-chatbot.chart" -}}
  {{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
  {{- end }}

  {{/*
  Common labels
  */}}
  {{- define "todo-chatbot.labels" -}}
  helm.sh/chart: {{ include "todo-chatbot.chart" . }}
  app.kubernetes.io/name: {{ include "todo-chatbot.name" . }}
  app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
  app.kubernetes.io/managed-by: {{ .Release.Service }}
  {{- end }}

  {{/*
  Backend selector labels
  */}}
  {{- define "todo-chatbot.backend.selectorLabels" -}}
  app.kubernetes.io/name: {{ include "todo-chatbot.name" . }}
  app.kubernetes.io/component: backend
  {{- end }}

  {{/*
  Frontend selector labels
  */}}
  {{- define "todo-chatbot.frontend.selectorLabels" -}}
  app.kubernetes.io/name: {{ include "todo-chatbot.name" . }}
  app.kubernetes.io/component: frontend
  {{- end }}
  ```
  **Expected**: Helper templates for labels and names
  **Dependencies**: T027

- [X] **T031** [US5] Create helm/todo-chatbot/templates/configmap.yaml (FR-021)
  **Content**: Convert kubernetes/configmap.yaml to Helm template
  ```yaml
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: {{ include "todo-chatbot.name" . }}-config
    labels:
      {{- include "todo-chatbot.labels" . | nindent 4 }}
  data:
    ALLOWED_ORIGINS: {{ .Values.config.allowedOrigins | quote }}
    NEXT_PUBLIC_API_URL: {{ .Values.config.apiUrl | quote }}
  ```
  **Expected**: Templated ConfigMap using values.yaml
  **Dependencies**: T019, T030

- [X] **T032** [US5] Create helm/todo-chatbot/templates/secret.yaml (FR-021)
  **Content**:
  ```yaml
  apiVersion: v1
  kind: Secret
  metadata:
    name: {{ include "todo-chatbot.name" . }}-secrets
    labels:
      {{- include "todo-chatbot.labels" . | nindent 4 }}
  type: Opaque
  data:
    DATABASE_URL: {{ .Values.secrets.databaseUrl | b64enc | quote }}
    GROQ_API_KEY: {{ .Values.secrets.groqApiKey | b64enc | quote }}
    BETTER_AUTH_SECRET: {{ .Values.secrets.betterAuthSecret | b64enc | quote }}
  ```
  **Expected**: Templated Secret with base64 encoding
  **Dependencies**: T020, T030

- [X] **T033** [US5] Create helm/todo-chatbot/templates/backend-deployment.yaml (FR-021)
  **Content**: Convert kubernetes/backend-deployment.yaml to Helm template
  - Use {{ .Values.backend.replicas }}
  - Use {{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}
  - Use {{ .Values.backend.resources }}
  - Reference configmap and secret by templated names
  **Expected**: Templated Deployment using values.yaml
  **Dependencies**: T021, T030

- [X] **T034** [US5] Create helm/todo-chatbot/templates/backend-service.yaml (FR-021)
  **Content**: Convert kubernetes/backend-service.yaml to Helm template
  - Use {{ .Values.backend.service.type }}
  - Use {{ .Values.backend.service.port }}
  - Use {{ .Values.backend.service.nodePort }}
  **Expected**: Templated Service using values.yaml
  **Dependencies**: T022, T030

- [X] **T035** [US5] Create helm/todo-chatbot/templates/frontend-deployment.yaml (FR-021)
  **Content**: Convert kubernetes/frontend-deployment.yaml to Helm template
  - Use {{ .Values.frontend.replicas }}
  - Use {{ .Values.frontend.image.repository }}:{{ .Values.frontend.image.tag }}
  - Use {{ .Values.frontend.resources }}
  **Expected**: Templated Deployment using values.yaml
  **Dependencies**: T023, T030

- [X] **T036** [US5] Create helm/todo-chatbot/templates/frontend-service.yaml (FR-021)
  **Content**: Convert kubernetes/frontend-service.yaml to Helm template
  **Expected**: Templated Service using values.yaml
  **Dependencies**: T024, T030

- [X] **T037** [US5] Create helm/todo-chatbot/templates/NOTES.txt (FR-022)
  **Content**:
  ```
  🎉 Todo AI Chatbot has been deployed!

  To access the application:

  1. Frontend (Web UI):
     {{- if eq .Values.frontend.service.type "NodePort" }}
     Run: minikube service {{ include "todo-chatbot.name" . }}-frontend --url
     Or access: http://localhost:{{ .Values.frontend.service.nodePort }}
     {{- end }}

  2. Backend (API):
     {{- if eq .Values.backend.service.type "NodePort" }}
     Run: minikube service {{ include "todo-chatbot.name" . }}-backend --url
     Or access: http://localhost:{{ .Values.backend.service.nodePort }}
     Health check: http://localhost:{{ .Values.backend.service.nodePort }}/api/health
     {{- end }}

  3. Check pod status:
     kubectl get pods -l app.kubernetes.io/name={{ include "todo-chatbot.name" . }}

  4. View logs:
     kubectl logs -l app.kubernetes.io/component=backend
     kubectl logs -l app.kubernetes.io/component=frontend

  5. To uninstall:
     helm uninstall {{ .Release.Name }}

  📚 For more information, see README.md
  ```
  **Expected**: Helpful post-install instructions
  **Dependencies**: T030

### Validation Tasks

- [X] **T038** [US5] Validate Helm chart with lint (FR-023)
  ```bash
  helm lint ./helm/todo-chatbot
  ```
  **Expected**: "0 chart(s) failed" - no errors or warnings
  **Dependencies**: T030-T037

- [X] **T039** [US5] Test Helm template rendering
  ```bash
  helm template todo-chatbot ./helm/todo-chatbot \
    --set secrets.databaseUrl=test \
    --set secrets.groqApiKey=test \
    --set secrets.betterAuthSecret=test
  ```
  **Expected**: Renders valid YAML for all resources
  **Dependencies**: T038

- [ ] **T040** [US5] Test Helm dry-run installation
  ```bash
  helm install todo-chatbot ./helm/todo-chatbot --dry-run \
    --set secrets.databaseUrl=test \
    --set secrets.groqApiKey=test \
    --set secrets.betterAuthSecret=test
  ```
  **Expected**: Dry run succeeds with no errors
  **Dependencies**: T039

**Checkpoint**: Helm chart complete, validated, ready for deployment

---

## Phase 5: Automation Scripts

**Purpose**: Create shell scripts for common operations
**Goal**: One-command build, deploy, cleanup, test
**Independent Test**: Each script runs without errors

### Script Tasks

- [X] **T041** [US2] Create scripts/build.sh
  **Content**:
  ```bash
  #!/bin/bash
  set -e

  echo "=== Building Todo Chatbot Docker Images ==="

  # Build backend
  echo "Building backend image..."
  docker build -t todo-backend:latest ./backend

  # Build frontend
  echo "Building frontend image..."
  docker build -t todo-frontend:latest \
    --build-arg NEXT_PUBLIC_API_URL=http://localhost:30800 \
    ./frontend

  # Verify sizes
  echo ""
  echo "=== Image Sizes ==="
  docker images | grep todo

  # Load into Minikube
  echo ""
  echo "=== Loading images into Minikube ==="
  minikube image load todo-backend:latest
  minikube image load todo-frontend:latest

  # Verify in Minikube
  echo ""
  echo "=== Images in Minikube ==="
  minikube image ls | grep todo

  echo ""
  echo "✅ Build complete!"
  ```
  **Expected**: Script builds and loads images
  **Dependencies**: T009, T015

- [X] **T042** [US5] Create scripts/deploy.sh
  **Content**:
  ```bash
  #!/bin/bash
  set -e

  echo "=== Deploying Todo Chatbot to Minikube ==="

  # Check Minikube status
  echo "Checking Minikube..."
  minikube status || { echo "❌ Minikube not running. Start with: minikube start"; exit 1; }

  # Check if .env file exists
  if [ ! -f .env ]; then
    echo "❌ .env file not found. Copy .env.example and fill in values."
    exit 1
  fi

  # Load environment variables
  source .env

  # Install/upgrade with Helm
  echo "Installing with Helm..."
  helm upgrade --install todo-chatbot ./helm/todo-chatbot \
    --set secrets.databaseUrl="$DATABASE_URL" \
    --set secrets.groqApiKey="$GROQ_API_KEY" \
    --set secrets.betterAuthSecret="$BETTER_AUTH_SECRET"

  # Wait for pods
  echo ""
  echo "Waiting for pods to be ready..."
  kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-chatbot --timeout=120s

  # Show status
  echo ""
  echo "=== Deployment Status ==="
  kubectl get pods -l app.kubernetes.io/name=todo-chatbot
  kubectl get services -l app.kubernetes.io/name=todo-chatbot

  echo ""
  echo "✅ Deployment complete!"
  echo "Frontend: http://localhost:30080"
  echo "Backend:  http://localhost:30800"
  ```
  **Expected**: Script deploys application with Helm
  **Dependencies**: T038
  **Manual**: Requires .env file with real values

- [X] **T043** [US5] Create scripts/cleanup.sh
  **Content**:
  ```bash
  #!/bin/bash
  set -e

  echo "=== Cleaning up Todo Chatbot ==="

  # Uninstall Helm release
  echo "Uninstalling Helm release..."
  helm uninstall todo-chatbot 2>/dev/null || echo "No Helm release found"

  # Verify cleanup
  echo ""
  echo "=== Remaining resources ==="
  kubectl get all -l app.kubernetes.io/name=todo-chatbot 2>/dev/null || echo "No resources found"

  # Optionally remove images
  read -p "Remove Docker images? (y/N) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker rmi todo-backend:latest todo-frontend:latest 2>/dev/null || true
    echo "Images removed"
  fi

  echo ""
  echo "✅ Cleanup complete!"
  ```
  **Expected**: Script removes all deployed resources
  **Dependencies**: T042

- [X] **T044** [US7] Create scripts/test.sh
  **Content**:
  ```bash
  #!/bin/bash
  set -e

  echo "=== Testing Todo Chatbot Deployment ==="

  # Check pods
  echo "1. Checking pod status..."
  kubectl get pods -l app.kubernetes.io/name=todo-chatbot

  BACKEND_READY=$(kubectl get pods -l app.kubernetes.io/component=backend -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}')
  FRONTEND_READY=$(kubectl get pods -l app.kubernetes.io/component=frontend -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}')

  if [[ "$BACKEND_READY" != *"True"* ]]; then
    echo "❌ Backend pods not ready"
    exit 1
  fi

  if [[ "$FRONTEND_READY" != *"True"* ]]; then
    echo "❌ Frontend pods not ready"
    exit 1
  fi
  echo "✅ All pods ready"

  # Check services
  echo ""
  echo "2. Checking services..."
  kubectl get services -l app.kubernetes.io/name=todo-chatbot
  echo "✅ Services exist"

  # Test backend health
  echo ""
  echo "3. Testing backend health endpoint..."
  BACKEND_HEALTH=$(curl -s http://localhost:30800/api/health)
  echo "$BACKEND_HEALTH"
  if [[ "$BACKEND_HEALTH" == *"healthy"* ]]; then
    echo "✅ Backend healthy"
  else
    echo "❌ Backend health check failed"
    exit 1
  fi

  # Test frontend
  echo ""
  echo "4. Testing frontend..."
  FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:30080)
  if [[ "$FRONTEND_STATUS" == "200" ]]; then
    echo "✅ Frontend responding (HTTP $FRONTEND_STATUS)"
  else
    echo "❌ Frontend not responding (HTTP $FRONTEND_STATUS)"
    exit 1
  fi

  echo ""
  echo "=== All tests passed! ==="
  echo "Frontend: http://localhost:30080"
  echo "Backend:  http://localhost:30800"
  ```
  **Expected**: Script verifies deployment health
  **Dependencies**: T042

- [ ] **T045** [US2] Make scripts executable
  ```bash
  chmod +x scripts/build.sh scripts/deploy.sh scripts/cleanup.sh scripts/test.sh
  ```
  **Expected**: Scripts are executable
  **Dependencies**: T041-T044

**Checkpoint**: All automation scripts created and tested

---

## Phase 6: Documentation (US6, US8)

**Purpose**: Create comprehensive documentation
**Goal**: New developer can deploy using only docs
**Independent Test**: Follow README from scratch, deployment succeeds

### Documentation Tasks

- [X] **T046** [US8] Create README.md (FR-029)
  **Sections**:
  1. Project Overview
  2. Prerequisites (Docker, Minikube, Helm, kubectl versions)
  3. Quick Start (5-minute deployment)
  4. Step-by-Step Deployment Guide
  5. Configuration (environment variables, values.yaml)
  6. Accessing the Application
  7. Scaling and Management
  8. Troubleshooting (link to TROUBLESHOOTING.md)
  9. AI Tools (link to AI_TOOLS_USAGE.md)
  10. Cleanup
  **Expected**: Complete deployment guide
  **Dependencies**: T045

- [X] **T047** [US8] Create TROUBLESHOOTING.md (FR-030)
  **Sections**:
  1. Pod Issues
     - CrashLoopBackOff
     - ImagePullBackOff
     - Pending pods
  2. Network Issues
     - Cannot access NodePort
     - CORS errors
     - Connection refused
  3. Database Issues
     - Connection timeout
     - Authentication failed
  4. Image Build Issues
     - Docker daemon not running
     - Build fails
     - Image too large
  5. Helm Issues
     - Release already exists
     - Template rendering errors
  6. Debugging Commands
  **Expected**: Solutions for common issues
  **Dependencies**: T046

- [X] **T048** [US6] Complete AI_TOOLS_USAGE.md (FR-031)
  **Sections**:
  1. Gordon (Docker AI)
     - Example 1: Creating backend Dockerfile
     - Example 2: Creating frontend Dockerfile
     - Example 3: Optimizing image size
     - Tips for effective prompts
  2. kubectl-ai
     - Example 1: Creating deployment manifest
     - Example 2: Creating service manifest
     - Example 3: Troubleshooting pod issues
     - Natural language command examples
  3. kagent
     - Example 1: Checking agent status
     - Example 2: Getting cluster recommendations
     - Example 3: Monitoring deployment
     - Agent capabilities overview
  **Expected**: 9+ documented AI tool examples (3 per tool)
  **Dependencies**: T018, T026
  **AI Tool**: All three (documentation compilation)

- [ ] **T049** [P] [US4] Update phase4/.env.example
  **Content**:
  ```bash
  # Database connection string (Neon PostgreSQL)
  DATABASE_URL=postgresql://user:password@host:5432/dbname

  # Groq AI API key (from console.groq.com)
  GROQ_API_KEY=gsk_your-api-key-here

  # JWT secret (must match frontend, same as Phase 3)
  BETTER_AUTH_SECRET=your-jwt-secret-here
  ```
  **Expected**: Clear template with all required variables
  **Dependencies**: T003

**Checkpoint**: All documentation complete, ready for user testing

---

## Phase 7: Integration Testing (US7: Application Functionality)

**Purpose**: Deploy and verify complete system
**Goal**: All functionality works as in Phase 3
**Independent Test**: Complete user journey succeeds

### Deployment Tasks

- [ ] **T050** [US2] Ensure Minikube is running
  ```bash
  minikube status || minikube start --driver=docker --cpus=2 --memory=4096
  ```
  **Expected**: Minikube shows Running
  **Dependencies**: None

- [ ] **T051** [US1] Run build script
  ```bash
  ./scripts/build.sh
  ```
  **Expected**: Both images built and loaded
  **Dependencies**: T045, T050

- [ ] **T052** [US4] Create .env file with real values
  **Manual Action**: Copy .env.example to .env, fill in real values
  ```bash
  cp .env.example .env
  # Edit .env with real DATABASE_URL, GROQ_API_KEY, BETTER_AUTH_SECRET
  ```
  **Expected**: .env file exists with valid credentials
  **Dependencies**: T049
  **Manual**: User must provide real credentials

- [ ] **T053** [US5] Run deploy script
  ```bash
  ./scripts/deploy.sh
  ```
  **Expected**: Helm release installed, pods running
  **Dependencies**: T051, T052

- [ ] **T054** [US2] Verify all pods Running
  ```bash
  kubectl get pods -l app.kubernetes.io/name=todo-chatbot
  ```
  **Expected**: 4 pods (2 backend, 2 frontend) all Running
  **Dependencies**: T053

- [ ] **T055** [US2] Run test script
  ```bash
  ./scripts/test.sh
  ```
  **Expected**: All health checks pass
  **Dependencies**: T054

### Functionality Tests (US7)

- [ ] **T056** [US7] Test frontend access
  ```bash
  # Open in browser or curl
  curl http://localhost:30080
  ```
  **Expected**: Frontend loads, shows login/signup page
  **Dependencies**: T054

- [ ] **T057** [US7] Test backend API
  ```bash
  curl http://localhost:30800/api/health
  curl http://localhost:30800/docs
  ```
  **Expected**: Health returns JSON, docs show Swagger UI
  **Dependencies**: T054

- [ ] **T058** [US7] Test user login flow
  **Manual Action**:
  1. Open http://localhost:30080 in browser
  2. Click Login/Signup
  3. Use existing Phase 3 credentials or create new account
  **Expected**: Login succeeds, redirects to dashboard
  **Dependencies**: T056
  **Manual**: Requires browser interaction

- [ ] **T059** [US7] Test dashboard functionality
  **Manual Action**:
  1. View existing tasks on dashboard
  2. Add a new task via UI
  3. Edit a task
  4. Delete a task
  **Expected**: All CRUD operations work
  **Dependencies**: T058
  **Manual**: Requires browser interaction

- [ ] **T060** [US7] Test AI chat interface
  **Manual Action**:
  1. Navigate to /chat
  2. Send "show my tasks"
  3. Send "add task: test kubernetes deployment"
  4. Verify task appears in response
  5. Check dashboard for new task
  **Expected**: AI responds correctly, task created
  **Dependencies**: T058
  **Manual**: Requires browser interaction

### Resilience Tests

- [ ] **T061** [US2] Test pod recovery
  ```bash
  # Delete a backend pod
  kubectl delete pod -l app.kubernetes.io/component=backend --wait=false | head -1
  # Wait and verify replacement
  sleep 10
  kubectl get pods -l app.kubernetes.io/component=backend
  ```
  **Expected**: New pod created automatically
  **Dependencies**: T054

- [ ] **T062** [US2] Test scaling
  ```bash
  # Scale backend to 3 replicas
  kubectl scale deployment todo-chatbot-backend --replicas=3
  kubectl get pods -l app.kubernetes.io/component=backend
  # Scale back to 2
  kubectl scale deployment todo-chatbot-backend --replicas=2
  ```
  **Expected**: Pods scale up and down correctly
  **Dependencies**: T054

### kagent Verification (US6)

- [ ] **T063** [US6] Verify kagent agents running
  ```bash
  kubectl get pods -n kagent
  ```
  **Expected**: All 16 kagent agent pods Running
  **Dependencies**: None (kagent pre-installed)

- [ ] **T064** [US6] Document kagent monitoring
  **Content for AI_TOOLS_USAGE.md**:
  - Commands to check agent status
  - Any recommendations received
  - Cluster health observations
  **Expected**: kagent examples added to documentation
  **Dependencies**: T063
  **AI Tool**: kagent

**Checkpoint**: Full deployment verified, all functionality working

---

## Phase 8: Final Validation (All Success Criteria)

**Purpose**: Verify all success criteria met
**Goal**: Project ready for demo
**Independent Test**: All 12 success criteria pass

### Success Criteria Verification

- [ ] **T065** Verify SC-001: Images build in < 5 minutes
  ```bash
  time ./scripts/build.sh
  ```
  **Expected**: Total time < 300 seconds
  **Dependencies**: T051

- [ ] **T066** Verify SC-002: Backend image < 500MB
  ```bash
  docker images todo-backend:latest --format "{{.Size}}"
  ```
  **Expected**: Size reported < 500MB
  **Dependencies**: T051

- [ ] **T067** Verify SC-003: Frontend image < 300MB
  ```bash
  docker images todo-frontend:latest --format "{{.Size}}"
  ```
  **Expected**: Size reported < 300MB
  **Dependencies**: T051

- [ ] **T068** Verify SC-004: Pods Running in < 2 minutes
  ```bash
  # Fresh deployment timing
  helm uninstall todo-chatbot
  time (helm install todo-chatbot ./helm/todo-chatbot ... && \
        kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-chatbot --timeout=120s)
  ```
  **Expected**: Time < 120 seconds
  **Dependencies**: T053

- [ ] **T069** Verify SC-005: Pods stable for 5+ minutes
  ```bash
  # Check restart count after 5 minutes
  kubectl get pods -l app.kubernetes.io/name=todo-chatbot -o jsonpath='{.items[*].status.containerStatuses[*].restartCount}'
  ```
  **Expected**: Restart count = 0
  **Dependencies**: T054

- [ ] **T070** Verify SC-006: Frontend loads in < 3 seconds
  ```bash
  time curl -s http://localhost:30080 > /dev/null
  ```
  **Expected**: Time < 3 seconds
  **Dependencies**: T056

- [ ] **T071** Verify SC-007: Backend health check < 500ms
  ```bash
  time curl -s http://localhost:30800/api/health > /dev/null
  ```
  **Expected**: Time < 0.5 seconds
  **Dependencies**: T057

- [ ] **T072** Verify SC-008: Full user journey works
  **Manual Verification**: T058, T059, T060 all passed
  **Expected**: All user journey tests successful
  **Dependencies**: T058, T059, T060

- [ ] **T073** Verify SC-009: helm lint passes
  ```bash
  helm lint ./helm/todo-chatbot
  ```
  **Expected**: 0 chart(s) failed
  **Dependencies**: T038

- [ ] **T074** Verify SC-010: helm install/uninstall clean
  ```bash
  helm uninstall todo-chatbot
  kubectl get all -l app.kubernetes.io/name=todo-chatbot
  # Re-install
  ./scripts/deploy.sh
  ```
  **Expected**: Clean uninstall, successful reinstall
  **Dependencies**: T053

- [ ] **T075** Verify SC-011: 9+ AI tool examples documented
  ```bash
  grep -c "Example" AI_TOOLS_USAGE.md
  ```
  **Expected**: Count >= 9
  **Dependencies**: T048

- [ ] **T076** Verify SC-012: README enables fresh deployment
  **Manual Verification**: Have someone follow README.md from scratch
  **Expected**: Successful deployment following only README
  **Dependencies**: T046
  **Manual**: Ideally tested by different person

### Final Tasks

- [ ] **T077** Create demo checklist
  **Content**:
  ```markdown
  # Demo Checklist

  ## Pre-Demo
  - [ ] Minikube running
  - [ ] Images built
  - [ ] Deployment running

  ## Demo Steps
  1. Show `kubectl get pods` - all Running
  2. Show `kubectl get services` - NodePorts exposed
  3. Open frontend in browser
  4. Login and show dashboard
  5. Add task via UI
  6. Use AI chat to add task
  7. Show pod recovery: `kubectl delete pod ...`
  8. Show scaling: `kubectl scale deployment ...`
  9. Show Helm operations: `helm list`
  10. Show kagent agents: `kubectl get pods -n kagent`

  ## Cleanup
  - [ ] helm uninstall todo-chatbot
  ```
  **Expected**: Demo preparation guide
  **Dependencies**: T074

- [ ] **T078** Final documentation review
  **Actions**:
  - Read through README.md
  - Verify all commands work
  - Check for typos
  - Ensure consistency
  **Expected**: Documentation polished
  **Dependencies**: T046, T047, T048

- [ ] **T079** Commit all changes
  ```bash
  git add .
  git status
  # Verify no secrets in staged files
  git commit -m "Phase 4: Local Kubernetes Deployment complete"
  ```
  **Expected**: All files committed (excluding .env)
  **Dependencies**: All tasks

**Checkpoint**: Project complete, all success criteria verified, ready for demo

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Docker) ←────────────┐
    ↓                         │
Phase 3 (K8s Manifests)       │ Can work in parallel
    ↓                         │ after Phase 1
Phase 4 (Helm) ←──────────────┘
    ↓
Phase 5 (Scripts) ←───────────┐
    ↓                         │ Can work in parallel
Phase 6 (Documentation) ←─────┘
    ↓
Phase 7 (Integration Testing)
    ↓
Phase 8 (Final Validation)
```

### Critical Path

```
T001 → T004 → T008 → T009 → T021 → T033 → T041 → T053 → T054 → T065
```
(Setup → Backend Dockerfile → Build → K8s Deployment → Helm Template → Build Script → Deploy → Verify → Validate)

### Parallel Opportunities

Within Phase 2:
- T007 (backend .dockerignore) || T012 (frontend .dockerignore)
- T008 (backend Dockerfile) can start after T007
- T014 (frontend Dockerfile) can start after T012

Within Phase 3:
- T019 (configmap) || T020 (secret)
- T021 (backend deployment) || T023 (frontend deployment) after T019

Within Phase 4:
- T031-T036 (templates) can be parallelized

Within Phase 6:
- T046 || T047 || T048 (all documentation tasks)

---

## Task Summary

| Phase | Tasks | Blocking | Parallel Opportunities |
|-------|-------|----------|------------------------|
| 1. Setup | T001-T006 | None | T002, T003 |
| 2. Docker | T007-T018 | Phase 1 | T007/T012, Backend/Frontend builds |
| 3. K8s Manifests | T019-T026 | Phase 2 | T019/T020, T021/T023 |
| 4. Helm | T027-T040 | Phase 3 | T031-T036 |
| 5. Scripts | T041-T045 | Phase 4 | None (sequential) |
| 6. Documentation | T046-T049 | Phase 2, 3 | T046/T047/T048 |
| 7. Testing | T050-T064 | Phase 5 | Functionality tests |
| 8. Validation | T065-T079 | Phase 7 | SC verifications |

**Total Tasks**: 79
**Manual Tasks**: T052 (create .env), T058-T060 (browser tests), T076 (README test)
**AI Tool Tasks**: T008, T014, T018 (Gordon), T021-T023, T026 (kubectl-ai), T063-T064 (kagent)

---

## Functional Requirements Coverage

| Requirement | Task(s) |
|-------------|---------|
| FR-001: Build backend image | T009 |
| FR-002: Build frontend image | T015 |
| FR-003: Backend multi-stage | T008 |
| FR-004: Frontend multi-stage | T014 |
| FR-005: Non-root user | T008, T014 |
| FR-006: Health checks | T008, T014 |
| FR-007: Backend < 500MB | T010 |
| FR-008: Frontend < 300MB | T016 |
| FR-009: Deployment manifests | T021, T023 |
| FR-010: 2 replicas | T021, T023 |
| FR-011: NodePort services | T022, T024 |
| FR-012: Frontend port 30080 | T024 |
| FR-013: Backend port 30800 | T022 |
| FR-014: ConfigMap | T019 |
| FR-015: Secret | T020 |
| FR-016: Resource limits | T021, T023 |
| FR-017: Probes | T021, T023 |
| FR-018: Helm chart | T027 |
| FR-019: Chart version 1.0.0 | T027 |
| FR-020: values.yaml | T028 |
| FR-021: Templates | T031-T036 |
| FR-022: NOTES.txt | T037 |
| FR-023: helm lint | T038 |
| FR-024: DATABASE_URL secret | T020, T032 |
| FR-025: GROQ_API_KEY secret | T020, T032 |
| FR-026: BETTER_AUTH_SECRET | T020, T032 |
| FR-027: ALLOWED_ORIGINS config | T019, T031 |
| FR-028: NEXT_PUBLIC_API_URL | T019, T031 |
| FR-029: README.md | T046 |
| FR-030: TROUBLESHOOTING.md | T047 |
| FR-031: AI_TOOLS_USAGE.md | T048 |

All 31 functional requirements are covered by the task breakdown.
