# Vault & Secrets Management

This skill provides HashiCorp Vault best practices for secrets management.

## When to Use

Activates when:
- Working with secrets in Kubernetes
- Managing Vault initialization and unsealing
- Using External Secrets Operator
- Setting up new environments

## Vault Lifecycle

### Initialization

**Command:** `make vault-init`

This initializes a new Vault instance and saves keys to `vault-init/` directory.

```bash
# Initialize Vault (first time only)
make vault-init

# Keys are saved to vault-init/ directory:
# - vault-init/unseal-key-1
# - vault-init/unseal-key-2
# - vault-init/unseal-key-3
# - vault-init/root-token
```

### Unsealing

**Command:** `make vault-unseal`

Required after pod restarts. Vault starts in a sealed state and must be unsealed with keys.

```bash
# Unseal Vault (after pod restart)
make vault-unseal
```

**Why unsealing is needed:**
- Vault pods restart (manual restart, node failure, updates)
- Vault starts sealed for security
- Must provide unseal keys to make Vault operational

## Security Best Practices

### Never Commit Vault Keys or Tokens

❌ **Don't:**
```bash
# Don't commit these files
git add vault-init/
git commit -m "vault keys"  # NEVER DO THIS
```

✅ **Do:**
```bash
# Ensure vault-init/ is in .gitignore
echo "vault-init/" >> .gitignore

# Store keys securely offline
# - Password manager
# - Encrypted backup
# - Secure key management system
```

### Secrets in Code

❌ **Don't:**
```go
// Don't hardcode secrets
const apiKey = "sk-1234567890abcdef"
password := "supersecret123"
```

✅ **Do:**
```go
// Use environment variables from Vault
apiKey := os.Getenv("API_KEY")

// Or use External Secrets Operator
// which automatically creates k8s Secrets from Vault
```

## External Secrets Operator

**External Secrets Operator manages Kubernetes Secret creation from Vault.**

### How It Works

1. Secrets stored in Vault
2. ExternalSecret CR references Vault path
3. ESO fetches secret from Vault
4. ESO creates/updates Kubernetes Secret automatically

### Example ExternalSecret

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: app-secrets
    creationPolicy: Owner
  data:
    - secretKey: api-key
      remoteRef:
        key: secret/data/app
        property: api_key
```

This creates a Kubernetes Secret named `app-secrets` with data from Vault.

## Common Workflows

### Storing a New Secret

```bash
# 1. Write secret to Vault
vault kv put secret/myapp/config \
  api_key=abc123 \
  db_password=secretpass

# 2. Create ExternalSecret CR
kubectl apply -f external-secret.yaml

# 3. Verify Kubernetes Secret was created
kubectl get secret app-secrets
kubectl describe secret app-secrets
```

### Rotating a Secret

```bash
# 1. Update secret in Vault
vault kv put secret/myapp/config api_key=newkey123

# 2. ESO automatically syncs (based on refreshInterval)
# Or manually trigger sync by deleting the k8s Secret
kubectl delete secret app-secrets

# 3. ESO recreates Secret with new value
kubectl get secret app-secrets -o yaml
```

### Debugging Secrets

```bash
# Check Vault status
kubectl exec -it vault-0 -- vault status

# Check if Vault is sealed
kubectl logs vault-0 | grep sealed

# Check External Secrets Operator
kubectl logs -n external-secrets deployment/external-secrets

# Check ExternalSecret status
kubectl describe externalsecret app-secrets
```

## Vault Initialization Checklist

When setting up Vault in a new environment:

- [ ] Run `make vault-init` to initialize Vault
- [ ] Securely save unseal keys and root token from `vault-init/`
- [ ] Add `vault-init/` to `.gitignore`
- [ ] Run `make vault-unseal` to unseal Vault
- [ ] Configure Vault policies and auth methods
- [ ] Set up External Secrets Operator integration
- [ ] Test secret retrieval and rotation

## Pod Restart Recovery

When Vault pods restart:

```bash
# 1. Check Vault status
kubectl get pods -l app=vault

# 2. Vault will be sealed - check logs
kubectl logs vault-0 | tail -20

# 3. Unseal Vault
make vault-unseal

# 4. Verify Vault is operational
kubectl exec vault-0 -- vault status
```

## Best Practices Summary

✅ **Do:**
- Initialize Vault with `make vault-init`
- Unseal Vault after restarts with `make vault-unseal`
- Use External Secrets Operator for Kubernetes secrets
- Store unseal keys securely offline
- Never commit Vault keys to git
- Rotate secrets regularly

❌ **Don't:**
- Commit vault-init/ directory to git
- Hardcode secrets in code
- Manually create Kubernetes Secrets for Vault-backed data
- Leave Vault sealed
- Share root token unnecessarily
