# AWS & Kubernetes Environment Setup for Judge

This skill ensures correct AWS and Kubernetes context before working on Judge platform tasks.

## When to Use

Automatically activates when:
- Working with Judge platform code
- Running AWS CLI or Terraform commands
- Executing kubectl commands
- Starting work on demo-judge cluster

## Critical Setup Command

**IMPORTANT: Always run this before starting Claude Code for Judge platform work:**

```bash
export AWS_PROFILE=conda-demo && kubectl config use-context arn:aws:eks:us-east-1:831646886084:cluster/demo-judge
```

This ensures:
- AWS CLI & Terraform use the `conda-demo` profile (demo account)
- kubectl commands target the `demo-judge` EKS cluster
- All agent commands will use the correct AWS account and Kubernetes context

## Command Prefixes

When executing commands in Judge context:

- **AWS/Terraform commands**: Always prefix with `AWS_PROFILE=conda-demo`
  ```bash
  AWS_PROFILE=conda-demo terraform plan
  AWS_PROFILE=conda-demo aws s3 ls
  ```

- **kubectl commands**: No prefix needed (context already set to demo-judge)
  ```bash
  kubectl get pods -n judge
  kubectl logs -n judge deployment/judge-api
  ```

## Verification

Before executing AWS or kubectl commands, verify:

```bash
# Check AWS profile
echo $AWS_PROFILE  # Should output: conda-demo

# Check kubectl context
kubectl config current-context  # Should output: arn:aws:eks:us-east-1:831646886084:cluster/demo-judge
```

## Auto-Configuration

When this skill is active, Claude will:
1. Verify AWS_PROFILE and kubectl context before AWS/kubectl commands
2. Automatically prefix AWS/Terraform commands with `AWS_PROFILE=conda-demo`
3. Warn if context appears incorrect for Judge platform work
4. Suggest re-running the setup command if needed
