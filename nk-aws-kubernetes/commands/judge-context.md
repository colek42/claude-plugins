---
description: Set up AWS and Kubernetes context for Judge platform work
---

# Judge Context Setup

Run the environment setup command to configure AWS profile and kubectl context for Judge platform work:

```bash
export AWS_PROFILE=conda-demo && kubectl config use-context arn:aws:eks:us-east-1:831646886084:cluster/demo-judge
```

Then verify the configuration:

```bash
echo "AWS Profile: $AWS_PROFILE"
kubectl config current-context
kubectl get nodes
```

Explain what was configured and confirm readiness for Judge platform work.
