# Limen - Controlador de Entrenamientos
# =============================================
# Este archivo maneja la lógica de negocio para entrenamientos

from models.training_model import TrainingModel
from services.training import TrainingService
from typing import Dict, Optional, List
from utils.helpers import format_date_display
import pandas as pd

class TrainingController:
    """Controlador para manejar la lógica de entrenamientos"""
    
    def __init__(self):
        """Inicializar el controlador"""
        self.training_model = TrainingModel()
        self.training_service = TrainingService()
    
    def add_training(self, activity, minutes, user_weight=70.0):
        """Añadir un nuevo entrenamiento"""
        try:
            # Validar datos de entrada usando el servicio (RESPETANDO MVC)
            validation_result = self.training_service.validate_training_input(str(minutes), activity)
            if not validation_result['valid']:
                return {'success': False, 'message': validation_result['error']}
            
            # Validar peso del usuario
            if user_weight <= 0 or user_weight > 500:  # Validar peso razonable
                return {'success': False, 'message': 'El peso debe ser un valor válido'}
            
            # Obtener calorías quemadas de la API usando el peso del usuario
            calories_burned = self.training_service.get_calories_burned(activity, minutes, user_weight)
            
            # Guardar en la base de datos
            training_id = self.training_model.add_training(activity, minutes, calories_burned)
            
            if training_id:
                return {
                    'success': True, 
                    'message': '',
                    'training_id': training_id,
                    'calories_burned': calories_burned,
                    'user_weight': user_weight
                }
            else:
                return {'success': False, 'message': 'Error al guardar el entrenamiento'}
                
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def validate_training_form(self, minutes_input: str, selected_sport: str) -> Dict:
        """
        Validar formulario de entrenamiento usando el servicio (RESPETANDO MVC)
        Retorna: {'valid': bool, 'minutes': Optional[int], 'error': Optional[str]}
        """
        return self.training_service.validate_training_input(minutes_input, selected_sport)
    
    def get_training_preview(self, selected_sport: str, minutes: int, user_weight: float) -> Dict:
        """
        Obtener vista previa del entrenamiento (RESPETANDO MVC)
        Retorna: {'sport_info': Dict, 'estimated_calories': int, 'valid': bool}
        """
        return self.training_service.get_training_preview(selected_sport, minutes, user_weight)
    
    def validate_sport_selection(self, selected_category: str, selected_sport_key: str) -> Dict:
        """
        Validar selección de deporte (RESPETANDO MVC)
        Retorna: {'valid': bool, 'selected_sport': Optional[str], 'error': Optional[str]}
        """
        return self.training_service.validate_sport_selection(selected_category, selected_sport_key)
    
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
            suggestions = self.training_service.search_sports(query)
            return {'success': True, 'data': suggestions}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_sports_database_stats(self):
        """Obtener estadísticas de la base de datos de deportes (RESPETANDO MVC)"""
        try:
            categories = self.training_service.get_sport_categories()
            total_sports = len(self.training_service.sports_database)
            total_categories = len(categories)
            
            return {
                'success': True,
                'data': {
                    'total_sports': total_sports,
                    'total_categories': total_categories,
                    'categories': categories
                }
            }
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    # ========================================
    # VIEWMODEL PARA TRAINING (RESPETANDO MVC)
    # ========================================
    
    def get_training_form_viewmodel(self, minutes_input: str, selected_sport: str, user_weight: float) -> Dict:
        """
        ViewModel completo para el formulario de training (RESPETANDO MVC)
        La vista solo necesita renderizar, sin lógica ni validaciones
        """
        try:
            # Obtener categorías y deportes procesados
            categories_result = self.get_sports_database_stats()
            if not categories_result['success']:
                return {
                    'success': False,
                    'error': 'Error al cargar categorías de deportes',
                    'form_data': None
                }
            
            categories = categories_result['data']['categories']
            
            # Preparar opciones de categorías para la vista
            emojis = {
                'deporte_equipo': '🏀', 'deporte_raqueta': '🎾', 'deporte_acuatico': '🏊‍♂️',
                'deporte_invierno': '⛷️', 'deporte_combate': '🥊', 'deporte_resistencia': '🏃‍♂️',
                'deporte_fuerza': '💪', 'deporte_aventura': '🧗‍♂️', 'deporte_baile': '💃',
                'deporte_precision': '🎯', 'fitness': '🧘‍♀️', 'ejercicio_fuerza': '🏋️',
                'actividad_diaria': '🚶‍♂️', 'deporte_extremo': '🪂', 'deporte_motor': '🏍️',
                'deporte_tradicional': '🏺', 'deporte_acuatico_extremo': '🏄‍♂️', 'deporte_invierno_extremo': '🎿'
            }
            
            category_options = [''] + ['Todas'] + list(categories.keys())
            category_display_names = {k: f"{emojis.get(k, '🏃‍♂️')} {k.replace('_', ' ').title()}" for k in categories.keys()}
            
            # Obtener deportes disponibles
            all_sports_result = self.get_activity_suggestions("")
            if not all_sports_result['success']:
                return {
                    'success': False,
                    'error': 'Error al cargar deportes',
                    'form_data': None
                }
            
            all_sports = all_sports_result['data']
            
            # Validar formulario
            validation_result = self.validate_training_form(minutes_input, selected_sport)
            
            # Obtener preview si es válido
            preview_data = None
            if validation_result['valid'] and selected_sport and validation_result.get('minutes'):
                preview_result = self.get_training_preview(selected_sport, validation_result['minutes'], user_weight)
                if preview_result['valid']:
                    preview_data = {
                        'sport_name': preview_result['sport_info']['name'],
                        'sport_category': preview_result['sport_info']['category'],
                        'estimated_calories': preview_result['estimated_calories'],
                        'display_text': f"📊 **{preview_result['sport_info']['name']}** - {preview_result['sport_info']['category']}",
                        'calories_text': f"🔥 **Calorías estimadas:** {preview_result['estimated_calories']} cal"
                    }
            
            # Estadísticas de la base de datos
            stats_data = {
                'total_sports': categories_result['data']['total_sports'],
                'total_categories': categories_result['data']['total_categories']
            }
            
            return {
                'success': True,
                'form_data': {
                    'categories': {
                        'options': category_options,
                        'display_names': category_display_names,
                        'format_func': lambda x: "Escoge una categoría" if x == '' else (category_display_names.get(x, x) if x != 'Todas' else 'Todas')
                    },
                    'sports': {
                        'all_sports': all_sports,
                        'categories_map': categories
                    },
                    'validation': {
                        'is_valid': validation_result['valid'],
                        'error_message': validation_result.get('error'),
                        'minutes': validation_result.get('minutes'),
                        'show_error': not validation_result['valid'] and bool(minutes_input)
                    },
                    'preview': preview_data,
                    'stats': stats_data,
                    'form_state': {
                        'minutes_placeholder': "Introduce el tiempo",
                        'minutes_help': "Valor entre 1 y 1440 minutos",
                        'sport_placeholder': "Escoge un deporte"
                    }
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al generar ViewModel: {str(e)}',
                'form_data': None
            }
    
    def get_training_form_submission_result(self, selected_sport: str, minutes: int, user_weight: float) -> Dict:
        """
        Procesar envío del formulario de training (RESPETANDO MVC)
        Retorna resultado completo para la vista
        """
        try:
            # Validar datos antes de enviar
            validation_result = self.validate_training_form(str(minutes), selected_sport)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'message': validation_result['error'],
                    'should_show_warnings': True,
                    'warnings': {
                        'sport_missing': not selected_sport,
                        'minutes_invalid': minutes is None or minutes <= 0
                    }
                }
            
            # Añadir entrenamiento
            result = self.add_training(selected_sport, minutes, user_weight)
            
            if result['success']:
                # Obtener información del deporte para el mensaje de éxito
                preview_result = self.get_training_preview(selected_sport, minutes, user_weight)
                success_message = "✅ Entrenamiento añadido exitosamente!"
                if preview_result['valid']:
                    success_message += f" Has quemado {preview_result['estimated_calories']} calorías."
                
                return {
                    'success': True,
                    'message': success_message,
                    'should_clear_form': True,
                    'should_rerun': True,
                    'clear_form_data': {
                        'category_index': 1,  # 'Todas'
                        'minutes': ''
                    },
                    'training_data': {
                        'id': result['training_id'],
                        'calories_burned': result['calories_burned'],
                        'sport': selected_sport,
                        'minutes': minutes
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
                'message': f'Error al procesar entrenamiento: {str(e)}',
                'should_show_warnings': False
            }
    
    def get_training_stats_viewmodel(self, date_str: str) -> Dict:
        """
        ViewModel para estadísticas de training (RESPETANDO MVC)
        """
        try:
            training_stats = self.get_training_stats(date_str)
            
            if not training_stats['success']:
                return {
                    'success': False,
                    'error': 'No hay estadísticas de entrenamiento disponibles',
                    'display_data': None
                }
            
            data = training_stats['data']
            display_data = {
                'total_calories_burned': data.get('total_calories_burned', 0),
                'total_minutes': data.get('total_minutes', 0),
                'calories_formatted': f"{data.get('total_calories_burned', 0)} cal",
                'minutes_formatted': f"{data.get('total_minutes', 0)} min",
                'has_data': data.get('total_calories_burned', 0) > 0 or data.get('total_minutes', 0) > 0
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
    
    def get_trainings_table_viewmodel(self, trainings_result: Dict, selected_date) -> Dict:
        """
        ViewModel completo para tabla de entrenamientos (RESPETANDO MVC)
        """
        try:
            if not trainings_result['success'] or not trainings_result['data']:
                date_display = format_date_display(selected_date)
                return {
                    'success': True,
                    'has_data': False,
                    'message': f"📭 No hay entrenamientos registrados para {'hoy' if date_display == 'hoy' else f'el {date_display}'}",
                    'table_data': None
                }
            
            # Formatear todas las filas
            formatted_rows = []
            for row in trainings_result['data']:
                try:
                    display_data = {
                        'id': row.get('id', ''),
                        'activity': row.get('activity', ''),
                        'minutes': row.get('minutes', 0),
                        'calories_burned': row.get('calories_burned', 0),
                        'created_at': row.get('created_at', ''),
                        'display_text': f"💪 **{row.get('activity', '')}** - {row.get('minutes', 0)} min - {row.get('calories_burned', 0)} cal",
                        'time_formatted': pd.to_datetime(row.get('created_at', '')).strftime('%H:%M') if row.get('created_at') else '',
                        'delete_key': f"delete_training_{row.get('id', '')}"
                    }
                    formatted_rows.append(display_data)
                except Exception as row_error:
                    print(f"Error al formatear fila de entrenamiento: {row_error}")
                    continue
            
            date_display = format_date_display(selected_date)
            count = len(formatted_rows)
            
            return {
                'success': True,
                'has_data': True,
                'table_data': {
                    'rows': formatted_rows,
                    'count': count,
                    'date_display': date_display,
                    'header_message': f"🏃‍♂️ Entrenamientos de {'hoy' if date_display == 'hoy' else f'el {date_display}'} ({count} registros)"
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al procesar tabla de entrenamientos: {str(e)}',
                'has_data': False,
                'table_data': None
            }
    
    def delete_training_with_feedback(self, training_id: str) -> Dict:
        """
        Eliminar entrenamiento con feedback completo (RESPETANDO MVC)
        """
        try:
            result = self.delete_training(training_id)
            
            return {
                'success': result['success'],
                'message': result['message'],
                'should_rerun': result['success'],
                'feedback_type': 'success' if result['success'] else 'error'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al eliminar entrenamiento: {str(e)}',
                'should_rerun': False,
                'feedback_type': 'error'
            }

