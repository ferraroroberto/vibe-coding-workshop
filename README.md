# Python Vibe-Coding Workshop

A hands-on workshop for learning data manipulation, automation, and visualization with Python in a corporate setting. Includes a **slideshow** for presenting exercises, plus structured exercises (main + bonus) with starter files, solutions, and sample data.

## Features

- **Vibe Coding Tips**: HTML slide presentation (`content/tips/index.html`) — playful, keyboard-navigable slides on practical LLM workflow tips (model selection, auto-approve, agents, markdown logging, validation, etc.) with full docs in `content/tips/docs/` and examples in `content/tips/examples/`
- **Slideshow**: HTML presentation (`content/slideshow/slideshow.html`, `content/slideshow/slideshow_es.html` for Spanish) with exercise menu, bonus section, and navigation; both decks load the shared stylesheet and their own exercise data script, so open it straight from the file system (no server needed)
- **"Not Everything Is AI" keynote**: Standalone bilingual talk deck (`content/slideshow_ai/slideshow_ai.html`) — self-contained, no build step, in-page ES/EN toggle (or `?lang=en|es`), arrow/space navigation plus `B` to open a slide's link (presentation clicker), with live HTML demos in `content/slideshow_ai/mockups/`
- **Main exercises**: Intro, ETL (merge, clean, survey), Viz (charts, reports), Auto (Excel polish, file organizer), plus Bonus “Big Data Stress Test”
- **Bonus exercises**: PDF report, API pipeline, D3 bar/force viz, geo heatmap, interactive dashboard, Seaborn scatter/statistical
- **Library testing**: `scripts/test_libraries.py` to verify required libraries and serves as the post-`pip install` smoke check for the Quick Start
- **Streamlit demo**: `content/streamlit_demo/` — multi-page reference app (inputs, viz, CRUD, file upload, process runner, session state)
- **Survey Data Dashboard**: `content/metadata/` — Streamlit dashboard for visualizing and managing survey data, with data entry, organizational import, and participation-rate treemaps (see `content/metadata/README.md`)
- **Environment tools**: `scripts/pip_ini_finder.py` for locating pip config; `requirements.txt` for dependencies

## Quick Start

1. Clone and enter the repo:
   ```bash
   git clone <repository-url>
   cd vibe-coding-workshop
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt   # Windows
   # ./.venv/bin/python -m pip install -r requirements.txt       # macOS/Linux
   ```

3. Run a presentation: open `content/slideshow/slideshow.html` (workshop exercises) or `content/tips/index.html` (Vibe Coding Tips & Tricks) in a browser (no server needed). Use arrow keys to navigate the tips slides.

4. (Optional) Test the environment:
   ```bash
   .venv\Scripts\python.exe scripts\test_libraries.py   # Windows
   # ./.venv/bin/python scripts/test_libraries.py       # macOS/Linux
   ```

5. (Optional) Run the Streamlit demo:
   ```bash
   cd content/streamlit_demo
   ..\..\.venv\Scripts\python.exe -m streamlit run main_menu.py   # Windows
   # ../../.venv/bin/python -m streamlit run main_menu.py      # macOS/Linux
   ```
   Or on Windows, double-click `content/streamlit_demo/run_app.bat`.

## Project Structure

| Path | Description |
|------|-------------|
| `content/tips/` | Vibe Coding Tips presentation: `index.html` (slides), `styles.css`, `script.js`, `content/tips/docs/vibe-coding-tips.md`, `examples/*.md` (12 tip examples) |
| `content/slideshow/slideshow.html` | Workshop slideshow shell (English): welcome, menu, main/bonus exercises, break, survey, congratulations; hand-edited |
| `content/slideshow/slideshow_es.html` | Spanish shell, derived from the English one by `scripts/build_slideshow.py` |
| `content/slideshow/slideshow.css` | Hand-edited stylesheet shared by both decks |
| `content/slideshow/slideshow_data_en.js`, `content/slideshow/slideshow_data_es.js` | Exercise content of each deck, generated from the `exercise_starter.md` files (edit those, not these) |
| `content/slideshow/assets/` | Images for slideshow (one per exercise + welcome, menu, break, survey, etc.) |
| `content/slideshow_ai/slideshow_ai.html` | Standalone bilingual keynote "Not Everything Is AI / No Todo Es IA" (ES/EN toggle, `?lang=`); self-contained, edited directly (no config/build) |
| `content/slideshow_ai/mockups/` | Live bilingual HTML demos linked from the keynote (automation, NLP, ML, transformer; plus the LLM deep-dive: tokenizer, base model, assistant, RLHF). Each has a `How it works?` toggle (`b` key) |
| `scripts/export_slideshow_ai_to_pdf.py` | Renders the keynote to `slideshow_ai_{en,es}.pdf` (one run per language); the PDFs are gitignored build artifacts |
| `content/exercises/` | Exercise folders: starter/solution/setup/data per exercise |
| `scripts/copy_data_to_live.py` | Facilitator tool: rebuilds the numbered `live/` bundle (starter + data per exercise, in slideshow order) that becomes the participant `live.zip` — see `content/preparation/live_preparation.md` |
| `content/preparation/` | Docs for building and extending the slideshow and images |
| `scripts/test_libraries.py` | Verifies installed libraries (including Streamlit); exits non-zero if any fails |
| `content/streamlit_demo/` | Streamlit reference app: main_menu.py, pages/, data/, scripts/ |
| `scripts/pip_ini_finder.py` | Finds pip configuration files |
| `requirements.txt` | Python dependencies |
| `content/metadata/` | Survey data dashboard: Streamlit app, config, and helper modules — see `content/metadata/README.md` |

