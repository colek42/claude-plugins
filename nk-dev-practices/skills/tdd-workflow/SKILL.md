# Test-Driven Development (TDD) Best Practices

This skill guides rigorous test-first development following the Red-Green-Refactor cycle.

## When to Use

Activate when:
- Implementing new features
- Fixing bugs
- Refactoring existing code
- Making any code changes

## TDD Core Principles

### Red-Green-Refactor Cycle
1. **Red** - Write tests FIRST before implementation
2. **Green** - Write minimal code to pass tests
3. **Refactor** - Clean up while keeping tests green

### Test Quality Standards

**Write Tests First:**
- Tests should be minimal and focused on single behaviors
- Tests are documentation - they clearly show expected behavior
- If you can't easily test it, the design is wrong - refactor for testability

**Test Organization:**
- Use table-driven tests for multiple inputs/scenarios in Go
- Test file naming: `*_test.go` for unit tests, `e2e_test.go` for integration
- Always test error cases and edge conditions

**Test Types:**
- **Unit tests** - Mock external dependencies (network, filesystem, time)
- **Integration tests** - Validate real component interactions
- **End-to-end tests** - Cover critical user workflows

### Assertion Libraries

**Go Testing:**
- Use `testify/require` for assertions that should stop test execution
- Use `testify/assert` for assertions that should continue test execution

## Design for Testability

✅ **Testable patterns:**
- Dependency injection
- Interface-based abstractions
- Pure functions
- Isolated side effects

❌ **Hard to test (redesign):**
- Global state
- Hidden dependencies
- Tight coupling
- Side effects mixed with logic

## TDD Workflow

1. Write failing test(s) embodying acceptance criteria
2. Run tests - verify they fail for the right reason
3. Implement minimal code to make tests pass
4. Run tests - verify they all pass
5. Refactor for quality while keeping tests green
6. Repeat

## Quality Gates

Before considering work "done":
- [ ] All tests pass locally and in CI
- [ ] Coverage ≥ 90% lines/branches
- [ ] Error cases are tested
- [ ] Edge conditions are tested
- [ ] Tests document expected behavior clearly
