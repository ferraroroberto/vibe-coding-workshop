import pandas as pd
import json
import os

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
INPUT_FILE = os.path.join(DATA_DIR, "monthly_product_sales.csv")
OUTPUT_HTML = os.path.join(DATA_DIR, "bar_chart_race.html")
TOP_N = 10  # Show top N products per frame


def main():
    # -------------------------------------------------------
    # STEP 1: Load and aggregate data
    # -------------------------------------------------------
    print("Loading data...")
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run 'exercise_setup_data.py' first.")
        return

    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} rows.\n")

    # -------------------------------------------------------
    # STEP 2: Compute cumulative revenue by product per month
    # -------------------------------------------------------
    print("Computing cumulative rankings...")

    # Monthly revenue per product
    monthly = (
        df.groupby(["Month", "Product", "Category"])["Revenue"]
        .sum()
        .reset_index()
    )

    # Sort by month to compute cumulative
    monthly = monthly.sort_values("Month")

    # Cumulative revenue per product over time
    monthly["Cumulative_Revenue"] = (
        monthly.groupby("Product")["Revenue"].cumsum()
    )

    # -------------------------------------------------------
    # STEP 3: Build frames (one per month, top N)
    # -------------------------------------------------------
    print("Building animation frames...")

    months = sorted(monthly["Month"].unique())
    frames = []

    # Build a category color map
    categories = sorted(monthly["Category"].unique())
    # D3 schemeTableau10 color indices
    cat_colors = {
        cat: i for i, cat in enumerate(categories)
    }

    for month in months:
        month_data = monthly[monthly["Month"] == month].copy()

        # Rank by cumulative revenue within this month
        month_data = month_data.sort_values("Cumulative_Revenue", ascending=False)
        month_data = month_data.head(TOP_N).reset_index(drop=True)
        month_data["rank"] = range(1, len(month_data) + 1)

        products = []
        for _, row in month_data.iterrows():
            products.append({
                "name": row["Product"],
                "value": round(row["Cumulative_Revenue"], 0),
                "category": row["Category"],
                "colorIndex": cat_colors[row["Category"]],
                "rank": int(row["rank"]),
            })

        frames.append({
            "month": month,
            "products": products,
        })

    # Category list for legend
    category_list = [{"name": cat, "colorIndex": idx} for cat, idx in cat_colors.items()]

    print(f"  Frames: {len(frames)}")
    print(f"  Categories: {len(category_list)}")

    # -------------------------------------------------------
    # STEP 4: Generate the HTML with embedded D3.js
    # -------------------------------------------------------
    print("Generating HTML with D3.js...")

    frames_json = json.dumps(frames)
    categories_json = json.dumps(category_list)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bar Chart Race — Product Revenue 2024</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f0f1a;
            color: #e0e0e0;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 30px 20px;
        }}
        h1 {{
            font-size: 1.8em;
            color: #00d4ff;
            margin-bottom: 5px;
        }}
        .subtitle {{
            color: #888;
            font-size: 0.95em;
            margin-bottom: 20px;
        }}
        .controls {{
            display: flex;
            gap: 15px;
            align-items: center;
            margin-bottom: 20px;
        }}
        button {{
            background: #00d4ff;
            color: #0f0f1a;
            border: none;
            padding: 10px 28px;
            border-radius: 6px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.2s;
        }}
        button:hover {{ background: #00b8e6; }}
        .month-label {{
            font-size: 1.5em;
            font-weight: bold;
            color: #fff;
            min-width: 120px;
            text-align: center;
        }}
        .speed-control {{ color: #aaa; font-size: 0.9em; }}
        .speed-control select {{
            background: #1a1a2e;
            color: #e0e0e0;
            border: 1px solid #333;
            padding: 5px;
            border-radius: 4px;
        }}
        #chart {{
            background: #1a1a2e;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }}
        .bar-label {{
            fill: #e0e0e0;
            font-size: 13px;
            font-weight: 600;
        }}
        .bar-value {{
            fill: #aaa;
            font-size: 12px;
        }}
        .legend {{
            display: flex;
            gap: 20px;
            margin-top: 15px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.85em;
            color: #bbb;
        }}
        .legend-swatch {{
            width: 14px;
            height: 14px;
            border-radius: 3px;
        }}
        .footer {{
            margin-top: 20px;
            color: #555;
            font-size: 0.8em;
        }}
    </style>
</head>
<body>
    <h1>Product Revenue Bar Chart Race</h1>
    <p class="subtitle">Cumulative Revenue Rankings — 2024</p>

    <div class="controls">
        <button id="playBtn">&#9654; Play</button>
        <div class="month-label" id="monthLabel">—</div>
        <div class="speed-control">
            Speed:
            <select id="speedSelect">
                <option value="2000">Slow</option>
                <option value="1200" selected>Normal</option>
                <option value="600">Fast</option>
            </select>
        </div>
    </div>

    <div id="chart"></div>
    <div class="legend" id="legend"></div>
    <p class="footer">Generated with Python &amp; D3.js — ChangeMakers Workshop</p>

    <script>
        // Data injected from Python
        const frames = {frames_json};
        const categories = {categories_json};

        // Chart dimensions
        const margin = {{ top: 10, right: 120, bottom: 10, left: 160 }};
        const width = 800;
        const height = 450;
        const barHeight = 36;
        const barPadding = 6;
        const n = {TOP_N};

        // D3 color scale (Tableau10)
        const color = d3.scaleOrdinal(d3.schemeTableau10);

        // SVG
        const svg = d3.select("#chart")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

        // Scales
        const x = d3.scaleLinear().range([0, width]);
        const y = d3.scaleBand()
            .range([0, height])
            .padding(0.15);

        // Animation state
        let currentFrame = 0;
        let playing = false;
        let intervalId = null;

        function getSpeed() {{
            return parseInt(document.getElementById("speedSelect").value);
        }}

        function formatCurrency(val) {{
            if (val >= 1e6) return "$" + (val / 1e6).toFixed(1) + "M";
            if (val >= 1e3) return "$" + (val / 1e3).toFixed(0) + "K";
            return "$" + val.toFixed(0);
        }}

        function renderFrame(frameIdx, duration) {{
            const frame = frames[frameIdx];
            const data = frame.products;

            document.getElementById("monthLabel").textContent = frame.month;

            // Update scales
            x.domain([0, d3.max(data, d => d.value) * 1.15]);
            y.domain(data.map(d => d.name));

            const t = svg.transition().duration(duration).ease(d3.easeCubicInOut);

            // --- BARS ---
            const bars = svg.selectAll(".bar")
                .data(data, d => d.name);

            // Enter
            bars.enter()
                .append("rect")
                .attr("class", "bar")
                .attr("y", d => y(d.name))
                .attr("height", y.bandwidth())
                .attr("x", 0)
                .attr("width", 0)
                .attr("rx", 4)
                .attr("fill", d => color(d.colorIndex))
                .attr("opacity", 0.85)
                .transition(t)
                .attr("width", d => x(d.value))
                .attr("y", d => y(d.name));

            // Update
            bars.transition(t)
                .attr("y", d => y(d.name))
                .attr("width", d => x(d.value))
                .attr("height", y.bandwidth());

            // Exit
            bars.exit()
                .transition(t)
                .attr("width", 0)
                .attr("opacity", 0)
                .remove();

            // --- LABELS (product names) ---
            const labels = svg.selectAll(".bar-label")
                .data(data, d => d.name);

            labels.enter()
                .append("text")
                .attr("class", "bar-label")
                .attr("x", -8)
                .attr("y", d => y(d.name) + y.bandwidth() / 2)
                .attr("dy", "0.35em")
                .attr("text-anchor", "end")
                .text(d => d.name)
                .transition(t)
                .attr("y", d => y(d.name) + y.bandwidth() / 2);

            labels.transition(t)
                .attr("y", d => y(d.name) + y.bandwidth() / 2)
                .text(d => d.name);

            labels.exit().transition(t).attr("opacity", 0).remove();

            // --- VALUES ---
            const values = svg.selectAll(".bar-value")
                .data(data, d => d.name);

            values.enter()
                .append("text")
                .attr("class", "bar-value")
                .attr("x", d => x(d.value) + 8)
                .attr("y", d => y(d.name) + y.bandwidth() / 2)
                .attr("dy", "0.35em")
                .text(d => formatCurrency(d.value))
                .transition(t)
                .attr("x", d => x(d.value) + 8)
                .attr("y", d => y(d.name) + y.bandwidth() / 2);

            values.transition(t)
                .attr("x", d => x(d.value) + 8)
                .attr("y", d => y(d.name) + y.bandwidth() / 2)
                .tween("text", function(d) {{
                    const node = this;
                    const prev = parseFloat(node.textContent.replace(/[$MK,]/g, "")) || 0;
                    const scale = node.textContent.includes("M") ? 1e6 :
                                  node.textContent.includes("K") ? 1e3 : 1;
                    const i = d3.interpolateNumber(prev * scale, d.value);
                    return function(t) {{
                        node.textContent = formatCurrency(i(t));
                    }};
                }});

            values.exit().transition(t).attr("opacity", 0).remove();
        }}

        function step() {{
            if (currentFrame >= frames.length) {{
                pause();
                currentFrame = 0;
                return;
            }}
            const duration = currentFrame === 0 ? 0 : getSpeed() * 0.8;
            renderFrame(currentFrame, duration);
            currentFrame++;
        }}

        function play() {{
            if (playing) return;
            playing = true;
            document.getElementById("playBtn").innerHTML = "&#9646;&#9646; Pause";
            step();
            intervalId = setInterval(step, getSpeed());
        }}

        function pause() {{
            playing = false;
            document.getElementById("playBtn").innerHTML = "&#9654; Play";
            clearInterval(intervalId);
        }}

        // Button handler
        document.getElementById("playBtn").addEventListener("click", () => {{
            if (playing) pause(); else play();
        }});

        // Speed change handler
        document.getElementById("speedSelect").addEventListener("change", () => {{
            if (playing) {{
                clearInterval(intervalId);
                intervalId = setInterval(step, getSpeed());
            }}
        }});

        // Build legend
        const legendDiv = document.getElementById("legend");
        categories.forEach(cat => {{
            const item = document.createElement("div");
            item.className = "legend-item";
            item.innerHTML = `<div class="legend-swatch" style="background: ${{color(cat.colorIndex)}}"></div>${{cat.name}}`;
            legendDiv.appendChild(item);
        }});

        // Render first frame immediately
        renderFrame(0, 0);
        document.getElementById("monthLabel").textContent = frames[0].month;
    </script>
</body>
</html>"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\nSUCCESS: Bar chart race saved to {OUTPUT_HTML}")
    print("Open in any browser and click Play to watch the animation!")
    print(f"  Frames: {len(frames)}")
    print(f"  Products tracked: {len(PRODUCTS)}")
    print(f"  Top N shown per frame: {TOP_N}")


# Unique products for summary
PRODUCTS = set()


def collect_products(frames_data):
    for frame in frames_data:
        for p in frame["products"]:
            PRODUCTS.add(p["name"])


if __name__ == "__main__":
    main()
