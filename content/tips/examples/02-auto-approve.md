# Auto Approve

## Idea

Enable automatic approval for safe, well-scoped LLM actions so you stay in flow and avoid paying for confirmation prompts.

## Why

Every confirmation break:
- Interrupts your focus and flow state.
- Costs a premium request in tools that bill per prompt turn.
- Adds latency with no real safety benefit for trusted actions.

Auto-approve lets the LLM execute a full task in one pass. You review the final result rather than each individual step.

## What to Auto-Approve

**Safe to auto-approve:**
- Writing files inside `src/`, `tests/`, `tmp/`, `config/`
- Running `pytest`, `pip install`, `git status`, `git diff`
- Linting and formatting commands (`ruff`, `black`, `flake8`)
- Reading any project file

**Keep manual approval for:**
- `rm -rf` or any destructive file operation
- External API calls with real side effects
- Database migrations on production
- `git push`, `git merge`

## Example Prompt

```
Auto-approve is enabled. Implement the following changes directly
without asking for confirmation at each step:

1. Create src/validation.py with the validate_schema() function
2. Create tests/test_validation.py with 5 pytest tests
3. Run pytest to verify everything passes

Report the final result only.
```

## Example Scenario

### Refactoring a Module Without Interruptions

Without auto-approve, refactoring 5 files takes 5 confirmation clicks.

With auto-approve and a single well-written prompt:

```
Refactor the following changes across the codebase.
Auto-proceed without asking for confirmation:

- Rename load_data() to read_source_data() in all files
- Update all callers in src/ and tests/
- Run pytest after completing all changes
- Report test results and a summary of files changed
```

The LLM executes all changes, runs tests, and reports back with one response.

## Best Practices

- Review `git diff` after auto-approve sessions, not during.
- Scope your prompts precisely so auto-approve doesn't go off-track.
- Use `tmp/` for experimental work — safer to auto-approve freely.
- Never enable auto-approve for commands that touch external systems.
