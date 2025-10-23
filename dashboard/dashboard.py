import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import psycopg2
from config import DB

def cargar_datos():
    conn = psycopg2.connect(**DB)
    df = pd.read_sql("SELECT * FROM model_metrics ORDER BY timestamp ASC", conn)
    conn.close()
    return df

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Container([
    html.H1("Dashboard de Monitoreo - Modelo de Regresión Lineal", className="text-center text-info mb-4"),
    dcc.Interval(id="interval", interval=15000, n_intervals=0),
    dcc.Graph(id="grafico_r2"),
    dcc.Graph(id="grafico_rmse")
])

@app.callback(
    [dash.Output("grafico_r2", "figure"),
     dash.Output("grafico_rmse", "figure")],
    [dash.Input("interval", "n_intervals")]
)
def actualizar(n):
    df = cargar_datos()
    fig_r2 = px.line(df, x="timestamp", y="r2", title="Evolución del R²")
    fig_rmse = px.line(df, x="timestamp", y="rmse", title="Evolución del RMSE")
    return fig_r2, fig_rmse

if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
