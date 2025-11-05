# model/train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
from datetime import datetime
from sqlalchemy import text
from api.config import DB
import json

# -------------------------------
# 1️⃣ CARGAR DATASET MINADO
# -------------------------------
DATA_PATH = "dataset/bank-full-minado.csv"
df = pd.read_csv(DATA_PATH)

# Separar variables
if "y" not in df.columns:
    raise ValueError("❌ El dataset debe tener la columna 'y'")

X = df.drop(columns=["y"])
y = df["y"]

# -------------------------------
# 2️⃣ DIVISIÓN DE DATOS
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------------------
# 3️⃣ ENTRENAR MODELO
# -------------------------------
model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)

# Predicciones
y_pred = model.predict(X_test)

# -------------------------------
# 4️⃣ MÉTRICAS
# -------------------------------
metrics = {
    "timestamp": datetime.now(),
    "accuracy": accuracy_score(y_test, y_pred),
    "precision": precision_score(y_test, y_pred),
    "recall": recall_score(y_test, y_pred),
    "f1": f1_score(y_test, y_pred),
    "matriz_confusion": confusion_matrix(y_test, y_pred).tolist()  # Convertimos a lista para almacenar en DB
}

print("✅ Modelo guardado correctamente")
print("✅ Métricas calculadas:", metrics)

# -------------------------------
# 5️⃣ GUARDAR MODELO
# -------------------------------
joblib.dump(model, "model/regresion_logistica.pkl")

# -------------------------------
# 6️⃣ GUARDAR MÉTRICAS EN LA BASE DE DATOS (tabla dbo.metricas)
# -------------------------------
try:
    conn = DB.connect()
    
    # Convertimos la matriz de confusión a JSON
    metrics_to_save = metrics.copy()
    metrics_to_save["matriz_confusion"] = json.dumps(metrics["matriz_confusion"])
    
    query = text("""
        INSERT INTO dbo.metricas (timestamp, accuracy, precision, recall, f1, matriz_confusion)
        VALUES (:timestamp, :accuracy, :precision, :recall, :f1, :matriz_confusion)
    """)
    
    conn.execute(query, metrics_to_save)
    conn.commit()
    conn.close()
    
    print("✅ Métricas guardadas en dbo.metricas correctamente")
except Exception as e:
    print("❌ Error al guardar métricas en la BD:", e)
