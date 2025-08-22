# Documentación Técnica - Limen Fitness Tracker

## Descripción General
Limen es una aplicación de seguimiento de fitness desarrollada en Python que combina nutrición y entrenamiento en un dashboard web interactivo. La aplicación sigue el patrón arquitectónico MVC (Model-View-Controller) y utiliza Streamlit para la interfaz de usuario.

## Arquitectura del Sistema

### Patrón MVC Implementado
- **Models**: Manejo de datos y persistencia en SQLite
- **Views**: Interfaz de usuario con Streamlit
- **Controllers**: Lógica de negocio y coordinación entre modelos y vistas

### Estructura de Directorios
```
fitness_tracker/
├── controllers/           # Lógica de negocio
├── models/               # Persistencia de datos
├── services/             # Servicios externos y APIs
├── views/                # Interfaces de usuario
├── utils/                # Utilidades y helpers
├── tests/                # Pruebas unitarias
└── data/                 # Base de datos SQLite
```

## Documentación de Funciones y Métodos

### 1. CONTROLADORES (Controllers)

#### TrainingController
**Propósito**: Maneja toda la lógica relacionada con entrenamientos y deportes.

**Métodos principales**:
- `add_training(activity, minutes, user_weight)`: Añade un nuevo entrenamiento a la base de datos
- `validate_training_form(minutes_input, selected_sport)`: Valida los datos del formulario de entrenamiento
- `get_training_preview(selected_sport, minutes, user_weight)`: Obtiene vista previa del entrenamiento con calorías estimadas
- `get_training_form_viewmodel(minutes_input, selected_sport, user_weight)`: Genera ViewModel completo para el formulario
- `get_training_form_submission_result(selected_sport, minutes, user_weight)`: Procesa el envío del formulario
- `get_training_stats_viewmodel(date_str)`: Genera ViewModel para estadísticas de entrenamiento
- `get_trainings_table_viewmodel(trainings_result, selected_date)`: Prepara datos para tabla de entrenamientos
- `delete_training_with_feedback(training_id)`: Elimina entrenamiento con feedback completo

#### NutritionController
**Propósito**: Maneja la lógica de nutrición y comidas.

**Métodos principales**:
- `add_meal(food, grams)`: Añade una nueva comida a la base de datos
- `add_meal_from_selection(options_data, selected_index)`: Añade comida desde opción seleccionada
- `get_meal_form_submission_result(food, grams)`: Procesa envío del formulario de comida
- `get_food_selector_viewmodel(options_data)`: Genera ViewModel para selector de alimentos
- `get_food_selection_result(options_data, selected_index)`: Procesa selección de alimento
- `get_nutrition_stats_viewmodel(date_str)`: Genera ViewModel para estadísticas nutricionales
- `get_meals_table_viewmodel(meals_result, selected_date)`: Prepara datos para tabla de comidas
- `get_calories_balance(date_str)`: Calcula balance calórico del día
- `get_macro_recommendations_viewmodel(objetivo)`: Genera recomendaciones de macronutrientes

#### UserController
**Propósito**: Maneja el perfil del usuario y configuraciones personales.

**Métodos principales**:
- `get_profile()`: Obtiene el perfil actual del usuario
- `save_profile(name, weight, objetivo)`: Guarda o actualiza el perfil del usuario
- `validate_profile_input(name, weight)`: Valida los datos de entrada del perfil
- `get_profile_display_data(profile)`: Prepara datos del perfil para mostrar en la vista
- `get_objetivo_options()`: Obtiene opciones de objetivo formateadas

#### DashboardController
**Propósito**: Maneja la lógica del dashboard y formularios.

**Métodos principales**:
- `get_training_form_state()`: Obtiene estado actual del formulario de entrenamiento
- `reset_training_form()`: Resetea el formulario de entrenamiento incrementando el counter
- `validate_form_inputs(selected_sport, minutes_input)`: Valida inputs del formulario
- `get_form_validation_status(validation_data)`: Procesa estado de validación del formulario
- `init_user_profile(user_controller)`: Inicializa perfil de usuario
- `get_sport_selector_data(sports_data, selected_category)`: Obtiene datos del selector de deportes
- `set_training_toast(message)`: Guarda mensaje para toast de entrenamiento
- `get_training_toast()`: Obtiene y limpia toast de entrenamiento

