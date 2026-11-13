# Avoid Confirmation Prompts

## Idea

Write prompts so clear and complete that the LLM never needs to ask for clarification. Every unnecessary back-and-forth costs money and time.

## Why

Some LLM tools (including Cursor, Copilot, and similar) bill each conversation turn as a premium request. This means:

- "Should I proceed?" = 1 premium request wasted.
- "Which directory should I use?" = 1 premium request wasted.
- "Do you want me to add error handling?" = 1 premium request wasted.

Beyond cost, each clarification:
- Breaks your flow state.
- Adds latency.
- Pollutes the session context.

## The Root Cause

Confirmation prompts happen when the LLM lacks information:
- File path not specified
- Function signature not defined
- Input/output format unclear
- Coding standards not communicated
- Expected behavior for edge cases not stated

The fix: provide all of this upfront.

## Anatomy of a Complete Prompt

```
[WHAT] Implement function normalize_product_names()
[WHERE] in src/transform.py
[SIGNATURE] normalize_product_names(df: pd.DataFrame, column: str) -> pd.DataFrame
[INPUT] DataFrame with a string column containing product names
[OUTPUT] Same DataFrame with the specified column lowercased and stripped
[STANDARDS] Use logging with ℹ️ on success. Raise ValueError if column doesn't exist.
[EXECUTION] Write it directly without asking for confirmation.
```

## Before vs. After

### ❌ Vague Prompt (causes confirmations)

```
Create a Python function to process sales data.
```

LLM asks:
- "What format is the input data?"
- "Where should I create this file?"
- "Should I add error handling?"
- "What transformation is needed?"

3–4 confirmation turns before any code is written.

### ✅ Complete Prompt (no confirmations)

```
Create function process_sales(df: pd.DataFrame) -> pd.DataFrame
in src/transform.py.

Input columns: [date, product_id, region, quantity, price]
Output: same DataFrame + new column [revenue] = quantity * price

Edge cases:
- Missing required columns → raise ValueError with column name
- Negative quantity or price → log ⚠️ warning, set revenue to 0.0
- Null values → fill quantity with 0, fill price with 0.0

Use logging (ℹ️ on success, ⚠️ on warnings). No print().
Write directly without asking for confirmation.
```

## Patterns That Eliminate Confirmations

| Problem | Solution |
|---|---|
| LLM asks which file | Always specify full path: `src/transform.py` |
| LLM asks about format | Always specify: function signature + types |
| LLM asks about edge cases | List them explicitly in the prompt |
| LLM asks about standards | Reference `agents/python-dev.md` |
| LLM asks to confirm | Add "proceed directly" or "write without asking" |
| LLM asks about dependencies | List allowed libraries explicitly |

## System-Level Prevention

Add to `AGENTS.md` or your agent file:

```markdown
## Execution Rules
- Write all requested files directly without asking for confirmation.
- When file paths are specified, use them exactly.
- When standards are unclear, default to snake_case, logging, type hints.
- Never ask "should I proceed?" — proceed unless the task is ambiguous.
- If genuinely ambiguous, state the assumption you're making and proceed.
```

## Best Practices

- If a prompt takes you 30 seconds to write, it should take the LLM one pass to execute.
- Front-load all context before describing the task.
- Use agent markdown files to avoid repeating standards.
- After each session, refine your templates based on what questions the LLM asked.
