# Manual de Instalação e Utilização - SERS Global Solution

## Índice

1. [Pré-requisitos do Sistema](#pré-requisitos-do-sistema)
2. [Instalação e Configuração](#instalação-e-configuração)
3. [Execução da Aplicação](#execução-da-aplicação)
4. [Guia de Utilização](#guia-de-utilização)
5. [Estrutura Técnica](#estrutura-técnica)

---

## Pré-requisitos do Sistema

### Requisitos Mínimos de Hardware

- Processador: Dual-core 2.0 GHz ou superior
- Memória RAM: 4 GB (recomendado 8 GB)
- Espaço em disco: 500 MB livres
- Sistema operacional: Windows 10/11, Linux Ubuntu 18.04+, macOS 10.14+

### Requisitos de Software

- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)
- Navegador web moderno (Chrome 90+, Firefox 88+, Edge 90+)
- Conexão com internet para instalação de dependências

### Verificação de Pré-requisitos

**Windows:**

```cmd
python --version
pip --version
```

**Linux/macOS:**

```bash
python3 --version
pip3 --version
```

---

## Instalação e Configuração

### Método 1: Instalação Direta (Recomendado)

#### Passo 1: Obtenção dos Arquivos do Projeto

```bash
# Opção A - Via Git
git clone https://github.com/seu-usuario/sers-global-solution.git
cd sers-global-solution

# Opção B - Download manual
# Faça download dos arquivos e extraia para uma pasta local
```

#### Passo 2: Instalação de Dependências

Execute os comandos sequencialmente no terminal/prompt de comando:

```bash
pip install streamlit==1.28.0
pip install pandas==2.0.3
pip install plotly==5.15.0
pip install numpy==1.24.3
```

#### Passo 3: Verificação da Instalação

```bash
python -c "import streamlit, pandas, plotly, numpy; print('Instalação verificada com sucesso')"
```

### Método 2: Ambiente Virtual (Opcional)

#### Para usuários avançados que desejam isolamento de ambiente:

**Windows:**

```cmd
python -m venv venv
venv\Scripts\activate
pip install streamlit pandas plotly numpy
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install streamlit pandas plotly numpy
```

---

## Execução da Aplicação

### Inicialização do Sistema

1. Abra o terminal/prompt de comando
2. Navegue até o diretório do projeto:

```bash
cd caminho/para/sers-global-solution
```

3. Execute o comando de inicialização:

```bash
streamlit run app.py
```

### Comportamento Esperado

- O terminal exibirá mensagens de inicialização
- O navegador padrão abrirá automaticamente
- A aplicação estará acessível em: http://localhost:8501
- Para acesso remoto: http://seu-ip:8501

### Encerramento da Aplicação

- No terminal: Pressione `Ctrl + C`
- Feche a janela do terminal
- A aplicação será automaticamente encerrada

---

## Guia de Utilização

### Interface Principal

#### Barra Lateral de Configuração

A barra lateral contém os parâmetros de configuração para análise:

1. **Configurações de Dados de Consumo**

   - Período de Análise: Seletor de 1 a 30 dias
   - Define o intervalo temporal para geração de dados simulados
2. **Configurações de Simulação Solar**

   - Estado da Instalação: Lista de estados brasileiros
   - Área Disponível: Controle deslizante de 20 a 200 m²
3. **Controle de Execução**

   - Botão "Executar Análise Completa": Inicia o processamento

### Fluxo de Trabalho Recomendado

#### Fase 1: Configuração Inicial

1. Selecione o período de análise (7-14 dias para análise padrão)
2. Escolha o estado correspondente à localização
3. Defina a área disponível para instalação de painéis solares
4. Clique em "Executar Análise Completa"

#### Fase 2: Análise dos Resultados

**Aba 1 - Resumo Executivo**

- Métricas consolidadas de consumo energético
- Indicadores de viabilidade do projeto solar
- Principais oportunidades identificadas
- Próximos passos recomendados

**Aba 2 - Análise de Consumo**

- Gráficos temporais de consumo por hora
- Distribuição de consumo por departamento
- Identificação de horários de pico
- Análise de desperdícios energéticos

**Aba 3 - Energia Solar**

- Classificação de viabilidade técnica
- Detalhamento financeiro (investimento, payback, ROI)
- Impacto ambiental quantificado
- Especificações técnicas do sistema

**Aba 4 - Recomendações**

- Ações priorizadas por criticidade
- Estimativas de economia para cada recomendação
- Descrição detalhada das implementações sugeridas

**Aba 5 - Cenários**

- Comparativo entre diferentes tamanhos de instalação
- Análise de trade-offs entre investimento e retorno
- Recomendação do cenário mais vantajoso

### Interpretação de Métricas Principais

#### Indicadores de Consumo

- **Consumo Total**: Soma energética em kWh no período
- **Horário de Pico**: Hora com maior demanda média
- **Desperdício Noturno**: Percentual consumido entre 0h-6h
- **Consumo Fora do Expediente**: Percentual fora do horário 8h-18h

#### Indicadores Solares

- **Autossuficiência**: Percentual do consumo atendido pela geração solar
- **Payback**: Período de retorno do investimento em anos
- **ROI 25 anos**: Retorno sobre investimento considerando vida útil
- **Redução de CO₂**: Toneladas de carbono evitadas anualmente

---

## Estrutura Técnica

### Arquitetura do Sistema

```
sers-global-solution/
├── app.py                 # Aplicação principal Streamlit
├── data_analyzer.py       # Módulo de análise de consumo
├── solar_simulator.py     # Módulo de simulação solar
└── requirements.txt       # Dependências do projeto
```

### Módulos Principais

**app.py**

- Interface gráfica do usuário
- Coordenação entre módulos
- Apresentação de resultados

**data_analyzer.py**

- Geração de dados simulados de consumo
- Análise de padrões energéticos
- Geração de recomendações

**solar_simulator.py**

- Cálculos de viabilidade técnica
- Simulações financeiras
- Análise de impacto ambiental

### Dependências Técnicas

- **Streamlit**: Framework para aplicações web em Python
- **Pandas**: Manipulação e análise de dados
- **Plotly**: Visualizações gráficas interativas
- **NumPy**: Computação científica e numérica

### Considerações de Segurança

- A aplicação executa localmente por padrão
- Dados são processados em memória local
- Não são realizadas conexões externas com dados sensíveis
- Recomenda-se uso em ambiente controlado para dados reais

---

**Versão do Documento:** 1.0
**Última Atualização:** 14/11/25
**Compatível com:** SERS Global Solution v1.0