### 2. SERVICIOS (Services)

#### TrainingService
**Propósito**: Calcula calorías quemadas y maneja la base de datos de deportes.

**Métodos principales**:
- `get_calories_burned(activity, minutes, weight)`: Calcula calorías quemadas usando valores MET
- `validate_training_input(minutes_input, selected_sport)`: Valida input de entrenamiento
- `get_training_preview(selected_sport, minutes, user_weight)`: Obtiene vista previa del entrenamiento
- `search_sports(query)`: Busca deportes por consulta
- `get_sport_categories()`: Obtiene deportes organizados por categorías
- `get_all_sports()`: Obtiene todos los deportes disponibles

**Base de datos de deportes**:
- 135 deportes y actividades físicas
- 19 categorías organizadas profesionalmente
- Valores MET precisos basados en estudios científicos

#### NutritionService
**Propósito**: Integra con la API de USDA para obtener información nutricional.

**Métodos principales**:
- `search_foods(query, page_size)`: Busca alimentos en la base de datos USDA
- `get_nutrition_info(food, grams)`: Obtiene información nutricional completa
- `get_nutrition_from_selected_option(options_data, selected_index)`: Obtiene nutrición de opción seleccionada
- `_make_api_request(endpoint, params)`: Realiza peticiones a la API de USDA

**Características**:
- Búsqueda híbrida (Foundation + Legacy)
- Traducción automática español-inglés y vicerversa
- Manejo de múltiples opciones de alimentos

#### TranslationService
**Propósito**: Proporciona traducción automática usando Api de OpenAI.

**Métodos principales**:
- `translate_to_english(spanish_text)`: Traduce texto del español al inglés
- `translate_to_spanish(english_text)`: Traduce texto del inglés al español
- `is_available()`: Verifica si el servicio está disponible

### 3. MODELOS (Models)

#### Database
**Propósito**: Maneja la conexión y estructura de la base de datos SQLite.

**Métodos principales**:
- `__init__()`: Inicializa conexión y crea tablas
- `create_tables()`: Crea las tablas necesarias
- `get_connection()`: Obtiene la conexión a la base de datos
- `close()`: Cierra la conexión

**Tablas creadas**:
- `trainings`: Entrenamientos registrados
- `meals`: Comidas registradas
- `user_profile`: Perfil del usuario

#### TrainingModel
**Propósito**: Maneja operaciones CRUD para entrenamientos.

**Métodos principales**:
- `add_training(activity, minutes, calories_burned)`: Añade entrenamiento
- `get_trainings_by_date(date)`: Obtiene entrenamientos por fecha
- `get_total_calories_burned(date)`: Calcula total de calorías quemadas
- `get_total_minutes(date)`: Calcula total de minutos activos
- `delete_training(training_id)`: Elimina entrenamiento

#### NutritionModel
**Propósito**: Maneja operaciones CRUD para comidas.

**Métodos principales**:
- `add_meal(food, grams, calories, proteins, carbs, fats)`: Añade comida
- `get_meals_by_date(date)`: Obtiene comidas por fecha
- `get_total_calories_consumed(date)`: Calcula total de calorías consumidas
- `get_macro_totals(date)`: Calcula totales de macronutrientes

#### UserModel
**Propósito**: Maneja el perfil del usuario.

**Métodos principales**:
- `get_profile()`: Obtiene perfil actual
- `upsert_profile(name, weight, objetivo)`: Guarda o actualiza perfil

### 4. VISTAS (Views)

#### DashboardView
**Propósito**: Interfaz principal de usuario con Streamlit.

**Métodos principales**:
- `render()`: Renderiza el dashboard completo
- `_render_header()`: Renderiza cabecera con datos del usuario
- `_render_profile_form()`: Renderiza formulario de perfil
- `_render_input_forms()`: Renderiza formularios de entrada
- `_render_training_form()`: Renderiza formulario de entrenamiento
- `_render_meal_form()`: Renderiza formulario de comida
- `_render_main_content()`: Renderiza contenido principal
- `_render_calories_chart()`: Renderiza gráfica de calorías
- `_render_macros_chart()`: Renderiza gráfica de macronutrientes

