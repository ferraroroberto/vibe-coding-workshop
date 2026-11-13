# Exercise Card: Viz 8 - The Relationship Network (D3.js Force Graph)

## Title & Problem Statement
**The Relationship Network: Visualizing Business Connections with D3.js Force Graphs**

Not all data is tabular. Relationships between entities — customers, products, departments, suppliers — form networks. Force-directed graphs are one of the most visually striking and analytically powerful ways to explore these connections. In this exercise, you use Python to extract relationships from transactional data and then generate a D3.js force simulation that reveals clusters, central nodes (hubs), and isolated entities. The physics simulation makes the graph self-organize: tightly connected groups cluster together, while loosely connected outliers drift to the edges.

## Difficulty & Estimated Time
*   **Difficulty:** Intermediate-Advanced (Network Visualization with D3.js)
*   **Estimated Time:** 35-45 Minutes

## Required Libraries
*   `pandas`: Data aggregation to extract nodes and edges from transaction data.
*   `json`: Serializing the graph data structure for embedding in HTML/JavaScript.
*   No D3 installation needed — D3.js is loaded via CDN.

## Didactic Step-by-Step

### 1. Data Preparation — Extracting the Graph
**Concept:** A network graph has **nodes** (entities) and **edges** (relationships). We derive both from transactional data.
*   **Action:** From a sales CSV, extract unique clients, products, and departments as nodes. Create edges where a client purchased a product, or a department sold a product.

### 2. Node and Edge Attributes
**Concept:** Nodes have properties (type, size, label) and edges have properties (weight/strength).
*   **Action:** Set node size = total revenue. Set edge weight = number of transactions between the two entities. Assign a `group` field for coloring by entity type.

### 3. JSON Graph Format
**Concept:** D3 force graphs expect `{nodes: [...], links: [...]}` JSON.
*   **Action:** Build the structure in Python and embed via `json.dumps()`.

### 4. D3 Force Simulation
**Concept:** D3's `forceSimulation` applies physics forces — charge repulsion (nodes push apart), link attraction (connected nodes pull together), and centering (gravity toward center).
*   **Action:** Configure `d3.forceSimulation(nodes)` with `.force('link')`, `.force('charge')`, `.force('center')`. On each tick, update node and link SVG positions.

### 5. Interactivity
**Concept:** Drag, hover, and zoom make the graph explorable.
*   **Action:** Add `d3.drag()` behavior to nodes. Add `mouseover` events for tooltips. Add `d3.zoom()` to the SVG container.

## Tips for Coding and Vibe-Coding

1.  **Charge strength controls spacing:** `d3.forceManyBody().strength(-300)` pushes nodes apart. More negative = more spread. Too little and nodes overlap.
2.  **Link distance controls edge length:** `d3.forceLink().distance(80)` sets the ideal edge length. Shorter = tighter clusters.
3.  **Drag = debugging:** If your graph looks like a mess, drag nodes around to see if clusters exist underneath the tangle.
4.  **Node size scaling:** Don't use raw revenue. Use `Math.sqrt(revenue / maxRevenue) * 30` for visual balance.
5.  **Tooltips with `<foreignObject>`:** For rich tooltips, you can use HTML inside SVG via `<foreignObject>`, or position an absolutely-placed `<div>` based on mouse coordinates.

## Copilot Master Prompt
*You can use this prompt to generate the solution code:*

> "I have a JSON object with 'nodes' (each has id, label, group, revenue) and 'links' (each has source, target, weight).
> Write a Python script that:
> 1. Reads a CSV with Client, Product, Department, Revenue columns.
> 2. Extracts unique nodes (clients, products, departments) and edges (client-product, department-product).
> 3. Serializes as JSON embedded in an HTML file with D3.js v7.
> 4. The HTML creates a force-directed graph with: node color by group, node size by revenue, edge thickness by weight.
> 5. Support drag on nodes, zoom/pan on the SVG, and tooltips on hover.
> 6. Use a dark theme with glowing node effects."
