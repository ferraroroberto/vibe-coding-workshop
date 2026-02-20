#!/usr/bin/env python3
"""
Extract exercise content from slideshow.html and slideshow_es.html,
then update all exercise_starter.md files to match (bilingual format).

Usage: python3 scripts/sync_slideshow_to_starters.py
"""

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "preparation" / "slideshow_config.json"
SLIDESHOW_EN = PROJECT_ROOT / "slideshow" / "slideshow.html"
SLIDESHOW_ES = PROJECT_ROOT / "slideshow" / "slideshow_es.html"
EXERCISES_DIR = PROJECT_ROOT / "exercises"


def extract_content_from_template_literal(js_content: str, start_marker: str) -> str:
    """Extract content from a JavaScript template literal (backtick string)."""
    # Find content: `...` - need to handle nested backticks (escaped as \`)
    idx = js_content.find(start_marker)
    if idx == -1:
        return ""
    # Find opening backtick after content: `
    backtick_start = js_content.find("`", idx)
    if backtick_start == -1:
        return ""
    # Parse until we find unescaped closing backtick
    result = []
    i = backtick_start + 1
    while i < len(js_content):
        if js_content[i] == "\\" and i + 1 < len(js_content):
            # Escaped char - in our case \` becomes `
            if js_content[i + 1] == "`":
                result.append("`")
                i += 2
                continue
            result.append(js_content[i])
            result.append(js_content[i + 1])
            i += 2
            continue
        if js_content[i] == "`":
            break
        result.append(js_content[i])
        i += 1
    return "".join(result)


def extract_exercises_from_slideshow(html_path: Path) -> list[dict]:
    """Extract exercises array from slideshow HTML."""
    html = html_path.read_text(encoding="utf-8")
    # Find the exercises array - each item has number, title, image, content
    exercises = []
    # Match each exercise block
    pattern = r'\{\s*number:\s*"([^"]*)"\s*,\s*title:\s*"([^"]*(?:\\.[^"]*)*)"\s*,\s*image:\s*"([^"]*)"\s*,\s*content:\s*`'
    for m in re.finditer(pattern, html):
        number, title, image = m.group(1), m.group(2).replace('\\"', '"'), m.group(3)
        content_start = m.end()
        content = extract_content_from_template_literal(html[content_start - 1 :], "content:")
        exercises.append({"number": number, "title": title, "image": image, "content": content})
    return exercises


def extract_exercises_by_regex(html_path: Path) -> list[dict]:
    """Extract exercises by matching the structure more carefully."""
    html = html_path.read_text(encoding="utf-8")
    exercises = []
    # Find all exercise blocks - from { number: to the closing ` of content
    # Pattern: { number: "X", title: "Y", image: "Z", content: `...`
    pos = 0
    while True:
        start = html.find('number: "', pos)
        if start == -1:
            break
        # Find the start of this object (the { before number)
        obj_start = html.rfind("{", 0, start)
        if obj_start == -1:
            break
        # Extract number
        num_match = re.search(r'number:\s*"([^"]*)"', html[obj_start:])
        if not num_match:
            pos = start + 1
            continue
        # Extract title (may have escaped quotes)
        title_match = re.search(r'title:\s*"((?:[^"\\]|\\.)*)"', html[obj_start:])
        if not title_match:
            pos = start + 1
            continue
        title = title_match.group(1).replace('\\"', '"')
        # Find content: `...`
        content_marker = html.find("content: `", obj_start)
        if content_marker == -1 or content_marker > obj_start + 500:
            pos = start + 1
            continue
        content_start = content_marker + len("content: `")
        # Parse content until matching `
        content_parts = []
        i = content_start
        while i < len(html):
            if html[i] == "\\" and i + 1 < len(html):
                if html[i + 1] == "`":
                    content_parts.append("`")
                    i += 2
                else:
                    content_parts.append(html[i : i + 2])
                    i += 2
                continue
            if html[i] == "`":
                break
            content_parts.append(html[i])
            i += 1
        content = "".join(content_parts)
        exercises.append(
            {
                "number": num_match.group(1),
                "title": title,
                "content": content,
            }
        )
        pos = i + 1
    return exercises


def main():
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    en_html = SLIDESHOW_EN.read_text(encoding="utf-8")
    es_html = SLIDESHOW_ES.read_text(encoding="utf-8")

    def get_content(html: str, folder: str, is_bonus: bool) -> str:
        """Extract content for a specific exercise from HTML."""
        # Find the block for this folder - match by image path
        if is_bonus:
            img_pattern = f"assets/bonus_{folder}.jpg"
        else:
            img_pattern = f"assets/{folder}.jpg"
        idx = html.find(img_pattern)
        if idx == -1:
            return ""
        # Find content: ` before this (go backwards to find the start of this exercise)
        block_start = html.rfind("{", 0, idx)
        content_marker = html.find("content: `", block_start)
        if content_marker == -1:
            return ""
        content_start = content_marker + len("content: `")
        content_parts = []
        i = content_start
        while i < len(html):
            if html[i] == "\\" and i + 1 < len(html):
                if html[i + 1] == "`":
                    content_parts.append("`")
                    i += 2
                else:
                    content_parts.append(html[i : i + 2])
                    i += 2
                continue
            if html[i] == "`":
                break
            content_parts.append(html[i])
            i += 1
        return "".join(content_parts)

    for item in config["main_exercises"]:
        folder = item["folder"]
        en_content = get_content(en_html, folder, False)
        es_content = get_content(es_html, folder, False)
        if not en_content:
            print(f"Warning: No content found for {folder}")
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
        print(f"Updated {starter_path}")

    for item in config["bonus_exercises"]:
        folder = item["folder"]
        en_content = get_content(en_html, folder, True)
        es_content = get_content(es_html, folder, True)
        if not en_content:
            print(f"Warning: No content found for {folder}")
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
        print(f"Updated {starter_path}")


if __name__ == "__main__":
    main()
