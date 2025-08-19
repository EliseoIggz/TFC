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
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_trainings_by_date(self, date):
        """Obtener entrenamientos de una fecha específica"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('SELECT * FROM trainings WHERE date = ? ORDER BY created_at DESC', (date,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_recent_trainings(self, limit=5):
        """Obtener entrenamientos recientes"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('SELECT * FROM trainings ORDER BY created_at DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
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
    
    # ===== MÉTODOS PARA FAVORITOS =====
    
    def add_exercise_favorite(self, exercise_data):
        """Añadir un ejercicio a favoritos"""
        cursor = self.db.get_connection().cursor()
        
        # Verificar si ya existe
        cursor.execute('''
            SELECT id, usage_count FROM exercise_favorites 
            WHERE activity_key = ?
        ''', (exercise_data['key'],))
        
        existing = cursor.fetchone()
        
        if existing:
            # Actualizar contador de uso
            cursor.execute('''
                UPDATE exercise_favorites 
                SET usage_count = usage_count + 1 
                WHERE id = ?
            ''', (existing['id'],))
            self.db.get_connection().commit()
            return existing['id']
        else:
            # Crear nuevo favorito
            created_at = datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO exercise_favorites (
                    activity_name, activity_key, met_value, category, created_at
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                exercise_data['name'], exercise_data['key'], 
                exercise_data['met'], exercise_data['category'], created_at
            ))
            
            self.db.get_connection().commit()
            return cursor.lastrowid
    
    def get_exercise_favorites(self, limit=10):
        """Obtener ejercicios favoritos ordenados por uso"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('''
            SELECT * FROM exercise_favorites 
            ORDER BY usage_count DESC, created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def remove_exercise_favorite(self, favorite_id):
        """Eliminar un ejercicio de favoritos"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('DELETE FROM exercise_favorites WHERE id = ?', (favorite_id,))
        self.db.get_connection().commit()
        return cursor.rowcount > 0
    
    def is_exercise_favorite(self, activity_key):
        """Verificar si un ejercicio está en favoritos"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('''
            SELECT id FROM exercise_favorites 
            WHERE activity_key = ?
        ''', (activity_key,))
        
        return cursor.fetchone() is not None
