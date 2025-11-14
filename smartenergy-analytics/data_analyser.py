"""
Módulo de Análise de Dados de Consumo Energético
SmartEnergy Analytics - Solução Express
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class FastEnergyAnalyzer:
    """
    Classe para análise rápida de dados de consumo energético
    Foco em identificar padrões, desperdícios e oportunidades de economia
    """
    
    def __init__(self):
        """Inicializa o analisador com parâmetros padrão"""
        self.data = None
        self.insights = {}
        
    def generate_basic_data(self, days=7):
        """
        Gera dados simulados realistas de consumo energético corporativo
        
        Args:
            days (int): Número de dias para simular (padrão: 7)
            
        Returns:
            pandas.DataFrame: DataFrame com dados de consumo
        """
        # Gera timestamps horários
        start_date = datetime(2025, 1, 1)
        dates = pd.date_range(start=start_date, periods=days*24, freq='H')
        
        data = []
        for date in dates:
            # Consumo base em kWh
            base_consumption = 50
            
            # Fator horário - maior consumo no horário comercial
            hour = date.hour
            if 8 <= hour <= 18:  # Horário comercial
                hour_factor = 1.8
            else:  # Fora do horário comercial
                hour_factor = 0.6
                
            # Fator diário - menor consumo nos fins de semana
            weekday = date.weekday()
            if weekday >= 5:  # Final de semana
                day_factor = 0.7
            else:  # Dia de semana
                day_factor = 1.0
                
            # Variação aleatória normal
            random_variation = np.random.normal(0, 5)
            
            # Cálculo do consumo final
            consumption = base_consumption * hour_factor * day_factor + random_variation
            consumption = max(consumption, 10)  # Mínimo de 10 kWh
            
            # Dados do registro
            record = {
                'timestamp': date,
                'consumo_kwh': round(consumption, 2),
                'departamento': random.choice(['TI', 'ADMINISTRATIVO', 'COMERCIAL', 'RH']),
                'andar': random.randint(1, 4),
                'hora': hour,
                'dia_semana': weekday
            }
            
            data.append(record)
        
        self.data = pd.DataFrame(data)
        return self.data
    
    def analyze_consumption(self, df):
        """
        Realiza análise rápida dos dados de consumo
        
        Args:
            df (pandas.DataFrame): DataFrame com dados de consumo
            
        Returns:
            dict: Dicionário com insights e métricas
        """
        if df is None or df.empty:
            raise ValueError("DataFrame vazio ou não fornecido")
        
        insights = {}
        
        # 1. Consumo total
        insights['consumo_total'] = round(df['consumo_kwh'].sum(), 2)
        
        # 2. Horário de pico
        hourly_consumption = df.groupby('hora')['consumo_kwh'].mean()
        insights['pico_horario'] = hourly_consumption.idxmax()
        insights['consumo_pico'] = round(hourly_consumption.max(), 2)
        
        # 3. Consumo médio por departamento
        dept_consumption = df.groupby('departamento')['consumo_kwh'].mean()
        insights['departamento_maior_consumo'] = dept_consumption.idxmax()
        insights['consumo_por_departamento'] = dept_consumption.round(2).to_dict()
        
        # 4. Desperdício noturno (consumo entre 0h-6h)
        night_consumption = df[df['hora'].between(0, 6)]['consumo_kwh'].sum()
        insights['desperdicio_noturno'] = round((night_consumption / insights['consumo_total']) * 100, 2)
        
        # 5. Consumo fora do horário comercial (19h-7h)
        off_hours_consumption = df[~df['hora'].between(8, 18)]['consumo_kwh'].sum()
        insights['consumo_fora_expediente'] = round((off_hours_consumption / insights['consumo_total']) * 100, 2)
        
        # 6. Diferença final de semana vs dia de semana
        weekday_avg = df[df['dia_semana'] < 5]['consumo_kwh'].mean()
        weekend_avg = df[df['dia_semana'] >= 5]['consumo_kwh'].mean()
        insights['diferenca_final_semana'] = round(((weekend_avg - weekday_avg) / weekday_avg) * 100, 2)
        
        self.insights = insights
        return insights
    
    def get_recommendations(self, insights):
        """
        Gera recomendações baseadas nos insights da análise
        
        Args:
            insights (dict): Dicionário com insights da análise
            
        Returns:
            list: Lista de recomendações
        """
        recommendations = []
        
        # Recomendações baseadas no desperdício noturno
        if insights['desperdicio_noturno'] > 15:
            recommendations.append({
                'tipo': 'ALTA_PRIORIDADE',
                'titulo': 'Automação de Desligamento Noturno',
                'descricao': f'Desperdício noturno de {insights["desperdicio_noturno"]}% detectado. Implementar sistema automático de desligamento.',
                'economia_estimada': f'{insights["desperdicio_noturno"] * 0.8:.1f}% do consumo total'
            })
        elif insights['desperdicio_noturno'] > 8:
            recommendations.append({
                'tipo': 'MEDIA_PRIORIDADE', 
                'titulo': 'Otimização de Equipamentos Noturnos',
                'descricao': f'Consumo noturno de {insights["desperdicio_noturno"]}%. Avaliar equipamentos que permanecem ligados.',
                'economia_estimada': f'{insights["desperdicio_noturno"] * 0.6:.1f}% do consumo total'
            })
        
        # Recomendações baseadas no consumo fora do expediente
        if insights['consumo_fora_expediente'] > 40:
            recommendations.append({
                'tipo': 'ALTA_PRIORIDADE',
                'titulo': 'Política de Horário Comercial',
                'descricao': f'Alto consumo ({insights["consumo_fora_expediente"]}%) fora do horário comercial. Revisar políticas de uso.',
                'economia_estimada': '15-25% do consumo total'
            })
        
        # Recomendação baseada no departamento com maior consumo
        dept_maior_consumo = insights['departamento_maior_consumo']
        recommendations.append({
            'tipo': 'ANALISE_ESPECIFICA',
            'titulo': f'Otimização no Departamento {dept_maior_consumo}',
            'descricao': f'Departamento com maior consumo médio. Avaliar equipamentos e processos.',
            'economia_estimada': '5-15% do consumo departamental'
        })
        
        return recommendations

# Exemplo de uso rápido
if __name__ == "__main__":
    analyzer = FastEnergyAnalyzer()
    data = analyzer.generate_basic_data(7)
    insights = analyzer.analyze_consumption(data)
    print("Insights:", insights)