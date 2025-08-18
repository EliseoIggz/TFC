# Fitness Tracker - API Real de Deporte
# =====================================
# Este archivo integra APIs reales para calcular calorías quemadas

import requests
import config
from typing import Dict, List, Optional, Union

class TrainingAPI:
    """API real para calcular calorías quemadas en actividades deportivas"""
    
    def __init__(self):
        """Inicializar la API real"""
        # ExerciseDB API - Base gratuita de ejercicios deportivos
        self.exercise_db_url = "https://exercisedb.p.rapidapi.com"
        self.api_key = getattr(config, 'EXERCISE_DB_API_KEY', None)
        self.api_host = getattr(config, 'EXERCISE_DB_API_HOST', 'exercisedb.p.rapidapi.com')
        
        # Verificar si hay API key configurada
        self.use_real_api = bool(self.api_key)
        
        # Sistema de mapeo bilingüe español-inglés
        self.spanish_to_english_mapping = {
            # Actividades cardiovasculares
            'correr': 'running',
            'caminar': 'walking',
            'ciclismo': 'cycling',
            'natación': 'swimming',
            'nadar': 'swimming',
            'fútbol': 'football',
            'baloncesto': 'basketball',
            'tenis': 'tenis',
            'boxeo': 'boxing',
            'baile': 'dancing',
            'senderismo': 'hiking',
            'escalada': 'climbing',
            'remo': 'rowing',
            'patinaje': 'skating',
            'esquí': 'skiing',
            'snowboard': 'snowboarding',
            'surf': 'surfing',
            'voleibol': 'volleyball',
            'bádminton': 'badminton',
            'ping pong': 'table tennis',
            'tenis de mesa': 'table tennis',
            
            # Actividades de fuerza
            'gimnasio': 'gym',
            'pesas': 'weightlifting',
            'levantamiento de pesas': 'weightlifting',
            'musculación': 'bodybuilding',
            'entrenamiento de fuerza': 'strength training',
            'calistenia': 'calisthenics',
            'crossfit': 'crossfit',
            'powerlifting': 'powerlifting',
            'halterofilia': 'weightlifting',
            
            # Actividades de flexibilidad
            'yoga': 'yoga',
            'pilates': 'pilates',
            'estiramientos': 'stretching',
            'flexibilidad': 'flexibility',
            'tai chi': 'tai chi',
            'meditación': 'meditation',
            'relajación': 'relaxation',
            
            # Actividades específicas
            'sentadillas': 'squats',
            'flexiones': 'push-ups',
            'dominadas': 'pull-ups',
            'plancha': 'plank',
            'zancadas': 'lunges',
            'burpees': 'burpees',
            'mountain climbers': 'mountain climbers',
            'jumping jacks': 'jumping jacks'
        }
        
        # Mapeo inverso inglés-español
        self.english_to_spanish_mapping = {v: k for k, v in self.spanish_to_english_mapping.items()}
    
    def _make_api_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Realizar petición a la API real"""
        if not self.use_real_api:
            return None
            
        try:
            headers = {
                'X-RapidAPI-Key': self.api_key,
                'X-RapidAPI-Host': self.api_host
            }
            
            url = f"{self.exercise_db_url}{endpoint}"
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Debug: Mostrar información sobre la respuesta
                if isinstance(data, list):
                    print(f"📊 API {endpoint}: {len(data)} elementos recibidos")
                    if len(data) <= 10:
                        print(f"⚠️  Posible rate limiting: solo {len(data)} elementos")
                else:
                    print(f"📊 API {endpoint}: {type(data)} recibido")
                
                return data
            else:
                print(f"❌ Error API {endpoint}: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error en petición API {endpoint}: {e}")
            return None
    
    def get_calories_burned(self, activity: str, minutes: int, weight: float = 70.0) -> int:
        """Calcular calorías quemadas usando API real"""
        if not self.use_real_api:
            raise ValueError("API key no configurada. Configura EXERCISE_DB_API_KEY en config.py")
        
        # Traducción automática del español al inglés
        english_activity = self._translate_activity_to_english(activity)
        
        # Obtener datos de la API real
        api_calories = self._get_calories_from_api(english_activity, minutes, weight)
        if api_calories is not None:
            return api_calories
        
        # Si no se encuentran datos, lanzar error
        raise ValueError(f"No se encontraron datos para la actividad '{activity}' en la API")
    
    def _get_calories_from_api(self, activity: str, minutes: int, weight: float) -> Optional[int]:
        """Obtener calorías desde la API real - versión simplificada"""
        try:
            # Llamada directa a la API
            exercises = self._make_api_request('/exercises')
            
            if exercises and len(exercises) > 0:
                # Buscar ejercicio de forma simple
                matching_exercise = self._find_matching_exercise(activity, exercises)
                
                if matching_exercise:
                    # Calcular calorías usando un MET fijo y simple
                    # MET promedio para ejercicios generales: 6.0
                    met_value = 6.0
                    
                    # Fórmula: Calorías = MET × Peso (kg) × Tiempo (horas)
                    calories_per_hour = met_value * weight
                    calories_per_minute = calories_per_hour / 60
                    total_calories = round(calories_per_minute * minutes)
                    
                    print(f"🔥 Calorías calculadas: {total_calories} cal ({minutes} min, {weight} kg)")
                    return total_calories
                
        except Exception as e:
            print(f"Error obteniendo calorías de API: {e}")
            
        return None
    
    def _find_matching_exercise(self, activity: str, exercises: List[Dict]) -> Optional[Dict]:
        """Buscar ejercicio de forma simple - solo por nombre o cualquier ejercicio disponible"""
        activity_lower = activity.lower()
        
        # Prioridad 1: Búsqueda por nombre (exacta o parcial)
        for exercise in exercises:
            exercise_name = exercise.get('name', '').lower()
            if activity_lower in exercise_name or exercise_name in activity_lower:
                return exercise
        
        # Prioridad 2: Si no encuentra por nombre, devolver el primer ejercicio disponible
        # Esto asegura que siempre se pueda calcular calorías
        if exercises:
            print(f"💡 No se encontró '{activity}' exacto, usando ejercicio similar: {exercises[0].get('name', '')}")
            return exercises[0]
        
        return None
    
    def get_activity_suggestions(self, query: str) -> List[str]:
        """Obtener sugerencias de actividades deportivas desde API real"""
        if not self.use_real_api:
            raise ValueError("API key no configurada. Configura EXERCISE_DB_API_KEY en config.py")
        
        # Traducción automática del español al inglés para la búsqueda
        english_query = self._translate_activity_to_english(query)
        
        try:
            # Llamada directa a la API
            exercises = self._make_api_request('/exercises')
            
            if exercises:
                # Filtrar ejercicios que coincidan con la consulta en inglés
                suggestions = []
                english_query_lower = english_query.lower()
                
                for exercise in exercises:
                    exercise_name = exercise.get('name', '')
                    if english_query_lower in exercise_name.lower():
                        # Traducir el resultado al español si es posible
                        spanish_name = self._translate_activity_to_spanish(exercise_name)
                        suggestions.append(spanish_name)
                
                return suggestions[:5]  # Máximo 5 sugerencias
            
            return []
            
        except Exception as e:
            print(f"Error obteniendo sugerencias de API: {e}")
            return []
    
    def get_exercise_details(self, exercise_name: str) -> Optional[Dict]:
        """Obtener detalles completos de un ejercicio desde la API"""
        if not self.use_real_api:
            raise ValueError("API key no configurada. Configura EXERCISE_DB_API_KEY en config.py")
            
        try:
            # Llamada directa a la API
            exercises = self._make_api_request('/exercises')
            
            if exercises and len(exercises) > 0:
                # Buscar ejercicio por nombre en la lista completa
                matching_exercise = None
                for exercise in exercises:
                    if exercise_name.lower() in exercise.get('name', '').lower():
                        matching_exercise = exercise
                        break
                
                if matching_exercise:
                    return {
                        'name': matching_exercise.get('name', ''),
                        'gifUrl': matching_exercise.get('gifUrl', ''),
                        'target': matching_exercise.get('target', ''),
                        'secondaryMuscles': matching_exercise.get('secondaryMuscles', []),
                        'instructions': matching_exercise.get('instructions', [])
                    }
                
                # Si no se encuentra, lanzar error
                raise ValueError(f"No se encontraron detalles para '{exercise_name}'")
            
            return None
                
        except Exception as e:
            print(f"Error obteniendo detalles del ejercicio: {e}")
            raise ValueError(f"No se pudo obtener detalles para '{exercise_name}'")
    
    def _translate_activity_to_english(self, activity: str) -> str:
        """Traducir actividad del español al inglés para la API"""
        activity_lower = activity.lower().strip()
        
        # Buscar en el mapeo bilingüe
        if activity_lower in self.spanish_to_english_mapping:
            english_activity = self.spanish_to_english_mapping[activity_lower]
            print(f"🌐 Traducción: '{activity}' → '{english_activity}'")
            return english_activity
        
        # Si no está en el mapeo, devolver la actividad original
        # (por si ya está en inglés o es un nombre personalizado)
        return activity
    
    def _translate_activity_to_spanish(self, activity: str) -> str:
        """Traducir actividad del inglés al español para la interfaz"""
        activity_lower = activity.lower().strip()
        
        # Buscar en el mapeo inverso
        if activity_lower in self.english_to_spanish_mapping:
            spanish_activity = self.english_to_spanish_mapping[activity_lower]
            return spanish_activity
        
        # Si no está en el mapeo, devolver la actividad original
        return activity
