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

# 2. Métricas
col1, col2, col3 = st.columns(3)
col1.metric("Ventas Totales", f"${df['sales'].sum():,.2f}")
col2.metric("Ganancia Total", f"${df['profit'].sum():,.2f}")
col3.metric("Registros", f"{len(df):,}")

# 3. Gráfico
df_cat = df.groupby('category')['sales'].sum().reset_index()
fig = px.bar(df_cat, x="category", y="sales", color="category")
st.plotly_chart(fig, use_container_width=True)