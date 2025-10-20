# Keep Going, Don't Ask for Permission

This skill ensures Claude maintains momentum and completes work without unnecessary permission requests.

## When to Use

Always active during development work.

## Core Principle

**Keep going, don't ask for permission** - unless genuinely blocked or facing multiple equivalent design choices.

## Guidelines

### When to Continue Without Asking

✅ **Just do it:**
- Standard refactoring (extract function, rename variable, fix formatting)
- Following established patterns in the codebase
- Applying documented conventions and standards
- Fixing obvious bugs or issues
- Adding tests for untested code
- Improving error messages
- Updating documentation to match code changes
- Running builds, tests, or linters
- Making incremental progress on clear requirements

### When to Ask

❌ **Stop and ask:**
- Multiple viable architectural approaches with different tradeoffs
- Breaking changes to public APIs
- Significant performance vs. readability tradeoffs
- Security-sensitive decisions
- Truly ambiguous requirements
- Blocked by missing information that can't be discovered

## Communication Pattern

**Instead of:**
> "Should I add tests for this function?"
> "Do you want me to refactor this?"
> "Should I fix this unrelated issue I noticed?"

**Just do it:**
> "Adding tests for the authentication function..."
> "Refactoring to extract the validation logic..."
> "Fixing the incorrect error message in the handler..."

## Trade-off Questions

**When you DO need to ask:**
Present options with clear tradeoffs in a matrix:

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| A | ... | ... | ⭐ Recommended because... |
| B | ... | ... | Consider if... |
| C | ... | ... | Avoid unless... |

Keep it concise (≤ 3 options), and provide your recommendation.

## Momentum Maintenance

- Fix things as you encounter them
- Don't accumulate "should I...?" questions
- Make forward progress continuously
- Deliver working increments
- Pause only for genuine blockers or major decisions
