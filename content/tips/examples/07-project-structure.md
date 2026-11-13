# Project Structure Consistency

## Idea

Use the same directory structure for every project. This removes the need to explain your layout to the LLM and ensures it places files correctly every time.

## Why

When the LLM encounters a familiar structure, it:
- Knows exactly where to create new files without being told.
- Generates correct import paths automatically.
- Understands where configs, tests, secrets, and docs live.
- Applies the right conventions per directory.

Inconsistent structures require extra prompting on every session and produce inconsistent file placement.

## Standard Project Structure

```
project-name/
  src/
    __init__.py
    main.py             # entry point
    transform.py        # business logic
    extract.py          # data ingestion
    load.py             # output / loading

  config/
    settings.json       # non-secret configuration
    schema.json         # data schemas / validation rules

  tests/
    __init__.py
    test_transform.py
    test_extract.py
    test_load.py
    conftest.py         # shared fixtures

  tmp/                  # gitignored — scratch space
    session-notes.md
    experiments.py

  docs/
    architecture.md
    runbook.md

  agents/
    python-dev.md
    data-engineer.md

  .env                  # secrets — always gitignored
  .gitignore
  requirements.txt
  README.md
  AGENTS.md             # Cursor/LLM workspace rules
```

## `tmp/` Folder — Sandbox Strategy

The `tmp/` folder is critical for safe LLM collaboration:

```
tmp/
  2026-03-13-session.md        # session notes
  spike_chunked_reader.py      # experiment (not production)
  test_query.sql               # throwaway SQL
```

- The LLM can create files here freely.
- Nothing in `tmp/` affects production.
- Add to `.gitignore` so experiments don't pollute the repo.

```
# .gitignore
tmp/
*.pyc
__pycache__/
.env
.venv/
```

## Prompt to Initialize Structure

```
Initialize this project with the standard structure below.
Create all directories and placeholder files:

src/__init__.py, src/main.py, src/transform.py
config/settings.json (with empty {} content)
tests/__init__.py, tests/conftest.py
tmp/.gitkeep
docs/architecture.md (with # Architecture header)
.gitignore (ignore: tmp/, .env, __pycache__, .venv/)
requirements.txt (with placeholder comment)
README.md (with project name as H1)
```

## Example Scenario

### Starting a New Python Automation Project

**Step 1** — Initialize the structure (one prompt).

**Step 2** — Point the LLM to the right directories:
```
Implement the CSV reader in src/extract.py.
Config for S3 bucket names lives in config/settings.json.
Tests go in tests/test_extract.py.
Use logging, not print().
```

**Result:** The LLM places everything correctly without further guidance.

## Best Practices

- Define the structure in `AGENTS.md` so it's automatically loaded.
- Never let the LLM invent top-level folders spontaneously.
- Use the same structure even for small scripts — consistency pays compound interest.
- Keep `src/` flat for small projects; add subdirectories only when needed.
