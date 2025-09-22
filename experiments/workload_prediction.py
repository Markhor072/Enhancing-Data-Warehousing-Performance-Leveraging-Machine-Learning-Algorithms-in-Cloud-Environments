"""
workload_prediction.py
Trains a regression model (RandomForest + XGBoost) to predict query runtime.
Outputs model metrics and a small results CSV.
"""
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

BASE = os.path.join(os.path.dirname(__file__), '..')
FEAT_CSV = os.path.join(BASE, 'results', 'logs', 'query_features.csv')
OUT_DIR = os.path.join(BASE, 'results', 'logs')
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(FEAT_CSV)
X = df[['sql_length','num_joins','num_filters','rows']]
y = df['runtime_ms']

# small dataset -> use random_state
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

models = {
    "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
    "XGBoost": XGBRegressor(n_estimators=100, use_label_encoder=False, eval_metric='rmse', random_state=42)
}

summary = []
for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    rmse = mean_squared_error(y_test, preds, squared=False)
    r2 = r2_score(y_test, preds)
    # save model
    joblib.dump(model, os.path.join(OUT_DIR, f"{name}.joblib"))
    summary.append({"model":name, "rmse":rmse, "r2":r2})
    print(f"{name} -> RMSE: {rmse:.3f} ms, R2: {r2:.3f}")

pd.DataFrame(summary).to_csv(os.path.join(OUT_DIR, "workload_prediction_summary.csv"), index=False)
print("Saved summary to results/logs/workload_prediction_summary.csv")
