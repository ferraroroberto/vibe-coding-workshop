# Iteration Summary Technique

## Idea

At the end of a working phase, ask the LLM to produce a structured summary of everything accomplished. Use that summary to start a clean new session.

## Why

Long sessions degrade in quality because:
- The context fills with failed attempts, corrections, and back-and-forth.
- The LLM has to reason over irrelevant history.
- Responses become less focused and more prone to repetition.

A summary compresses all signal and discards the noise. Starting fresh with it is almost always faster and cleaner than continuing the same session.

## The Summary Prompt

Use this exact prompt at the end of any significant phase:

```
We've completed this phase of work. Before we move on,
produce a structured summary with these sections:

## Summary

### Goal
What were we trying to achieve?

### Approach
What strategy did we use? Why?

### Final Solution
What was built? Where does it live? What does it do?

### Key Decisions
What choices were made and why?

### Edge Cases Handled
What non-obvious scenarios were addressed?

### Tests
How was the implementation validated?

### What Still Needs To Be Done
List any pending tasks or known gaps.

Format this so I can paste it as the opening message of the next session.
```

## Example: Before Summary

*Context after a messy debugging session — 25 messages, 3 failed approaches, 1 working solution.*

## Example: After Summary

```markdown
## Summary

### Goal
Add retry logic to the S3 reader in src/etl/s3_reader.py.

### Approach
Used tenacity library with exponential backoff. Retries on
boto3.exceptions.BotoCoreError and ConnectionError.

### Final Solution
src/etl/s3_reader.py — read_csv_from_s3() now wrapped with
@retry(stop=stop_after_attempt(3), wait=wait_exponential()).
Logs ⚠️ on each retry, ❌ on final failure.

### Key Decisions
- Max 3 retries (enough for transient failures, not infinite loops)
- Exponential backoff starting at 2s (avoids hammering S3)
- Raises the original exception after exhausting retries

### Edge Cases Handled
- Empty S3 file returns empty DataFrame with correct schema
- Invalid CSV raises ValueError immediately (no retry)
- Missing S3 key raises FileNotFoundError immediately (no retry)

### Tests
pytest tests/test_s3_reader.py — 6 tests, all passing.
Uses moto to mock S3 interactions.

### What Still Needs To Be Done
- [ ] Add integration test with real S3 (dev bucket)
- [ ] Add metrics: retry count per file
```

## Using the Summary to Restart

Open a new session and paste:

```
Context for this session:
[paste the summary above]

Today's task: implement the integration test mentioned in "What Still Needs To Be Done".
Use the existing mock pattern in tests/test_s3_reader.py as reference.
```

## Best Practices

- Always produce a summary before switching between major tasks.
- Save summaries to `tmp/` with the date as filename prefix.
- Chain summaries: each session starts from the previous one's summary.
- If a session went badly, still produce a summary — note what failed and why.
