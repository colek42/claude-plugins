---
description: Clean Docker build cache in Minikube to free disk space
---

# Disk Space Cleanup for Minikube

Minikube docker build cache can grow to 200GB+ from repeated Skaffold builds. This command checks disk usage and cleans the cache without destroying cluster state.

## Check Disk Usage

```bash
docker exec minikube df -h /var/lib/docker
```

## Clean Build Cache

This frees ~240GB+ without destroying cluster state (PVCs, volumes remain intact):

```bash
docker exec minikube docker builder prune -af && docker exec minikube docker image prune -af
```

## What Gets Cleaned

- Docker build cache
- Dangling images
- Unused images

## What Remains Intact

- Running containers
- Persistent Volume Claims (PVCs)
- Kubernetes volumes
- Current pod states
- Cluster configuration

Execute the disk check first, show the results, then ask if the user wants to proceed with cleanup.
