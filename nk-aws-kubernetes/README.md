# NK AWS & Kubernetes Plugin

AWS profile management and kubectl context configuration for Judge platform work.

## What's Included

### Skills

- **aws-judge-setup** - Automatic AWS profile and kubectl context management for Judge demo cluster

### Commands

- `/judge-context` - Set up AWS and Kubernetes context for Judge platform work

## Installation

```bash
/plugin marketplace add ~/claude-plugins
/plugin install nk-aws-kubernetes@nkennedy-personal
```

## Usage

### Automatic Context Management

The aws-judge-setup skill automatically:
- Ensures `AWS_PROFILE=conda-demo` is set for AWS/Terraform commands
- Verifies kubectl context points to demo-judge cluster
- Prefixes AWS commands appropriately

### Manual Setup

Use the `/judge-context` command to manually configure your environment:

```bash
/judge-context
```

## Configuration Details

- **AWS Profile**: `conda-demo` (demo account)
- **kubectl Context**: `arn:aws:eks:us-east-1:831646886084:cluster/demo-judge`
- **Cluster**: demo-judge EKS cluster in us-east-1
