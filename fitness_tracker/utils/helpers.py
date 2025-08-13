# Fitness Tracker - Funciones Auxiliares
# ======================================
# Este archivo contiene funciones útiles para el proyecto

from datetime import datetime, date, timedelta

def format_date(date_obj):
    """Formatear fecha en formato legible"""
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
        except ValueError:
            return date_obj
    
    if isinstance(date_obj, date):
        return date_obj.strftime('%d/%m/%Y')
    
    return str(date_obj)

def format_time(minutes):
    """Formatear tiempo en formato legible"""
    if minutes < 60:
        return f"{minutes} min"
    else:
        hours = minutes // 60
        remaining_minutes = minutes % 60
        if remaining_minutes == 0:
            return f"{hours}h"
        else:
            return f"{hours}h {remaining_minutes}min"

def format_calories(calories):
    """Formatear calorías en formato legible"""
    if calories >= 1000:
        return f"{calories/1000:.1f}k cal"
    else:
        return f"{calories} cal"

def format_weight(grams):
    """Formatear peso en formato legible"""
    if grams >= 1000:
        return f"{grams/1000:.1f} kg"
    else:
        return f"{grams} g"

def get_current_date():
    """Obtener fecha actual en formato YYYY-MM-DD"""
    return date.today().strftime('%Y-%m-%d')

def get_date_range(days_back=7):
    """Obtener rango de fechas para los últimos N días"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days_back)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

def validate_positive_number(value, min_value=0, max_value=None):
    """Validar que un número sea positivo y esté en rango"""
    try:
        num = float(value)
        if num < min_value:
            return False, f"El valor debe ser mayor o igual a {min_value}"
        if max_value and num > max_value:
            return False, f"El valor debe ser menor o igual a {max_value}"
        return True, num
    except (ValueError, TypeError):
        return False, "El valor debe ser un número válido"

def truncate_text(text, max_length=50):
    """Truncar texto si es muy largo"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def calculate_percentage(part, total):
    """Calcular porcentaje"""
    if total == 0:
        return 0
    return round((part / total) * 100, 1)
