from typing import Dict
from services.statistics import StatisticsService
from controllers.nutrition_controller import NutritionController
from controllers.training_controller import TrainingController

class StatisticsController:
    """Controlador para manejar estadísticas y métricas de la aplicación"""
    
    def __init__(self, nutrition_controller: NutritionController, training_controller: TrainingController):
        self.nutrition_controller = nutrition_controller
        self.training_controller = training_controller
        self.statistics_service = StatisticsService(
            nutrition_controller.nutrition_api, 
            training_controller.training_service
        )
    
    def get_daily_calories_balance(self, date_str: str) -> Dict:
        """Obtener balance calórico del día"""
        try:
            # Obtener estadísticas nutricionales
            nutrition_stats = self.nutrition_controller.get_nutrition_stats_viewmodel(date_str)
            if not nutrition_stats['success']:
                return {
                    'success': False,
                    'error': 'Error al obtener estadísticas nutricionales',
                    'data': None
                }
            
            # Obtener estadísticas de entrenamiento
            training_stats = self.training_controller.get_training_stats_viewmodel(date_str)
            if not training_stats['success']:
                return {
                    'success': False,
                    'error': 'Error al obtener estadísticas de entrenamiento',
                    'data': None
                }
            
            # Calcular balance usando el servicio
            balance_result = self.statistics_service.calculate_daily_calories_balance(
                date_str,
                nutrition_stats['display_data'],
                training_stats['display_data']
            )
            
            return balance_result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al obtener balance calórico: {str(e)}',
                'data': None
            }
    
    def get_chart_data_for_date(self, date_str: str) -> Dict:
        """Obtener datos para gráficos de una fecha específica"""
        try:
            # Obtener estadísticas nutricionales
            nutrition_stats = self.nutrition_controller.get_nutrition_stats_viewmodel(date_str)
            if not nutrition_stats['success']:
                return {
                    'success': False,
                    'error': 'Error al obtener estadísticas nutricionales',
                    'data': None
                }
            
            # Obtener estadísticas de entrenamiento
            training_stats = self.training_controller.get_training_stats_viewmodel(date_str)
            if not training_stats['success']:
                return {
                    'success': False,
                    'error': 'Error al obtener estadísticas de entrenamiento',
                    'data': None
                }
            
            # Calcular datos del gráfico usando el servicio
            chart_result = self.statistics_service.calculate_chart_data_for_date(
                date_str,
                nutrition_stats['display_data'],
                training_stats['display_data']
            )
            
            return chart_result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al obtener datos del gráfico: {str(e)}',
                'data': None
            }
    
    def get_macros_distribution(self, date_str: str) -> Dict:
        """Obtener distribución de macronutrientes para gráficos"""
        try:
            # Obtener estadísticas nutricionales
            nutrition_stats = self.nutrition_controller.get_nutrition_stats_viewmodel(date_str)
            if not nutrition_stats['success']:
                return {
                    'success': False,
                    'error': 'Error al obtener estadísticas nutricionales',
                    'data': None
                }
            
            # Calcular distribución usando el servicio
            macros_result = self.statistics_service.calculate_macros_distribution(
                nutrition_stats['display_data']
            )
            
            return macros_result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al obtener distribución de macros: {str(e)}',
                'data': None
            }
    
    def get_daily_summary(self, date_str: str) -> Dict:
        """Obtener resumen completo del día para el dashboard"""
        try:
            # Obtener estadísticas nutricionales
            nutrition_stats = self.nutrition_controller.get_nutrition_stats_viewmodel(date_str)
            training_stats = self.training_controller.get_training_stats_viewmodel(date_str)
            
            # Verificar que ambas consultas sean exitosas
            if not nutrition_stats['success'] or not training_stats['success']:
                return {
                    'success': False,
                    'error': 'Error al obtener estadísticas del día',
                    'data': None
                }
            
            # Calcular balance calórico
            balance_result = self.statistics_service.calculate_daily_calories_balance(
                date_str,
                nutrition_stats['display_data'],
                training_stats['display_data']
            )
            
            if not balance_result['success']:
                return balance_result
            
            # Preparar resumen completo
            summary_data = {
                'nutrition': nutrition_stats['display_data'],
                'training': training_stats['display_data'],
                'balance': balance_result['data'],
                'chart_data': {
                    'calories_consumed': nutrition_stats['display_data'].get('calories', 0),
                    'calories_burned': training_stats['display_data'].get('total_calories_burned', 0)
                }
            }
            
            return {
                'success': True,
                'data': summary_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al obtener resumen del día: {str(e)}',
                'data': None
            }
    
    def get_weekly_summary(self, start_date: str, end_date: str) -> Dict:
        """Obtener resumen semanal (placeholder para futuras implementaciones)"""
        try:
            # Por ahora retornamos un placeholder
            # En el futuro se podría implementar agregación semanal
            return {
                'success': True,
                'data': {
                    'has_data': False,
                    'message': 'Resumen semanal no implementado aún',
                    'period': {
                        'start_date': start_date,
                        'end_date': end_date
                    }
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al obtener resumen semanal: {str(e)}',
                'data': None
            }
