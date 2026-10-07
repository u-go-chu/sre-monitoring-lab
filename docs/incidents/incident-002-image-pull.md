# Incident 002 — ImagePullBackOff

## 1. Alert

**Incident:** API pod failed to start  
**Severity:** SEV-2

**Impact:**  
A new API pod could not start because Kubernetes was unable to pull the configured Docker image.

---

## 2. Observe

```bash
kubectl get pods
```

A newly created pod showed:

```text
sre-api-86bc4b9d44-grhjg   0/1   ErrImagePull
```

---

## 3. Investigation

The pod was investigated using:

```bash
kubectl describe pod sre-api-86bc4b9d44-grhjg
```

The Kubernetes events indicated that the configured Docker image could not be pulled.

The deployment was checked and the image was found to be:

```text
uggoiffi/sre-monitoring-api:wrong
```

---

## 4. Root Cause

The Kubernetes Deployment referenced an invalid Docker image tag.

The correct image tag was:

```text
uggoiffi/sre-monitoring-api:latest
```

---

## 5. Fix

The image tag was changed from:

```text
wrong
```

to:

```text
latest
```

The deployment was then reapplied:

```bash
kubectl apply -f k8s/deployment.yaml
```

---

## 6. Verification

```bash
kubectl get pods
```

Both API pods returned to:

```text
1/1 Running
```

**Incident status:** Resolved

---

## 7. Lesson Learned

An incorrect image name or tag can prevent Kubernetes from starting a pod.

When investigating `ErrImagePull` or `ImagePullBackOff`, check the image reference in the Deployment and inspect the pod events for the exact pull error.