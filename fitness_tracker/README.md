# Limen - Fitness Tracker Inteligente

**Seguimiento completo de entrenamientos y nutrición con dashboard web interactivo**

Aplicación Python moderna para registrar y analizar actividad física y alimentación. Desarrollada con arquitectura MVC, Streamlit para la interfaz web y SQLite para persistencia local.

## Características Principales

- **Registro de Comidas**: Búsqueda inteligente con traducción automática español-inglés usando OpenAI GPT
- **Seguimiento de Entrenamientos**: 135 deportes organizados en 19 categorías con cálculo automático de calorías basándose en los valores MET (Metabolic Equivalent of Task)
- **Dashboard Interactivo**: Gráficas y estadísticas en tiempo real con base de datos local
- **Funcionalidad Offline**: Deportes y cálculos disponibles sin conexión a internet
- **Sistema de Toast Inteligente**: Notificaciones automáticas en sidebar para comidas y entrenamientos
- **Reset Automático de Formularios**: Los desplegables se limpian automáticamente después de añadir registros

## Sistema de Nutrición

### USDA FoodData Central
- Base de datos oficial del gobierno de Estados Unidos con 300,000+ alimentos
- Información nutricional completa y verificada
- Búsqueda híbrida: Foundation (materias primas) + Legacy (secundaria)(más opciones sobre registros antiguos)

### Traducción Automática
- API de OpenAI para terminología nutricional específica
- Entrada en español, búsqueda en la API de USDA en inglés, resultados en español

## Sistema de Entrenamientos

### Base de Datos Local
- **135 deportes** organizados en 19 categorías
- Valores MET (Metabolic Equivalent of Task) precisos basados en estudios científicos
- Cálculo automático de calorías según peso del usuario, la duración y el MET

### Categorías Principales
- **Deportes de Equipo**: Fútbol, Baloncesto, Voleibol, Rugby...
- **Deportes Acuáticos**: Natación, Waterpolo, Surf, Buceo...
- **Deportes de Combate**: Boxeo, Karate, MMA, Judo...
- **Deportes de Resistencia**: Correr, Ciclismo, Triatlón...
- **Actividades Fitness**: Yoga, Pilates, Spinning, CrossFit...

## Instalación y Uso

### Ejecución Rápida
**Doble clic en:** `run_app.bat` (hace todo automáticamente)

### Instalación Manual
Ver `INSTALACION.md` para pasos detallados.

### Uso Básico
1. **Perfil**: Configura nombre, peso y objetivo (en dashboard)
2. **Comidas**: Busca alimentos en español, selecciona opción, especifica gramos
3. **Entrenamientos**: Elige categoría, deporte, duración y confirma
4. **Dashboard**: Visualiza balance calórico, macronutrientes y estadísticas
5. **Notificaciones**: Los toasts aparecen automáticamente en el sidebar
6. **Formularios**: Se limpian automáticamente después de cada registro

## Arquitectura del Proyecto

### Estructura MVC
```
fitness_tracker/
├── controllers/           # Lógica de negocio y ViewModels
├── models/               # Persistencia SQLite
├── services/             # APIs externas y lógica de dominio
├── views/                # Interfaz Streamlit
├── utils/                # Utilidades y helpers
└── tests/                # Pruebas unitarias
```

### Tecnologías
- **Frontend**: Streamlit (dashboard web responsive)
- **Backend**: Python con patrón MVC
- **Base de datos**: SQLite local
- **APIs externas**: USDA FoodData Central, OpenAI GPT

## Configuración y APIs

### Límites de API
- **USDA**: 3,600 peticiones/día (sin key) / 10,000 (con key **Actual**)
- **OpenAI**: Según plan de suscripción

### Configuración
- **USDA API Key**: En `config.py` para mayor límite de peticiones
- **OpenAI API Key**: En `config.py` para traducción automática

### Dependencias y Limitaciones
- **USDA API**: Requerida para búsqueda de alimentos (sin conexión = no funciona nutrición)
- **OpenAI API**: Requerida para traducción automática (sin conexión = búsqueda manual en inglés)
- **Sistema offline**: Solo funciona para deportes y cálculos locales

## Estadísticas del Sistema

- **Deportes**: 135 actividades físicas (MET: 1.5 - 12.0)
- **Alimentos**: 300,000+ en base USDA
- **Categorías**: 19 tipos de deportes organizados
- **Funcionalidades**: Dashboard interactivo, cálculos automáticos, historial completo

## Testing

### Ejecutar Pruebas (Windows)
**Opción 1 - Automático (Recomendado):**
```bash
# Solo ejecutar este comando:
run_tests.bat
```

**Opción 2 - Manual:**
```bash
# Activar entorno virtual
venv\Scripts\activate

# Ejecutar tests individuales
python tests/test_translation_service.py
python tests/test_sports_database.py
python tests/test_usda_search.py
```

### Tests Disponibles
- **`test_translation_service.py`** - 🔤 OpenAI y traducciones español ↔ inglés ✅
- **`test_sports_database.py`** - 🏃‍♂️ Base de datos de 135 deportes y cálculos MET ✅
- **`test_usda_search.py`** - 🔍 Filtros inteligentes USDA (Foundation + Legacy) ✅

## Escalabilidad

### Uso Actual
- Seguimiento personal con dashboard privado
- Base de datos local SQLite
- Funcionalidad offline completa

### Escalabilidad Futura
- Migración a servidor web (arquitectura MVC preparada)
- Base de datos multi-usuario (PostgreSQL/MySQL)
- Sistema de autenticación y API REST
- Aplicación web y móvil

## Documentación

- **README**: Información general y uso básico
- **[Documentación Técnica](DOCUMENTACION_TECNICA.md)**: Detalles de implementación para desarrolladores


### Desarrollo Local
1. Clona el repositorio
2. `python -m venv venv`
3. `venv\Scripts\activate` (Windows)
4. `pip install -r requirements.txt`
5. `streamlit run app.py`
