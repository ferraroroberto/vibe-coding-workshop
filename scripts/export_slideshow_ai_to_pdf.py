import logging
import os
import sys

from _slideshow_pdf import render_slideshow_pdf

log = logging.getLogger(__name__)

# Freeze transitions/animations and hide the live-only language toggle so it
# never bleeds into the exported pages.
STYLES = [
    """
        * { transition: none !important; animation: none !important; }
        .slide .content { transition: none !important; }
        /* live-only language toggle — keep it out of the exported pages */
        .lang-toggle { display: none !important; }
    """,
]

# Activate slide `index`, refreshing the keynote's counter and title-tag chrome.
ACTIVATION_JS = """
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
"""


def export_slideshow(html_path: str, output_pdf: str, lang: str | None = None) -> None:
    render_slideshow_pdf(
        html_path,
        output_pdf,
        styles=STYLES,
        activation_js=ACTIVATION_JS,
        lang=lang,
        wait_networkidle=True,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    slideshow_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "slideshow_ai")
    )

    if len(sys.argv) > 1:
        # explicit file(s): one PDF each, default language
        for html_file in sys.argv[1:]:
            if not os.path.exists(html_file):
                log.error("File not found: %s — skipping", html_file)
                continue
            export_slideshow(html_file, os.path.splitext(html_file)[0] + ".pdf")
        sys.exit(0)

    # default: render the single bilingual deck once per language
    single = os.path.join(slideshow_dir, "slideshow_ai.html")
    if not os.path.exists(single):
        log.error("Deck not found: %s", single)
        sys.exit(1)

    for lang in ("en", "es"):
        output_file = os.path.join(slideshow_dir, f"slideshow_ai_{lang}.pdf")
        export_slideshow(single, output_file, lang=lang)
