# 🏃‍♂️ Fitness Tracker

**Seguimiento de entrenamientos y nutrición con dashboard web**

Una aplicación Python para registrar y analizar tu actividad física y alimentación. Desarrollada siguiendo el patrón MVC con Streamlit para la interfaz y SQLite para la base de datos.

## ✨ Características

- **📝 Registro de Comidas**: Añade alimentos y obtén información nutricional automática
- **💪 Seguimiento de Entrenamientos**: Registra actividades físicas y calcula calorías quemadas con **base de datos local de 251 deportes**
- **🌍 Soporte Bilingüe**: Interfaz en español e inglés con base de datos local
- **📊 Dashboard Interactivo**: Visualiza tu progreso con gráficas y estadísticas
- **🗄️ Base de Datos Local**: Almacena todos tus datos en SQLite
- **🔌 Base de Datos Local**: 251 deportes y actividades con valores MET precisos
- **📱 Interfaz Web**: Dashboard responsive con Streamlit

## 🆕 Mejoras Recientes

### 🚀 Base de Datos Local de Deportes
- **251 Deportes Disponibles**: Base de datos local completa y verificada
- **Sin Dependencias Externas**: Funciona offline sin conexión a internet
- **Valores MET Precisos**: Cálculos de calorías basados en estudios científicos
- **19 Categorías**: Organización profesional por tipo de deporte

### 🌍 Sistema Bilingüe
- **Español ↔ Inglés**: Soporte completo en ambos idiomas
- **Variantes de Nombres**: Fútbol/Soccer, Tenis/Tennis, etc.
- **Sin Traducción**: Nombres nativos en cada idioma
- **Búsqueda Inteligente**: Encuentra deportes en ambos idiomas

### ⚡ Rendimiento Óptimo
- **Respuesta Instantánea**: Sin latencia de red
- **Sin Límites**: No hay restricciones de peticiones
- **Datos Consistentes**: Información siempre disponible
- **Mantenimiento Fácil**: Código limpio y directo

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd fitness_tracker
   ```

2. **Crear y activar entorno virtual (Recomendado)**
   
   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **Linux/Mac:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   
   **O usar los scripts incluidos:**
   - Windows: `activate_venv.bat`
   - Linux/Mac: `./activate_venv.sh`

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   streamlit run app.py
   ```

5. **Abrir en el navegador**
   - La aplicación se abrirá automáticamente en `http://localhost:8501`

### 🔧 Instalación Rápida (Windows)
```bash
# Opción 1: Script automático (RECOMENDADO)
# Solo hacer doble clic en: run_app.bat

# Opción 2: Manual
activate_venv.bat
streamlit run app.py
```

### 🔧 Instalación Rápida (Linux/Mac)
```bash
# Opción 1: Script automático (RECOMENDADO)
./run_app.sh

# Opción 2: Manual
./activate_venv.sh
streamlit run app.py
```

## 🏃‍♂️ Base de Datos de Deportes

### 📊 Estadísticas
- **Total de deportes**: 251 actividades
- **Categorías**: 19 tipos diferentes
- **Idiomas**: Español + Inglés
- **Niveles de intensidad**: 5 (muy_baja a muy_alta)
- **Rango de METs**: 1.5 - 12.0

### 🗂️ Categorías Principales
- **Deportes de Equipo**: Fútbol, Baloncesto, Tenis, Voleibol
- **Deportes Acuáticos**: Natación, Surf, Remo, Buceo
- **Deportes de Invierno**: Esquí, Snowboard, Patinaje
- **Deportes de Combate**: Boxeo, Karate, MMA, Judo
- **Deportes de Resistencia**: Running, Ciclismo, Triatlón
- **Deportes de Fuerza**: CrossFit, Calistenia, Bodybuilding
- **Deportes de Aventura**: Escalada, Senderismo, Parkour
- **Deportes de Baile**: Zumba, Salsa, Ballet, Hip Hop
- **Deportes de Precisión**: Golf, Tiro con Arco, Billar
- **Actividades Fitness**: Yoga, Pilates, Spinning

### 🔥 Niveles de Intensidad
- **Muy baja**: Ajedrez (1.5), Dardos (2.0), Billar (2.5)
- **Baja**: Yoga (2.5), Golf (3.0), Surf (3.0)
- **Moderada**: Voleibol (4.0), Ciclismo (6.0), Senderismo (6.0)
- **Alta**: Fútbol (8.0), Tenis (7.0), Escalada (8.0)
- **Muy alta**: Boxeo (12.0), MMA (11.0), Parkour Extremo (10.0)

