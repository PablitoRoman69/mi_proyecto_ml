import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import json
from config import DB
import psycopg2
from datetime import datetime

# 1️⃣ Cargar dataset limpio
df = pd.read_csv("dataset/bank-full-minado.csv")

# 2️⃣ Leer nuevos datos desde la BD (si hay)
conn = psycopg2.connect(**DB)
df_new = pd.read_sql("SELECT data, balance FROM new_data", conn)
conn.close()

if not df_new.empty:
    df_new_expanded = pd.json_normalize(df_new['data'])
    df_new_expanded['balance'] = df_new['balance']
    df = pd.concat([df, df_new_expanded], ignore_index=True)

# 3️⃣ Separar variables
y = df["balance"]
X = df.drop(columns=["balance"])

# 4️⃣ División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5️⃣ Entrenar modelo
model = LinearRegression()
model.fit(X_train, y_train)

# 6️⃣ Evaluar
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
rmse = mse ** 0.5

metrics = {
    "modelo": "Regresión Lineal",
    "R2": r2,
    "MSE": mse,
    "RMSE": rmse,
    "MAE": mae
}

print("✅ Modelo entrenado correctamente")
print(json.dumps(metrics, indent=4))

# 7️⃣ Guardar modelo y métricas
joblib.dump(model, "../model/linear_model.pkl")
with open("../model/metrics.json", "w") as f:
    json.dump(metrics, f)

# 8️⃣ Guardar métricas en la BD
try:
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO model_metrics (timestamp, modelo, r2, mse, rmse, mae)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        datetime.now(),
        metrics["modelo"],
        metrics["R2"],
        metrics["MSE"],
        metrics["RMSE"],
        metrics["MAE"]
    ))
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Métricas guardadas en la base de datos")
except Exception as e:
    print("❌ Error al guardar métricas en la BD:", e)
