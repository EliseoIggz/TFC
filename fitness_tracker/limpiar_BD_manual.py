#!/usr/bin/env python3
"""
Script para limpiar la base de datos del Limen
Permite limpieza parcial (solo registros) o completa (todo)
"""

import sys
import os

# Añadir el directorio actual al path para poder importar desde el directorio raíz
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import Database

def clear_records_only():
    """Limpiar solo registros de comidas y entrenamientos"""
    print("LIMPIEZA PARCIAL - SOLO REGISTROS")
    print("=" * 50)
    
    try:
        db = Database()
        cursor = db.conn.cursor()
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM meals")
        meals_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM trainings")
        trainings_count = cursor.fetchone()[0]
        
        print(f"Registros encontrados:")
        print(f"  Comidas: {meals_count}")
        print(f"  Entrenamientos: {trainings_count}")
        
        if meals_count == 0 and trainings_count == 0:
            print("\nNo hay registros para eliminar")
            return
        
        # Eliminar registros
        print("\nEliminando registros...")
        
        if meals_count > 0:
            cursor.execute("DELETE FROM meals")
            print(f"{meals_count} comidas eliminadas")
        
        if trainings_count > 0:
            cursor.execute("DELETE FROM trainings")
            print(f"{trainings_count} entrenamientos eliminados")
        
        db.conn.commit()
        print("\nRegistros eliminados exitosamente")
        print("Tu perfil de usuario se mantiene intacto")
        
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if 'db' in locals():
            db.close()

def clear_everything():
    """Limpiar TODO incluyendo perfil del usuario"""
    print("LIMPIEZA COMPLETA - TODO")
    print("=" * 50)
    
    try:
        db = Database()
        cursor = db.conn.cursor()
        
        # Contar todo
        cursor.execute("SELECT COUNT(*) FROM meals")
        meals_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM trainings")
        trainings_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM user_profile")
        profile_count = cursor.fetchone()[0]
        
        print(f"Estado actual:")
        print(f"  Comidas: {meals_count}")
        print(f"  Entrenamientos: {trainings_count}")
        print(f"  Perfil de usuario: {profile_count}")
        
        if meals_count == 0 and trainings_count == 0 and profile_count == 0:
            print("\nLa base de datos ya está completamente limpia")
            return
        
        # Confirmar
        print(f"\nEsta acción eliminará TODO:")
        print(f"  - {meals_count} comidas")
        print(f"  - {trainings_count} entrenamientos")
        print(f"  - Perfil del usuario")
        
        confirm = input("\nEscribe 'BORRAR TODO' para confirmar: ").strip().upper()
        
        if confirm != 'BORRAR TODO':
            print("Operación cancelada")
            return
        
        # Eliminar todo
        print("\nEliminando todo...")
        
        if meals_count > 0:
            cursor.execute("DELETE FROM meals")
            print(f"{meals_count} comidas eliminadas")
        
        if trainings_count > 0:
            cursor.execute("DELETE FROM trainings")
            print(f"{trainings_count} entrenamientos eliminados")
        
        if profile_count > 0:
            cursor.execute("DELETE FROM user_profile")
            print("Perfil de usuario eliminado")
        
        db.conn.commit()
        print("\nBase de datos completamente limpiada")
        print("Tendrás que configurar tu perfil desde cero")
        
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if 'db' in locals():
            db.close()

def show_database_status():
    """Mostrar estado actual de la base de datos"""
    print("ESTADO ACTUAL DE LA BASE DE DATOS")
    print("=" * 50)
    
    try:
        db = Database()
        cursor = db.conn.cursor()
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM meals")
        meals_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM trainings")
        trainings_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM user_profile")
        profile_count = cursor.fetchone()[0]
        
        print(f"Comidas registradas: {meals_count}")
        print(f"Entrenamientos registrados: {trainings_count}")
        print(f"Perfil de usuario: {profile_count}")
        
        # Mostrar perfil si existe
        if profile_count > 0:
            cursor.execute("SELECT name, weight, objetivo FROM user_profile WHERE id = 1")
            profile = cursor.fetchone()
            if profile:
                print(f"\nDetalles del perfil:")
                print(f"  Nombre: {profile[0] or 'No establecido'}")
                print(f"  Peso: {profile[1] or 'No establecido'} kg")
                print(f"  Objetivo: {profile[2] or 'No establecido'}")
        
        # Tamaño del archivo
        import config
        if os.path.exists(config.DATABASE_PATH):
            size_bytes = os.path.getsize(config.DATABASE_PATH)
            size_mb = size_bytes / (1024 * 1024)
            print(f"\nTamaño del archivo: {size_mb:.2f} MB")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'db' in locals():
            db.close()

def main_menu():
    """Menú principal"""
    while True:
        print("\n" + "=" * 60)
        print("LIMPIADOR DE BASE DE DATOS - Limen")
        print("=" * 60)
        print("\nOPCIONES DISPONIBLES:")
        print("1. Limpieza PARCIAL (solo comidas + entrenamientos)")
        print("2. Limpieza COMPLETA (todo incluyendo perfil)")
        print("3. Ver estado actual de la base de datos")
        print("4. Salir")
        
        option = input("\nSelecciona una opción (1-4): ").strip()
        
        if option == '1':
            clear_records_only()
        elif option == '2':
            clear_everything()
        elif option == '3':
            show_database_status()
        elif option == '4':
            print("\n¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor selecciona 1, 2, 3 o 4.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main_menu()
