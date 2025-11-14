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
    
    # CSS customizado - Tema verde e branco
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.8rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.4rem;
        color: #228B22;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #FFFFFF;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 5px solid #2E8B57;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .recommendation-high {
        background-color: #FFE6E6;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #DC143C;
        margin: 0.5rem 0;
        border: 1px solid #FFCCCC;
    }
    .recommendation-medium {
        background-color: #FFF9E6;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #FFA500;
        margin: 0.5rem 0;
        border: 1px solid #FFE4B5;
    }
    .recommendation-low {
        background-color: #F0FFF0;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #32CD32;
        margin: 0.5rem 0;
        border: 1px solid #98FB98;
    }
    .section-header {
        color: #2E8B57;
        border-bottom: 2px solid #32CD32;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .sidebar .sidebar-content {
        background-color: #F8FFF8;
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
    if st.sidebar.button("Executar Análise Completa", type="primary"):
        execute_analysis(analyzer, solar_simulator, analysis_days, state, available_area)
    else:
        show_initial_screen()
    
    # Informações na sidebar
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Sobre esta solução:**
    
    - Análise de padrões de consumo energético
    - Detecção de desperdícios e otimizações
    - Simulação de viabilidade de energia solar
    - Cálculo de impacto ambiental e financeiro
    
    *Desenvolvido para o projeto SERS Global Solution*
    """)

def show_initial_screen():
    """Mostra tela inicial antes da análise"""
    st.info("""
    **Bem-vindo ao SERS Global Solution**
    
    Configure os parâmetros na barra lateral e clique em **Executar Análise Completa** para:
    
    - Analisar padrões de consumo energético
    - Identificar oportunidades de economia  
    - Simular viabilidade de energia solar
    - Calcular impacto ambiental
    
    *Solução desenvolvida para eficiência energética corporativa*
    """)

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
    
    # Exibição dos resultados
    display_results(consumption_data, consumption_insights, recommendations, 
                   solar_simulation, classification, scenarios)

def display_results(consumption_data, consumption_insights, recommendations, 
                   solar_simulation, classification, scenarios):
    """Exibe os resultados da análise no dashboard"""
    
    # SEÇÃO 1: MÉTRICAS PRINCIPAIS
    st.markdown('<h3 class="section-header">Métricas Principais de Consumo</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Consumo Total", f"{consumption_insights['total_consumption']:,.0f} kWh")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Horário de Pico", f"{consumption_insights['peak_hour']}h")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                "Desperdício Noturno", 
                f"{consumption_insights['night_waste']}%",
                delta=f"-{consumption_insights['night_waste']}% potencial",
                delta_color="inverse"
            )
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Maior Consumo", consumption_insights['highest_consumption_dept'])
            st.markdown('</div>', unsafe_allow_html=True)
    
    # SEÇÃO 2: GRÁFICOS DE ANÁLISE
    st.markdown('<h3 class="section-header">Análise Visual do Consumo</h3>', unsafe_allow_html=True)
    
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
        fig_hour.update_traces(line_color='#2E8B57')
        fig_hour.add_vrect(x0=8, x1=18, fillcolor="#32CD32", opacity=0.1, 
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
            color_discrete_sequence=['#2E8B57', '#3CB371', '#32CD32', '#90EE90']
        )
        st.plotly_chart(fig_dept, use_container_width=True)
    
    # SEÇÃO 3: RECOMENDAÇÕES
    st.markdown('<h3 class="section-header">Recomendações de Otimização</h3>', unsafe_allow_html=True)
    
    if not recommendations:
        st.warning("Nenhuma recomendação gerada para os dados atuais.")
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
                {rec['description']}<br>
                <em>Economia estimada: {rec['estimated_savings']}</em>
            </div>
            """, unsafe_allow_html=True)
    
    # SEÇÃO 4: SIMULAÇÃO DE ENERGIA SOLAR
    st.markdown('<h3 class="section-header">Simulação de Energia Solar</h3>', unsafe_allow_html=True)
    
    # Métricas solares
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Potência Instalável", f"{solar_simulation['installed_power']} kWp")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Geração Mensal", f"{solar_simulation['monthly_generation']:,.0f} kWh")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Autossuficiência", f"{solar_simulation['self_sufficiency']}%")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Classificação", classification['classification'])
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Detalhes financeiros e ambientais
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Análise Financeira")
        st.markdown(f"""
        - **Investimento Total**: R$ {solar_simulation['total_investment']:,.2f}
        - **Economia Mensal**: R$ {solar_simulation['monthly_savings']:,.2f}
        - **Payback**: {solar_simulation['payback_years']} anos
        - **ROI (25 anos)**: {solar_simulation['roi_25_years']}%
        """)
    
    with col2:
        st.subheader("Impacto Ambiental")
        st.markdown(f"""
        - **Redução de CO₂**: {solar_simulation['co2_reduction']} ton/ano
        - **Equivalente a árvores**: {solar_simulation['co2_reduction'] * 7:.0f} árvores plantadas
        - **Vida Útil do Sistema**: {solar_simulation['lifespan_years']} anos
        - **Energia Limpa Gerada**: {solar_simulation['monthly_generation'] * 12:,.0f} kWh/ano
        """)
    
    # SEÇÃO 5: CENÁRIOS COMPARATIVOS
    st.markdown('<h3 class="section-header">Cenários Comparativos de Instalação</h3>', unsafe_allow_html=True)
    
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
    
    # SEÇÃO 6: RESUMO EXECUTIVO
    st.markdown('<h3 class="section-header">Resumo Executivo</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Principais Oportunidades")
        st.success(f"**Redução de Custos**: Potencial de economia de até {consumption_insights['night_waste'] + 10:.1f}% com otimizações")
        st.info(f"**Energia Solar**: {solar_simulation['self_sufficiency']}% do consumo pode ser solar")
        st.warning(f"**Sustentabilidade**: Redução de {solar_simulation['co2_reduction']} toneladas de CO₂/ano")
    
    with col2:
        st.subheader("Próximos Passos Recomendados")
        st.markdown("""
        1. Implementar automação para reduzir desperdício noturno
        2. Realizar estudo detalhado de viabilidade solar
        3. Desenvolver campanha de conscientização para colaboradores
        4. Implementar sistema de monitoramento contínuo
        """)
    
    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #2E8B57;'>
        SERS Global Solution - Sistema de Eficiência Energética e Sustentabilidade<br>
        Desenvolvido para o projeto acadêmico - Ciências da Computação - 2025
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()