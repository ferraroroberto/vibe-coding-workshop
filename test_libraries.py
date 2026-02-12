# Simple script to test basic imports and functionality of workshop libraries
import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import docx
import pptx
import xlrd
import xlwt
import win32api
import os


def check(msg, success):
	# Green check for success, red cross for failure
	if success:
		print(f"\033[92m✔\033[0m {msg}")
	else:
		print(f"\033[91m✘\033[0m {msg}")

print("Testing imports...\n")


# Data manipulation
try:
	print("Pandas version:", pd.__version__)
	df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
	print("DataFrame:\n", df)
	check("Pandas test", True)
except Exception as e:
	check(f"Pandas test failed: {e}", False)
print()


# Numpy
try:
	arr = np.array([1, 2, 3])
	print("Numpy array:", arr)
	check("Numpy test", True)
except Exception as e:
	check(f"Numpy test failed: {e}", False)
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
	print("Seaborn set style.")
	check("Seaborn test", True)
except Exception as e:
	check(f"Seaborn test failed: {e}", False)
print()


# Openpyxl
try:
	wb = openpyxl.Workbook()
	print("Openpyxl workbook created.")
	check("Openpyxl test", True)
except Exception as e:
	check(f"Openpyxl test failed: {e}", False)
print()


# python-docx
try:
	print("python-docx available:", hasattr(docx, 'Document'))
	check("python-docx test", True)
except Exception as e:
	check(f"python-docx test failed: {e}", False)
print()

# python-pptx

# python-pptx
try:
	print("python-pptx available:", hasattr(pptx, 'Presentation'))
	check("python-pptx test", True)
except Exception as e:
	check(f"python-pptx test failed: {e}", False)
print()

# xlrd

# xlrd
try:
	print("xlrd version:", xlrd.__version__)
	check("xlrd test", True)
except Exception as e:
	check(f"xlrd test failed: {e}", False)
print()

# xlwt

# xlwt
try:
	print("xlwt version:", xlwt.__VERSION__)
	check("xlwt test", True)
except Exception as e:
	check(f"xlwt test failed: {e}", False)
print()

# win32api

# win32api
try:
	print("win32api available:", hasattr(win32api, 'GetUserName'))
	check("win32api test", True)
except Exception as e:
	check(f"win32api test failed: {e}", False)
print()

# os

# os
try:
	print("Current working directory:", os.getcwd())
	check("os test", True)
except Exception as e:
	check(f"os test failed: {e}", False)
print()

print("All libraries tested.")
