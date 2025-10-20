# NK Dev Practices Plugin

Core development philosophy and practices for Cole Kennedy's development workflow.

## What's Included

### Skills

- **critical-thinking** - Linus Torvalds mindset, self-skepticism, red-team analysis
- **tdd-workflow** - Test-Driven Development best practices and Red-Green-Refactor cycle
- **tcr-practice** - Test && Commit || Revert - "TDD on steroids" for baby-step programming
- **no-permission-asking** - Maintain momentum, keep going without unnecessary permission requests

### Commands

- `/tcr-setup` - Set up TCR (Test && Commit || Revert) for the current project
- `/tcr-log-failure` - Document a TCR failure to build pattern recognition

## Installation

```bash
/plugin marketplace add ~/claude-plugins
/plugin install nk-dev-practices@nkennedy-personal
```

## Usage

These skills activate automatically based on context:
- TDD workflow activates during implementation tasks
- TCR practice activates when using TCR (and reminds to document failures)
- Critical thinking activates during design and review discussions
- No-permission-asking is always active to maintain momentum

**Special TCR behavior:** When TCR reverts your code, the skill will prompt you to use `/tcr-log-failure` to document what happened and build pattern recognition.

## Philosophy

This plugin embodies:
- **Extraordinary skepticism** of your own correctness
- **Test-first development** - Red, Green, Refactor
- **TCR for baby steps** - Test && Commit || Revert forces truly tiny increments
- **Critical analysis** over emotional validation
- **Continuous forward motion** without asking for permission
- **Technical accuracy** over false agreement
- **Sustainable pace** through small, committed steps
