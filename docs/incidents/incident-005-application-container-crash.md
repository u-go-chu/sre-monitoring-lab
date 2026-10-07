# Incident 005 — CrashLoopBackOff

## 1. Alert

**Incident:** API pods repeatedly crashed after startup  
**Severity:** SEV-2  
**Impact:** Both API replicas were unavailable because their containers failed during startup.

---

## 2. Observe

The API pods were checked:

```bash
kubectl get pods
```

Result:

```text
NAME                       READY   STATUS             RESTARTS
sre-api-6d6cf4654b-j9v4j   0/1     CrashLoopBackOff   11
sre-api-6d6cf4654b-jl4fs   0/1     CrashLoopBackOff   8
```

Both replicas were repeatedly failing.

The increasing restart count indicated that Kubernetes was repeatedly restarting the containers.

---

## 3. Investigation

The logs of one failing pod were checked:

```bash
kubectl logs sre-api-6d6cf4654b-j9v4j
```

The following error was returned:

```text
python: can't open file '/app/missing-app.py': [Errno 2] No such file or directory
```

This showed that the container was attempting to start a Python file that did not exist inside the Docker image.

The Deployment configuration was then inspected.

The problematic configuration was:

```yaml
command: ["python", "missing-app.py"]
```

The Docker image actually contains the application's `app.py` file and is configured to start the application normally.

---

## 4. Root Cause

The root cause was an incorrect container startup command in the Kubernetes Deployment.

The Deployment instructed the container to run:

```text
missing-app.py
```

However, that file did not exist inside the container.

The application therefore exited immediately after startup.

Kubernetes detected the container failure and repeatedly restarted it, eventually reporting:

```text
CrashLoopBackOff
```

---

## 5. Fix

The incorrect `command` configuration was removed from:

```text
k8s/deployment.yaml
```

The Deployment was restored to use the Docker image's normal startup command.

The corrected container configuration included:

```yaml
containers:
  - name: sre-api
    image: uggoiffi/sre-monitoring-api:latest
    ports:
      - containerPort: 5000
```

The corrected Deployment was applied:

```bash
kubectl apply -f deployment.yaml
```

---

## 6. Verification

The pods were checked after applying the fix:

```bash
kubectl get pods
```

The API pods returned to a healthy running state:

```text
1/1   Running
1/1   Running
```

The CrashLoopBackOff condition was resolved.

---

## 7. Lesson Learned

`CrashLoopBackOff` means Kubernetes is repeatedly attempting to restart a container that is failing.

The correct troubleshooting approach is to investigate the container rather than immediately modifying unrelated Kubernetes resources.

A useful investigation sequence is:

```text
kubectl get pods
        ↓
Identify CrashLoopBackOff
        ↓
kubectl logs <pod>
        ↓
Identify application/container error
        ↓
Inspect Deployment configuration
        ↓
Fix root cause
        ↓
kubectl apply
        ↓
Verify pods are Running
```

The key lesson is:

**When a pod enters CrashLoopBackOff, check the container logs first. The logs often reveal the actual application or startup error.**