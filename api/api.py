from fastapi import FastAPI
import joblib, json, pandas as pd
from datetime import datetime
import psycopg2
from config import DB

app = FastAPI(title="API - Regresión Lineal Bank Marketing")

# Cargar modelo y métricas
model = joblib.load("../model/linear_model.pkl")
with open("../model/metrics.json") as f:
    metrics = json.load(f)

@app.get("/")
def root():
    return {"status": "API funcionando correctamente"}

@app.get("/metrics")
def get_metrics():
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
    return metrics

@app.post("/predict")
def predict(data: dict):
    df_input = pd.DataFrame([data])
    pred = model.predict(df_input)
    return {"prediccion_balance": float(pred[0])}

@app.post("/add_data")
def add_data(data: dict):
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO new_data (timestamp, data, balance)
        VALUES (%s, %s, %s)
    """, (
        datetime.now(),
        json.dumps(data),
        data.get("balance")
    ))
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "dato guardado correctamente"}
