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

    /* ============================================
       NUEVO: Cards mejoradas para traders
       ============================================ */
    .trader-card {{
        background: {COLORES['fondo_cards']};
        border-radius: 12px;
        padding: 1.1rem 1.2rem;
        border: 1px solid {COLORES['bordes']};
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    .trader-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 12px 12px 0 0;
    }}
    .trader-card.verde::before {{ background: {COLORES['exito']}; }}
    .trader-card.rojo::before  {{ background: {COLORES['error']}; }}
    .trader-card.azul::before  {{ background: {COLORES['primario']}; }}
    .trader-card.naranja::before {{ background: {COLORES['advertencia']}; }}

    .trader-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        border-color: {COLORES['primario']};
    }}
    .tc-label {{
        font-size: 0.72rem;
        color: {COLORES['texto_secundario']};
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }}
    .tc-value {{
        font-size: 2rem;
        font-weight: 800;
        line-height: 1;
        margin: 0.2rem 0;
        font-variant-numeric: tabular-nums;
    }}
    .tc-bench {{
        font-size: 0.72rem;
        color: {COLORES['texto_secundario']};
        margin-top: 0.4rem;
        line-height: 1.4;
    }}
    .tc-badge {{
        display: inline-block;
        padding: 2px 7px;
        border-radius: 20px;
        font-size: 0.68rem;
        font-weight: 700;
        margin-top: 0.35rem;
        letter-spacing: 0.4px;
    }}
    .badge-ok  {{ background: rgba(45,199,109,0.18); color: {COLORES['exito']}; }}
    .badge-warn{{ background: rgba(255,165,2,0.18);  color: {COLORES['advertencia']}; }}
    .badge-bad {{ background: rgba(255,71,87,0.18);  color: {COLORES['error']}; }}

    /* Tabla de operaciones */
    .op-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.82rem;
    }}
    .op-table th {{
        background: {COLORES['fondo_sidebar']};
        color: {COLORES['texto_secundario']};
        text-transform: uppercase;
        font-size: 0.7rem;
        letter-spacing: 0.6px;
        padding: 8px 10px;
        text-align: left;
        border-bottom: 1px solid {COLORES['bordes']};
    }}
    .op-table td {{
        padding: 7px 10px;
        border-bottom: 1px solid {COLORES['bordes']};
        color: {COLORES['texto']};
    }}
    .op-table tr:hover td {{
        background: {COLORES['fondo_sidebar']};
    }}
    .pill-long  {{ background: rgba(45,199,109,0.2); color:{COLORES['exito']};
                  padding:2px 8px; border-radius:20px; font-size:0.7rem; font-weight:700; }}
    .pill-short {{ background: rgba(255,71,87,0.2);  color:{COLORES['error']};
                  padding:2px 8px; border-radius:20px; font-size:0.7rem; font-weight:700; }}
    .pill-ok    {{ background: rgba(45,199,109,0.15); color:{COLORES['exito']};
                  padding:2px 6px; border-radius:20px; font-size:0.7rem; }}
    .pill-err   {{ background: rgba(255,71,87,0.15);  color:{COLORES['error']};
                  padding:2px 6px; border-radius:20px; font-size:0.7rem; }}

    /* Advertencia sesgo temporal */
    .bias-warning {{
        background: rgba(255,165,2,0.08);
        border: 1px solid rgba(255,165,2,0.35);
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 0.8rem;
        color: {COLORES['advertencia']};
        margin: 10px 0 0 0;
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
        archivo_path = 'tweets_GOZU_SENTIMIENTO_MEJORADO.xlsx'
        df = pd.read_excel(archivo_path, engine='openpyxl')

        df['Fecha'] = pd.to_datetime(df['TweetCreateTime']).dt.date
        df = df.dropna(subset=['sentimiento_numerico', 'Compra'])

        df_daily = df.groupby('Fecha').agg({
            'sentimiento_numerico': 'mean',
            'Compra': 'mean'
        }).reset_index()

        df_daily = df_daily.sort_values('Fecha').reset_index(drop=True)
        df_daily['Fecha'] = pd.to_datetime(df_daily['Fecha'])

        fecha_inicio = pd.Timestamp('2021-04-01')
        fecha_fin = pd.Timestamp('2021-05-31')
        df_daily = df_daily[(df_daily['Fecha'] >= fecha_inicio) & (df_daily['Fecha'] <= fecha_fin)].copy()

        df_daily['Variacion_Dolar'] = df_daily['Compra'].pct_change() * 100
        df_daily['Sentimiento_Ayer'] = df_daily['sentimiento_numerico'].shift(1)
        df_daily['Cambio_Sentimiento'] = df_daily['Sentimiento_Ayer'].diff()

        df_daily['Prediccion'] = np.where(
            df_daily['Cambio_Sentimiento'] < 0,
            1,
            -1
        )

        df_daily['Realidad'] = np.where(
            df_daily['Variacion_Dolar'] > 0,
            1,
            -1
        )

        df_daily['Acierto'] = df_daily['Prediccion'] == df_daily['Realidad']
        df_daily['Retorno'] = df_daily['Prediccion'] * df_daily['Variacion_Dolar']
        df_daily['Retorno_Acumulado'] = df_daily['Retorno'].cumsum()
        df_daily = agregar_datos_detallados(df_daily, df)

        return df_daily

    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return None


def agregar_datos_detallados(df_daily, df_original):
    """Agrega información detallada de sentimiento para tooltips"""
    df_original['Fecha'] = pd.to_datetime(df_original['TweetCreateTime']).dt.date
    df_original['Fecha'] = pd.to_datetime(df_original['Fecha'])

    stats_por_dia = df_original.groupby('Fecha').apply(lambda x: pd.Series({
        'total_tweets': len(x),
        'anti_castillo': (x['sentimiento_economico'].str.contains('ANTI_CASTILLO', na=False)).sum(),
        'anti_keiko': (x['sentimiento_economico'].str.contains('ANTI_KEIKO', na=False)).sum(),
        'neutral': (x['sentimiento_economico'] == 'NEUTRAL').sum(),
        'razones_top': x['razones'].mode()[0] if len(x['razones'].mode()) > 0 else 'N/A'
    })).reset_index()

    df_daily = df_daily.merge(stats_por_dia, on='Fecha', how='left')
    df_daily['pct_anti_castillo'] = (df_daily['anti_castillo'] / df_daily['total_tweets'] * 100).fillna(0)
    df_daily['pct_anti_keiko']    = (df_daily['anti_keiko']    / df_daily['total_tweets'] * 100).fillna(0)
    df_daily['pct_neutral']       = (df_daily['neutral']       / df_daily['total_tweets'] * 100).fillna(0)

    df_daily['influencia_predominante'] = df_daily.apply(lambda row:
        'Anti-Castillo' if row['pct_anti_castillo'] > row['pct_anti_keiko'] and row['pct_anti_castillo'] > row['pct_neutral']
        else 'Anti-Keiko' if row['pct_anti_keiko'] > row['pct_anti_castillo'] and row['pct_anti_keiko'] > row['pct_neutral']
        else 'Neutral/Mixto', axis=1)

    return df_daily


def filtrar_por_fecha(df, fecha_inicio, fecha_fin):
    mask = (df['Fecha'] >= pd.Timestamp(fecha_inicio)) & (df['Fecha'] <= pd.Timestamp(fecha_fin))
    return df[mask].copy()


def filtrar_por_resultado(df, filtro_resultado):
    if filtro_resultado == "Todos":
        return df.copy()
    elif filtro_resultado == "Solo Aciertos":
        return df[df['Acierto'] == True].copy()
    elif filtro_resultado == "Solo Errores":
        return df[df['Acierto'] == False].copy()
    return df.copy()


def calcular_metricas(df_filtrado):
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

    metricas['precision_sube'] = (metricas['aciertos_sube'] / metricas['dias_sube'] * 100) if metricas['dias_sube'] > 0 else 0
    metricas['precision_baja'] = (metricas['aciertos_baja'] / metricas['dias_baja'] * 100) if metricas['dias_baja'] > 0 else 0

    return metricas


# ============================================
# NUEVO: Cálculo centralizado de métricas avanzadas
# ============================================

def calcular_metricas_avanzadas(df):
    """
    Calcula todas las métricas de trading en un solo lugar.
    Evita recalcular en cada tab y expone Sharpe Ratio y Drawdown.
    """
    df = df.copy()
    retornos = df['Retorno'].dropna()

    # Drawdown
    df['Retorno_Max'] = df['Retorno_Acumulado'].cummax()
    df['Drawdown']    = df['Retorno_Acumulado'] - df['Retorno_Max']
    max_drawdown = abs(df['Drawdown'].min())

    # Retorno
    retorno_total       = df['Retorno_Acumulado'].iloc[-1] if len(df) > 0 else 0
    retorno_prom_diario = retornos.mean()
    retorno_anualizado  = retorno_prom_diario * 252

    # Profit Factor
    ganancias = retornos[retornos > 0].sum()
    perdidas  = abs(retornos[retornos < 0].sum())
    profit_factor = ganancias / perdidas if perdidas > 0 else 0

    # Win/Loss promedio
    avg_win  = retornos[retornos > 0].mean() if (retornos > 0).any() else 0
    avg_loss = retornos[retornos < 0].mean() if (retornos < 0).any() else 0
    win_rate = (retornos > 0).mean() * 100

    # Payoff Ratio
    payoff_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0

    # Sharpe Ratio (diario, rf=0)
    std_retornos = retornos.std()
    sharpe_ratio = (retorno_prom_diario / std_retornos * np.sqrt(252)) if std_retornos > 0 else 0

    # Sortino Ratio
    std_neg = retornos[retornos < 0].std()
    sortino_ratio = (retorno_prom_diario / std_neg) if std_neg > 0 else 0

    # Calmar Ratio
    calmar_ratio = retorno_anualizado / max_drawdown if max_drawdown > 0 else 0

    # Recovery Factor
    recovery_factor = retorno_total / max_drawdown if max_drawdown > 0 else 0

    # Precisión ponderada por magnitud
    aciertos_pond = df[df['Acierto']]['Variacion_Dolar'].abs().sum()
    total_pond    = df['Variacion_Dolar'].abs().sum()
    precision_ponderada = (aciertos_pond / total_pond * 100) if total_pond > 0 else 0

    # Rachas
    max_win_streak = max_loss_streak = cur_win = cur_loss = 0
    for r in retornos:
        if r > 0:
            cur_win  += 1; cur_loss = 0
            max_win_streak  = max(max_win_streak,  cur_win)
        elif r < 0:
            cur_loss += 1; cur_win  = 0
            max_loss_streak = max(max_loss_streak, cur_loss)

    return {
        'max_drawdown':       max_drawdown,
        'retorno_total':      retorno_total,
        'retorno_anualizado': retorno_anualizado,
        'profit_factor':      profit_factor,
        'avg_win':            avg_win,
        'avg_loss':           avg_loss,
        'win_rate':           win_rate,
        'payoff_ratio':       payoff_ratio,
        'sharpe_ratio':       sharpe_ratio,
        'sortino_ratio':      sortino_ratio,
        'calmar_ratio':       calmar_ratio,
        'recovery_factor':    recovery_factor,
        'precision_ponderada': precision_ponderada,
        'max_win_streak':     max_win_streak,
        'max_loss_streak':    max_loss_streak,
        'df_con_drawdown':    df,
    }


# ============================================
# FUNCIONES DE VISUALIZACIÓN (sin cambios)
# ============================================

def crear_grafico_principal(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['Compra'],
        mode='lines',
        name='Tipo de Cambio',
        line=dict(color=COLORES['primario'], width=3),
        hovertemplate='<b>%{x|%d/%m/%Y}</b><br>S/ %{y:.4f}<extra></extra>'
    ))

    for idx, row in df.iterrows():
        color   = COLORES['exito'] if row['Acierto'] else COLORES['error']
        simbolo = 'triangle-up' if row['Prediccion'] == 1 else 'triangle-down'
        fig.add_trace(go.Scatter(
            x=[row['Fecha']], y=[row['Compra']],
            mode='markers',
            marker=dict(size=10, color=color, symbol=simbolo, opacity=0.8,
                        line=dict(width=1, color='white')),
            showlegend=False,
            hoverinfo='text',
            hovertext=f"<b>{row['Fecha'].strftime('%d/%m')}</b><br>S/ {row['Compra']:.4f}<br>"
                      f"{'✅ Acierto' if row['Acierto'] else '❌ Error'} {row['Variacion_Dolar']:+.2f}%<br>"
                      f"Señal: {'LONG ▲' if row['Prediccion']==1 else 'SHORT ▼'}"
        ))

    fig.update_layout(
        title=dict(text='Evolución del Tipo de Cambio USD/PEN con Predicciones',
                   font=dict(size=18, color=COLORES['texto']), x=0.05),
        xaxis=dict(title='Fecha', tickformat='%d/%m', gridcolor=COLORES['bordes'],
                   zerolinecolor=COLORES['bordes'], linecolor=COLORES['bordes'],
                   tickfont=dict(color=COLORES['texto_secundario'])),
        yaxis=dict(title='Tipo de Cambio (Soles por Dólar)', gridcolor=COLORES['bordes'],
                   zerolinecolor=COLORES['bordes'], linecolor=COLORES['bordes'],
                   tickfont=dict(color=COLORES['texto_secundario'])),
        hovermode='closest',
        plot_bgcolor=COLORES['fondo'], paper_bgcolor=COLORES['fondo'],
        font=dict(color=COLORES['texto']), height=500, showlegend=True,
        legend=dict(bgcolor=COLORES['fondo_cards'], bordercolor=COLORES['bordes'],
                    borderwidth=1, font=dict(color=COLORES['texto']))
    )
    return fig


from plotly.subplots import make_subplots

def crear_grafico_sentimiento_variacion(df):
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Sentimiento Político Diario', 'Variación del Dólar vs Predicciones'),
        vertical_spacing=0.15
    )

    hover_texts = []
    for idx, row in df.iterrows():
        hover_texts.append(
            f"<b>Fecha:</b> {row['Fecha'].strftime('%d/%m/%Y')}<br>"
            f"<b>Sentimiento:</b> {row['sentimiento_numerico']:.3f}<br>"
            f"<b>Total tweets:</b> {int(row['total_tweets'])}<br>"
            f"<b>Influencia predominante:</b> {row['influencia_predominante']}<br>"
            f"<b>Anti-Castillo:</b> {row['pct_anti_castillo']:.1f}% ({int(row['anti_castillo'])} tweets)<br>"
            f"<b>Anti-Keiko:</b> {row['pct_anti_keiko']:.1f}% ({int(row['anti_keiko'])} tweets)<br>"
            f"<b>Neutral:</b> {row['pct_neutral']:.1f}% ({int(row['neutral'])} tweets)<br>"
            f"<b>Razones principales:</b> {row['razones_top']}"
        )

    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['sentimiento_numerico'],
        mode='lines+markers', name='Sentimiento',
        line=dict(color=COLORES['primario_suave'], width=2),
        marker=dict(size=6, color=COLORES['primario_suave']),
        fill='tozeroy', fillcolor='rgba(107, 138, 255, 0.1)',
        hovertext=hover_texts, hoverinfo='text'
    ), row=1, col=1)

    fig.add_hline(y=0, line_dash="dash", line_color=COLORES['neutro'], row=1, col=1)

    colores_barras = [COLORES['exito'] if a else COLORES['error'] for a in df['Acierto']]
    fig.add_trace(go.Bar(
        x=df['Fecha'], y=df['Variacion_Dolar'],
        marker_color=colores_barras, name='Variación', showlegend=False
    ), row=2, col=1)

    fig.add_hline(y=0, line_color=COLORES['texto'], line_width=1, row=2, col=1)

    fig.update_layout(
        height=600, plot_bgcolor=COLORES['fondo'], paper_bgcolor=COLORES['fondo'],
        font=dict(color=COLORES['texto']), showlegend=True,
        legend=dict(bgcolor=COLORES['fondo_cards'], bordercolor=COLORES['bordes'], borderwidth=1)
    )
    for r in [1, 2]:
        fig.update_xaxes(tickformat='%d/%m', gridcolor=COLORES['bordes'],
                         tickfont=dict(color=COLORES['texto_secundario']), row=r, col=1)
    fig.update_yaxes(title_text='Índice de Sentimiento', gridcolor=COLORES['bordes'],
                     tickfont=dict(color=COLORES['texto_secundario']), row=1, col=1)
    fig.update_yaxes(title_text='Variación (%)', gridcolor=COLORES['bordes'],
                     tickfont=dict(color=COLORES['texto_secundario']), row=2, col=1)
    return fig


