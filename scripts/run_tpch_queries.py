"""
run_tpch_queries.py
Executes a set of TPC-H queries against the tpch-sf10.db and logs runtimes + plan info.
Outputs CSV to results/logs/query_runs.csv
"""
import duckdb
import os
import time
import pandas as pd
from tqdm import tqdm

BASE = os.path.join(os.path.dirname(__file__), '..')
DB_PATH = os.path.join(BASE, 'data', 'tpch-sf10.db')
OUT_DIR = os.path.join(BASE, 'results', 'logs')
os.makedirs(OUT_DIR, exist_ok=True)
OUT_CSV = os.path.join(OUT_DIR, 'query_runs.csv')

# Minimal set of TPC-H query SQL strings (Q1..Q22). We'll include a few to start.
# You can replace these with the official TPC-H SQL files from the kit for full 22 queries.
queries = {
    "Q1": """
    /* TPC-H Q1 simplified: revenue by nation */
    SELECT l_returnflag, l_linestatus, sum(l_quantity) as sum_qty, sum(l_extendedprice) as sum_base_price
    FROM lineitem
    WHERE l_shipdate <= DATE '1998-12-01'
    GROUP BY l_returnflag, l_linestatus
    """,
    "Q3": """
    SELECT o_orderpriority, count(*) as order_count
    FROM orders
    WHERE o_orderdate < DATE '1995-03-15' AND o_orderpriority IN ('1-URGENT','2-HIGH')
    GROUP BY o_orderpriority
    """,
    "Q6": """
    SELECT sum(l_extendedprice * (1 - l_discount)) as revenue
    FROM lineitem
    WHERE l_shipdate BETWEEN DATE '1994-01-01' AND DATE '1994-12-31' AND l_discount BETWEEN 0.05 AND 0.07
    """,
    "Q9": """
    SELECT nation, sum(volume) as tot_volume
    FROM (
      SELECT n_name as nation, l_extendedprice * (1 - l_discount) as volume
      FROM customer c JOIN orders o ON c.c_custkey=o.o_custkey
      JOIN lineitem l ON l.l_orderkey=o.o_orderkey
      JOIN nation n ON c.c_nationkey=n.n_nationkey
    )
    GROUP BY nation
    ORDER BY tot_volume DESC
    LIMIT 10
    """
}

# Connect to DuckDB
conn = duckdb.connect(DB_PATH)
conn.execute("PRAGMA threads=4;")  # tune threads if desired

results = []
for qname, qsql in tqdm(queries.items()):
    # warm-up
    try:
        conn.execute("EXPLAIN " + qsql)
    except Exception:
        pass
    t0 = time.perf_counter()
    conn.execute(qsql)
    _ = conn.fetchall()
    t1 = time.perf_counter()
    runtime_ms = (t1 - t0) * 1000.0
    # get simple plan info (string)
    plan = conn.execute("EXPLAIN " + qsql).fetchall()
    plan_text = "\n".join([row[0] for row in plan]) if plan else ""
    results.append({
        "query": qname,
        "runtime_ms": runtime_ms,
        "plan": plan_text,
        "rows": len(_)
    })
    print(f"{qname}: {runtime_ms:.1f} ms, rows {len(_)}")

df = pd.DataFrame(results)
df.to_csv(OUT_CSV, index=False)
print("Saved results to", OUT_CSV)
