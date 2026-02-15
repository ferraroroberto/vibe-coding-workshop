# Exercise Card: Viz 7 - The Animated Bar Race (D3.js)

## Title & Problem Statement
**The Animated Bar Race: Generating D3.js Visualizations from Python**

D3.js (Data-Driven Documents) is the gold standard for web-based data visualization. While Python libraries like matplotlib and seaborn generate static images, D3 produces interactive, animated, browser-native visualizations powered by SVG and JavaScript. In this exercise, you will use Python for what it does best — data preparation — and then generate a complete HTML file with embedded D3.js code that creates an animated "bar chart race." This is the bridge between Python data engineering and front-end data visualization.

## Difficulty & Estimated Time
*   **Difficulty:** Intermediate-Advanced (Cross-Technology: Python + D3.js)
*   **Estimated Time:** 35-45 Minutes

## Required Libraries
*   `pandas`: Data aggregation and time-series pivoting.
*   `json`: Serializing Python data structures into JSON for embedding in HTML/JavaScript.
*   No D3 installation needed — D3.js is loaded via CDN (`<script src="https://d3js.org/d3.v7.min.js">`).

## Didactic Step-by-Step

### 1. Data Preparation in Python
**Concept:** D3 consumes JSON. Python transforms raw CSV into the exact JSON shape D3 needs.
*   **Action:** Load sales data, group by month and product, compute cumulative revenue, rank products per month, and take top 10 per month.

### 2. JSON Serialization
**Concept:** Python dictionaries map directly to JavaScript objects via JSON.
*   **Action:** Structure the data as a list of "frames" — one per month — each containing an ordered list of `{product, revenue, category, rank}` objects.

### 3. D3 Bar Chart Skeleton
**Concept:** D3 binds data to SVG elements. Each bar is an SVG `<rect>` whose width is proportional to revenue.
*   **Action:** The Python script writes an HTML file containing D3 code that creates an SVG, binds the first frame of data, and draws horizontal bars.

### 4. Animation with Transitions
**Concept:** D3's `.transition()` method smoothly interpolates between states (position, width, color) over a specified duration.
*   **Action:** A `setInterval` loop advances through frames. On each tick, D3 re-binds the new frame's data and transitions bars to their new positions and widths.

### 5. Interactivity
**Concept:** HTML buttons can control the animation state.
*   **Action:** Add a Play/Pause button that toggles the interval. Display the current month as a large label that updates with each frame.

## Tips for Coding and Vibe-Coding

1.  **Python generates, browser renders:** Your Python script never runs D3. It writes an HTML file that a browser interprets. Think of Python as the "template engine."
2.  **JSON.dumps is the bridge:** Use `json.dumps(data)` to convert Python lists/dicts into a JavaScript-compatible string embedded in the HTML.
3.  **D3 `key` functions matter:** When D3 rebinds data, it needs to know which bar corresponds to which product. Use `.data(frame, d => d.product)` so bars animate correctly instead of morphing into each other.
4.  **Easing functions:** D3 has built-in easing: `d3.easeCubicInOut`, `d3.easeElastic`, `d3.easeBounce`. Experiment for different visual effects.
5.  **CDN fallback:** If the network is unavailable, the D3 CDN won't load. For offline use, download `d3.v7.min.js` and reference it locally.

## Copilot Master Prompt
*You can use this prompt to generate the solution code:*

> "I have monthly product sales data as a Python dict structured as a list of frames, where each frame has a 'month' key and a 'products' list of {name, revenue, category, rank} objects.
> Write a Python script that:
> 1. Reads a CSV with Date, Product, Category, Revenue columns.
> 2. Aggregates cumulative revenue by product per month and takes top 10 per month.
> 3. Serializes the data as JSON embedded in an HTML file.
> 4. The HTML file uses D3.js v7 (loaded via CDN) to create an animated horizontal bar chart race.
> 5. Bars should transition smoothly between months, reordering and resizing.
> 6. Include a Play/Pause button and a month label.
> 7. Use a color scale mapped to product category."
