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
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS customizado - Tema Claro Profissional
    st.markdown("""
    <style>
        /* Configuração geral do tema claro */
        .main {
            background-color: #ffffff;
            color: #333333;
        }
        
        .stApp {
            background-color: #ffffff;
        }
        
        /* Tipografia e espaçamento */
        .main-header {
            font-size: 2.5rem;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 600;
            padding-top: 1rem;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 1rem;
        }
        
        .sub-header {
            font-size: 1.4rem;
            color: #7f8c8d;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 400;
        }
        
        .section-header {
            color: #2c3e50;
            border-bottom: 2px solid #bdc3c7;
            padding-bottom: 0.8rem;
            margin-top: 2rem;
            margin-bottom: 1.5rem;
            font-weight: 600;
            font-size: 1.6rem;
        }
        
        /* Cartões de métricas profissionais */
        .metric-card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #dee2e6;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            text-align: center;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #6c757d;
            margin-bottom: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
        }
        
        .metric-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 0.3rem;
            line-height: 1.2;
        }
        
        .metric-unit {
            font-size: 0.8rem;
            color: #6c757d;
            font-weight: 400;
        }
        
        /* Caixas informativas */
        .info-box, .success-box, .warning-box {
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            border-left: 4px solid;
        }
        
        .info-box {
            background: #e3f2fd;
            border-left-color: #2196f3;
        }
        
        .success-box {
            background: #e8f5e8;
            border-left-color: #4caf50;
        }
        
        .warning-box {
            background: #fff3e0;
            border-left-color: #ff9800;
        }
        
        .recommendation-high {
            background: #ffebee;
            padding: 1.2rem;
            border-radius: 6px;
            border-left: 4px solid #f44336;
            margin: 0.8rem 0;
        }
        
        .recommendation-medium {
            background: #fff8e1;
            padding: 1.2rem;
            border-radius: 6px;
            border-left: 4px solid #ffc107;
            margin: 0.8rem 0;
        }
        
        .recommendation-low {
            background: #e8f5e8;
            padding: 1.2rem;
            border-radius: 6px;
            border-left: 4px solid #4caf50;
            margin: 0.8rem 0;
        }
        
        /* Abas */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            padding: 0.8rem 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 0.8rem 1.2rem;
            font-size: 1rem;
            background-color: #f8f9fa;
            border-radius: 4px;
            font-weight: 500;
            color: #495057;
            border: 1px solid #dee2e6;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #ffffff;
            color: #2c3e50;
            border: 1px solid #2c3e50;
        }
        
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
            color: #333333;
        }
        
        /* Botões */
        .stButton button {
            background: #2c3e50 !important;
            color: #ffffff !important;
            border: none !important;
            padding: 0.8rem 1.5rem !important;
            border-radius: 4px !important;
            font-weight: 500 !important;
            width: 100% !important;
            font-size: 1rem !important;
            margin: 0.8rem 0 !important;
        }

        .stButton button div p {
            color: #ffffff !important;
        }

        .stButton button span {
            color: #ffffff !important;
        }

        .stButton button:hover {
            background: #34495e !important;
            color: #ffffff !important;
        }

        .stButton button:hover span {
            color: #ffffff !important;
        }

        .stButton button:hover div p {
            color: #ffffff !important;
        }
        
        /* Espaçamento de colunas */
        [data-testid="column"] {
            padding: 0 0.8rem;
        }
        
        /* Listas */
        ol, ul {
            line-height: 1.6;
        }
        
        li {
            margin-bottom: 0.8rem;
            padding-left: 0.5rem;
        }
        
        /* Elementos do Streamlit */
        .stSlider > div > div > div {
            color: #333333;
        }
        
        .stSelectbox > div > div {
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #ced4da;
        }
        
        .stNumberInput > div > div > input {
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #ced4da;
        }
        
        /* Garantir que todos os textos sejam visíveis */
        .stDataFrame {
            background-color: white;
        }
        
        p, li, span, div {
            color: #333333 !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #333333 !important;
        }
                
    .roi-box {
        background: #ffebee;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #c62828;
    }
    
    </style>
    """, unsafe_allow_html=True)

