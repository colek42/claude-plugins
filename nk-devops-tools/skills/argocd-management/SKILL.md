# ArgoCD Management Best Practices

This skill provides ArgoCD application management patterns.

## When to Use

Activates when:
- Working with ArgoCD-managed applications
- Creating or modifying Kubernetes resources in ArgoCD repos
- Deploying applications via ArgoCD

## Core Principle

**Never manually create/modify Kubernetes resources when using ArgoCD.**

ArgoCD manages the lifecycle of your Kubernetes resources. Manual kubectl operations will be overwritten by ArgoCD's sync process.

## The ArgoCD Way

### Creating Resources

❌ **Wrong - Manual kubectl:**
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

✅ **Correct - ArgoCD Application CR:**
```bash
# Only kubectl apply for ArgoCD Application CRs
kubectl apply -f argocd-application.yaml
```

Then let ArgoCD handle the actual application resources.

### Application CR Pattern

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo
    targetRevision: HEAD
    path: k8s/manifests
  destination:
    server: https://kubernetes.default.svc
    namespace: my-app
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Workflow

### 1. Update Source Repository
```bash
# Modify your Kubernetes manifests or Helm charts in git
git add k8s/
git commit -m "update deployment configuration"
git push
```

### 2. Let ArgoCD Sync
```bash
# ArgoCD automatically detects changes and syncs

# Or manually trigger sync
argocd app sync my-app

# Check sync status
argocd app get my-app
```

### 3. Verify Deployment
```bash
# Use kubectl for read-only operations
kubectl get pods -n my-app
kubectl logs -n my-app deployment/my-app
kubectl describe deployment -n my-app my-app
```

## ArgoCD CLI Commands

### Application Management
```bash
# List applications
argocd app list

# Get application details
argocd app get my-app

# Sync application
argocd app sync my-app

# Check sync status
argocd app wait my-app --health

# View application logs
argocd app logs my-app

# Diff current state vs desired
argocd app diff my-app
```

### Debugging
```bash
# See why sync failed
argocd app get my-app

# View events
kubectl get events -n my-app

# Check ArgoCD controller logs
kubectl logs -n argocd deployment/argocd-application-controller
```

## Best Practices

✅ **Do:**
- Use `kubectl apply -f` ONLY for ArgoCD Application CRs
- Let ArgoCD handle all application resources
- Use git as the single source of truth
- Use automated sync policies for continuous deployment
- Use read-only kubectl commands for debugging

❌ **Don't:**
- Manually create/modify Kubernetes resources with kubectl
- Edit resources directly with `kubectl edit`
- Use `kubectl apply` for app resources in ArgoCD-managed namespaces
- Fight with ArgoCD by manually changing resources

## GitOps Workflow

1. **Code Change** → Commit to git repository
2. **ArgoCD Detects** → Automatic or manual sync trigger
3. **ArgoCD Applies** → Resources created/updated in cluster
4. **ArgoCD Monitors** → Health and sync status tracked
5. **Self-Heal** → Auto-corrects manual changes (if enabled)

## Emergency Override

If you absolutely must make a manual change:

```bash
# 1. Pause auto-sync temporarily
argocd app set my-app --sync-policy none

# 2. Make your manual change
kubectl apply -f emergency-fix.yaml

# 3. Update git to match your change
git add k8s/emergency-fix.yaml
git commit -m "emergency fix applied"
git push

# 4. Re-enable auto-sync
argocd app set my-app --sync-policy automated
```

**But prefer:** Make the change in git first, then let ArgoCD apply it.
