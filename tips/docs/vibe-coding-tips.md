# Vibe Coding Tips & Tricks

> Practical techniques for high-velocity development with LLMs.

---

## 1. Model Selection

### Explanation

Not all models are created equal. Using the wrong model for the wrong task costs money, time, and quality. Match model capability to task complexity.

### Reasoning

- **Large, complex tasks** need deep reasoning and long context windows.
- **Medium tasks** are best served by fast, cost-efficient models.
- **Small edits** should be handled by cheap, reliable models.

### Model Guide

| Complexity | Model | Multiplier | Use Case |
|---|---|---|---|
| Complex | Gemini 3.1 / Claude Sonnet 4.6 | 1× | Architecture, large refactors, long context |
| Medium | Grok Fast | 0.25× | Moderate features, debugging sessions |
| Small | GPT-4.1 | Low | Quick edits, renaming, small fixes |

### Best Practices

- Start complex planning with a reasoning model (Gemini / Sonnet).
- Switch to a cheaper model once the architecture is decided.
- Never use an expensive model for a one-line fix.

### Example Prompt

```
Use Claude Sonnet to design the ETL pipeline architecture.
Once approved, switch to GPT-4.1 to implement individual functions.
```

---

## 2. Auto Approve

### Explanation

Most LLM coding tools ask for confirmation before writing files or running commands. For safe, well-understood tasks, this is unnecessary friction.

### Reasoning

Each confirmation prompt:
- Breaks your flow state.
- Costs a premium request in some tools.
- Slows iteration velocity.

### Workflow Example

Enable auto-approve for:
- File writes within `src/`, `tests/`, `tmp/`.
- Safe shell commands (`pip install`, `pytest`, `git status`).

Keep manual approval for:
- Destructive commands (`rm -rf`, `DROP TABLE`).
- External API calls with real side effects.

### Best Practices

- Set auto-approve globally for trusted directories.
- Use `tmp/` as a sandbox for risky experiments.
- Review the final diff rather than each individual step.

### Example Prompt

```
Implement the three functions below. Write them directly to src/transform.py
without asking for confirmation at each step.
```

---

## 3. Agents

### Explanation

Agent markdown files are reusable prompt templates stored inside your repository. They define a persona, context, coding standards, and expectations for the LLM.

### Reasoning

Without agents, you repeat the same context at the start of every session:
- "You are a Python developer..."
- "Use snake_case..."
- "Never use print(), use logging..."

With agent files, you reference the file once and all that context loads instantly.

### Workflow Example

```
agents/
  python-dev.md       # Python coding standards, style guide
  data-engineer.md    # DBT, SQL, Airflow patterns
  sql-analyst.md      # Query patterns, naming conventions
  code-reviewer.md    # Review criteria and output format
```

### Best Practices

- Keep agents under 500 lines — longer files dilute the signal.
- Include: role, coding standards, preferred libraries, output format.
- Update agents when conventions change.
- Store agents in version control alongside the codebase.

### Example Prompt

```
Read agents/python-dev.md and follow those standards throughout this session.
Now implement the data validation module in src/validation.py.
```

---

## 4. Markdown Logging

### Explanation

Use a `tmp/` folder to save session notes as markdown files. Capture prompts, reasoning, decisions, and outcomes during a coding session.

### Reasoning

Long sessions accumulate messy context — failed attempts, revised approaches, abandoned ideas. A clean markdown log lets you:
- Hand off to another LLM cleanly.
- Resume sessions without re-explaining everything.
- Review your own reasoning later.

### Workflow Example

```
tmp/
  2026-03-13-etl-pipeline.md
  2026-03-14-api-integration.md
```

Each file contains:

```markdown
## Goal
Build S3-to-Postgres ETL pipeline.

## Prompt Used
"Create a Python script that reads CSV files from S3..."

## Solution
Used pandas + boto3. Added retry logic with tenacity.

## Iterations
- Attempt 1: Failed on S3 auth. Fixed by using env vars.
- Attempt 2: Memory issue with large files. Switched to chunked reads.

## Final State
src/etl/s3_reader.py — working, tested with mock data.

## Next
Add unit tests for transform layer.
```

### Best Practices

- Log at the end of each working session.
- Include what worked AND what failed.
- Use the log as the opening prompt for the next session.

---

## 5. Iteration Summary Technique

### Explanation

After completing a significant step with an LLM, request a structured summary before starting a new session or new phase.

### Reasoning

Long conversations accumulate noise: failed attempts, corrections, back-and-forth. The LLM's context window fills with irrelevant history. A summary:

