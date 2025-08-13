# Fitness Tracker - Controlador de Nutrición
# =========================================
# Este archivo maneja la lógica de negocio para comidas

from models.nutrition_model import NutritionModel
from services.nutrition_api import NutritionAPI

class NutritionController:
    """Controlador para manejar la lógica de nutrición"""
    
    def __init__(self):
        """Inicializar el controlador"""
        self.nutrition_model = NutritionModel()
        self.nutrition_api = NutritionAPI()
    
    def add_meal(self, food, grams):
        """Añadir una nueva comida"""
        try:
            # Validar datos de entrada
            if not food or not grams:
                return {'success': False, 'message': 'Alimento y gramos son requeridos'}
            
            if grams <= 0 or grams > 10000:  # Máximo 10 kg
                return {'success': False, 'message': 'Los gramos deben estar entre 1 y 10000'}
            
            # Obtener información nutricional de la API
            nutrition_info = self.nutrition_api.get_nutrition_info(food, grams)
            
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
                    'message': f'Comida registrada: {food} - {grams}g - {nutrition_info["calories"]} cal',
                    'meal_id': meal_id,
                    'nutrition_info': nutrition_info
                }
            else:
                return {'success': False, 'message': 'Error al guardar la comida'}
                
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
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
    
    def get_nutrition_stats(self, date=None):
        """Obtener estadísticas nutricionales"""
        try:
            nutrition_totals = self.nutrition_model.get_nutrition_totals(date)
            total_calories = self.nutrition_model.get_total_calories(date)
            
            return {
                'success': True,
                'data': {
                    'total_calories': total_calories,
                    'total_proteins': nutrition_totals['proteins'],
                    'total_carbs': nutrition_totals['carbs'],
                    'total_fats': nutrition_totals['fats'],
                    'date': date
                }
            }
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def search_food(self, query):
        """Buscar alimentos"""
        try:
            results = self.nutrition_api.search_food(query)
            return {'success': True, 'data': results}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_food_suggestions(self, query):
        """Obtener sugerencias de alimentos"""
        try:
            suggestions = self.nutrition_api.search_food(query)
            return {'success': True, 'data': suggestions}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
