import pandas as pd
import json
import os

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
INPUT_FILE = os.path.join(DATA_DIR, "client_transactions.csv")
OUTPUT_HTML = os.path.join(DATA_DIR, "solutions", "relationship_network.html")

# Limits for visual clarity
MAX_CLIENTS = 15   # Top N clients by revenue
MIN_EDGE_WEIGHT = 2  # Minimum transactions to show an edge



# Ensure solutions directory exists
os.makedirs(os.path.join(DATA_DIR, 'solutions'), exist_ok=True)

def main():
    # -------------------------------------------------------
    # STEP 1: Load data
    # -------------------------------------------------------
    print("Loading data...")
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run 'exercise_setup_data.py' first.")
        return

    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} transactions.\n")

    # -------------------------------------------------------
    # STEP 2: Extract nodes
    # -------------------------------------------------------
    print("Extracting nodes...")

    # Top clients by revenue
    client_rev = df.groupby("Client")["Revenue"].sum().nlargest(MAX_CLIENTS)
    top_clients = set(client_rev.index)

    # Filter to only top clients
    df_filtered = df[df["Client"].isin(top_clients)].copy()

    # All products and departments in the filtered set
    products = df_filtered["Product"].unique()
    departments = df_filtered["Department"].unique()

    # Build nodes list
    nodes = []
    node_ids = {}  # maps entity name -> node index

    # Group 0 = Client, 1 = Product, 2 = Department
    idx = 0
    for client in sorted(top_clients):
        rev = float(client_rev[client])
        nodes.append({
            "id": idx, "label": client, "group": 0,
            "type": "Client", "revenue": round(rev, 0),
        })
        node_ids[("client", client)] = idx
        idx += 1

    product_rev = df_filtered.groupby("Product")["Revenue"].sum()
    for product in sorted(products):
        rev = float(product_rev.get(product, 0))
        nodes.append({
            "id": idx, "label": product, "group": 1,
            "type": "Product", "revenue": round(rev, 0),
        })
        node_ids[("product", product)] = idx
        idx += 1

    dept_rev = df_filtered.groupby("Department")["Revenue"].sum()
    for dept in sorted(departments):
        rev = float(dept_rev.get(dept, 0))
        nodes.append({
            "id": idx, "label": dept, "group": 2,
            "type": "Department", "revenue": round(rev, 0),
        })
        node_ids[("department", dept)] = idx
        idx += 1

    print(f"  Nodes: {len(nodes)} (Clients: {len(top_clients)}, "
          f"Products: {len(products)}, Departments: {len(departments)})")

    # -------------------------------------------------------
    # STEP 3: Extract edges
    # -------------------------------------------------------
    print("Extracting edges...")

    links = []
    link_set = {}  # (source, target) -> weight

    for _, row in df_filtered.iterrows():
        client_id = node_ids[("client", row["Client"])]
        product_id = node_ids[("product", row["Product"])]
        dept_id = node_ids[("department", row["Department"])]

        # Client <-> Product
        key_cp = (min(client_id, product_id), max(client_id, product_id))
        link_set[key_cp] = link_set.get(key_cp, 0) + 1

        # Department <-> Product
        key_dp = (min(dept_id, product_id), max(dept_id, product_id))
        link_set[key_dp] = link_set.get(key_dp, 0) + 1

    # Filter by minimum weight and build links
    for (source, target), weight in link_set.items():
        if weight >= MIN_EDGE_WEIGHT:
            links.append({
                "source": source,
                "target": target,
                "weight": weight,
            })

    print(f"  Edges: {len(links)} (min weight: {MIN_EDGE_WEIGHT})")

    # -------------------------------------------------------
    # STEP 4: Generate HTML with D3.js
    # -------------------------------------------------------
    print("\nGenerating HTML with D3.js force graph...")

    graph_json = json.dumps({"nodes": nodes, "links": links})

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Business Relationship Network</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0a0a1a;
            color: #e0e0e0;
            overflow: hidden;
        }}
        .header {{
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 100;
            background: rgba(10, 10, 26, 0.9);
            padding: 12px 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #222;
        }}
        .header h1 {{
            font-size: 1.3em;
            color: #00d4ff;
        }}
        .legend {{
            display: flex;
            gap: 20px;
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
            border-radius: 50%;
        }}
        svg {{
            display: block;
        }}
        .tooltip {{
            position: absolute;
            background: rgba(20, 20, 40, 0.95);
            border: 1px solid #00d4ff;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 13px;
            color: #e0e0e0;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
            max-width: 220px;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.2);
        }}
        .tooltip .tt-label {{
            font-size: 15px;
            font-weight: bold;
            color: #fff;
            margin-bottom: 6px;
        }}
        .tooltip .tt-type {{
            color: #00d4ff;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }}
        .footer {{
            position: fixed;
            bottom: 8px;
            left: 0; right: 0;
            text-align: center;
            color: #444;
            font-size: 0.75em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Business Relationship Network</h1>
        <div class="legend">
            <div class="legend-item">
                <div class="legend-swatch" style="background: #ff6b6b;"></div>
                Clients
            </div>
            <div class="legend-item">
                <div class="legend-swatch" style="background: #4ecdc4;"></div>
                Products
            </div>
            <div class="legend-item">
                <div class="legend-swatch" style="background: #ffe66d;"></div>
                Departments
            </div>
        </div>
    </div>
    <div class="tooltip" id="tooltip"></div>
    <div class="footer">Drag nodes to explore &bull; Scroll to zoom &bull; Generated with Python &amp; D3.js</div>

    <script>
        const graph = {graph_json};

        const width = window.innerWidth;
        const height = window.innerHeight;

        // Color by group
        const groupColors = ["#ff6b6b", "#4ecdc4", "#ffe66d"];
        const groupGlow = ["rgba(255,107,107,0.4)", "rgba(78,205,196,0.4)", "rgba(255,230,109,0.4)"];

        // Scale node radius by revenue
        const maxRevenue = d3.max(graph.nodes, d => d.revenue) || 1;
        const radiusScale = d => Math.max(6, Math.sqrt(d.revenue / maxRevenue) * 35);

        // Scale edge width by weight
        const maxWeight = d3.max(graph.links, d => d.weight) || 1;
        const edgeWidth = d => Math.max(0.5, (d.weight / maxWeight) * 4);

        // SVG
        const svg = d3.select("body")
            .append("svg")
            .attr("width", width)
            .attr("height", height);

        // Zoom
        const g = svg.append("g");
        svg.call(d3.zoom()
            .scaleExtent([0.3, 5])
            .on("zoom", (event) => g.attr("transform", event.transform))
        );

        // Glow filter
        const defs = svg.append("defs");
        const filter = defs.append("filter").attr("id", "glow");
        filter.append("feGaussianBlur").attr("stdDeviation", 4).attr("result", "blur");
        const merge = filter.append("feMerge");
        merge.append("feMergeNode").attr("in", "blur");
        merge.append("feMergeNode").attr("in", "SourceGraphic");

        // Force simulation
        const simulation = d3.forceSimulation(graph.nodes)
            .force("link", d3.forceLink(graph.links)
                .id(d => d.id)
                .distance(100)
                .strength(d => Math.min(0.5, d.weight / maxWeight))
            )
            .force("charge", d3.forceManyBody().strength(-350))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(d => radiusScale(d) + 5));

        // Links
        const link = g.append("g")
            .selectAll("line")
            .data(graph.links)
            .join("line")
            .attr("stroke", "#334")
            .attr("stroke-opacity", 0.5)
            .attr("stroke-width", d => edgeWidth(d));

        // Nodes
        const node = g.append("g")
            .selectAll("circle")
            .data(graph.nodes)
            .join("circle")
            .attr("r", d => radiusScale(d))
            .attr("fill", d => groupColors[d.group])
            .attr("stroke", d => groupColors[d.group])
            .attr("stroke-width", 2)
            .attr("opacity", 0.85)
            .style("filter", "url(#glow)")
            .call(d3.drag()
                .on("start", dragStarted)
                .on("drag", dragged)
                .on("end", dragEnded)
            );

        // Labels (only for larger nodes)
        const label = g.append("g")
            .selectAll("text")
            .data(graph.nodes)
            .join("text")
            .text(d => radiusScale(d) > 12 ? d.label : "")
            .attr("font-size", d => Math.max(9, radiusScale(d) * 0.45) + "px")
            .attr("fill", "#e0e0e0")
            .attr("text-anchor", "middle")
            .attr("dy", d => radiusScale(d) + 14)
            .attr("pointer-events", "none")
            .style("text-shadow", "0 0 4px #000");

        // Tooltip
        const tooltip = d3.select("#tooltip");

        function formatCurrency(v) {{
            if (v >= 1e6) return "$" + (v / 1e6).toFixed(1) + "M";
            if (v >= 1e3) return "$" + (v / 1e3).toFixed(0) + "K";
            return "$" + v.toFixed(0);
        }}

        node.on("mouseover", (event, d) => {{
            tooltip.style("opacity", 1)
                .html(`<div class="tt-type">${{d.type}}</div>
                       <div class="tt-label">${{d.label}}</div>
                       <div>Revenue: ${{formatCurrency(d.revenue)}}</div>
                       <div>Connections: ${{graph.links.filter(l =>
                           (l.source.id || l.source) === d.id ||
                           (l.target.id || l.target) === d.id
                       ).length}}</div>`);

            // Highlight connected links
            link.attr("stroke-opacity", l =>
                (l.source.id === d.id || l.target.id === d.id) ? 1 : 0.1
            ).attr("stroke", l =>
                (l.source.id === d.id || l.target.id === d.id) ? groupColors[d.group] : "#334"
            );

            // Dim unconnected nodes
            const connectedIds = new Set();
            connectedIds.add(d.id);
            graph.links.forEach(l => {{
                if ((l.source.id || l.source) === d.id) connectedIds.add(l.target.id || l.target);
                if ((l.target.id || l.target) === d.id) connectedIds.add(l.source.id || l.source);
            }});
            node.attr("opacity", n => connectedIds.has(n.id) ? 1 : 0.15);
            label.attr("opacity", n => connectedIds.has(n.id) ? 1 : 0.1);
        }})
        .on("mousemove", (event) => {{
            tooltip.style("left", (event.pageX + 15) + "px")
                   .style("top", (event.pageY - 10) + "px");
        }})
        .on("mouseout", () => {{
            tooltip.style("opacity", 0);
            link.attr("stroke-opacity", 0.5).attr("stroke", "#334");
            node.attr("opacity", 0.85);
            label.attr("opacity", 1);
        }});

        // Simulation tick
        simulation.on("tick", () => {{
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);

            label
                .attr("x", d => d.x)
                .attr("y", d => d.y);
        }});

        // Drag functions
        function dragStarted(event) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }}

        function dragged(event) {{
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }}

        function dragEnded(event) {{
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }}
    </script>
</body>
</html>"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\nSUCCESS: Network graph saved to {OUTPUT_HTML}")
    print("Open in any browser to explore the interactive network!")
    print(f"  Nodes: {len(nodes)}")
    print(f"  Edges: {len(links)}")


if __name__ == "__main__":
    main()
