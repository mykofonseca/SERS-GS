"""
SERS Global Solution - Módulo de Simulação de Energia Solar
"""

import pandas as pd

class SolarSimulator:
    """
    Classe para simulação de viabilidade de energia solar fotovoltaica
    """
    
    def __init__(self):
        """Inicializa o simulador com dados de irradiação solar"""
        self.irradiation = {
            'SP': 4.5, 'RJ': 4.8, 'MG': 5.2, 'RS': 4.2, 'PR': 4.6,
            'SC': 4.3, 'BA': 5.5, 'CE': 5.8, 'PE': 5.6, 'GO': 5.3,
            'DF': 5.4, 'ES': 4.9
        }
        
        self.cost_per_kwp = 4500
        self.energy_tariff = 0.80
        self.co2_emission_factor = 0.5
    
    def calculate_feasibility(self, monthly_consumption, state, available_area=50, cost_kwp=None):
        """
        Calcula viabilidade de instalação de sistema solar
        
        Args:
            monthly_consumption (float): Consumo mensal em kWh
            state (str): Sigla do estado brasileiro
            available_area (float): Área disponível em m²
            cost_kwp (float): Custo por kWp (opcional)
            
        Returns:
            dict: Resultados da simulação
        """
        if monthly_consumption <= 0:
            raise ValueError("Consumo mensal deve ser maior que zero")
        
        if state not in self.irradiation:
            raise ValueError(f"Estado {state} não encontrado")
        
        if cost_kwp is None:
            cost_kwp = self.cost_per_kwp
        
        state_irradiation = self.irradiation[state]
        
        panel_efficiency = 0.15
        installed_power = available_area * panel_efficiency
        
        performance_ratio = 0.75
        monthly_generation = (installed_power * state_irradiation * 30 * performance_ratio)
        
        self_sufficiency = min(100, (monthly_generation / monthly_consumption) * 100)
        
        total_investment = installed_power * cost_kwp
        monthly_savings = monthly_generation * self.energy_tariff
        
        if monthly_savings > 0:
            payback_years = total_investment / (monthly_savings * 12)
        else:
            payback_years = float('inf')
        
        co2_reduction = (monthly_generation * 12 * self.co2_emission_factor) / 1000
        
        lifespan_years = 25
        total_savings = monthly_savings * 12 * lifespan_years
        roi_25_years = ((total_savings - total_investment) / total_investment) * 100
        
        results = {
            'state': state,
            'available_area': available_area,
            'irradiation': state_irradiation,
            'installed_power': round(installed_power, 2),
            'monthly_generation': round(monthly_generation, 2),
            'self_sufficiency': round(self_sufficiency, 2),
            'total_investment': round(total_investment, 2),
            'monthly_savings': round(monthly_savings, 2),
            'payback_years': round(payback_years, 2),
            'co2_reduction': round(co2_reduction, 2),
            'roi_25_years': round(roi_25_years, 2),
            'lifespan_years': lifespan_years
        }
        
        return results
    
    def generate_comparative_scenarios(self, monthly_consumption, state):
        """
        Gera diferentes cenários de instalação solar
        
        Args:
            monthly_consumption (float): Consumo mensal em kWh
            state (str): Sigla do estado
            
        Returns:
            dict: Dicionário com múltiplos cenários
        """
        scenarios = {
            'pequeno': self.calculate_feasibility(monthly_consumption, state, 25),
            'medio': self.calculate_feasibility(monthly_consumption, state, 50),
            'grande': self.calculate_feasibility(monthly_consumption, state, 100),
            'maximo': self.calculate_feasibility(monthly_consumption, state, 200)
        }
        
        return scenarios
    
    def classify_feasibility(self, results):
        """
        Classifica a viabilidade do projeto solar
        
        Args:
            results (dict): Resultados da simulação
            
        Returns:
            dict: Classificação e recomendação
        """
        payback = results['payback_years']
        self_sufficiency = results['self_sufficiency']
        roi = results['roi_25_years']
        
        if payback <= 4 and self_sufficiency >= 50:
            classification = 'ALTAMENTE VIÁVEL'
            recommendation = 'Investimento recomendado - retorno rápido e alto impacto'
            color = 'green'
        elif payback <= 6 and self_sufficiency >= 30:
            classification = 'VIÁVEL'
            recommendation = 'Investimento atrativo - bom retorno financeiro'
            color = 'blue'
        elif payback <= 8:
            classification = 'MODERADAMENTE VIÁVEL'
            recommendation = 'Avaliar outros benefícios além do financeiro'
            color = 'orange'
        else:
            classification = 'POUCO VIÁVEL'
            recommendation = 'Considerar outras alternativas de eficiência energética'
            color = 'red'
        
        return {
            'classification': classification,
            'recommendation': recommendation,
            'color': color,
            'payback_years': payback,
            'self_sufficiency': self_sufficiency
        }

if __name__ == "__main__":
    simulator = SolarSimulator()
    result = simulator.calculate_feasibility(5000, 'SP', 50)
    print("Resultado da simulação:", result)