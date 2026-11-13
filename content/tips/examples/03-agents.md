# Agents — Reusable Prompt Files

## Idea

Store LLM personas and coding standards as markdown files inside your repository. Reference them at the start of sessions instead of re-explaining context every time.

## Why

Without agent files, every session starts with:
> "You are a Python developer. Use snake_case. Never use print(). Use logging..."

This repeated context:
- Wastes tokens every session.
- Gets inconsistent as you forget details.
- Isn't version-controlled or shared with teammates.

Agent markdown files solve all three problems.

## Repository Structure

```
agents/
  python-dev.md       # Python coding persona and standards
  data-engineer.md    # DBT, SQL, Airflow, pipeline patterns
  sql-analyst.md      # Query patterns, naming conventions
  code-reviewer.md    # Review criteria, output format
  refactoring.md      # Refactoring principles and approach
```

## Example Agent File: `agents/python-dev.md`

```markdown
# Python Developer Agent

## Role
You are a senior Python developer working in this monorepo.
Follow all conventions in AGENTS.md.

## Coding Standards
- Files/Functions: snake_case
- Classes: PascalCase
- Constants: UPPER_CASE
- No print() — always use logging module
- Log with emojis: ℹ️ info, ⚠️ warning, ❌ error
- Fail fast with clear error messages

## Libraries
- Data: pandas, polars
- AWS: boto3
- HTTP: httpx
- Config: python-dotenv (.env files)
- Testing: pytest + pytest-mock
- DB: SQLAlchemy (async where possible)

## Project Structure
- src/: all production code
- tests/: pytest test files named test_*.py
- config/: JSON config files
- tmp/: experiments and scratch files (gitignored)

## Output Format
- Implement exactly what is requested, nothing more
- Add docstrings to public functions
- No commented-out code
- No placeholder implementations — write real code
```

## Example Prompt

```
Read agents/python-dev.md. Follow those standards for the entire session.

Now implement src/transform.py with these functions:
- normalize_dates(df: pd.DataFrame) -> pd.DataFrame
- fill_missing_revenue(df: pd.DataFrame) -> pd.DataFrame
- validate_required_columns(df: pd.DataFrame, columns: list[str]) -> None
```

## Best Practices

- Keep agent files under 500 lines — concise beats comprehensive.
- Update agent files when conventions change; commit them like code.
- Create task-specific agents for different domains (data, API, frontend).
- Reference the agent file at the start of every relevant session.