- Compresses the signal, removes the noise.
- Creates a clean starting point.
- Enables context reset without losing progress.

### Workflow Example

At the end of a phase, send:

```
Summarize what we built in this session:
- What was the goal?
- What approach did we use?
- What was the final solution?
- What edge cases did we handle?
- What still needs to be done?

Format it as a markdown document I can use as the opening prompt for the next session.
```

### Best Practices

- Always summarize before switching tasks.
- Save the summary to `tmp/`.
- Start the next session by pasting the summary as the first message.
- Use summaries to create documentation.

---

## 6. Validation

### Explanation

LLM-generated code is often almost correct. Validation is the step that catches the difference between "looks right" and "works right."

### Reasoning

LLMs:
- Hallucinate function signatures.
- Make off-by-one errors.
- Generate plausible-but-wrong SQL.
- Miss edge cases.

You cannot trust output you haven't run.

### Validation Strategies

**Python:**
```bash
pytest tests/ -v --tb=short
```

Use mock data to test transforms. Use `pytest.raises()` to test error paths.

**SQL:**
```sql
-- Run against a sample of real data
SELECT * FROM transformed_table LIMIT 100;

-- Verify row counts
SELECT COUNT(*) FROM source_table;
SELECT COUNT(*) FROM transformed_table;
```

**APIs:**
```bash
curl -X POST http://localhost:8000/endpoint \
  -H "Content-Type: application/json" \
  -d '{"test": "payload"}'
```

### Best Practices

- Write tests before asking the LLM to implement.
- Run tests after every LLM-generated change.
- Add edge cases the LLM likely missed.
- Never deploy without passing tests.

### Example Prompt

```
Write pytest tests for the transform_sales_data() function.
Cover: empty input, null values, incorrect column names, and happy path.
```

---

## 7. Project Structure Consistency

### Explanation

Use the same directory structure across all projects. This reduces cognitive overhead and allows the LLM to navigate the codebase without explanation.

### Reasoning

When the LLM knows the structure, it:
- Places files correctly without being told.
- Writes import paths accurately.
- Knows where configs, tests, and docs live.

### Standard Structure

```
project/
  src/          # All production code
  config/       # JSON configuration files
  tests/        # pytest test suite
  tmp/          # Scratch space, experiments, session notes
  docs/         # Markdown documentation
  agents/       # LLM prompt files
  .env          # Secrets (always gitignored)
  .gitignore
  requirements.txt
  README.md
```

### `tmp/` Folder Strategy

Use `tmp/` as a sandbox:
- LLM experiments go here, not in `src/`.
- Session notes live here.
- Generated drafts sit here before promotion to `src/`.

Add to `.gitignore`:
```
tmp/
```

### Best Practices

- Start every project with this structure before writing any code.
- Include the structure in your agent markdown files.
- Never let the LLM create top-level folders spontaneously.

---

## 8. Audio Prompting

### Explanation

Voice is faster than typing, especially for complex, multi-part requirements. Record your explanation, transcribe it, and use the LLM to structure it into a proper prompt.

### Reasoning

- Speaking is 3–4× faster than typing.
- Complex requirements are easier to explain verbally.
- Freeform speech captures nuances that structured typing misses.

### Workflow

1. **Record** a voice explanation of your problem, requirements, or context.
2. **Transcribe** using Whisper, Gemini, or a voice recording app with transcription.
3. **Paste transcript** into the LLM with:

```
Clean up this voice transcript and convert it into a structured prompt.
Preserve all technical details. Fix transcription errors.
```

4. **Use the structured prompt** as your actual session opener.

### Best Practices

- Always speak in **English**. Other languages increase token costs and introduce translation artifacts.
- Be specific and technical in your recording — don't worry about perfect grammar.
- Re-read the structured prompt before sending to verify accuracy.
- Save useful prompts to your `agents/` folder.

### Example

Raw transcript:
```
So I want to build a thing that reads CSV files from S3 and uh then
processes them and puts them in postgres and it needs to handle like
retries if the connection drops and also I want logging with emojis...
```

Structured result:
```
Build a Python ETL module that:
1. Reads CSV files from S3 using boto3
2. Transforms using pandas
3. Loads into PostgreSQL using SQLAlchemy
4. Handles connection retries with exponential backoff (tenacity)
5. Uses logging with emoji indicators (ℹ️ ⚠️ ❌)
```

---

## 9. Reverting and Checkpoints

### Explanation

When an LLM starts looping — making a change that breaks something else, then fixing that which breaks the original — stop immediately. Revert to a clean state and restart with a better prompt.

### Reasoning

