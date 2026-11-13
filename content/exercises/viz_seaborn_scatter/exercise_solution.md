# Exercise Card: Viz 5 - The Executive Scatter (Seaborn Advanced)

## Title & Problem Statement
**The Executive Scatter: Multi-Dimensional Data Storytelling with Seaborn**

Bar charts show one dimension. Line charts show trends. But scatter plots can encode *four or more* dimensions simultaneously — position (x, y), color (hue), and size. This is the visualization that separates "reporting" from "analysis." In this exercise, you will use Seaborn's `scatterplot()` with continuous hues and sizes — inspired by the [Seaborn gallery example](https://seaborn.pydata.org/examples/scatterplot_sizes.html) — to create a chart that tells a rich, multi-layered story about your sales data. You will also explore `lmplot()` to overlay regression lines, revealing hidden trends within each category.

## Difficulty & Estimated Time
*   **Difficulty:** Intermediate (Seaborn Deep Dive)
*   **Estimated Time:** 30-40 Minutes

## Required Libraries
*   `pandas`: Data loading and preparation.
*   `seaborn`: The star — `scatterplot()`, `lmplot()`, `set_theme()`, and palettes.
*   `matplotlib.pyplot`: Fine-tuning axes, titles, formatters, and saving.
*   `numpy`: Light usage for log scaling or data transforms if needed.

## Didactic Step-by-Step

### 1. Data Preparation
**Concept:** Scatter plots work best with continuous numerical variables and a categorical grouping variable.
*   **Action:** Load the sales CSV. Ensure `Unit_Price`, `Revenue`, and `Quantity` are numeric. The `Category` column will drive color encoding.

### 2. Basic Scatter with Hue and Size
**Concept:** Seaborn's `scatterplot()` maps aesthetics (color, size) to data columns automatically.
*   **Action:** Call `sns.scatterplot(data=df, x='Unit_Price', y='Revenue', hue='Category', size='Quantity')`. This single line encodes four variables.

### 3. Theme and Palette Selection
**Concept:** Seaborn themes transform the entire look with one line.
*   **Action:** Use `sns.set_theme(style='whitegrid', context='talk')` for a clean, presentation-ready look. Use `palette='deep'` or `'husl'` for vibrant category colors.

### 4. Axis Formatting
**Concept:** Raw numbers on axes confuse executives. Currency and comma formatting make charts readable.
*   **Action:** Use `matplotlib.ticker.FuncFormatter` to add `$` prefixes and comma separators to both axes.

### 5. Regression Lines (Tier 2)
**Concept:** `lmplot()` overlays linear regression fits per category, revealing if higher-priced items generate proportionally more revenue.
*   **Action:** Use `sns.lmplot(data=df, x='Unit_Price', y='Revenue', hue='Category', scatter_kws={'alpha': 0.5})` to see the trend per group.

### 6. Multi-Panel Scatter (Tier 2)
**Concept:** `FacetGrid` splits the scatter into separate panels per region.
*   **Action:** Use `sns.relplot(data=df, x='Unit_Price', y='Revenue', hue='Category', size='Quantity', col='Region', col_wrap=2)` for a faceted view.

## Tips for Coding and Vibe-Coding

1.  **`context` parameter is underused:** `sns.set_theme(context='talk')` makes fonts larger — perfect for presentations. Try `'poster'` for even bigger text.
2.  **Alpha is essential:** With 1000+ points, set `alpha=0.6` to handle overplotting. Without it, the chart is an unreadable blob.
3.  **Size range:** By default, Seaborn picks small size ranges. Use `sizes=(20, 400)` to make the size encoding actually visible.
4.  **`relplot` > `scatterplot`:** For faceted multi-panel charts, use `sns.relplot(kind='scatter')` instead of `sns.scatterplot()`. It returns a FacetGrid which is easier to customize.
5.  **Legend outside:** If the legend overlaps data, use `plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')` to push it outside the chart area.

## Copilot Master Prompt
*You can use this prompt to generate the solution code:*

> "I have a pandas DataFrame with columns: Category, Product, Region, Unit_Price, Revenue, Quantity, Satisfaction_Score.
> Using Seaborn, create:
> 1. A scatter plot with x=Unit_Price, y=Revenue, hue=Category, size=Quantity. Use the 'deep' palette, alpha=0.6, sizes=(20, 400). Apply the 'whitegrid' theme with 'talk' context.
> 2. Add currency formatting ($) to both axes. Add a bold title.
> 3. Save as 'executive_scatter.png' at 150 DPI.
> 4. Also create an lmplot showing regression lines per Category.
> 5. Also create a relplot with col='Region' and col_wrap=2 showing the same scatter faceted by region."
