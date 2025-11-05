from sqlalchemy import create_engine, text

DB_URL = "mssql+pyodbc://mladmin:Equipo269@mlpserver.database.windows.net/ml_db?driver=ODBC+Driver+18+for+SQL+Server"
engine = create_engine(DB_URL, fast_executemany=True)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Conexión exitosa:", result.fetchone())
except Exception as e:
    print("❌ Error de conexión:", e)