The annotated repo tree and where new code goes: [docs/layout.md](docs/layout.md). The structural diagram is [docs/architecture.mmd](docs/architecture.mmd).

### Preparation docs

- `content/preparation/slideshow_part01_exercises.md` – How the basic slideshow was built
- `content/preparation/slideshow_part02_sequence.md` – Sequence, menu, and navigation
- `content/preparation/slideshow_part03_bonus.md` – Bonus section (menu, 8 exercises, navigation)
- `content/slideshow/slideshow_config.json` – Main and bonus exercise order; used by `scripts/build_slideshow.py` to generate the exercise data scripts and the Spanish shell
- `content/preparation/how_images_were_created.md` – How workshop images were made (Part 1: main set; Part 2: bonus images prompt for Gemini)

## Exercises

Exercises use a consistent layout: problem description (starter), solution code, and optional setup/data scripts.

- **Main menu (slideshow)**: Intro → ETL 1–3 → Viz 1–2 → Auto 1–2 → Bonus (Big Data Stress Test)
- **Bonus menu (slideshow)**: Auto PDF Report, ETL API Pipeline, D3 Bar/Force, Geo Heatmap, Interactive Dashboard, Seaborn Scatter/Statistical

See the slideshow for titles and goals; details live in each exercise folder under `content/exercises/`.

## Usage

1. **Presenting**: Open `content/slideshow/slideshow.html` and use the menu (or arrow keys) to move between exercises, bonus section, break, and survey.
2. **Doing exercises**: Go to the matching folder under `content/exercises/`, read the starter (or slideshow description), then code and run; compare with the solution if provided.
3. **Generating exercise data**: `content/exercises/*/data/` is not tracked. In each exercise folder run `exercise_setup_data.py` first to create its input files, then work from the starter or run `exercise_solution.py`. Run all of them before `scripts/copy_data_to_live.py`, which only copies the `data/` folders that exist into the `live/` bundle (`live.zip`).
4. **Internet access**: the HTML outputs of `viz_d3_bar_chart`, `viz_d3_force_network` and `viz_interactive_dashboard` load D3 / Plotly from a CDN, and the map tiles in `viz_geo_heatmap` come from OpenStreetMap, so those exercises need internet access on the participant machine (a blocked network shows a blank page or map).

## Contributing

- **New exercise**: Follow `content/preparation/metaprompt.md`; add a folder under `content/exercises/` with starter (bilingual: `## English` and `## Español` sections), solution, setup, and data; add the exercise to `content/slideshow/slideshow_config.json` (main or bonus list) and run `python3 scripts/build_slideshow.py` to regenerate `content/slideshow/slideshow_data_en.js`, `content/slideshow/slideshow_data_es.js` and `content/slideshow/slideshow_es.html`; add an image to `content/slideshow/assets/` if needed.
- **New bonus image**: Use the table and instructions in `content/preparation/how_images_were_created.md` Part 2, generate images (e.g. with Gemini), save as the listed `bonus_*.jpg` names in `content/slideshow/assets/`.
- **Ship gate**: before committing, run `.\scripts\verify-before-ship.ps1`. It needs `.venv\Scripts\python.exe` (see Quick Start) plus Node (`npx`) and `ruff` for the static ratchet. The gate also runs the dashboard's unit tests in `content/metadata/` (`test_*.py`, found by discovery), and its last stage runs every exercise's setup and solution (`scripts/validate_exercises.py`), so a solution that stops working fails it; run that script alone for a quicker check. The gate's last stdout line is `GATE-RESULT: PASS` or `GATE-RESULT: FAIL` (`scripts/test_gate_result.py` checks it), so assert on that line rather than the exit code when the output has to go through a pipe.

## Requirements

- Python 3.11+
- See `requirements.txt` for packages (e.g. pandas, numpy, matplotlib, seaborn, openpyxl, python-docx, python-pptx, fpdf, and others used by specific exercises). Versions are pinned to the set the exercises were last tested with (Python 3.14); re-test the exercises before bumping any of them.

## License

[Add license information if applicable]
