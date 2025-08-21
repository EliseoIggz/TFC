# Fitness Tracker - Controlador de Nutrición
# =========================================
# Este archivo maneja la lógica de negocio para comidas

from typing import Dict, Optional, List
from models.nutrition_model import NutritionModel
from services.nutrition_api import NutritionService
import pandas as pd

class NutritionController:
    """Controlador para manejar la lógica de nutrición"""
    
    def __init__(self, training_controller=None):
        """Inicializar el controlador"""
        self.nutrition_model = NutritionModel()
        self.nutrition_api = NutritionService()
        self.training_controller = training_controller
    
    def add_meal(self, food, grams):
        """Añadir una nueva comida"""
        try:
            # Validar datos de entrada
            if not food or not grams:
                return {'success': False, 'message': 'Alimento y gramos son requeridos'}
            
            if grams <= 0 or grams > 10000:  # Máximo 10 kg
                return {'success': False, 'message': 'Los gramos deben estar entre 1 y 10000'}
            
            # Obtener información nutricional de la API de USDA
            nutrition_info = self.nutrition_api.get_nutrition_info(food, grams)
            
            # Verificar si hay múltiples opciones
            if isinstance(nutrition_info, dict) and nutrition_info.get('multiple_options'):
                return {
                    'success': False,
                    'multiple_options': True,
                    'options_data': nutrition_info,
                    'message': f'Se encontraron {len(nutrition_info["options"])} opciones para "{food}". Selecciona una opción específica.'
                }
            
            # Guardar en la base de datos
            meal_id = self.nutrition_model.add_meal(
                food, 
                grams, 
                nutrition_info['calories'],
                nutrition_info['proteins'],
                nutrition_info['carbs'],
                nutrition_info['fats']
            )
            
            if meal_id:
                return {
                    'success': True, 
                    'message': f'Comida registrada: {nutrition_info["product_name"]} - {grams}g - {nutrition_info["calories"]} cal',
                    'meal_id': meal_id,
                    'nutrition_info': nutrition_info
                }
            else:
                return {'success': False, 'message': 'Error al guardar la comida'}
                
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def add_meal_from_selection(self, options_data: Dict, selected_index: int) -> Dict:
        """Añadir comida desde una opción seleccionada por el usuario"""
        try:
            # Obtener información nutricional del producto seleccionado
            nutrition_info = self.nutrition_api.get_nutrition_from_selected_option(options_data, selected_index)
            
            # Obtener datos originales
            food_name = options_data['options'][selected_index]['name']
            grams = options_data['grams']
            
            # Guardar en la base de datos
            meal_id = self.nutrition_model.add_meal(
                food_name,
                grams,
                nutrition_info['calories'],
                nutrition_info['proteins'],
                nutrition_info['carbs'],
                nutrition_info['fats']
            )
            
            if meal_id:
                return {
                    'success': True,
                    'message': f'Comida registrada: {food_name} - {grams}g - {nutrition_info["calories"]} cal',
                    'meal_id': meal_id,
                    'nutrition_info': nutrition_info
                }
            else:
                return {'success': False, 'message': 'Error al guardar la comida seleccionada'}
                
        except Exception as e:
            return {'success': False, 'message': f'Error procesando selección: {str(e)}'}
    
    def get_all_meals(self):
        """Obtener todas las comidas"""
        try:
            meals = self.nutrition_model.get_all_meals()
            return {'success': True, 'data': meals}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_meals_by_date(self, date):
        """Obtener comidas de una fecha específica"""
        try:
            meals = self.nutrition_model.get_meals_by_date(date)
            return {'success': True, 'data': meals}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_recent_meals(self, limit=5):
        """Obtener comidas recientes"""
        try:
            meals = self.nutrition_model.get_recent_meals(limit)
            return {'success': True, 'data': meals}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def delete_meal(self, meal_id):
        """Eliminar una comida"""
        try:
            if self.nutrition_model.delete_meal(meal_id):
                return {'success': True, 'message': 'Comida eliminada correctamente'}
            else:
                return {'success': False, 'message': 'Comida no encontrada'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_nutrition_stats(self, date):
        """Obtener estadísticas nutricionales de una fecha"""
        try:
            totals = self.nutrition_model.get_nutrition_totals(date)
            return {'success': True, 'data': totals}
        except Exception as e:
            return {'success': False, 'message': f'Error obteniendo estadísticas: {str(e)}'}
    

    
    def search_food(self, query):
        """Buscar alimentos en USDA"""
        try:
            results = self.nutrition_api.search_food(query)
            return {'success': True, 'data': results}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_food_suggestions(self, query):
        """Obtener sugerencias de alimentos desde USDA"""
        try:
            suggestions = self.nutrition_api.get_food_suggestions(query)
            return {'success': True, 'data': suggestions}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_activity_suggestions(self, query):
        """Obtener sugerencias de actividades basadas en una consulta"""
        try:
            suggestions = self.nutrition_api.search_foods(query)
            return {'success': True, 'data': suggestions}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    # ========================================
    # MÉTODOS DE LÓGICA DE NEGOCIO (RESPETANDO MVC)
    # ========================================
    
    def get_calories_balance(self, date_str: str) -> Dict:
        """
        Obtener balance calórico del día (RESPETANDO MVC)
        Retorna: {'success': bool, 'data': Dict, 'error': Optional[str]}
        """
        try:
            nutrition_stats = self.get_nutrition_stats(date_str)
            
            if not self.training_controller:
                return {
                    'success': False,
                    'error': 'Training controller no disponible'
                }
            
            training_stats = self.training_controller.get_training_stats(date_str)
            
            if not nutrition_stats['success'] or not training_stats['success']:
                return {
                    'success': False,
                    'error': 'No se pudieron obtener las estadísticas'
                }
            
            calories_consumed = nutrition_stats['data']['calories']
            calories_burned = training_stats['data']['total_calories_burned']
            
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
                'error': f'Error al calcular balance: {str(e)}'
            }
    
    def get_macro_recommendations(self, objetivo: str) -> Dict:
        """
        Obtener recomendaciones de macronutrientes (RESPETANDO MVC)
        Retorna: {'success': bool, 'data': Dict}
        """
        recomendaciones = {
            "mantener_peso": {
                "nombre": "Mantener Peso",
                "protein": "15-25%",
                "carbs": "45-55%",
                "fat": "25-35%",
                "protein_value": 20,
                "carbs_value": 50,
                "fat_value": 30
            },
            "perdida_grasa": {
                "nombre": "Pérdida de Grasa",
                "protein": "25-35%",
                "carbs": "30-40%",
                "fat": "25-30%",
                "protein_value": 30,
                "carbs_value": 35,
                "fat_value": 35
            },
            "ganancia_musculo": {
                "nombre": "Ganancia de Músculo",
                "protein": "25-35%",
                "carbs": "40-50%",
                "fat": "20-30%",
                "protein_value": 30,
                "carbs_value": 45,
                "fat_value": 25
            },
            "resistencia_cardio": {
                "nombre": "Resistencia y Cardio",
                "protein": "15-20%",
                "carbs": "55-65%",
                "fat": "20-25%",
                "protein_value": 18,
                "carbs_value": 60,
                "fat_value": 22
            },
            "fuerza_maxima": {
                "nombre": "Fuerza Máxima",
                "protein": "25-30%",
                "carbs": "40-50%",
                "fat": "20-30%",
                "protein_value": 28,
                "carbs_value": 45,
                "fat_value": 27
            }
        }
        
        return {
            'success': True,
            'data': recomendaciones.get(objetivo, recomendaciones["mantener_peso"])
        }
    
    def get_macro_recommendations_viewmodel(self, objetivo: str) -> Dict:
        """
        ViewModel para recomendaciones de macronutrientes (RESPETANDO MVC)
        Retorna: {'success': bool, 'data': Dict, 'chart_data': Dict}
        """
        try:
            recomendacion = self.get_macro_recommendations(objetivo)
            
            if not recomendacion['success']:
                return {
                    'success': False,
                    'error': 'Error al obtener recomendaciones de macronutrientes',
                    'data': None,
                    'chart_data': None
                }
            
            data = recomendacion['data']
            
            # Preparar datos para el gráfico
            chart_data = {
                'labels': [
                    data['protein'], 
                    data['carbs'], 
                    data['fat']
                ],
                'values': [data["protein_value"], data["carbs_value"], data["fat_value"]],
                'colors': ['#FF6B6B', '#FFD93D', '#45B7D1'],
                'title': f"Recomendado: {data['nombre']}"
            }
            
            return {
                'success': True,
                'data': data,
                'chart_data': chart_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al generar ViewModel de recomendaciones: {str(e)}',
                'data': None,
                'chart_data': None
            }
    
    def format_meals_for_display(self, meals_result: Dict, selected_date) -> Dict:
        """
        Formatear comidas para mostrar en la vista (RESPETANDO MVC)
        Retorna: {'success': bool, 'data': Dict, 'formatted_data': Optional[DataFrame]}
        """
        try:
            if not meals_result['success'] or not meals_result['data']:
                return {
                    'success': False,
                    'data': meals_result,
                    'formatted_data': None
                }
            
            meals_df = pd.DataFrame(meals_result['data'])
            meals_display = meals_df[['id', 'food', 'grams', 'calories', 'proteins', 'carbs', 'fats', 'created_at']].copy()
            meals_display.columns = ['ID', 'Alimento', 'Gramos', 'Calorías', 'Proteínas', 'Carbohidratos', 'Grasas', 'Hora']
            meals_display['Hora'] = pd.to_datetime(meals_df['created_at']).dt.strftime('%H:%M')
            
            return {
                'success': True,
                'data': meals_result,
                'formatted_data': meals_display,
                'count': len(meals_result['data'])
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al formatear comidas: {str(e)}'
            }
    
    def get_nutrition_stats_display_data(self, nutrition_stats: Dict) -> Dict:
        """
        Preparar datos de estadísticas nutricionales para mostrar (RESPETANDO MVC)
        Retorna: {'success': bool, 'data': Dict}
        """
        try:
            if not nutrition_stats['success']:
                return {
                    'success': False,
                    'error': 'No hay estadísticas nutricionales disponibles'
                }
            
            data = nutrition_stats['data']
            display_data = {
                'calories': data.get('calories', 0),
                'proteins': data.get('proteins', 0),
                'carbs': data.get('carbs', 0),
                'fats': data.get('fats', 0),
                'calories_formatted': f"{data.get('calories', 0)} cal",
                'proteins_formatted': f"{data.get('proteins', 0):.1f}g",
                'carbs_formatted': f"{data.get('carbs', 0):.1f}g",
                'fats_formatted': f"{data.get('fats', 0):.1f}g"
            }
            
            return {
                'success': True,
                'data': display_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al preparar datos nutricionales: {str(e)}'
            }
    
    def get_training_stats_display_data(self, training_stats: Dict) -> Dict:
        """
        Preparar datos de estadísticas de entrenamiento para mostrar (RESPETANDO MVC)
        Retorna: {'success': bool, 'data': Dict}
        """
        try:
            if not training_stats['success']:
                return {
                    'success': False,
                    'error': 'No hay estadísticas de entrenamiento disponibles'
                }
            
            data = training_stats['data']
            display_data = {
                'total_calories_burned': data.get('total_calories_burned', 0),
                'total_minutes': data.get('total_minutes', 0),
                'calories_formatted': f"{data.get('total_calories_burned', 0)} cal",
                'minutes_formatted': f"{data.get('total_minutes', 0)} min"
            }
            
            return {
                'success': True,
                'data': display_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al preparar datos de entrenamiento: {str(e)}'
            }
    
    def format_meal_row_for_display(self, row: Dict) -> Dict:
        """
        Formatear una fila de comida para mostrar (RESPETANDO MVC)
        Retorna: {'success': bool, 'data': Dict}
        """
        try:
            display_data = {
                'id': row.get('id', ''),
                'food': row.get('food', ''),
                'grams': row.get('grams', 0),
                'calories': row.get('calories', 0),
                'proteins': row.get('proteins', 0),
                'created_at': row.get('created_at', ''),
                'food_display': f"🍽️ **{row.get('food', '')}** - {row.get('grams', 0)}g - {row.get('calories', 0)} cal - {row.get('proteins', 0)}g prot",
                'time_formatted': pd.to_datetime(row.get('created_at', '')).strftime('%H:%M') if row.get('created_at') else '',
                'delete_key': f"delete_meal_{row.get('id', '')}"
            }
            
            return {
                'success': True,
                'data': display_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al formatear fila de comida: {str(e)}'
            }
    
    def format_training_row_for_display(self, row: Dict) -> Dict:
        """
        Formatear una fila de entrenamiento para mostrar (RESPETANDO MVC)
        Retorna: {'success': bool, 'data': Dict}
        """
        try:
            display_data = {
                'id': row.get('id', ''),
                'activity': row.get('activity', ''),
                'minutes': row.get('minutes', 0),
                'calories_burned': row.get('calories_burned', 0),
                'created_at': row.get('created_at', ''),
                'activity_display': f"💪 **{row.get('activity', '')}** - {row.get('minutes', 0)} min - {row.get('calories_burned', 0)} cal",
                'time_formatted': pd.to_datetime(row.get('created_at', '')).strftime('%H:%M') if row.get('created_at') else '',
                'delete_key': f"delete_training_{row.get('id', '')}"
            }
            
            return {
                'success': True,
                'data': display_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al formatear fila de entrenamiento: {str(e)}'
            }
    
    def get_meals_table_data(self, meals_result: Dict, selected_date) -> Dict:
        """
        Obtener datos de tabla de comidas completamente procesados (RESPETANDO MVC)
        Retorna: {'success': bool, 'data': Dict, 'formatted_rows': List}
        """
        try:
            if not meals_result['success'] or not meals_result['data']:
                return {
                    'success': False,
                    'data': meals_result,
                    'formatted_rows': [],
                    'count': 0
                }
            
            # Formatear todas las filas
            formatted_rows = []
            for row in meals_result['data']:
                row_display = self.format_meal_row_for_display(row)
                if row_display['success']:
                    formatted_rows.append(row_display['data'])
                else:
                    print(f"Error al formatear fila: {row_display['error']}")
            
            return {
                'success': True,
                'data': meals_result,
                'formatted_rows': formatted_rows,
                'count': len(meals_result['data'])
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al procesar tabla de comidas: {str(e)}'
            }
    
    def get_trainings_table_data(self, trainings_result: Dict, selected_date) -> Dict:
        """
        Obtener datos de tabla de entrenamientos completamente procesados (RESPETANDO MVC)
        Retorna: {'success': bool, 'data': Dict, 'formatted_rows': List}
        """
        try:
            if not trainings_result['success'] or not trainings_result['data']:
                return {
                    'success': False,
                    'data': trainings_result,
                    'formatted_rows': [],
                    'count': 0
                }
            
            # Formatear todas las filas
            formatted_rows = []
            for row in trainings_result['data']:
                row_display = self.format_training_row_for_display(row)
                if row_display['success']:
                    formatted_rows.append(row_display['data'])
                else:
                    print(f"Error al formatear fila: {row_display['error']}")
            
            return {
                'success': True,
                'data': trainings_result,
                'formatted_rows': formatted_rows,
                'count': len(trainings_result['data'])
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al procesar tabla de entrenamientos: {str(e)}'
            }
    
    # ========================================
    # VIEWMODELS PARA NUTRITION (RESPETANDO MVC)
    # ========================================
    
    def get_meal_form_viewmodel(self, food: str, grams: int) -> Dict:
        """
        ViewModel completo para el formulario de comidas (RESPETANDO MVC)
        La vista solo necesita renderizar, sin lógica ni validaciones
        """
        try:
            # Validar datos de entrada
            if not food or not grams:
                return {
                    'success': False,
                    'error': 'Alimento y gramos son requeridos',
                    'form_data': None
                }
            
            if grams <= 0 or grams > 10000:
                return {
                    'success': False,
                    'error': 'Los gramos deben estar entre 1 y 10000',
                    'form_data': None
                }
            
            # Obtener información nutricional de la API de USDA
            nutrition_info = self.nutrition_api.get_nutrition_info(food, grams)
            
            # Verificar si hay múltiples opciones
            if isinstance(nutrition_info, dict) and nutrition_info.get('multiple_options'):
                return {
                    'success': False,
                    'multiple_options': True,
                    'options_data': nutrition_info,
                    'message': f'Se encontraron {len(nutrition_info["options"])} opciones para "{food}". Selecciona una opción específica.',
                    'form_data': {
                        'search_term': food,
                        'grams': grams,
                        'options_count': len(nutrition_info["options"])
                    }
                }
            
            # Preparar datos para la vista
            form_data = {
                'food': food,
                'grams': grams,
                'nutrition_info': nutrition_info,
                'display_data': {
                    'product_name': nutrition_info.get('product_name', food),
                    'calories': nutrition_info.get('calories', 0),
                    'proteins': nutrition_info.get('proteins', 0),
                    'carbs': nutrition_info.get('carbs', 0),
                    'fats': nutrition_info.get('fats', 0),
                    'calories_per_100g': nutrition_info.get('calories_per_100g', 0),
                    'proteins_per_100g': nutrition_info.get('proteins_per_100g', 0),
                    'carbs_per_100g': nutrition_info.get('carbs_per_100g', 0),
                    'fats_per_100g': nutrition_info.get('fats_per_100g', 0)
                }
            }
            
            return {
                'success': True,
                'form_data': form_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al generar ViewModel: {str(e)}',
                'form_data': None
            }
    
    def get_meal_form_submission_result(self, food: str, grams: int) -> Dict:
        """
        Procesar envío del formulario de comidas (RESPETANDO MVC)
        Retorna resultado completo para la vista
        """
        try:
            # Validar datos antes de enviar
            if not food or not grams:
                return {
                    'success': False,
                    'message': 'Alimento y gramos son requeridos',
                    'should_show_warnings': True
                }
            
            if grams <= 0 or grams > 10000:
                return {
                    'success': False,
                    'message': 'Los gramos deben estar entre 1 y 10000',
                    'should_show_warnings': True
                }
            
            # Añadir comida
            result = self.add_meal(food, grams)
            
            # Si hay múltiples opciones, devolverlas
            if result.get('multiple_options'):
                return {
                    'success': False,
                    'multiple_options': True,
                    'options_data': result['options_data'],
                    'message': result['message'],
                    'should_show_warnings': False
                }
            
            if result['success']:
                return {
                    'success': True,
                    'message': result['message'],
                    'should_clear_form': True,
                    'should_rerun': True,
                    'meal_data': {
                        'id': result['meal_id'],
                        'food': food,
                        'grams': grams,
                        'nutrition_info': result['nutrition_info']
                    }
                }
            else:
                return {
                    'success': False,
                    'message': result['message'],
                    'should_show_warnings': False
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al procesar comida: {str(e)}',
                'should_show_warnings': False
            }
    
    def get_food_selector_viewmodel(self, options_data: Dict) -> Dict:
        """
        ViewModel para selector de alimentos (RESPETANDO MVC)
        """
        try:
            if not options_data or 'options' not in options_data:
                return {
                    'success': False,
                    'error': 'Datos de opciones no válidos',
                    'selector_data': None
                }
            
            options = options_data['options']
            search_term = options_data.get('search_term', '')
            grams = options_data.get('grams', 0)
            
            # Preparar opciones para la vista
            option_labels = [opt['display_name'] for opt in options]
            
            # Preparar datos de producto seleccionado
            selected_product_data = {
                'search_term': search_term,
                'grams': grams,
                'options_count': len(options),
                'option_labels': option_labels,
                'radio_key': f"food_radio_{search_term}_{len(options)}",
                'confirm_key': f"confirm_food_{search_term}"
            }
            
            return {
                'success': True,
                'selector_data': selected_product_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al generar ViewModel del selector: {str(e)}',
                'selector_data': None
            }
    
    def get_food_selection_result(self, options_data: Dict, selected_index: int) -> Dict:
        """
        Procesar selección de alimento (RESPETANDO MVC)
        """
        try:
            if selected_index is None or selected_index < 0:
                return {
                    'success': False,
                    'message': 'Índice de selección no válido',
                    'should_show_warnings': True
                }
            
            # Añadir comida desde selección
            result = self.add_meal_from_selection(options_data, selected_index)
            
            if result['success']:
                return {
                    'success': True,
                    'message': result['message'],
                    'should_clear_selector': True,
                    'should_rerun': True,
                    'meal_data': {
                        'id': result['meal_id'],
                        'food_name': options_data['options'][selected_index]['name'],
                        'grams': options_data['grams'],
                        'nutrition_info': result['nutrition_info']
                    }
                }
            else:
                return {
                    'success': False,
                    'message': result['message'],
                    'should_show_warnings': False
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al procesar selección: {str(e)}',
                'should_show_warnings': False
            }
    
    def get_nutrition_stats_viewmodel(self, date_str: str) -> Dict:
        """
        ViewModel para estadísticas nutricionales (RESPETANDO MVC)
        """
        try:
            nutrition_stats = self.get_nutrition_stats(date_str)
            
            if not nutrition_stats['success']:
                return {
                    'success': False,
                    'error': 'No hay estadísticas nutricionales disponibles',
                    'display_data': None
                }
            
            data = nutrition_stats['data']
            display_data = {
                'calories': data.get('calories', 0),
                'proteins': data.get('proteins', 0),
                'carbs': data.get('carbs', 0),
                'fats': data.get('fats', 0),
                'calories_formatted': f"{data.get('calories', 0)} cal",
                'proteins_formatted': f"{data.get('proteins', 0):.1f}g",
                'carbs_formatted': f"{data.get('carbs', 0):.1f}g",
                'fats_formatted': f"{data.get('fats', 0):.1f}g",
                'has_data': data.get('calories', 0) > 0
            }
            
            return {
                'success': True,
                'display_data': display_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al obtener estadísticas: {str(e)}',
                'display_data': None
            }
    
    def get_meals_table_viewmodel(self, meals_result: Dict, selected_date) -> Dict:
        """
        ViewModel completo para tabla de comidas (RESPETANDO MVC)
        """
        try:
            if not meals_result['success'] or not meals_result['data']:
                from utils.helpers import format_date_display
                date_display = format_date_display(selected_date)
                return {
                    'success': True,
                    'has_data': False,
                    'message': f"📭 No hay comidas registradas para {'hoy' if date_display == 'hoy' else f'el {date_display}'}",
                    'table_data': None
                }
            
            # Formatear todas las filas
            formatted_rows = []
            for row in meals_result['data']:
                row_display = self.format_meal_row_for_display(row)
                if row_display['success']:
                    formatted_rows.append(row_display['data'])
                else:
                    print(f"Error al formatear fila de comida: {row_display['error']}")
                    continue
            
            from utils.helpers import format_date_display
            date_display = format_date_display(selected_date)
            count = len(formatted_rows)
            
            return {
                'success': True,
                'has_data': True,
                'table_data': {
                    'rows': formatted_rows,
                    'count': count,
                    'date_display': date_display,
                    'header_message': f"🍽️ Comidas de {'hoy' if date_display == 'hoy' else f'el {date_display}'} ({count} registros)"
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al procesar tabla de comidas: {str(e)}',
                'has_data': False,
                'table_data': None
            }
    
    def delete_meal_with_feedback(self, meal_id: str) -> Dict:
        """
        Eliminar comida con feedback completo (RESPETANDO MVC)
        """
        try:
            result = self.delete_meal(meal_id)
            
            return {
                'success': result['success'],
                'message': result['message'],
                'should_rerun': result['success'],
                'feedback_type': 'success' if result['success'] else 'error'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al eliminar comida: {str(e)}',
                'should_rerun': False,
                'feedback_type': 'error'
            }
