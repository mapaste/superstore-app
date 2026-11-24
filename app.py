import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Superstore Nube", layout="wide")
st.title("📊 Panel de Control Superstore (En la Nube)")

# 1. Cargar datos limpios incluidos en el repositorio
DATA_PATH = Path(__file__).resolve().parent / "superstore_limpio.csv"

@st.cache_data
def cargar_datos():
    return pd.read_csv(DATA_PATH, encoding="utf-8")

df = cargar_datos()

# 2. Filtros
st.sidebar.header("Filtros")

categorias = sorted(df["category"].dropna().unique())
regiones = sorted(df["region"].dropna().unique())
segmentos = sorted(df["segment"].dropna().unique())

categoria_seleccionada = st.sidebar.multiselect(
    "Categoría",
    categorias,
    default=categorias,
)
region_seleccionada = st.sidebar.multiselect(
    "Región",
    regiones,
    default=regiones,
)
segmento_seleccionado = st.sidebar.multiselect(
    "Segmento",
    segmentos,
    default=segmentos,
)

df_filtrado = df[
    df["category"].isin(categoria_seleccionada)
    & df["region"].isin(region_seleccionada)
    & df["segment"].isin(segmento_seleccionado)
]

# 3. Métricas
col1, col2, col3 = st.columns(3)
col1.metric("Ventas Totales", f"${df_filtrado['sales'].sum():,.2f}")
col2.metric("Ganancia Total", f"${df_filtrado['profit'].sum():,.2f}")
col3.metric("Registros", f"{len(df_filtrado):,}")

# 4. Gráfico
df_cat = df_filtrado.groupby("category", as_index=False)["sales"].sum()
fig = px.bar(df_cat, x="category", y="sales", color="category")
st.plotly_chart(fig, use_container_width=True)