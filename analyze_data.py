import pandas as pd
import numpy as np

# Load data
try:
    df = pd.read_csv('fraud.csv')
    print("Columns found in CSV:", df.columns.tolist())
except Exception as e:
    print("Error reading with headers:", e)
    df = pd.read_csv('fraud.csv', header=None)
    print("Reading without headers. Columns:", df.columns.tolist())

# Basic info
print("\nShape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

print("\nUnique values in categorical-looking columns:")
for col in df.columns:
    if df[col].nunique() < 20:
        print(f"{col}: {df[col].unique()}")

print("\nTarget distribution:")
last_col = df.columns[-1]
print(df[last_col].value_counts(normalize=True))

