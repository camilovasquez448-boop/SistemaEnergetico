import streamlit as st
import pandas as pd
import sqlite3
import math
import matplotlib.pyplot as plt

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Sistema Energético Inteligente",
    page_icon="⚡",
    layout="wide"
)

# =====================================================
# ESTILOS
# =====================================================

st.markdown("""

<style>

.main{
    background-color:#0E1117;
}

h1,h2,h3{
    color:#00D4FF;
}

.stMetric{
    background-color:#1C1F26;
    padding:15px;
    border-radius:15px;
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
btu_aire TEXT,
voltaje_aire TEXT,
horas_aire TEXT,

ventiladores TEXT,
horas_vent TEXT,

refrigerador TEXT,
potencia_refri REAL,
voltaje_refri TEXT,
corriente_refri REAL,
horas_refri REAL,

bombillos TEXT,
tipo_iluminacion TEXT,
potencia_bombillos REAL,
horas_luces REAL,

tv TEXT,
horas_tv REAL,

lavadora TEXT,
horas_lavadora REAL,

microondas TEXT,
horas_micro REAL,

pc TEXT,
horas_pc REAL,

consumo_percibido TEXT,
problemas TEXT,

potencia REAL,
corriente REAL,
energia REAL,
joule REAL,
campo REAL,
densidad REAL,
fp REAL,

riesgo TEXT

)

""")

conexion.commit()

# =====================================================
# FUNCIONES
# =====================================================

def valor_numero(texto):

    mapa = {

        "No":0,
        "Sí":1,

        "0":0,
        "1":1,
        "2":2,
        "3 o más":3,

        "1 a 3 horas":2,
        "4 a 6 horas":5,
        "Más de 8 horas":9

    }

    return mapa.get(str(texto), 0)

# =====================================================
# TÍTULO
# =====================================================

st.title("⚡ Sistema Inteligente de Análisis Energético")

st.markdown("---")

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

    # =================================================
    # AIRES
    # =================================================

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
            "Portátil"
        ]
    )

    btu_aire = st.selectbox(
        "BTU del aire",
        [
            "9000",
            "12000",
            "18000",
            "24000"
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
        "Horas uso aire",
        [
            "1 a 3 horas",
            "4 a 6 horas",
            "Más de 8 horas"
        ]
    )

    # =================================================
    # VENTILADORES
    # =================================================

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

    # =================================================
    # NEVERA
    # =================================================

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

    horas_refri = st.slider(
        "Horas refrigerador",
        1,
        24,
        12
    )

    # =================================================
    # ILUMINACIÓN
    # =================================================

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
        "Potencia bombillo (W)",
        min_value=0.0,
        value=15.0
    )

    horas_luces = st.slider(
        "Horas iluminación",
        1,
        24,
        6
    )

    # =================================================
    # OTROS EQUIPOS
    # =================================================

    st.subheader("📺 Otros Equipos")

    tv = st.selectbox(
        "¿Tiene TV?",
        [
            "Sí",
            "No"
        ]
    )

    horas_tv = st.slider(
        "Horas TV",
        1,
        24,
        5
    )

    lavadora = st.selectbox(
        "¿Tiene lavadora?",
        [
            "Sí",
            "No"
        ]
    )

    horas_lavadora = st.slider(
        "Horas lavadora",
        1,
        24,
        2
    )

    microondas = st.selectbox(
        "¿Tiene microondas?",
        [
            "Sí",
            "No"
        ]
    )

    horas_micro = st.slider(
        "Horas microondas",
        1,
        24,
        1
    )

    pc = st.selectbox(
        "¿Tiene computador?",
        [
            "Sí",
            "No"
        ]
    )

    horas_pc = st.slider(
        "Horas computador",
        1,
        24,
        6
    )

    # =================================================
    # COMPORTAMIENTO
    # =================================================

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
# BOTÓN
# =====================================================

analizar = st.button("⚡ ANALIZAR")

# =====================================================
# ANÁLISIS
# =====================================================

