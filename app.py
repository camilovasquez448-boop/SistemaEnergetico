import streamlit as st
import pandas as pd
import sqlite3
import math
import matplotlib.pyplot as plt

# =====================================================
# CONFIGURACION
# =====================================================

st.set_page_config(
    page_title="Sistema Energético",
    page_icon="⚡",
    layout="wide"
)

# =====================================================
# ESTILOS
# =====================================================

st.markdown("""

<style>

.main {
    background-color: #0E1117;
}

h1,h2,h3 {
    color: #00D4FF;
}

.stMetric {
    background-color: #1C1F26;
    padding: 15px;
    border-radius: 15px;
}

</style>

""", unsafe_allow_html=True)

# =====================================================
# BASE DE DATOS
# =====================================================

conexion = sqlite3.connect(
    "energia.db",
    check_same_thread=False
)

cursor = conexion.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS encuestas(

id INTEGER PRIMARY KEY AUTOINCREMENT,

torre TEXT,
personas TEXT,
habitacion TEXT,

aire TEXT,
cantidad_aires TEXT,
tipo_aire TEXT,
voltaje_aire TEXT,
horas_aire TEXT,

ventiladores TEXT,
horas_vent TEXT,

refrigerador TEXT,
potencia_refri REAL,
voltaje_refri TEXT,
corriente_refri REAL,

bombillos TEXT,
tipo_iluminacion TEXT,
potencia_bombillos REAL,

tv TEXT,
lavadora TEXT,
microondas TEXT,
pc TEXT,

consumo_percibido TEXT,
problemas TEXT,

potencia REAL,
corriente REAL,
energia REAL,
joule REAL,
campo REAL,
densidad REAL,

riesgo TEXT

)

