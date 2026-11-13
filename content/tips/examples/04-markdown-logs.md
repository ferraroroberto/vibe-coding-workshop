# Markdown Logging

## Idea

Save session notes, prompts, reasoning, and decisions to markdown files in `tmp/` as you work. Use these logs to resume sessions, hand off context, or generate documentation.

## Why

Long LLM sessions accumulate noise:
- Failed attempts that polluted the context.
- Corrected misunderstandings.
- Revised approaches.

A clean markdown log captures only the signal: the goal, the approach, the solution. This lets another LLM (or future you) pick up exactly where you left off.

## File Naming Convention

```
tmp/
  2026-03-13-etl-pipeline.md
  2026-03-14-api-auth.md
  2026-03-15-dashboard-fix.md
```

## Log Template

```markdown
# Session: [Feature/Task Name]
Date: YYYY-MM-DD

## Goal
What was the objective of this session?

## Context
What did the LLM need to know?
- Relevant files
- Existing patterns
- Constraints

## Prompt Used
Paste the key prompt(s) used.

## Approach
How did we tackle it? What decisions were made?

## Solution
Where does the final implementation live?
What does it do at a high level?

## Iterations
- Attempt 1: [What happened, what broke]
- Attempt 2: [What changed, why]
- Final: [What worked]

## Edge Cases Handled
- [Edge case 1]
- [Edge case 2]

## Tests
How was this validated?

## Next Steps
- [ ] What needs to be done next?
```

## Example: Completed Log

```markdown
# Session: S3 to Postgres ETL
Date: 2026-03-13

## Goal
Build a Python ETL that reads CSV from S3 and loads to PostgreSQL.

## Context
- S3 bucket: data-lake-prod
- Schema: sales (date, product_id, quantity, price)
- Config in config/etl.json

## Prompt Used
"Build src/etl.py that reads CSV from S3, transforms with pandas,
loads to PostgreSQL. Use retry logic, logging with emojis."

## Approach
Used boto3 for S3, pandas for transform, SQLAlchemy for PG.
Added tenacity for retries on connection failures.

## Solution
src/etl.py — complete pipeline in single module.

## Iterations
- Attempt 1: S3 auth failed (missing region env var). Fixed via .env.
- Attempt 2: Memory spike on 500MB files. Switched to chunked reads.
- Final: Chunked read + batched PG inserts. Works on test data.

## Tests
pytest tests/test_etl.py — all 8 tests pass.

## Next Steps
- [ ] Add unit test for null revenue rows
- [ ] Add monitoring alert when row count drops below threshold
```

## How to Use the Log in the Next Session

```
Context from last session (tmp/2026-03-13-etl-pipeline.md):
[paste log content]

Continue from where we left off. Today's task: add unit test
for null revenue rows in tests/test_etl.py.
```

## Best Practices

- Log after every session, not during.
- Keep logs in `tmp/` (gitignored) — they're working notes, not docs.
- If a log is worth preserving, promote it to `docs/`.
- Use logs to generate release notes, ADRs, or documentation.
