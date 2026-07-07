import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# ==========================================
# CONFIGURACIÓN GLOBAL Y CONSTANTES
# ==========================================
AZUL_CL = '#5b8db8'
AZUL_OS = '#2c5f8a'
PALETA_CORP = [AZUL_OS, AZUL_CL, '#8cb8d9', '#193f61']

BASE_DIR = Path(__file__).parent

# ==========================================
# CARGA Y PREPROCESAMIENTO DE DATOS
# ==========================================
df_base = pd.read_csv(BASE_DIR / "citas_2025_metropolitan_limpio.csv")
df_base = df_base.drop(['ID_cit'], axis=1, errors='ignore')
df_base['fechacit'] = pd.to_datetime(df_base['fechacit'])
df_base['mes'] = df_base['fechacit'].dt.to_period('M').astype(str)

# ==========================================
# PROCESAMIENTO DE MÉTRICAS (KPIs)
# ==========================================
def get_kpis(df):
    if df.empty:
        return {"ingresos": "$0.00", "citas": "0", "tasa_cancelacion": "0.00%", "ticket_promedio": "$0.00"}

    df_completadas = df[df['estado'] == 'Completada']
    total_ingresos = df_completadas['totalpagado'].sum() if not df_completadas.empty else 0
    total_citas = len(df)

    canceladas = len(df[df['estado'] == 'Cancelada'])
    tasa_cancelacion = (canceladas / total_citas) * 100 if total_citas > 0 else 0

    ticket_promedio = (total_ingresos / len(df_completadas)) if not df_completadas.empty else 0

    return {
        "ingresos": f"${total_ingresos:,.2f}",
        "citas": f"{total_citas:,}",
        "tasa_cancelacion": f"{tasa_cancelacion:.2f}%",
        "ticket_promedio": f"${ticket_promedio:,.2f}"
    }

# ==========================================
# GRÁFICOS DE ESTADO Y CANCELACIONES
# ==========================================
def get_fig_distribucion_estado(df):
    counts = df['estado'].value_counts().reset_index()
    counts.columns = ['estado', 'cantidad']

    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}]],
                        subplot_titles=("Comparativa", "Proporción"))
    fig.add_trace(
        go.Bar(x=counts['estado'], y=counts['cantidad'], marker_color=[AZUL_CL, AZUL_OS], text=counts['cantidad'],
               textposition='outside', name="Volumen"), row=1, col=1)
    fig.add_trace(go.Pie(labels=counts['estado'], values=counts['cantidad'], marker=dict(colors=[AZUL_CL, AZUL_OS]),
                         textinfo='label+percent', name="Proporción"), row=1, col=2)
    fig.update_layout(title_text="Completados vs Cancelados", showlegend=False)
    return fig


def get_fig_tasa_cancelacion(df):
    if df.empty:
        return px.bar(title='Tasa de Cancelación por Sucursal (%)')

    estado_sucursal = df.groupby(['sucursal', 'estado']).size().reset_index(name='cantidad')
    total_sucursal = df.groupby('sucursal').size().reset_index(name='total')
    merged = pd.merge(estado_sucursal, total_sucursal, on='sucursal')

    merged['tasa'] = (merged['cantidad'] / merged['total']) * 100
    df_canceladas = merged[merged['estado'] == 'Cancelada']

    if df_canceladas.empty:
        df_canceladas = total_sucursal.copy()
        df_canceladas['tasa'] = 0.0

    fig = px.bar(
        df_canceladas, x='sucursal', y='tasa',
        color_discrete_sequence=[AZUL_OS],
        title='Tasa de Cancelación por Sucursal (%)',
        labels={'sucursal': 'Sucursal', 'tasa': 'Tasa de Cancelación (%)'}
    )

    max_y = df_canceladas['tasa'].max()
    max_y = 100 if pd.isna(max_y) else max(max_y + 5, 20)
    fig.update_yaxes(range=[0, max_y])

    return fig

# ==========================================
# GRÁFICOS DE VOLUMEN Y ANÁLISIS DE PACIENTES
# ==========================================
def get_fig_pacientes_mes(df):
    pacientes_mes = df.groupby('mes').size().reset_index(name='cantidad')
    return px.line(pacientes_mes, x='mes', y='cantidad', markers=True, color_discrete_sequence=[AZUL_OS],
                   title='Volumen Total de Pacientes Atendidos por Mes',
                   labels={'mes': 'Mes', 'cantidad': 'Cantidad de Citas'})

def get_fig_frecuencia_pacientes(df):
    if df.empty: return px.histogram(title='Distribución de Recurrencia de Pacientes')
    visitas = df.groupby('paciente').size().reset_index(name='frecuencia')
    max_val = visitas['frecuencia'].max()
    max_bins = int(max_val) if pd.notna(max_val) else 10
    fig = px.histogram(visitas, x='frecuencia', nbins=max_bins, color_discrete_sequence=[AZUL_CL],
                       title='Distribución de Recurrencia de Pacientes', labels={'frecuencia': 'Número de Visitas'})
    fig.update_layout(yaxis_title="Frecuencia (Cantidad de Pacientes)", bargap=0.1)
    return fig


# ==========================================
# GRÁFICOS RENDIMIENTO DE SUCURSALES (FINANCIERO)
# ==========================================
def get_fig_ingresos_sucursal(df):
    df_completadas = df[df['estado'] == 'Completada']
    ingresos = df_completadas.groupby('sucursal')['totalpagado'].sum().reset_index().sort_values('totalpagado')
    return px.bar(ingresos, x='totalpagado', y='sucursal', orientation='h', color_discrete_sequence=[AZUL_CL],
                  title='Ingresos Totales por Sucursal',
                  labels={'totalpagado': 'Ingreso Total ($)', 'sucursal': 'Sucursal'})


