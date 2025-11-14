"""
Dashboard Principal - SmartEnergy Analytics
Solução Express para Eficiência Energética e Energia Solar
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import sys
import os

# Adiciona o diretório atual ao path do Python para importar módulos locais
sys.path.append(os.path.dirname(__file__))

# Importa módulos customizados
try:
    from data_analyzer import FastEnergyAnalyzer
    from solar_simulator import SimpleSolarSimulator
except ImportError as e:
    st.error(f"Erro ao importar módulos: {e}")
    st.stop()

def setup_page():
    """Configuração inicial da página Streamlit"""
    st.set_page_config(
        page_title="SmartEnergy Analytics",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS customizado para melhorar aparência
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .recommendation-high {
        background-color: #ffcccc;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ff0000;
        margin: 0.5rem 0;
    }
    .recommendation-medium {
        background-color: #fff4cc;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffcc00;
        margin: 0.5rem 0;
    }
    .recommendation-low {
        background-color: #ccffcc;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #00cc00;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Função principal do dashboard"""
    setup_page()
    
    # Cabeçalho principal
    st.markdown('<h1 class="main-header">⚡ SmartEnergy Analytics</h1>', unsafe_allow_html=True)
    st.markdown("### Solução Express para Eficiência Energética e Sustentabilidade Corporativa")
    
    # Inicialização dos módulos
    try:
        analyzer = FastEnergyAnalyzer()
        solar_simulator = SimpleSolarSimulator()
    except Exception as e:
        st.error(f"Erro ao inicializar módulos: {e}")
        return
    
    # Sidebar - Configurações
    st.sidebar.header("🎯 Configurações da Análise")
    
    st.sidebar.subheader("📊 Dados de Consumo")
    dias_analise = st.sidebar.slider("Período de Análise (dias)", 1, 30, 7, 
                                   help="Número de dias para simular dados de consumo")
    
    st.sidebar.subheader("☀️ Simulação Solar")
    estado = st.sidebar.selectbox("Estado da Instalação", 
                                options=list(solar_simulator.irradiacao.keys()),
                                index=0,
                                help="Selecione o estado para cálculo de irradiação solar")
    
    area_disponivel = st.sidebar.slider("Área Disponível para Painéis (m²)", 
                                      20, 200, 50,
                                      help="Área total disponível para instalação de painéis solares")
    
    # Botão de execução principal
    if st.sidebar.button("🚀 Executar Análise Completa", type="primary"):
        execute_analysis(analyzer, solar_simulator, dias_analise, estado, area_disponivel)
    else:
        # Mostra tela inicial quando não há análise
        show_initial_screen()
    
    # Seção de informações na sidebar
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **💡 Sobre esta solução:**
    
    - Análise de padrões de consumo
    - Detecção de desperdícios energéticos
    - Simulação de energia solar
    - Cálculo de viabilidade financeira
    
    *Desenvolvido para o projeto Global Solution*
    """)

def show_initial_screen():
    """Mostra tela inicial antes da análise"""
    st.info("""
    **👋 Bem-vindo ao SmartEnergy Analytics!**
    
    Configure os parâmetros na sidebar e clique em **🚀 Executar Análise Completa** para:
    
    - 📊 Analisar padrões de consumo energético
    - 💡 Identificar oportunidades de economia  
    - ☀️ Simular viabilidade de energia solar
    - 🌍 Calcular impacto ambiental
    
    *Solução desenvolvida para eficiência energética corporativa*
    """)

def execute_analysis(analyzer, solar_simulator, dias_analise, estado, area_disponivel):
    """
    Executa a análise completa e exibe resultados
    
    Args:
        analyzer: Instância do analisador de dados
        solar_simulator: Instância do simulador solar
        dias_analise: Dias para análise
        estado: Estado selecionado
        area_disponivel: Área disponível para painéis
    """
    with st.spinner("🔄 Processando dados e gerando insights..."):
        # Simula tempo de processamento
        time.sleep(2)
        
        try:
            # 1. Geração e análise de dados de consumo
            dados_consumo = analyzer.generate_basic_data(dias_analise)
            insights_consumo = analyzer.analyze_consumption(dados_consumo)
            recomendacoes = analyzer.get_recommendations(insights_consumo)
            
            # 2. Simulação de energia solar
            simulacao_solar = solar_simulator.calcular_viabilidade(
                insights_consumo['consumo_total'], estado, area_disponivel
            )
            
            classificacao = solar_simulator.classificar_viabilidade(simulacao_solar)
            
            # 3. Geração de cenários comparativos
            cenarios = solar_simulator.gerar_cenarios_comparativos(
                insights_consumo['consumo_total'], estado
            )
            
        except Exception as e:
            st.error(f"Erro durante a análise: {e}")
            return
    
    # Exibição dos resultados
    display_results(dados_consumo, insights_consumo, recomendacoes, 
                   simulacao_solar, classificacao, cenarios)

def display_results(dados_consumo, insights_consumo, recomendacoes, 
                   simulacao_solar, classificacao, cenarios):
    """
    Exibe os resultados da análise no dashboard
    
    Args:
        dados_consumo: DataFrame com dados de consumo
        insights_consumo: Insights da análise de consumo
        recomendacoes: Lista de recomendações
        simulacao_solar: Resultados da simulação solar
        classificacao: Classificação da viabilidade
        cenarios: Cenários comparativos
    """
    
    # SEÇÃO 1: MÉTRICAS PRINCIPAIS
    st.header("📈 Métricas Principais de Consumo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Consumo Total Analisado",
            value=f"{insights_consumo['consumo_total']:,.0f} kWh"
        )
    
    with col2:
        st.metric(
            label="Horário de Pico",
            value=f"{insights_consumo['pico_horario']}h"
        )
    
    with col3:
        st.metric(
            label="Desperdício Noturno",
            value=f"{insights_consumo['desperdicio_noturno']}%",
            delta=f"-{insights_consumo['desperdicio_noturno']}% potencial",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="Departamento Maior Consumo",
            value=insights_consumo['departamento_maior_consumo']
        )
    
    # SEÇÃO 2: GRÁFICOS DE ANÁLISE
    st.header("📊 Análise Visual do Consumo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de consumo por hora
        consumo_horario = dados_consumo.groupby('hora')['consumo_kwh'].mean().reset_index()
        fig_hora = px.line(
            consumo_horario, 
            x='hora', 
            y='consumo_kwh',
            title="📅 Consumo Médio por Hora do Dia",
            labels={'hora': 'Hora do Dia', 'consumo_kwh': 'Consumo (kWh)'}
        )
        fig_hora.add_vrect(x0=8, x1=18, fillcolor="green", opacity=0.1, 
                          annotation_text="Horário Comercial", annotation_position="top left")
        st.plotly_chart(fig_hora, use_container_width=True)
    
    with col2:
        # Gráfico de consumo por departamento
        consumo_dept = dados_consumo.groupby('departamento')['consumo_kwh'].sum().reset_index()
        fig_dept = px.pie(
            consumo_dept,
            values='consumo_kwh',
            names='departamento',
            title="🏢 Distribuição do Consumo por Departamento"
        )
        st.plotly_chart(fig_dept, use_container_width=True)
    
    # SEÇÃO 3: RECOMENDAÇÕES
    st.header("💡 Recomendações de Otimização")
    
    if not recomendacoes:
        st.warning("Nenhuma recomendação gerada para os dados atuais.")
    else:
        for rec in recomendacoes:
            if rec['tipo'] == 'ALTA_PRIORIDADE':
                css_class = "recommendation-high"
                emoji = "🔴"
            elif rec['tipo'] == 'MEDIA_PRIORIDADE':
                css_class = "recommendation-medium" 
                emoji = "🟡"
            else:
                css_class = "recommendation-low"
                emoji = "🔵"
            
            st.markdown(f"""
            <div class="{css_class}">
                <strong>{emoji} {rec['titulo']}</strong><br>
                {rec['descricao']}<br>
                <em>Economia estimada: {rec['economia_estimada']}</em>
            </div>
            """, unsafe_allow_html=True)
    
    # SEÇÃO 4: SIMULAÇÃO DE ENERGIA SOLAR
    st.header("☀️ Simulação de Energia Solar")
    
    # Classificação com cor
    if classificacao['cor'] == 'green':
        class_emoji = "✅"
    elif classificacao['cor'] == 'blue':
        class_emoji = "ℹ️"
    elif classificacao['cor'] == 'orange':
        class_emoji = "⚠️"
    else:
        class_emoji = "❌"
    
    # Métricas solares
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Potência Instalável",
            value=f"{simulacao_solar['potencia_instalada_kwp']} kWp"
        )
    
    with col2:
        st.metric(
            label="Geração Mensal",
            value=f"{simulacao_solar['geracao_mensal_kwh']:,.0f} kWh"
        )
    
    with col3:
        st.metric(
            label="Autossuficiência",
            value=f"{simulacao_solar['autossuficiencia_percentual']}%"
        )
    
    with col4:
        st.metric(
            label="Classificação",
            value=f"{class_emoji} {classificacao['classificacao']}"
        )
    
    # Detalhes financeiros e ambientais
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Análise Financeira")
        st.markdown(f"""
        - **Investimento Total**: R$ {simulacao_solar['investimento_total']:,.2f}
        - **Economia Mensal**: R$ {simulacao_solar['economia_mensal']:,.2f}
        - **Payback**: {simulacao_solar['payback_anos']} anos
        - **ROI (25 anos)**: {simulacao_solar['roi_25_anos_percentual']}%
        """)
    
    with col2:
        st.subheader("🌍 Impacto Ambiental")
        st.markdown(f"""
        - **Redução de CO₂**: {simulacao_solar['reducao_co2_ton_ano']} ton/ano
        - **Equivalente a árvores**: {simulacao_solar['reducao_co2_ton_ano'] * 7:.0f} árvores plantadas
        - **Vida Útil do Sistema**: {simulacao_solar['vida_util_anos']} anos
        - **Energia Limpa Gerada**: {simulacao_solar['geracao_mensal_kwh'] * 12:,.0f} kWh/ano
        """)
    
    # SEÇÃO 5: CENÁRIOS COMPARATIVOS
    st.header("📋 Cenários Comparativos de Instalação")
    
    # Tabela comparativa
    comparacao_data = []
    for cenario, dados in cenarios.items():
        comparacao_data.append({
            'Cenário': cenario.upper(),
            'Área (m²)': dados['area_disponivel_m2'],
            'Potência (kWp)': dados['potencia_instalada_kwp'],
            'Geração (kWh/mês)': dados['geracao_mensal_kwh'],
            'Autossuficiência (%)': dados['autossuficiencia_percentual'],
            'Investimento (R$)': dados['investimento_total'],
            'Payback (anos)': dados['payback_anos']
        })
    
    df_comparacao = pd.DataFrame(comparacao_data)
    st.dataframe(df_comparacao, use_container_width=True)
    
    # SEÇÃO 6: RESUMO EXECUTIVO
    st.header("🎯 Resumo Executivo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Principais Oportunidades")
        st.success(f"**Redução de Custos**: Potencial de economia de até {insights_consumo['desperdicio_noturno'] + 10:.1f}% com otimizações")
        st.info(f"**Energia Solar**: {simulacao_solar['autossuficiencia_percentual']}% do consumo pode ser solar")
        st.warning(f"**Sustentabilidade**: Redução de {simulacao_solar['reducao_co2_ton_ano']} toneladas de CO₂/ano")
    
    with col2:
        st.subheader("🚀 Próximos Passos Recomendados")
        st.markdown("""
        1. **Implementar automação** para reduzir desperdício noturno
        2. **Estudo detalhado** de viabilidade solar
        3. **Campanha de conscientização** para colaboradores
        4. **Monitoramento contínuo** com IoT
        """)
    
    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        ⚡ SmartEnergy Analytics - Solução desenvolvida para o projeto Global Solution<br>
        Ciências da Computação - 2° semestre de 2025
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()