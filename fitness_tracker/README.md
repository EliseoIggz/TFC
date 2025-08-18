# 🏃‍♂️ Fitness Tracker

**Seguimiento de entrenamientos y nutrición con dashboard web**

Una aplicación Python para registrar y analizar tu actividad física y alimentación. Desarrollada siguiendo el patrón MVC con Streamlit para la interfaz y SQLite para la base de datos.

## ✨ Características

- **📝 Registro de Comidas**: Añade alimentos y obtén información nutricional automática
- **💪 Seguimiento de Entrenamientos**: Registra actividades físicas y calcula calorías quemadas con **API real de ExerciseDB**
- **🌍 Traducción Automática**: Interfaz en español con traducción automática a inglés para la API
- **📊 Dashboard Interactivo**: Visualiza tu progreso con gráficas y estadísticas
- **🗄️ Base de Datos Local**: Almacena todos tus datos en SQLite
- **🔌 API Real de Deportes**: Conexión directa a ExerciseDB para datos precisos de ejercicios
- **📱 Interfaz Web**: Dashboard responsive con Streamlit

## 🆕 Mejoras Recientes

### 🚀 API Real de Deportes
- **ExerciseDB Integrado**: Conexión directa a base de datos real de ejercicios
- **Sin Caché**: Datos siempre actualizados y precisos
- **69+ Actividades**: Amplia gama de ejercicios deportivos
- **Cálculos MET**: Valores metabólicos reales para precisión

### 🌍 Sistema de Traducción
- **Español ↔ Inglés**: Interfaz en español, API en inglés
- **Traducción Automática**: Sin intervención del usuario
- **69 Mapeos**: Actividades comunes predefinidas
- **Extensible**: Fácil añadir nuevas traducciones

### ⚡ Código Simplificado
- **Sin Sistema de Fallback**: Solo API real, sin datos simulados
- **Llamadas Directas**: Sin intermediarios ni caché
- **Mantenimiento Fácil**: Código más limpio y directo
- **Errores Claros**: Mensajes informativos cuando algo falla

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

## 📁 Estructura del Proyecto

```
fitness_tracker/
├── app.py                     # Punto de entrada principal
├── requirements.txt           # Dependencias del proyecto
├── config.py                 # Configuración general
│
├── models/                    # Modelos de datos
│   ├── __init__.py
│   ├── database.py           # Conexión SQLite
│   ├── training_model.py     # CRUD entrenamientos
│   └── nutrition_model.py    # CRUD comidas
│
├── views/                     # Interfaz de usuario
│   ├── __init__.py
│   └── dashboard_view.py     # Dashboard con Streamlit
│
├── controllers/               # Lógica de negocio
│   ├── __init__.py
│   ├── training_controller.py # Controlador entrenamientos
│   └── nutrition_controller.py # Controlador comidas
│
├── services/                  # APIs externas
│   ├── __init__.py
│   ├── nutrition_api.py      # API nutrición (mock)
│   └── training_api.py          # API entrenamiento (real - ExerciseDB)
│
├── tests/                     # Pruebas unitarias
│   ├── __init__.py
│   ├── test_training.py      # Pruebas entrenamientos
│   └── test_nutrition.py     # Pruebas nutrición
│
└── utils/                     # Utilidades
    ├── __init__.py
    ├── check_dependencies.py  # Verificación dependencias
    └── helpers.py             # Funciones auxiliares
```

## 🎯 Uso de la Aplicación

### Añadir Comida
1. En la barra lateral, ve a la pestaña "🍽️ Comida"
2. Escribe el nombre del alimento (ej: "pollo", "arroz", "manzana")
3. Especifica los gramos
4. Haz clic en "➕ Añadir Comida"
5. La aplicación calculará automáticamente las calorías y macronutrientes

### Añadir Entrenamiento
1. En la barra lateral, ve a la pestaña "💪 Entrenamiento"
2. Escribe la actividad **en español** (ej: "correr", "gimnasio", "yoga")
3. Especifica los minutos
4. Haz clic en "🏃‍♂️ Añadir Entrenamiento"
5. La aplicación **traducirá automáticamente** al inglés y calculará las calorías quemadas usando la **API real de ExerciseDB**

### Ver Estadísticas
- **Balance Calórico**: Compara calorías consumidas vs quemadas
- **Macronutrientes**: Distribución de proteínas, carbohidratos y grasas
- **Actividad Física**: Progreso de entrenamientos por día
- **Registros Recientes**: Últimas comidas y entrenamientos

## 🔧 Configuración

Puedes modificar la configuración en `config.py`:

- **Base de datos**: Cambiar nombre y ubicación
- **Gráficas**: Ajustar dimensiones y colores
- **APIs**: Modificar delays y configuraciones
- **Metas**: Establecer objetivos nutricionales y de fitness

