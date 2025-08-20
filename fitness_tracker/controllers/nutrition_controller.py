# Fitness Tracker - Controlador de Nutrición
# =========================================
# Este archivo maneja la lógica de negocio para comidas

from typing import Dict
from models.nutrition_model import NutritionModel
from services.nutrition_api import NutritionService

class NutritionController:
    """Controlador para manejar la lógica de nutrición"""
    
    def __init__(self):
        """Inicializar el controlador"""
        self.nutrition_model = NutritionModel()
        self.nutrition_api = NutritionService()
    
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
