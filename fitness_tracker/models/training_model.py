# Fitness Tracker - Modelo de entrenamientos
# =========================================
# Este archivo maneja las operaciones CRUD para entrenamientos

from datetime import datetime
from .database import Database

class TrainingModel:
    """Modelo para manejar entrenamientos en la base de datos"""
    
    def __init__(self):
        """Inicializar el modelo con una conexión a la base de datos"""
        self.db = Database()
    
    def add_training(self, activity, minutes, calories_burned):
        """Añadir un nuevo entrenamiento"""
        cursor = self.db.get_connection().cursor()
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        created_at = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO trainings (activity, minutes, calories_burned, date, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (activity, minutes, calories_burned, current_date, created_at))
        
        self.db.get_connection().commit()
        return cursor.lastrowid
    
    def get_all_trainings(self):
        """Obtener todos los entrenamientos"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('SELECT * FROM trainings ORDER BY date DESC, created_at DESC')
        return cursor.fetchall()
    
    def get_trainings_by_date(self, date):
        """Obtener entrenamientos de una fecha específica"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('SELECT * FROM trainings WHERE date = ? ORDER BY created_at DESC', (date,))
        return cursor.fetchall()
    
    def get_recent_trainings(self, limit=5):
        """Obtener entrenamientos recientes"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('SELECT * FROM trainings ORDER BY created_at DESC LIMIT ?', (limit,))
        return cursor.fetchall()
    
    def delete_training(self, training_id):
        """Eliminar un entrenamiento por ID"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('DELETE FROM trainings WHERE id = ?', (training_id,))
        self.db.get_connection().commit()
        return cursor.rowcount > 0
    
    def get_total_calories_burned(self, date=None):
        """Obtener total de calorías quemadas (opcionalmente por fecha)"""
        cursor = self.db.get_connection().cursor()
        
        if date:
            cursor.execute('SELECT SUM(calories_burned) FROM trainings WHERE date = ?', (date,))
        else:
            cursor.execute('SELECT SUM(calories_burned) FROM trainings')
        
        result = cursor.fetchone()[0]
        return result if result else 0
    
    def get_total_minutes(self, date=None):
        """Obtener total de minutos de entrenamiento (opcionalmente por fecha)"""
        cursor = self.db.get_connection().cursor()
        
        if date:
            cursor.execute('SELECT SUM(minutes) FROM trainings WHERE date = ?', (date,))
        else:
            cursor.execute('SELECT SUM(minutes) FROM trainings')
        
        result = cursor.fetchone()[0]
        return result if result else 0