def crear_grafico_retorno_acumulado(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['Retorno_Acumulado'],
        mode='lines', name='Retorno Acumulado',
        line=dict(color=COLORES['exito'], width=3),
        fill='tozeroy', fillcolor='rgba(45, 199, 109, 0.1)'
    ))
    fig.add_hline(y=0, line_color=COLORES['texto'], line_width=1)
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
        title=dict(text='Retorno Acumulado del Modelo Predictivo',
                   font=dict(size=16, color=COLORES['texto'])),
        xaxis=dict(title='Fecha', tickformat='%d/%m', gridcolor=COLORES['bordes'],
                   tickfont=dict(color=COLORES['texto_secundario'])),
        yaxis=dict(title='Retorno Acumulado (%)', gridcolor=COLORES['bordes'],
                   tickfont=dict(color=COLORES['texto_secundario'])),
        plot_bgcolor=COLORES['fondo'], paper_bgcolor=COLORES['fondo'],
        font=dict(color=COLORES['texto']), height=400
    )
    return fig


def crear_grafico_matriz_desempeno(metricas):
    categorias = ['Predijo SUBE', 'Predijo BAJA']
    precisiones = [metricas['precision_sube'], metricas['precision_baja']]
    colores = []
    for p in precisiones:
        colores.append(COLORES['exito'] if p >= 70 else COLORES['advertencia'] if p >= 50 else COLORES['error'])

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categorias, y=precisiones, marker_color=colores,
        text=[f'{p:.1f}%' for p in precisiones],
        textposition='outside', textfont=dict(size=14, color=COLORES['texto'])
    ))
    fig.add_hline(y=50, line_dash="dash", line_color=COLORES['neutro'],
                  annotation_text="Azar (50%)", annotation_position="top right",
                  annotation_font=dict(color=COLORES['texto_secundario']))
    fig.add_hline(y=60, line_dash="dash", line_color=COLORES['exito_suave'],
                  annotation_text="Bueno (60%)", annotation_position="top right",
                  annotation_font=dict(color=COLORES['exito_suave']))
    fig.update_layout(
        title=dict(text='Precisión por Tipo de Predicción',
                   font=dict(size=16, color=COLORES['texto'])),
        xaxis=dict(title='Tipo de Predicción', gridcolor=COLORES['bordes'],
                   tickfont=dict(color=COLORES['texto_secundario'])),
        yaxis=dict(title='Precisión (%)', range=[0, 100], gridcolor=COLORES['bordes'],
                   tickfont=dict(color=COLORES['texto_secundario'])),
        plot_bgcolor=COLORES['fondo'], paper_bgcolor=COLORES['fondo'],
        font=dict(color=COLORES['texto']), height=350
    )
    return fig