### 🆕 Configuración de API de Deportes
La API de ExerciseDB ya está configurada y lista para usar:
- **API Key**: Configurada automáticamente
- **Host**: exercisedb.p.rapidapi.com
- **Traducción**: 69+ actividades en español-inglés
- **Sin configuración adicional**: ¡Lista para usar!

## 🧪 Ejecutar Pruebas

```bash
# Instalar pytest si no está instalado
pip install pytest

# Ejecutar todas las pruebas
python -m pytest tests/

# Ejecutar pruebas específicas
python -m pytest tests/test_training.py
python -m pytest tests/test_nutrition.py
```

## 📊 APIs

### Nutrición
La aplicación incluye una base de datos simulada con alimentos comunes:
- **Alimentos conocidos**: Valores nutricionales realistas
- **Alimentos nuevos**: Cálculos aproximados basados en patrones

### Deporte 🆕
**API Real de ExerciseDB** integrada para actividades deportivas:
- **🌐 API Real**: Conexión directa a ExerciseDB (RapidAPI)
- **🌍 Traducción Automática**: Español ↔ Inglés automático
- **💪 69+ Actividades**: Correr, caminar, gimnasio, yoga, etc.
- **🔥 Cálculo Preciso**: Calorías basadas en valores MET reales
- **⚡ Sin Caché**: Datos siempre actualizados de la API
- **🔑 Configuración**: API key configurada y lista para usar

**Actividades Soportadas:**
- **Cardio**: Correr, caminar, ciclismo, natación, fútbol
- **Fuerza**: Gimnasio, pesas, calistenia, crossfit
- **Flexibilidad**: Yoga, pilates, estiramientos
- **Específicas**: Sentadillas, flexiones, dominadas, plancha
- **Equipamiento**: Mancuernas, barra, máquina, cable
- **Partes del Cuerpo**: Pecho, espalda, brazos, piernas, core

## 🛠️ Desarrollo

### Entorno Virtual
- **venv**: Entorno virtual aislado para el proyecto
- **requirements.txt**: Dependencias principales del proyecto
- **requirements-lock.txt**: Versiones exactas de las dependencias instaladas
- **Scripts automáticos**: `run_app.bat` (Windows) y `run_app.sh` (Linux/Mac) - Hacen TODO automáticamente
- **Scripts de activación**: `activate_venv.bat` (Windows) y `activate_venv.sh` (Linux/Mac) - Solo activan el entorno

### Patrón MVC
- **Models**: Acceso a datos y lógica de persistencia
- **Views**: Interfaz de usuario con Streamlit
- **Controllers**: Lógica de negocio y validaciones
- **Services**: APIs externas (nutrición mock + deportes real)

### Base de Datos
- **SQLite**: Base de datos ligera y portable
- **Tablas**: `trainings` y `meals`
- **Índices**: Optimizados para consultas por fecha

### Dependencias Principales
- **Streamlit**: Framework web para el dashboard
- **Plotly**: Gráficas interactivas y visualizaciones
- **Pandas**: Manipulación y análisis de datos
- **SQLite3**: Base de datos (incluida en Python)
- **Requests**: Conexión a API real de ExerciseDB

## 🚨 Solución de Problemas

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Database error"
- Verifica permisos de escritura en el directorio
- Elimina el archivo de base de datos corrupto

### Error: "Streamlit not found"
```bash
pip install streamlit
```

### Error: "API key no configurada"
- La API de ExerciseDB ya está configurada automáticamente
- Si hay problemas, verifica la conexión a internet
- La API tiene rate limiting gratuito (10 ejercicios por llamada)

### Error: "No se encontraron datos para la actividad"
- Verifica que la actividad esté en español
- La API soporta 69+ actividades predefinidas
- Algunas actividades pueden no estar disponibles en la base de datos

## 📝 Notas del Desarrollador

Este proyecto fue desarrollado como ejercicio de aprendizaje de Python, siguiendo buenas prácticas de programación:

- **Código limpio**: Comentarios claros y estructura organizada
- **Manejo de errores**: Try-catch y validaciones apropiadas
- **Pruebas unitarias**: Cobertura básica de funcionalidades
- **Documentación**: README completo y comentarios en código

### 🆕 Cambios Recientes
- **API Real de Deportes**: Integración completa con ExerciseDB
- **Sistema de Traducción**: 69+ actividades en español-inglés
- **Código Simplificado**: Eliminación del sistema de caché para mayor simplicidad
- **Datos Precisos**: Cálculos de calorías basados en valores MET reales

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork del proyecto
2. Crear rama para nueva funcionalidad
3. Implementar cambios
4. Añadir pruebas
5. Crear Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

**Estudiante de Python** - Desarrollado como proyecto de aprendizaje

---

**¡Disfruta usando Fitness Tracker para mejorar tu salud y fitness! 🎉**
