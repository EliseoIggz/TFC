# Fitness Tracker - Conexión a la base de datos
# =============================================
# Este archivo maneja la conexión a SQLite y crea las tablas necesarias

import sqlite3
import os
from datetime import datetime
import config

class Database:
    """Clase para manejar la conexión a la base de datos SQLite"""
    
    def __init__(self):
        """Inicializar la conexión a la base de datos"""
        # Crear directorio data si no existe
        os.makedirs(os.path.dirname(config.DATABASE_PATH), exist_ok=True)
        
        # Conectar a la base de datos
        self.conn = sqlite3.connect(config.DATABASE_PATH)
        self.conn.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
        
        # Crear tablas si no existen
        self.create_tables()
    
    def create_tables(self):
        """Crear las tablas necesarias en la base de datos"""
        cursor = self.conn.cursor()
        
        # Tabla de entrenamientos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trainings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity TEXT NOT NULL,
                minutes INTEGER NOT NULL,
                calories_burned INTEGER NOT NULL,
                date TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Tabla de comidas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food TEXT NOT NULL,
                grams INTEGER NOT NULL,
                calories INTEGER NOT NULL,
                proteins REAL NOT NULL,
                carbs REAL NOT NULL,
                fats REAL NOT NULL,
                date TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        
        self.conn.commit()
    
    def get_connection(self):
        """Obtener la conexión a la base de datos"""
        return self.conn
    
    def close(self):
        """Cerrar la conexión a la base de datos"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Context manager para usar 'with'"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cerrar conexión al salir del context manager"""
        self.close()
