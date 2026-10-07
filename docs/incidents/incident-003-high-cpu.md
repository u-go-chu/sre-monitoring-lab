# Incident 003 — High CPU / HPA Autoscaling

## 1. Alert

**Incident:** High CPU utilization detected  
**Severity:** SEV-3  
**Impact:** Increased CPU utilization triggered Kubernetes horizontal autoscaling. No API outage occurred.

---

## 2. Observe

Initial state:

```bash
kubectl get hpa
```

The application was running with 2 replicas and low CPU utilization.

A controlled load test was then started using k6 with 100 virtual users for 2 minutes.

CPU increased significantly:

```bash
kubectl top pods
```

CPU usage reached approximately:

```text
83m
90m
```

The HPA showed:

```bash
kubectl get hpa
```

```text
NAME          REFERENCE            TARGETS       MINPODS   MAXPODS   REPLICAS
sre-api-hpa   Deployment/sre-api   cpu: 72%/50%   2         5         4
```

---

## 3. Investigation

The HPA was configured with:

- Minimum replicas: 2
- Maximum replicas: 5
- CPU target: 50%

The deployment also had a CPU request of:

```yaml
requests:
  cpu: "100m"
```

The k6 test generated controlled traffic against:

```text
/health
```

As traffic increased, CPU utilization exceeded the HPA target.

Kubernetes responded by increasing the number of API pods from:

```text
2 → 4
```

---

## 4. Root Cause

The increased request volume from the k6 load test caused higher CPU utilization.

Once CPU utilization exceeded the configured HPA target of 50%, Kubernetes automatically scaled the deployment from 2 replicas to 4 replicas.

This was an intentional load test rather than an unexpected production failure.

---

## 5. Recovery

After the k6 load test stopped, CPU utilization returned to normal levels.

The HPA eventually scaled the application back down:

```text
4 → 2 pods
```

Final HPA status:

```text
CPU: 1% / 50%
Replicas: 2
```

---

## 6. Verification

Check the pods:

```bash
kubectl get pods
```

The application returned to 2 healthy replicas.

API health was verified with:

```bash
curl http://127.0.0.1:31265/health
```

Response:

```json
{"status":"healthy"}
```

---

## 7. Lesson Learned

High CPU utilization does not automatically mean that an application is failing.

An SRE should determine:

- What is the normal CPU baseline?
- What threshold triggers an alert or scaling action?
- Is the application actually unavailable?
- Is Kubernetes responding correctly?
- Did the workload recover after traffic decreased?

In this incident, Kubernetes successfully detected increased CPU utilization and automatically scaled the application.

The incident demonstrates how Horizontal Pod Autoscaling can protect an application from increased workload by adding additional replicas.