# Incident 006 — OOMKilled / Memory Exhaustion

## 1. Incident Summary

**Incident:** API container repeatedly terminated with `OOMKilled`  
**Severity:** SEV-2  
**Status:** Resolved  
**Component:** `sre-api` Kubernetes Deployment  
**Environment:** Local Kubernetes (K3s)

The API pods repeatedly restarted because the container was configured with an intentionally low memory limit of `16Mi`.

---

## 2. Alert / Symptom

The initial pod state showed:

```text
sre-api-68b8f85f54-bkss5   0/1   ErrImagePull
sre-api-68b8f85f54-mznt6   0/1   OOMKilled
```

The relevant failure was:

```text
OOMKilled
```

This indicated that Kubernetes had terminated the container after it exceeded its configured memory limit.

---

## 3. Investigation

The Kubernetes Deployment was inspected in:

```text
k8s/deployment.yaml
```

The container had been configured with:

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "16Mi"
  limits:
    cpu: "500m"
    memory: "16Mi"
```

The `16Mi` memory limit was deliberately introduced to reproduce a memory-exhaustion incident.

Pod events showed that the image was successfully pulled and the container successfully started:

```text
Successfully pulled image
Container created
Container started
```

The container subsequently terminated and Kubernetes attempted to restart it.

---

## 4. Root Cause

The root cause was an **insufficient Kubernetes memory limit**.

The Flask application was allowed to use only:

```text
16Mi
```

of memory.

Once the container exceeded that limit, Kubernetes terminated the container with the reason:

```text
OOMKilled
```

This was a configuration-induced resource exhaustion scenario rather than an application code failure.

---

## 5. Remediation

The memory configuration was increased to:

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "64Mi"
  limits:
    cpu: "500m"
    memory: "128Mi"
```

The Deployment was then reapplied to Kubernetes.

Kubernetes created new pods using the corrected resource configuration.

---

## 6. Verification

After the configuration was corrected:

```text
sre-api   1/1   Running
sre-api   1/1   Running
```

The API health endpoint was also tested:

```bash
curl http://127.0.0.1:31265/health
```

Result:

```json
{"status":"healthy"}
```

The service was therefore confirmed operational.

---

## 7. SRE Lesson

`OOMKilled` means the container exceeded its available memory limit.

An SRE should investigate:

1. Pod status
2. Container termination reason
3. Current memory usage
4. Kubernetes memory requests and limits
5. Application logs
6. Whether the problem is caused by:
   - an undersized resource limit,
   - a memory leak,
   - increased traffic,
   - or another application/system issue.

A key lesson from this incident is:

> **Do not assume every OOMKilled event is an application memory leak. Check the Kubernetes resource configuration first.**

Resource limits should be based on observed application behaviour and established baselines rather than arbitrary values.