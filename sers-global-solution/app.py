"""
SERS Global Solution - Dashboard Principal
Sistema de Eficiência Energética e Sustentabilidade Corporativa
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import sys
import os

# Configuração de imports
sys.path.append(os.path.dirname(__file__))

try:
    from data_analyzer import EnergyAnalyzer
    from solar_simulator import SolarSimulator
except ImportError as e:
    st.error(f"Erro ao importar módulos: {e}")
    st.stop()

def setup_page():
    """Configuração inicial da página Streamlit"""
    st.set_page_config(
        page_title="SERS Global Solution",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS customizado - Tema Escuro Melhorado
    st.markdown("""
    <style>
    /* Configuração geral do tema escuro */
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    .stApp {
        background-color: #0e1117;
    }
    
    /* Improved spacing and layout */
    .main-header {
        font-size: 3rem;
        background: linear-gradient(90deg, #00d4ff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 700;
        padding-top: 1rem;
    }
    
    .sub-header {
        font-size: 1.6rem;
        color: #b0b0b0;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    .section-header {
        color: #00d4ff;
        border-bottom: 3px solid #00d4ff;
        padding-bottom: 1rem;
        margin-top: 3rem;
        margin-bottom: 2rem;
        font-weight: 600;
        font-size: 1.8rem;
    }
    
    /* More spacious metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #333333;
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        color: #ffffff;
        text-align: center;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.5);
        border: 1px solid #00d4ff;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #b0b0b0;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        color: #00d4ff;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .metric-unit {
        font-size: 0.9rem;
        color: #b0b0b0;
        font-weight: 400;
    }
    
    /* More spacious boxes */
    .info-box, .success-box, .warning-box {
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .info-box {
        background: linear-gradient(135deg, #1a2a3a 0%, #2a3a4a 100%);
        border: 1px solid #00d4ff;
    }
    
    .success-box {
        background: linear-gradient(135deg, #1a2a1a 0%, #2a3a2a 100%);
        border: 1px solid #00ff88;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #2a2a1a 0%, #3a3a2a 100%);
        border: 1px solid #ffaa00;
    }
    
    .recommendation-high {
        background: linear-gradient(135deg, #2a1a1a 0%, #3d1f1f 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #ff4444;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(255, 68, 68, 0.3);
        color: #ffffff;
    }
    
    .recommendation-medium {
        background: linear-gradient(135deg, #2a2a1a 0%, #3d3d1f 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #ffaa00;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(255, 170, 0, 0.3);
        color: #ffffff;
    }
    
    .recommendation-low {
        background: linear-gradient(135deg, #1a2a1a 0%, #1f3d1f 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #00ff88;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 255, 136, 0.3);
        color: #ffffff;
    }
    
    /* Better tab spacing */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        padding: 1rem 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 1rem 1.5rem;
        font-size: 2em;
        margin: 0 0.5rem;
        background-color: #2d2d2d;
        border-radius: 8px;
        font-weight: 600;
        color: #b0b0b0;
        border: 1px solid #333333;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00d4ff;
        color: #000000;
        border: 1px solid #00d4ff;
    }
    
    .sidebar .sidebar-content {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        color: #000000;
        border: none;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        font-size: 1.1rem;
        margin: 1rem 0;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 212, 255, 0.4);
        background: linear-gradient(135deg, #00ff88 0%, #00d4ff 100%);
    }
    
    /* Better column spacing */
    [data-testid="column"] {
        padding: 0 1rem;
    }
    
    /* Improved list spacing */
    ol, ul {
        line-height: 1.8;
    }
    
    li {
        margin-bottom: 1rem;
        padding-left: 0.5rem;
    }
    
    /* Estilos para elementos do Streamlit no tema escuro */
    .stSlider > div > div > div {
        color: #ffffff;
    }
    
    .stSelectbox > div > div {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #333333;
    }
    
    .stSelectbox > div > div:hover {
        border: 1px solid #00d4ff;
    }
    
    .stNumberInput > div > div > input {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #333333;
    }
    
    .stDataFrame {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    /* Ajustes para textos gerais */
    p, li, span, div {
        color: #ffffff !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Ajustes para gráficos Plotly */
    .js-plotly-plot .plotly .modebar {
        background-color: #1e1e1e !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

def main():
    """Função principal do dashboard"""
    setup_page()
    
    # Cabeçalho principal com mais espaço
    st.markdown('<div style="padding: 2rem 0;">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-header">SERS Global Solution</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Sistema de Eficiência Energética e Sustentabilidade</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Inicialização dos módulos
    try:
        analyzer = EnergyAnalyzer()
        solar_simulator = SolarSimulator()
    except Exception as e:
        st.error(f"Erro ao inicializar módulos: {e}")
        return
    
    # Sidebar - Configurações com mais espaço
    st.sidebar.markdown('<div style="padding: 1rem 0;">', unsafe_allow_html=True)
    st.sidebar.header("⚙️ Configurações da Análise")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown('<div style="padding: 1rem 0;">', unsafe_allow_html=True)
    st.sidebar.subheader("📊 Dados de Consumo")
    analysis_days = st.sidebar.slider("Período de Análise (dias)", 1, 30, 7)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown('<div style="padding: 1rem 0;">', unsafe_allow_html=True)
    st.sidebar.subheader("☀️ Simulação Solar")
    state = st.sidebar.selectbox(
        "Estado da Instalação", 
        options=list(solar_simulator.irradiation.keys()),
        index=0
    )
    
    available_area = st.sidebar.slider("Área Disponível para Painéis (m²)", 20, 200, 50)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Botão de execução principal com mais espaço
    st.sidebar.markdown('<div style="padding: 2rem 0;">', unsafe_allow_html=True)
    if st.sidebar.button("🚀 Executar Análise Completa", type="primary"):
        execute_analysis(analyzer, solar_simulator, analysis_days, state, available_area)
    else:
        show_initial_screen()
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Informações na sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='background-color: #1a2a3a; padding: 1.5rem; border-radius: 12px; border: 1px solid #00d4ff;'>
        <h4 style='color: #00d4ff; margin-top: 0; margin-bottom: 1rem;'>ℹ️ Sobre esta solução:</h4>
        <ul style='color: #ffffff; line-height: 1.6;'>
            <li style='margin-bottom: 0.5rem;'>Análise de padrões de consumo energético</li>
            <li style='margin-bottom: 0.5rem;'>Detecção de desperdícios e otimizações</li>
            <li style='margin-bottom: 0.5rem;'>Simulação de viabilidade de energia solar</li>
            <li style='margin-bottom: 0.5rem;'>Cálculo de impacto ambiental e financeiro</li>
        </ul>
        <p style='color: #b0b0b0; font-size: 0.9rem; margin-bottom: 0; margin-top: 1rem;'><em>Desenvolvido para o projeto SERS Global Solution</em></p>
    </div>
    """, unsafe_allow_html=True)

def show_initial_screen():
    """Mostra tela inicial antes da análise"""
    st.markdown("""
    <div class="info-box">
        <h3 style='color: #00d4ff; margin-top: 0; margin-bottom: 1.5rem;'>👋 Bem-vindo ao SERS Global Solution</h3>
        <p style='color: #ffffff; margin-bottom: 1rem; line-height: 1.6;'>Configure os parâmetros na barra lateral e clique em <strong style='color: #00ff88;'>Executar Análise Completa</strong> para:</p>
        <ul style='color: #ffffff; line-height: 1.6;'>
            <li style='margin-bottom: 0.5rem;'>Analisar padrões de consumo energético</li>
            <li style='margin-bottom: 0.5rem;'>Identificar oportunidades de economia</li>
            <li style='margin-bottom: 0.5rem;'>Simular viabilidade de energia solar</li>
            <li style='margin-bottom: 0.5rem;'>Calcular impacto ambiental</li>
        </ul>
        <p style='color: #b0b0b0; margin-bottom: 0; margin-top: 1rem;'><em>Solução desenvolvida para eficiência energética corporativa</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-box">
            <h4 style='color: #00ff88; margin-top: 0; margin-bottom: 1rem;'>💡 Benefícios Esperados</h4>
            <ul style='color: #ffffff; line-height: 1.6;'>
                <li style='margin-bottom: 0.5rem;'>Redução de custos energéticos</li>
                <li style='margin-bottom: 0.5rem;'>Melhoria na eficiência operacional</li>
                <li style='margin-bottom: 0.5rem;'>Sustentabilidade ambiental</li>
                <li style='margin-bottom: 0;'>Retorno sobre investimento</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
            <h4 style='color: #ffaa00; margin-top: 0; margin-bottom: 1rem;'>📈 Como Funciona</h4>
            <ol style='color: #ffffff; line-height: 1.6;'>
                <li style='margin-bottom: 0.5rem;'>Coleta dados de consumo</li>
                <li style='margin-bottom: 0.5rem;'>Analisa padrões e desperdícios</li>
                <li style='margin-bottom: 0.5rem;'>Simula soluções energéticas</li>
                <li style='margin-bottom: 0;'>Apresenta recomendações</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

def execute_analysis(analyzer, solar_simulator, analysis_days, state, available_area):
    """Executa a análise completa e exibe resultados"""
    with st.spinner("🔄 Processando dados e gerando insights..."):
        time.sleep(2)
        
        try:
            # 1. Geração e análise de dados de consumo
            consumption_data = analyzer.generate_consumption_data(analysis_days)
            consumption_insights = analyzer.analyze_consumption_patterns(consumption_data)
            recommendations = analyzer.generate_recommendations(consumption_insights)
            
            # 2. Simulação de energia solar
            solar_simulation = solar_simulator.calculate_feasibility(
                consumption_insights['total_consumption'], state, available_area
            )
            
            classification = solar_simulator.classify_feasibility(solar_simulation)
            
            # 3. Geração de cenários comparativos
            scenarios = solar_simulator.generate_comparative_scenarios(
                consumption_insights['total_consumption'], state
            )
            
        except Exception as e:
            st.error(f"Erro durante a análise: {e}")
            return
    
    # Exibição dos resultados em abas
    display_results_in_tabs(consumption_data, consumption_insights, recommendations, 
                           solar_simulation, classification, scenarios)

def display_results_in_tabs(consumption_data, consumption_insights, recommendations, 
                           solar_simulation, classification, scenarios):
    """Exibe os resultados da análise em abas organizadas"""
    
    # Criar abas para organização
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Resumo Executivo", 
        "🔍 Análise de Consumo", 
        "☀️ Energia Solar", 
        "💡 Recomendações", 
        "📈 Cenários"
    ])
    
    with tab1:
        display_executive_summary(consumption_insights, solar_simulation, classification, recommendations)
    
    with tab2:
        display_consumption_analysis(consumption_data, consumption_insights)
    
    with tab3:
        display_solar_analysis(solar_simulation, classification)
    
    with tab4:
        display_recommendations(recommendations)
    
    with tab5:
        display_scenarios_comparison(scenarios, solar_simulation)

def display_executive_summary(consumption_insights, solar_simulation, classification, recommendations):
    """Exibe o resumo executivo na primeira aba"""
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">📋 Resumo Executivo</h3>', unsafe_allow_html=True)
    
    # Métricas principais com mais espaço
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Consumo Total</div>
            <div class="metric-value">{consumption_insights['total_consumption']:,.0f}</div>
            <div class="metric-unit">kWh</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Autossuficiência Solar</div>
            <div class="metric-value" style="color: #00ff88;">{solar_simulation['self_sufficiency']}%</div>
            <div class="metric-unit">do consumo</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Viabilidade</div>
            <div class="metric-value" style="font-size: 1.6rem;">{classification['classification']}</div>
            <div class="metric-unit">Projeto solar</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Economia Anual</div>
            <div class="metric-value" style="color: #00ff88;">R$ {solar_simulation['monthly_savings'] * 12:,.0f}</div>
            <div class="metric-unit">com energia solar</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Espaço entre seções
    st.markdown('<div style="margin: 3rem 0;"></div>', unsafe_allow_html=True)
    
    # Análise de oportunidades
    st.markdown("### 🎯 Principais Oportunidades")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="success-box">
            <h4 style='color: #00ff88; margin-top: 0; margin-bottom: 1rem;'>💸 Redução de Custos</h4>
            <p style='color: #ffffff; margin-bottom: 0; line-height: 1.6;'>
                Potencial de economia de até <strong style='color: #00ff88;'>{consumption_insights['night_waste'] + 10:.1f}%</strong> 
                com otimizações identificadas
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-box">
            <h4 style='color: #00d4ff; margin-top: 0; margin-bottom: 1rem;'>☀️ Energia Solar</h4>
            <p style='color: #ffffff; margin-bottom: 0; line-height: 1.6;'>
                <strong style='color: #00d4ff;'>{solar_simulation['self_sufficiency']}%</strong> do consumo 
                pode ser atendido por energia solar
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="warning-box">
            <h4 style='color: #ffaa00; margin-top: 0; margin-bottom: 1rem;'>🌱 Sustentabilidade</h4>
            <p style='color: #ffffff; margin-bottom: 0; line-height: 1.6;'>
                Redução de <strong style='color: #ffaa00;'>{solar_simulation['co2_reduction']}</strong> 
                toneladas de CO₂ por ano
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ROI do Projeto</div>
            <div class="metric-value" style="color: #00d4ff;">{solar_simulation['roi_25_years']}%</div>
            <div class="metric-unit">em 25 anos</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Mais espaço
    st.markdown('<div style="margin: 3rem 0;"></div>', unsafe_allow_html=True)
    
    # Próximos passos
    st.markdown("### 🚀 Próximos Passos Recomendados")
    st.markdown("""
    <div style='background-color: #2d2d2d; padding: 2rem; border-radius: 12px; border: 1px solid #333333;'>
        <ol style='color: #ffffff; line-height: 2;'>
            <li style='margin-bottom: 1rem; padding-left: 1rem;'><strong style='color: #00d4ff;'>Implementar automação</strong> para reduzir desperdício noturno</li>
            <li style='margin-bottom: 1rem; padding-left: 1rem;'><strong style='color: #00d4ff;'>Realizar estudo detalhado</strong> de viabilidade solar</li>
            <li style='margin-bottom: 1rem; padding-left: 1rem;'><strong style='color: #00d4ff;'>Desenvolver campanha</strong> de conscientização para colaboradores</li>
            <li style='margin-bottom: 1rem; padding-left: 1rem;'><strong style='color: #00d4ff;'>Implementar sistema</strong> de monitoramento contínuo</li>
            <li style='padding-left: 1rem;'><strong style='color: #00d4ff;'>Avaliar financiamento</strong> para projeto de energia solar</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close tab-container

def display_consumption_analysis(consumption_data, consumption_insights):
    """Exibe a análise de consumo na segunda aba"""
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">🔍 Análise de Consumo Energético</h3>', unsafe_allow_html=True)
    
    # Métricas de consumo
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Horário de Pico</div>
            <div class="metric-value">{consumption_insights['peak_hour']}h</div>
            <div class="metric-unit">Maior consumo médio</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Desperdício Noturno</div>
            <div class="metric-value" style="color: #ff4444;">{consumption_insights['night_waste']}%</div>
            <div class="metric-unit">0h-6h otimizável</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Consumo Fora do Expediente</div>
            <div class="metric-value" style="color: #ffaa00;">{consumption_insights['off_hours_consumption']}%</div>
            <div class="metric-unit">fora de 8h-18h</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Maior Consumo</div>
            <div class="metric-value" style="font-size: 1.6rem;">{consumption_insights['highest_consumption_dept']}</div>
            <div class="metric-unit">Departamento</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Espaço entre seções
    st.markdown('<div style="margin: 3rem 0;"></div>', unsafe_allow_html=True)
    
    # Gráficos de análise
    st.markdown("### 📊 Visualização de Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de consumo por hora com tema escuro
        hourly_consumption = consumption_data.groupby('hour')['consumption_kwh'].mean().reset_index()
        fig_hour = px.line(
            hourly_consumption, 
            x='hour', 
            y='consumption_kwh',
            title="Consumo Médio por Hora do Dia",
            labels={'hour': 'Hora do Dia', 'consumption_kwh': 'Consumo (kWh)'}
        )
        fig_hour.update_traces(line_color='#00d4ff', line_width=3)
        fig_hour.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font=dict(color='#ffffff'),
            xaxis=dict(gridcolor='#333333', showgrid=True),
            yaxis=dict(gridcolor='#333333', showgrid=True),
            title_font=dict(size=20)
        )
        fig_hour.add_vrect(x0=8, x1=18, fillcolor="#00d4ff", opacity=0.1, 
                          annotation_text="Horário Comercial", annotation_position="top left")
        st.plotly_chart(fig_hour, use_container_width=True)
    
    with col2:
        # Gráfico de consumo por departamento com tema escuro
        dept_consumption = consumption_data.groupby('department')['consumption_kwh'].sum().reset_index()
        fig_dept = px.pie(
            dept_consumption,
            values='consumption_kwh',
            names='department',
            title="Distribuição do Consumo por Departamento",
            color_discrete_sequence=['#00d4ff', '#00ff88', '#ffaa00', '#ff4444']
        )
        fig_dept.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font=dict(color='#ffffff'),
            title_font=dict(size=20)
        )
        st.plotly_chart(fig_dept, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close tab-container

def display_solar_analysis(solar_simulation, classification):
    """Exibe a análise de energia solar na terceira aba"""
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">☀️ Análise de Energia Solar</h3>', unsafe_allow_html=True)
    
    # Status de viabilidade
    st.markdown(f"""
    <div style='background-color: {'#1a2a1a' if classification['color'] == 'green' else '#2a2a1a' if classification['color'] == 'orange' else '#2a1a1a' if classification['color'] == 'red' else '#1a2a3a'}; 
                padding: 2rem; border-radius: 12px; border-left: 6px solid {'#00ff88' if classification['color'] == 'green' else '#ffaa00' if classification['color'] == 'orange' else '#ff4444' if classification['color'] == 'red' else '#00d4ff'}; 
                margin-bottom: 2rem;'>
        <h4 style='color: {'#00ff88' if classification['color'] == 'green' else '#ffaa00' if classification['color'] == 'orange' else '#ff4444' if classification['color'] == 'red' else '#00d4ff'}; margin-top: 0; margin-bottom: 1rem;'>
            {classification['classification']}
        </h4>
        <p style='color: #ffffff; margin-bottom: 0; line-height: 1.6;'>{classification['recommendation']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas solares
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Potência Instalável</div>
            <div class="metric-value">{solar_simulation['installed_power']}</div>
            <div class="metric-unit">kWp</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Geração Mensal</div>
            <div class="metric-value" style="color: #00ff88;">{solar_simulation['monthly_generation']:,.0f}</div>
            <div class="metric-unit">kWh</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Investimento Total</div>
            <div class="metric-value" style="color: #00d4ff;">R$ {solar_simulation['total_investment']:,.0f}</div>
            <div class="metric-unit">Sistema solar</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Payback</div>
            <div class="metric-value" style="color: #ffaa00;">{solar_simulation['payback_years']}</div>
            <div class="metric-unit">anos</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Espaço entre seções
    st.markdown('<div style="margin: 3rem 0;"></div>', unsafe_allow_html=True)
    
    # Detalhes financeiros e ambientais
    st.markdown("### 💰 Análise Financeira e Ambiental")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Financeiro")
        st.markdown(f"""
        <div style='background-color: #2d2d2d; padding: 2rem; border-radius: 12px; border: 1px solid #333333;'>
            <p style='color: #ffffff; margin-bottom: 1rem; line-height: 1.6;'><strong style='color: #00d4ff;'>Investimento Total:</strong> R$ {solar_simulation['total_investment']:,.2f}</p>
            <p style='color: #ffffff; margin-bottom: 1rem; line-height: 1.6;'><strong style='color: #00d4ff;'>Economia Mensal:</strong> R$ {solar_simulation['monthly_savings']:,.2f}</p>
            <p style='color: #ffffff; margin-bottom: 1rem; line-height: 1.6;'><strong style='color: #00d4ff;'>Economia Anual:</strong> R$ {solar_simulation['monthly_savings'] * 12:,.2f}</p>
            <p style='color: #ffffff; margin-bottom: 1rem; line-height: 1.6;'><strong style='color: #00d4ff;'>Payback Estimado:</strong> {solar_simulation['payback_years']} anos</p>
            <p style='color: #ffffff; margin-bottom: 0; line-height: 1.6;'><strong style='color: #00d4ff;'>ROI (25 anos):</strong> {solar_simulation['roi_25_years']}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🌍 Ambiental")
        st.markdown(f"""
        <div style='background-color: #2d2d2d; padding: 2rem; border-radius: 12px; border: 1px solid #333333;'>
            <p style='color: #ffffff; margin-bottom: 1rem; line-height: 1.6;'><strong style='color: #00ff88;'>Redução de CO₂:</strong> {solar_simulation['co2_reduction']} ton/ano</p>
            <p style='color: #ffffff; margin-bottom: 1rem; line-height: 1.6;'><strong style='color: #00ff88;'>Equivalente a árvores:</strong> {solar_simulation['co2_reduction'] * 7:.0f} árvores</p>
            <p style='color: #ffffff; margin-bottom: 1rem; line-height: 1.6;'><strong style='color: #00ff88;'>Vida Útil do Sistema:</strong> {solar_simulation['lifespan_years']} anos</p>
            <p style='color: #ffffff; margin-bottom: 0; line-height: 1.6;'><strong style='color: #00ff88;'>Energia Limpa Anual:</strong> {solar_simulation['monthly_generation'] * 12:,.0f} kWh</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close tab-container

def display_recommendations(recommendations):
    """Exibe as recomendações na quarta aba"""
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">💡 Recomendações de Otimização</h3>', unsafe_allow_html=True)
    
    if not recommendations:
        st.markdown("""
        <div class="info-box">
            <h4 style='color: #00d4ff; margin-top: 0;'>ℹ️ Nenhuma recomendação crítica</h4>
            <p style='color: #ffffff; margin-bottom: 0;'>Seu consumo energético está dentro dos parâmetros esperados. Continue monitorando para identificar novas oportunidades de otimização.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for rec in recommendations:
            if rec['priority'] == 'HIGH':
                css_class = "recommendation-high"
                priority_text = "🔴 Alta Prioridade"
            elif rec['priority'] == 'MEDIUM':
                css_class = "recommendation-medium"
                priority_text = "🟡 Média Prioridade"
            else:
                css_class = "recommendation-low"
                priority_text = "🟢 Baixa Prioridade"
            
            st.markdown(f"""
            <div class="{css_class}">
                <strong>{priority_text}: {rec['title']}</strong><br>
                <p style='margin: 0.5rem 0; line-height: 1.6;'>{rec['description']}</p>
                <em>💰 Economia estimada: {rec['estimated_savings']}</em>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close tab-container

def display_scenarios_comparison(scenarios, solar_simulation):
    """Exibe a comparação de cenários na quinta aba"""
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">📈 Cenários Comparativos de Instalação</h3>', unsafe_allow_html=True)
    
    # Tabela comparativa
    comparison_data = []
    for scenario, data in scenarios.items():
        comparison_data.append({
            'Cenário': scenario.upper(),
            'Área (m²)': data['available_area'],
            'Potência (kWp)': data['installed_power'],
            'Geração (kWh/mês)': data['monthly_generation'],
            'Autossuficiência (%)': data['self_sufficiency'],
            'Investimento (R$)': data['total_investment'],
            'Payback (anos)': data['payback_years']
        })
    
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True)
    
    # Espaço entre seções
    st.markdown('<div style="margin: 3rem 0;"></div>', unsafe_allow_html=True)
    
    # Gráfico comparativo com tema escuro
    fig_comparison = go.Figure()
    
    fig_comparison.add_trace(go.Bar(
        name='Investimento (R$ mil)',
        x=[c.upper() for c in scenarios.keys()],
        y=[dados['total_investment'] / 1000 for dados in scenarios.values()],
        marker_color='#00d4ff'
    ))
    
    fig_comparison.add_trace(go.Scatter(
        name='Autossuficiência (%)',
        x=[c.upper() for c in scenarios.keys()],
        y=[dados['self_sufficiency'] for dados in scenarios.values()],
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='#00ff88', width=3),
        marker=dict(size=8)
    ))
    
    fig_comparison.update_layout(
        title='Comparação entre Cenários - Investimento vs Autossuficiência',
        xaxis=dict(title='Cenários', gridcolor='#333333', showgrid=True),
        yaxis=dict(title='Investimento (R$ mil)', side='left', gridcolor='#333333', showgrid=True),
        yaxis2=dict(title='Autossuficiência (%)', side='right', overlaying='y', gridcolor='#333333', showgrid=True),
        legend=dict(x=0.1, y=1.1, orientation='h'),
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='#ffffff'),
        title_font=dict(size=20)
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Recomendação baseada nos cenários
    best_scenario = max(scenarios.items(), key=lambda x: x[1]['roi_25_years'])
    st.markdown(f"""
    <div class="info-box">
        <h4 style='color: #00d4ff; margin-top: 0; margin-bottom: 1rem;'>💡 Recomendação Baseada nos Cenários</h4>
        <p style='color: #ffffff; margin-bottom: 0; line-height: 1.6;'>
            O cenário <strong style='color: #00ff88;'>{best_scenario[0].upper()}</strong> apresenta o melhor ROI ({best_scenario[1]['roi_25_years']}%) 
            com autossuficiência de {best_scenario[1]['self_sufficiency']}% e payback de {best_scenario[1]['payback_years']} anos.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close tab-container

if __name__ == "__main__":
    main()