def main():
    """Função principal do dashboard"""
    setup_page()
    
    # Cabeçalho principal
    st.markdown('<h1 class="main-header">SERS Global Solution</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Sistema de Eficiência Energética e Sustentabilidade</h2>', unsafe_allow_html=True)
    
    # Inicialização dos módulos
    try:
        analyzer = EnergyAnalyzer()
        solar_simulator = SolarSimulator()
    except Exception as e:
        st.error(f"Erro ao inicializar módulos: {e}")
        return
    
    # Sidebar - Configurações
    st.sidebar.header("Configurações da Análise")
    
    st.sidebar.subheader("Dados de Consumo")
    analysis_days = st.sidebar.slider("Período de Análise (dias)", 1, 30, 7)
    
    st.sidebar.subheader("Simulação Solar")
    state = st.sidebar.selectbox(
        "Estado da Instalação", 
        options=list(solar_simulator.irradiation.keys()),
        index=0
    )
    
    available_area = st.sidebar.slider("Área Disponível para Painéis (m²)", 20, 200, 50)
    
    # Botão de execução principal
    if st.sidebar.button("Executar Análise Completa"):
        execute_analysis(analyzer, solar_simulator, analysis_days, state, available_area)
    else:
        show_initial_screen()
    
    # Informações na sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='background-color: #e3f2fd; padding: 1.2rem; border-radius: 6px; border-left: 4px solid #2196f3;'>
        <h4 style='color: #1976d2; margin-top: 0; margin-bottom: 1rem;'>Sobre esta solução:</h4>
        <ul style='color: #333333; line-height: 1.5;'>
            <li style='margin-bottom: 0.5rem;'>Análise de padrões de consumo energético</li>
            <li style='margin-bottom: 0.5rem;'>Detecção de desperdícios e otimizações</li>
            <li style='margin-bottom: 0.5rem;'>Simulação de viabilidade de energia solar</li>
            <li style='margin-bottom: 0.5rem;'>Cálculo de impacto ambiental e financeiro</li>
        </ul>
        <p style='color: #666666; font-size: 0.9rem; margin-bottom: 0; margin-top: 1rem;'>Desenvolvido para o projeto SERS Global Solution</p>
    </div>
    """, unsafe_allow_html=True)

def show_initial_screen():
    """Mostra tela inicial antes da análise"""
    st.markdown("""
    <div class="info-box">
        <h3 style='color: #1976d2; margin-top: 0; margin-bottom: 1.2rem;'>Bem-vindo ao SERS Global Solution</h3>
        <p style='color: #333333; margin-bottom: 1rem; line-height: 1.5;'>Configure os parâmetros na barra lateral e clique em <strong>Executar Análise Completa</strong> para:</p>
        <ul style='color: #333333; line-height: 1.5;'>
            <li style='margin-bottom: 0.5rem;'>Analisar padrões de consumo energético</li>
            <li style='margin-bottom: 0.5rem;'>Identificar oportunidades de economia</li>
            <li style='margin-bottom: 0.5rem;'>Simular viabilidade de energia solar</li>
            <li style='margin-bottom: 0.5rem;'>Calcular impacto ambiental</li>
        </ul>
        <p style='color: #666666; margin-bottom: 0; margin-top: 1rem;'>Solução desenvolvida para eficiência energética corporativa</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-box">
            <h4 style='color: #2e7d32; margin-top: 0; margin-bottom: 1rem;'>Benefícios Esperados</h4>
            <ul style='color: #333333; line-height: 1.5;'>
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
            <h4 style='color: #ef6c00; margin-top: 0; margin-bottom: 1rem;'>Como Funciona</h4>
            <ol style='color: #333333; line-height: 1.5;'>
                <li style='margin-bottom: 0.5rem;'>Coleta dados de consumo</li>
                <li style='margin-bottom: 0.5rem;'>Analisa padrões e desperdícios</li>
                <li style='margin-bottom: 0.5rem;'>Simula soluções energéticas</li>
                <li style='margin-bottom: 0;'>Apresenta recomendações</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

