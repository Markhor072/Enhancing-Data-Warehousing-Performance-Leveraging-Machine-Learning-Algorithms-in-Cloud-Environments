"""
anomaly_detection.py
Uses Isolation Forest and a simple Autoencoder to detect anomalous query runtimes / resource spikes.
We mark as anomalies runs with runtime_ms > mean + 2*std (synthetic labels), then evaluate.
"""
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_score, recall_score, f1_score
import tensorflow as tf
from tensorflow.keras import layers, models

BASE = os.path.join(os.path.dirname(__file__), '..')
FEAT_CSV = os.path.join(BASE, 'results', 'logs', 'query_features.csv')
OUT_DIR = os.path.join(BASE, 'results', 'logs')
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(FEAT_CSV)
X = df[['sql_length','num_joins','num_filters','rows']].values
y_runtime = df['runtime_ms'].values

# Create synthetic anomaly labels: runtime > mean + 2*std
thr = y_runtime.mean() + 2*y_runtime.std()
y_label = (y_runtime > thr).astype(int)
print(f"Anomalies by threshold: {y_label.sum()}/{len(y_label)}")

# Isolation Forest
iso = IsolationForest(contamination=0.1, random_state=42)
iso.fit(X)
iso_preds = iso.predict(X)
iso_labels = (iso_preds == -1).astype(int)

p_iso = precision_score(y_label, iso_labels, zero_division=0)
r_iso = recall_score(y_label, iso_labels, zero_division=0)
f_iso = f1_score(y_label, iso_labels, zero_division=0)
print(f"IsolationForest -> Precision: {p_iso:.3f}, Recall: {r_iso:.3f}, F1: {f_iso:.3f}")

# Autoencoder
n_features = X.shape[1]
X_norm = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-9)
train_idx = np.where(y_label == 0)[0]
X_train = X_norm[train_idx]

ae = models.Sequential([
    layers.Input(shape=(n_features,)),
    layers.Dense(8, activation='relu'),
    layers.Dense(4, activation='relu'),
    layers.Dense(8, activation='relu'),
    layers.Dense(n_features)
])
ae.compile(optimizer='adam', loss='mse')
ae.fit(X_train, X_train, epochs=50, batch_size=8, verbose=0)

recon = ae.predict(X_norm)
mse = np.mean(np.square(recon - X_norm), axis=1)
thr_ae = np.percentile(mse, 95)
ae_labels = (mse > thr_ae).astype(int)

p_ae = precision_score(y_label, ae_labels, zero_division=0)
r_ae = recall_score(y_label, ae_labels, zero_division=0)
f_ae = f1_score(y_label, ae_labels, zero_division=0)
print(f"Autoencoder -> Precision: {p_ae:.3f}, Recall: {r_ae:.3f}, F1: {f_ae:.3f}")

# Save summary
summary = pd.DataFrame([
    {"method":"IsolationForest","precision":p_iso,"recall":r_iso,"f1":f_iso},
    {"method":"Autoencoder","precision":p_ae,"recall":r_ae,"f1":f_ae}
])
summary.to_csv(os.path.join(OUT_DIR, "anomaly_detection_summary.csv"), index=False)
print("Saved anomaly detection summary to results/logs/anomaly_detection_summary.csv")
