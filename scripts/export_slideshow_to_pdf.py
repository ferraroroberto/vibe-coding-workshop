import logging
import os
import sys

from _slideshow_pdf import render_slideshow_pdf

log = logging.getLogger(__name__)

# Freeze transitions and force exactly one slide visible at a time.
STYLES = [
    """
        * { transition: none !important; }
        .slide { transition: none !important; opacity: 1 !important; display: none; }
        .slide.active { display: flex; }
    """,
    """
        .slide { transition: none !important; }
    """,
]

# Activate slide `index`, keeping the legacy counter hooks in sync if present.
ACTIVATION_JS = """
    (index) => {
        const slides = document.querySelectorAll('.slide');
        slides.forEach(s => s.classList.remove('active'));
        slides[index].classList.add('active');
        if (typeof currentSlide !== 'undefined') currentSlide = index;
        if (typeof updateCounter === 'function') updateCounter();
    }
"""


def export_slideshow(html_path, output_pdf):
    render_slideshow_pdf(html_path, output_pdf, styles=STYLES, activation_js=ACTIVATION_JS)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    default_target = os.path.join(os.path.dirname(__file__), "..", "slideshow", "slideshow.html")

    target_file = default_target
    if len(sys.argv) > 1:
        target_file = sys.argv[1]

    if not os.path.exists(target_file):
        log.error("Usage: python export_slideshow_to_pdf.py [path_to_html]")
        log.error("Default target not found: %s", default_target)
        sys.exit(1)

    output_file = os.path.splitext(target_file)[0] + ".pdf"
    export_slideshow(target_file, output_file)
