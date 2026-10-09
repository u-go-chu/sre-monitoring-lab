SRE Troubleshooting Runbook

Purpose

A repeatable process for diagnosing and resolving incidents in the SRE Monitoring Lab.

Troubleshooting Workflow

Alert — Identify the alert, user impact, and affected service.

Observe — Check the overall health of the application and infrastructure.

Check metrics — Inspect CPU, memory, pod status, restarts, and autoscaling.

Check logs — Review application and container logs for errors.

Check Kubernetes — Inspect pods, deployments, services, events, and endpoints.

Identify root cause — Use evidence to determine why the incident occurred.

Fix — Apply the smallest safe corrective change.

Verify — Confirm recovery using health checks, metrics, and pod status.

Useful Commands

kubectl get pods
kubectl get deployments
kubectl get services
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl top pods
kubectl get hpa

Incident Record

For each incident, record:

Impact and severity

Detection time and symptoms

Investigation and evidence

Root cause

Remediation

Recovery verification

Lessons learned

Principle: Diagnose using evidence, make a controlled change, and verify recovery before closing an incident.