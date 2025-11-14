"""
Módulo de Simulação de Energia Solar
SmartEnergy Analytics - Solução Express
"""
import pandas as pd

class SimpleSolarSimulator:
    """
    Classe para simulação rápida de viabilidade de energia solar
    Calcula geração, custos, payback e impacto ambiental
    """
    
    def __init__(self):
        """Inicializa o simulador com dados de irradiação solar por estado"""
        # Dados de irradiação solar média no Brasil (kWh/m²/dia)
        # Fonte: Atlas Brasileiro de Energia Solar - INPE
        self.irradiacao = {
            'SP': 4.5,   # São Paulo
            'RJ': 4.8,   # Rio de Janeiro
            'MG': 5.2,   # Minas Gerais
            'RS': 4.2,   # Rio Grande do Sul
            'PR': 4.6,   # Paraná
            'SC': 4.3,   # Santa Catarina
            'BA': 5.5,   # Bahia
            'CE': 5.8,   # Ceará
            'PE': 5.6,   # Pernambuco
            'GO': 5.3,   # Goiás
            'DF': 5.4,   # Distrito Federal
            'ES': 4.9    # Espírito Santo
        }
        
        # Custo médio por kWp instalado (R$)
        self.custo_por_kwp = 4500
        
        # Tarifa média de energia elétrica (R$/kWh)
        self.tarifa_energia = 0.80
        
        # Fator de emissão de CO₂ (kg CO₂/kWh) - fonte: EPE
        self.fator_emissao_co2 = 0.5  # kg CO₂ por kWh
        
    def calcular_viabilidade(self, consumo_mensal, estado, area_disponivel=50, custo_kwp=None):
        """
        Calcula viabilidade de instalação de sistema solar fotovoltaico
        
        Args:
            consumo_mensal (float): Consumo mensal em kWh
            estado (str): Sigla do estado brasileiro
            area_disponivel (float): Área disponível para painéis em m²
            custo_kwp (float): Custo por kWp (opcional)
            
        Returns:
            dict: Dicionário com resultados da simulação
        """
        # Validações iniciais
        if consumo_mensal <= 0:
            raise ValueError("Consumo mensal deve ser maior que zero")
        
        if estado not in self.irradiacao:
            raise ValueError(f"Estado {estado} não encontrado. Estados disponíveis: {list(self.irradiacao.keys())}")
        
        # Usa custo padrão se não fornecido
        if custo_kwp is None:
            custo_kwp = self.custo_por_kwp
        
        # Obtém irradiação solar do estado
        irradiacao_estado = self.irradiacao[estado]
        
        # 1. Cálculo da potência instalável
        # Eficiência típica de painéis: 150-200 W/m² (usamos 150 W/m² = 0.15 kW/m²)
        eficiencia_painel = 0.15  # kW/m²
        potencia_instalada_kwp = area_disponivel * eficiencia_painel
        
        # 2. Cálculo da geração mensal de energia
        # Fórmula: Potência (kWp) × Irradiação (kWh/m²/dia) × Dias × Performance Ratio
        performance_ratio = 0.75  # Considera perdas no sistema (cabo, inversor, etc.)
        geracao_mensal_kwh = (potencia_instalada_kwp * irradiacao_estado * 30 * performance_ratio)
        
        # 3. Cálculo da autossuficiência
        autossuficiencia_percentual = min(100, (geracao_mensal_kwh / consumo_mensal) * 100)
        
        # 4. Cálculo do investimento
        investimento_total = potencia_instalada_kwp * custo_kwp
        
        # 5. Cálculo da economia mensal
        economia_mensal = geracao_mensal_kwh * self.tarifa_energia
        
        # 6. Cálculo do payback (Tempo de retorno do investimento)
        if economia_mensal > 0:
            payback_anos = investimento_total / (economia_mensal * 12)
        else:
            payback_anos = float('inf')
        
        # 7. Cálculo do impacto ambiental
        reducao_co2_ton_ano = (geracao_mensal_kwh * 12 * self.fator_emissao_co2) / 1000
        
        # 8. Cálculo do ROI (Return on Investment) em 25 anos (vida útil do sistema)
        vida_util_anos = 25
        economia_total_vida_util = economia_mensal * 12 * vida_util_anos
        roi_percentual = ((economia_total_vida_util - investimento_total) / investimento_total) * 100
        
        # Resultados formatados
        resultados = {
            'estado': estado,
            'area_disponivel_m2': area_disponivel,
            'irradiacao_kwh_m2_dia': irradiacao_estado,
            'potencia_instalada_kwp': round(potencia_instalada_kwp, 2),
            'geracao_mensal_kwh': round(geracao_mensal_kwh, 2),
            'autossuficiencia_percentual': round(autossuficiencia_percentual, 2),
            'investimento_total': round(investimento_total, 2),
            'economia_mensal': round(economia_mensal, 2),
            'payback_anos': round(payback_anos, 2),
            'reducao_co2_ton_ano': round(reducao_co2_ton_ano, 2),
            'roi_25_anos_percentual': round(roi_percentual, 2),
            'vida_util_anos': vida_util_anos
        }
        
        return resultados
    
    def gerar_cenarios_comparativos(self, consumo_mensal, estado):
        """
        Gera diferentes cenários de instalação solar
        
        Args:
            consumo_mensal (float): Consumo mensal em kWh
            estado (str): Sigla do estado
            
        Returns:
            dict: Dicionário com múltiplos cenários
        """
        cenarios = {
            'pequeno': self.calcular_viabilidade(consumo_mensal, estado, 25),
            'medio': self.calcular_viabilidade(consumo_mensal, estado, 50),
            'grande': self.calcular_viabilidade(consumo_mensal, estado, 100),
            'maximo': self.calcular_viabilidade(consumo_mensal, estado, 200)
        }
        
        return cenarios
    
    def classificar_viabilidade(self, resultados):
        """
        Classifica a viabilidade do projeto solar baseado nos resultados
        
        Args:
            resultados (dict): Resultados da simulação
            
        Returns:
            dict: Classificação e recomendação
        """
        payback = resultados['payback_anos']
        autossuficiencia = resultados['autossuficiencia_percentual']
        roi = resultados['roi_25_anos_percentual']
        
        if payback <= 4 and autossuficiencia >= 50:
            classificacao = 'ALTAMENTE VIÁVEL'
            recomendacao = 'Investimento recomendado - retorno rápido e alto impacto'
            cor = 'green'
        elif payback <= 6 and autossuficiencia >= 30:
            classificacao = 'VIÁVEL' 
            recomendacao = 'Investimento atrativo - bom retorno financeiro'
            cor = 'blue'
        elif payback <= 8:
            classificacao = 'MODERADAMENTE VIÁVEL'
            recomendacao = 'Avaliar outros benefícios além do financeiro'
            cor = 'orange'
        else:
            classificacao = 'POUCO VIÁVEL'
            recomendacao = 'Considerar outras alternativas de eficiência energética'
            cor = 'red'
        
        return {
            'classificacao': classificacao,
            'recomendacao': recomendacao,
            'cor': cor,
            'payback_anos': payback,
            'autossuficiencia_percentual': autossuficiencia
        }

# Exemplo de uso rápido
if __name__ == "__main__":
    simulador = SimpleSolarSimulator()
    resultado = simulador.calcular_viabilidade(5000, 'SP', 50)
    print("Resultado da simulação:", resultado)