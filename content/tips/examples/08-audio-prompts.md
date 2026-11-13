# Audio Prompting

## Idea

Record complex requirements as voice notes. Transcribe and structure them with an LLM. Use the result as your session prompt.

## Why

Typing detailed, multi-part requirements is slow and often incomplete.

- Speaking is 3–4× faster than typing.
- Voice captures nuance, priority, and context naturally.
- You can ramble and let the LLM clean it up.
- Long explanations that would take 10 minutes to type take 2 minutes to say.

## Workflow

```
1. 🎤 Record audio note
        ↓
2. 📝 Transcribe (Whisper / Gemini / Voice Memos)
        ↓
3. 🤖 Ask LLM: "Structure this as a prompt"
        ↓
4. 👀 Review structured prompt
        ↓
5. ✅ Use as session opener
```

## Step 1: Record

Use any tool:
- Phone voice memos app
- Windows Voice Recorder
- Whisper locally
- Any app with transcription built in

Speak freely and technically. Don't worry about grammar or structure.

## Step 2: Transcribe

Paste audio or transcript into any LLM:

```
Transcribe this voice note accurately. Preserve all technical terms.
Fix obvious transcription errors (e.g. "pie thon" → "Python").
Do not summarize yet — give me the full cleaned-up transcript.
```

## Step 3: Structure

```
Convert this voice transcript into a structured LLM prompt.

Requirements:
- Preserve all technical details and constraints
- Organize into clear sections: Goal, Context, Requirements, Output
- Use bullet points for lists
- Add any obvious implied requirements (e.g. error handling, logging)
- Keep it concise but complete

Transcript:
[paste transcript here]
```

## Example

### Raw Voice Transcript

```
So I need to build a dashboard thing in Streamlit where the user
can upload a CSV file and then it shows some charts you know like
a bar chart of revenue by region and a line chart for monthly trends
and there should be a filter for year and region and I want it to
use the company colors which are blue and gray and it should be
fast and not break if the CSV has missing values or wrong column names
it should show a proper error message
```

### Structured Prompt Output

```markdown
## Goal
Build a Streamlit dashboard for CSV-based sales analytics.

## Requirements
- File upload widget accepting CSV files
- Validation: show user-friendly error if:
  - Required columns are missing
  - File contains invalid data types
- Charts (using company colors: blue #0055CC, gray #6B7280):
  - Bar chart: revenue by region
  - Line chart: monthly revenue trend
- Sidebar filters:
  - Year selector (derived from data)
  - Region multi-select
- Handle missing values gracefully (drop or fill, with warning)

## Output
Single-file app: src/dashboard.py
Use streamlit with width='stretch' for full-width charts.
Use logging for errors, not print().
```

## Important: Speak in English

Always record audio prompts in **English**, even if it's not your first language.

Reasons:
- LLMs have significantly larger training data in English.
- Technical terms (function names, library names) are English by nature.
- Transcription accuracy is higher in English.
- Translating from another language introduces token overhead and potential misinterpretation.

## Best Practices

- Keep recordings under 5 minutes — longer gets unfocused.
- Say file names and function names slowly and clearly.
- At the end of the recording, summarize the 3 most important points.
- Save useful structured prompts to `agents/` for reuse.