# ============================================
# NUEVO: Gráfico de composición política (área apilada 100%)
# ============================================

def crear_grafico_composicion_politica(df):
    """
    Área apilada 100%: evolución diaria Anti-Castillo / Anti-Keiko / Neutral.
    Este gráfico es el corazón del modelo: muestra cómo la narrativa política
    en Twitter se desplazó durante el período electoral.
    """
    fig = go.Figure()

    # Anti-Castillo (rojo → dólar sube)
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['pct_anti_castillo'],
        name='Anti-Castillo',
        mode='lines',
        stackgroup='one',
        groupnorm='percent',
        line=dict(width=0.5, color='rgba(255,71,87,0.8)'),
        fillcolor='rgba(255,71,87,0.55)',
        hovertemplate=(
            "<b>%{x|%d/%m/%Y}</b><br>"
            "Anti-Castillo: <b>%{y:.1f}%</b><extra></extra>"
        )
    ))

    # Anti-Keiko (naranja → dólar baja)
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['pct_anti_keiko'],
        name='Anti-Keiko',
        mode='lines',
        stackgroup='one',
        line=dict(width=0.5, color='rgba(255,165,2,0.8)'),
        fillcolor='rgba(255,165,2,0.45)',
        hovertemplate=(
            "<b>%{x|%d/%m/%Y}</b><br>"
            "Anti-Keiko: <b>%{y:.1f}%</b><extra></extra>"
        )
    ))

    # Neutral (gris)
    fig.add_trace(go.Scatter(
        x=df['Fecha'], y=df['pct_neutral'],
        name='Neutral',
        mode='lines',
        stackgroup='one',
        line=dict(width=0.5, color='rgba(116,125,140,0.8)'),
        fillcolor='rgba(116,125,140,0.35)',
        hovertemplate=(
            "<b>%{x|%d/%m/%Y}</b><br>"
            "Neutral: <b>%{y:.1f}%</b><extra></extra>"
        )
    ))

    # Anotaciones de eventos electorales clave
    eventos = [
        {'fecha': '2021-04-11', 'texto': '1ª Vuelta', 'color': COLORES['advertencia']},
        {'fecha': '2021-06-06', 'texto': '2ª Vuelta', 'color': COLORES['primario']},
    ]
    for ev in eventos:
        ts = pd.Timestamp(ev['fecha'])
        if df['Fecha'].min() <= ts <= df['Fecha'].max():
            fig.add_vline(
                x=ts, line_dash='dot', line_color=ev['color'], line_width=1.5,
                annotation_text=ev['texto'],
                annotation_position='top left',
                annotation_font=dict(color=ev['color'], size=11)
            )

    fig.update_layout(
        title=dict(
            text='Composición Política del Sentimiento en Twitter (% diario)',
            font=dict(size=16, color=COLORES['texto'])
        ),
        xaxis=dict(
            title='Fecha', tickformat='%d/%m',
            gridcolor=COLORES['bordes'],
            tickfont=dict(color=COLORES['texto_secundario'])
        ),
        yaxis=dict(
            title='Proporción (%)',
            gridcolor=COLORES['bordes'],
            tickfont=dict(color=COLORES['texto_secundario']),
            range=[0, 100]
        ),
        plot_bgcolor=COLORES['fondo'],
        paper_bgcolor=COLORES['fondo'],
        font=dict(color=COLORES['texto']),
        height=380,
        hovermode='x unified',
        legend=dict(
            bgcolor=COLORES['fondo_cards'],
            bordercolor=COLORES['bordes'],
            borderwidth=1,
            orientation='h',
            y=1.08, x=0
        )
    )
    return fig


