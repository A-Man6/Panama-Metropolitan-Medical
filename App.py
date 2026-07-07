from flask import Flask
from dash import Dash, html, dcc, Input, Output
import Analysis
import plotly.graph_objects as go

server = Flask(__name__)

app = Dash(
    __name__,
    server=server,
)

# ==========================================
# Variables de Estilo Globales
# ==========================================
GRADIENT_BG = 'linear-gradient(to bottom, #0b1116 0%, #121212 50%, #193f61 100%)'
CARD_BG_TRANSLUCENT = 'rgba(30, 30, 30, 0.75)'
TEXT_COLOR = '#e0e0e0'
ACCENT_COLOR = '#5b8db8'
FONT_FAMILY = 'Arial, sans-serif'

card_style = {
    'backgroundColor': CARD_BG_TRANSLUCENT,
    'borderRadius': '12px',
    'padding': '20px',
    'boxShadow': '0 8px 24px rgba(0, 0, 0, 0.5)',
    'border': '1px solid rgba(255, 255, 255, 0.05)',
    'backdropFilter': 'blur(10px)',
    'display': 'flex',
    'flexDirection': 'column'
}

# Estilos de KPIs compactados
kpi_card_style = {
    **card_style,
    'alignItems': 'center',
    'justifyContent': 'center',
    'textAlign': 'center',
    'padding': '15px 10px'
}
kpi_title_style = {'fontSize': '14px', 'color': '#a0a0a0', 'marginBottom': '8px', 'fontWeight': 'bold',
                   'textTransform': 'uppercase'}
kpi_value_style = {'fontSize': '26px', 'color': ACCENT_COLOR, 'fontWeight': 'bold', 'margin': '0'} 

# Estilo de Sección más resaltante
section_title_style = {
    'color': ACCENT_COLOR,
    'borderBottom': f'2px solid rgba(91, 141, 184, 0.3)',
    'paddingBottom': '10px',
    'marginBottom': '25px',
    'marginTop': '40px',
    'fontWeight': 'bold',
    'fontSize': '28px',
    'letterSpacing': '1px',
    'textShadow': '1px 1px 4px rgba(0,0,0,0.5)'
}

grid_style = {
    'display': 'grid',
    'gridTemplateColumns': 'repeat(auto-fit, minmax(500px, 1fr))',
    'gap': '25px',
    'marginBottom': '25px',
    'position': 'relative',
    'zIndex': '1'
}

# ==========================================
# Layout del Dashboard
# ==========================================
app.layout = html.Div(style={
    'backgroundImage': GRADIENT_BG,
    'backgroundAttachment': 'fixed',
    'color': TEXT_COLOR,
    'fontFamily': FONT_FAMILY,
    'minHeight': '100vh',
    'display': 'flex',
    'flexDirection': 'column',
    'margin': '0',
    'padding': '0'
}, children=[

    # ENCABEZADO
    html.Div(style={
        'padding': '40px 5% 10px 5%',
        'zIndex': '10',
        'position': 'relative',
    }, children=[
        html.H1("Dashboard Gerencial - Clínica Metropolitana",
                style={'textAlign': 'center', 'fontWeight': 'bold', 'margin': '0 0 10px 0', 'color': '#ffffff',
                       'textShadow': '0px 2px 4px rgba(0,0,0,0.6)'}),
        html.P("Análisis Operativo y Financiero",
               style={'textAlign': 'center', 'color': ACCENT_COLOR, 'fontSize': '18px', 'margin': '0',
                      'fontWeight': 'bold'}),
    ]),

    # CUERPO DEL DASHBOARD
    html.Div(style={
        'flexGrow': '1',
        'padding': '20px 5% 40px 5%',
        'boxSizing': 'border-box'
    }, children=[

        # FILTROS
        html.Div(style={
            'display': 'flex', 'gap': '30px', 'justifyContent': 'center',
            'marginBottom': '30px', 'flexWrap': 'wrap',
            'position': 'relative', 'zIndex': '1000'
        }, children=[
            html.Div([
                html.Label("📍 Filtro por Sucursal:",
                           style={'fontWeight': 'bold', 'marginBottom': '10px', 'display': 'block'}),
                dcc.Dropdown(
                    id="dropdown-sucursal",
                    options=[{"label": "Todas", "value": "Todas"}] +
                            [{"label": s, "value": s} for s in sorted(Analysis.df_base["sucursal"].dropna().unique())],
                    value="Todas", clearable=False, style={'color': '#000', 'fontFamily': FONT_FAMILY}
                )
            ], style={'width': '300px', **card_style, 'padding': '15px'}),

            html.Div([
                html.Label("📋 Filtro por Estado:",
                           style={'fontWeight': 'bold', 'marginBottom': '10px', 'display': 'block'}),
                dcc.Dropdown(
                    id="dropdown-estado",
                    options=[
                        {"label": "Todos", "value": "Todos"},
                        {"label": "Completada", "value": "Completada"},
                        {"label": "Cancelada", "value": "Cancelada"}
                    ],
                    value="Todos", clearable=False, style={'color': '#000', 'fontFamily': FONT_FAMILY}
                )
            ], style={'width': '300px', **card_style, 'padding': '15px'}),
        ]),

        # KPIs
        html.Div(style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
            'gap': '20px',
            'marginBottom': '40px',
            'position': 'relative',
            'zIndex': '1'
        }, children=[
            html.Div([
                html.P("Ingresos Totales", style=kpi_title_style),
                html.H3(id="kpi-ingresos", style=kpi_value_style)
            ], style=kpi_card_style),
            html.Div([
                html.P("Total de Citas", style=kpi_title_style),
                html.H3(id="kpi-citas", style=kpi_value_style)
            ], style=kpi_card_style),
            html.Div([
                html.P("Ticket Promedio", style=kpi_title_style),
                html.H3(id="kpi-ticket", style=kpi_value_style)
            ], style=kpi_card_style),
            html.Div([
                html.P("Tasa de Cancelación", style=kpi_title_style),
                html.H3(id="kpi-cancelacion", style=kpi_value_style)
            ], style=kpi_card_style),
        ]),

        # SECCIÓN 1: Operativa
        html.H3("1. Visión General y Tráfico Operativo", style=section_title_style),
        html.Div(style=grid_style, children=[
            html.Div([dcc.Graph(id="grafica-pacientes-mes")], style=card_style),
            html.Div([dcc.Graph(id="grafica-dist-estado")], style=card_style),
            html.Div([dcc.Graph(id="grafica-tasa-cancelacion")], style=card_style),
            html.Div([dcc.Graph(id="grafica-frecuencia-pacientes")], style=card_style),
        ]),

        # MAPA GEOGRÁFICO
        html.Div([
            dcc.Graph(id="grafica-pacientes-sucursal-mes", style={'height': '700px'})
        ], style={**card_style, 'marginBottom': '40px', 'position': 'relative', 'zIndex': '1'}),

        # SECCIÓN 2: Financiera
        html.H3("2. Desempeño Financiero", style=section_title_style),
        html.Div(style=grid_style, children=[
            html.Div([dcc.Graph(id="grafica-evolucion-financiera")], style=card_style),
            html.Div([dcc.Graph(id="grafica-ingresos-sucursal")], style=card_style),
            html.Div([dcc.Graph(id="grafica-proporcion-pago")], style=card_style),
            html.Div([dcc.Graph(id="grafica-boxplot-citas")], style=card_style),
        ]),

        # SECCIÓN 3: Médica
        html.H3("3. Rendimiento del Personal Médico", style=section_title_style),
        html.Div(style=grid_style, children=[
            html.Div([dcc.Graph(id="grafica-top-doctores")], style=card_style),
            html.Div([dcc.Graph(id="grafica-top-ingresos-doctores")], style=card_style),
        ]),

    ])
])


