# Fitness Tracker

**Seguimiento de entrenamientos y nutrición con dashboard web**

Una aplicación Python completa para registrar y analizar tu actividad física y alimentación. Desarrollada siguiendo el patrón MVC con Streamlit para la interfaz y SQLite para la base de datos local.

## Características Principales

- **Registro de Comidas**: Añade alimentos y obtén información nutricional automática desde la base de datos oficial del USDA
- **Seguimiento de Entrenamientos**: Registra actividades físicas y calcula calorías quemadas con base de datos local de 251 deportes
- **Traducción Automática**: Búsqueda de alimentos en español con traducción automática a inglés para la API del USDA
- **Dashboard Interactivo**: Visualiza tu progreso con gráficas y estadísticas en tiempo real
- **Base de Datos Local**: Almacena todos tus datos en SQLite sin dependencias externas
- **Interfaz Web**: Dashboard responsive con Streamlit

## Sistema de Nutrición

### USDA FoodData Central
- Base de datos oficial del gobierno de Estados Unidos
- Más de 300,000 alimentos con información nutricional precisa
- Datos verificados y actualizados regularmente
- Información detallada: macronutrientes, vitaminas, minerales

### Traducción Automática
- Traducción español-inglés automática usando OpenAI
- Detección inteligente del idioma de entrada
- Búsqueda bilingüe transparente para el usuario
- Servicio premium con alta precisión y confiabilidad

### Cómo Funciona
1. El usuario escribe el nombre del alimento en español
2. El sistema detecta el idioma y traduce automáticamente a inglés
3. Se busca en la base de datos oficial del USDA
4. Los resultados se traducen de vuelta al español
5. El usuario selecciona la opción específica y se registra


## Sistema de Deportes

### Base de Datos Local
- **251 deportes y actividades** disponibles sin conexión a internet
- **19 categorías** organizadas profesionalmente
- **Valores MET precisos** basados en estudios científicos

### Categorías Principales
- Deportes de Equipo, Acuáticos, Invierno, Combate
- Deportes de Resistencia, Fuerza, Aventura, Baile
- Deportes de Precisión, Actividades Fitness y más




## Instalación

Ver archivo `instrucciones.md` para pasos detallados de instalación y ejecución.

## Uso de la Aplicación

### Dashboard Principal
- **Perfil del Usuario**: Configura tu nombre y peso para cálculos personalizados
- **Registro de Comidas**: Busca alimentos y añade comidas con información nutricional completa
- **Registro de Entrenamientos**: Selecciona deportes de la base de datos y registra tu actividad
- **Estadísticas**: Visualiza tu balance calórico, macronutrientes y actividad física

### Búsqueda de Alimentos
1. Escribe el nombre del alimento en español o inglés
2. El sistema traduce automáticamente y busca en la base de datos del USDA
3. Selecciona la opción específica de la lista de resultados
4. Especifica la cantidad en gramos
5. La comida se registra automáticamente con toda la información nutricional

### Registro de Entrenamientos
1. Selecciona la categoría de deporte
2. Elige el deporte específico de la lista
3. Especifica la duración en minutos
4. El sistema calcula automáticamente las calorías quemadas basándose en tu peso
5. El entrenamiento se registra en tu historial

## Arquitectura del Proyecto

```
fitness_tracker/
├── controllers/           # Lógica de negocio
│   ├── nutrition_controller.py    # Controlador de nutrición
│   ├── training_controller.py     # Controlador de entrenamiento
│   └── user_controller.py         # Controlador de usuario
├── data/                 # Base de datos
│   └── fitness_tracker.db   # Base de datos SQLite
├── models/               # Modelos de datos
│   ├── database.py          # Conexión a base de datos
│   ├── nutrition_model.py   # Modelo de nutrición
│   ├── training_model.py    # Modelo de entrenamiento
│   └── user_model.py        # Modelo de usuario
├── services/             # Servicios y APIs
│   ├── nutrition_api.py     # API de nutrición USDA
│   ├── openai_translation_service.py # Servicio de traducción OpenAI
│   └── training.py          # Servicio de deportes (base local)
├── views/                # Interfaces de usuario
│   └── dashboard_view.py    # Vista del dashboard
├── utils/                # Utilidades
│   ├── check_dependencies.py # Verificación de dependencias
│   └── helpers.py           # Funciones auxiliares
├── tests/                # Pruebas unitarias
├── app.py                   # Aplicación principal
├── config.py                # Configuración
└── requirements.txt         # Dependencias
```

## Rendimiento del Sistema

- Funciona offline para funcionalidades básicas
- Búsqueda eficiente en bases de datos locales
- Código limpio y mantenible

## Casos de Uso

### Uso Actual (Entorno Local)
- **Seguimiento personal**: Registro individual de comidas y entrenamientos
- **Dashboard privado**: Visualización de progreso personal
- **Base de datos local**: Almacenamiento en SQLite del usuario

### Escalabilidad Futura
El sistema está diseñado para poder escalar a un entorno de producción:

- **Despliegue en servidor**: La arquitectura MVC permite migrar a un servidor web
- **Base de datos multi-usuario**: Cambiar SQLite por PostgreSQL o MySQL
- **Sistema de autenticación**: Implementar login y gestión de usuarios
- **API REST**: Exponer funcionalidades como servicio web
- **Aplicación web**: Acceso desde cualquier dispositivo con navegador
- **Aplicación móvil**: Crear apps nativas usando la API del servidor

### Aplicaciones Potenciales
- **Gimnasios**: Seguimiento de clientes y planificación de entrenamientos
- **Entrenadores personales**: Gestión de múltiples clientes
- **Centros deportivos**: Control de actividades y estadísticas
- **Aplicaciones de fitness**: Integración con wearables y apps móviles

## Personalización

### Agregar Nuevos Deportes
```python
# En services/training.py, agregar a sports_database
'nombre_deporte': {
    'name': 'Nombre del Deporte',
    'met': 7.0,  # Valor MET del deporte
    'category': 'categoria_deporte'
}
```

### Modificar Valores MET
```python
# Cambiar el valor MET de un deporte existente
self.sports_database['futbol']['met'] = 8.5
```

## Testing

### Probar la Base de Deportes
```bash
cd fitness_tracker
python tests/test_expanded_sports.py
```

### Probar el Sistema de Nutrición
```bash
python tests/test_usda_nutrition.py
```

### Probar Funcionalidades Básicas
```python
# Probar cálculo de calorías
from services.training import Training
api = Training()
calories = api.get_calories_burned('fútbol', 30, 70)
print(f'Calorías: {calories}')
```

## Consideraciones Importantes

### Límites de las APIs
- **USDA sin API Key**: 3,600 peticiones por día
- **USDA con API Key**: 10,000 peticiones por día
- **OpenAI**: Límites según tu plan de suscripción

### Dependencias de Internet
- **USDA API**: Requiere conexión a internet
- **OpenAI**: Requiere conexión a internet
- **Sistema offline**: Funciona para datos ya cargados y cálculos de deportes

## Estadísticas del Sistema

- **Total de deportes**: 251 actividades
- **Categorías de deportes**: 19 tipos diferentes
- **Alimentos disponibles**: 300,000+ en base de datos USDA
- **Rango de METs**: 1.5 - 12.0
