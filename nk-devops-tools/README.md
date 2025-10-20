# NK DevOps Tools Plugin

Helm, ArgoCD, Vault best practices and disk space management for Minikube/Skaffold workflows.

## What's Included

### Skills

- **helm-practices** - Dependency management, chart development, testing patterns
- **argocd-management** - GitOps workflows, Application CR patterns, never manual kubectl
- **vault-secrets** - Initialization, unsealing, External Secrets Operator integration

### Commands

- `/disk-cleanup` - Clean Docker build cache in Minikube to free disk space (240GB+)

## Installation

```bash
/plugin marketplace add ~/claude-plugins
/plugin install nk-devops-tools@nkennedy-personal
```

## Usage

### Automatic Best Practices

The skills automatically provide guidance for:

**Helm:**
- Use `helm dependency update` (not `build`)
- Run `make check-deps` before committing
- Pre-commit hooks handle dependency rebuilds

**ArgoCD:**
- Only `kubectl apply -f` for ArgoCD Application CRs
- Let ArgoCD handle all application resources
- Git as single source of truth

**Vault:**
- `make vault-init` for initialization (saves keys to `vault-init/`)
- `make vault-unseal` required after pod restarts
- Never commit Vault keys or tokens
- External Secrets Operator manages Kubernetes Secrets

### Disk Cleanup

Free 240GB+ from Minikube build cache:
```bash
/disk-cleanup
```

## Key Patterns

### Helm Workflow
```bash
vim Chart.yaml
helm dependency update
make check-deps
git commit
```

### ArgoCD GitOps
```bash
# 1. Update git
git push

# 2. ArgoCD syncs automatically

# 3. Verify (read-only)
kubectl get pods
```

### Vault Lifecycle
```bash
# First time
make vault-init

# After pod restart
make vault-unseal
```

## Security Reminders

- Never commit `vault-init/` directory
- Use External Secrets Operator for K8s secrets
- Store unseal keys securely offline
- Rotate secrets regularly
