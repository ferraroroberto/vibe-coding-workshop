#!/usr/bin/env python3
"""
Build slideshow.html and slideshow_es.html from exercise_starter.md files.

Reads preparation/slideshow_config.json for main and bonus exercise order.
Parses each exercise_starter.md for ## English and ## Español sections.
Outputs both English and Spanish slideshows.

Run from project root: python scripts/build_slideshow.py
"""

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "preparation" / "slideshow_config.json"
EXERCISES_DIR = PROJECT_ROOT / "exercises"
SLIDESHOW_PATH = PROJECT_ROOT / "slideshow" / "slideshow.html"
SLIDESHOW_ES_PATH = PROJECT_ROOT / "slideshow" / "slideshow_es.html"


def parse_exercise_starter(md_path: Path) -> tuple[str, str]:
    """
    Parse exercise_starter.md. Returns (english_content, spanish_content).
    If ## English / ## Español sections exist, use them. Otherwise use whole content as English.
    """
    if not md_path.exists():
        return ("# Missing\n\nExercise file not found.", "# Faltante\n\nArchivo de ejercicio no encontrado.")

    text = md_path.read_text(encoding="utf-8")

    # Try to find ## English and ## Español sections
    english_match = re.search(r"##\s+English\s*\n(.*?)(?=\n---|\n##\s+Español|$)", text, re.DOTALL)
    spanish_match = re.search(r"##\s+Español\s*\n(.*?)(?=\n---|$)", text, re.DOTALL)

    if english_match and spanish_match:
        english = english_match.group(1).strip()
        spanish = spanish_match.group(1).strip()
        return (english, spanish)

    # Fallback: use whole content as English, same as placeholder for Spanish
    content = text.strip()
    return (content, content)


def extract_title(content: str) -> str:
    """Extract title from first # heading in content."""
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else "Exercise"


def js_escape(content: str) -> str:
    """Escape content for use inside JavaScript template literal (backticks)."""
    return content.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")


def build_exercise_js(exercises_data: list[dict], lang: str) -> str:
    """Build JavaScript array string for exercises."""
    lines = [
        "        // Exercise data - matches the sequence from exercises_selection.md",
        "        const exercises = [",
    ]
    for ex in exercises_data:
        title = ex["title_" + lang] if f"title_{lang}" in ex else ex["title_en"]
        content = ex["content_" + lang] if f"content_{lang}" in ex else ex["content_en"]
        content_escaped = js_escape(content)
        lines.append(f'            {{\n                number: "{ex["number"]}",')
        lines.append(f'                title: "{title.replace(chr(34), chr(92)+chr(34))}",')
        lines.append(f'                image: "{ex["image"]}",')
        lines.append(f'                content: `{content_escaped}`')
        lines.append("            },")
    lines.append("        ];")
    return "\n".join(lines)


def build_bonus_exercises_js(bonus_data: list[dict], lang: str) -> str:
    """Build JavaScript array string for bonus exercises."""
    lines = ["        const bonusExercises = ["]
    for ex in bonus_data:
        title = ex["title_" + lang] if f"title_{lang}" in ex else ex["title_en"]
        content = ex["content_" + lang] if f"content_{lang}" in ex else ex["content_en"]
        content_escaped = js_escape(content)
        lines.append(f'            {{\n                number: "{ex["number"]}",')
        lines.append(f'                title: "{title.replace(chr(34), chr(92)+chr(34))}",')
        lines.append(f'                image: "{ex["image"]}",')
        lines.append(f'                content: `{content_escaped}`')
        lines.append("            },")
    lines.append("        ];")
    return "\n".join(lines)


