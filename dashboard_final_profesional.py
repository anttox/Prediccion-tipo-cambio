import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================
# CONFIGURACIÓN PROFESIONAL - MODO OSCURO
# ============================================

st.set_page_config(
    page_title="Predicción USD/PEN - Twitter Sentiment Analysis",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de colores profesional para fondo oscuro
COLORES = {
    'fondo': '#0f1116',
    'fondo_cards': '#1a1d29',
    'fondo_sidebar': '#161a25',
    'texto': '#ffffff',
    'texto_secundario': '#a0a4b3',
    'primario': '#4a6fff',
    'primario_suave': '#6b8aff',
    'exito': '#2dc76d',
    'exito_suave': '#34d178',
    'error': '#ff4757',
    'error_suave': '#ff6b81',
    'advertencia': '#ffa502',
    'neutro': '#747d8c',
    'bordes': '#2a2f3d'
}

# Estilos CSS optimizados para modo oscuro
st.markdown(f"""
<style>
    /* Fondo principal */
    .stApp {{
        background-color: {COLORES['fondo']};
        color: {COLORES['texto']};
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {COLORES['fondo_sidebar']};
        border-right: 1px solid {COLORES['bordes']};
    }}

    /* Títulos mejorados */
    .titulo-principal {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {COLORES['texto']};
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, {COLORES['primario']}, {COLORES['primario_suave']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.3;
        letter-spacing: -0.5px;
    }}

    .subtitulo {{
        font-size: 0.95rem;
        color: {COLORES['texto_secundario']};
        margin-bottom: 1.5rem;
        font-weight: 400;
        line-height: 1.5;
    }}

    /* Tarjetas de métricas - Diseño moderno */
    .metric-card {{
        background: {COLORES['fondo_cards']};
        border-radius: 10px;
        padding: 1.2rem;
        border: 1px solid {COLORES['bordes']};
        transition: all 0.3s ease;
        height: 100%;
    }}

    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(74, 111, 255, 0.15);
        border-color: {COLORES['primario']};
    }}

    .metric-title {{
        font-size: 0.85rem;
        color: {COLORES['texto_secundario']};
        margin-bottom: 0.5rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .metric-value {{
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        color: {COLORES['texto']};
    }}

    .metric-subtext {{
        font-size: 0.8rem;
        color: {COLORES['texto_secundario']};
    }}

    /* Sidebar mejorado */
    .sidebar-section {{
        background: {COLORES['fondo_cards']};
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid {COLORES['bordes']};
    }}

    .sidebar-section-title {{
        font-size: 0.9rem;
        font-weight: 600;
        color: {COLORES['primario']};
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .sidebar-help {{
        font-size: 0.75rem;
        color: {COLORES['texto_secundario']};
        font-style: italic;
        margin-top: 0.3rem;
        line-height: 1.3;
    }}

    /* Pestañas */
    .stTabs {{
        margin-top: 1rem;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background-color: {COLORES['fondo']};
        padding: 5px;
        border-radius: 8px;
        border: 1px solid {COLORES['bordes']};
    }}

    .stTabs [data-baseweb="tab"] {{
        background-color: {COLORES['fondo_cards']};
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 500;
        color: {COLORES['texto_secundario']};
        border: 1px solid transparent;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {COLORES['primario']} !important;
        color: {COLORES['texto']} !important;
        border-color: {COLORES['primario']} !important;
    }}

    /* Botones */
    .stButton>button {{
        background-color: {COLORES['primario']};
        color: {COLORES['texto']};
        border: none;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.3s ease;
    }}

    .stButton>button:hover {{
        background-color: {COLORES['primario_suave']};
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(74, 111, 255, 0.3);
    }}

    /* Métricas del sidebar */
    .sidebar-metric {{
        background: linear-gradient(135deg, {COLORES['fondo_cards']}, {COLORES['fondo_sidebar']});
        padding: 0.8rem;
        border-radius: 6px;
        text-align: center;
        border: 1px solid {COLORES['bordes']};
        margin-bottom: 0.5rem;
    }}

    .sidebar-metric-label {{
        font-size: 0.7rem;
        color: {COLORES['texto_secundario']};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }}

    .sidebar-metric-value {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {COLORES['texto']};
    }}
    
    /* Manual de usuario compacto */
    .help-banner {{
        background: linear-gradient(135deg, {COLORES['fondo_cards']}, {COLORES['fondo_sidebar']});
        border: 1px solid {COLORES['primario']};
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }}
    
    .help-icon {{
        display: inline-block;
        width: 24px;
        height: 24px;
        background: {COLORES['primario']};
        border-radius: 50%;
        text-align: center;
        line-height: 24px;
        color: white;
        font-weight: bold;
        margin-right: 8px;
    }}
    
    .step-card {{
        background: {COLORES['fondo']};
        border-radius: 6px;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        border-left: 3px solid {COLORES['primario']};
    }}
    
    .step-number {{
        display: inline-block;
        background: {COLORES['primario']};
        color: white;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        text-align: center;
        line-height: 22px;
        font-size: 0.85rem;
        font-weight: bold;
        margin-right: 8px;
    }}
    
    .step-title {{
        color: {COLORES['texto']};
        font-weight: 600;
        font-size: 0.95rem;
    }}
    
    .step-desc {{
        color: {COLORES['texto_secundario']};
        font-size: 0.85rem;
        margin-top: 0.3rem;
        line-height: 1.4;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCIONES DE PROCESAMIENTO DE DATOS
# ============================================

@st.cache_data
def cargar_datos_completos():
    """Carga todos los datos del período completo (abril-mayo 2021)"""
    try:
        # Cargar datos del archivo Excel
        archivo_path = 'tweets_GOZU_SENTIMIENTO_MEJORADO.xlsx'
        df = pd.read_excel(archivo_path, engine='openpyxl')

        # Procesamiento básico
        df['Fecha'] = pd.to_datetime(df['TweetCreateTime']).dt.date
        df = df.dropna(subset=['sentimiento_numerico', 'Compra'])

        # Agrupar por día
        df_daily = df.groupby('Fecha').agg({
            'sentimiento_numerico': 'mean',
            'Compra': 'mean'
        }).reset_index()

        # Ordenar por fecha
        df_daily = df_daily.sort_values('Fecha').reset_index(drop=True)
        df_daily['Fecha'] = pd.to_datetime(df_daily['Fecha'])

        # Filtrar solo período de interés (abril-mayo 2021)
        fecha_inicio = pd.Timestamp('2021-04-01')
        fecha_fin = pd.Timestamp('2021-05-31')
        df_daily = df_daily[(df_daily['Fecha'] >= fecha_inicio) & (df_daily['Fecha'] <= fecha_fin)].copy()

        # Cálculos base
        df_daily['Variacion_Dolar'] = df_daily['Compra'].pct_change() * 100

        # Crear lags para predicción
        df_daily['Sentimiento_Ayer'] = df_daily['sentimiento_numerico'].shift(1)
        df_daily['Cambio_Sentimiento'] = df_daily['Sentimiento_Ayer'].diff()

        # Predicción basada en correlación real (r = -0.26)
        df_daily['Prediccion'] = np.where(
            df_daily['Cambio_Sentimiento'] < 0,  # Si el sentimiento empeoró ayer
            1,   # Predice que hoy el dólar SUBE
            -1   # Predice que hoy el dólar BAJA
        )

        # Realidad
        df_daily['Realidad'] = np.where(
            df_daily['Variacion_Dolar'] > 0,
            1,   # El dólar subió
            -1   # El dólar bajó
        )

        # Calcular aciertos
        df_daily['Acierto'] = df_daily['Prediccion'] == df_daily['Realidad']
        df_daily['Retorno'] = df_daily['Prediccion'] * df_daily['Variacion_Dolar']

        # Métricas acumuladas
        df_daily['Retorno_Acumulado'] = df_daily['Retorno'].cumsum()
        
        # Cargar datos originales para tooltips detallados
        df_daily = agregar_datos_detallados(df_daily, df)

        return df_daily

    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return None

def agregar_datos_detallados(df_daily, df_original):
    """Agrega información detallada de sentimiento para tooltips"""
    
    # Convertir fecha para merge
    df_original['Fecha'] = pd.to_datetime(df_original['TweetCreateTime']).dt.date
    df_original['Fecha'] = pd.to_datetime(df_original['Fecha'])
    
    # Calcular estadísticas por día
    stats_por_dia = df_original.groupby('Fecha').apply(lambda x: pd.Series({
        'total_tweets': len(x),
        'anti_castillo': (x['sentimiento_economico'].str.contains('ANTI_CASTILLO', na=False)).sum(),
        'anti_keiko': (x['sentimiento_economico'].str.contains('ANTI_KEIKO', na=False)).sum(),
        'neutral': (x['sentimiento_economico'] == 'NEUTRAL').sum(),
        'razones_top': x['razones'].mode()[0] if len(x['razones'].mode()) > 0 else 'N/A'
    })).reset_index()
    
    # Merge con datos diarios
    df_daily = df_daily.merge(stats_por_dia, on='Fecha', how='left')
    
    # Calcular porcentajes
    df_daily['pct_anti_castillo'] = (df_daily['anti_castillo'] / df_daily['total_tweets'] * 100).fillna(0)
    df_daily['pct_anti_keiko'] = (df_daily['anti_keiko'] / df_daily['total_tweets'] * 100).fillna(0)
    df_daily['pct_neutral'] = (df_daily['neutral'] / df_daily['total_tweets'] * 100).fillna(0)
    
    # Determinar influencia predominante
    df_daily['influencia_predominante'] = df_daily.apply(lambda row: 
        'Anti-Castillo' if row['pct_anti_castillo'] > row['pct_anti_keiko'] and row['pct_anti_castillo'] > row['pct_neutral']
        else 'Anti-Keiko' if row['pct_anti_keiko'] > row['pct_anti_castillo'] and row['pct_anti_keiko'] > row['pct_neutral']
        else 'Neutral/Mixto', axis=1)
    
    return df_daily

def filtrar_por_fecha(df, fecha_inicio, fecha_fin):
    """Filtra datos por rango de fechas"""
    mask = (df['Fecha'] >= pd.Timestamp(fecha_inicio)) & (df['Fecha'] <= pd.Timestamp(fecha_fin))
    return df[mask].copy()

def filtrar_por_resultado(df, filtro_resultado):
    """Filtra datos por resultado de predicción (acierto o error)"""
    if filtro_resultado == "Todos":
        return df.copy()
    elif filtro_resultado == "Solo Aciertos":
        return df[df['Acierto'] == True].copy()
    elif filtro_resultado == "Solo Errores":
        return df[df['Acierto'] == False].copy()
    return df.copy()

def calcular_metricas(df_filtrado):
    """Calcula métricas para el período filtrado"""
    if len(df_filtrado) == 0:
        return {}

    metricas = {
        'total_dias': len(df_filtrado),
        'precision': df_filtrado['Acierto'].mean() * 100,
        'retorno_total': df_filtrado['Retorno'].sum(),
        'dias_sube': (df_filtrado['Prediccion'] == 1).sum(),
        'dias_baja': (df_filtrado['Prediccion'] == -1).sum(),
        'aciertos': df_filtrado['Acierto'].sum(),
        'aciertos_sube': df_filtrado[(df_filtrado['Prediccion'] == 1) & (df_filtrado['Acierto'])].shape[0],
        'aciertos_baja': df_filtrado[(df_filtrado['Prediccion'] == -1) & (df_filtrado['Acierto'])].shape[0],
    }

    # Precisión por tipo de señal
    if metricas['dias_sube'] > 0:
        metricas['precision_sube'] = (metricas['aciertos_sube'] / metricas['dias_sube']) * 100
    else:
        metricas['precision_sube'] = 0

    if metricas['dias_baja'] > 0:
        metricas['precision_baja'] = (metricas['aciertos_baja'] / metricas['dias_baja']) * 100
    else:
        metricas['precision_baja'] = 0

    return metricas

# ============================================
# FUNCIONES DE VISUALIZACIÓN (MODO OSCURO)
# ============================================

def crear_grafico_principal(df):
    """Gráfico principal del tipo de cambio con predicciones"""
    fig = go.Figure()

    # Línea del tipo de cambio
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['Compra'],
        mode='lines',
        name='Tipo de Cambio',
        line=dict(color=COLORES['primario'], width=3),
        hovertemplate='<b>%{x|%d/%m/%Y}</b><br>S/ %{y:.4f}<extra></extra>'
    ))

    # Marcadores para todos los días
    for idx, row in df.iterrows():
        color = COLORES['exito'] if row['Acierto'] else COLORES['error']
        simbolo = 'triangle-up' if row['Prediccion'] == 1 else 'triangle-down'
        tamaño = 10
        opacidad = 0.8

        fig.add_trace(go.Scatter(
            x=[row['Fecha']], y=[row['Compra']],
            mode='markers',
            marker=dict(
                size=tamaño,
                color=color,
                symbol=simbolo,
                opacity=opacidad,
                line=dict(width=1, color='white')
            ),
            showlegend=False,
            hoverinfo='text',
            hovertext=f"<b>{row['Fecha'].strftime('%d/%m')}</b><br>S/ {row['Compra']:.4f}<br>{'Acierto' if row['Acierto'] else 'Error'} {row['Variacion_Dolar']:+.2f}%"
        ))

    # Layout personalizado para modo oscuro
    fig.update_layout(
        title=dict(
            text='Evolución del Tipo de Cambio USD/PEN con Predicciones',
            font=dict(size=18, color=COLORES['texto']),
            x=0.05
        ),
        xaxis=dict(
            title='Fecha',
            tickformat='%d/%m',
            gridcolor=COLORES['bordes'],
            zerolinecolor=COLORES['bordes'],
            linecolor=COLORES['bordes'],
            tickfont=dict(color=COLORES['texto_secundario'])
        ),
        yaxis=dict(
            title='Tipo de Cambio (Soles por Dólar)',
            gridcolor=COLORES['bordes'],
            zerolinecolor=COLORES['bordes'],
            linecolor=COLORES['bordes'],
            tickfont=dict(color=COLORES['texto_secundario'])
        ),
        hovermode='closest',
        plot_bgcolor=COLORES['fondo'],
        paper_bgcolor=COLORES['fondo'],
        font=dict(color=COLORES['texto']),
        height=500,
        showlegend=True,
        legend=dict(
            bgcolor=COLORES['fondo_cards'],
            bordercolor=COLORES['bordes'],
            borderwidth=1,
            font=dict(color=COLORES['texto'])
        )
    )

    return fig

from plotly.subplots import make_subplots

def crear_grafico_sentimiento_variacion(df):
    """Gráfico combinado de sentimiento y variación del dólar con tooltips detallados"""
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Sentimiento Político Diario', 'Variación del Dólar vs Predicciones'),
        vertical_spacing=0.15
    )

    # Crear texto personalizado para hover con información detallada
    hover_texts = []
    for idx, row in df.iterrows():
        hover_text = (
            f"<b>Fecha:</b> {row['Fecha'].strftime('%d/%m/%Y')}<br>"
            f"<b>Sentimiento:</b> {row['sentimiento_numerico']:.3f}<br>"
            f"<b>Total tweets:</b> {int(row['total_tweets'])}<br>"
            f"<b>Influencia predominante:</b> {row['influencia_predominante']}<br>"
            f"<b>Anti-Castillo:</b> {row['pct_anti_castillo']:.1f}% ({int(row['anti_castillo'])} tweets)<br>"
            f"<b>Anti-Keiko:</b> {row['pct_anti_keiko']:.1f}% ({int(row['anti_keiko'])} tweets)<br>"
            f"<b>Neutral:</b> {row['pct_neutral']:.1f}% ({int(row['neutral'])} tweets)<br>"
            f"<b>Razones principales:</b> {row['razones_top']}"
        )
        hover_texts.append(hover_text)

    # Gráfico 1: Sentimiento con tooltips detallados
    fig.add_trace(
        go.Scatter(
            x=df['Fecha'], 
            y=df['sentimiento_numerico'],
            mode='lines+markers',
            name='Sentimiento',
            line=dict(color=COLORES['primario_suave'], width=2),
            marker=dict(size=6, color=COLORES['primario_suave']),
            fill='tozeroy',
            fillcolor='rgba(107, 138, 255, 0.1)',
            hovertext=hover_texts,
            hoverinfo='text'
        ),
        row=1, col=1
    )

    # Línea de referencia en cero
    fig.add_hline(y=0, line_dash="dash", line_color=COLORES['neutro'], row=1, col=1)

    # Gráfico 2: Variación del dólar coloreada por acierto
    colores_barras = [COLORES['exito'] if a else COLORES['error'] for a in df['Acierto']]

    fig.add_trace(
        go.Bar(
            x=df['Fecha'], y=df['Variacion_Dolar'],
            marker_color=colores_barras,
            name='Variación',
            showlegend=False
        ),
        row=2, col=1
    )

    fig.add_hline(y=0, line_color=COLORES['texto'], line_width=1, row=2, col=1)

    # Actualizar layout
    fig.update_layout(
        height=600,
        plot_bgcolor=COLORES['fondo'],
        paper_bgcolor=COLORES['fondo'],
        font=dict(color=COLORES['texto']),
        showlegend=True,
        legend=dict(
            bgcolor=COLORES['fondo_cards'],
            bordercolor=COLORES['bordes'],
            borderwidth=1
        )
    )

    fig.update_xaxes(
        tickformat='%d/%m',
        gridcolor=COLORES['bordes'],
        tickfont=dict(color=COLORES['texto_secundario']),
        row=1, col=1
    )

    fig.update_xaxes(
        tickformat='%d/%m',
        gridcolor=COLORES['bordes'],
        tickfont=dict(color=COLORES['texto_secundario']),
        row=2, col=1
    )

    fig.update_yaxes(
        title_text='Índice de Sentimiento',
        gridcolor=COLORES['bordes'],
        tickfont=dict(color=COLORES['texto_secundario']),
        row=1, col=1
    )

    fig.update_yaxes(
        title_text='Variación (%)',
        gridcolor=COLORES['bordes'],
        tickfont=dict(color=COLORES['texto_secundario']),
        row=2, col=1
    )

    return fig

def crear_grafico_retorno_acumulado(df):
    """Gráfico de retorno acumulado del modelo"""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['Retorno_Acumulado'],
        mode='lines',
        name='Retorno Acumulado',
        line=dict(color=COLORES['exito'], width=3),
        fill='tozeroy',
        fillcolor='rgba(45, 199, 109, 0.1)'
    ))

    # Línea de referencia en cero
    fig.add_hline(y=0, line_color=COLORES['texto'], line_width=1)

    # Punto final
    if len(df) > 0:
        fig.add_trace(go.Scatter(
            x=[df['Fecha'].iloc[-1]], y=[df['Retorno_Acumulado'].iloc[-1]],
            mode='markers+text',
            marker=dict(size=12, color=COLORES['exito']),
            text=[f"{df['Retorno_Acumulado'].iloc[-1]:+.2f}%"],
            textposition='top right',
            textfont=dict(size=12, color=COLORES['exito']),
            showlegend=False
        ))

    fig.update_layout(
        title=dict(
            text='Retorno Acumulado del Modelo Predictivo',
            font=dict(size=16, color=COLORES['texto'])
        ),
        xaxis=dict(
            title='Fecha',
            tickformat='%d/%m',
            gridcolor=COLORES['bordes'],
            tickfont=dict(color=COLORES['texto_secundario'])
        ),
        yaxis=dict(
            title='Retorno Acumulado (%)',
            gridcolor=COLORES['bordes'],
            tickfont=dict(color=COLORES['texto_secundario'])
        ),
        plot_bgcolor=COLORES['fondo'],
        paper_bgcolor=COLORES['fondo'],
        font=dict(color=COLORES['texto']),
        height=400
    )

    return fig

def crear_grafico_matriz_desempeno(metricas):
    """Gráfico de matriz de desempeño del modelo"""
    # Datos para la matriz
    categorias = ['Predijo SUBE', 'Predijo BAJA']
    precisiones = [metricas['precision_sube'], metricas['precision_baja']]

    # Colores basados en la precisión
    colores = []
    for precision in precisiones:
        if precision >= 70:
            colores.append(COLORES['exito'])
        elif precision >= 50:
            colores.append(COLORES['advertencia'])
        else:
            colores.append(COLORES['error'])

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categorias,
        y=precisiones,
        marker_color=colores,
        text=[f'{p:.1f}%' for p in precisiones],
        textposition='outside',
        textfont=dict(size=14, color=COLORES['texto'])
    ))

    # Líneas de referencia
    fig.add_hline(y=50, line_dash="dash", line_color=COLORES['neutro'],
                 annotation_text="Azar (50%)",
                 annotation_position="top right",
                 annotation_font=dict(color=COLORES['texto_secundario']))

    fig.add_hline(y=60, line_dash="dash", line_color=COLORES['exito_suave'],
                 annotation_text="Bueno (60%)",
                 annotation_position="top right",
                 annotation_font=dict(color=COLORES['exito_suave']))

    fig.update_layout(
        title=dict(
            text='Precisión por Tipo de Predicción',
            font=dict(size=16, color=COLORES['texto'])
        ),
        xaxis=dict(
            title='Tipo de Predicción',
            gridcolor=COLORES['bordes'],
            tickfont=dict(color=COLORES['texto_secundario'])
        ),
        yaxis=dict(
            title='Precisión (%)',
            range=[0, 100],
            gridcolor=COLORES['bordes'],
            tickfont=dict(color=COLORES['texto_secundario'])
        ),
        plot_bgcolor=COLORES['fondo'],
        paper_bgcolor=COLORES['fondo'],
        font=dict(color=COLORES['texto']),
        height=350
    )

    return fig

# ============================================
# MANUAL DE USUARIO
# ============================================

def mostrar_guia_rapida():
    """Guía rápida visual y compacta"""
    
    with st.expander("Guía Rápida - Cómo usar el dashboard", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="step-card">
                <div><span class="step-number">1</span><span class="step-title">Filtrar Período</span></div>
                <div class="step-desc">Use el <b>Panel de Control</b> (izquierda) para seleccionar fechas y tipo de resultado.</div>
            </div>
            
            <div class="step-card">
                <div><span class="step-number">2</span><span class="step-title">Explorar Gráficos</span></div>
                <div class="step-desc">Navegue por las pestañas. Pase el mouse sobre los puntos para ver detalles.</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="step-card">
                <div><span class="step-number">3</span><span class="step-title">Interpretar Marcadores</span></div>
                <div class="step-desc">
                    <span style='color:#2dc76d'>▲ Verde</span>: Acierto (SUBE)<br>
                    <span style='color:#2dc76d'>▼ Verde</span>: Acierto (BAJA)<br>
                    <span style='color:#ff4757'>Rojo</span>: Error
                </div>
            </div>
            
            <div class="step-card">
                <div><span class="step-number">4</span><span class="step-title">Ver Sentimiento</span></div>
                <div class="step-desc">En <b>Análisis Detallado</b>, pase el mouse sobre el gráfico para ver influencia política del día.</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="step-card">
                <div><span class="step-number">TIP</span><span class="step-title">Clave</span></div>
                <div class="step-desc">Precisión >55% indica que el modelo supera el azar (50%).</div>
            </div>
            
            <div class="step-card">
                <div><span class="step-number">!</span><span class="step-title">Importante</span></div>
                <div class="step-desc">El sentimiento empeorando (↓) predice dólar subiendo (↑). <b>Relación inversa.</b></div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Información rápida de tooltips
        st.markdown("""
        <div style='background: #1a1d29; padding: 12px; border-radius: 6px; border: 1px solid #2a2f3d;'>
            <b style='color: #4a6fff;'>Información en Tooltips (Sentimiento):</b><br>
            <span style='color: #a0a4b3; font-size: 0.9rem;'>
            • <b>Influencia predominante:</b> Anti-Castillo / Anti-Keiko / Neutral<br>
            • <b>Distribución:</b> % de tweets por categoría<br>
            • <b>Razones:</b> Patrones detectados (IZQUIERDA, ERROR_FACTUAL, etc.)
            </span>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# INTERFAZ PRINCIPAL
# ============================================

def main():
    # Cargar datos completos
    with st.spinner('Cargando datos del período electoral 2021...'):
        df_completo = cargar_datos_completos()

    if df_completo is None or len(df_completo) == 0:
        st.error("No se pudieron cargar los datos. Verifica la ruta del archivo.")
        return

    # ============================================
    # ENCABEZADO PRINCIPAL
    # ============================================
    col_titulo1, col_titulo2 = st.columns([3, 1])

    with col_titulo1:
        st.markdown('<h1 class="titulo-principal">Predicción de la Direccionalidad del Tipo de Cambio USD/PEN mediante Análisis de Sentimiento en Twitter/X durante Elecciones en Perú</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitulo">Sistema predictivo basado en análisis de sentimiento político | Elecciones Presidenciales 2021</p>', unsafe_allow_html=True)

    with col_titulo2:
        # Mostrar período total disponible
        fecha_min = df_completo['Fecha'].min()
        fecha_max = df_completo['Fecha'].max()
        st.info(f"**Período disponible:**\n{fecha_min.strftime('%d/%m/%Y')} al {fecha_max.strftime('%d/%m/%Y')}")
    
    # Guía rápida justo después del título
    mostrar_guia_rapida()

    # ============================================
    # SIDEBAR MEJORADO
    # ============================================
    with st.sidebar:
        st.markdown("# Panel de Control")
        st.markdown("---")

        # SECCIÓN 1: PERÍODO DE ANÁLISIS
        st.markdown('<div class="sidebar-section-title">Período de Análisis</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-help">Selecciona el rango de fechas que deseas analizar</div>', unsafe_allow_html=True)

        fecha_min_disponible = df_completo['Fecha'].min()
        fecha_max_disponible = df_completo['Fecha'].max()

        col_fecha1, col_fecha2 = st.columns(2)

        with col_fecha1:
            fecha_inicio = st.date_input(
                "Desde",
                value=fecha_min_disponible,
                min_value=fecha_min_disponible,
                max_value=fecha_max_disponible,
                help="Fecha inicial del análisis"
            )

        with col_fecha2:
            fecha_fin = st.date_input(
                "Hasta",
                value=fecha_max_disponible,
                min_value=fecha_min_disponible,
                max_value=fecha_max_disponible,
                help="Fecha final del análisis"
            )

        # Validación de fechas
        if fecha_inicio > fecha_fin:
            st.error("La fecha inicial debe ser anterior a la final")
            fecha_fin = fecha_inicio

        st.markdown("---")

        # SECCIÓN 2: FILTRO DE RESULTADO
        st.markdown('<div class="sidebar-section-title">Filtro de Resultado</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-help">Analiza solo aciertos o errores del modelo</div>', unsafe_allow_html=True)

        filtro_resultado = st.selectbox(
            "Tipo de resultado",
            options=["Todos", "Solo Aciertos", "Solo Errores"],
            index=0,
            help="Filtra las predicciones según fueron correctas o incorrectas"
        )

        st.markdown("---")

        # SECCIÓN 3: MÉTRICAS RÁPIDAS
        st.markdown('<div class="sidebar-section-title">Métricas del Período</div>', unsafe_allow_html=True)

        # Calcular métricas para el período filtrado
        df_filtrado_temp = filtrar_por_fecha(df_completo, fecha_inicio, fecha_fin)
        df_filtrado_temp = filtrar_por_resultado(df_filtrado_temp, filtro_resultado)
        metricas_sidebar = calcular_metricas(df_filtrado_temp)

        if metricas_sidebar:
            # Métrica 1: Días analizados
            st.markdown(f"""
            <div class="sidebar-metric">
                <div class="sidebar-metric-label">Total de Días</div>
                <div class="sidebar-metric-value">{metricas_sidebar['total_dias']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Métrica 2: Precisión
            color_precision = COLORES['exito'] if metricas_sidebar['precision'] >= 55 else COLORES['advertencia']
            st.markdown(f"""
            <div class="sidebar-metric" style="border-color: {color_precision};">
                <div class="sidebar-metric-label">Precisión Global</div>
                <div class="sidebar-metric-value" style="color: {color_precision};">{metricas_sidebar['precision']:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

            # Métrica 3: Aciertos
            st.markdown(f"""
            <div class="sidebar-metric">
                <div class="sidebar-metric-label">Predicciones Correctas</div>
                <div class="sidebar-metric-value" style="color: {COLORES['exito']};">{metricas_sidebar['aciertos']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Métrica 4: Retorno
            color_retorno = COLORES['exito'] if metricas_sidebar['retorno_total'] > 0 else COLORES['error']
            st.markdown(f"""
            <div class="sidebar-metric" style="border-color: {color_retorno};">
                <div class="sidebar-metric-label">Retorno Acumulado</div>
                <div class="sidebar-metric-value" style="color: {color_retorno};">{metricas_sidebar['retorno_total']:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # SECCIÓN 4: INFORMACIÓN
        with st.expander("Información del Sistema"):
            st.markdown("""
            **Metodología:**
            - Análisis de sentimiento político en Twitter/X
            - Predicción basada en cambios de sentimiento
            - Correlación negativa sentimiento-tipo de cambio

            **Período:**
            - Elecciones Presidenciales Perú 2021
            - Abril - Mayo 2021
            - Segunda vuelta electoral

            **Indicadores:**
            - Triángulo verde: Predicción correcta (SUBE)
            - Triángulo rojo: Predicción correcta (BAJA)
            - Precisión >55%: Mejor que azar

            **Filtro de Resultado:**
            - Todos: Muestra todas las predicciones
            - Solo Aciertos: Predicciones correctas
            - Solo Errores: Predicciones incorrectas
            """)

    # ============================================
    # CONTENIDO PRINCIPAL
    # ============================================

    # Filtrar datos por el rango seleccionado Y resultado
    df_filtrado = filtrar_por_fecha(df_completo, fecha_inicio, fecha_fin)
    df_filtrado = filtrar_por_resultado(df_filtrado, filtro_resultado)

    if len(df_filtrado) == 0:
        st.warning("No hay datos disponibles para los filtros seleccionados. Ajusta los filtros en el panel lateral.")
        return

    # Calcular métricas para el período filtrado
    metricas = calcular_metricas(df_filtrado)

    # ============================================
    # SECCIÓN 1: MÉTRICAS PRINCIPALES
    # ============================================

    st.markdown("## Desempeño del Modelo Predictivo")

    # Crear 4 columnas para métricas principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        color_precision = COLORES['exito'] if metricas['precision'] >= 55 else COLORES['error']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Precisión Global</div>
            <div class="metric-value" style="color: {color_precision};">
                {metricas['precision']:.1f}%
            </div>
            <div class="metric-subtext">{metricas['aciertos']} de {metricas['total_dias']} días</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        color_retorno = COLORES['exito'] if metricas['retorno_total'] > 0 else COLORES['error']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Retorno Total</div>
            <div class="metric-value" style="color: {color_retorno};">
                {metricas['retorno_total']:+.2f}%
            </div>
            <div class="metric-subtext">Ganancia acumulada</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Detección de Subidas</div>
            <div class="metric-value" style="color: {COLORES['exito']};">
                {metricas['precision_sube']:.1f}%
            </div>
            <div class="metric-subtext">{metricas['aciertos_sube']} de {metricas['dias_sube']} predicciones</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Detección de Bajadas</div>
            <div class="metric-value" style="color: {COLORES['error']};">
                {metricas['precision_baja']:.1f}%
            </div>
            <div class="metric-subtext">{metricas['aciertos_baja']} de {metricas['dias_baja']} predicciones</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ============================================
    # PESTAÑAS PRINCIPALES
    # ============================================

    tab1, tab2, tab3 = st.tabs(["Vista Principal", "Análisis Detallado", "Retorno y Desempeño"])

    with tab1:
        # Gráfico principal
        st.markdown("### Evolución del Tipo de Cambio con Predicciones del Modelo")

        # Información del contexto y estadísticas clave
        col_info1, col_info2, col_info3, col_info4 = st.columns(4)
        
        with col_info1:
            st.caption(f"**Período:** {fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}")
        
        with col_info2:
            tipo_cambio_inicio = df_filtrado['Compra'].iloc[0] if len(df_filtrado) > 0 else 0
            tipo_cambio_fin = df_filtrado['Compra'].iloc[-1] if len(df_filtrado) > 0 else 0
            variacion_periodo = ((tipo_cambio_fin - tipo_cambio_inicio) / tipo_cambio_inicio * 100) if tipo_cambio_inicio > 0 else 0
            st.caption(f"**TC Variación:** S/ {tipo_cambio_inicio:.3f} → S/ {tipo_cambio_fin:.3f} ({variacion_periodo:+.2f}%)")
        
        with col_info3:
            st.caption(f"**Señales:** {metricas['dias_sube']} LONG | {metricas['dias_baja']} SHORT")
        
        with col_info4:
            st.caption(f"**Filtro activo:** {filtro_resultado}")

        # Crear y mostrar gráfico principal
        fig_principal = crear_grafico_principal(df_filtrado)
        st.plotly_chart(fig_principal, use_container_width=True)

        # Leyenda del gráfico - más clara y compacta
        st.markdown(f"""
        <div style='background: {COLORES['fondo_cards']}; padding: 10px; border-radius: 6px; margin-top: 10px;'>
            <span style='color: {COLORES['texto_secundario']}; font-size: 0.85rem;'><b>Leyenda:</b></span>
            <span style='color:{COLORES['exito']}; margin-left: 15px;'>▲ Acierto SUBE</span>
            <span style='color:{COLORES['exito']}; margin-left: 15px;'>▼ Acierto BAJA</span>
            <span style='color:{COLORES['error']}; margin-left: 15px;'>● Error</span>
            <span style='color:{COLORES['primario']}; margin-left: 15px;'>━ Tipo de cambio</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabla de resumen de operaciones destacadas
        if len(df_filtrado) > 0:
            st.markdown("---")
            st.markdown("### Resumen de Operaciones Destacadas")
            
            col_dest1, col_dest2, col_dest3 = st.columns(3)
            
            with col_dest1:
                # Mejor operación
                mejor_idx = df_filtrado['Retorno'].idxmax()
                mejor_op = df_filtrado.loc[mejor_idx]
                st.markdown(f"""
                <div style='background: {COLORES['fondo_cards']}; padding: 12px; border-radius: 6px; border-left: 3px solid {COLORES['exito']};'>
                    <b style='color: {COLORES['exito']};'>Mejor Operación</b><br>
                    <span style='color: {COLORES['texto_secundario']}; font-size: 0.85rem;'>
                    Fecha: {mejor_op['Fecha'].strftime('%d/%m/%Y')}<br>
                    Retorno: <b style='color: {COLORES['exito']};'>{mejor_op['Retorno']:+.3f}%</b><br>
                    Variación TC: {mejor_op['Variacion_Dolar']:+.3f}%
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            with col_dest2:
                # Peor operación
                peor_idx = df_filtrado['Retorno'].idxmin()
                peor_op = df_filtrado.loc[peor_idx]
                st.markdown(f"""
                <div style='background: {COLORES['fondo_cards']}; padding: 12px; border-radius: 6px; border-left: 3px solid {COLORES['error']};'>
                    <b style='color: {COLORES['error']};'>Peor Operación</b><br>
                    <span style='color: {COLORES['texto_secundario']}; font-size: 0.85rem;'>
                    Fecha: {peor_op['Fecha'].strftime('%d/%m/%Y')}<br>
                    Retorno: <b style='color: {COLORES['error']};'>{peor_op['Retorno']:+.3f}%</b><br>
                    Variación TC: {peor_op['Variacion_Dolar']:+.3f}%
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            with col_dest3:
                # Día de mayor volatilidad
                mayor_vol_idx = df_filtrado['Variacion_Dolar'].abs().idxmax()
                mayor_vol = df_filtrado.loc[mayor_vol_idx]
                color_vol = COLORES['exito'] if mayor_vol['Acierto'] else COLORES['error']
                st.markdown(f"""
                <div style='background: {COLORES['fondo_cards']}; padding: 12px; border-radius: 6px; border-left: 3px solid {COLORES['advertencia']};'>
                    <b style='color: {COLORES['advertencia']};'>Mayor Volatilidad</b><br>
                    <span style='color: {COLORES['texto_secundario']}; font-size: 0.85rem;'>
                    Fecha: {mayor_vol['Fecha'].strftime('%d/%m/%Y')}<br>
                    Variación: <b>{mayor_vol['Variacion_Dolar']:+.3f}%</b><br>
                    Predicción: <b style='color: {color_vol};'>{'Correcta' if mayor_vol['Acierto'] else 'Incorrecta'}</b>
                    </span>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### Análisis Detallado del Sentimiento y Variación")

        # Gráfico combinado de sentimiento y variación
        fig_combinado = crear_grafico_sentimiento_variacion(df_filtrado)
        st.plotly_chart(fig_combinado, use_container_width=True)
        
        # Nota informativa sobre tooltips - más compacta y clara
        st.markdown(f"""
        <div style='background: {COLORES['fondo_cards']}; padding: 12px; border-radius: 6px; border-left: 3px solid {COLORES['primario']}; margin: 10px 0;'>
            <span style='color: {COLORES['primario']}; font-weight: 600;'>INFO:</span>
            <span style='color: {COLORES['texto_secundario']}; font-size: 0.9rem;'>
            Pase el mouse sobre los puntos del gráfico de sentimiento para ver: <b>Influencia predominante</b> (Anti-Castillo/Anti-Keiko/Neutral), 
            <b>distribución de tweets</b> y <b>razones principales</b> detectadas.
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Análisis de tendencias
        st.markdown("---")
        st.markdown("### Análisis Cuantitativo del Modelo")

        col_analisis1, col_analisis2 = st.columns(2)

        with col_analisis1:
            # Calcular correlación entre sentimiento y variación del dólar
            corr_sentimiento = df_filtrado['sentimiento_numerico'].corr(df_filtrado['Variacion_Dolar'])
            
            # Determinar fortaleza de la señal
            fortaleza = "Débil" if abs(corr_sentimiento) < 0.3 else "Moderada" if abs(corr_sentimiento) < 0.5 else "Fuerte"
            color_corr = COLORES['advertencia'] if abs(corr_sentimiento) < 0.3 else COLORES['exito']

            st.metric(
                "Coeficiente de Correlación",
                f"{corr_sentimiento:.3f}",
                f"Señal {fortaleza} (r < 0.3 = débil)"
            )

            # Análisis de volatilidad
            volatilidad = df_filtrado['Variacion_Dolar'].std()
            volatilidad_anualizada = volatilidad * np.sqrt(252)
            st.metric(
                "Volatilidad Diaria / Anualizada",
                f"{volatilidad:.2f}% / {volatilidad_anualizada:.1f}%",
                "Medida de riesgo del mercado"
            )

        with col_analisis2:
            # Factor de rentabilidad (Profit Factor)
            retornos_positivos = df_filtrado[df_filtrado['Retorno'] > 0]['Retorno'].sum()
            retornos_negativos = abs(df_filtrado[df_filtrado['Retorno'] < 0]['Retorno'].sum())
            profit_factor = retornos_positivos / retornos_negativos if retornos_negativos > 0 else 0
            
            color_pf = COLORES['exito'] if profit_factor > 1.5 else COLORES['advertencia']
            st.metric(
                "Profit Factor",
                f"{profit_factor:.2f}",
                "Ganancia/Pérdida (>1.5 = bueno)"
            )

            # Expectativa matemática
            expectativa = df_filtrado['Retorno'].mean()
            dias_positivos = (df_filtrado['Retorno'] > 0).sum()
            expectativa_anualizada = expectativa * 252
            
            st.metric(
                "Expectativa Matemática",
                f"{expectativa:+.3f}% / día",
                f"Proyección anual: {expectativa_anualizada:+.1f}%"
            )

    with tab3:
        st.markdown("### Retorno y Desempeño del Modelo")

        col_retorno1, col_retorno2 = st.columns([2, 1])

        with col_retorno1:
            # Gráfico de retorno acumulado
            fig_retorno = crear_grafico_retorno_acumulado(df_filtrado)
            st.plotly_chart(fig_retorno, use_container_width=True)

        with col_retorno2:
            # Matriz de desempeño
            fig_matriz = crear_grafico_matriz_desempeno(metricas)
            st.plotly_chart(fig_matriz, use_container_width=True)

        # Métricas de riesgo y retorno
        st.markdown("---")
        st.markdown("### Análisis de Performance Trading")

        col_riesgo1, col_riesgo2, col_riesgo3, col_riesgo4 = st.columns(4)

        with col_riesgo1:
            # Profit Factor
            retornos_positivos = df_filtrado[df_filtrado['Retorno'] > 0]['Retorno'].sum()
            retornos_negativos = abs(df_filtrado[df_filtrado['Retorno'] < 0]['Retorno'].sum())
            profit_factor = retornos_positivos / retornos_negativos if retornos_negativos > 0 else 0
            
            color_pf = COLORES['exito'] if profit_factor > 1.5 else COLORES['advertencia']

            st.metric(
                "Profit Factor",
                f"{profit_factor:.2f}",
                "Ganancia/Pérdida total"
            )

        with col_riesgo2:
            # Recovery Factor (Retorno / Max Drawdown)
            df_filtrado['Retorno_Max'] = df_filtrado['Retorno_Acumulado'].cummax()
            df_filtrado['Drawdown'] = df_filtrado['Retorno_Acumulado'] - df_filtrado['Retorno_Max']
            max_drawdown = abs(df_filtrado['Drawdown'].min())
            
            retorno_total = df_filtrado['Retorno_Acumulado'].iloc[-1] if len(df_filtrado) > 0 else 0
            recovery_factor = retorno_total / max_drawdown if max_drawdown > 0 else 0
            
            color_rf = COLORES['exito'] if recovery_factor > 2 else COLORES['advertencia']

            st.metric(
                "Recovery Factor",
                f"{recovery_factor:.2f}",
                "Retorno/Drawdown máximo"
            )

        with col_riesgo3:
            # Expectativa por operación
            expectativa = df_filtrado['Retorno'].mean()
            win_rate = (df_filtrado['Retorno'] > 0).mean() * 100
            
            # Retorno promedio cuando gana vs cuando pierde
            avg_win = df_filtrado[df_filtrado['Retorno'] > 0]['Retorno'].mean() if (df_filtrado['Retorno'] > 0).any() else 0
            avg_loss = df_filtrado[df_filtrado['Retorno'] < 0]['Retorno'].mean() if (df_filtrado['Retorno'] < 0).any() else 0
            
            color_exp = COLORES['exito'] if expectativa > 0.15 else COLORES['advertencia']

            st.metric(
                "Expectativa Matemática",
                f"{expectativa:+.3f}%",
                f"Win: {avg_win:.3f}% | Loss: {avg_loss:.3f}%"
            )

        with col_riesgo4:
            # Calmar Ratio (Retorno anualizado / Max Drawdown)
            retorno_promedio_diario = df_filtrado['Retorno'].mean()
            retorno_anualizado = retorno_promedio_diario * 252
            
            calmar_ratio = retorno_anualizado / max_drawdown if max_drawdown > 0 else 0
            
            color_calmar = COLORES['exito'] if calmar_ratio > 0.5 else COLORES['advertencia']

            st.metric(
                "Calmar Ratio",
                f"{calmar_ratio:.2f}",
                f"Ret.Anual: {retorno_anualizado:+.1f}%"
            )
        
        # Segunda fila de métricas adicionales
        st.markdown("---")
        col_extra1, col_extra2, col_extra3, col_extra4 = st.columns(4)
        
        with col_extra1:
            # Ratio de aciertos ponderado por magnitud
            aciertos_ponderados = df_filtrado[df_filtrado['Acierto']]['Variacion_Dolar'].abs().sum()
            total_ponderado = df_filtrado['Variacion_Dolar'].abs().sum()
            precision_ponderada = (aciertos_ponderados / total_ponderado * 100) if total_ponderado > 0 else 0
            
            st.metric(
                "Precisión Ponderada",
                f"{precision_ponderada:.1f}%",
                "Por magnitud de movimiento"
            )
        
        with col_extra2:
            # Payoff Ratio (Average Win / Average Loss)
            payoff_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0
            
            color_payoff = COLORES['exito'] if payoff_ratio > 1.5 else COLORES['advertencia']
            
            st.metric(
                "Payoff Ratio",
                f"{payoff_ratio:.2f}",
                "Ganancia media/Pérdida media"
            )
        
        with col_extra3:
            # Días consecutivos ganadores vs perdedores
            max_winning_streak = 0
            max_losing_streak = 0
            current_win = 0
            current_loss = 0
            
            for retorno in df_filtrado['Retorno']:
                if retorno > 0:
                    current_win += 1
                    max_winning_streak = max(max_winning_streak, current_win)
                    current_loss = 0
                elif retorno < 0:
                    current_loss += 1
                    max_losing_streak = max(max_losing_streak, current_loss)
                    current_win = 0
            
            st.metric(
                "Racha Máxima",
                f"+{max_winning_streak} / -{max_losing_streak}",
                "Días ganadores/perdedores"
            )
        
        with col_extra4:
            # Sortino Ratio (solo considera volatilidad negativa)
            retornos_negativos_std = df_filtrado[df_filtrado['Retorno'] < 0]['Retorno'].std()
            sortino_ratio = retorno_promedio_diario / retornos_negativos_std if retornos_negativos_std > 0 else 0
            
            color_sortino = COLORES['exito'] if sortino_ratio > 0.3 else COLORES['advertencia']
            
            st.metric(
                "Sortino Ratio",
                f"{sortino_ratio:.2f}",
                "Ajuste por riesgo a la baja"
            )

    # ============================================
    # PIE DE PÁGINA
    # ============================================

    st.markdown("---")

    col_footer1, col_footer2, col_footer3 = st.columns([1, 2, 1])

    with col_footer2:
        st.markdown(f"""
        <div style="text-align: center; color: {COLORES['texto_secundario']}; padding: 20px; font-size: 0.9rem;">
            <div style="margin-bottom: 10px;">
                <strong>Modelo Predictivo - Análisis de Sentimiento en Twitter/X</strong><br>
                Período: Elecciones Presidenciales Perú 2021 (Abril-Mayo)
            </div>
            <div>
                Precisión: <span style="color: {COLORES['exito']}">{metricas['precision']:.1f}%</span> |
                Retorno: <span style="color: {COLORES['exito'] if metricas['retorno_total'] > 0 else COLORES['error']}">{metricas['retorno_total']:+.2f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    main()
