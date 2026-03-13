# Using Images with LLMs

## Idea

Attach screenshots, diagrams, and annotated images to your prompts. Multimodal models process visual context faster and more accurately than text descriptions of the same thing.

## Why

A screenshot eliminates ambiguity that text descriptions can't:
- A UI bug described in words can be misunderstood.
- A UI bug shown in a screenshot is unambiguous.
- An error message screenshot includes stack trace, line numbers, and context automatically.
- A dashboard mockup screenshot replaces 200 words of layout description.

Use images when you'd otherwise spend more than 2–3 sentences describing what you're looking at.

## Use Cases

| Situation | What to Capture | Why It Helps |
|---|---|---|
| UI bug | Screenshot of broken component | Shows exact visual state |
| Error message | Full terminal / browser error | Includes complete context |
| Dashboard layout | Annotated wireframe or mockup | Replaces layout description |
| Database schema | ERD or table screenshot | Shows all columns + types |
| Code to refactor | Screenshot of messy section | Pinpoints exact code |
| Competitor UI | Screenshot of target design | Reference for replication |

## Annotation Techniques

Before attaching a screenshot, annotate it:

- **Red circle or arrow** → "Fix this element"
- **Yellow highlight** → "This is what currently exists"
- **Text label** → "This button should trigger X"
- **Numbered regions** → Match numbers in your text prompt

Free annotation tools:
- Windows Snipping Tool (Win + Shift + S → Edit)
- macOS Markup (Cmd + Shift + 4 → annotate in Preview)
- Monosnap, ShareX, Greenshot

## Example Prompts

### UI Bug

```
[Attach screenshot with red circle around broken chart]

The revenue chart (circled in red) is not rendering correctly.
The Y-axis labels overlap when there are more than 6 months.

Fix this in src/components/RevenueChart.tsx.
The component uses recharts. Apply a custom tick formatter to truncate labels.
```

### Error Message

```
[Attach screenshot of terminal showing the full traceback]

This error occurs when running the ETL pipeline with large files.
The screenshot shows the full traceback.

Identify the root cause and fix it in src/etl/s3_reader.py.
```

### Dashboard Layout

```
[Attach annotated wireframe screenshot]

Implement this dashboard layout in src/dashboard.py using Streamlit.
Labels in the image:
  1 = sidebar with year and region filters
  2 = KPI cards row (Total Revenue, Orders, Avg Order Value)
  3 = bar chart revenue by region
  4 = line chart monthly trend

Use width='stretch' for all charts.
Use company colors: primary #0055CC, gray #6B7280.
```

### Database Schema

```
[Attach ERD screenshot]

The screenshot shows the data model for the sales database.
Implement SQLAlchemy models for all tables shown.
Use the column names and types exactly as shown in the diagram.
Create the models in src/models/sales.py.
```

## Workflow

```
1. 📸 Capture screenshot (Win+Shift+S / Cmd+Shift+4)
        ↓
2. ✏️ Annotate (circle the relevant part, add labels)
        ↓
3. 💬 Write a brief text prompt describing what you want
        ↓
4. 📎 Attach image + send
        ↓
5. ✅ LLM responds with targeted solution
```

## Best Practices

- Annotate before attaching — unfocused images produce unfocused responses.
- Keep the text prompt brief — the image carries most of the context.
- Crop to relevant area only — full desktop screenshots dilute attention.
- For code screenshots: ensure text is sharp and readable.
- Combine multiple screenshots into one annotated image when showing before/after.
- Works especially well with: Gemini 1.5 Pro, Claude Sonnet, GPT-4o.
