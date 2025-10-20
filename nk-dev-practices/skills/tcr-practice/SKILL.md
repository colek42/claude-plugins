# TCR: Test && Commit || Revert

TCR (Test && Commit || Revert) is "TDD on steroids" - a practice that forces truly tiny steps and yields high coverage by design.

## When to Use

Activate during:
- Katas and practice sessions
- Refactoring existing code
- Pure TDD work with fast test suites
- Mob/ensemble programming sessions
- Training others in baby-step programming

**When TCR reverts code:** Automatically prompt to document the failure using `/tcr-log-failure` command.

## What is TCR?

TCR replaces the test command with:

```bash
<test command> && git commit -am "TCR" || git restore.
```

**If tests pass → Auto-commit**
**If tests fail → Auto-revert**

You literally cannot save failing code. This forces you to work in the smallest possible increments.

## The Flow

### Standard TCR (Refactoring-Focused)

1. Make a tiny code change
2. Run TCR command
3. Tests pass → Code automatically committed
4. Tests fail → Code automatically reverted to last working state
5. **On revert → Document the failure** (what you tried, why it failed, what you learned)

### TRC Variant (TDD Red Phase)

For the "Red" phase of TDD, use the symmetric TRC flow:

```bash
<test command> && git revert || git commit -am "TRC"
```

