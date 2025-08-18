# Fitness Tracker - Configuración general
# ======================================
# Este archivo contiene configuraciones básicas de la aplicación

# Configuración de la base de datos
DATABASE_NAME = "fitness_tracker.db"
DATABASE_PATH = f"./data/{DATABASE_NAME}"

# Configuración de la aplicación
APP_NAME = "Fitness Tracker"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Eliseo"

# Configuración de Streamlit
STREAMLIT_TITLE = "Fitness Tracker - Seguimiento de Entrenamientos y Nutrición"
STREAMLIT_LAYOUT = "wide"
STREAMLIT_SIDEBAR_STATE = "expanded"

# Configuración de gráficas
CHART_HEIGHT = 400
CHART_WIDTH = 800

# Configuración de paginación
ITEMS_PER_PAGE = 10

# Configuración de APIs mock
MOCK_API_DELAY = 0.1  # Simular delay de API real

# Configuración de APIs reales
# ExerciseDB API - Base gratuita de ejercicios deportivos
# Registro: https://rapidapi.com/justin-WFnsXH_t6/api/exercisedb
EXERCISE_DB_API_KEY = "bf70a288f1msheaea4dc6b6fe11cp185ca9jsn4c3f1c8661c5"  # API key configurada
EXERCISE_DB_API_HOST = "exercisedb.p.rapidapi.com"

# Open Food Facts API - Base gratuita de información nutricional
# Documentación: https://world.openfoodfacts.org/data
OPENFOODFACTS_API_URL = "https://world.openfoodfacts.org/cgi/search.pl"
OPENFOODFACTS_API_TIMEOUT = 10  # Timeout en segundos

# Configuración de cálculo de calorías
DEFAULT_WEIGHT = 70.0  # Peso por defecto en kg para cálculos
MET_VALUES = {
    'cardio': 8.0,
    'strength': 6.0,
    'flexibility': 3.0,
    'chest': 6.0,
    'back': 6.0,
    'shoulders': 6.0,
    'upper arms': 6.0,
    'lower arms': 6.0,
    'upper legs': 6.0,
    'lower legs': 6.0,
    'waist': 6.0
} 