""")

conexion.commit()

# =====================================================
# FUNCIONES
# =====================================================

def valor_numero(texto):

    mapa = {

        "No": 0,
        "Sí": 1,

        "0": 0,
        "1": 1,
        "2": 2,
        "3 o más": 3,

        "1 a 3 horas": 2,
        "4 a 6 horas": 5,
        "Más de 8 horas": 9,

        "Bajo": 1,
        "Medio": 2,
        "Alto": 3
    }

    return mapa.get(str(texto), 0)

# =====================================================
# TITULO
# =====================================================

st.title("⚡ Sistema Inteligente de Análisis Energético")

st.markdown("---")

# =====================================================
# FORMULARIO
# =====================================================

col1, col2 = st.columns(2)

# =====================================================
# COLUMNA 1
# =====================================================

with col1:

    st.subheader("🏢 Información General")

    torre = st.selectbox(
        "Torre",
        [
            "Torre A",
            "Torre B",
            "Torre C",
            "Torre D"
        ]
    )

    personas = st.selectbox(
        "Número de personas",
        [
            "1",
            "2",
            "3",
            "4",
            "5 o más"
        ]
    )

    habitacion = st.selectbox(
        "¿Habita permanentemente?",
        [
            "Sí",
            "No"
        ]
    )

    st.subheader("❄ Aire Acondicionado")

    aire = st.selectbox(
        "¿Tiene aire acondicionado?",
        [
            "Sí",
            "No"
        ]
    )

    cantidad_aires = st.selectbox(
        "Cantidad de aires",
        [
            "0",
            "1",
            "2",
            "3 o más"
        ]
    )

    tipo_aire = st.selectbox(
        "Tipo de aire",
        [
            "Mini Split",
            "Ventana",
            "Inverter",
            "No sabe"
        ]
    )

    voltaje_aire = st.selectbox(
        "Voltaje aire",
        [
            "110",
            "220"
        ]
    )

    horas_aire = st.selectbox(
        "Horas de uso aire",
        [
            "1 a 3 horas",
            "4 a 6 horas",
            "Más de 8 horas"
        ]
    )

    st.subheader("🌀 Ventiladores")

    ventiladores = st.selectbox(
        "Cantidad ventiladores",
        [
            "0",
            "1",
            "2",
            "3 o más"
        ]
    )

    horas_vent = st.selectbox(
        "Horas ventiladores",
        [
            "1 a 3 horas",
            "4 a 6 horas",
            "Más de 8 horas"
        ]
    )

# =====================================================
# COLUMNA 2
# =====================================================

with col2:

    st.subheader("🧊 Refrigerador")

    refrigerador = st.selectbox(
        "¿Tiene refrigerador?",
        [
            "Sí",
            "No"
        ]
    )

    potencia_refri = st.number_input(
        "Potencia refrigerador (W)",
        min_value=0.0,
        value=180.0
    )

    voltaje_refri = st.selectbox(
        "Voltaje refrigerador",
        [
            "110",
            "220"
        ]
    )

    corriente_refri = st.number_input(
        "Corriente refrigerador (A)",
        min_value=0.0,
        value=1.5
    )

    st.subheader("💡 Iluminación")

    bombillos = st.selectbox(
        "Cantidad bombillos",
        [
            "0",
            "1",
            "2",
            "3 o más"
        ]
    )

    tipo_iluminacion = st.selectbox(
        "Tipo iluminación",
        [
            "LED",
            "Ahorrador",
            "Incandescente"
        ]
    )

    potencia_bombillos = st.number_input(
        "Potencia bombillos (W)",
        min_value=0.0,
        value=15.0
    )

    st.subheader("📺 Otros Equipos")

    tv = st.selectbox(
        "¿Tiene TV?",
        [
            "Sí",
            "No"
        ]
    )

    lavadora = st.selectbox(
        "¿Tiene lavadora?",
        [
            "Sí",
            "No"
        ]
    )

    microondas = st.selectbox(
        "¿Tiene microondas?",
        [
            "Sí",
            "No"
        ]
    )

    pc = st.selectbox(
        "¿Tiene computador?",
        [
            "Sí",
            "No"
        ]
    )

    st.subheader("📊 Comportamiento")

    consumo_percibido = st.selectbox(
        "Percepción del consumo",
        [
            "Bajo",
            "Medio",
            "Alto"
        ]
    )

    problemas = st.selectbox(
        "Problemas eléctricos",
        [
            "No",
            "Sí, a veces",
            "Frecuentes"
        ]
    )

# =====================================================
# BOTON
# =====================================================

analizar = st.button("⚡ ANALIZAR")

# =====================================================
# ANALISIS
# =====================================================

if analizar:

    # =================================================
    # POTENCIAS
    # =================================================

    potencia_aires = valor_numero(cantidad_aires) * 850

    potencia_vent = valor_numero(ventiladores) * 80

    potencia_refrigerador = (
        valor_numero(refrigerador) * potencia_refri
    )

    potencia_luces = (
        valor_numero(bombillos) * potencia_bombillos
    )

    potencia_tv = valor_numero(tv) * 120

    potencia_lavadora = valor_numero(lavadora) * 500

    potencia_micro = valor_numero(microondas) * 1200

    potencia_pc = valor_numero(pc) * 300

    potencia = (

        potencia_aires +
        potencia_vent +
        potencia_refrigerador +
        potencia_luces +
        potencia_tv +
        potencia_lavadora +
        potencia_micro +
        potencia_pc

    )

    # =================================================
    # LEY DE OHM
    # =================================================

    voltaje = float(voltaje_aire)

    corriente = potencia / voltaje

    # =================================================
    # ENERGIA
    # =================================================

    energia = (potencia * 30) / 1000

    # =================================================
    # EFECTO JOULE
    # =================================================

    resistencia = 0.05

    joule = (corriente ** 2) * resistencia

    # =================================================
    # LEY DE AMPERE
    # =================================================

    mu0 = 4 * math.pi * (10 ** -7)

    campo = (

        mu0 * corriente

    ) / (

        2 * math.pi * 0.05
    )

    # =================================================
    # DENSIDAD
    # =================================================

    densidad = corriente / 2.5e-6

    # =================================================
    # RIESGO
    # =================================================

    if corriente > 25:

        riesgo = "MUY ALTO"

    elif corriente > 15:

        riesgo = "ALTO"

    elif corriente > 8:

        riesgo = "MEDIO"

    else:

        riesgo = "BAJO"

    # =================================================
    # GUARDAR
    # =================================================

    cursor.execute("""

    INSERT INTO encuestas(

    torre,
    personas,
    habitacion,

    aire,
    cantidad_aires,
    tipo_aire,
    voltaje_aire,
    horas_aire,

    ventiladores,
    horas_vent,

    refrigerador,
    potencia_refri,
    voltaje_refri,
    corriente_refri,

    bombillos,
    tipo_iluminacion,
    potencia_bombillos,

    tv,
    lavadora,
    microondas,
    pc,

    consumo_percibido,
    problemas,

    potencia,
    corriente,
    energia,
    joule,
    campo,
    densidad,

    riesgo

    )

    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

    """, (

        torre,
        personas,
        habitacion,

        aire,
        cantidad_aires,
        tipo_aire,
        voltaje_aire,
        horas_aire,

        ventiladores,
        horas_vent,

        refrigerador,
        potencia_refri,
        voltaje_refri,
        corriente_refri,

        bombillos,
        tipo_iluminacion,
        potencia_bombillos,

        tv,
        lavadora,
        microondas,
        pc,

        consumo_percibido,
        problemas,

        potencia,
        corriente,
        energia,
        joule,
        campo,
        densidad,

        riesgo

    ))

    conexion.commit()

    # =================================================
    # RESULTADOS
    # =================================================

    st.success("✅ Encuesta registrada")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "⚡ Potencia Total",
        f"{potencia:.2f} W"
    )

    col2.metric(
        "🔌 Corriente",
        f"{corriente:.2f} A"
    )

    col3.metric(
        "⚠ Riesgo",
        riesgo
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "🔥 Pérdidas Joule",
        f"{joule:.2f} W"
    )

    col5.metric(
        "🧲 Campo Magnético",
        f"{campo:.10f} T"
    )

    col6.metric(
        "⚡ Energía Mensual",
        f"{energia:.2f} kWh"
    )

    # =================================================
    # GRAFICAS
    # =================================================

    st.markdown("---")

    st.subheader("📊 Distribución de Consumo")

    equipos = [
        "Aires",
        "Ventiladores",
        "Refrigerador",
        "Bombillos",
        "TV",
        "Lavadora",
        "Microondas",
        "PC"
    ]

    consumos = [

        potencia_aires,
        potencia_vent,
        potencia_refrigerador,
        potencia_luces,
        potencia_tv,
        potencia_lavadora,
        potencia_micro,
        potencia_pc

    ]

    fig, ax = plt.subplots(figsize=(10,5))

    ax.bar(
        equipos,
        consumos
    )

    plt.xticks(rotation=20)

    st.pyplot(fig)

    # =================================================
    # GRAFICA CIRCULAR
    # =================================================

    fig2, ax2 = plt.subplots(figsize=(7,7))

    ax2.pie(
        consumos,
        labels=equipos,
        autopct='%1.1f%%'
    )

    st.pyplot(fig2)

# =====================================================
# HISTORIAL
# =====================================================

st.markdown("---")

st.subheader("📁 Historial")

datos = pd.read_sql_query(
    "SELECT * FROM encuestas",
    conexion
)

st.dataframe(datos)

# =====================================================
# EXPORTAR EXCEL
# =====================================================

if st.button("📥 GENERAR EXCEL"):

    datos.to_excel(
        "ReporteEnergetico.xlsx",
        index=False
    )

    st.success("✅ Excel generado")