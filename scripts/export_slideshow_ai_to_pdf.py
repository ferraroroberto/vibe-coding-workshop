import logging
import os
import sys
from glob import glob
from playwright.sync_api import sync_playwright
from PIL import Image

log = logging.getLogger(__name__)


def export_slideshow(html_path: str, output_pdf: str) -> None:
    abs_html_path = os.path.abspath(html_path)
    if not os.path.exists(abs_html_path):
        log.error("File not found: %s", abs_html_path)
        return

    log.info("Opening content from: %s", abs_html_path)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        url = f'file:///{abs_html_path}'
        page.goto(url)
        page.wait_for_load_state('networkidle')

        try:
            page.wait_for_selector('.slide', timeout=10000)
        except Exception as e:
            log.error("Slides did not load within timeout: %s", e)
            browser.close()
            return

        page.add_style_tag(content="""
            * { transition: none !important; animation: none !important; }
            .slide .content { transition: none !important; }
        """)

        total_slides = page.evaluate("document.querySelectorAll('.slide').length")
        log.info("Found %d slides.", total_slides)

        screenshot_paths = []
        temp_dir = os.path.join(os.path.dirname(abs_html_path), "tmp_pdf_slides")
        os.makedirs(temp_dir, exist_ok=True)

        for i in range(total_slides):
            page.evaluate("""
                (index) => {
                    const slides = document.querySelectorAll('.slide');
                    slides.forEach(s => s.classList.remove('active', 'text-visible'));
                    slides[index].classList.add('active', 'text-visible');
                    const counter = document.getElementById('counter');
                    if (counter) counter.textContent = `${index + 1} / ${slides.length}`;
                    const titleTag = document.getElementById('title-tag');
                    if (titleTag && typeof window.slides !== 'undefined') {
                        titleTag.textContent = window.slides[index]?.tag || '';
                    }
                }
            """, i)

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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    if len(sys.argv) > 1:
        html_files = sys.argv[1:]
    else:
        slideshow_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "slideshow_ai")
        )
        html_files = sorted(glob(os.path.join(slideshow_dir, "slideshow_ai_*.html")))

    if not html_files:
        log.error("No slideshow HTML files found in slideshow_ai/.")
        sys.exit(1)

    for html_file in html_files:
        if not os.path.exists(html_file):
            log.error("File not found: %s — skipping", html_file)
            continue
        output_file = os.path.splitext(html_file)[0] + ".pdf"
        export_slideshow(html_file, output_file)