### 5. UTILIDADES (Utils)

#### Helpers
**Propósito**: Funciones auxiliares para formateo y validación.

**Funciones principales**:
- `format_date(date_obj)`: Formatea fecha en formato legible
- `format_date_display(date_obj)`: Formatea fecha para mostrar
- `format_time(minutes)`: Formatea tiempo en formato legible
- `format_calories(calories)`: Formatea calorías en formato legible
- `format_weight(grams)`: Formatea peso en formato legible
- `get_current_date()`: Obtiene fecha actual en formato YYYY-MM-DD
- `validate_positive_number(value, min_value, max_value)`: Valida número positivo
- `calculate_percentage(part, total)`: Calcula porcentaje

#### CheckDependencies
**Propósito**: Verifica que todas las dependencias estén instaladas.

**Funciones principales**:
- `check_dependencies()`: Verifica estado de dependencias
- `install_missing_dependencies()`: Instala dependencias faltantes
- `get_dependency_status()`: Obtiene estado completo de dependencias

## Flujos de Datos Principales

### 1. Registro de Entrenamiento
1. Usuario selecciona deporte y especifica minutos
2. `TrainingController.validate_training_form()` valida datos
3. `TrainingService.get_calories_burned()` calcula calorías
4. `TrainingModel.add_training()` guarda en base de datos
5. Vista muestra confirmación y actualiza estadísticas

### 2. Registro de Comida
1. Usuario escribe nombre del alimento
2. `NutritionService.search_foods()` busca en API USDA
3. Si hay múltiples opciones, se muestran para selección
4. `NutritionModel.add_meal()` guarda en base de datos
5. Vista muestra confirmación y actualiza estadísticas

### 3. Actualización de Perfil
1. Usuario modifica nombre o peso
2. `UserController.validate_profile_input()` valida datos
3. `UserModel.upsert_profile()` guarda cambios
4. Vista actualiza automáticamente y muestra confirmación

## Configuración y Dependencias

### Dependencias Principales
- **Streamlit**: Framework web para el dashboard
- **Plotly**: Gráficas interactivas y visualizaciones
- **Pandas**: Manipulación y análisis de datos
- **Requests**: Peticiones HTTP para APIs externas
- **OpenAI**: API para traducción automática

### APIs Externas
- **USDA FoodData Central**: Base de datos nutricional oficial
- **OpenAI GPT**: Servicio de traducción automática

### Configuración
- **Base de datos**: SQLite local
- **Puerto**: Streamlit por defecto (8501)
- **Layout**: Wide (pantalla completa)
- **Sidebar**: Expandido por defecto

## Consideraciones de Rendimiento

### Optimizaciones Implementadas
- Búsqueda híbrida en USDA (Foundation + Legacy)
- Base de datos local para deportes (sin latencia de red)
- Caching de resultados de búsqueda
- Validaciones en frontend para reducir peticiones

### Límites de API
- **USDA**: 10,000 peticiones/día con API key
- **OpenAI**: Según plan de suscripción

## Testing

### Archivos de Prueba
- `test_training.py`: Pruebas del sistema de entrenamiento
- `test_nutrition_complete.py`: Pruebas completas del sistema de nutrición
- `test_usda_nutrition.py`: Pruebas de integración con USDA
- `test_openai_integration.py`: Pruebas del servicio de traducción
- `test_expanded_sports.py`: Pruebas de la base de datos de deportes

### Ejecución de Pruebas
```bash
cd fitness_tracker
python -m pytest tests/
```

## Mantenimiento y Escalabilidad

### Agregar Nuevos Deportes
```python
# En services/training.py
'nombre_deporte': {
    'name': 'Nombre del Deporte',
    'met': 7.0,  # Valor MET del deporte
    'category': 'categoria_deporte'
}
```

### Modificar Configuración
- **config.py**: Configuraciones generales de la aplicación
- **requirements.txt**: Dependencias del proyecto
- **.env**: Variables de entorno (crear si es necesario)

### Estructura para Escalabilidad
- Arquitectura MVC permite migración a servidor web
- Separación clara de responsabilidades
- ViewModels preparan datos para diferentes tipos de vistas
- Servicios pueden ser reemplazados por implementaciones alternativas
