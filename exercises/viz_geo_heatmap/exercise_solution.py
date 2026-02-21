import pandas as pd
import folium
from folium.plugins import HeatMap
import math
import os

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
INPUT_FILE = os.path.join(DATA_DIR, "global_sales_geo.csv")
OUTPUT_HTML = os.path.join(DATA_DIR, "solutions", "sales_heatmap.html")

# Map settings
MAP_CENTER = [20, 0]  # Roughly centered for a world view
MAP_ZOOM = 2
MAP_TILES = "CartoDB dark_matter"  # Dramatic dark theme



# Ensure solutions directory exists
os.makedirs(os.path.join(DATA_DIR, 'solutions'), exist_ok=True)

def main():
    # -------------------------------------------------------
    # STEP 1: Load and aggregate data
    # -------------------------------------------------------
    print("Loading data...")
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run 'exercise_setup_data.py' first.")
        return

    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} rows from {df['City'].nunique()} cities.\n")

    # Aggregate by city for markers
    city_summary = (
        df.groupby(["City", "Country"])
        .agg(
            Latitude=("Latitude", "mean"),
            Longitude=("Longitude", "mean"),
            Total_Revenue=("Revenue", "sum"),
            Order_Count=("Order_ID", "count"),
            Avg_Order_Value=("Revenue", "mean"),
            Top_Product=("Product", lambda x: x.value_counts().index[0]),
        )
        .reset_index()
    )

    city_summary["Total_Revenue"] = city_summary["Total_Revenue"].round(2)
    city_summary["Avg_Order_Value"] = city_summary["Avg_Order_Value"].round(2)

    # Find max revenue for scaling
    max_revenue = city_summary["Total_Revenue"].max()

    print(f"City summary: {len(city_summary)} cities")
    print(city_summary.nlargest(5, "Total_Revenue")[["City", "Total_Revenue", "Order_Count"]].to_string(index=False))

    # -------------------------------------------------------
    # STEP 2: Create the base map
    # -------------------------------------------------------
    print("\nCreating base map...")

    m = folium.Map(
        location=MAP_CENTER,
        zoom_start=MAP_ZOOM,
        tiles=MAP_TILES,
        attr="CartoDB",
    )

    # -------------------------------------------------------
    # STEP 3: Add heatmap layer
    # -------------------------------------------------------
    print("Adding heatmap layer...")

    # Prepare heat data: [lat, lon, weight]
    # Use log scale for weight to prevent one city from dominating
    heat_data = []
    for _, row in city_summary.iterrows():
        weight = math.log1p(row["Total_Revenue"])  # log(1 + x) to handle zeros
        heat_data.append([row["Latitude"], row["Longitude"], weight])

    heatmap_layer = HeatMap(
        heat_data,
        name="Revenue Heatmap",
        min_opacity=0.4,
        max_zoom=10,
        radius=25,
        blur=15,
        gradient={
            0.2: "#0000ff",
            0.4: "#00ffff",
            0.6: "#00ff00",
            0.8: "#ffff00",
            1.0: "#ff0000",
        },
    )
    heatmap_layer.add_to(m)

    # -------------------------------------------------------
    # STEP 4: Add circle markers with popups
    # -------------------------------------------------------
    print("Adding city markers...")

    # Create a feature group for markers (so they can be toggled)
    marker_group = folium.FeatureGroup(name="City Markers")

    for _, row in city_summary.iterrows():
        # Scale radius: square root for visual balance, capped between 5 and 35
        radius = max(5, min(35, math.sqrt(row["Total_Revenue"] / max_revenue) * 50))

        # Color based on revenue tier
        if row["Total_Revenue"] > max_revenue * 0.7:
            color = "#ff4444"  # Red: top tier
        elif row["Total_Revenue"] > max_revenue * 0.4:
            color = "#ffaa00"  # Orange: mid tier
        elif row["Total_Revenue"] > max_revenue * 0.2:
            color = "#44aaff"  # Blue: growing
        else:
            color = "#44ff88"  # Green: emerging

        # Build rich HTML popup
        popup_html = f"""
        <div style="font-family: 'Segoe UI', sans-serif; width: 220px; padding: 5px;">
            <h4 style="margin: 0 0 8px 0; color: #333; border-bottom: 2px solid {color}; padding-bottom: 5px;">
                {row['City']}, {row['Country']}
            </h4>
            <table style="width: 100%; font-size: 12px; color: #555;">
                <tr>
                    <td><b>Total Revenue:</b></td>
                    <td style="text-align: right; color: #222;">${row['Total_Revenue']:,.0f}</td>
                </tr>
                <tr>
                    <td><b>Orders:</b></td>
                    <td style="text-align: right; color: #222;">{row['Order_Count']:,}</td>
                </tr>
                <tr>
                    <td><b>Avg Order:</b></td>
                    <td style="text-align: right; color: #222;">${row['Avg_Order_Value']:,.0f}</td>
                </tr>
                <tr>
                    <td><b>Top Product:</b></td>
                    <td style="text-align: right; color: #222;">{row['Top_Product']}</td>
                </tr>
            </table>
        </div>
        """

        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{row['City']}: ${row['Total_Revenue']:,.0f}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            weight=2,
        ).add_to(marker_group)

    marker_group.add_to(m)

    # -------------------------------------------------------
    # STEP 5: Add title overlay and layer control
    # -------------------------------------------------------
    print("Adding finishing touches...")

    # Title overlay using HTML
    title_html = """
    <div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
                z-index: 1000; background: rgba(0,0,0,0.8); color: #00d4ff;
                padding: 12px 30px; border-radius: 8px; font-family: 'Segoe UI', sans-serif;
                font-size: 18px; font-weight: bold; box-shadow: 0 2px 10px rgba(0,0,0,0.5);
                pointer-events: none;">
        Global Sales Heatmap 2026
    </div>
    """
    m.get_root().html.add_child(folium.Element(title_html))

    # Layer control (toggle heatmap / markers)
    folium.LayerControl(collapsed=False).add_to(m)

    # -------------------------------------------------------
    # STEP 6: Save
    # -------------------------------------------------------
    m.save(OUTPUT_HTML)
    print(f"\nSUCCESS: Heatmap saved to {OUTPUT_HTML}")
    print("Open this file in any browser to explore the interactive map!")
    print(f"  - Cities mapped: {len(city_summary)}")
    print(f"  - Total revenue visualized: ${city_summary['Total_Revenue'].sum():,.0f}")


if __name__ == "__main__":
    main()
