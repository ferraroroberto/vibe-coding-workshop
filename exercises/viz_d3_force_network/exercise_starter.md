# Exercise: Viz 8 - The Relationship Network (D3.js Force Graph)

## The Goal

The VP of Partnerships wants to understand how departments, products, and clients are connected. Who buys what? Which departments share the same top clients? Which products are frequently purchased together? Spreadsheets can't show relationships — you need a **network graph**.

**Your Mission:**
Using Python to prepare the data and generate an HTML file with embedded **D3.js**, build an interactive force-directed network graph that:
1. Shows **nodes** representing departments, products, and top clients.
2. Shows **edges** (links) representing purchase relationships between them.
3. Uses **node color** to distinguish entity types (department, product, client).
4. Uses **node size** proportional to total revenue.
5. Supports **drag interaction** — the user can grab and move nodes to explore clusters.
6. Shows **tooltips** on hover with entity details.

**Expected Outcome:**
A self-contained `relationship_network.html` file that opens in a browser and shows a physics-based network that self-organizes into clusters. You can drag nodes around, hover for details, and zoom in/out. It should reveal hidden patterns like which clients are central to the business or which products always appear together.
