import pandas as pd
import random
import os

# --- DOCUMENTATION ---
"""
This script generates a global sales dataset with geographic coordinates.
Each row represents a sale tied to a specific city with lat/lon coordinates.
This data is designed for creating geographic heatmaps and marker maps.
"""

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
FILE_NAME = "global_sales_geo.csv"
NUM_ROWS = 1500

# --- CITY DATABASE (City, Country, Lat, Lon) ---
CITIES = [
    # North America
    ("New York", "USA", 40.7128, -74.0060),
    ("Los Angeles", "USA", 34.0522, -118.2437),
    ("Chicago", "USA", 41.8781, -87.6298),
    ("Houston", "USA", 29.7604, -95.3698),
    ("Toronto", "Canada", 43.6532, -79.3832),
    ("Mexico City", "Mexico", 19.4326, -99.1332),
    ("San Francisco", "USA", 37.7749, -122.4194),
    ("Miami", "USA", 25.7617, -80.1918),
    ("Seattle", "USA", 47.6062, -122.3321),
    ("Atlanta", "USA", 33.7490, -84.3880),
    # Europe
    ("London", "UK", 51.5074, -0.1278),
    ("Paris", "France", 48.8566, 2.3522),
    ("Berlin", "Germany", 52.5200, 13.4050),
    ("Amsterdam", "Netherlands", 52.3676, 4.9041),
    ("Madrid", "Spain", 40.4168, -3.7038),
    ("Milan", "Italy", 45.4642, 9.1900),
    ("Stockholm", "Sweden", 59.3293, 18.0686),
    ("Zurich", "Switzerland", 47.3769, 8.5417),
    ("Dublin", "Ireland", 53.3498, -6.2603),
    ("Warsaw", "Poland", 52.2297, 21.0122),
    # Asia Pacific
    ("Tokyo", "Japan", 35.6762, 139.6503),
    ("Singapore", "Singapore", 1.3521, 103.8198),
    ("Sydney", "Australia", -33.8688, 151.2093),
    ("Mumbai", "India", 19.0760, 72.8777),
    ("Shanghai", "China", 31.2304, 121.4737),
    ("Seoul", "South Korea", 37.5665, 126.9780),
    ("Hong Kong", "China", 22.3193, 114.1694),
    ("Melbourne", "Australia", -37.8136, 144.9631),
    ("Bangkok", "Thailand", 13.7563, 100.5018),
    ("Jakarta", "Indonesia", -6.2088, 106.8456),
    # Latin America
    ("São Paulo", "Brazil", -23.5505, -46.6333),
    ("Buenos Aires", "Argentina", -34.6037, -58.3816),
    ("Bogotá", "Colombia", 4.7110, -74.0721),
    ("Lima", "Peru", -12.0464, -77.0428),
    ("Santiago", "Chile", -33.4489, -70.6693),
    # Middle East & Africa
    ("Dubai", "UAE", 25.2048, 55.2708),
    ("Tel Aviv", "Israel", 32.0853, 34.7818),
    ("Cape Town", "South Africa", -33.9249, 18.4241),
    ("Nairobi", "Kenya", -1.2921, 36.8219),
    ("Lagos", "Nigeria", 6.5244, 3.3792),
]

# Revenue weights by city (bigger cities get more sales)
CITY_WEIGHTS = {
    "New York": 12, "London": 11, "Tokyo": 10, "San Francisco": 9,
    "Los Angeles": 8, "Paris": 8, "Singapore": 8, "Sydney": 7,
    "Chicago": 7, "Toronto": 7, "Shanghai": 7, "Berlin": 6,
    "Seoul": 6, "Hong Kong": 6, "Mumbai": 5, "São Paulo": 5,
    "Dubai": 5, "Amsterdam": 5, "Seattle": 5, "Miami": 4,
}

PRODUCTS = [
    "Enterprise License", "Cloud Platform", "Security Suite",
    "Analytics Pro", "Support Package", "Training Program",
    "Consulting Service", "DevOps Kit", "Data Warehouse",
    "Mobile SDK", "API Gateway", "Compliance Module",
]


def get_city_weight(city_name):
    """Return a weight for the city (higher = more orders)."""
    return CITY_WEIGHTS.get(city_name, 3)


def create_dataset():
    """Generate the global sales dataset."""
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Generating {NUM_ROWS} rows of global sales data...\n")

    records = []
    city_names = [c[0] for c in CITIES]
    city_weights = [get_city_weight(c[0]) for c in CITIES]
    city_lookup = {c[0]: c for c in CITIES}

    for i in range(1, NUM_ROWS + 1):
        # Pick a city (weighted — bigger markets get more orders)
        city_name = random.choices(city_names, weights=city_weights, k=1)[0]
        city_info = city_lookup[city_name]

        _, country, lat, lon = city_info

        # Add slight coordinate jitter so markers don't stack perfectly
        lat_jitter = lat + random.uniform(-0.05, 0.05)
        lon_jitter = lon + random.uniform(-0.05, 0.05)

        product = random.choice(PRODUCTS)
        quantity = random.randint(1, 20)
        unit_price = round(random.uniform(100, 5000), 2)
        revenue = round(quantity * unit_price, 2)

        records.append({
            "Order_ID": f"GEO-{40000 + i}",
            "City": city_name,
            "Country": country,
            "Latitude": round(lat_jitter, 4),
            "Longitude": round(lon_jitter, 4),
            "Product": product,
            "Quantity": quantity,
            "Unit_Price": unit_price,
            "Revenue": revenue,
        })

    df = pd.DataFrame(records)

    # Save
    output_path = os.path.join(DATA_DIR, FILE_NAME)
    df.to_csv(output_path, index=False)

    print(f"SUCCESS: Created {output_path}")
    print(f"  Rows: {len(df)}")
    print(f"  Unique Cities: {df['City'].nunique()}")
    print(f"\nTop 10 cities by revenue:")
    city_summary = (
        df.groupby(["City", "Country"])["Revenue"]
        .agg(["sum", "count"])
        .rename(columns={"sum": "Total_Revenue", "count": "Orders"})
        .sort_values("Total_Revenue", ascending=False)
    )
    print(city_summary.head(10).to_string())
    print(f"\nYou are ready to create your geographic heatmap!")


if __name__ == "__main__":
    create_dataset()
