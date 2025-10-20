# NK Go Development Plugin

Go-specific TDD patterns, testing conventions, and test execution helpers.

## What's Included

### Skills

- **go-tdd-patterns** - Table-driven tests, testify usage, mock patterns, integration tests

### Commands

- `/go-test-single` - Run a single Go test by name with verbose output

## Installation

```bash
/plugin marketplace add ~/claude-plugins
/plugin install nk-go-development@nkennedy-personal
```

## Usage

### Automatic TDD Guidance

The go-tdd-patterns skill automatically provides:
- Table-driven test structures
- Proper use of `require` vs `assert`
- Mock setup patterns
- Integration test organization
- Error case testing

### Test Execution

Run single tests easily:
```bash
/go-test-single TestMyFunction
```

## Key Patterns

### Table-Driven Tests
Used for multiple scenarios with structured test cases

### Testify Assertions
- `require.*` - Stop on failure (prerequisites)
- `assert.*` - Continue on failure (multiple checks)

### Coverage Standards
- Minimum 90% lines and branches
- Every exported function tested
- Error cases explicitly tested

### Integration Tests
- Use `//go:build integration` tag
- Run with `-tags=integration`
- Test real component interactions
