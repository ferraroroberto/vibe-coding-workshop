# Simple script to test basic imports and functionality of workshop libraries
# Testing libraries from requirements.txt in root folder
import faker
import duckdb
import matplotlib.pyplot as plt
import openpyxl
import pandas as pd
import pyarrow
import seaborn as sns
import xlsxwriter
import os


def check(msg, success):
	# Green check for success, red cross for failure
	if success:
		print(f"\033[92m✔\033[0m {msg}")
	else:
		print(f"\033[91m✘\033[0m {msg}")

print("Testing imports...\n")


# Faker
try:
	fake = faker.Faker()
	print("Faker imported successfully")
	print("Sample name:", fake.name())
	check("Faker test", True)
except Exception as e:
	check(f"Faker test failed: {e}", False)
print()


# DuckDB
try:
	conn = duckdb.connect()
	result = conn.execute("SELECT 1 as test").fetchone()
	print("DuckDB version:", duckdb.__version__)
	print("DuckDB test query result:", result)
	conn.close()
	check("DuckDB test", True)
except Exception as e:
	check(f"DuckDB test failed: {e}", False)
print()


# Pandas
try:
	print("Pandas version:", pd.__version__)
	df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
	print("DataFrame:\n", df)
	check("Pandas test", True)
except Exception as e:
	check(f"Pandas test failed: {e}", False)
print()


# Matplotlib
try:
	plt.plot([1, 2, 3], [4, 5, 6])
	plt.title("Demo Plot")
	plt.close()
	print("Matplotlib plot created.")
	check("Matplotlib test", True)
except Exception as e:
	check(f"Matplotlib test failed: {e}", False)
print()


# Seaborn
try:
	sns.set()
	print("Seaborn version:", sns.__version__)
	check("Seaborn test", True)
except Exception as e:
	check(f"Seaborn test failed: {e}", False)
print()


# Openpyxl
try:
	wb = openpyxl.Workbook()
	print("Openpyxl version:", openpyxl.__version__)
	print("Openpyxl workbook created.")
	check("Openpyxl test", True)
except Exception as e:
	check(f"Openpyxl test failed: {e}", False)
print()


# PyArrow
try:
	import pyarrow as pa
	print("PyArrow version:", pa.__version__)
	table = pa.table({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
	print("PyArrow table created with", len(table), "rows")
	check("PyArrow test", True)
except Exception as e:
	check(f"PyArrow test failed: {e}", False)
print()


# XlsxWriter
try:
	print("XlsxWriter version:", xlsxwriter.__version__)
	wb = xlsxwriter.Workbook('test_temp.xlsx')
	ws = wb.add_worksheet()
	ws.write('A1', 'Test')
	wb.close()
	os.remove('test_temp.xlsx')
	print("XlsxWriter workbook created and cleaned up.")
	check("XlsxWriter test", True)
except Exception as e:
	check(f"XlsxWriter test failed: {e}", False)
	# Clean up temp file if it exists
	if os.path.exists('test_temp.xlsx'):
		os.remove('test_temp.xlsx')
print()


# os (built-in, but included for completeness)
try:
	print("Current working directory:", os.getcwd())
	check("os test", True)
except Exception as e:
	check(f"os test failed: {e}", False)
print()

print("All libraries tested.")
