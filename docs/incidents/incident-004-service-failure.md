# Incident 004 — Kubernetes Service Failure

## 1. Alert

**Incident:** API Service became unreachable  
**Severity:** SEV-2  
**Impact:** The API pods were healthy, but the Kubernetes Service had no endpoints and could not route traffic to the pods.

---

## 2. Observe

The API pods were checked:

```bash
kubectl get pods --show-labels
```

Result:

```text
NAME                       READY   STATUS    RESTARTS   AGE     LABELS
sre-api-5cc75ddf64-mgzs5   1/1     Running   0          3h58m   app=sre-api,pod-template-hash=5cc75ddf64
sre-api-5cc75ddf64-wkpp7   1/1     Running   0          29h     app=sre-api,pod-template-hash=5cc75ddf64
```

Both API pods were healthy.

The Service endpoints were then checked:

```bash
kubectl get endpoints sre-api-service
```

Result:

```text
NAME              ENDPOINTS   AGE
sre-api-service   <none>      37h
```

The Service had no backend endpoints.

---

## 3. Investigation

The pod labels showed that the API pods had:

```text
app=sre-api
```

The Kubernetes Service configuration was inspected:

```bash
kubectl get svc sre-api-service -o yaml
```

The Service selector was:

```yaml
selector:
  app: broken-api
```

This did not match the labels on the API pods.

The Service was therefore looking for:

```text
app=broken-api
```

while the actual pods were labelled:

```text
app=sre-api
```

Because there were no matching pods, Kubernetes created no Service endpoints.

---

## 4. Root Cause

The root cause was an incorrect Kubernetes Service selector.

The Service selector had been changed from:

```yaml
selector:
  app: sre-api
```

to:

```yaml
selector:
  app: broken-api
```

This