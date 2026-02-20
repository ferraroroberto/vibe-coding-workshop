# Slideshow PDF Export Guide

This guide documents the process and tools used to generate a static PDF version of the HTML slideshow. This allows for easier sharing and offline viewing of the workshop materials.

## Overview

The slideshow is a dynamic HTML/JS application located at `slideshow/slideshow.html`. To convert this into a PDF, we cannot simply "Print to PDF" from a browser because the slideshow renders content dynamically using JavaScript and controls visibility with CSS classes.

Instead, we use a programmatic approach with **Playwright** (a browser automation tool) to step through each slide, capture a high-quality screenshot, and stitch them together.

## Prerequisites

The following Python packages are required (included in `requirements.txt`):
- `playwright`: For controlling a headless browser.
- `Pillow` (PIL): For image processing and creating the PDF.

Before running the script for the first time, you must install the Playwright browser binaries:

```bash
pip install -r requirements.txt
playwright install chromium
```

## The Export Script

The conversion logic is contained in `scripts/export_slideshow_to_pdf.py`.

### How it Works

1.  **Headless Browser**: The script launches a headless Chromium instance.
2.  **Loads Content**: It opens the local `slideshow/slideshow.html` file.
3.  **Disables Animations**: It injects CSS to disable all transitions. This ensures screenshots are crisp and instant, avoiding motion blur or "fading in" artifacts.
4.  **Iterates Slides**: It detects the total number of slides and programmatically activates each one (by modifying CSS classes via JavaScript).
5.  **Captures Screenshots**: It takes a full-resolution (1920x1080) PNG screenshot of every slide.
6.  **Compiles PDF**: Finally, it uses the Pillow library to merge all PNGs into a single PDF file.

## Usage

To generate the PDF, simply run the script from the project root:

```bash
python scripts/export_slideshow_to_pdf.py
```

By default, it looks for `slideshow/slideshow.html` relative to the project root and outputs `slideshow/slideshow.pdf` in the same location.

You can also specify a custom path:

```bash
python scripts/export_slideshow_to_pdf.py slideshow/slideshow.html
```
