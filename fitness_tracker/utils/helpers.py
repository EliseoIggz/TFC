#!/usr/bin/env python3
"""
Utilidades y funciones auxiliares para el proyecto
"""

import streamlit as st
from datetime import datetime, date, timedelta

def format_date(date_obj):
    """Formatear fecha para mostrar"""
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
        except ValueError:
            return date_obj
    
    if isinstance(date_obj, date):
        return date_obj.strftime('%d/%m/%Y')
    return str(date_obj)

def format_date_display(date_obj):
    """Formatear fecha para mostrar de forma amigable"""
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
        except ValueError:
            return date_obj
    
    if isinstance(date_obj, date):
        today = date.today()
        if date_obj == today:
            return "hoy"
        elif date_obj == today.replace(day=today.day - 1):
            return "ayer"
        elif date_obj == today.replace(day=today.day + 1):
            return "mañana"
        else:
            return date_obj.strftime('%d/%m/%Y')
    return str(date_obj)

def show_success_message(message: str):
    """
    Mostrar mensaje de éxito de forma simple
    
    Args:
        message: Mensaje a mostrar
    """
    st.success(message)

def format_time(minutes):
    """Formatear tiempo en formato legible"""
    if minutes is None or minutes <= 0:
        return "0 min"
    
    if minutes < 60:
        return f"{int(minutes)} min"
    
    hours = int(minutes // 60)
    remaining_minutes = int(minutes % 60)
    
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
    """Calcular porcentaje con manejo de división por cero"""
    if total == 0:
        return 0
    return round((part / total) * 100, 1)
