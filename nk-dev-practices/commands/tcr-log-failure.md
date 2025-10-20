---
description: Document a TCR failure to build pattern recognition and learning
---

# Log TCR Failure

Document what you tried, why it failed, and what you learned when TCR reverts your code.

## Purpose

Every TCR revert is a teaching moment. Documenting failures helps you:
- Calibrate step sizes
- Recognize patterns in what fails
- Build confidence in what's safe
- Track fatigue-related failures
- Learn your personal coding patterns

## Usage

When TCR reverts your code, immediately document:

1. **What you tried** - Describe the change you attempted
2. **Why it failed** - What test broke or error occurred
3. **What you learned** - Pattern or insight gained
4. **Next step** - How you'll break it down smaller

## Log File

Creates or appends to `TCR-LEARNINGS.md` in current directory.

## Template

```markdown
## [Date] [Time] - [Brief description]

**What I tried:** [The change you attempted]

**Why it failed:** [Test failure, error message, or behavior]

**What I learned:** [Pattern or insight]

**Next time:** [How to avoid or what to do differently]

**Step size:** Too big | Just right but timing wrong | Other: [explain]

**Time of day:** [Morning/Afternoon/Evening - track fatigue patterns]

---
```

## Example

```markdown
## 2025-01-20 14:30 - Extract validation and rename together

**What I tried:** Extract email validation to helper function AND rename emailAddr to email

**Why it failed:** Tests failed because they expected old variable name in error messages

**What I learned:** Extract and rename are two separate steps, even if they feel related

**Next time:**
1. Extract with existing names first
2. Verify tests pass
3. THEN rename in a second TCR cycle

**Step size:** Too big - combined two logical changes

**Time of day:** Early afternoon (2:30pm) - moderate fatigue

**Pattern:** This is the 3rd time I've failed combining extract + rename. Need to internalize this!

---
```

## Auto-Generation

If `$ARGUMENTS` provided, use as brief description. Otherwise, prompt for:
- What you tried
- Why it failed
- What you learned

Then append to `TCR-LEARNINGS.md` with template filled in.

## Review Your Log

Periodically review your `TCR-LEARNINGS.md` to:
- Identify recurring failure patterns
- Calibrate your step sizes
- Recognize fatigue indicators
- Build confidence in safe changes

Execute the logging and confirm the entry was added to the file.
