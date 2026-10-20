from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="People Analytics | Turnover", page_icon="📊", layout="wide")

RED = "#E30613"
DARK = "#252525"
GRAY = "#6B6B6B"
PALETTE = [RED, "#F57C84", "#7A1E25", "#FFB3B8", "#A9A9A9"]

st.markdown("""
<style>
.block-container {max-width: 1250px; padding-top: 1.5rem;}
.hero {background: linear-gradient(120deg,#E30613,#9E0010); color:white; padding:1.8rem 2rem; border-radius:20px; margin-bottom:1rem;}
.hero h1 {margin:0; font-size:2.25rem;}
.hero p {margin:.4rem 0 0; opacity:.95;}
[data-testid="stMetric"] {background:#F7F7F7; border:1px solid #ECECEC; padding:14px; border-radius:14px;}
[data-testid="stSidebar"] {background:#F7F7F7;}
</style>
""", unsafe_allow_html=True)

DATA_FILE = Path("HR_Analytics_Dashboard.xlsx")

@st.cache_data
def load_data():
    df = pd.read_excel(DATA_FILE, sheet_name="HR_Analytics", engine="openpyxl")
    df.columns = df.columns.str.strip()
    return df

def turnover_table(data, category):
    out = (data.groupby(category, dropna=False)
           .agg(Colaboradores=("ID_Empleado", "count"), Casos_TO=("TO_Decod", "sum"), Tasa_TO=("TO_Decod", "mean"))
           .reset_index())
    out["Tasa_TO"] = out["Tasa_TO"] * 100
    return out.sort_values("Tasa_TO", ascending=False)

def rate_chart(data, category, title, horizontal=True):
    t = turnover_table(data, category)
    if horizontal:
        fig = px.bar(t.sort_values("Tasa_TO"), x="Tasa_TO", y=category, orientation="h", text_auto=".1f", title=title,
                     color="Tasa_TO", color_continuous_scale=["#F4D4D6", RED])
        fig.update_xaxes(title="Tasa de turnover (%)")
        fig.update_yaxes(title="")
    else:
        fig = px.bar(t, x=category, y="Tasa_TO", text_auto=".1f", title=title,
                     color="Tasa_TO", color_continuous_scale=["#F4D4D6", RED])
        fig.update_yaxes(title="Tasa de turnover (%)")
        fig.update_xaxes(title="")
    fig.update_layout(coloraxis_showscale=False, margin=dict(l=10,r=10,t=55,b=10), height=390)
    return fig

if not DATA_FILE.exists():
    st.error("No se encontró HR_Analytics_Dashboard.xlsx en la raíz del repositorio.")
    st.stop()

df = load_data()

