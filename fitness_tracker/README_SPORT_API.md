# Fitness Tracker - TrainingAPI (API de Entrenamiento)
# ===================================================
# Documentación para la API de entrenamiento y cálculo de calorías

## Descripción

Esta implementación reemplaza la API mock anterior con una **API real** que obtiene datos de ejercicios deportivos desde **ExerciseDB**, una base de datos gratuita y completa de ejercicios.

## ✨ Características Principales

### 🔥 Cálculo Real de Calorías
- **Fórmula MET**: Usa valores MET (Metabolic Equivalent of Task) reales
- **Personalización**: Considera peso del usuario para cálculos precisos
- **Variabilidad**: Incluye variación natural en el gasto calórico

### 📚 Base de Datos Completa
- **1300+ ejercicios** con información detallada
- **Partes del cuerpo** trabajadas
- **Equipamiento** necesario
- **Instrucciones** paso a paso
- **GIFs animados** de los ejercicios

### 🎯 Funcionalidades Avanzadas
- Búsqueda inteligente de ejercicios
- Filtrado por parte del cuerpo
- Filtrado por equipamiento
- Sugerencias contextuales
- Fallback a datos locales si la API falla

## 🚀 Configuración

### 1. Obtener API Key Gratuita

1. Ve a [ExerciseDB en RapidAPI](https://rapidapi.com/justin-WFnsXH_t6/api/exercisedb)
2. Regístrate gratuitamente
3. Suscríbete al plan gratuito (1000 requests/mes)
4. Copia tu API key

### 2. Configurar en `config.py`

```python
# Configuración de APIs reales
EXERCISE_DB_API_KEY = "tu_api_key_aqui"  # Reemplaza con tu key real
EXERCISE_DB_API_HOST = "exercisedb.p.rapidapi.com"
```

### 3. Instalar Dependencias

```bash
pip install requests
```

## 📖 Uso Básico

### Inicialización
```python
from services.training_api import TrainingAPI

# Crear instancia de la API
training_api = TrainingAPI()

# Verificar si está usando API real
if training_api.use_real_api:
    print("✅ Usando API real")
else:
    print("⚠️ Usando datos locales")
```

### Calcular Calorías
```python
# Calcular calorías quemadas
calories = training_api.get_calories_burned("running", 30, 75.0)
print(f"Calorías quemadas: {calories}")

# Parámetros:
# - activity: nombre del ejercicio
# - minutes: duración en minutos
# - weight: peso en kg (opcional, por defecto 70.0)
```

### Obtener Sugerencias
```python
# Buscar ejercicios
suggestions = training_api.get_activity_suggestions("cardio")
print(f"Sugerencias: {suggestions}")
```

### Detalles del Ejercicio
```python
# Obtener información completa
details = training_api.get_exercise_details("push-up")
if details:
    print(f"Nombre: {details['name']}")
    print(f"Parte del cuerpo: {details['bodyPart']}")
    print(f"Equipamiento: {details['equipment']}")
    print(f"GIF: {details['gifUrl']}")
```

## 🔍 Funciones Disponibles

| Función | Descripción | Parámetros |
|---------|-------------|------------|
| `get_calories_burned()` | Calcula calorías quemadas | `activity`, `minutes`, `weight` |
| `get_activity_suggestions()` | Sugiere ejercicios | `query` |
| `get_activity_intensity()` | Obtiene intensidad | `activity` |
| `get_exercise_details()` | Detalles completos | `exercise_name` |
| `get_exercises_by_body_part()` | Ejercicios por parte del cuerpo | `body_part` |
| `get_exercises_by_equipment()` | Ejercicios por equipamiento | `equipment` |

## 📊 Cálculo de Calorías

### Fórmula MET
```
Calorías = MET × Peso (kg) × Tiempo (horas)
```

### Valores MET por Categoría
- **Cardio**: 8.0 MET
- **Fuerza**: 6.0 MET  
- **Flexibilidad**: 3.0 MET
- **Partes específicas**: 6.0 MET

### Ejemplo
```python
# Correr 30 minutos, peso 75kg
# MET running ≈ 8.0
# Calorías = 8.0 × 75 × 0.5 = 300 kcal
```

## 🛡️ Sistema de Fallback

La API está diseñada para ser **robusta**:

1. **Intenta usar API real** primero
2. **Si falla**, usa base de datos local
3. **Si no encuentra actividad**, genera valores realistas
4. **Manejo de errores** completo

## 📱 Integración con la App

### En el Controlador de Entrenamiento
```python
# El controlador existente seguirá funcionando
# Solo necesitas configurar la API key
```

### Nuevas Funcionalidades Disponibles
- Búsqueda avanzada de ejercicios
- Información detallada de cada ejercicio
- Cálculos más precisos de calorías
- Sugerencias inteligentes

## 🧪 Testing

Ejecuta el ejemplo incluido:

```bash
cd fitness_tracker
python examples/training_api_usage.py
```

## 📊 Límites de la API Gratuita

- **ExerciseDB**: 1000 requests/mes
- **Rate limiting**: 100 requests/día
- **Timeout**: 10 segundos por request

## 🔧 Personalización

### Añadir Nuevos Valores MET
```python
# En config.py
MET_VALUES = {
    'tu_actividad': 7.0,
    # ... otros valores
}
```

### Modificar Base de Datos Local
```python
# En training_api.py, editar self.local_activity_database
```