if analizar:

    # =================================================
    # VALIDACIONES
    # =================================================

    if aire == "No":

        cantidad_aires = "0"
        tipo_aire = "Ninguno"
        btu_aire = "0"

    if refrigerador == "No":

        potencia_refri = 0
        corriente_refri = 0
        horas_refri = 0

    if tv == "No":

        horas_tv = 0

    if lavadora == "No":

        horas_lavadora = 0

    if microondas == "No":

        horas_micro = 0

    if pc == "No":

        horas_pc = 0

    # =================================================
    # BTU
    # =================================================

    if btu_aire == "9000":

        potencia_base_aire = 800

    elif btu_aire == "12000":

        potencia_base_aire = 1200

    elif btu_aire == "18000":

        potencia_base_aire = 1800

    elif btu_aire == "24000":

        potencia_base_aire = 2500

    else:

        potencia_base_aire = 0

    # =================================================
    # TIPO DE AIRE
    # =================================================

    if tipo_aire == "Mini Split":

        potencia_base_aire *= 0.90
        fp = 0.90

    elif tipo_aire == "Ventana":

        potencia_base_aire *= 1.15
        fp = 0.80

    elif tipo_aire == "Inverter":

        potencia_base_aire *= 0.70
        fp = 0.95

    elif tipo_aire == "Portátil":

        potencia_base_aire *= 1.25
        fp = 0.75

    else:

        fp = 0.90

    # =================================================
    # HORAS
    # =================================================

    horas_aire_num = valor_numero(horas_aire)
    horas_vent_num = valor_numero(horas_vent)

    # =================================================
    # ILUMINACIÓN
    # =================================================

    if tipo_iluminacion == "LED":

        eficiencia_luz = 0.7

    elif tipo_iluminacion == "Ahorrador":

        eficiencia_luz = 1

    else:

        eficiencia_luz = 1.8

    # =================================================
    # POTENCIAS
    # =================================================

    potencia_aires = (

        valor_numero(cantidad_aires)
        * potencia_base_aire
        * (horas_aire_num / 24)

    )

    potencia_vent = (

        valor_numero(ventiladores)
        * 80
        * (horas_vent_num / 24)

    )

    potencia_refrigerador = (

        valor_numero(refrigerador)
        * potencia_refri
        * (horas_refri / 24)

    )

    potencia_luces = (

        valor_numero(bombillos)
        * potencia_bombillos
        * eficiencia_luz
        * (horas_luces / 24)

    )

    potencia_tv = (

        valor_numero(tv)
        * 90
        * (horas_tv / 24)

    )

    potencia_lavadora = (

        valor_numero(lavadora)
        * 500
        * (horas_lavadora / 24)

    )

    potencia_micro = (

        valor_numero(microondas)
        * 900
        * (horas_micro / 24)

    )

    potencia_pc = (

        valor_numero(pc)
        * 300
        * (horas_pc / 24)

    )

    # =================================================
    # POTENCIA TOTAL
    # =================================================

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
    # CONSUMO PERCIBIDO
    # =================================================

    if consumo_percibido == "Alto":

        factor_consumo = 1.20

    elif consumo_percibido == "Medio":

        factor_consumo = 1

    else:

        factor_consumo = 0.85

    potencia *= factor_consumo

    # =================================================
    # SIMULTANEIDAD
    # =================================================

    factor_simultaneidad = 0.80

    potencia *= factor_simultaneidad

    # =================================================
    # LEY DE OHM
    # =================================================

    voltaje = float(voltaje_aire)

    corriente = potencia / (voltaje * fp)

    # =================================================
    # CORRIENTE TOTAL
    # =================================================

    corriente_total = (

        corriente +
        corriente_refri

    )

    # =================================================
    # ENERGÍA
    # =================================================

    energia_aires = (

        potencia_base_aire
        * horas_aire_num
        * 30
        * valor_numero(cantidad_aires)

    ) / 1000

    energia_vent = (

        80
        * horas_vent_num
        * 30
        * valor_numero(ventiladores)

    ) / 1000

    energia_refri = (

        potencia_refri
        * horas_refri
        * 30

    ) / 1000

    energia_luces = (

        potencia_bombillos
        * horas_luces
        * 30
        * valor_numero(bombillos)

    ) / 1000

    energia_tv = (

        90
        * horas_tv
        * 30
        * valor_numero(tv)

    ) / 1000

    energia_lavadora = (

        500
        * horas_lavadora
        * 30
        * valor_numero(lavadora)

    ) / 1000

    energia_micro = (

        900
        * horas_micro
        * 30
        * valor_numero(microondas)

    ) / 1000

    energia_pc = (

        300
        * horas_pc
        * 30
        * valor_numero(pc)

    ) / 1000

    energia = (

        energia_aires +
        energia_vent +
        energia_refri +
        energia_luces +
        energia_tv +
        energia_lavadora +
        energia_micro +
        energia_pc

    )

    # =================================================
    # RESISTENCIA
    # =================================================

    if problemas == "Frecuentes":

        resistencia = 0.30

    elif problemas == "Sí, a veces":

        resistencia = 0.20

    else:

        resistencia = 0.15

    # =================================================
    # EFECTO JOULE
    # =================================================

    joule = (

        corriente_total ** 2

    ) * resistencia

    # =================================================
    # LEY DE AMPÈRE / BIOT-SAVART
    # =================================================

    mu0 = 4 * math.pi * (10**-7)

    distancia = 0.10

    campo = (

        mu0 * corriente_total

    ) / (

        2 * math.pi * distancia

    )

    # =================================================
    # DENSIDAD
    # =================================================

    area_cable = 3.31e-6

    densidad = (

        corriente_total / area_cable

    )

    # =================================================
    # RIESGO
    # =================================================

    if (

        corriente_total > 30
        or joule > 120
        or densidad > 9000000

    ):

        riesgo = "MUY ALTO"

    elif (

        corriente_total > 20
        or joule > 80
        or densidad > 6000000

    ):

        riesgo = "ALTO"

    elif (

        corriente_total > 10
        or joule > 40
        or densidad > 3000000

    ):

        riesgo = "MEDIO"

    else:

        riesgo = "BAJO"

    # =================================================
    # GUARDAR
    # =================================================

    cursor.execute("""

    INSERT INTO encuestas VALUES(

    NULL,

    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,
    ?,?,?,?,
    ?,?,
    ?,?,
    ?,?,
    ?,?,
    ?,?,

    ?,?,?,?,?,?,?,?

    )

    """, (

        torre,
        personas,
        habitacion,

        aire,
        cantidad_aires,
        tipo_aire,
        btu_aire,
        voltaje_aire,
        horas_aire,

        ventiladores,
        horas_vent,

        refrigerador,
        potencia_refri,
        voltaje_refri,
        corriente_refri,
        horas_refri,

        bombillos,
        tipo_iluminacion,
        potencia_bombillos,
        horas_luces,

        tv,
        horas_tv,

        lavadora,
        horas_lavadora,

        microondas,
        horas_micro,

        pc,
        horas_pc,

        consumo_percibido,
        problemas,

        potencia,
        corriente_total,
        energia,
        joule,
        campo,
        densidad,
        fp,

        riesgo

    ))

    conexion.commit()

    # =================================================
    # RESULTADOS
    # =================================================

    st.success("✅ Encuesta registrada")

    st.markdown("---")

    c1,c2,c3 = st.columns(3)

    c1.metric(
        "⚡ Potencia Total",
        f"{potencia:.2f} W"
    )

    c2.metric(
        "🔌 Corriente Total",
        f"{corriente_total:.2f} A"
    )

    c3.metric(
        "⚠ Riesgo",
        riesgo
    )

    c4,c5,c6 = st.columns(3)

    c4.metric(
        "🔥 Pérdidas Joule",
        f"{joule:.2f} W"
    )

    c5.metric(
        "🧲 Campo Magnético",
        f"{campo:.10f} T"
    )

    c6.metric(
        "⚡ Energía Mensual",
        f"{energia:.2f} kWh"
    )

    c7,c8 = st.columns(2)

    c7.metric(
        "FP",
        f"{fp:.2f}"
    )

    c8.metric(
        "⚡ Densidad Corriente",
        f"{densidad:.2f}"
    )

    # =================================================
    # ALERTAS
    # =================================================

    if joule > 80:

        st.error(
            "⚠ Riesgo térmico elevado"
        )

    if corriente_total > 25:

        st.warning(
            "⚠ Corriente elevada"
        )

    if densidad > 6000000:

        st.warning(
            "⚠ Alta densidad de corriente"
        )

    # =================================================
    # CONCLUSIÓN
    # =================================================

    if riesgo == "MUY ALTO":

        st.error("""

        El apartamento presenta
        un riesgo eléctrico muy alto.

        """)

    elif riesgo == "ALTO":

        st.warning("""

        El apartamento presenta
        un consumo elevado.

        """)

    elif riesgo == "MEDIO":

        st.info("""

        El apartamento presenta
        un comportamiento moderado.

        """)

    else:

        st.success("""

        El apartamento presenta
        condiciones eléctricas estables.

        """)

    # =================================================
    # GRÁFICAS
    # =================================================

    st.markdown("---")

    st.subheader("📊 Distribución Consumo")

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
    # PIE
    # =================================================

    consumos_filtrados = []
    equipos_filtrados = []

    for e,c in zip(equipos, consumos):

        if c > 0:

            equipos_filtrados.append(e)
            consumos_filtrados.append(c)

    fig2, ax2 = plt.subplots(figsize=(7,7))

    ax2.pie(
        consumos_filtrados,
        labels=equipos_filtrados,
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
# ESTADÍSTICAS AVANZADAS
# =====================================================

st.markdown("---")

st.subheader("📈 Estadísticas Avanzadas")

if len(datos) > 0:

    promedio_potencia = datos["potencia"].mean()
    promedio_corriente = datos["corriente"].mean()
    promedio_energia = datos["energia"].mean()
    promedio_joule = datos["joule"].mean()

    mediana_potencia = datos["potencia"].median()

    desviacion_potencia = datos["potencia"].std()

    max_corriente = datos["corriente"].max()

    apto_critico = datos.loc[
        datos["potencia"].idxmax()
    ]

    e1,e2,e3 = st.columns(3)

    e1.metric(
        "⚡ Promedio Potencia",
        f"{promedio_potencia:.2f} W"
    )

    e2.metric(
        "🔌 Promedio Corriente",
        f"{promedio_corriente:.2f} A"
    )

    e3.metric(
        "⚡ Promedio Energía",
        f"{promedio_energia:.2f} kWh"
    )

    e4,e5,e6 = st.columns(3)

    e4.metric(
        "🔥 Promedio Joule",
        f"{promedio_joule:.2f} W"
    )

    e5.metric(
        "⚡ Mediana Potencia",
        f"{mediana_potencia:.2f} W"
    )

    e6.metric(
        "📊 Desv. Potencia",
        f"{desviacion_potencia:.2f}"
    )

    # =================================================
    # COMPARACIÓN
    # =================================================

    if analizar:

        diferencia = (
            (
                potencia - promedio_potencia
            ) / promedio_potencia
        ) * 100

        if diferencia > 0:

            st.warning(f"""

            ⚠ Tu apartamento consume
            {diferencia:.2f}% MÁS
            que el promedio.

            """)

        else:

            st.success(f"""

            ✅ Tu apartamento consume
            {abs(diferencia):.2f}% MENOS
            que el promedio.

            """)

    # =================================================
    # RIESGO
    # =================================================

    st.markdown("---")

    st.subheader("⚠ Distribución Riesgo")

    riesgo_count = datos["riesgo"].value_counts()

    fig4, ax4 = plt.subplots(figsize=(7,5))

    ax4.bar(
        riesgo_count.index,
        riesgo_count.values
    )

    st.pyplot(fig4)

    # =================================================
    # TORRES
    # =================================================

    st.markdown("---")

    st.subheader("🏢 Consumo por Torre")

    promedio_torres = datos.groupby(
        "torre"
    )["potencia"].mean()

    fig5, ax5 = plt.subplots(figsize=(8,5))

    ax5.bar(
        promedio_torres.index,
        promedio_torres.values
    )

    st.pyplot(fig5)

    torre_critica = promedio_torres.idxmax()

    st.error(f"""

    ⚠ Torre con mayor consumo promedio:

    {torre_critica}

    """)

    # =================================================
    # JOULE POR TORRE
    # =================================================

    st.markdown("---")

    st.subheader("🔥 Joule por Torre")

    joule_torre = datos.groupby(
        "torre"
    )["joule"].mean()

    fig6, ax6 = plt.subplots(figsize=(8,5))

    ax6.bar(
        joule_torre.index,
        joule_torre.values
    )

    st.pyplot(fig6)

    # =================================================
    # HISTOGRAMA
    # =================================================

    st.markdown("---")

    st.subheader("📈 Distribución Potencias")

    fig7, ax7 = plt.subplots(figsize=(9,5))

    ax7.hist(
        datos["potencia"],
        bins=10
    )

    st.pyplot(fig7)

    # =================================================
    # APTO CRÍTICO
    # =================================================

    st.markdown("---")

    st.subheader("🚨 Apartamento Más Crítico")

    st.write(f"""

    Torre:
    {apto_critico['torre']}

    Potencia:
    {apto_critico['potencia']:.2f} W

    Corriente:
    {apto_critico['corriente']:.2f} A

    Energía:
    {apto_critico['energia']:.2f} kWh

    Riesgo:
    {apto_critico['riesgo']}

    """)

# =====================================================
# EXPORTAR EXCEL
# =====================================================

if st.button("📥 GENERAR EXCEL"):

    datos.to_excel(
        "ReporteEnergetico.xlsx",
        index=False
    )

    st.success("✅ Excel generado")