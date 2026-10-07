# Incident 001 — API Pod Failure

## 1. Alert

**Incident:** API availability temporarily degraded  
**Time detected:** 2026-10-06 18:30  
**Severity:** SEV-2

**Impact:**  
One API pod was unavailable while Kubernetes created a replacement pod.

---

## 2. Observe

Initial observation:

```bash
kubectl get pods
```

One pod was in `ContainerCreating` while the other remained `Running`.

```text
sre-api-5cc75ddf64-mgzs5   0/1   ContainerCreating
sre-api-5cc75ddf64-wkpp7   1/1   Running
```

---

## 3. Investigation

The pod was investigated using:

```bash
kubectl describe pod sre-api-5cc75ddf64-mgzs5
```

Kubernetes events showed:

```text
Pulling image "uggoiffi/sre-monitoring-api:latest"
Successfully pulled image
Container created
Container started
```

The Docker image pull took approximately **3 minutes 15 seconds**.

The container itself started successfully.

---

## 4. Root Cause

The API pod did not crash.

The temporary degradation was caused by a slow Docker image pull when Kubernetes created the replacement pod.

---

## 5. Recovery

No manual fix was required.

Kubernetes automatically created the replacement pod because the Deployment was configured to maintain **2 replicas**.

Final state:

```text
2/2 pods Running
```

API health check:

```bash
curl http://127.0.0.1:31265/health
```

Result:

```json
{"status":"healthy"}
```

---

## 6. Verification

The API was confirmed healthy and both replicas were running.

**Incident status:** Resolved

## 7. Lesson Learned

Kubernetes automatically maintained the desired replica count, but slow image pulls can delay recovery when a replacement pod is required.

Monitoring pod startup time and image-pull performance can help identify this type of issue.