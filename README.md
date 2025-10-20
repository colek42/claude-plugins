# Cole Kennedy's Claude Code Plugin System

Modular, composable plugins for development workflows across all projects.

## Overview

This plugin system provides:
- **Personal plugins** - Reusable development practices across all projects
- **Project-specific plugins** - Auto-installed when working in specific repos
- **Skill-based activation** - Claude automatically uses relevant skills based on context
- **Command shortcuts** - Quick access to common workflows

## Personal Marketplace

Location: `~/claude-plugins/`

### Available Plugins

#### nk-dev-practices
Core development philosophy and practices.

**Skills:**
- `critical-thinking` - Linus Torvalds mindset, self-skepticism, red-team analysis
- `tdd-workflow` - Test-Driven Development, Red-Green-Refactor cycle
- `tcr-practice` - Test && Commit || Revert for baby-step programming
- `no-permission-asking` - Maintain momentum without unnecessary permission requests

**Commands:**
- `/tcr-setup` - Set up TCR for current project

#### nk-aws-kubernetes
AWS profile and kubectl context management.

**Skills:**
- `aws-judge-setup` - Automatic AWS/kubectl configuration for Judge platform

**Commands:**
- `/judge-context` - Set up AWS and kubectl context for Judge work

#### nk-go-development
Go-specific TDD patterns and testing.

**Skills:**
- `go-tdd-patterns` - Table-driven tests, testify usage, mock patterns

**Commands:**
- `/go-test-single` - Run single Go test by name

#### nk-devops-tools
Helm, ArgoCD, Vault best practices.

**Skills:**
- `helm-practices` - Dependency management, chart development
- `argocd-management` - GitOps workflows, never manual kubectl
- `vault-secrets` - Initialization, unsealing, External Secrets Operator

**Commands:**
- `/disk-cleanup` - Free 240GB+ from Minikube build cache

## Installation

### 1. Add Personal Marketplace

```bash
/plugin marketplace add ~/claude-plugins
```

### 2. Install Personal Plugins

```bash
/plugin install nk-dev-practices@nkennedy-personal
/plugin install nk-aws-kubernetes@nkennedy-personal
/plugin install nk-go-development@nkennedy-personal
/plugin install nk-devops-tools@nkennedy-personal
```

### 3. Project-Specific Plugins

Project plugins (like Judge team plugins) auto-install when you:
1. Have the project repo in your trust list
2. The project has `.claude/settings.json` configured

## Usage

### Skills Auto-Activate

Skills automatically activate based on context:
- Working in Go → `go-tdd-patterns` activates
- Writing GraphQL → Judge `graphql-conventions` activates
- Using Helm → `helm-practices` and `argocd-management` activate
- Always active: `critical-thinking`, `tdd-workflow`, `no-permission-asking`

### Commands Are Explicit

Use slash commands when you need them:
- `/tcr-setup` - Set up Test && Commit || Revert
- `/judge-context` - Configure AWS/kubectl for Judge
- `/go-test-single TestName` - Run specific test
- `/disk-cleanup` - Free Minikube disk space

## Project-Specific Plugins

### Judge Team Marketplace

Location: `~/proj/judge/.claude-plugins/`

Auto-installs when working in Judge repo with these plugins:

#### judge-platform
- GraphQL conventions (PascalCase operations, `make generate`)
- Dapr workflow patterns (deterministic orchestrators, idempotent activities)
- Build/test/lint commands

#### judge-compliance
- Compliance API patterns (frameworks, controls, directives, policies)
- SSP generation with native Dapr activities
- GRC document management

#### judge-helm-agents
- `helm-implementor` agent - Make production-ready Helm changes
- `helm-reviewer` agent - Audit charts for anti-patterns

#### judge-pair-programming
- Git commit conventions (lowercase, conventional commits)
- XP workflow (Red-Green-Refactor, completion checklist)

## Philosophy

### Composability

