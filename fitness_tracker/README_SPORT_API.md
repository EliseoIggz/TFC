# 🏃‍♂️ Fitness Tracker - API de Deportes Local

## 📋 Descripción

**Fitness Tracker** es una aplicación que calcula calorías quemadas en actividades deportivas utilizando una **base de datos local completa** con 251 deportes y actividades diferentes.

## ✨ Características

- **🏃‍♂️ 251 deportes y actividades** disponibles
- **🌍 Soporte bilingüe** (Español + Inglés)
- **🏷️ 19 categorías** de deportes organizadas
- **🔥 5 niveles de intensidad** (muy_baja a muy_alta)
- **💪 Cálculo preciso** basado en valores MET reales
- **🚀 Sin dependencias externas** - 100% local
- **⚡ Respuesta instantánea** sin latencia de red

## 🗂️ Categorías de Deportes

| Categoría | Deportes | Ejemplos |
|-----------|----------|----------|
| **Deportes de Equipo** | 13 | Fútbol, Baloncesto, Tenis, Voleibol |
| **Deportes Acuáticos** | 16 | Natación, Surf, Remo, Buceo |
| **Deportes de Invierno** | 16 | Esquí, Snowboard, Patinaje |
| **Deportes de Combate** | 15 | Boxeo, Karate, MMA, Judo |
| **Deportes de Resistencia** | 19 | Running, Ciclismo, Triatlón |
| **Deportes de Fuerza** | 10 | CrossFit, Calistenia, Bodybuilding |
| **Deportes de Aventura** | 18 | Escalada, Senderismo, Parkour |
| **Deportes de Baile** | 15 | Zumba, Salsa, Ballet, Hip Hop |
| **Deportes de Precisión** | 14 | Golf, Tiro con Arco, Billar |
| **Actividades Fitness** | 15 | Yoga, Pilates, Spinning |
| **Ejercicios Específicos** | 23 | Sentadillas, Flexiones, Burpees |
| **Actividades Diarias** | 26 | Caminar, Limpiar, Jardinería |
| **Deportes Extremos** | 8 | Paracaidismo, Escalada Libre |
| **Deportes Motorizados** | 5 | Motocross, Karting, Rally |
| **Deportes de Mesa** | 7 | Ajedrez, Póker, Dardos |
| **Deportes Tradicionales** | 7 | Pelota Vasca, Lucha Canaria |
| **Deportes Acuáticos Extremos** | 10 | Kitesurf, Windsurf, Wakeboard |
| **Deportes de Invierno Extremos** | 8 | Esquí Extremo, Freestyle |

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd fitness_tracker
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. ¡Listo! No se requieren APIs externas

## 📖 Uso Básico

### Inicialización
```python
from services.training_api import TrainingAPI

# Crear instancia de la API
training_api = TrainingAPI()

# Verificar deportes disponibles
total_sports = len(training_api.sports_database)
print(f"🏃‍♂️ {total_sports} deportes disponibles")
```

### Calcular Calorías
```python
# Calcular calorías quemadas
calories = training_api.get_calories_burned("running", 30, 75.0)
print(f"Calorías quemadas: {calories}")

# Parámetros:
# - activity: nombre del deporte (español o inglés)
# - minutes: duración en minutos
# - weight: peso en kg (opcional, por defecto 70.0)
```

### Ejemplos de Uso
```python
# Deportes en español
calories_futbol = training_api.get_calories_burned("fútbol", 60, 70)
calories_yoga = training_api.get_calories_burned("yoga", 45, 65)

# Deportes en inglés
calories_soccer = training_api.get_calories_burned("soccer", 60, 70)
calories_boxing = training_api.get_calories_burned("boxing", 30, 80)

# Deportes extremos
calories_parkour = training_api.get_calories_burned("parkour_extremo", 20, 70)
calories_escalada = training_api.get_calories_burned("escalada_libre", 45, 75)
```

## 🔍 Funciones Disponibles

| Función | Descripción | Parámetros |
|---------|-------------|------------|
| `get_calories_burned()` | Calcula calorías quemadas | `activity`, `minutes`, `weight` |
| `get_sport_categories()` | Obtiene todas las categorías | - |
| `get_sports_by_intensity()` | Deportes por intensidad | `intensity` |
| `search_sports()` | Busca deportes por consulta | `query` |

## 📊 Cálculo de Calorías

