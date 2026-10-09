# SRE Monitoring Lab

A hands-on Site Reliability Engineering (SRE) project demonstrating Kubernetes deployment, monitoring, autoscaling, incident troubleshooting, and service recovery in a local Linux environment.

## Architecture

**Flask API → Docker → Kubernetes (K3s) → Prometheus → Grafana**

## Technology Stack

- **Application:** Python, Flask
- **Containerization:** Docker
- **Orchestration:** Kubernetes (K3s)
- **Monitoring:** Prometheus, Grafana
- **Autoscaling:** Kubernetes Horizontal Pod Autoscaler (HPA)
- **Load Testing:** k6
- **Version Control:** Git, GitHub

## SRE Practices Demonstrated

- Application health checks and resource monitoring
- CPU-based horizontal pod autoscaling
- Troubleshooting `CrashLoopBackOff`, `ImagePullBackOff`, service failures, and `OOMKilled`
- Root-cause analysis, remediation, and recovery verification
- Incident documentation and a repeatable troubleshooting runbook

## Run Environment

The project runs locally using K3s. Prometheus and Grafana provide monitoring, while Kubernetes manages application replicas and autoscaling.

## Repository Contents

- `app/` — application source code
- `docs/incidents/` — incident reports and recovery records
- `docs/troubleshooting-runbook.md` — troubleshooting workflow

## Objective

Demonstrate practical SRE skills through controlled failure scenarios, evidence-based troubleshooting, monitoring, and service recovery.