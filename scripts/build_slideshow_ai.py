#!/usr/bin/env python3
"""
Build slideshow_ai_{lang}.html for every language in slideshow_ai_config.json.

Edit slides in the config file, then run this script to regenerate all HTML files.
Run from project root: python scripts/build_slideshow_ai.py
"""

import json
import logging
import re
from pathlib import Path

log = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "slideshow_ai" / "slideshow_ai_config.json"
TEMPLATE_PATH = PROJECT_ROOT / "slideshow_ai" / "slideshow_ai_en.html"


def js_escape(html: str) -> str:
    return html.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")


def build_slides_js(slides: list[dict]) -> str:
    lines = ["        const slides = ["]
    for s in slides:
        type_val = s["type"].replace("'", "\\'")
        image_val = s.get("image", "").replace("'", "\\'")
        tag_val = s.get("tag", "").replace("'", "\\'")
        html_escaped = js_escape(s["html"])

        lines.append("            {")
        if image_val:
            lines.append(f"                type: '{type_val}', image: '{image_val}', tag: '{tag_val}',")
        else:
            lines.append(f"                type: '{type_val}', tag: '{tag_val}',")
        lines.append(f"                html: `{html_escaped}`")
        lines.append("            },")
    lines.append("        ];")
    return "\n".join(lines)


def replace_slides_array(html: str, slides_js: str) -> str:
    pattern = r"        const slides = \[[\s\S]*?\n        \];"
    result, n = re.subn(pattern, slides_js, html)
    if n == 0:
        raise ValueError("Could not find 'const slides = [...]' in template — pattern mismatch")
    return result


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    titles = config.get("title", {})
    all_slides = config["slides"]

    template_html = TEMPLATE_PATH.read_text(encoding="utf-8")
    log.info("Loaded template from %s", TEMPLATE_PATH)

    for lang, slides in all_slides.items():
        html = template_html
        if lang in titles:
            html = re.sub(r"<title>[^<]*</title>", f"<title>{titles[lang]}</title>", html)
        slides_js = build_slides_js(slides)
        html = replace_slides_array(html, slides_js)
        output_path = PROJECT_ROOT / "slideshow_ai" / f"slideshow_ai_{lang}.html"
        output_path.write_text(html, encoding="utf-8")
        log.info("Wrote %s (%d slides)", output_path, len(slides))


if __name__ == "__main__":
    main()
