# Python Vibe-Coding Workshop

A hands-on workshop for learning data manipulation, automation, and visualization with Python in a corporate setting. Includes a **slideshow** for presenting exercises, plus structured exercises (main + bonus) with starter files, solutions, and sample data.

## Features

- **Vibe Coding Tips**: HTML slide presentation (`tips/index.html`) — playful, keyboard-navigable slides on practical LLM workflow tips (model selection, auto-approve, agents, markdown logging, validation, etc.) with full docs in `tips/docs/` and examples in `tips/examples/`
- **Slideshow**: Single-file HTML presentation (`slideshow/slideshow.html`, `slideshow/slideshow_es.html` for Spanish) with exercise menu, bonus section, and navigation (open in a browser)
- **"Not Everything Is AI" keynote**: Standalone bilingual talk deck (`slideshow_ai/slideshow_ai.html`) — self-contained, no build step, in-page ES/EN toggle (or `?lang=en|es`), arrow/space navigation plus `B` to open a slide's link (presentation clicker), with live HTML demos in `slideshow_ai/mockups/`
- **Main exercises**: Intro, ETL (merge, clean, survey), Viz (charts, reports), Auto (Excel polish, file organizer), plus Bonus “Big Data Stress Test”
- **Bonus exercises**: PDF report, API pipeline, D3 bar/force viz, geo heatmap, interactive dashboard, Seaborn scatter/statistical
- **Library testing**: `scripts/test_libraries.py` to verify required libraries and serves as the post-`pip install` smoke check for the Quick Start
- **Streamlit demo**: `streamlit_demo/` — multi-page reference app (inputs, viz, CRUD, file upload, process runner, session state)
- **Survey Data Dashboard**: `metadata/` — Streamlit dashboard for visualizing and managing survey data, with data entry, organizational import, and participation-rate treemaps (see `metadata/README.md`)
- **Environment tools**: `scripts/pip_ini_finder.py` for locating pip config; `requirements.txt` for dependencies

## Quick Start

1. Clone and enter the repo:
   ```bash
   git clone <repository-url>
   cd vibe-coding-workshop
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run a presentation: open `slideshow/slideshow.html` (workshop exercises) or `tips/index.html` (Vibe Coding Tips & Tricks) in a browser (no server needed). Use arrow keys to navigate the tips slides.

4. (Optional) Test the environment:
   ```bash
   python scripts/test_libraries.py
   ```

5. (Optional) Run the Streamlit demo:
   ```bash
   cd streamlit_demo && streamlit run main_menu.py
   ```
   Or on Windows, double-click `streamlit_demo/run_app.bat`.

## Project Structure

| Path | Description |
|------|-------------|
| `tips/` | Vibe Coding Tips presentation: `index.html` (slides), `styles.css`, `script.js`, `docs/vibe-coding-tips.md`, `examples/*.md` (12 tip examples) |
| `slideshow/slideshow.html` | Workshop slideshow (English): welcome, menu, main/bonus exercises, break, survey, congratulations |
| `slideshow/slideshow_es.html` | Spanish version of the slideshow |
| `slideshow/assets/` | Images for slideshow (one per exercise + welcome, menu, break, survey, etc.) |
| `slideshow_ai/slideshow_ai.html` | Standalone bilingual keynote "Not Everything Is AI / No Todo Es IA" (ES/EN toggle, `?lang=`); self-contained, edited directly (no config/build) |
| `slideshow_ai/mockups/` | Live bilingual HTML demos linked from the keynote (automation, NLP, ML, transformer; plus the LLM deep-dive: tokenizer, base model, assistant, RLHF). Each has a `How it works?` toggle (`b` key) |
| `scripts/export_slideshow_ai_to_pdf.py` | Renders the keynote to `slideshow_ai_{en,es}.pdf` (one run per language); the PDFs are gitignored build artifacts |
| `exercises/` | Exercise folders: starter/solution/setup/data per exercise |
| `scripts/copy_data_to_live.py` | Facilitator tool: rebuilds the numbered `live/` bundle (starter + data per exercise, in slideshow order) that becomes the participant `live.zip` — see `preparation/live_preparation.md` |
| `preparation/` | Docs for building and extending the slideshow and images |
| `scripts/test_libraries.py` | Verifies installed libraries (including Streamlit) |
| `streamlit_demo/` | Streamlit reference app: main_menu.py, pages/, data/, scripts/ |
| `scripts/pip_ini_finder.py` | Finds pip configuration files |
| `requirements.txt` | Python dependencies |
| `metadata/` | Survey data dashboard: Streamlit app, config, and helper modules — see `metadata/README.md` |

### Preparation docs

- `preparation/slideshow_part01_exercises.md` – How the basic slideshow was built
- `preparation/slideshow_part02_sequence.md` – Sequence, menu, and navigation
- `preparation/slideshow_part03_bonus.md` – Bonus section (menu, 8 exercises, navigation)
- `slideshow/slideshow_config.json` – Main and bonus exercise order; used by `scripts/build_slideshow.py` to generate slideshows
- `preparation/how_images_were_created.md` – How workshop images were made (Part 1: main set; Part 2: bonus images prompt for Gemini)

## Exercises

Exercises use a consistent layout: problem description (starter), solution code, and optional setup/data scripts.

- **Main menu (slideshow)**: Intro → ETL 1–3 → Viz 1–2 → Auto 1–2 → Bonus (Big Data Stress Test)
- **Bonus menu (slideshow)**: Auto PDF Report, ETL API Pipeline, D3 Bar/Force, Geo Heatmap, Interactive Dashboard, Seaborn Scatter/Statistical

See the slideshow for titles and goals; details live in each exercise folder under `exercises/`.

## Usage

1. **Presenting**: Open `slideshow/slideshow.html` and use the menu (or arrow keys) to move between exercises, bonus section, break, and survey.
2. **Doing exercises**: Go to the matching folder under `exercises/`, read the starter (or slideshow description), then code and run; compare with the solution if provided.

## Contributing

- **New exercise**: Follow `preparation/metaprompt.md`; add a folder under `exercises/` with starter (bilingual: `## English` and `## Español` sections), solution, setup, and data; add the exercise to `slideshow/slideshow_config.json` (main or bonus list) and run `python3 scripts/build_slideshow.py` to regenerate `slideshow/slideshow.html` and `slideshow/slideshow_es.html`; add an image to `slideshow/assets/` if needed.
- **New bonus image**: Use the table and instructions in `preparation/how_images_were_created.md` Part 2, generate images (e.g. with Gemini), save as the listed `bonus_*.jpg` names in `slideshow/assets/`.

## Requirements

- Python 3.11+
- See `requirements.txt` for packages (e.g. pandas, numpy, matplotlib, seaborn, openpyxl, python-docx, python-pptx, fpdf, and others used by specific exercises).

## License

[Add license information if applicable]
