---
description: Run a single Go test by name with verbose output
---

# Run Single Go Test

Run a specific Go test function. Provide the test name and optionally the package path.

**Usage:**
```bash
# Test in current directory
go test -v -run $ARGUMENTS

# Test in specific package
go test -v ./path/to/package -run $ARGUMENTS

# With failfast
go test -v --failfast -run $ARGUMENTS
```

Ask for the test name if not provided in the request, then execute the test with verbose output and show the results.
