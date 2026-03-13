# Model Selection Strategy

## Idea

Choose the right LLM for the complexity of the task. Bigger is not always better — it's just more expensive.

## Why

- Complex reasoning tasks benefit from large models with long context windows.
- Repetitive or small tasks are handled perfectly by cheaper, faster models.
- Using a premium model for a trivial rename wastes tokens and money.

## Model Guide

| Task Complexity | Recommended Model | Cost Multiplier |
|---|---|---|
| Architecture design, large refactors, long context | Gemini 3.1 / Claude Sonnet 4.6 | 1× |
| Feature implementation, debugging sessions | Grok Fast | 0.25× |
| Small edits, renames, quick fixes | GPT-4.1 | Low |

## Example Prompt

```
I need to design a Python data pipeline architecture for ingesting
10 million rows daily from S3 into Snowflake. Use Gemini to plan
the architecture and identify all components. Once approved,
switch to GPT-4.1 to scaffold each individual module.
```

## Example Scenario

### Building a Python ETL Pipeline

**Phase 1 — Design (use Gemini / Sonnet):**
```
We are building an ETL pipeline:
- Source: S3 bucket with daily CSV dumps
- Transform: Aggregate by region, filter nulls, calculate revenue
- Destination: PostgreSQL warehouse

Design the full architecture: modules, interfaces, data flow, error handling strategy.
```

**Phase 2 — Implement modules (switch to GPT-4.1):**
```
Implement src/extract.py based on this spec:
- Function: read_csv_from_s3(bucket: str, key: str) -> pd.DataFrame
- Use boto3 + pandas
- Log success with ℹ️ and errors with ❌
```

## Decision Checklist

- [ ] Does this require reasoning over multiple files? → Use large model.
- [ ] Is this a single function or small change? → Use cheap model.
- [ ] Is the problem well-defined? → Cheap model is fine.
- [ ] Is it unclear and exploratory? → Use large model.
