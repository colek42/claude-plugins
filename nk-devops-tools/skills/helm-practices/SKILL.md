# Helm Best Practices

This skill provides Helm chart development and maintenance patterns.

## When to Use

Activates when:
- Working with Helm charts
- Modifying Chart.yaml dependencies
- Updating Helm values
- Deploying applications with Helm

## Dependency Management

### Critical Rules

**Always use `helm dependency update`** - NOT `helm dependency build`

```bash
# Correct
helm dependency update

# Wrong - Don't use this
helm dependency build
```

**After changing Chart.yaml dependencies:**

1. Run `helm dependency update` to fetch updated dependencies
2. Run `make check-deps` before committing changes
3. Pre-commit hooks automatically rebuild dependencies

### Common Workflow

```bash
# 1. Modify Chart.yaml
vim Chart.yaml

# 2. Update dependencies
helm dependency update

# 3. Check dependencies
make check-deps

# 4. Commit changes (pre-commit hook runs automatically)
git add Chart.yaml Chart.lock charts/
git commit -m "update helm dependencies"
```

## Helm Commands

### Testing Charts

```bash
# Template and check output
helm template <release-name> <chart-path>

# Template with specific values
helm template <release-name> <chart-path> -f values.yaml

# Dry-run install
helm install <release-name> <chart-path> --dry-run --debug
```

### Debugging

```bash
# Check current values
helm get values <release-name>

# Check all computed values
helm get values <release-name> --all

# Get manifest
helm get manifest <release-name>
```

## Best Practices

### Chart Structure
- Keep templates focused and modular
- Use helpers (`_helpers.tpl`) for repeated logic
- Document all values in `values.yaml` with comments
- Use semantic versioning for chart versions

### Values Organization
- Use nested structures for related values
- Provide sensible defaults
- Document required vs optional values
- Use `.Values` consistently

### Dependency Management
- Pin dependency versions explicitly
- Use repository URLs, not local paths in production
- Keep `Chart.lock` in version control
- Run `make check-deps` before committing

## Common Gotchas

❌ **Don't:**
- Use `helm dependency build` (use `update` instead)
- Forget to run `make check-deps` before committing
- Commit without running pre-commit hooks
- Hard-code values that should be configurable

✅ **Do:**
- Use `helm dependency update` for dependency changes
- Run `make check-deps` as part of your workflow
- Let pre-commit hooks rebuild dependencies automatically
- Make values configurable and well-documented