### Fórmula MET
```
Calorías = MET × Peso (kg) × Tiempo (horas)
```

### Valores MET por Intensidad
- **Muy baja**: 1.5-2.5 MET (Ajedrez, Billar)
- **Baja**: 2.5-4.0 MET (Yoga, Golf, Surf)
- **Moderada**: 4.0-6.0 MET (Voleibol, Ciclismo)
- **Alta**: 6.0-9.0 MET (Fútbol, Tenis, Escalada)
- **Muy alta**: 9.0-12.0 MET (Boxeo, MMA, Parkour Extremo)

### Ejemplos de Cálculo
```python
# Fútbol: 30 minutos, peso 70kg
# MET fútbol = 8.0
# Calorías = 8.0 × 70 × 0.5 = 280 kcal

# Yoga: 45 minutos, peso 65kg  
# MET yoga = 2.5
# Calorías = 2.5 × 65 × 0.75 = 122 kcal

# Boxeo: 20 minutos, peso 80kg
# MET boxeo = 12.0
# Calorías = 12.0 × 80 × 0.33 = 320 kcal
```

## 🌍 Soporte Bilingüe

La base de datos incluye **variantes en español e inglés**:

| Español | Inglés | MET | Intensidad |
|---------|--------|-----|------------|
| Fútbol | Soccer | 8.0 | Alta |
| Baloncesto | Basketball | 8.0 | Alta |
| Tenis | Tennis | 7.0 | Alta |
| Natación | Swimming | 7.0 | Alta |
| Ciclismo | Cycling | 6.0 | Moderada |
| Yoga | Yoga | 2.5 | Baja |

## 🏆 Ventajas de la Base Local

### ✅ **Sin Dependencias Externas**
- No requiere conexión a internet
- No hay límites de peticiones
- No hay latencia de red

### ✅ **Datos Consistentes**
- 251 deportes verificados
- METs precisos y fiables
- Categorización profesional

### ✅ **Rendimiento Óptimo**
- Respuesta instantánea
- Búsqueda eficiente
- Sin timeouts ni errores de red

### ✅ **Cobertura Completa**
- Deportes tradicionales y modernos
- Actividades de fitness y diarias
- Deportes extremos y de aventura

## 🎯 Casos de Uso

### 🏋️‍♂️ **Gimnasios y Centros Deportivos**
- Cálculo de calorías para clientes
- Planificación de entrenamientos
- Seguimiento de progreso

### 🏃‍♀️ **Entrenadores Personales**
- Programas de ejercicios personalizados
- Estimación de gasto calórico
- Recomendaciones de intensidad

### 📱 **Aplicaciones de Fitness**
- Integración en apps móviles
- Widgets de calorías
- Historial de actividades

### 🏫 **Educación Física**
- Programas escolares
- Evaluación de actividades
- Concienciación sobre ejercicio

## 🔧 Personalización

### Agregar Nuevos Deportes
```python
# En training_api.py, agregar a sports_database
'nombre_deporte': {
    'name': 'Nombre del Deporte',
    'met': 7.0,  # Valor MET del deporte
    'category': 'categoria_deporte',
    'intensity': 'moderada'  # muy_baja, baja, moderada, alta, muy_alta
}
```

### Modificar Valores MET
```python
# Cambiar el valor MET de un deporte existente
self.sports_database['futbol']['met'] = 8.5  # Ajustar según estudios
```

## 📈 Estadísticas de la Base de Datos

- **Total de deportes**: 251
- **Categorías**: 19
- **Idiomas**: 2 (Español + Inglés)
- **Niveles de intensidad**: 5
- **Rango de METs**: 1.5 - 12.0
- **Deportes más intensos**: Boxeo (12.0), MMA (11.0), Parkour Extremo (10.0)
- **Deportes menos intensos**: Ajedrez (1.5), Dardos (2.0), Billar (2.5)

## 🎉 Conclusión

**Fitness Tracker** demuestra que una **base de datos local bien diseñada** puede ser **más efectiva** que depender de APIs externas:

- ✅ **Sin costos** de APIs
- ✅ **Sin límites** de peticiones  
- ✅ **Sin problemas** de conectividad
- ✅ **Con datos** verificados y precisos
- ✅ **Con cobertura** completa de deportes

¡Perfecto para demostrar dominio de **estructuras de datos locales** y **cálculos precisos** en tu trabajo! 🚀