"""
extract_features.py
Reads results/logs/query_runs.csv and produces a feature CSV for ML training:
- features: query_name, sql_length, num_joins (estimated), num_filters, rows, runtime_ms
This is a simple heuristic extractor. For production, parse the SQL AST.
"""
import os, re, pandas as pd
BASE = os.path.join(os.path.dirname(__file__), '..')
IN_CSV = os.path.join(BASE, 'results', 'logs', 'query_runs.csv')
OUT_CSV = os.path.join(BASE, 'results', 'logs', 'query_features.csv')

df = pd.read_csv(IN_CSV)
feats = []
for _, row in df.iterrows():
    qname = row['query']
    plan = str(row.get('plan',''))
    # heuristic SQL token counts (fallback)
    sql_text = plan.lower()
    sql_length = len(sql_text)
    num_joins = sql_text.count('join')
    num_filters = sql_text.count('filter') + sql_text.count('where')
    feats.append({
        "query": qname,
        "sql_length": sql_length,
        "num_joins": num_joins,
        "num_filters": num_filters,
        "rows": int(row.get('rows',0)),
        "runtime_ms": float(row.get('runtime_ms',0.0))
    })

pd.DataFrame(feats).to_csv(OUT_CSV, index=False)
print("Saved features to", OUT_CSV)
