# Exercise: Viz 5 - The Executive Scatter (Seaborn Advanced)

## The Goal

The Head of Strategy wants to see the *relationship* between deal size and quantity sold — but broken down by product category and region simultaneously. A simple bar chart won't cut it; she needs a chart where every data point tells a story: its position shows the deal economics, its color shows the category, and its size shows the volume.

**Your Mission:**
Build a publication-quality scatter plot using **Seaborn** that encodes four dimensions of data in a single chart:
1. **X-axis:** Unit Price (how expensive is the product?).
2. **Y-axis:** Revenue (how much money did the deal generate?).
3. **Color (hue):** Product Category — a continuous or categorical color mapping.
4. **Size:** Quantity sold — bigger bubbles = bigger volume.

**Expected Outcome:**
A polished PNG image (`executive_scatter.png`) that looks like it belongs in a Harvard Business Review article. It should include:
- A clear title and axis labels with currency formatting.
- A legend explaining both the color and size encoding.
- A professional theme (no default matplotlib gray).
- Optional: regression trend lines per category using `lmplot`.