def get_fig_proporcion_pago(df):
    df_completadas = df[df['estado'] == 'Completada']
    pagos_agrupados = df_completadas.groupby('sucursal')[['pagopaciente', 'pagoaseguradora']].sum().reset_index()
    pagos_melted = pagos_agrupados.melt(id_vars='sucursal', var_name='origen_pago', value_name='monto')
    return px.bar(pagos_melted, x='sucursal', y='monto', color='origen_pago', barmode='stack',
                  color_discrete_sequence=[AZUL_CL, AZUL_OS], title='Composición de Ingresos: Paciente vs. Aseguradora',
                  labels={'sucursal': 'Sucursal', 'monto': 'Total Pagado ($)', 'origen_pago': 'Origen del Pago'})

def get_fig_evolucion_financiera(df):
    df_completadas = df[df['estado'] == 'Completada']
    ingresos_mes = df_completadas.groupby('mes')['totalpagado'].sum().reset_index()
    return px.line(ingresos_mes, x='mes', y='totalpagado', markers=True, color_discrete_sequence=['#d62728'],
                   title='Tendencia de Ingresos Mensuales', labels={'mes': 'Mes', 'totalpagado': 'Ingreso Total ($)'})

def get_fig_boxplot_citas(df):
    df_completadas = df[df['estado'] == 'Completada']
    fig = px.box(df_completadas, x='sucursal', y='totalpagado', color='sucursal', color_discrete_sequence=PALETA_CORP,
                 title='Dispersión y Valores Atípicos del Costo de Citas',
                 labels={'sucursal': 'Sucursal', 'totalpagado': 'Total Pagado ($)'})
    fig.update_traces(showlegend=False)
    return fig


# ==========================================
# GRÁFICOS RENDIMIENTO DE MÉDICOS
# ==========================================
def get_fig_top_doctores(df):
    doctores_top = df['doctor'].value_counts().nlargest(20).iloc[::-1].reset_index()
    doctores_top.columns = ['doctor', 'pacientes']
    fig = px.bar(doctores_top, x='doctor', y='pacientes', title='Pacientes atendidos por doctor (TOP 20)',
                 labels={'doctor': 'Doctores', 'pacientes': 'Número de pacientes'}, color_discrete_sequence=['skyblue'])
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def get_fig_top_ingresos_doctores(df):
    df_completadas = df[df['estado'] == 'Completada']
    top_ingresos = df_completadas.groupby('doctor')['totalpagado'].sum().nlargest(10).reset_index().sort_values(
        'totalpagado')
    return px.bar(top_ingresos, x='totalpagado', y='doctor', orientation='h', color_discrete_sequence=['#2ca02c'],
                  title='Top 10 Doctores por Recaudación Total',
                  labels={'totalpagado': 'Total Recaudado ($)', 'doctor': 'Doctor'})


# ==========================================
# GEOLOCALIZACIÓN Y MAPAS
# ==========================================
def get_fig_mapa_sucursales(df_filtrado):
    if df_filtrado.empty:
        return px.scatter_map(title="Expansión Geográfica de Pacientes por Sucursal y Mes")

    df_mapa = df_filtrado.groupby(['mes', 'sucursal']).size().reset_index(name='cantidad')

    df_mapa['cantidad_ajustada'] = df_mapa['cantidad'] ** 1.5

    ubicaciones_reales = {
        "PMM BELLA VISTA": {"lat": 8.9818, "lon": -79.5221},
        "PMM CLAYTON": {"lat": 9.0063, "lon": -79.5841},
        "PMM COSTA DEL ESTE": {"lat": 9.0084, "lon": -79.4673},
        "PMM EL DORADO": {"lat": 9.0062, "lon": -79.5342},
        "PMM PUNTA PACIFICA": {"lat": 8.9745, "lon": -79.5085},
        "PMM SAN FRANCISCO": {"lat": 8.9875, "lon": -79.5050}
    }

    def obtener_coordenadas(nombre_sucursal, indice):
        nombre_limpio = str(nombre_sucursal).strip().upper()
        if nombre_limpio in ubicaciones_reales: return ubicaciones_reales[nombre_limpio]
        offset_lat, offset_lon = (indice % 5) * 0.02, (indice % 4) * 0.02
        return {"lat": 8.9900 + offset_lat, "lon": -79.5200 + offset_lon}

    sucursales_unicas = df_mapa['sucursal'].unique()
    mapa_coords = {suc: obtener_coordenadas(suc, i) for i, suc in enumerate(sucursales_unicas)}

    df_mapa['lat'] = df_mapa['sucursal'].map(lambda x: mapa_coords[x]['lat'])
    df_mapa['lon'] = df_mapa['sucursal'].map(lambda x: mapa_coords[x]['lon'])
    df_mapa = df_mapa.sort_values('mes')

    fig_mapa = px.scatter_map(
        df_mapa, lat="lat", lon="lon", color="sucursal",
        size="cantidad_ajustada", 
        animation_frame="mes", hover_name="sucursal",
        hover_data={"lat": False, "lon": False, "cantidad": True, "mes": False, "cantidad_ajustada": False},
        size_max=70, zoom=11.5, map_style="carto-darkmatter",
        title="Expansión Geográfica de Pacientes por Sucursal y Mes"
    )

    fig_mapa.update_traces(marker=dict(opacity=0.7))

    return fig_mapa