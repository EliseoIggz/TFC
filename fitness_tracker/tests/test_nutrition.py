# Fitness Tracker - Pruebas del Modelo de Nutrición
# =================================================
# Este archivo contiene pruebas unitarias para nutrición

import pytest
import os
import tempfile
from models.nutrition_model import NutritionModel
from models.database import Database

class TestNutritionModel:
    """Pruebas para el modelo de nutrición"""
    
    def setup_method(self):
        """Configurar prueba - crear base de datos temporal"""
        # Crear base de datos temporal para pruebas
        self.temp_dir = tempfile.mkdtemp()
        self.original_db_path = Database.DATABASE_PATH
        Database.DATABASE_PATH = os.path.join(self.temp_dir, "test_fitness_tracker.db")
        
        # Crear nueva instancia del modelo
        self.nutrition_model = NutritionModel()
    
    def teardown_method(self):
        """Limpiar después de la prueba"""
        # Restaurar configuración original
        Database.DATABASE_PATH = self.original_db_path
        
        # Limpiar archivos temporales
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_add_meal(self):
        """Probar añadir una comida"""
        # Añadir comida
        meal_id = self.nutrition_model.add_meal("pollo", 150, 250, 45.5, 0, 5.4)
        
        # Verificar que se creó
        assert meal_id is not None
        assert meal_id > 0
        
        # Verificar que se guardó en la base de datos
        meals = self.nutrition_model.get_all_meals()
        assert len(meals) == 1
        
        meal = meals[0]
        assert meal['food'] == "pollo"
        assert meal['grams'] == 150
        assert meal['calories'] == 250
        assert meal['proteins'] == 45.5
        assert meal['carbs'] == 0
        assert meal['fats'] == 5.4
    
    def test_get_all_meals(self):
        """Probar obtener todas las comidas"""
        # Añadir varias comidas
        self.nutrition_model.add_meal("pollo", 150, 250, 45.5, 0, 5.4)
        self.nutrition_model.add_meal("arroz", 100, 130, 2.7, 28, 0.3)
        
        # Obtener todas
        meals = self.nutrition_model.get_all_meals()
        
        # Verificar resultados
        assert len(meals) == 2
        assert meals[0]['food'] == "arroz"  # Más reciente primero
        assert meals[1]['food'] == "pollo"
    
    def test_get_meals_by_date(self):
        """Probar obtener comidas por fecha"""
        # Añadir comidas
        self.nutrition_model.add_meal("pollo", 150, 250, 45.5, 0, 5.4)
        self.nutrition_model.add_meal("arroz", 100, 130, 2.7, 28, 0.3)
        
        # Obtener por fecha actual
        from datetime import date
        today = date.today().strftime('%Y-%m-%d')
        meals = self.nutrition_model.get_meals_by_date(today)
        
        # Verificar resultados
        assert len(meals) == 2
    
    def test_get_recent_meals(self):
        """Probar obtener comidas recientes"""
        # Añadir varias comidas
        for i in range(10):
            self.nutrition_model.add_meal(f"food_{i}", 100, 100, 10, 10, 5)
        
        # Obtener solo 5 recientes
        recent = self.nutrition_model.get_recent_meals(5)
        assert len(recent) == 5
        
        # Verificar que son las más recientes
        assert recent[0]['food'] == "food_9"
    
    def test_delete_meal(self):
        """Probar eliminar una comida"""
        # Añadir comida
        meal_id = self.nutrition_model.add_meal("pollo", 150, 250, 45.5, 0, 5.4)
        
        # Verificar que existe
        meals = self.nutrition_model.get_all_meals()
        assert len(meals) == 1
        
        # Eliminar
        success = self.nutrition_model.delete_meal(meal_id)
        assert success is True
        
        # Verificar que se eliminó
        meals = self.nutrition_model.get_all_meals()
        assert len(meals) == 0
    
    def test_get_total_calories(self):
        """Probar obtener total de calorías"""
        # Añadir comidas
        self.nutrition_model.add_meal("pollo", 150, 250, 45.5, 0, 5.4)
        self.nutrition_model.add_meal("arroz", 100, 130, 2.7, 28, 0.3)
        
        # Obtener total
        total = self.nutrition_model.get_total_calories()
        assert total == 380
    
    def test_get_nutrition_totals(self):
        """Probar obtener totales nutricionales"""
        # Añadir comidas
        self.nutrition_model.add_meal("pollo", 150, 250, 45.5, 0, 5.4)
        self.nutrition_model.add_meal("arroz", 100, 130, 2.7, 28, 0.3)
        
        # Obtener totales
        totals = self.nutrition_model.get_nutrition_totals()
        
        # Verificar resultados
        assert totals['calories'] == 380
        assert totals['proteins'] == 48.2  # 45.5 + 2.7
        assert totals['carbs'] == 28.0     # 0 + 28
        assert totals['fats'] == 5.7       # 5.4 + 0.3

if __name__ == "__main__":
    # Ejecutar pruebas si se ejecuta directamente
    pytest.main([__file__])