Mix personal + project plugins:
```
Personal plugins (always active)
  + nk-dev-practices (critical thinking, TDD, TCR)
  + nk-go-development (Go testing patterns)
  + nk-devops-tools (Helm, Vault, ArgoCD)

Project plugins (when in Judge repo)
  + judge-platform (GraphQL, Dapr)
  + judge-compliance (SSP, OSCAL)
  + judge-helm-agents (Helm implementor/reviewer)
  + judge-pair-programming (Git, XP workflow)
```

### Modularity

Each plugin is independent and focused:
- Install only what you need
- Disable plugins per-project
- Version plugins independently

### Team Sharing

Project plugins checked into git:
- Team automatically gets same configuration
- Consistent practices across team
- Version-controlled and documented

## Directory Structure

```
~/claude-plugins/                          # Personal marketplace
├── .claude-plugin/
│   └── marketplace.json
├── nk-dev-practices/
│   ├── .claude-plugin/plugin.json
│   ├── skills/
│   │   ├── critical-thinking/SKILL.md
│   │   ├── tdd-workflow/SKILL.md
│   │   ├── tcr-practice/SKILL.md
│   │   └── no-permission-asking/SKILL.md
│   ├── commands/
│   │   └── tcr-setup.md
│   └── README.md
├── nk-aws-kubernetes/
├── nk-go-development/
└── nk-devops-tools/

~/proj/judge/.claude-plugins/              # Judge team marketplace
├── .claude-plugin/
│   └── marketplace.json
├── judge-platform/
├── judge-compliance/
├── judge-helm-agents/
└── judge-pair-programming/
```

## Managing Plugins

### List Installed Plugins

```bash
/plugin
```

### Enable/Disable Plugins

```bash
/plugin enable plugin-name@marketplace-name
/plugin disable plugin-name@marketplace-name
```

### Update Plugins

Plugins update automatically when you pull changes from git (for project plugins) or update files (for personal plugins).

Restart Claude Code to load updates:
```bash
ccr restart
```

## Best Practices

### Personal Plugins

- Keep general-purpose and reusable
- Don't include project-specific details
- Version carefully (semver)

### Project Plugins

- Include team-shared practices
- Check into version control
- Document in project README
- Configure auto-install in `.claude/settings.json`

### Skill Design

- Clear activation triggers
- Concise and actionable
- Include examples
- Explain why, not just what

### Command Design

- Single responsibility
- Clear parameter handling
- Helpful descriptions
- Idempotent when possible

## Troubleshooting

### Plugin Not Activating

1. Check plugin is installed: `/plugin`
2. Verify plugin is enabled
3. Restart Claude Code: `ccr restart`

### Skills Not Triggering

- Skills activate based on context
- Check skill's "When to Use" section
- Some skills are always active (e.g., critical-thinking)

### Project Plugins Not Auto-Installing

1. Ensure project repo is in trust list
2. Check `.claude/settings.json` exists
3. Verify marketplace source path is correct
4. Restart Claude Code

## Advanced Usage

### Creating Custom Plugins

1. Create plugin directory structure
2. Add plugin.json manifest
3. Create skills/ and/or commands/ directories
4. Add to marketplace.json
5. Install and test

See existing plugins for examples.

### Plugin Hooks

Configure hooks in plugin's `.claude-plugin/hooks.json` for:
- Pre/post tool use
- File change triggers
- Custom validations

## Version History

- **v1.0.0** (2025-01-20) - Initial plugin system
  - 4 personal plugins
  - 4 Judge team plugins
  - Auto-installation configured

## Contributing

To add new plugins or improve existing ones:
1. Create/modify plugin in appropriate marketplace
2. Test thoroughly
3. Update marketplace.json
4. Document in README
5. Share with team (for project plugins)

## Support

Questions or issues:
- Personal plugins: Update yourself in `~/claude-plugins/`
- Judge plugins: Discuss with Judge team
- Claude Code issues: https://github.com/anthropics/claude-code/issues