# ============================================
# NUEVO: Gráfico de Drawdown
# ============================================

def crear_grafico_drawdown(df_con_dd):
    """Gráfico de Drawdown junto al retorno acumulado."""
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Retorno Acumulado (%)', 'Drawdown (%)'),
        vertical_spacing=0.12,
        row_heights=[0.65, 0.35]
    )

    # Retorno acumulado
    fig.add_trace(go.Scatter(
        x=df_con_dd['Fecha'], y=df_con_dd['Retorno_Acumulado'],
        mode='lines', name='Retorno',
        line=dict(color=COLORES['exito'], width=2.5),
        fill='tozeroy', fillcolor='rgba(45,199,109,0.08)'
    ), row=1, col=1)

    fig.add_hline(y=0, line_color=COLORES['neutro'], line_width=1, row=1, col=1)

    # Drawdown (siempre negativo o cero)
    fig.add_trace(go.Scatter(
        x=df_con_dd['Fecha'], y=df_con_dd['Drawdown'],
        mode='lines', name='Drawdown',
        line=dict(color=COLORES['error'], width=2),
        fill='tozeroy', fillcolor='rgba(255,71,87,0.12)'
    ), row=2, col=1)

    fig.add_hline(y=0, line_color=COLORES['neutro'], line_width=1, row=2, col=1)

    fig.update_layout(
        height=480,
        plot_bgcolor=COLORES['fondo'],
        paper_bgcolor=COLORES['fondo'],
        font=dict(color=COLORES['texto']),
        showlegend=True,
        legend=dict(bgcolor=COLORES['fondo_cards'], bordercolor=COLORES['bordes'], borderwidth=1)
    )
    for r in [1, 2]:
        fig.update_xaxes(tickformat='%d/%m', gridcolor=COLORES['bordes'],
                         tickfont=dict(color=COLORES['texto_secundario']), row=r, col=1)
        fig.update_yaxes(gridcolor=COLORES['bordes'],
                         tickfont=dict(color=COLORES['texto_secundario']), row=r, col=1)
    return fig


# ============================================
# NUEVO: Cards de métricas avanzadas para traders
# ============================================

def _badge(valor, umbrales, etiquetas=("BUENO", "REGULAR", "BAJO")):
    """Devuelve HTML de badge según umbrales (alto=bueno)."""
    if valor >= umbrales[0]:
        return f'<span class="tc-badge badge-ok">✔ {etiquetas[0]}</span>'
    elif valor >= umbrales[1]:
        return f'<span class="tc-badge badge-warn">~ {etiquetas[1]}</span>'
    else:
        return f'<span class="tc-badge badge-bad">✘ {etiquetas[2]}</span>'


