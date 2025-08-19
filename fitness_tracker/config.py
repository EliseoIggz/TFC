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

# Configuración de APIs de Nutrición
# USDA FoodData Central API
USDA_API_KEY = "bf3XJ01Yo9NRD8AvrXse5gOsN4BK4AfGGLEHmXZZ"
USDA_API_BASE_URL = "https://api.nal.usda.gov/fdc/v1"

# OpenAI API para traducción (único servicio de traducción)

# OpenAI API para traducción
OPENAI_API_KEY = "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"
OPENAI_MODEL = "gpt-3.5-turbo"  # Modelo recomendado para traducción