#!/bin/bash
# Phase 4: Test Todo Chatbot Deployment
# Verifies that all components are running correctly

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=============================================="
echo "Testing Todo Chatbot Deployment"
echo "=============================================="

cd "$PROJECT_ROOT"

TESTS_PASSED=0
TESTS_FAILED=0

# Test 1: Check pod status
echo ""
echo "1. Checking pod status..."
kubectl get pods -l app.kubernetes.io/name=todo-chatbot

BACKEND_READY=$(kubectl get pods -l app.kubernetes.io/component=backend -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}' 2>/dev/null)
FRONTEND_READY=$(kubectl get pods -l app.kubernetes.io/component=frontend -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}' 2>/dev/null)

if [[ "$BACKEND_READY" == *"True"* ]]; then
  echo "   [PASS] Backend pods are ready"
  ((TESTS_PASSED++))
else
  echo "   [FAIL] Backend pods are not ready"
  ((TESTS_FAILED++))
fi

if [[ "$FRONTEND_READY" == *"True"* ]]; then
  echo "   [PASS] Frontend pods are ready"
  ((TESTS_PASSED++))
else
  echo "   [FAIL] Frontend pods are not ready"
  ((TESTS_FAILED++))
fi

# Test 2: Check services
echo ""
echo "2. Checking services..."
kubectl get services -l app.kubernetes.io/name=todo-chatbot

BACKEND_SVC=$(kubectl get svc -l app.kubernetes.io/component=backend -o jsonpath='{.items[*].spec.ports[*].nodePort}' 2>/dev/null)
FRONTEND_SVC=$(kubectl get svc -l app.kubernetes.io/component=frontend -o jsonpath='{.items[*].spec.ports[*].nodePort}' 2>/dev/null)

if [ "$BACKEND_SVC" == "30800" ]; then
  echo "   [PASS] Backend service on NodePort 30800"
  ((TESTS_PASSED++))
else
  echo "   [FAIL] Backend service not on expected port (got: $BACKEND_SVC)"
  ((TESTS_FAILED++))
fi

if [ "$FRONTEND_SVC" == "30080" ]; then
  echo "   [PASS] Frontend service on NodePort 30080"
  ((TESTS_PASSED++))
else
  echo "   [FAIL] Frontend service not on expected port (got: $FRONTEND_SVC)"
  ((TESTS_FAILED++))
fi

# Test 3: Backend health check
echo ""
echo "3. Testing backend health endpoint..."
BACKEND_HEALTH=$(curl -s --connect-timeout 5 http://localhost:30800/api/health 2>/dev/null || echo "connection_failed")
if [[ "$BACKEND_HEALTH" == *"healthy"* ]] || [[ "$BACKEND_HEALTH" == *"status"* ]]; then
  echo "   [PASS] Backend health check passed"
  echo "   Response: $BACKEND_HEALTH"
  ((TESTS_PASSED++))
else
  echo "   [FAIL] Backend health check failed"
  echo "   Response: $BACKEND_HEALTH"
  ((TESTS_FAILED++))
fi

# Test 4: Frontend accessibility
echo ""
echo "4. Testing frontend..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 http://localhost:30080 2>/dev/null || echo "000")
if [ "$FRONTEND_STATUS" == "200" ]; then
  echo "   [PASS] Frontend responding (HTTP $FRONTEND_STATUS)"
  ((TESTS_PASSED++))
else
  echo "   [FAIL] Frontend not responding (HTTP $FRONTEND_STATUS)"
  ((TESTS_FAILED++))
fi

# Test 5: Check replica counts
echo ""
echo "5. Checking replica counts..."
BACKEND_REPLICAS=$(kubectl get deployment -l app.kubernetes.io/component=backend -o jsonpath='{.items[*].status.readyReplicas}' 2>/dev/null || echo "0")
FRONTEND_REPLICAS=$(kubectl get deployment -l app.kubernetes.io/component=frontend -o jsonpath='{.items[*].status.readyReplicas}' 2>/dev/null || echo "0")

if [ "$BACKEND_REPLICAS" == "2" ]; then
  echo "   [PASS] Backend has 2 replicas"
  ((TESTS_PASSED++))
else
  echo "   [WARN] Backend replicas: $BACKEND_REPLICAS (expected 2)"
fi

if [ "$FRONTEND_REPLICAS" == "2" ]; then
  echo "   [PASS] Frontend has 2 replicas"
  ((TESTS_PASSED++))
else
  echo "   [WARN] Frontend replicas: $FRONTEND_REPLICAS (expected 2)"
fi

# Summary
echo ""
echo "=============================================="
echo "Test Results"
echo "=============================================="
echo "Passed: $TESTS_PASSED"
echo "Failed: $TESTS_FAILED"

if [ $TESTS_FAILED -eq 0 ]; then
  echo ""
  echo "All tests passed!"
  echo ""
  echo "Access the application:"
  echo "  Frontend: http://localhost:30080"
  echo "  Backend:  http://localhost:30800"
  exit 0
else
  echo ""
  echo "Some tests failed. Check pod logs for details:"
  echo "  kubectl logs -l app.kubernetes.io/component=backend"
  echo "  kubectl logs -l app.kubernetes.io/component=frontend"
  exit 1
fi
