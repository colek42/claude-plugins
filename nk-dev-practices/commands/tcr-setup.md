---
description: Set up TCR (Test && Commit || Revert) for the current project
---

# TCR Setup

Set up TCR (Test && Commit || Revert) for practicing baby-step programming.

## Steps

1. Ensure git is initialized:
```bash
git init
```

2. Create a TCR script:
```bash
cat > tcr.sh << 'EOF'
#!/bin/bash
# TCR: Test && Commit || Revert

# Replace with your actual test command
TEST_CMD="go test -v ./... || npm test"

echo "Running TCR..."
if $TEST_CMD; then
    git add -A
    git commit -m "TCR $(date +%H:%M:%S)"
    echo "✅ Tests passed - Changes committed"
else
    git restore .
    echo "❌ Tests failed - Changes reverted"
fi
EOF

chmod +x tcr.sh
```

3. Test it:
```bash
./tcr.sh
```

## Usage

After making a tiny code change:
```bash
./tcr.sh
```

- If tests pass → Changes automatically committed
- If tests fail → Changes automatically reverted

## Tips

- Start with refactoring only (not new features)
- Make the smallest possible changes
- When you get stuck (keep reverting), take a break
- Don't cheat with CTRL+Z to recover reverted code

## Advanced: Watch Mode

Auto-run TCR on file changes:
```bash
# macOS with fswatch
fswatch -o src/ test/ | xargs -n1 -I{} ./tcr.sh

# Linux with inotifywait
while inotifywait -r -e modify src/ test/; do ./tcr.sh; done
```

Ask which test command to use, then create the TCR script and explain how to use it.
