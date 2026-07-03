"""Build the participant `live/` bundle from the workshop exercises.

Facilitator tooling. Reads the exercise order straight from the Spanish
slideshow, then copies each exercise's `data/` folder and `exercise_starter.md`
into a fresh, numbered `live/` tree (`00_Intro_Hello_World`, `01_...`). That
tree is what gets zipped into the `live.zip` participants download (see
`preparation/live_preparation.md`).

Destructive: rebuilding wipes and recreates the `live/` folder. Nothing runs on
import — call `main()` (or run the file) to do the work.

    python scripts/copy_data_to_live.py
"""

import logging
import os
import re
import shutil
from pathlib import Path

log = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXERCISES_DIR = PROJECT_ROOT / "exercises"
LIVE_DIR = PROJECT_ROOT / "live"
SLIDESHOW_FILE = PROJECT_ROOT / "slideshow" / "slideshow_es.html"

# Display names for specific folder names (keys are FOLDER names).
DISPLAY_NAMES = {
    "intro_python": "Intro_Hello_World",
    "etl_merger": "The_Great_Merger",
    "etl_detective": "The_Detective",
    "etl_survey": "The_Messy_Survey",
    "viz_managers_chart": "The_Managers_Chart",
    "viz_report_generator": "The_Report_Generator",
    "auto_excel_polish": "The_Professional_Polish",
    "auto_file_organizer": "The_File_Organizer",
    "etl_bonus_big_data": "The_Big_Data_Stress_Test",
    "auto_pdf_report": "Auto_PDF_Report",
    "etl_api_pipeline": "ETL_API_Pipeline",
    "viz_d3_bar_chart": "D3_Bar_Chart",
    "viz_d3_force_network": "D3_Force_Network",
    "viz_geo_heatmap": "Viz_Geo_Heatmap",
    "viz_interactive_dashboard": "Interactive_Dashboard",
    "viz_seaborn_scatter": "Seaborn_Scatter",
    "viz_seaborn_statistical": "Seaborn_Statistical",
}


def read_exercise_order(slideshow_file: Path) -> list[str]:
    """Return exercise folder names in slideshow order, parsed from its images."""
    content = slideshow_file.read_text(encoding="utf-8")
    order = []
    for match in re.findall(r'image: "assets/([^"]+)\.jpg"', content):
        folder_name = match
        if folder_name.startswith("bonus_"):
            folder_name = folder_name.replace("bonus_", "")
        order.append(folder_name)
    return order


def build_live_bundle(
    exercises_dir: Path, live_dir: Path, exercise_order: list[str]
) -> int:
    """Rebuild `live_dir` with a numbered folder per exercise that has materials.

    Wipes any existing `live_dir` first. Returns the number of exercises copied.
    """
    if live_dir.exists():
        log.info("Removing existing live folder: %s", live_dir)
        shutil.rmtree(live_dir)
    live_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    for i, exercise in enumerate(exercise_order):
        exercise_path = exercises_dir / exercise
        if not exercise_path.is_dir():
            log.warning("Exercise folder not found, skipping: %s", exercise)
            continue

        data_dir = exercise_path / "data"
        starter_file = exercise_path / "exercise_starter.md"
        has_data = data_dir.exists()
        has_starter = starter_file.is_file()
        if not (has_data or has_starter):
            continue

        display_name = DISPLAY_NAMES.get(exercise, exercise)
        numbered_name = f"{i:02d}_{display_name}"
        live_exercise_dir = live_dir / numbered_name
        live_exercise_dir.mkdir(parents=True, exist_ok=True)

        if has_data:
            shutil.copytree(data_dir, live_exercise_dir / "data")
        if has_starter:
            shutil.copy2(starter_file, live_exercise_dir / "exercise_starter.md")
        log.info("Built %s", numbered_name)
        copied += 1

    return copied


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    if not SLIDESHOW_FILE.exists():
        log.error("Slideshow not found: %s", SLIDESHOW_FILE)
        raise SystemExit(1)

    exercise_order = read_exercise_order(SLIDESHOW_FILE)
    copied = build_live_bundle(EXERCISES_DIR, LIVE_DIR, exercise_order)
    log.info("Done: %d exercise(s) copied into %s", copied, LIVE_DIR)


if __name__ == "__main__":
    main()
