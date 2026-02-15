import pandas as pd
import random
import os

# --- DOCUMENTATION ---
"""
This script generates a transactional dataset linking clients, products,
and departments — designed for extracting a network graph. The data has
enough variety to create interesting clusters when visualized as a
force-directed network.
"""

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
FILE_NAME = "client_transactions.csv"
NUM_ROWS = 800

# --- REFERENCE DATA ---
DEPARTMENTS = ["Sales", "Enterprise", "Partnerships", "Government", "Retail"]

CLIENTS = [
    "Acme Corp", "Globex Inc", "Initech", "Umbrella Ltd", "Stark Industries",
    "Wayne Enterprises", "Cyberdyne Systems", "Soylent Corp", "Oscorp",
    "LexCorp", "Wonka Industries", "Aperture Science", "Tyrell Corp",
    "Massive Dynamic", "Hooli", "Pied Piper", "Dunder Mifflin",
    "Sterling Cooper", "InGen", "Weyland-Yutani",
]

PRODUCTS = [
    "Cloud Platform", "Security Suite", "Analytics Dashboard",
    "CRM Enterprise", "DevOps Pipeline", "Mobile SDK",
    "Data Warehouse", "API Gateway", "Compliance Module",
    "Training Platform", "Support Premium", "Migration Toolkit",
]

# Define affinities: some clients prefer certain products / departments
CLIENT_DEPT_AFFINITY = {
    "Acme Corp": ["Enterprise", "Sales"],
    "Globex Inc": ["Partnerships", "Enterprise"],
    "Stark Industries": ["Enterprise", "Government"],
    "Wayne Enterprises": ["Government", "Enterprise"],
    "Hooli": ["Sales", "Retail"],
    "Pied Piper": ["Partnerships", "Sales"],
    "Dunder Mifflin": ["Retail", "Sales"],
}

CLIENT_PRODUCT_AFFINITY = {
    "Acme Corp": ["Cloud Platform", "Security Suite", "CRM Enterprise"],
    "Globex Inc": ["Analytics Dashboard", "Data Warehouse", "API Gateway"],
    "Stark Industries": ["Security Suite", "Compliance Module", "DevOps Pipeline"],
    "Wayne Enterprises": ["Cloud Platform", "Compliance Module", "Support Premium"],
    "Hooli": ["Cloud Platform", "Mobile SDK", "Training Platform"],
    "Pied Piper": ["DevOps Pipeline", "API Gateway", "Cloud Platform"],
}


def create_dataset():
    """Generate transactional data with client-product-department relationships."""
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Generating {NUM_ROWS} client transactions...\n")

    records = []

    for i in range(1, NUM_ROWS + 1):
        client = random.choice(CLIENTS)

        # Use affinity if available, otherwise random
        if client in CLIENT_DEPT_AFFINITY and random.random() < 0.7:
            department = random.choice(CLIENT_DEPT_AFFINITY[client])
        else:
            department = random.choice(DEPARTMENTS)

        if client in CLIENT_PRODUCT_AFFINITY and random.random() < 0.7:
            product = random.choice(CLIENT_PRODUCT_AFFINITY[client])
        else:
            product = random.choice(PRODUCTS)

        quantity = random.randint(1, 25)
        unit_price = round(random.uniform(500, 15000), 2)
        revenue = round(quantity * unit_price, 2)

        records.append({
            "Transaction_ID": f"NET-{80000 + i}",
            "Client": client,
            "Department": department,
            "Product": product,
            "Quantity": quantity,
            "Unit_Price": unit_price,
            "Revenue": revenue,
        })

    df = pd.DataFrame(records)

    output_path = os.path.join(DATA_DIR, FILE_NAME)
    df.to_csv(output_path, index=False)

    print(f"SUCCESS: Created {output_path}")
    print(f"  Rows: {len(df)}")
    print(f"  Unique Clients: {df['Client'].nunique()}")
    print(f"  Unique Products: {df['Product'].nunique()}")
    print(f"  Unique Departments: {df['Department'].nunique()}")

    print(f"\nTop 5 clients by revenue:")
    top = df.groupby("Client")["Revenue"].sum().sort_values(ascending=False).head()
    for client, rev in top.items():
        print(f"  {client}: ${rev:,.0f}")

    print(f"\nClient-Product pairs: {df.groupby(['Client', 'Product']).ngroups}")
    print(f"Department-Product pairs: {df.groupby(['Department', 'Product']).ngroups}")
    print(f"\nReady to build the network graph!")


if __name__ == "__main__":
    create_dataset()
