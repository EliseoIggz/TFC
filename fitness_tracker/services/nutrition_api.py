# Fitness Tracker - API Mock de Nutrición
# ======================================
# Este archivo simula una API real para obtener información nutricional

import time
import random
import config

class NutritionAPI:
    """API mock para obtener información nutricional de alimentos"""
    
    def __init__(self):
        """Inicializar la API mock"""
        # Base de datos simulada de alimentos comunes
        self.food_database = {
            'pollo': {'calories_per_100g': 165, 'proteins_per_100g': 31, 'carbs_per_100g': 0, 'fats_per_100g': 3.6},
            'arroz': {'calories_per_100g': 130, 'proteins_per_100g': 2.7, 'carbs_per_100g': 28, 'fats_per_100g': 0.3},
            'huevo': {'calories_per_100g': 155, 'proteins_per_100g': 13, 'carbs_per_100g': 1.1, 'fats_per_100g': 11},
            'manzana': {'calories_per_100g': 52, 'proteins_per_100g': 0.3, 'carbs_per_100g': 14, 'fats_per_100g': 0.2},
            'plátano': {'calories_per_100g': 89, 'proteins_per_100g': 1.1, 'carbs_per_100g': 23, 'fats_per_100g': 0.3},
            'leche': {'calories_per_100g': 42, 'proteins_per_100g': 3.4, 'carbs_per_100g': 5, 'fats_per_100g': 1},
            'pan': {'calories_per_100g': 265, 'proteins_per_100g': 9, 'carbs_per_100g': 49, 'fats_per_100g': 3.2},
            'atún': {'calories_per_100g': 144, 'proteins_per_100g': 30, 'carbs_per_100g': 0, 'fats_per_100g': 1},
            'brócoli': {'calories_per_100g': 34, 'proteins_per_100g': 2.8, 'carbs_per_100g': 7, 'fats_per_100g': 0.4},
            'pasta': {'calories_per_100g': 131, 'proteins_per_100g': 5, 'carbs_per_100g': 25, 'fats_per_100g': 1.1}
        }
    
    def get_nutrition_info(self, food, grams):
        """Obtener información nutricional de un alimento"""
        # Simular delay de API real
        time.sleep(config.MOCK_API_DELAY)
        
        # Buscar el alimento en la base de datos
        food_lower = food.lower().strip()
        
        # Si no está en la base de datos, generar valores aleatorios
        if food_lower not in self.food_database:
            return self._generate_random_nutrition(grams)
        
        # Calcular valores basados en los gramos
        food_info = self.food_database[food_lower]
        multiplier = grams / 100
        
        return {
            'calories': round(food_info['calories_per_100g'] * multiplier),
            'proteins': round(food_info['proteins_per_100g'] * multiplier, 1),
            'carbs': round(food_info['carbs_per_100g'] * multiplier, 1),
            'fats': round(food_info['fats_per_100g'] * multiplier, 1)
        }
    
    def _generate_random_nutrition(self, grams):
        """Generar valores nutricionales aleatorios para alimentos desconocidos"""
        # Valores aproximados por 100g
        calories_per_100g = random.randint(50, 300)
        proteins_per_100g = random.uniform(1, 25)
        carbs_per_100g = random.uniform(0, 60)
        fats_per_100g = random.uniform(0, 20)
        
        multiplier = grams / 100
        
        return {
            'calories': round(calories_per_100g * multiplier),
            'proteins': round(proteins_per_100g * multiplier, 1),
            'carbs': round(carbs_per_100g * multiplier, 1),
            'fats': round(fats_per_100g * multiplier, 1)
        }
    
    def search_food(self, query):
        """Buscar alimentos en la base de datos"""
        # Simular delay de API real
        time.sleep(config.MOCK_API_DELAY)
        
        query_lower = query.lower()
        results = []
        
        for food_name in self.food_database.keys():
            if query_lower in food_name:
                results.append(food_name)
        
        return results[:5]  # Máximo 5 resultados
