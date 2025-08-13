# Fitness Tracker - API Mock de Deporte
# =====================================
# Este archivo simula una API real para calcular calorías quemadas

import time
import random
import config

class SportAPI:
    """API mock para calcular calorías quemadas en actividades deportivas"""
    
    def __init__(self):
        """Inicializar la API mock"""
        # Base de datos simulada de actividades deportivas
        self.activity_database = {
            'running': {'calories_per_minute': 10, 'intensity': 'high'},
            'correr': {'calories_per_minute': 10, 'intensity': 'high'},
            'caminar': {'calories_per_minute': 4, 'intensity': 'low'},
            'walking': {'calories_per_minute': 4, 'intensity': 'low'},
            'cycling': {'calories_per_minute': 8, 'intensity': 'medium'},
            'ciclismo': {'calories_per_minute': 8, 'intensity': 'medium'},
            'swimming': {'calories_per_minute': 9, 'intensity': 'high'},
            'natación': {'calories_per_minute': 9, 'intensity': 'high'},
            'gym': {'calories_per_minute': 6, 'intensity': 'medium'},
            'pesas': {'calories_per_minute': 6, 'intensity': 'medium'},
            'yoga': {'calories_per_minute': 3, 'intensity': 'low'},
            'pilates': {'calories_per_minute': 3, 'intensity': 'low'},
            'tenis': {'calories_per_minute': 7, 'intensity': 'medium'},
            'fútbol': {'calories_per_minute': 8, 'intensity': 'high'},
            'baloncesto': {'calories_per_minute': 8, 'intensity': 'high'},
            'boxing': {'calories_per_minute': 12, 'intensity': 'very_high'},
            'boxeo': {'calories_per_minute': 12, 'intensity': 'very_high'},
            'dancing': {'calories_per_minute': 5, 'intensity': 'medium'},
            'baile': {'calories_per_minute': 5, 'intensity': 'medium'},
            'hiking': {'calories_per_minute': 6, 'intensity': 'medium'},
            'senderismo': {'calories_per_minute': 6, 'intensity': 'medium'}
        }
    
    def get_calories_burned(self, activity, minutes):
        """Calcular calorías quemadas en una actividad"""
        # Simular delay de API real
        time.sleep(config.MOCK_API_DELAY)
        
        # Buscar la actividad en la base de datos
        activity_lower = activity.lower().strip()
        
        # Si no está en la base de datos, generar valores aleatorios
        if activity_lower not in self.activity_database:
            return self._generate_random_calories(minutes)
        
        # Calcular calorías basadas en los minutos
        activity_info = self.activity_database[activity_lower]
        base_calories = activity_info['calories_per_minute']
        
        # Añadir variabilidad realista (±20%)
        variation = random.uniform(0.8, 1.2)
        total_calories = round(base_calories * minutes * variation)
        
        return total_calories
    
    def _generate_random_calories(self, minutes):
        """Generar calorías aleatorias para actividades desconocidas"""
        # Calorías por minuto entre 3 y 12
        calories_per_minute = random.uniform(3, 12)
        
        # Añadir variabilidad
        variation = random.uniform(0.8, 1.2)
        total_calories = round(calories_per_minute * minutes * variation)
        
        return total_calories
    
    def get_activity_suggestions(self, query):
        """Obtener sugerencias de actividades deportivas"""
        # Simular delay de API real
        time.sleep(config.MOCK_API_DELAY)
        
        query_lower = query.lower()
        suggestions = []
        
        for activity_name in self.activity_database.keys():
            if query_lower in activity_name:
                suggestions.append(activity_name)
        
        return suggestions[:5]  # Máximo 5 sugerencias
    
    def get_activity_intensity(self, activity):
        """Obtener la intensidad de una actividad"""
        activity_lower = activity.lower().strip()
        
        if activity_lower in self.activity_database:
            return self.activity_database[activity_lower]['intensity']
        
        # Intensidad por defecto para actividades desconocidas
        intensities = ['low', 'medium', 'high']
        return random.choice(intensities)
