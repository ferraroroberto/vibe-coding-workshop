import json
import random
import os
from datetime import datetime, timedelta

# --- DOCUMENTATION ---
"""
This script generates dummy JSON files simulating paginated API responses
from a CRM system. It creates:
  - Multiple 'customers_page_*.json' files with nested address objects.
  - Multiple 'orders_page_*.json' files with references to customer IDs.
  - Some intentional messiness: missing phone numbers, inconsistent casing.
"""

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
NUM_CUSTOMERS = 50
NUM_ORDERS = 200
CUSTOMERS_PER_PAGE = 20
ORDERS_PER_PAGE = 50

# --- HELPER DATA ---
FIRST_NAMES = [
    "Alice", "Bob", "Charlie", "Dana", "Eve", "Frank", "Grace", "Hank",
    "Ivy", "Jack", "Karen", "Leo", "Mia", "Nate", "Olivia", "Pete",
    "Quinn", "Rosa", "Sam", "Tina", "Uma", "Victor", "Wendy", "Xander",
    "Yara", "Zane"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Anderson", "Taylor", "Thomas",
    "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White", "Lopez"
]

STREETS = [
    "123 Main St", "456 Oak Ave", "789 Pine Rd", "321 Elm Blvd",
    "654 Maple Dr", "987 Cedar Ln", "111 Birch Way", "222 Walnut Ct",
    "333 Spruce Pl", "444 Willow Ter"
]

CITIES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "Austin"
]

STATES = ["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA", "TX", "TX"]

PRODUCTS = [
    "Enterprise License", "Cloud Storage Plan", "Support Package",
    "Training Bundle", "API Access Tier", "Analytics Module",
    "Security Add-on", "Migration Service", "Consulting Hours",
    "Premium Dashboard"
]

COMPANY_SUFFIXES = ["Inc.", "LLC", "Corp.", "Ltd.", "Group", "Solutions"]


def generate_customers():
    """Generate a list of customer dictionaries with nested address."""
    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        city_idx = random.randint(0, len(CITIES) - 1)

        customer = {
            "customer_id": f"CUST-{1000 + i}",
            "name": f"{first} {last}",
            "email": f"{first.lower()}.{last.lower()}@{random.choice(['company', 'enterprise', 'biz'])}.com",
            "company": f"{last} {random.choice(COMPANY_SUFFIXES)}",
            "address": {
                "street": random.choice(STREETS),
                "city": CITIES[city_idx],
                "state": STATES[city_idx],
                "zip": f"{random.randint(10000, 99999)}"
            },
            "tier": random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
            "active": random.choice([True, True, True, False])  # 75% active
        }

        # Intentional messiness: ~20% have no phone number
        if random.random() > 0.2:
            area = random.randint(200, 999)
            num1 = random.randint(100, 999)
            num2 = random.randint(1000, 9999)
            customer["phone"] = f"({area}) {num1}-{num2}"
        # else: phone key is simply absent

        customers.append(customer)

    return customers


def generate_orders(customer_ids):
    """Generate a list of order dictionaries referencing customer IDs."""
    orders = []
    start_date = datetime(2024, 1, 1)

    for i in range(1, NUM_ORDERS + 1):
        order_date = start_date + timedelta(days=random.randint(0, 364))
        quantity = random.randint(1, 20)
        unit_price = round(random.uniform(50.0, 5000.0), 2)

        order = {
            "order_id": f"ORD-{20000 + i}",
            "customer_id": random.choice(customer_ids),
            "order_date": order_date.strftime("%Y-%m-%d"),
            "product": random.choice(PRODUCTS),
            "quantity": quantity,
            "unit_price": unit_price,
            "amount": round(quantity * unit_price, 2),
            "status": random.choice(["completed", "pending", "cancelled", "refunded"])
        }
        orders.append(order)

    return orders


def paginate_and_save(records, prefix, per_page):
    """Split records into pages and save as JSON files."""
    pages = [records[i:i + per_page] for i in range(0, len(records), per_page)]

    for page_num, page_data in enumerate(pages, start=1):
        filename = f"{prefix}_page_{page_num}.json"
        filepath = os.path.join(DATA_DIR, filename)

        # Wrap in an API-style response envelope
        response = {
            "page": page_num,
            "total_pages": len(pages),
            "count": len(page_data),
            "results": page_data
        }

        with open(filepath, "w") as f:
            json.dump(response, f, indent=2)

        print(f"  Created: {filename} ({len(page_data)} records)")


def create_dataset():
    """Main function to generate all data files."""
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Generating API simulation data in {DATA_DIR}...\n")

    # Generate customers
    print(f"--- Customers ({NUM_CUSTOMERS} total) ---")
    customers = generate_customers()
    customer_ids = [c["customer_id"] for c in customers]
    paginate_and_save(customers, "customers", CUSTOMERS_PER_PAGE)

    # Generate orders
    print(f"\n--- Orders ({NUM_ORDERS} total) ---")
    orders = generate_orders(customer_ids)
    paginate_and_save(orders, "orders", ORDERS_PER_PAGE)

    print(f"\nSUCCESS: Data generation complete!")
    print(f"  - Customer pages: {(NUM_CUSTOMERS + CUSTOMERS_PER_PAGE - 1) // CUSTOMERS_PER_PAGE}")
    print(f"  - Order pages: {(NUM_ORDERS + ORDERS_PER_PAGE - 1) // ORDERS_PER_PAGE}")
    print(f"\nYou can now start the exercise!")


if __name__ == "__main__":
    create_dataset()