Continuing a looping session:
- Compounds errors.
- Wastes prompts.
- Produces unmaintainable code.
- Degrades context quality.

A clean restart with a targeted prompt almost always outperforms continued patching.

### Technique

**Phase 1: Get the solution**
1. Let the LLM find a working approach (even if messy).
2. Note the key insight or solution in markdown.

**Phase 2: Revert**
```bash
git stash
# or
git checkout <clean-commit-hash>
```

**Phase 3: Restart clean**
1. Open a new session.
2. Paste the summary of the working solution as the opening prompt.
3. Ask for a clean implementation.

### Best Practices

- Commit frequently. Small commits = easier rollback targets.
- Always save the key insight before reverting.
- Treat "working but messy" as a prototype, not final code.
- Restart early — the longer you wait, the messier the codebase.

---

## 10. Avoid Confirmation Prompts

### Explanation

Some LLM tools bill each conversation turn as a premium request — including unnecessary confirmation questions from the model.

### Reasoning

Confirmation prompts waste:
- **Money**: each "Should I proceed?" costs the same as a real prompt.
- **Time**: each confirmation breaks your flow and adds latency.
- **Context**: unnecessary back-and-forth pollutes the session history.

### Solution

Front-load all context in your initial prompt. Make it impossible for the LLM to need clarification.

### Bad Example

```
Create a Python function to process sales data.
```
Result: LLM asks "What format is the input? Where should I write it? Should I add error handling?"

### Good Example

```
Create a function process_sales_data(df: pd.DataFrame) -> pd.DataFrame in src/transform.py.
Input: pandas DataFrame with columns [date, product_id, quantity, price].
Output: DataFrame with added column [revenue] = quantity * price.
Add logging with ℹ️ on success. Raise ValueError if required columns are missing.
Write it directly without asking for confirmation.
```

### Best Practices

- Always specify: file path, function signature, input/output format.
- Add "write it directly" or "proceed without asking" to long-running tasks.
- Use AGENTS.md or agent markdown files to avoid repeating standards.

---

## 11. Architecture Strategy

### Explanation

The optimal starting architecture depends on how well you understand the problem. Use a different approach for exploration vs. execution.

### When Exploring: Monolith First

Start with a single file containing all logic:

```python
# main.py — everything in one place first
def extract(): ...
def transform(): ...
def load(): ...

if __name__ == '__main__':
    data = extract()
    transformed = transform(data)
    load(transformed)
```

Once working, refactor into modules:

```
src/
  extract.py
  transform.py
  load.py
  pipeline.py
```

### When Architecture is Clear: Start Modular

If you've done this before or the structure is obvious, define modules upfront:

```
Create the following module structure for an ETL pipeline:
- src/extract.py: S3 reader
- src/transform.py: business logic
- src/load.py: PostgreSQL writer
- src/pipeline.py: orchestration

Implement each module with stubs and docstrings first.
```

### Iteration Limits

Set iteration limits **high** when working with strong models. A high iteration limit:
- Lets the LLM complete long tasks uninterrupted.
- Reduces session fragmentation.
- Enables autonomous multi-step implementation.

Monitor progress rather than micromanaging step-by-step.

### Best Practices

- Default to monolith first unless you've built this exact thing before.
- Only refactor after it works end-to-end.
- Document the chosen architecture at the top of the main file.

---

## 12. Using Images with LLMs

### Explanation

Multimodal LLMs can process screenshots, diagrams, and annotated images directly. This is often faster and more accurate than describing UI elements or error messages in text.

### Reasoning

A screenshot of an error message or UI is:
- Unambiguous — no room for misinterpretation.
- Complete — includes all context automatically.
- Fast — no need to describe every detail.

### Use Cases

| Situation | What to Capture |
|---|---|
| UI bug | Screenshot of the broken component |
| API error | Screenshot of the error message + response |
| Dashboard layout | Annotated screenshot of desired result |
| Database schema | ERD diagram or table screenshot |
| Code review | Screenshot of relevant code section |

### Workflow

1. Take a screenshot of the relevant UI, error, or diagram.
2. Annotate with arrows, circles, or text if needed.
3. Attach to the prompt with a brief description:

```
Screenshot attached shows the dashboard layout we want to replicate.
The red circle indicates the broken chart component.
Implement the fix in src/components/SalesChart.tsx.
```

### Best Practices

- Annotate before attaching — guide the LLM's attention.
- Use screenshots for UI, errors, and visual artifacts.
- Combine image + text for best results.
- For complex diagrams, describe what the image shows briefly.

---

*Generated for the Vibe Coding Workshop — March 2026*
