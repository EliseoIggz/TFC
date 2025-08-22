from typing import Dict, Tuple, Optional
from datetime import date
import pandas as pd

class StatisticsService:
    """Servicio para cálculos estadísticos y métricas de la aplicación"""
    
    def __init__(self, nutrition_service, training_service):
        self.nutrition_service = nutrition_service
        self.training_service = training_service
    
    def calculate_daily_calories_balance(self, date_str: str, nutrition_stats: Dict, training_stats: Dict) -> Dict:
        """Calcular balance calórico diario"""
        try:
            calories_consumed = nutrition_stats.get('calories', 0)
            calories_burned = training_stats.get('total_calories_burned', 0)
            
            # Calcular balance
            balance = calories_consumed - calories_burned
            
            # Determinar estado del balance
            if balance > 0:
                balance_status = 'superavit'
                balance_color = "🔴"
                balance_text = f"+{balance} cal"
                balance_help = "Superávit calórico (ganancia de peso)"
            elif balance < 0:
                balance_status = 'deficit'
                balance_color = "🟢"
                balance_text = f"{balance} cal"
                balance_help = "Déficit calórico (pérdida de peso)"
            else:
                balance_status = 'equilibrio'
                balance_color = "🟡"
                balance_text = "0 cal"
                balance_help = "Equilibrio calórico (mantenimiento de peso)"
            
            return {
                'success': True,
                'data': {
                    'calories_consumed': calories_consumed,
                    'calories_burned': calories_burned,
                    'balance': balance,
                    'balance_status': balance_status,
                    'balance_color': balance_color,
                    'balance_text': balance_text,
                    'balance_help': balance_help
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al calcular balance: {str(e)}',
                'data': None
            }
    
    def calculate_chart_data_for_date(self, date_str: str, nutrition_stats: Dict, training_stats: Dict) -> Dict:
        """Calcular datos para gráficos de una fecha específica"""
        try:
            calories_consumed = nutrition_stats.get('calories', 0)
            calories_burned = training_stats.get('total_calories_burned', 0)
            
            # Verificar si hay datos para mostrar
            has_data = calories_consumed > 0 or calories_burned > 0
            
            return {
                'success': True,
                'data': {
                    'calories_consumed': calories_consumed,
                    'calories_burned': calories_burned,
                    'has_data': has_data,
                    'chart_data': {
                        'consumed': calories_consumed,
                        'burned': calories_burned,
                        'labels': ['Calorías'],
                        'consumed_values': [calories_consumed],
                        'burned_values': [calories_burned]
                    }
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al calcular datos del gráfico: {str(e)}',
                'data': None
            }
    
    def calculate_macros_distribution(self, nutrition_stats: Dict) -> Dict:
        """Calcular distribución de macronutrientes para gráficos"""
        try:
            proteins = nutrition_stats.get('proteins', 0)
            carbs = nutrition_stats.get('carbs', 0)
            fats = nutrition_stats.get('fats', 0)
            
            total = proteins + carbs + fats
            
            if total == 0:
                return {
                    'success': True,
                    'data': {
                        'has_data': False,
                        'distribution': {
                            'proteins': 0,
                            'carbs': 0,
                            'fats': 0,
                            'percentages': {'proteins': 0, 'carbs': 0, 'fats': 0}
                        }
                    }
                }
            
            # Calcular porcentajes
            percentages = {
                'proteins': round((proteins / total) * 100, 1),
                'carbs': round((carbs / total) * 100, 1),
                'fats': round((fats / total) * 100, 1)
            }
            
            return {
                'success': True,
                'data': {
                    'has_data': True,
                    'distribution': {
                        'proteins': proteins,
                        'carbs': carbs,
                        'fats': fats,
                        'percentages': percentages,
                        'chart_data': {
                            'labels': ['Proteínas', 'Carbohidratos', 'Grasas'],
                            'values': [proteins, carbs, fats],
                            'colors': ['#FF6B6B', '#FFD93D', '#45B7D1']
                        }
                    }
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al calcular distribución de macros: {str(e)}',
                'data': None
            }
    
    def calculate_weekly_trends(self, start_date: str, end_date: str) -> Dict:
        """Calcular tendencias semanales de calorías"""
        try:
            # Esta función podría implementarse para mostrar tendencias semanales
            # Por ahora retornamos un placeholder
            return {
                'success': True,
                'data': {
                    'has_data': False,
                    'message': 'Tendencias semanales no implementadas aún'
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al calcular tendencias: {str(e)}',
                'data': None
            }
    
    def format_calories_for_display(self, calories: int) -> str:
        """Formatear calorías para mostrar en la UI"""
        if calories == 0:
            return "0 cal"
        elif calories < 1000:
            return f"{calories} cal"
        else:
            return f"{calories:,} cal".replace(",", ".")
    
    def format_time_for_display(self, minutes: int) -> str:
        """Formatear tiempo para mostrar en la UI"""
        if minutes == 0:
            return "0 min"
        elif minutes < 60:
            return f"{minutes} min"
        else:
            hours = minutes // 60
            remaining_minutes = minutes % 60
            if remaining_minutes == 0:
                return f"{hours}h"
            else:
                return f"{hours}h {remaining_minutes}min"
