"""Shared Playwright -> PDF renderer for the workshop slideshows.

Both ``export_slideshow_to_pdf`` (the workshop deck) and
``export_slideshow_ai_to_pdf`` (the keynote) drive the same pipeline: open the
HTML in headless Chromium, walk every ``.slide`` activating one at a time,
screenshot each, then stitch the PNGs into a single PDF with Pillow. They differ
only in the freeze CSS, the per-slide activation JS, and whether the AI deck's
``?lang=`` query + ``networkidle`` wait apply. Those three differences are
arguments; the scaffolding lives here once instead of in two near-copies.
"""

import logging
import os

from playwright.sync_api import sync_playwright
from PIL import Image

log = logging.getLogger(__name__)


def render_slideshow_pdf(
    html_path,
    output_pdf,
    *,
    styles,
    activation_js,
    lang=None,
    wait_networkidle=False,
):
    """Render every ``.slide`` of ``html_path`` to ``output_pdf``.

    ``styles`` is a list of CSS snippets injected via ``add_style_tag`` (the
    workshop deck needs two, the keynote one). ``activation_js`` is the
    ``(index) => {...}`` function called once per slide. ``lang`` appends a
    ``?lang=`` query and is logged; ``wait_networkidle`` adds a post-navigation
    ``networkidle`` wait.
    """
    abs_html_path = os.path.abspath(html_path)
    if not os.path.exists(abs_html_path):
        log.error("File not found: %s", abs_html_path)
        return

    log.info("Opening content from: %s%s", abs_html_path, f" (lang={lang})" if lang else "")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        url = f'file:///{abs_html_path}'
        if lang:
            url += f'?lang={lang}'
        page.goto(url)
        if wait_networkidle:
            page.wait_for_load_state('networkidle')

        try:
            page.wait_for_selector('.slide', timeout=10000)
        except Exception as e:
            log.error("Slides did not load within timeout: %s", e)
            browser.close()
            return

        for style in styles:
            page.add_style_tag(content=style)

        total_slides = page.evaluate("document.querySelectorAll('.slide').length")
        log.info("Found %d slides.", total_slides)

        screenshot_paths = []
        temp_dir = os.path.join(os.path.dirname(abs_html_path), "tmp_pdf_slides")
        os.makedirs(temp_dir, exist_ok=True)

        for i in range(total_slides):
            page.evaluate(activation_js, i)

            temp_path = os.path.join(temp_dir, f"slide_{i:03d}.png")
            page.screenshot(path=temp_path)
            screenshot_paths.append(temp_path)
            log.info("Captured slide %d/%d", i + 1, total_slides)

        browser.close()

        log.info("Compiling PDF...")
        if screenshot_paths:
            first_image = Image.open(screenshot_paths[0]).convert('RGB')
            other_images = [Image.open(p).convert('RGB') for p in screenshot_paths[1:]]

            first_image.save(
                output_pdf,
                "PDF",
                resolution=100.0,
                save_all=True,
                append_images=other_images
            )
            log.info("Successfully created PDF: %s", output_pdf)

            log.info("Cleaning up temporary images...")
            for p in screenshot_paths:
                try:
                    os.remove(p)
                except Exception:
                    pass
            try:
                os.rmdir(temp_dir)
            except Exception:
                pass
