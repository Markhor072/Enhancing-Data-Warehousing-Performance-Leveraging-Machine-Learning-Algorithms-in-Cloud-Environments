"""
download_tpch_db.py
Downloads the pre-generated DuckDB TPC-H SF10 database (~2.5GB).
Stores it in ./data/tpch-sf10.db
"""

import os
import urllib.request

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

url = "https://d3ko4xb3s7a54y.cloudfront.net/tpch-sf10.db"  # DuckDB-hosted TPC-H
out_path = os.path.join(DATA_DIR, "tpch-sf10.db")

if os.path.exists(out_path):
    print(f"Database already exists at {out_path}")
else:
    print("Downloading tpch-sf10.db (~2.5GB)...")
    urllib.request.urlretrieve(url, out_path)
    print(f"Saved to {out_path}")
