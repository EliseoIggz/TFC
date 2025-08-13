# 🏃‍♂️ Fitness Tracker

**Seguimiento de entrenamientos y nutrición con dashboard web**

Una aplicación Python para registrar y analizar tu actividad física y alimentación. Desarrollada siguiendo el patrón MVC con Streamlit para la interfaz y SQLite para la base de datos.

## ✨ Características

- **📝 Registro de Comidas**: Añade alimentos y obtén información nutricional automática
- **💪 Seguimiento de Entrenamientos**: Registra actividades físicas y calcula calorías quemadas
- **📊 Dashboard Interactivo**: Visualiza tu progreso con gráficas y estadísticas
- **🗄️ Base de Datos Local**: Almacena todos tus datos en SQLite
- **🔌 APIs Mock**: Simula APIs reales para nutrición y deporte
- **📱 Interfaz Web**: Dashboard responsive con Streamlit

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
├── services/                  # APIs externas (mock)
│   ├── __init__.py
│   ├── nutrition_api.py      # API nutrición
│   └── sport_api.py          # API deporte
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
2. Escribe la actividad (ej: "running", "gym", "yoga")
3. Especifica los minutos
4. Haz clic en "🏃‍♂️ Añadir Entrenamiento"
5. La aplicación calculará automáticamente las calorías quemadas

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

## 📊 APIs Mock

### Nutrición
La aplicación incluye una base de datos simulada con alimentos comunes:
- **Alimentos conocidos**: Valores nutricionales realistas
- **Alimentos nuevos**: Cálculos aproximados basados en patrones

### Deporte
Base de datos de actividades deportivas:
- **Actividades conocidas**: Calorías por minuto precisas
- **Actividades nuevas**: Estimaciones basadas en intensidad

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

### Base de Datos
- **SQLite**: Base de datos ligera y portable
- **Tablas**: `trainings` y `meals`
- **Índices**: Optimizados para consultas por fecha

### Dependencias Principales
- **Streamlit**: Framework web para el dashboard
- **Plotly**: Gráficas interactivas y visualizaciones
- **Pandas**: Manipulación y análisis de datos
- **SQLite3**: Base de datos (incluida en Python)

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

## 📝 Notas del Desarrollador

Este proyecto fue desarrollado como ejercicio de aprendizaje de Python, siguiendo buenas prácticas de programación:

- **Código limpio**: Comentarios claros y estructura organizada
- **Manejo de errores**: Try-catch y validaciones apropiadas
- **Pruebas unitarias**: Cobertura básica de funcionalidades
- **Documentación**: README completo y comentarios en código

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