st.markdown('<div class="hero"><h1>People Analytics · Turnover</h1><p>Diagnóstico descriptivo para identificar segmentos y factores asociados a la deserción.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Filtros")
    functions = st.multiselect("Función", sorted(df["Funcion"].dropna().unique()), default=sorted(df["Funcion"].dropna().unique()))
    ages = st.multiselect("Grupo de edad", sorted(df["Grupo_Edad"].dropna().unique()), default=sorted(df["Grupo_Edad"].dropna().unique()))
    overtime = st.multiselect("Sobretiempo", sorted(df["Sobretiempo"].dropna().unique()), default=sorted(df["Sobretiempo"].dropna().unique()))
    travel = st.multiselect("Viaje de negocio", sorted(df["Viaje_Negocio"].dropna().unique()), default=sorted(df["Viaje_Negocio"].dropna().unique()))
    salary = st.multiselect("Rango salarial", sorted(df["Rango_salarial"].dropna().unique()), default=sorted(df["Rango_salarial"].dropna().unique()))
    st.caption("Todos los indicadores y gráficos responden a estos filtros.")

f = df[df["Funcion"].isin(functions) & df["Grupo_Edad"].isin(ages) & df["Sobretiempo"].isin(overtime) & df["Viaje_Negocio"].isin(travel) & df["Rango_salarial"].isin(salary)].copy()
if f.empty:
    st.warning("La combinación de filtros no devuelve registros.")
    st.stop()

n = len(f)
to_cases = int(f["TO_Decod"].sum())
to_rate = f["TO_Decod"].mean() * 100
salary_avg = f["Salario_mensual"].mean()
overtime_rate = (f["Sobretiempo_Decod"].mean() * 100)

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Colaboradores", f"{n:,}")
c2.metric("Casos de TO", f"{to_cases:,}")
c3.metric("Tasa de TO", f"{to_rate:.1f}%")
c4.metric("Salario mensual prom.", f"{salary_avg:,.0f}")
c5.metric("Con sobretiempo", f"{overtime_rate:.1f}%")

page = st.radio("Vista", ["Resumen ejecutivo", "Experiencia y carga", "Carrera y compensación", "Detalle"], horizontal=True)

if page == "Resumen ejecutivo":
    a,b = st.columns(2)
    with a: st.plotly_chart(rate_chart(f, "Funcion", "Turnover por función"), use_container_width=True)
    with b: st.plotly_chart(rate_chart(f, "Grupo_Edad", "Turnover por grupo de edad"), use_container_width=True)
    a,b = st.columns(2)
    with a: st.plotly_chart(rate_chart(f, "Sobretiempo", "Turnover y sobretiempo", horizontal=False), use_container_width=True)
    with b: st.plotly_chart(rate_chart(f, "Viaje_Negocio", "Turnover y frecuencia de viaje"), use_container_width=True)
    st.subheader("Lectura rápida del segmento filtrado")
    drivers = []
    for col, label in [("Sobretiempo","sobretiempo"),("Grupo_Edad","grupo de edad"),("Viaje_Negocio","frecuencia de viaje"),("Rango_salarial","rango salarial")]:
        t = turnover_table(f, col)
        if len(t): drivers.append(f"**{label.capitalize()}:** `{t.iloc[0][col]}` presenta la mayor tasa descriptiva ({t.iloc[0]['Tasa_TO']:.1f}%, n={int(t.iloc[0]['Colaboradores'])}).")
    st.markdown("\n\n".join(drivers))

elif page == "Experiencia y carga":
    a,b = st.columns(2)
    with a: st.plotly_chart(rate_chart(f, "SatisfaccionLaboral", "Turnover por satisfacción laboral", False), use_container_width=True)
    with b: st.plotly_chart(rate_chart(f, "Satisfaccion_Trabajo", "Turnover por satisfacción con el trabajo", False), use_container_width=True)
    a,b = st.columns(2)
    with a: st.plotly_chart(rate_chart(f, "Satisfaccion_equipo_directo", "Turnover por satisfacción con equipo directo", False), use_container_width=True)
    with b: st.plotly_chart(rate_chart(f, "Nivel_balance_laboral", "Turnover por balance laboral", False), use_container_width=True)

elif page == "Carrera y compensación":
    a,b = st.columns(2)
    with a: st.plotly_chart(rate_chart(f, "Rango_salarial", "Turnover por rango salarial"), use_container_width=True)
    with b: st.plotly_chart(rate_chart(f, "Nivel_Trabajo", "Turnover por nivel de trabajo", False), use_container_width=True)
    a,b = st.columns(2)
    with a:
        fig=px.histogram(f, x="Anios_compania", color="TO", barmode="overlay", color_discrete_map={"Si":RED,"No":"#BDBDBD"}, title="Antigüedad en la compañía")
        fig.update_layout(margin=dict(l=10,r=10,t=55,b=10), height=390); st.plotly_chart(fig,use_container_width=True)
    with b:
        fig=px.box(f, x="TO", y="Salario_mensual", color="TO", color_discrete_map={"Si":RED,"No":"#BDBDBD"}, title="Salario mensual según turnover")
        fig.update_layout(showlegend=False, margin=dict(l=10,r=10,t=55,b=10), height=390); st.plotly_chart(fig,use_container_width=True)

else:
    st.subheader("Base filtrada")
    cols = ["ID_Empleado","TO","Funcion","Rol_Organizacion","Grupo_Edad","Sobretiempo","Viaje_Negocio","Rango_salarial","Salario_mensual","Anios_compania","Nivel_balance_laboral"]
    st.dataframe(f[cols], use_container_width=True, hide_index=True)
    st.download_button("Descargar detalle filtrado", f[cols].to_csv(index=False).encode("utf-8-sig"), "detalle_turnover_filtrado.csv", "text/csv")

st.divider()
st.caption("Análisis descriptivo. Las asociaciones observadas no establecen causalidad ni deben usarse para decisiones individuales de empleo.")
