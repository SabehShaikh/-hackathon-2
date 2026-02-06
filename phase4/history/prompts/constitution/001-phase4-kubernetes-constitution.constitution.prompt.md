---
id: 001
title: Phase 4 Kubernetes Deployment Constitution
stage: constitution
date: 2025-02-04
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: 002-ai-chat-interface
user: SABEH
command: /sp.constitution
labels: ["kubernetes", "minikube", "helm", "docker", "devops", "constitution"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

/sp.constitution

Project: Phase 4 - Local Kubernetes Deployment (Minikube, Helm Charts, kubectl-ai, kagent, Docker Desktop, Gordon)

Context:
This is Phase 4 of a multi-phase hackathon project. Phases 1-3 are complete and deployed:
- Phase 1: Console-based Todo app
- Phase 2: Full-stack web app (FastAPI + Next.js) deployed to HuggingFace + Vercel
- Phase 3: AI Chatbot with natural language interface (Groq + MCP + OpenAI Agents SDK)

Phase 3 source code is located at ../phase3/ and consists of:
- Backend: FastAPI with Groq AI integration, 5 MCP tools, OpenAI Agents SDK
- Frontend: Next.js 16 with ChatKit for conversational UI
- Database: Neon PostgreSQL (cloud-hosted, connection string in .env)
- Authentication: JWT with Better Auth
- Deployment: HuggingFace Spaces (backend) + Vercel (frontend)

Phase 4 Objective:
Containerize the Phase 3 application and deploy it to a local Kubernetes cluster using Minikube, demonstrating cloud-native deployment practices with AI-assisted DevOps tools.

Technology Stack (All Installed and Verified):
- Docker Desktop 29.1.5 with Gordon AI Agent
- Minikube v1.38.0 (docker driver)
- kubectl v1.34.1
- Helm v3.16.4
- kubectl-ai (via krew)
- kagent 0.7.13 (16 agents in cluster)

## Response snapshot

Created comprehensive constitution document at `.specify/memory/constitution.md` with 10 core principles:

1. **Code Reuse Over Duplication** - Reference Phase 3 code, copy only essentials for Docker builds
2. **AI-First DevOps Workflow** - Leverage Gordon, kubectl-ai, kagent as primary assistants
3. **Spec-Driven Development** - Follow SpecifyPlus workflow throughout
4. **Container Best Practices** - Multi-stage builds, Alpine base, non-root user, health checks
5. **Kubernetes Resource Design** - Separate manifests, 2 replicas, NodePort services, proper labels
6. **Helm Chart Organization** - Single chart (todo-chatbot) with templated manifests
7. **Stateless Application Architecture** - External database, ephemeral pods
8. **Local Development Focus** - Minikube-optimized, no TLS required
9. **Production-Ready Practices** - Error handling, logging, resource limits
10. **Documentation and Reproducibility** - Complete guides and AI tool documentation

Defined deliverables: Docker images, Kubernetes manifests, Helm chart, scripts, documentation.
Established success criteria: pods running, services accessible, full functionality verified.
Explicitly scoped out: cloud deployment, TLS, Ingress, PVs, CI/CD.

## Outcome

- ✅ Impact: Established foundational principles for Phase 4 Kubernetes deployment
- 🧪 Tests: N/A (constitution document)
- 📁 Files: Created .specify/memory/constitution.md
- 🔁 Next prompts: /sp.specify to create feature specification, /sp.plan for implementation planning
- 🧠 Reflection: Constitution captures all key requirements from user context including AI DevOps tools

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to specification phase