## 📖 Uso de la API de Deportes

### Inicialización
```python
from services.training_api import TrainingAPI

# Crear instancia
api = TrainingAPI()

# Verificar deportes disponibles
total = len(api.sports_database)
print(f"🏃‍♂️ {total} deportes disponibles")
```

### Calcular Calorías
```python
# Deportes en español
calories_futbol = api.get_calories_burned("fútbol", 60, 70)
calories_yoga = api.get_calories_burned("yoga", 45, 65)

# Deportes en inglés
calories_soccer = api.get_calories_burned("soccer", 60, 70)
calories_boxing = api.get_calories_burned("boxing", 30, 80)

# Deportes extremos
calories_parkour = api.get_calories_burned("parkour_extremo", 20, 70)
```

### Funciones Disponibles
```python
# Obtener categorías
categories = api.get_sport_categories()

# Deportes por intensidad
high_intensity = api.get_sports_by_intensity("alta")

# Buscar deportes
results = api.search_sports("cardio")
```

## 📊 Cálculo de Calorías

### Fórmula MET
```
Calorías = MET × Peso (kg) × Tiempo (horas)
```

### Ejemplos de Cálculo
```python
# Fútbol: 60 minutos, peso 70kg
# MET fútbol = 8.0
# Calorías = 8.0 × 70 × 1.0 = 560 kcal

# Yoga: 45 minutos, peso 65kg  
# MET yoga = 2.5
# Calorías = 2.5 × 65 × 0.75 = 122 kcal

# Boxeo: 30 minutos, peso 80kg
# MET boxeo = 12.0
# Calorías = 12.0 × 80 × 0.5 = 480 kcal
```

## 🏗️ Arquitectura del Proyecto

```
fitness_tracker/
├── 📁 controllers/           # Lógica de negocio
│   ├── nutrition_controller.py    # Controlador de nutrición
│   └── training_controller.py     # Controlador de entrenamiento
├── 📁 data/                 # Base de datos y datos
│   └── fitness_tracker.db   # Base de datos SQLite
├── 📁 models/               # Modelos de datos
│   ├── database.py          # Conexión a base de datos
│   ├── nutrition_model.py   # Modelo de nutrición
│   └── training_model.py    # Modelo de entrenamiento
├── 📁 services/             # Servicios y APIs
│   ├── nutrition_api.py     # API de nutrición
│   └── training_api.py      # API de deportes (base local)
├── 📁 views/                # Interfaces de usuario
│   └── dashboard_view.py    # Vista del dashboard
├── 📁 utils/                # Utilidades
│   ├── check_dependencies.py # Verificación de dependencias
│   └── helpers.py           # Funciones auxiliares
├── 📁 tests/                # Pruebas unitarias
├── app.py                   # Aplicación principal
├── config.py                # Configuración
└── requirements.txt         # Dependencias
```

## 🧪 Testing

### Probar la Base de Deportes
```bash
cd fitness_tracker
python test_expanded_sports.py
```

### Probar Funcionalidades
```bash
# Probar cálculo de calorías
python -c "
from services.training_api import TrainingAPI
api = TrainingAPI()
calories = api.get_calories_burned('fútbol', 30, 70)
print(f'Calorías: {calories}')
"
```

## 🌟 Ventajas de la Base Local

### ✅ **Sin Dependencias Externas**
- No requiere conexión a internet
- No hay límites de peticiones
- No hay latencia de red
- No hay costos de APIs

### ✅ **Datos Consistentes**
- 251 deportes verificados
- METs precisos y fiables
- Categorización profesional
- Sin cambios inesperados

### ✅ **Rendimiento Óptimo**
- Respuesta instantánea
- Búsqueda eficiente
- Sin timeouts ni errores de red
- Funciona offline

### ✅ **Cobertura Completa**
- Deportes tradicionales y modernos
- Actividades de fitness y diarias
- Deportes extremos y de aventura
- Soporte bilingüe completo

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

## 📞 Soporte

Si tienes preguntas o necesitas ayuda:
- Revisa la documentación en `README_SPORT_API.md`
- Ejecuta las pruebas incluidas
- Consulta el código fuente para ejemplos

## 📄 Licencia

Este proyecto es de uso educativo y personal.