def load_exercise_data(config: dict) -> tuple[list[dict], list[dict]]:
    """Load main and bonus exercise data from exercise_starter.md files."""
    main_data = []
    for item in config["main_exercises"]:
        md_path = EXERCISES_DIR / item["folder"] / "exercise_starter.md"
        en_content, es_content = parse_exercise_starter(md_path)
        main_data.append({
            "number": item["number"],
            "image": item["image"],
            "title_en": extract_title(en_content),
            "title_es": extract_title(es_content),
            "content_en": en_content,
            "content_es": es_content,
        })

    bonus_data = []
    for item in config["bonus_exercises"]:
        md_path = EXERCISES_DIR / item["folder"] / "exercise_starter.md"
        en_content, es_content = parse_exercise_starter(md_path)
        bonus_data.append({
            "number": item["number"],
            "image": item["image"],
            "title_en": extract_title(en_content),
            "title_es": extract_title(es_content),
            "content_en": en_content,
            "content_es": es_content,
        })

    return main_data, bonus_data


def replace_exercises_array(html: str, exercises_js: str) -> str:
    """Replace the exercises array in the HTML."""
    pattern = r"// Exercise data - matches the sequence from exercises_selection\.md\s*\n\s*const exercises = \[[\s\S]*?\n        \];"
    return re.sub(pattern, exercises_js, html)


def replace_bonus_exercises_array(html: str, bonus_js: str) -> str:
    """Replace the bonusExercises array in the HTML."""
    pattern = r"// Bonus-only exercises \(separate menu\)[^\n]*\n\s*const mainExercises = exercises;\n\s*const bonusExercises = \[[\s\S]*?\n        \];"
    replacement = "// Bonus-only exercises (separate menu); main menu shows all of `exercises` including \"The Big Data Stress Test\"\n        const mainExercises = exercises;\n        " + bonus_js
    return re.sub(pattern, replacement, html)


def apply_ui_strings(html: str, ui: dict) -> str:
    """Replace UI strings in the HTML with locale-specific ones."""
    replacements = [
        ("Bonus Exercises", ui["bonus_exercises"]),
        ("Break Time", ui["break_time_btn"]),
        ("Finish Session", ui["finish_session"]),
        ("← Back to Menu", ui["back_to_menu"]),
        ("← Bonus Menu", ui["bonus_menu"]),
        ("← Main Menu", ui["main_menu"]),
        ("← Menu", ui["menu"]),
        ("← Back to Bonus", ui["back_to_bonus"]),
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    # Bonus menu heading
    html = re.sub(
        r'<h2 style="color: white; margin-bottom: 1rem;">Bonus Exercises</h2>',
        f'<h2 style="color: white; margin-bottom: 1rem;">{ui["bonus_exercises"]}</h2>',
        html,
    )
    return html


def main():
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    main_data, bonus_data = load_exercise_data(config)

    # Read template (use existing slideshow.html as base)
    html_en = SLIDESHOW_PATH.read_text(encoding="utf-8")

    # Build exercises JS - need to match the exact format (mainExercises = exercises, bonusExercises separate)
    exercises_js_en = build_exercise_js(main_data, "en")
    bonus_js_en = build_bonus_exercises_js(bonus_data, "en")
    exercises_js_es = build_exercise_js(main_data, "es")
    bonus_js_es = build_bonus_exercises_js(bonus_data, "es")

    # Replace in English version
    html_en = replace_exercises_array(html_en, exercises_js_en)
    html_en = replace_bonus_exercises_array(html_en, bonus_js_en)

    # Write English slideshow
    SLIDESHOW_PATH.write_text(html_en, encoding="utf-8")
    print(f"Wrote {SLIDESHOW_PATH}")

    # Build Spanish version
    html_es = html_en  # Start from updated English
    html_es = replace_exercises_array(html_es, exercises_js_es)
    html_es = replace_bonus_exercises_array(html_es, bonus_js_es)
    html_es = apply_ui_strings(html_es, config["ui_strings"]["es"])

    # Update lang and title for Spanish
    html_es = html_es.replace('lang="en"', 'lang="es"', 1)
    html_es = html_es.replace("<title>Workshop Exercises Slideshow</title>", "<title>Taller de Ejercicios - Presentación</title>", 1)

    SLIDESHOW_ES_PATH.write_text(html_es, encoding="utf-8")
    print(f"Wrote {SLIDESHOW_ES_PATH}")


if __name__ == "__main__":
    main()
