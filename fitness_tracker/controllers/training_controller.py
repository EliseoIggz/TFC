# Fitness Tracker - Controlador de Entrenamientos
# ==============================================
# Este archivo maneja la lógica de negocio para entrenamientos

from models.training_model import TrainingModel
from services.training import Training

class TrainingController:
    """Controlador para manejar la lógica de entrenamientos"""
    
    def __init__(self):
        """Inicializar el controlador"""
        self.training_model = TrainingModel()
        self.training_service = Training()
    
    def add_training(self, activity, minutes, user_weight=70.0):
        """Añadir un nuevo entrenamiento"""
        try:
            # Validar datos de entrada
            if not activity or not minutes:
                return {'success': False, 'message': 'Actividad y minutos son requeridos'}
            
            if minutes <= 0 or minutes > 1440:  # Máximo 24 horas
                return {'success': False, 'message': 'Los minutos deben estar entre 1 y 1440'}
            
            if user_weight <= 0 or user_weight > 500:  # Validar peso razonable
                return {'success': False, 'message': 'El peso debe ser un valor válido'}
            
            # Obtener calorías quemadas de la API usando el peso del usuario
            calories_burned = self.training_service.get_calories_burned(activity, minutes, user_weight)
            
            # Guardar en la base de datos
            training_id = self.training_model.add_training(activity, minutes, calories_burned)
            
            if training_id:
                return {
                    'success': True, 
                    'message': f'Entrenamiento registrado: {activity} - {minutes} min - {calories_burned} cal (peso: {user_weight} kg)',
                    'training_id': training_id,
                    'calories_burned': calories_burned,
                    'user_weight': user_weight
                }
            else:
                return {'success': False, 'message': 'Error al guardar el entrenamiento'}
                
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_all_trainings(self):
        """Obtener todos los entrenamientos"""
        try:
            trainings = self.training_model.get_all_trainings()
            return {'success': True, 'data': trainings}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_trainings_by_date(self, date):
        """Obtener entrenamientos de una fecha específica"""
        try:
            trainings = self.training_model.get_trainings_by_date(date)
            return {'success': True, 'data': trainings}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_recent_trainings(self, limit=5):
        """Obtener entrenamientos recientes"""
        try:
            trainings = self.training_model.get_recent_trainings(limit)
            return {'success': True, 'data': trainings}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def delete_training(self, training_id):
        """Eliminar un entrenamiento"""
        try:
            if self.training_model.delete_training(training_id):
                return {'success': True, 'message': 'Entrenamiento eliminado correctamente'}
            else:
                return {'success': False, 'message': 'Entrenamiento no encontrado'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_training_stats(self, date=None):
        """Obtener estadísticas de entrenamiento"""
        try:
            total_calories = self.training_model.get_total_calories_burned(date)
            total_minutes = self.training_model.get_total_minutes(date)
            
            return {
                'success': True,
                'data': {
                    'total_calories_burned': total_calories,
                    'total_minutes': total_minutes,
                    'date': date
                }
            }
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_activity_suggestions(self, query):
        """Obtener sugerencias de actividades basadas en una consulta"""
        try:
            suggestions = self.training_service.search_activities(query)
            return {'success': True, 'data': suggestions}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    # ===== MÉTODOS PARA FAVORITOS =====
    
    def add_exercise_favorite(self, exercise_data):
        """Añadir un ejercicio a favoritos"""
        try:
            favorite_id = self.training_model.add_exercise_favorite(exercise_data)
            if favorite_id:
                return {
                    'success': True,
                    'message': f'"{exercise_data["name"]}" añadido a favoritos',
                    'favorite_id': favorite_id
                }
            else:
                return {'success': False, 'message': 'Error al añadir a favoritos'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_exercise_favorites(self, limit=10):
        """Obtener ejercicios favoritos del usuario"""
        try:
            favorites = self.training_model.get_exercise_favorites(limit)
            return {'success': True, 'data': favorites}
        except Exception as e:
            return {'success': False, 'message': f'Error obteniendo favoritos: {str(e)}'}
    
    def remove_exercise_favorite(self, favorite_id):
        """Eliminar un ejercicio de favoritos"""
        try:
            if self.training_model.remove_exercise_favorite(favorite_id):
                return {'success': True, 'message': 'Ejercicio eliminado de favoritos'}
            else:
                return {'success': False, 'message': 'Error al eliminar de favoritos'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def is_exercise_favorite(self, activity_key):
        """Verificar si un ejercicio está en favoritos"""
        try:
            return self.training_model.is_exercise_favorite(activity_key)
        except Exception as e:
            return False
    
    def quick_add_from_favorite(self, favorite_id, minutes, user_weight=70.0):
        """Añadir rápidamente un ejercicio desde favoritos"""
        try:
            # Obtener datos del favorito
            favorites = self.training_model.get_exercise_favorites(1000)  # Obtener todos
            favorite = next((f for f in favorites if f['id'] == favorite_id), None)
            
            if not favorite:
                return {'success': False, 'message': 'Favorito no encontrado'}
            
            # Calcular calorías quemadas
            calories_burned = self.training_service.get_calories_burned(
                favorite['activity_key'], minutes, user_weight
            )
            
            # Guardar en la base de datos
            training_id = self.training_model.add_training(
                favorite['activity_name'], minutes, calories_burned
            )
            
            if training_id:
                return {
                    'success': True,
                    'message': f'Ejercicio añadido: {favorite["activity_name"]} - {minutes} min - {calories_burned} cal',
                    'training_id': training_id
                }
            else:
                return {'success': False, 'message': 'Error al guardar el entrenamiento'}
                
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
