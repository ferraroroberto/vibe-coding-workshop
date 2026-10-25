#!/usr/bin/env python3
"""
Extract exercise content from slideshow_data_en.js and slideshow_data_es.js,
then update all exercise_starter.md files to match (bilingual format).

Usage: python3 scripts/sync_slideshow_to_starters.py
"""

import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "slideshow" / "slideshow_config.json"
SLIDESHOW_EN = PROJECT_ROOT / "slideshow" / "slideshow_data_en.js"
SLIDESHOW_ES = PROJECT_ROOT / "slideshow" / "slideshow_data_es.js"
EXERCISES_DIR = PROJECT_ROOT / "exercises"


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    en_js = SLIDESHOW_EN.read_text(encoding="utf-8")
    es_js = SLIDESHOW_ES.read_text(encoding="utf-8")

    def get_content(js: str, folder: str, is_bonus: bool) -> str:
        """Extract content for a specific exercise from a data script."""
        # Find the block for this folder - match by image path
        if is_bonus:
            img_pattern = f"assets/bonus_{folder}.jpg"
        else:
            img_pattern = f"assets/{folder}.jpg"
        idx = js.find(img_pattern)
        if idx == -1:
            return ""
        # Find content: ` before this (go backwards to find the start of this exercise)
        block_start = js.rfind("{", 0, idx)
        content_marker = js.find("content: `", block_start)
        if content_marker == -1:
            return ""
        content_start = content_marker + len("content: `")
        content_parts = []
        i = content_start
        while i < len(js):
            if js[i] == "\\" and i + 1 < len(js):
                if js[i + 1] == "`":
                    content_parts.append("`")
                    i += 2
                else:
                    content_parts.append(js[i : i + 2])
                    i += 2
                continue
            if js[i] == "`":
                break
            content_parts.append(js[i])
            i += 1
        return "".join(content_parts)

    for item in config["main_exercises"]:
        folder = item["folder"]
        en_content = get_content(en_js, folder, False)
        es_content = get_content(es_js, folder, False)
        if not en_content:
            log.warning("No content found for %s", folder)
            continue
        if not es_content:
            es_content = en_content  # Fallback
        starter_path = EXERCISES_DIR / folder / "exercise_starter.md"
        starter_path.parent.mkdir(parents=True, exist_ok=True)
        content = f"""## English

{en_content}

---

## Español

{es_content}
"""
        starter_path.write_text(content, encoding="utf-8")
        log.info("Updated %s", starter_path)

    for item in config["bonus_exercises"]:
        folder = item["folder"]
        en_content = get_content(en_js, folder, True)
        es_content = get_content(es_js, folder, True)
        if not en_content:
            log.warning("No content found for %s", folder)
            continue
        if not es_content:
            es_content = en_content
        starter_path = EXERCISES_DIR / folder / "exercise_starter.md"
        content = f"""## English

{en_content}

---

## Español

{es_content}
"""
        starter_path.write_text(content, encoding="utf-8")
        log.info("Updated %s", starter_path)


if __name__ == "__main__":
    main()
