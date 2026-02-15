# Python Vibe-Coding Workshop

A hands-on workshop for learning data manipulation, automation, and visualization with Python in a corporate setting. Includes a **slideshow** for presenting exercises, plus structured exercises (main + bonus) with starter files, solutions, and sample data.

## Features

- **Slideshow**: Single-file HTML presentation (`slideshow.html`) with exercise menu, bonus section, and navigation (open in a browser)
- **Main exercises**: Intro, ETL (merge, clean, survey), Viz (charts, reports), Auto (Excel polish, file organizer), plus Bonus “Big Data Stress Test”
- **Bonus exercises**: PDF report, API pipeline, D3 bar/force viz, geo heatmap, interactive dashboard, Seaborn scatter/statistical
- **Library testing**: `test_libraries.py` to verify required libraries
- **Environment tools**: `pip_ini_finder.py` for locating pip config; `requirements.txt` for dependencies

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

3. Run the slideshow: open `slideshow.html` in a browser (no server needed).

4. (Optional) Test the environment:
   ```bash
   python test_libraries.py
   ```

## Project Structure

| Path | Description |
|------|-------------|
| `slideshow.html` | Workshop slideshow: welcome, menu, main/bonus exercises, break, survey, congratulations |
| `assets/` | Images for slideshow (one per exercise + welcome, menu, break, survey, etc.) |
| `exercises/` | Exercise folders: starter/solution/setup/data per exercise |
| `preparation/` | Docs for building and extending the slideshow and images |
| `test_libraries.py` | Verifies installed libraries |
| `pip_ini_finder.py` | Finds pip configuration files |
| `requirements.txt` | Python dependencies |

### Preparation docs

- `preparation/slideshow_part01_exercises.md` – How the basic slideshow was built
- `preparation/slideshow_part02_sequence.md` – Sequence, menu, and navigation
- `preparation/slideshow_part03_bonus.md` – Bonus section (menu, 8 exercises, navigation)
- `preparation/how_images_were_created.md` – How workshop images were made (Part 1: main set; Part 2: bonus images prompt for Gemini)

## Exercises

Exercises use a consistent layout: problem description (starter), solution code, and optional setup/data scripts.

- **Main menu (slideshow)**: Intro → ETL 1–3 → Viz 1–2 → Auto 1–2 → Bonus (Big Data Stress Test)
- **Bonus menu (slideshow)**: Auto PDF Report, ETL API Pipeline, D3 Bar/Force, Geo Heatmap, Interactive Dashboard, Seaborn Scatter/Statistical

See the slideshow for titles and goals; details live in each exercise folder under `exercises/`.

## Usage

1. **Presenting**: Open `slideshow.html` and use the menu (or arrow keys) to move between exercises, bonus section, break, and survey.
2. **Doing exercises**: Go to the matching folder under `exercises/`, read the starter (or slideshow description), then code and run; compare with the solution if provided.

## Contributing

- **New exercise**: Follow `exercises/metaprompt.md`; add a folder under `exercises/` with starter, solution, setup, and data; add the exercise to the slideshow data in `slideshow.html` (and to `assets/` if you add an image).
- **New bonus image**: Use the table and instructions in `preparation/how_images_were_created.md` Part 2, generate images (e.g. with Gemini), save as the listed `bonus_*.jpg` names in `assets/`.

## Requirements

- Python 3.7+
- See `requirements.txt` for packages (e.g. pandas, numpy, matplotlib, seaborn, openpyxl, python-docx, python-pptx, fpdf, and others used by specific exercises).

## License

[Add license information if applicable]