def mostrar_cards_trader(ma):
    """
    Fila de 6 cards premium para traders:
    Precisión Global, Sharpe Ratio, Max Drawdown, Profit Factor,
    Win Rate, Sortino Ratio.
    Cada card tiene barra de color superior, valor grande,
    benchmark y badge de semáforo.
    """
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    datos_cards = [
        # (col, color_clase, label, valor_str, bench_txt, badge_html, tooltip)
        (col1, "azul",   "Precisión Global",
         f"{ma['precision']:.1f}%" if 'precision' in ma else "—",
         "Benchmark: >55% supera el azar",
         _badge(ma.get('precision', 0), [65, 55]),
         "% de días en que el modelo acertó la dirección"),

        (col2, "verde",  "Sharpe Ratio",
         f"{ma['sharpe_ratio']:.2f}",
         "Ret. ajustado por riesgo total | >1 = bueno",
         _badge(ma['sharpe_ratio'], [1.0, 0.5], ("BUENO", "ACEPTABLE", "BAJO")),
         "Retorno anualizado / Volatilidad anualizada (rf=0)"),

        (col3, "rojo",   "Max Drawdown",
         f"-{ma['max_drawdown']:.2f}%",
         "Caída máxima desde el pico | <5% = conservador",
         _badge(5 - ma['max_drawdown'], [0, -5], ("BAJO", "MODERADO", "ALTO")),
         "Mayor pérdida acumulada desde un máximo previo"),

        (col4, "naranja","Profit Factor",
         f"{ma['profit_factor']:.2f}",
         "Ganancia bruta / Pérdida bruta | >1.5 = bueno",
         _badge(ma['profit_factor'], [1.5, 1.0], ("BUENO", "ACEPTABLE", "BAJO")),
         "Ratio entre suma de ganancias y suma de pérdidas"),

        (col5, "verde",  "Win Rate",
         f"{ma['win_rate']:.1f}%",
         "% días ganadores | >55% = efectivo",
         _badge(ma['win_rate'], [60, 50], ("ALTO", "MEDIO", "BAJO")),
         "Porcentaje de operaciones con retorno positivo"),

        (col6, "azul",   "Sortino Ratio",
         f"{ma['sortino_ratio']:.2f}",
         "Ret. ajustado solo por riesgo bajista | >1 = bueno",
         _badge(ma['sortino_ratio'], [1.0, 0.3], ("BUENO", "ACEPTABLE", "BAJO")),
         "Como Sharpe pero penaliza solo la volatilidad negativa"),
    ]

    for col, clase, label, valor, bench, badge, tip in datos_cards:
        with col:
            st.markdown(f"""
            <div class="trader-card {clase}" title="{tip}">
                <div class="tc-label">{label}</div>
                <div class="tc-value">{valor}</div>
                <div class="tc-bench">{bench}</div>
                {badge}
            </div>
            """, unsafe_allow_html=True)


# ============================================
# NUEVO: Tabla de operaciones diarias (P&L log)
# ============================================

def mostrar_tabla_operaciones(df):
    """
    Tabla compacta con todas las operaciones del período filtrado.
    Muestra: Fecha, Señal, TC, Variación real, Retorno, Acumulado, Resultado.
    """
    filas = []
    for _, row in df.iterrows():
        if pd.isna(row['Variacion_Dolar']):
            continue
        senal_html = (
            '<span class="pill-long">▲ LONG</span>'
            if row['Prediccion'] == 1
            else '<span class="pill-short">▼ SHORT</span>'
        )
        resultado_html = (
            '<span class="pill-ok">✔ Acierto</span>'
            if row['Acierto']
            else '<span class="pill-err">✘ Error</span>'
        )
        color_ret = COLORES['exito'] if row['Retorno'] >= 0 else COLORES['error']
        color_acc = COLORES['exito'] if row['Retorno_Acumulado'] >= 0 else COLORES['error']
        inf = row.get('influencia_predominante', '—')

        filas.append(f"""
        <tr>
          <td>{row['Fecha'].strftime('%d/%m/%Y')}</td>
          <td>{senal_html}</td>
          <td>S/ {row['Compra']:.4f}</td>
          <td style="color:{COLORES['exito'] if row['Variacion_Dolar']>=0 else COLORES['error']}">
              {row['Variacion_Dolar']:+.3f}%</td>
          <td style="color:{color_ret}; font-weight:700">{row['Retorno']:+.3f}%</td>
          <td style="color:{color_acc}">{row['Retorno_Acumulado']:+.3f}%</td>
          <td>{resultado_html}</td>
          <td style="color:{COLORES['texto_secundario']}; font-size:0.75rem">{inf}</td>
        </tr>
        """)

    tabla_html = f"""
    <div style="overflow-x:auto; max-height:420px; overflow-y:auto;
                border:1px solid {COLORES['bordes']}; border-radius:8px;">
    <table class="op-table">
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Señal</th>
          <th>Tipo Cambio</th>
          <th>Var. Real</th>
          <th>Retorno</th>
          <th>Acumulado</th>
          <th>Resultado</th>
          <th>Influencia Twitter</th>
        </tr>
      </thead>
      <tbody>
        {''.join(filas)}
      </tbody>
    </table>
    </div>
    """
    st.markdown(tabla_html, unsafe_allow_html=True)


# ============================================
# MANUAL DE USUARIO (sin cambios)
# ============================================

