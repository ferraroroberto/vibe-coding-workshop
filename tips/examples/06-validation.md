# Validation

## Idea

Never trust LLM-generated code without running it. Build validation into your workflow as a non-negotiable step.

## Why

LLMs confidently produce code that:
- Calls functions with wrong signatures.
- Makes off-by-one errors in data transformations.
- Generates plausible SQL that returns incorrect results.
- Handles the happy path perfectly but fails on edge cases.

Running the code is the only way to know it works.

## Validation by Technology

### Python — pytest

```bash
# Run full test suite with verbose output
pytest tests/ -v --tb=short

# Run a specific test file
pytest tests/test_transform.py -v

# Run tests matching a keyword
pytest tests/ -k "test_revenue" -v
```

**Write tests before asking for implementation:**

```
Before implementing transform_sales_data(), write 5 pytest tests in
tests/test_transform.py that cover:
1. Happy path with valid DataFrame
2. Empty DataFrame input
3. Missing required column (should raise ValueError)
4. Null values in quantity column
5. Negative price values

Use pytest.raises() for error cases. Mock external dependencies.
```

### SQL — Sample Queries

```sql
-- Count check: source vs transformed
SELECT COUNT(*) AS source_count FROM raw_sales;
SELECT COUNT(*) AS output_count FROM transformed_sales;

-- Spot check values
SELECT date, product_id, quantity, price, revenue
FROM transformed_sales
WHERE revenue != quantity * price
LIMIT 10;

-- Null check
SELECT COUNT(*) FROM transformed_sales WHERE revenue IS NULL;
```

### APIs — curl / httpx

```bash
# Test endpoint directly
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{"records": [{"id": 1, "value": 99.9}]}'

# Check error handling
curl -X POST http://localhost:8000/api/process \
  -H "Content-Type: application/json" \
  -d '{"records": []}'
```

## Example Scenario

### Validating an LLM-Generated Transform Function

**LLM generates:**
```python
def calculate_revenue(df: pd.DataFrame) -> pd.DataFrame:
    df['revenue'] = df['quantity'] * df['price']
    return df
```

**Validation prompt:**
```
The function calculate_revenue() has been implemented.
Write and run pytest tests covering:
- Normal rows: revenue = quantity * price
- Zero quantity: revenue should be 0.0
- Null price: should raise ValueError
- Negative quantity: should raise ValueError (business rule)

After running tests, report which passed and which failed.
Fix any failures found.
```

**LLM runs tests, finds the null/negative cases aren't handled, fixes them.**

## Validation Checklist

- [ ] Happy path works with real/mock data
- [ ] Edge cases: empty input, nulls, type mismatches
- [ ] Error paths: does it raise the right exceptions?
- [ ] Row counts match expectations (for transforms)
- [ ] No silent data corruption (spot-check output values)

## Best Practices

- Write tests before implementation (TDD with an LLM is very effective).
- Ask the LLM to run tests after implementing — don't run them manually first.
- Include real edge cases you know from the domain, not just generic ones.
- Treat failing tests as the LLM's problem to fix, not yours.