# ==========================================
# Callback Principal de Renderizado
# ==========================================
@app.callback(
    Output("kpi-ingresos", "children"),
    Output("kpi-citas", "children"),
    Output("kpi-ticket", "children"),
    Output("kpi-cancelacion", "children"),

    Output("grafica-dist-estado", "figure"),
    Output("grafica-tasa-cancelacion", "figure"),
    Output("grafica-pacientes-mes", "figure"),
    Output("grafica-pacientes-sucursal-mes", "figure"),
    Output("grafica-frecuencia-pacientes", "figure"),
    Output("grafica-top-doctores", "figure"),
    Output("grafica-top-ingresos-doctores", "figure"),
    Output("grafica-ingresos-sucursal", "figure"),
    Output("grafica-proporcion-pago", "figure"),
    Output("grafica-evolucion-financiera", "figure"),
    Output("grafica-boxplot-citas", "figure"),

    Input("dropdown-sucursal", "value"),
    Input("dropdown-estado", "value")
)
def actualizar_dashboard(sucursal, estado):
    df_filtrado = Analysis.df_base.copy()

    if sucursal.upper() != "TODAS":
        df_filtrado = df_filtrado[df_filtrado["sucursal"].str.upper() == sucursal.upper()]
    if estado.upper() != "TODOS":
        df_filtrado = df_filtrado[df_filtrado["estado"].str.upper() == estado.upper()]

    kpis = Analysis.get_kpis(df_filtrado)

    # UNIFORMIDAD DE TÍTULOS: Se establece un estilo de fuente consistente y centrado para todos los gráficos
    dark_layout_updates = {
        'template': 'plotly_dark',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': TEXT_COLOR, 'family': FONT_FAMILY},
        'margin': dict(t=70, b=40, l=40, r=20),
        'title': dict(
            font=dict(size=22, family=FONT_FAMILY, color='#ffffff'),
            x=0.5,
            xanchor='center'
        )
    }

    if df_filtrado.empty:
        fig_vacia = go.Figure().update_layout(title="Sin datos para esta selección", **dark_layout_updates)
        return (
            kpis["ingresos"], kpis["citas"], kpis["ticket_promedio"], kpis["tasa_cancelacion"],
            *([fig_vacia] * 11)
        )

    figuras = [
        Analysis.get_fig_distribucion_estado(df_filtrado),
        Analysis.get_fig_tasa_cancelacion(df_filtrado),
        Analysis.get_fig_pacientes_mes(df_filtrado),
        Analysis.get_fig_mapa_sucursales(df_filtrado),
        Analysis.get_fig_frecuencia_pacientes(df_filtrado),
        Analysis.get_fig_top_doctores(df_filtrado),
        Analysis.get_fig_top_ingresos_doctores(df_filtrado),
        Analysis.get_fig_ingresos_sucursal(df_filtrado),
        Analysis.get_fig_proporcion_pago(df_filtrado),
        Analysis.get_fig_evolucion_financiera(df_filtrado),
        Analysis.get_fig_boxplot_citas(df_filtrado)
    ]

    for fig in figuras:
        fig.update_layout(**dark_layout_updates)

    return (
        kpis["ingresos"],
        kpis["citas"],
        kpis["ticket_promedio"],
        kpis["tasa_cancelacion"],
        *figuras
    )

if __name__ == "__main__":
    app.run(debug=True)