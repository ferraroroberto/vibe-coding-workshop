import pandas as pd
import numpy as np
import random
import os

# --- DOCUMENTATION ---
"""
This script generates a synthetic employee performance dataset designed for
statistical visualizations: correlation heatmaps, violin plots, pair plots,
and box plots. Variables are intentionally correlated to make the charts
reveal meaningful patterns (e.g., experience correlates with revenue).
"""

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
FILE_NAME = "employee_performance.csv"
NUM_ROWS = 400

# --- REFERENCE DATA ---
DEPARTMENTS = ["Sales", "Marketing", "Engineering", "Operations", "Finance"]
SENIORITY_LEVELS = ["Junior", "Mid-Level", "Senior", "Lead", "Director"]
GENDERS = ["Male", "Female"]


def create_dataset():
    """Generate an employee performance dataset with correlated variables."""
    os.makedirs(DATA_DIR, exist_ok=True)
    np.random.seed(42)
    random.seed(42)
    print(f"Generating {NUM_ROWS} employee records...\n")

    records = []

    for i in range(1, NUM_ROWS + 1):
        department = random.choice(DEPARTMENTS)
        gender = random.choice(GENDERS)

        # Seniority weighted by a distribution (more juniors/mids)
        seniority = random.choices(
            SENIORITY_LEVELS,
            weights=[0.25, 0.30, 0.25, 0.12, 0.08],
            k=1
        )[0]

        # Years of experience correlated with seniority
        seniority_base = {
            "Junior": 1, "Mid-Level": 3, "Senior": 6, "Lead": 9, "Director": 12
        }
        years_experience = max(0, round(
            seniority_base[seniority] + np.random.normal(0, 1.5), 1
        ))

        # Satisfaction: department-dependent with noise
        dept_satisfaction = {
            "Sales": 6.5, "Marketing": 7.0, "Engineering": 7.5,
            "Operations": 6.0, "Finance": 6.8
        }
        satisfaction = round(np.clip(
            np.random.normal(dept_satisfaction[department], 1.3), 1.0, 10.0
        ), 1)

        # Revenue: correlated with experience and seniority
        base_revenue = seniority_base[seniority] * 8000
        revenue = max(0, round(
            base_revenue + years_experience * 3000
            + np.random.normal(0, 15000)
            + (satisfaction - 5) * 2000,
            2
        ))

        # Deals closed: correlated with revenue (roughly)
        deals_closed = max(0, int(
            revenue / 5000 + np.random.normal(0, 3)
        ))

        # Training hours: inversely related to seniority (juniors train more)
        training_base = {
            "Junior": 40, "Mid-Level": 30, "Senior": 20, "Lead": 15, "Director": 10
        }
        training_hours = max(0, int(
            training_base[seniority] + np.random.normal(0, 8)
        ))

        records.append({
            "Employee_ID": f"EMP-{7000 + i}",
            "Department": department,
            "Gender": gender,
            "Seniority": seniority,
            "Years_Experience": years_experience,
            "Satisfaction_Score": satisfaction,
            "Revenue_Generated": revenue,
            "Deals_Closed": deals_closed,
            "Training_Hours": training_hours,
        })

    df = pd.DataFrame(records)

    # Enforce seniority as an ordered categorical for correct plot ordering
    df["Seniority"] = pd.Categorical(
        df["Seniority"],
        categories=SENIORITY_LEVELS,
        ordered=True
    )

    output_path = os.path.join(DATA_DIR, FILE_NAME)
    df.to_csv(output_path, index=False)

    print(f"SUCCESS: Created {output_path}")
    print(f"  Rows: {len(df)}")
    print(f"  Columns: {list(df.columns)}")
    print(f"\nDepartment distribution:")
    print(df["Department"].value_counts().to_string())
    print(f"\nSeniority distribution:")
    print(df["Seniority"].value_counts().to_string())
    print(f"\nCorrelation preview (Revenue vs Experience): "
          f"{df['Revenue_Generated'].corr(df['Years_Experience']):.3f}")
    print(f"Correlation preview (Revenue vs Satisfaction): "
          f"{df['Revenue_Generated'].corr(df['Satisfaction_Score']):.3f}")
    print(f"\nReady for statistical visualization!")


if __name__ == "__main__":
    create_dataset()