def mostrar_guia_rapida():
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
    with st.spinner('Cargando datos del período electoral 2021...'):
        df_completo = cargar_datos_completos()

    if df_completo is None or len(df_completo) == 0:
        st.error("No se pudieron cargar los datos. Verifica la ruta del archivo.")
        return

    # --- Encabezado ---
    col_titulo1, col_titulo2 = st.columns([3, 1])
    with col_titulo1:
        st.markdown('<h1 class="titulo-principal">Predicción de la Direccionalidad del Tipo de Cambio USD/PEN mediante Análisis de Sentimiento en Twitter/X durante Elecciones en Perú</h1>',
                    unsafe_allow_html=True)
        st.markdown('<p class="subtitulo">Sistema predictivo basado en análisis de sentimiento político | Elecciones Presidenciales 2021</p>',
                    unsafe_allow_html=True)
    with col_titulo2:
        fecha_min = df_completo['Fecha'].min()
        fecha_max = df_completo['Fecha'].max()
        st.info(f"**Período disponible:**\n{fecha_min.strftime('%d/%m/%Y')} al {fecha_max.strftime('%d/%m/%Y')}")

    mostrar_guia_rapida()

    # --- Sidebar (sin cambios) ---
    with st.sidebar:
        st.markdown("# Panel de Control")
        st.markdown("---")
        st.markdown('<div class="sidebar-section-title">Período de Análisis</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-help">Selecciona el rango de fechas que deseas analizar</div>', unsafe_allow_html=True)

        fecha_min_disponible = df_completo['Fecha'].min()
        fecha_max_disponible = df_completo['Fecha'].max()

        col_fecha1, col_fecha2 = st.columns(2)
        with col_fecha1:
            fecha_inicio = st.date_input("Desde", value=fecha_min_disponible,
                                          min_value=fecha_min_disponible, max_value=fecha_max_disponible)
        with col_fecha2:
            fecha_fin = st.date_input("Hasta", value=fecha_max_disponible,
                                       min_value=fecha_min_disponible, max_value=fecha_max_disponible)

        if fecha_inicio > fecha_fin:
            st.error("La fecha inicial debe ser anterior a la final")
            fecha_fin = fecha_inicio

        st.markdown("---")
        st.markdown('<div class="sidebar-section-title">Filtro de Resultado</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-help">Analiza solo aciertos o errores del modelo</div>', unsafe_allow_html=True)
        filtro_resultado = st.selectbox("Tipo de resultado",
                                         options=["Todos", "Solo Aciertos", "Solo Errores"], index=0)
        st.markdown("---")
        st.markdown('<div class="sidebar-section-title">Métricas del Período</div>', unsafe_allow_html=True)

        df_filtrado_temp = filtrar_por_fecha(df_completo, fecha_inicio, fecha_fin)
        df_filtrado_temp = filtrar_por_resultado(df_filtrado_temp, filtro_resultado)
        metricas_sidebar = calcular_metricas(df_filtrado_temp)

        if metricas_sidebar:
            st.markdown(f"""
            <div class="sidebar-metric">
                <div class="sidebar-metric-label">Total de Días</div>
                <div class="sidebar-metric-value">{metricas_sidebar['total_dias']}</div>
            </div>
            """, unsafe_allow_html=True)
            color_precision = COLORES['exito'] if metricas_sidebar['precision'] >= 55 else COLORES['advertencia']
            st.markdown(f"""
            <div class="sidebar-metric" style="border-color: {color_precision};">
                <div class="sidebar-metric-label">Precisión Global</div>
                <div class="sidebar-metric-value" style="color: {color_precision};">{metricas_sidebar['precision']:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="sidebar-metric">
                <div class="sidebar-metric-label">Predicciones Correctas</div>
                <div class="sidebar-metric-value" style="color: {COLORES['exito']};">{metricas_sidebar['aciertos']}</div>
            </div>
            """, unsafe_allow_html=True)
            color_retorno = COLORES['exito'] if metricas_sidebar['retorno_total'] > 0 else COLORES['error']
            st.markdown(f"""
            <div class="sidebar-metric" style="border-color: {color_retorno};">
                <div class="sidebar-metric-label">Retorno Acumulado</div>
                <div class="sidebar-metric-value" style="color: {color_retorno};">{metricas_sidebar['retorno_total']:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
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
            ""))

    # --- Datos filtrados ---
    df_filtrado = filtrar_por_fecha(df_completo, fecha_inicio, fecha_fin)
    df_filtrado = filtrar_por_resultado(df_filtrado, filtro_resultado)

    if len(df_filtrado) == 0:
        st.warning("No hay datos disponibles para los filtros seleccionados.")
        return

    metricas   = calcular_metricas(df_filtrado)
    ma         = calcular_metricas_avanzadas(df_filtrado)   # ← NUEVO: cálculo único
    ma['precision'] = metricas.get('precision', 0)          # añadir precision al dict

    # ============================================
    # NUEVO: Fila de 6 cards para traders (reemplaza las 4 cards originales)
    # ============================================
    st.markdown("## Desempeño del Modelo Predictivo")
    mostrar_cards_trader(ma)

    # Advertencia de sesgo temporal (debajo de las cards)
    st.markdown(f"""
    <div class="bias-warning">
        ⚠️ <b>Nota metodológica:</b> Las métricas anualizadas (Sharpe, Calmar, Retorno anual)
        se calculan sobre un período de ~2 meses. Interprétalas como indicadores de dirección,
        no como proyecciones reales de rendimiento anual.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ============================================
    # PESTAÑAS PRINCIPALES (tab1 y tab2 sin cambios internos;
    # tab3 mejorado con Drawdown + tabla; tab4 nuevo)
    # ============================================
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Vista Principal",
        "🧠 Análisis Detallado",
        "💰 Retorno y Desempeño",
        "🐦 Composición Política"   # ← TAB NUEVO
    ])

    # ------ TAB 1: sin cambios ------
    with tab1:
        st.markdown("### Evolución del Tipo de Cambio con Predicciones del Modelo")
        col_info1, col_info2, col_info3, col_info4 = st.columns(4)
        with col_info1:
            st.caption(f"**Período:** {fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}")
        with col_info2:
            tc_i = df_filtrado['Compra'].iloc[0]
            tc_f = df_filtrado['Compra'].iloc[-1]
            var_p = (tc_f - tc_i) / tc_i * 100
            st.caption(f"**TC Variación:** S/ {tc_i:.3f} → S/ {tc_f:.3f} ({var_p:+.2f}%)")
        with col_info3:
            st.caption(f"**Señales:** {metricas['dias_sube']} LONG | {metricas['dias_baja']} SHORT")
        with col_info4:
            st.caption(f"**Filtro activo:** {filtro_resultado}")

        fig_principal = crear_grafico_principal(df_filtrado)
        st.plotly_chart(fig_principal, use_container_width=True)

        st.markdown(f"""
        <div style='background: {COLORES['fondo_cards']}; padding: 10px; border-radius: 6px; margin-top: 10px;'>
            <span style='color: {COLORES['texto_secundario']}; font-size: 0.85rem;'><b>Leyenda:</b></span>
            <span style='color:{COLORES['exito']}; margin-left: 15px;'>▲ Acierto SUBE</span>
            <span style='color:{COLORES['exito']}; margin-left: 15px;'>▼ Acierto BAJA</span>
            <span style='color:{COLORES['error']}; margin-left: 15px;'>● Error</span>
            <span style='color:{COLORES['primario']}; margin-left: 15px;'>━ Tipo de cambio</span>
        </div>
        """, unsafe_allow_html=True)

        if len(df_filtrado) > 0:
            st.markdown("---")
            st.markdown("### Resumen de Operaciones Destacadas")
            col_dest1, col_dest2, col_dest3 = st.columns(3)
            with col_dest1:
                mejor_op = df_filtrado.loc[df_filtrado['Retorno'].idxmax()]
                st.markdown(f"""
                <div style='background:{COLORES['fondo_cards']};padding:12px;border-radius:6px;border-left:3px solid {COLORES['exito']};'>
                    <b style='color:{COLORES['exito']};'>Mejor Operación</b><br>
                    <span style='color:{COLORES['texto_secundario']};font-size:0.85rem;'>
                    Fecha: {mejor_op['Fecha'].strftime('%d/%m/%Y')}<br>
                    Retorno: <b style='color:{COLORES['exito']};'>{mejor_op['Retorno']:+.3f}%</b><br>
                    Señal: {'▲ LONG' if mejor_op['Prediccion']==1 else '▼ SHORT'} | TC varió {mejor_op['Variacion_Dolar']:+.3f}%
                    </span>
                </div>
                """, unsafe_allow_html=True)
            with col_dest2:
                peor_op = df_filtrado.loc[df_filtrado['Retorno'].idxmin()]
                st.markdown(f"""
                <div style='background:{COLORES['fondo_cards']};padding:12px;border-radius:6px;border-left:3px solid {COLORES['error']};'>
                    <b style='color:{COLORES['error']};'>Peor Operación</b><br>
                    <span style='color:{COLORES['texto_secundario']};font-size:0.85rem;'>
                    Fecha: {peor_op['Fecha'].strftime('%d/%m/%Y')}<br>
                    Retorno: <b style='color:{COLORES['error']};'>{peor_op['Retorno']:+.3f}%</b><br>
                    Señal: {'▲ LONG' if peor_op['Prediccion']==1 else '▼ SHORT'} | TC varió {peor_op['Variacion_Dolar']:+.3f}%
                    </span>
                </div>
                """, unsafe_allow_html=True)
            with col_dest3:
                mayor_vol = df_filtrado.loc[df_filtrado['Variacion_Dolar'].abs().idxmax()]
                color_vol = COLORES['exito'] if mayor_vol['Acierto'] else COLORES['error']
                st.markdown(f"""
                <div style='background:{COLORES['fondo_cards']};padding:12px;border-radius:6px;border-left:3px solid {COLORES['advertencia']};'>
                    <b style='color:{COLORES['advertencia']};'>Mayor Volatilidad</b><br>
                    <span style='color:{COLORES['texto_secundario']};font-size:0.85rem;'>
                    Fecha: {mayor_vol['Fecha'].strftime('%d/%m/%Y')}<br>
                    Variación: <b>{mayor_vol['Variacion_Dolar']:+.3f}%</b><br>
                    Predicción: <b style='color:{color_vol};'>{'Correcta ✔' if mayor_vol['Acierto'] else 'Incorrecta ✘'}</b>
                    </span>
                </div>
                """, unsafe_allow_html=True)

        # NUEVO: Tabla de operaciones al final de tab1
        st.markdown("---")
        st.markdown("### 📋 Log de Operaciones Diarias")
        st.caption("Cada fila es un día de operación. La señal LONG/SHORT la genera el modelo 24h antes.")
        mostrar_tabla_operaciones(df_filtrado)

    # ------ TAB 2: sin cambios ------
    with tab2:
        st.markdown("### Análisis Detallado del Sentimiento y Variación")
        fig_combinado = crear_grafico_sentimiento_variacion(df_filtrado)
        st.plotly_chart(fig_combinado, use_container_width=True)

        st.markdown(f"""
        <div style='background:{COLORES['fondo_cards']};padding:12px;border-radius:6px;border-left:3px solid {COLORES['primario']};margin:10px 0;'>
            <span style='color:{COLORES['primario']};font-weight:600;'>INFO:</span>
            <span style='color:{COLORES['texto_secundario']};font-size:0.9rem;'>
            Pase el mouse sobre los puntos del gráfico de sentimiento para ver: <b>Influencia predominante</b>
            (Anti-Castillo/Anti-Keiko/Neutral), <b>distribución de tweets</b> y <b>razones principales</b> detectadas.
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Análisis Cuantitativo del Modelo")
        col_analisis1, col_analisis2 = st.columns(2)
        with col_analisis1:
            corr_sentimiento = df_filtrado['sentimiento_numerico'].corr(df_filtrado['Variacion_Dolar'])
            fortaleza = "Débil" if abs(corr_sentimiento) < 0.3 else "Moderada" if abs(corr_sentimiento) < 0.5 else "Fuerte"
            st.metric("Coeficiente de Correlación (lag 0)", f"{corr_sentimiento:.3f}",
                      f"Señal {fortaleza} — sentimiento mismo día vs dólar")
            volatilidad = df_filtrado['Variacion_Dolar'].std()
            st.metric("Volatilidad Diaria / Anualizada",
                      f"{volatilidad:.2f}% / {volatilidad * np.sqrt(252):.1f}%",
                      "Medida de riesgo del mercado cambiario")
        with col_analisis2:
            retornos_pos = df_filtrado[df_filtrado['Retorno'] > 0]['Retorno'].sum()
            retornos_neg = abs(df_filtrado[df_filtrado['Retorno'] < 0]['Retorno'].sum())
            pf = retornos_pos / retornos_neg if retornos_neg > 0 else 0
            st.metric("Profit Factor", f"{pf:.2f}", "Ganancia bruta / Pérdida bruta (>1.5 = bueno)")
            expectativa = df_filtrado['Retorno'].mean()
            st.metric("Expectativa Matemática", f"{expectativa:+.3f}% / día",
                      f"Proyección referencial anual: {expectativa * 252:+.1f}%")

    # ------ TAB 3: MEJORADO con Drawdown ---
    with tab3:
        st.markdown("### Retorno y Desempeño del Modelo")

        # Gráfico combinado retorno + drawdown (nuevo)
        fig_dd = crear_grafico_drawdown(ma['df_con_drawdown'])
        st.plotly_chart(fig_dd, use_container_width=True)

        # Matriz de desempeño (sin cambios)
        col_retorno1, col_retorno2 = st.columns([2, 1])
        with col_retorno1:
            st.markdown(f"""
            <div style='background:{COLORES['fondo_cards']};padding:14px;border-radius:8px;
                        border:1px solid {COLORES['bordes']};margin-bottom:1rem;'>
                <b style='color:{COLORES['texto_secundario']};font-size:0.8rem;text-transform:uppercase;
                           letter-spacing:0.5px;'>Resumen de Riesgo</b><br><br>
                <span style='color:{COLORES['texto']};font-size:0.9rem;'>
                • Max Drawdown: <b style='color:{COLORES['error']};'>-{ma['max_drawdown']:.2f}%</b><br>
                • Recovery Factor: <b style='color:{COLORES['exito']};'>{ma['recovery_factor']:.2f}x</b>
                  (retorno / max caída)<br>
                • Calmar Ratio: <b>{ma['calmar_ratio']:.2f}</b>
                  (ret. anualizado / drawdown)<br>
                • Win Rate: <b>{ma['win_rate']:.1f}%</b> |
                  Avg Win: <b style='color:{COLORES['exito']};'>{ma['avg_win']:+.3f}%</b> |
                  Avg Loss: <b style='color:{COLORES['error']};'>{ma['avg_loss']:+.3f}%</b>
                </span>
            </div>
            """, unsafe_allow_html=True)
        with col_retorno2:
            fig_matriz = crear_grafico_matriz_desempeno(metricas)
            st.plotly_chart(fig_matriz, use_container_width=True)

        st.markdown("---")
        st.markdown("### Análisis de Performance Trading")

        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        with col_r1:
            st.metric("Profit Factor", f"{ma['profit_factor']:.2f}", "Ganancia/Pérdida total (>1.5 = bueno)")
        with col_r2:
            st.metric("Recovery Factor", f"{ma['recovery_factor']:.2f}", "Retorno / Drawdown máximo")
        with col_r3:
            st.metric("Expectativa Matemática", f"{df_filtrado['Retorno'].mean():+.3f}%",
                      f"Win: {ma['avg_win']:.3f}% | Loss: {ma['avg_loss']:.3f}%")
        with col_r4:
            st.metric("Calmar Ratio", f"{ma['calmar_ratio']:.2f}",
                      f"Ret.Anual ref.: {ma['retorno_anualizado']:+.1f}%")

        st.markdown("---")
        col_e1, col_e2, col_e3, col_e4 = st.columns(4)
        with col_e1:
            st.metric("Precisión Ponderada", f"{ma['precision_ponderada']:.1f}%", "Por magnitud de movimiento")
        with col_e2:
            st.metric("Payoff Ratio", f"{ma['payoff_ratio']:.2f}", "Ganancia media / Pérdida media")
        with col_e3:
            st.metric("Racha Máxima", f"+{ma['max_win_streak']} / -{ma['max_loss_streak']}",
                      "Días ganadores / perdedores")
        with col_e4:
            st.metric("Sortino Ratio", f"{ma['sortino_ratio']:.2f}", "Ajuste por riesgo bajista")

        # Advertencia sesgo temporal
        st.markdown(f"""
        <div class="bias-warning">
            ⚠️ <b>Sesgo temporal:</b> Calmar Ratio {ma['calmar_ratio']:.1f} y Retorno anual ref. {ma['retorno_anualizado']:+.1f}%
            se calculan linealizando ~2 meses a 252 días. Este período electoral es atípico en volatilidad.
            Úsalos como referencia relativa, no como proyección.
        </div>
        """, unsafe_allow_html=True)

    # ------ TAB 4: NUEVO — Composición Política ------
    with tab4:
        st.markdown("### 🐦 Composición del Sentimiento Político en Twitter")
        st.markdown(f"""
        <div style='background:{COLORES['fondo_cards']};padding:12px;border-radius:6px;
                    border-left:3px solid {COLORES['primario']};margin-bottom:1rem;'>
            <span style='color:{COLORES['primario']};font-weight:600;'>¿Por qué importa este gráfico?</span><br>
            <span style='color:{COLORES['texto_secundario']};font-size:0.88rem;'>
            La narrativa Anti-Castillo en Twitter se asocia con <b style='color:{COLORES['error']};'>mayor incertidumbre</b>
            → el mercado huye al dólar → <b>dólar sube</b>. La narrativa Anti-Keiko reduce el miedo
            al socialismo → <b>dólar baja</b>. Este gráfico muestra cómo esa batalla narrativa evolucionó día a día.
            </span>
        </div>
        """, unsafe_allow_html=True)

        fig_comp = crear_grafico_composicion_politica(df_filtrado)
        st.plotly_chart(fig_comp, use_container_width=True)

        # Estadísticas de composición
        st.markdown("---")
        st.markdown("### Estadísticas de Composición por Período")
        col_c1, col_c2, col_c3, col_c4 = st.columns(4)

        prom_ac = df_filtrado['pct_anti_castillo'].mean()
        prom_ak = df_filtrado['pct_anti_keiko'].mean()
        prom_n  = df_filtrado['pct_neutral'].mean()
        total_t = df_filtrado['total_tweets'].sum() if 'total_tweets' in df_filtrado.columns else 0

        with col_c1:
            st.markdown(f"""
            <div class="trader-card rojo">
                <div class="tc-label">Promedio Anti-Castillo</div>
                <div class="tc-value" style="color:{COLORES['error']};">{prom_ac:.1f}%</div>
                <div class="tc-bench">Asociado a presión alcista del dólar</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c2:
            st.markdown(f"""
            <div class="trader-card naranja">
                <div class="tc-label">Promedio Anti-Keiko</div>
                <div class="tc-value" style="color:{COLORES['advertencia']};">{prom_ak:.1f}%</div>
                <div class="tc-bench">Asociado a presión bajista del dólar</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c3:
            st.markdown(f"""
            <div class="trader-card azul">
                <div class="tc-label">Promedio Neutral</div>
                <div class="tc-value" style="color:{COLORES['neutro']};">{prom_n:.1f}%</div>
                <div class="tc-bench">Sin señal política predominante</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c4:
            st.markdown(f"""
            <div class="trader-card verde">
                <div class="tc-label">Total Tweets Analizados</div>
                <div class="tc-value" style="color:{COLORES['exito']};">{int(total_t):,}</div>
                <div class="tc-bench">Volumen del corpus de datos</div>
            </div>
            """, unsafe_allow_html=True)

        # Días de predominancia
        st.markdown("---")
        st.markdown("### Días por Narrativa Predominante")
        col_d1, col_d2, col_d3 = st.columns(3)
        dias_ac = (df_filtrado['influencia_predominante'] == 'Anti-Castillo').sum()
        dias_ak = (df_filtrado['influencia_predominante'] == 'Anti-Keiko').sum()
        dias_n  = (df_filtrado['influencia_predominante'] == 'Neutral/Mixto').sum()
        total_dias = len(df_filtrado)

        for col, label, dias, color in [
            (col_d1, "Anti-Castillo dominó", dias_ac, COLORES['error']),
            (col_d2, "Anti-Keiko dominó",    dias_ak, COLORES['advertencia']),
            (col_d3, "Neutral/Mixto",         dias_n,  COLORES['neutro'])
        ]:
            with col:
                pct = dias / total_dias * 100 if total_dias > 0 else 0
                st.markdown(f"""
                <div style='background:{COLORES['fondo_cards']};padding:14px;border-radius:8px;
                            border:1px solid {COLORES['bordes']};text-align:center;'>
                    <div style='font-size:0.75rem;color:{COLORES['texto_secundario']};
                                text-transform:uppercase;letter-spacing:0.5px;'>{label}</div>
                    <div style='font-size:2.2rem;font-weight:800;color:{color};'>{dias}</div>
                    <div style='font-size:0.8rem;color:{COLORES['texto_secundario']};'>
                        días ({pct:.1f}% del período)</div>
                    <div style='background:{COLORES['fondo']};border-radius:4px;
                                height:6px;margin-top:8px;'>
                        <div style='background:{color};border-radius:4px;
                                    height:6px;width:{pct:.1f}%;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # --- Footer (sin cambios) ---
    st.markdown("---")
    col_footer1, col_footer2, col_footer3 = st.columns([1, 2, 1])
    with col_footer2:
        st.markdown(f"""
        <div style="text-align:center;color:{COLORES['texto_secundario']};padding:20px;font-size:0.9rem;">
            <div style="margin-bottom:10px;">
                <strong>Modelo Predictivo - Análisis de Sentimiento en Twitter/X</strong><br>
                Período: Elecciones Presidenciales Perú 2021 (Abril-Mayo)
            </div>
            <div>
                Precisión: <span style="color:{COLORES['exito']}">{metricas['precision']:.1f}%</span> |
                Retorno: <span style="color:{COLORES['exito'] if metricas['retorno_total'] > 0 else COLORES['error']}">{metricas['retorno_total']:+.2f}%</span> |
                Sharpe: <span style="color:{COLORES['primario']}">{ma['sharpe_ratio']:.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
