# Fitness Tracker - Modelo de nutrición
# ====================================
# Este archivo maneja las operaciones CRUD para comidas

from datetime import datetime
from .database import Database

class NutritionModel:
    """Modelo para manejar comidas en la base de datos"""
    
    def __init__(self):
        """Inicializar el modelo con una conexión a la base de datos"""
        self.db = Database()
    
    def add_meal(self, food, grams, calories, proteins, carbs, fats):
        """Añadir una nueva comida"""
        cursor = self.db.get_connection().cursor()
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        created_at = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO meals (food, grams, calories, proteins, carbs, fats, date, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (food, grams, calories, proteins, carbs, fats, current_date, created_at))
        
        self.db.get_connection().commit()
        return cursor.lastrowid
    
    def get_all_meals(self):
        """Obtener todas las comidas"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('SELECT * FROM meals ORDER BY date DESC, created_at DESC')
        rows = cursor.fetchall()
        # Convertir Row objects a diccionarios
        return [dict(row) for row in rows]
    
    def get_meals_by_date(self, date):
        """Obtener comidas de una fecha específica"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('SELECT * FROM meals WHERE date = ? ORDER BY created_at DESC', (date,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_recent_meals(self, limit=5):
        """Obtener comidas recientes"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('SELECT * FROM meals ORDER BY created_at DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def delete_meal(self, meal_id):
        """Eliminar una comida por ID"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('DELETE FROM meals WHERE id = ?', (meal_id,))
        self.db.get_connection().commit()
        return cursor.rowcount > 0
    
    def get_total_calories(self, date=None):
        """Obtener total de calorías consumidas (opcionalmente por fecha)"""
        cursor = self.db.get_connection().cursor()
        
        if date:
            cursor.execute('SELECT SUM(calories) FROM meals WHERE date = ?', (date,))
        else:
            cursor.execute('SELECT SUM(calories) FROM meals')
        
        result = cursor.fetchone()[0]
        return result if result else 0
    
    def get_nutrition_totals(self, date=None):
        """Obtener totales nutricionales (opcionalmente por fecha)"""
        cursor = self.db.get_connection().cursor()
        
        if date:
            cursor.execute('''
                SELECT SUM(calories) as total_calories, 
                       SUM(proteins) as total_proteins,
                       SUM(carbs) as total_carbs,
                       SUM(fats) as total_fats
                FROM meals WHERE date = ?
            ''', (date,))
        else:
            cursor.execute('''
                SELECT SUM(calories) as total_calories, 
                       SUM(proteins) as total_proteins,
                       SUM(carbs) as total_carbs,
                       SUM(fats) as total_fats
                FROM meals
            ''')
        
        result = cursor.fetchone()
        return {
            'calories': result['total_calories'] if result['total_calories'] else 0,
            'proteins': result['total_proteins'] if result['total_proteins'] else 0,
            'carbs': result['total_carbs'] if result['total_carbs'] else 0,
            'fats': result['total_fats'] if result['total_fats'] else 0
        }
    
    # ===== MÉTODOS PARA FAVORITOS =====
    
    def add_food_favorite(self, food_data):
        """Añadir una comida a favoritos"""
        cursor = self.db.get_connection().cursor()
        
        # Verificar si ya existe
        cursor.execute('''
            SELECT id, usage_count FROM food_favorites 
            WHERE food_name = ? AND display_name = ?
        ''', (food_data['name'], food_data['display_name']))
        
        existing = cursor.fetchone()
        
        if existing:
            # Actualizar contador de uso
            cursor.execute('''
                UPDATE food_favorites 
                SET usage_count = usage_count + 1 
                WHERE id = ?
            ''', (existing['id'],))
            self.db.get_connection().commit()
            return existing['id']
        else:
            # Crear nuevo favorito
            created_at = datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO food_favorites (
                    food_name, display_name, calories_per_100g, 
                    proteins_per_100g, carbs_per_100g, fats_per_100g,
                    brand_owner, category, fdc_id, data_type, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                food_data['name'], food_data['display_name'], 
                food_data['calories_per_100g'],
                food_data.get('proteins_per_100g', 0),
                food_data.get('carbs_per_100g', 0),
                food_data.get('fats_per_100g', 0),
                food_data.get('brand_owner', ''),
                food_data.get('category', ''),
                food_data.get('fdc_id', ''),
                food_data.get('data_type', ''),
                created_at
            ))
            
            self.db.get_connection().commit()
            return cursor.lastrowid
    
    def get_food_favorites(self, limit=10):
        """Obtener comidas favoritas ordenadas por uso"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('''
            SELECT * FROM food_favorites 
            ORDER BY usage_count DESC, created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def remove_food_favorite(self, favorite_id):
        """Eliminar una comida de favoritos"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('DELETE FROM food_favorites WHERE id = ?', (favorite_id,))
        self.db.get_connection().commit()
        return cursor.rowcount > 0
    
    def is_food_favorite(self, food_name, display_name):
        """Verificar si una comida está en favoritos"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('''
            SELECT id FROM food_favorites 
            WHERE food_name = ? AND display_name = ?
        ''', (food_name, display_name))
        
        return cursor.fetchone() is not None
