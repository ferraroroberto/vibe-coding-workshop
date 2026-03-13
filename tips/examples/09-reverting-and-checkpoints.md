# Reverting and Checkpoints

## Idea

When an LLM enters a debugging loop — fixing one thing, breaking another — stop immediately. Extract the key insight, revert to a clean state, and restart with a targeted prompt.

## Why

Continuing a looping session:
- Compounds errors (every fix introduces new bugs).
- Wastes expensive prompts on incremental patches.
- Produces tangled, hard-to-review diffs.
- Degrades the LLM's context quality over time.

A clean restart with a clear prompt almost always outperforms 10 more rounds of patching.

## Recognizing the Loop

Signs you're in a loop:
- The LLM has tried the same approach twice.
- Fixing bug A breaks bug B, then fixing B breaks A.
- The diff is growing larger with every round.
- The LLM says "let me try a different approach" for the third time.
- You're not sure what state the codebase is in anymore.

**When you see these signs: stop immediately.**

## The Checkpoint Technique

### Phase 1: Extract the insight

Before reverting, ask:
```
We've been going in circles. Don't make any more changes.

Just tell me:
1. What is the root cause of the problem?
2. What is the correct solution approach?
3. What specific change needs to be made and where?

Don't implement anything yet. Just explain the solution clearly.
```

Save the response to `tmp/`.

### Phase 2: Revert

```bash
# Option 1: Discard all uncommitted changes
git checkout -- .

# Option 2: Revert to a specific clean commit
git log --oneline -10        # find the clean commit
git checkout <commit-hash>   # go back to that state

# Option 3: Stash changes temporarily
git stash
```

### Phase 3: Restart with the solution

Open a **new session** and start with:
```
I need to implement the following fix cleanly.

Context:
[paste the root cause + solution from Phase 1]

Current state:
[describe the file and the existing code]

Task:
Implement the solution described above. Make only the minimum
necessary change. Do not refactor or improve anything else.
```

## Example Scenario

### The Loop

You asked the LLM to add retry logic to a database connection. After 6 rounds:
- Round 1: Adds retry → breaks connection pooling
- Round 2: Fixes pooling → breaks retry count
- Round 3: Fixes retry count → breaks error handling
- Round 6: Back to original problem

**Stop. Extract the insight:**

```
Don't make any more changes. Explain:
- Why does adding retry logic break the connection pooling?
- What's the correct pattern for retry with SQLAlchemy's connection pool?
```

LLM explains: "The pool recycle setting conflicts with the retry backoff timing."

**Revert:**
```bash
git checkout -- src/db.py
```

**Restart clean:**
```
Add retry logic to src/db.py's get_connection() function.

Known constraint: pool recycle is set to 3600s. Retry backoff
must not exceed 30s to avoid pool exhaustion. Use tenacity with
wait_exponential(min=1, max=30, multiplier=2).

Make only this change. Do not modify pool settings.
```

## Best Practices

- Commit before starting any significant feature or debugging session.
- Use small, frequent commits as revert checkpoints.
- The sooner you recognize a loop, the less you lose by reverting.
- Treat "working but messy" as a prototype — always rewrite clean.
- The key insight from the loop is valuable; never lose it before reverting.
