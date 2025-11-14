"""
SERS Global Solution - Módulo de Análise de Dados de Consumo Energético
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class EnergyAnalyzer:
    """
    Classe para análise de dados de consumo energético corporativo
    """
    
    def __init__(self):
        """Inicializa o analisador com parâmetros padrão"""
        self.data = None
        self.insights = {}
        
    def generate_consumption_data(self, days=7):
        """
        Gera dados simulados de consumo energético corporativo
        
        Args:
            days (int): Número de dias para simular
            
        Returns:
            pandas.DataFrame: DataFrame com dados de consumo
        """
        start_date = datetime(2025, 1, 1)
        dates = pd.date_range(start=start_date, periods=days*24, freq='H')
        
        data = []
        for date in dates:
            base_consumption = 50
            
            hour = date.hour
            if 8 <= hour <= 18:
                hour_factor = 1.8
            else:
                hour_factor = 0.6
                
            weekday = date.weekday()
            if weekday >= 5:
                day_factor = 0.7
            else:
                day_factor = 1.0
                
            random_variation = np.random.normal(0, 5)
            consumption = base_consumption * hour_factor * day_factor + random_variation
            consumption = max(consumption, 10)
            
            record = {
                'timestamp': date,
                'consumption_kwh': round(consumption, 2),
                'department': random.choice(['TI', 'ADMINISTRATIVO', 'COMERCIAL', 'RH']),
                'floor': random.randint(1, 4),
                'hour': hour,
                'weekday': weekday
            }
            
            data.append(record)
        
        self.data = pd.DataFrame(data)
        return self.data
    
    def analyze_consumption_patterns(self, df):
        """
        Analisa padrões de consumo nos dados
        
        Args:
            df (pandas.DataFrame): DataFrame com dados de consumo
            
        Returns:
            dict: Dicionário com insights da análise
        """
        if df is None or df.empty:
            raise ValueError("DataFrame vazio ou não fornecido")
        
        insights = {}
        
        insights['total_consumption'] = round(df['consumption_kwh'].sum(), 2)
        
        hourly_consumption = df.groupby('hour')['consumption_kwh'].mean()
        insights['peak_hour'] = hourly_consumption.idxmax()
        insights['peak_consumption'] = round(hourly_consumption.max(), 2)
        
        dept_consumption = df.groupby('department')['consumption_kwh'].mean()
        insights['highest_consumption_dept'] = dept_consumption.idxmax()
        insights['department_consumption'] = dept_consumption.round(2).to_dict()
        
        night_consumption = df[df['hour'].between(0, 6)]['consumption_kwh'].sum()
        insights['night_waste'] = round((night_consumption / insights['total_consumption']) * 100, 2)
        
        off_hours_consumption = df[~df['hour'].between(8, 18)]['consumption_kwh'].sum()
        insights['off_hours_consumption'] = round((off_hours_consumption / insights['total_consumption']) * 100, 2)
        
        weekday_avg = df[df['weekday'] < 5]['consumption_kwh'].mean()
        weekend_avg = df[df['weekday'] >= 5]['consumption_kwh'].mean()
        insights['weekend_difference'] = round(((weekend_avg - weekday_avg) / weekday_avg) * 100, 2)
        
        self.insights = insights
        return insights
    
    def generate_recommendations(self, insights):
        """
        Gera recomendações baseadas nos insights da análise
        
        Args:
            insights (dict): Dicionário com insights da análise
            
        Returns:
            list: Lista de recomendações
        """
        recommendations = []
        
        if insights['night_waste'] > 15:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Automação de Desligamento Noturno',
                'description': f'Desperdício noturno de {insights["night_waste"]}% detectado. Implementar sistema automático de desligamento.',
                'estimated_savings': f'{insights["night_waste"] * 0.8:.1f}% do consumo total'
            })
        elif insights['night_waste'] > 8:
            recommendations.append({
                'priority': 'MEDIUM',
                'title': 'Otimização de Equipamentos Noturnos',
                'description': f'Consumo noturno de {insights["night_waste"]}%. Avaliar equipamentos que permanecem ligados.',
                'estimated_savings': f'{insights["night_waste"] * 0.6:.1f}% do consumo total'
            })
        
        if insights['off_hours_consumption'] > 40:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Política de Horário Comercial',
                'description': f'Alto consumo ({insights["off_hours_consumption"]}%) fora do horário comercial. Revisar políticas de uso.',
                'estimated_savings': '15-25% do consumo total'
            })
        
        highest_dept = insights['highest_consumption_dept']
        recommendations.append({
            'priority': 'LOW',
            'title': f'Otimização no Departamento {highest_dept}',
            'description': f'Departamento com maior consumo médio. Avaliar equipamentos e processos.',
            'estimated_savings': '5-15% do consumo departamental'
        })
        
        return recommendations

if __name__ == "__main__":
    analyzer = EnergyAnalyzer()
    data = analyzer.generate_consumption_data(7)
    insights = analyzer.analyze_consumption_patterns(data)
    print("Insights:", insights)