def execute_analysis(analyzer, solar_simulator, analysis_days, state, available_area):
    """Executa a análise completa e exibe resultados"""
    with st.spinner("Processando dados e gerando insights..."):
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
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Resumo Executivo", 
        "Análise de Consumo", 
        "Energia Solar", 
        "Recomendações", 
        "Cenários"
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
    st.markdown('<h3 class="section-header p-color">Resumo Executivo</h3>', unsafe_allow_html=True)
    
    # Métricas principais
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
            <div class="metric-value">{solar_simulation['self_sufficiency']}%</div>
            <div class="metric-unit">do consumo</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Viabilidade</div>
            <div class="metric-value" style="font-size: 1.4rem;">{classification['classification']}</div>
            <div class="metric-unit">Projeto solar</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Economia Anual</div>
            <div class="metric-value">R$ {solar_simulation['monthly_savings'] * 12:,.0f}</div>
            <div class="metric-unit">com energia solar</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Análise de oportunidades
    st.markdown("### Principais Oportunidades")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="success-box">
            <h4 style='color: #2e7d32; margin-top: 0; margin-bottom: 1rem;'>Redução de Custos</h4>
            <p style='color: #333333; margin-bottom: 0; line-height: 1.5;'>
                Potencial de economia de até {consumption_insights['night_waste'] + 10:.1f}% 
                com otimizações identificadas
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-box">
            <h4 style='color: #1976d2; margin-top: 0; margin-bottom: 1rem;'>Energia Solar</h4>
            <p style='color: #333333; margin-bottom: 0; line-height: 1.5;'>
                {solar_simulation['self_sufficiency']}% do consumo 
                pode ser atendido por energia solar
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="warning-box">
            <h4 style='color: #ef6c00; margin-top: 0; margin-bottom: 1rem;'>Sustentabilidade</h4>
            <p style='color: #333333; margin-bottom: 0; line-height: 1.5;'>
                Redução de {solar_simulation['co2_reduction']} 
                toneladas de CO₂ por ano
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="roi-box">
            <h4 style='color: #c62828; margin-top: 0; margin-bottom: 1rem;'>ROI do Projeto</h4>
            <p style='color: #333333; margin-bottom: 0; line-height: 1.5;'>
                Retorno sobre investimento de {solar_simulation['roi_25_years']}% 
                em 25 anos com energia solar
            </p>
        </div>
        """, unsafe_allow_html=True)

def display_consumption_analysis(consumption_data, consumption_insights):
    """Exibe a análise de consumo na segunda aba"""
    st.markdown('<h3 class="section-header p-color">Análise de Consumo Energético</h3>', unsafe_allow_html=True)
    
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
            <div class="metric-value">{consumption_insights['night_waste']}%</div>
            <div class="metric-unit">0h-6h otimizável</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Consumo Fora do Expediente</div>
            <div class="metric-value">{consumption_insights['off_hours_consumption']}%</div>
            <div class="metric-unit">fora de 8h-18h</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Maior Consumo</div>
            <div class="metric-value" style="font-size: 1.4rem;">{consumption_insights['highest_consumption_dept']}</div>
            <div class="metric-unit">Departamento</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráficos de análise
    st.markdown("### Visualização de Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de consumo por hora
        hourly_consumption = consumption_data.groupby('hour')['consumption_kwh'].mean().reset_index()
        fig_hour = px.line(
            hourly_consumption, 
            x='hour', 
            y='consumption_kwh',
            title="Consumo Médio por Hora do Dia",
            labels={'hour': 'Hora do Dia', 'consumption_kwh': 'Consumo (kWh)'}
        )
        fig_hour.update_traces(line_color='#2c3e50', line_width=2)
        fig_hour.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#333333'),
            xaxis=dict(gridcolor='#e0e0e0', showgrid=True),
            yaxis=dict(gridcolor='#e0e0e0', showgrid=True)
        )
        fig_hour.add_vrect(x0=8, x1=18, fillcolor="#2c3e50", opacity=0.1, 
                          annotation_text="Horário Comercial", annotation_position="top left")
        st.plotly_chart(fig_hour, use_container_width=True)
    
    with col2:
        # Gráfico de consumo por departamento
        dept_consumption = consumption_data.groupby('department')['consumption_kwh'].sum().reset_index()
        fig_dept = px.pie(
            dept_consumption,
            values='consumption_kwh',
            names='department',
            title="Distribuição do Consumo por Departamento",
            color_discrete_sequence=['#2c3e50', '#34495e', '#7f8c8d', '#bdc3c7']
        )
        fig_dept.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#333333')
        )
        st.plotly_chart(fig_dept, use_container_width=True)

def display_solar_analysis(solar_simulation, classification):
    """Exibe a análise de energia solar na terceira aba"""
    st.markdown('<h3 class="section-header p-color">Análise de Energia Solar</h3>', unsafe_allow_html=True)
    
    # Status de viabilidade
    st.markdown(f"""
    <div style='background-color: {'#e8f5e8' if classification['color'] == 'green' else '#fff3e0' if classification['color'] == 'orange' else '#ffebee' if classification['color'] == 'red' else '#e3f2fd'}; 
                padding: 1.5rem; border-radius: 6px; border-left: 4px solid {'#4caf50' if classification['color'] == 'green' else '#ff9800' if classification['color'] == 'orange' else '#f44336' if classification['color'] == 'red' else '#2196f3'}; 
                margin-bottom: 1.5rem;'>
        <h4 style='color: {'#2e7d32' if classification['color'] == 'green' else '#ef6c00' if classification['color'] == 'orange' else '#c62828' if classification['color'] == 'red' else '#1976d2'}; margin-top: 0; margin-bottom: 1rem;'>
            {classification['classification']}
        </h4>
        <p style='color: #333333; margin-bottom: 0; line-height: 1.5;'>{classification['recommendation']}</p>
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
            <div class="metric-value">{solar_simulation['monthly_generation']:,.0f}</div>
            <div class="metric-unit">kWh</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Investimento Total</div>
            <div class="metric-value">R$ {solar_simulation['total_investment']:,.0f}</div>
            <div class="metric-unit">Sistema solar</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Payback</div>
            <div class="metric-value">{solar_simulation['payback_years']}</div>
            <div class="metric-unit">anos</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Detalhes financeiros e ambientais
    st.markdown("### Análise Financeira e Ambiental")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Financeiro")
        st.markdown(f"""
        <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 6px; border: 1px solid #dee2e6;'>
            <p style='color: #333333; margin-bottom: 0.8rem; line-height: 1.5;'><strong>Investimento Total:</strong> R$ {solar_simulation['total_investment']:,.2f}</p>
            <p style='color: #333333; margin-bottom: 0.8rem; line-height: 1.5;'><strong>Economia Mensal:</strong> R$ {solar_simulation['monthly_savings']:,.2f}</p>
            <p style='color: #333333; margin-bottom: 0.8rem; line-height: 1.5;'><strong>Economia Anual:</strong> R$ {solar_simulation['monthly_savings'] * 12:,.2f}</p>
            <p style='color: #333333; margin-bottom: 0.8rem; line-height: 1.5;'><strong>Payback Estimado:</strong> {solar_simulation['payback_years']} anos</p>
            <p style='color: #333333; margin-bottom: 0; line-height: 1.5;'><strong>ROI (25 anos):</strong> {solar_simulation['roi_25_years']}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Ambiental")
        st.markdown(f"""
        <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 6px; border: 1px solid #dee2e6;'>
            <p style='color: #333333; margin-bottom: 0.8rem; line-height: 1.5;'><strong>Redução de CO₂:</strong> {solar_simulation['co2_reduction']} ton/ano</p>
            <p style='color: #333333; margin-bottom: 0.8rem; line-height: 1.5;'><strong>Equivalente a árvores:</strong> {solar_simulation['co2_reduction'] * 7:.0f} árvores</p>
            <p style='color: #333333; margin-bottom: 0.8rem; line-height: 1.5;'><strong>Vida Útil do Sistema:</strong> {solar_simulation['lifespan_years']} anos</p>
            <p style='color: #333333; margin-bottom: 0; line-height: 1.5;'><strong>Energia Limpa Anual:</strong> {solar_simulation['monthly_generation'] * 12:,.0f} kWh</p>
        </div>
        """, unsafe_allow_html=True)

def display_recommendations(recommendations):
    """Exibe as recomendações na quarta aba"""
    st.markdown('<h3 class="section-header p-color">Recomendações de Otimização</h3>', unsafe_allow_html=True)
    
    if not recommendations:
        st.markdown("""
        <div class="info-box">
            <h4 style='color: #1976d2; margin-top: 0;'>Nenhuma recomendação crítica</h4>
            <p style='color: #333333; margin-bottom: 0;'>Seu consumo energético está dentro dos parâmetros esperados. Continue monitorando para identificar novas oportunidades de otimização.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for rec in recommendations:
            if rec['priority'] == 'HIGH':
                css_class = "recommendation-high"
                priority_text = "Alta Prioridade"
            elif rec['priority'] == 'MEDIUM':
                css_class = "recommendation-medium"
                priority_text = "Média Prioridade"
            else:
                css_class = "recommendation-low"
                priority_text = "Baixa Prioridade"
            
            st.markdown(f"""
            <div class="{css_class}">
                <strong>{priority_text}: {rec['title']}</strong><br>
                <p style='margin: 0.5rem 0; line-height: 1.5;'>{rec['description']}</p>
                <em>Economia estimada: {rec['estimated_savings']}</em>
            </div>
            """, unsafe_allow_html=True)

def display_scenarios_comparison(scenarios, solar_simulation):
    """Exibe a comparação de cenários na quinta aba"""
    st.markdown('<h3 class="section-header p-color">Cenários Comparativos de Instalação</h3>', unsafe_allow_html=True)
    
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
    
    # Gráfico comparativo
    fig_comparison = go.Figure()
    
    fig_comparison.add_trace(go.Bar(
        name='Investimento (R$ mil)',
        x=[c.upper() for c in scenarios.keys()],
        y=[dados['total_investment'] / 1000 for dados in scenarios.values()],
        marker_color='#2c3e50'
    ))
    
    fig_comparison.add_trace(go.Scatter(
        name='Autossuficiência (%)',
        x=[c.upper() for c in scenarios.keys()],
        y=[dados['self_sufficiency'] for dados in scenarios.values()],
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='red', width=3),  # Mudei para vermelho
        marker=dict(size=8, color='red')  # Mudei para vermelho
    ))
    
    fig_comparison.update_layout(
        title='Comparação entre Cenários - Investimento vs Autossuficiência',
        xaxis=dict(title='Cenários', gridcolor='#e0e0e0', showgrid=True),
        yaxis=dict(title='Investimento (R$ mil)', side='left', gridcolor='#e0e0e0', showgrid=True),
        yaxis2=dict(title='Autossuficiência (%)', side='right', overlaying='y', gridcolor='#e0e0e0', showgrid=True),
        legend=dict(x=0.1, y=1.1, orientation='h'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#333333')
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Recomendação baseada nos cenários
    best_scenario = max(scenarios.items(), key=lambda x: x[1]['roi_25_years'])
    st.markdown(f"""
    <div class="info-box">
        <h4 style='color: #1976d2; margin-top: 0; margin-bottom: 1rem;'>Recomendação Baseada nos Cenários</h4>
        <p style='color: #333333; margin-bottom: 0; line-height: 1.5;'>
            O cenário <strong>{best_scenario[0].upper()}</strong> apresenta o melhor ROI ({best_scenario[1]['roi_25_years']}%) 
            com autossuficiência de {best_scenario[1]['self_sufficiency']}% e payback de {best_scenario[1]['payback_years']} anos.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()