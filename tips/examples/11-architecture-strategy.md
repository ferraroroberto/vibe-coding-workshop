# Architecture Strategy

## Idea

Start with a monolith when exploring. Start modular when the architecture is already clear. Set iteration limits high to let strong models run autonomously.

## Why

The biggest mistake in LLM-assisted development:
- Designing a perfect modular architecture before the first line works.
- Spending 80% of prompts on structure instead of substance.
- Getting stuck in architecture debates when you don't know the domain yet.

The second biggest mistake:
- Building a working monolith and never refactoring it.

The right strategy depends on how well you understand the problem.

---

## Strategy 1: Exploring → Monolith First

When you're building something new or unfamiliar, start with everything in one file.

### Phase 1: Build the monolith

```
Build a complete ETL pipeline in a single file: src/pipeline.py

It should:
- Read CSV from S3
- Filter rows where revenue > 0
- Aggregate by region and month
- Write results to PostgreSQL

Keep everything in one file. No modules yet. Get it working first.
```

### Phase 2: Validate it works

```bash
pytest tests/test_pipeline.py -v
```

### Phase 3: Refactor into modules

Only after it works end-to-end:

```
The pipeline in src/pipeline.py is working and tested.

Now refactor it into this module structure without changing behavior:
- src/extract.py → S3 reading logic
- src/transform.py → filtering and aggregation
- src/load.py → PostgreSQL writing
- src/pipeline.py → orchestration only (imports from above modules)

All existing tests must still pass after refactoring.
```

---

## Strategy 2: Known Architecture → Start Modular

When you've built this type of system before and the structure is obvious, define it upfront.

```
Create the following module structure for a REST API:

src/
  api/
    routes.py           # FastAPI route definitions
    dependencies.py     # shared dependencies (auth, db)
  services/
    user_service.py     # business logic
    email_service.py    # email sending
  models/
    user.py             # SQLAlchemy models
  schemas/
    user_schema.py      # Pydantic schemas

Create all files with correct imports and stub implementations.
Add docstrings to every public function.
Do not implement logic yet — just structure.
```

Then implement module by module.

---

## Iteration Limits

Set maximum iterations **as high as the tool allows** when working with strong models (Gemini, Sonnet).

### Why

- Strong models reason well over long tasks.
- Stopping prematurely fragments the work unnecessarily.
- Each session restart adds overhead (context re-loading, re-prompting).

### The Human's Role

With high iteration limits, your job shifts:
- **Don't** approve every step.
- **Do** monitor progress and course-correct when needed.
- **Do** set up validation (pytest) so the LLM self-corrects.
- **Do** intervene if the LLM goes off-course.

### Anti-Pattern: Low Iteration Limits

```
# ❌ Don't do this
"Implement function 1. Stop. Wait for approval. Then implement function 2."
```

This is exhausting and slow. Trust strong models on well-scoped tasks.

---

## Decision Tree

```
Is this a new domain/problem?
├── YES → Monolith first → validate → refactor
└── NO → Have you built this architecture before?
         ├── YES → Start modular from the start
         └── NO → Monolith first
```

## Best Practices

- Always state the strategy at the top of your opening prompt.
- Commit after the monolith works, before refactoring.
- Never refactor and add features at the same time.
- Treat the monolith as a prototype — it will be replaced.
- When starting modular, define interfaces first, implementation second.