**If tests pass → Revert** (you're writing a test, it should fail first)
**If tests fail → Commit** (good, your test fails as expected)

## Key Benefits

### Forces Baby Steps
> "I thought I was doing small steps, but I discovered I could make them even smaller!"

TCR teaches you to split work into truly atomic changes.

### High Coverage by Design
90%+ branch coverage naturally emerges. You cannot commit untested code because untested code fails TCR.

### Feedback on Fatigue
When you get stuck and keep reverting, it's a signal you're too tired. Stop and rest.

### Learning from Failures
Every revert is a teaching moment. Document what you tried and why it failed to build pattern recognition.

### Seamless Remote Mobbing
TCR + git push creates automatic git-handover for remote mob programming:
- Every change is committed and pushed
- Next person pulls and continues
- No manual handover ceremony needed

### Sustainable Pace
- Less tiring than traditional development
- Clear stopping points (every commit)
- No fear of losing work (it's all committed)

## Getting Started

### Start with Katas

Don't jump into production code. Practice TCR on a kata first:

```bash
# Initialize git
git init

# Run your TCR script
./run-tests && git commit -am "TCR" || git restore.
```

### Start with Refactoring Only

Use TCR only during the "Refactor" phase of Red-Green-Refactor:
- Write test (normal way)
- Make it pass (normal way)
- **Refactor with TCR** ← Start here

### Challenges You'll Face

**"Oh no, I'm going to lose my code!"**

Yes, you will. That's the point. You'll learn to:
- Make smaller changes
- Trust your tests more
- Work more sustainably

**"I can't see my tests go red!"**

Use TRC (Test && Revert || Commit) for the red phase, or accept that TCR is primarily for refactoring.

**"I have so many commit messages to write!"**

Use a simple message like "TCR" or "WIP" during the session. Squash and rewrite the commit history when done.

## Common Mistakes

### Don't Cheat!

Your IDE is just a CTRL+Z away from recovering reverted code. **Don't do it.**

If TCR reverted your code, there's a reason. Stop and think. Document why it failed. Make a smaller step.

### Don't Ignore Failures

Each revert teaches you something:
- **Immediate documentation:** Write down what failed and why (comment, note, or commit message when you succeed)
- **Pattern recognition:** "I always fail when I try to X and Y together - I need to split them"
- **Step size calibration:** "This type of change needs 3 smaller steps, not 1"

**Create a failure log:**
```markdown
# TCR Failure Log

## 2025-01-20 14:30 - Attempted refactoring

**What I tried:** Extract validation logic and rename variables in one step
**Why it failed:** Tests broke because of variable name mismatch
**What I learned:** Extract first, rename second - two separate steps
**Next time:** Always extract with existing names, then rename separately
```

### Don't Push Through Fatigue

When you start reverting repeatedly:
1. **Document the pattern** - Write down what keeps failing
2. You're too tired OR your steps are too big
3. Review your failure log to see if there's a pattern
4. Stop for the day or take a different approach

### Don't Skip the Practice Phase

Don't use TCR on production code without practicing on katas first. You need to develop the muscle memory for tiny steps.

## Advanced: TCRDD (TCR with Deliberate Documentation)

Combine TCR with betting and learning:
1. Make a change
2. **Bet** on whether tests will pass or fail
3. Run TCR
4. **If you lost the bet:** Document why you were wrong
5. See patterns in your failed bets

This builds:
- Confidence in your code
- Understanding of what "safe changes" look like
- A failure catalog you can learn from

**Enhanced failure documentation:**
```markdown
# TCR Session: Refactoring UserAuth

## Bet Results
- ✅ Pass bet: Renamed parameter (confidence: high)
- ✅ Pass bet: Extracted constant (confidence: high)
- ❌ Fail bet: Inlined helper function (confidence: medium)
  - **Why I thought it would pass:** Function was only used once
  - **Why it failed:** Tests depended on the helper being mockable
  - **Learning:** Check test doubles before inlining

## Patterns Observed
- Renaming is safe (3/3 passed)
- Inlining needs test review first (0/1 passed)
```

## Tools

### Simple Script
```bash
#!/bin/bash
# Save as tcr.sh and chmod +x

<your test command> && git commit -am "TCR $(date +%H:%M:%S)" || git restore.
```

### Watch Mode
```bash
#!/bin/bash
# Run TCR automatically on file changes

watch_files() {
    while inotifywait -r -e modify,create,delete src/ test/; do
        ./tcr.sh
    done
}

watch_files
```

### Open Source Options
- Thomas Deniffel's shell script variations
- Xavier's TCRDD tool (bet on tests, see failures)
- Lars Eckart's JUnit 5 extension
- Murex TCR tool (cross-language, remote mobbing)

## TCR Philosophy

### "Test-Driven Development is a way of managing fear during programming." - Kent Beck

TCR amplifies this. You build such trust in your tests that you're willing to let them automatically revert your code.

### "You're bound to learn something."

TCR is an experiment. Try it. Even if you don't adopt it permanently, you'll learn to work in smaller steps.

### Continuous Integration by Design

Every change is committed immediately. Your code is always integrated. Your team can see your work in progress at any moment.

## When NOT to Use TCR

❌ **Avoid TCR when:**
- Tests are slow (>5 seconds)
- You're learning a new domain/codebase
- You're exploring or spiking
- You're doing big design changes

✅ **Use TCR when:**
- Tests are fast (<2 seconds)
- You're refactoring
- You're implementing well-understood features
- You're practicing or training
- You're mob programming remotely

## The TCR Promise

If you stick with TCR through the initial discomfort:
- You'll discover steps can be smaller than you thought possible
- You'll build unshakeable trust in your tests
- You'll work at a sustainable, less tiring pace
- You'll naturally achieve 90%+ coverage
- You'll integrate continuously without thinking about it
- **You'll build a catalog of learned patterns from documented failures**

## Failure Documentation Template

Create a `TCR-LEARNINGS.md` file in your project:

```markdown
# TCR Learnings

## Success Patterns
- Renaming variables: Always succeeds if tests are good
- Extracting constants: Safe 95% of the time
- Moving pure functions: Safe if no test dependencies

## Failure Patterns
- Combining extraction + rename: Always fails - do separately
- Refactoring without reading tests first: 70% failure rate
- Changes after 5pm: Fatigue-induced failures increase 3x

## Step Size Calibration
- **Too small:** Changing a single character (wastes time)
- **Just right:** One logical micro-change (rename, extract, inline)
- **Too big:** Refactor + behavior change together (always fails)

## Time-of-Day Patterns
- Morning (8-10am): Largest safe steps, <10% revert rate
- Afternoon (2-4pm): Medium steps needed, ~20% revert rate
- Evening (6-8pm): Tiny steps only, 40%+ revert rate → Stop!

## Notes
- When I get 3 reverts in a row: Take a 10-minute break
- When uncertain: Bet "fail" and make an even smaller step
- Review this file weekly to reinforce patterns
```

Try it. Be patient. Document failures. You might hate it at first. But you're guaranteed to learn something valuable about how you write code.
