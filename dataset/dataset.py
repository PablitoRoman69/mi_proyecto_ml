import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from sklearn.preprocessing import MinMaxScaler
print("✅ Todo instalado correctamente")

# ================================
# 1. ADQUISICIÓN DE DATOS
# ================================
df = pd.read_csv("bank-full.csv", sep=";")  # leemos todo el dataset original

# ================================
# 2. LIMPIEZA DE DATOS
# ================================
# Revisar valores nulos
print("Valores nulos por columna:\n", df.isnull().sum())

# Revisar duplicados
print("Duplicados encontrados:", df.duplicated().sum())

# Eliminamos duplicados si existieran
df = df.drop_duplicates()

# ================================
# 3. TRANSFORMACIÓN DE DATOS
# ================================
# - Codificación de variables categóricas
df_transformed = pd.get_dummies(df, drop_first=True)

# - Normalización de columnas numéricas (ejemplo: age y balance)
scaler = MinMaxScaler()
df_transformed[["age", "balance"]] = scaler.fit_transform(df[["age", "balance"]])

# ================================
# 3.1 GUARDAR DATOS MINADOS
# ================================
df_transformed.to_csv("bank-full-minado.csv", index=False)
print("✅ Archivo 'bank-full-minado.csv' generado con éxito.")


# ================================
# 4. VISUALIZACIÓN DE DATOS (DASHBOARD)
# ================================
# Gráficas principales
fig_age = px.histogram(df, x="age", nbins=30, title="Distribución de la Edad", marginal="box")

fig_target = px.histogram(df, x="y", title="Distribución de la variable objetivo (y)")

fig_scatter = px.scatter(df, x="age", y="balance", color="y",
                         title="Relación entre Edad, Balance y Suscripción")

fig_box = px.box(df, x="job", y="balance", title="Distribución de Balance por Tipo de Trabajo")
fig_box.update_xaxes(tickangle=45)

# ================================
# DASHBOARD EN DASH
# ================================
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Dashboard - Bank Marketing Dataset", className="text-center my-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_age), md=6),
        dbc.Col(dcc.Graph(figure=fig_target), md=6)
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_scatter), md=12)
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_box), md=12)
    ])
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True, port=8050)

