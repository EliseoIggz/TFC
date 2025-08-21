# Limen - Pruebas del Modelo de Entrenamientos
# ======================================================
# Este archivo contiene pruebas unitarias para entrenamientos

import pytest
import os
import tempfile
from models.training_model import TrainingModel
from models.database import Database

class TestTrainingModel:
    """Pruebas para el modelo de entrenamientos"""
    
    def setup_method(self):
        """Configurar prueba - crear base de datos temporal"""
        # Crear base de datos temporal para pruebas
        self.temp_dir = tempfile.mkdtemp()
        self.original_db_path = Database.DATABASE_PATH
        Database.DATABASE_PATH = os.path.join(self.temp_dir, "test_fitness_tracker.db")
        
        # Crear nueva instancia del modelo
        self.training_model = TrainingModel()
    
    def teardown_method(self):
        """Limpiar después de la prueba"""
        # Restaurar configuración original
        Database.DATABASE_PATH = self.original_db_path
        
        # Limpiar archivos temporales
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_add_training(self):
        """Probar añadir un entrenamiento"""
        # Añadir entrenamiento
        training_id = self.training_model.add_training("running", 30, 300)
        
        # Verificar que se creó
        assert training_id is not None
        assert training_id > 0
        
        # Verificar que se guardó en la base de datos
        trainings = self.training_model.get_all_trainings()
        assert len(trainings) == 1
        
        training = trainings[0]
        assert training['activity'] == "running"
        assert training['minutes'] == 30
        assert training['calories_burned'] == 300
    
    def test_get_all_trainings(self):
        """Probar obtener todos los entrenamientos"""
        # Añadir varios entrenamientos
        self.training_model.add_training("running", 30, 300)
        self.training_model.add_training("gym", 45, 270)
        
        # Obtener todos
        trainings = self.training_model.get_all_trainings()
        
        # Verificar resultados
        assert len(trainings) == 2
        assert trainings[0]['activity'] == "gym"  # Más reciente primero
        assert trainings[1]['activity'] == "running"
    
    def test_get_trainings_by_date(self):
        """Probar obtener entrenamientos por fecha"""
        # Añadir entrenamientos
        self.training_model.add_training("running", 30, 300)
        self.training_model.add_training("gym", 45, 270)
        
        # Obtener por fecha actual
        from datetime import date
        today = date.today().strftime('%Y-%m-%d')
        trainings = self.training_model.get_trainings_by_date(today)
        
        # Verificar resultados
        assert len(trainings) == 2
    
    def test_get_recent_trainings(self):
        """Probar obtener entrenamientos recientes"""
        # Añadir varios entrenamientos
        for i in range(10):
            self.training_model.add_training(f"activity_{i}", 30, 300)
        
        # Obtener solo 5 recientes
        recent = self.training_model.get_recent_trainings(5)
        assert len(recent) == 5
        
        # Verificar que son los más recientes
        assert recent[0]['activity'] == "activity_9"
    
    def test_delete_training(self):
        """Probar eliminar un entrenamiento"""
        # Añadir entrenamiento
        training_id = self.training_model.add_training("running", 30, 300)
        
        # Verificar que existe
        trainings = self.training_model.get_all_trainings()
        assert len(trainings) == 1
        
        # Eliminar
        success = self.training_model.delete_training(training_id)
        assert success is True
        
        # Verificar que se eliminó
        trainings = self.training_model.get_all_trainings()
        assert len(trainings) == 0
    
    def test_get_total_calories_burned(self):
        """Probar obtener total de calorías quemadas"""
        # Añadir entrenamientos
        self.training_model.add_training("running", 30, 300)
        self.training_model.add_training("gym", 45, 270)
        
        # Obtener total
        total = self.training_model.get_total_calories_burned()
        assert total == 570
    
    def test_get_total_minutes(self):
        """Probar obtener total de minutos"""
        # Añadir entrenamientos
        self.training_model.add_training("running", 30, 300)
        self.training_model.add_training("gym", 45, 270)
        
        # Obtener total
        total = self.training_model.get_total_minutes()
        assert total == 75

if __name__ == "__main__":
    # Ejecutar pruebas si se ejecuta directamente
    pytest.main([__file__])
