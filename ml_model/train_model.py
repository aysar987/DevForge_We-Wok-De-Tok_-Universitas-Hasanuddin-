import pandas as pd
import time
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import GridSearchCV
import joblib
import os

USE_FEATURES_CSV = True

if USE_FEATURES_CSV and os.path.exists("Cleaned_PhishScan_Features_v2.csv"):
    print("Memuat data dari Cleaned_PhishScan_Features_v2.csv...")
    df = pd.read_csv("Cleaned_PhishScan_Features_v2.csv")
    df["label"] = df["label"].astype(int)
    df = df.dropna(subset=["label"])
    print(df["label"].value_counts())
    X = df.drop(columns=["url", "label"])
    y = df["label"]
    

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)


print("Melatih model XGBoost...")
start = time.time()

param_grid = {
   'max_depth': [3, 5],
    'n_estimators': [100],
    'learning_rate': [0.1],
    'subsample': [1.0],
    'colsample_bytree': [1.0],
    'scale_pos_weight': [1, 2]
}

xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
grid_search = GridSearchCV(
    estimator=xgb,
    param_grid=param_grid,
    scoring='f1',
    cv=3,
    verbose=2,
    n_jobs=2
)

print("Melakukan grid search hyperparameter...")
grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_:.4f}")

model = grid_search.best_estimator_

duration = round(time.time() - start, 2)
print(f"Model dilatih dalam {duration} detik")

#Evaluasi model
y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)

print("\nClassification Report:")
print(report)


with open("model_report.txt", "w") as f:
    f.write("=== Classification Report ===\n")
    f.write(report)
    f.write("\n\n=== Confusion Matrix ===\n")
    f.write(str(conf_matrix))
    f.write(f"\n\nAccuracy: {accuracy:.4f}")

print("Laporan evaluasi disimpan ke model_report.txt")

joblib.dump(model, "model.pkl")
print("Model disimpan ke model.pkl")

import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(10, 6))
importances = model.feature_importances_
features = X.columns
indices = np.argsort(importances)

plt.barh(range(len(indices)), importances[indices], align="center")
plt.yticks(range(len(indices)), [features[i] for i in indices])
plt.xlabel("Pentingnya Fitur")
plt.title("Feature Importance - XGBoost")
plt.tight_layout()
plt.savefig("feature_importance.png")
print("Diagram feature importance disimpan ke feature_importance.png")
