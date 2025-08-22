# Limen - Fitness Tracker Inteligente

**Seguimiento completo de entrenamientos y nutrición con dashboard web interactivo**

Aplicación Python moderna para registrar y analizar actividad física y alimentación. Desarrollada con arquitectura MVC, Streamlit para la interfaz web y SQLite para persistencia local.

## Características Principales

- **Registro de Comidas**: Búsqueda inteligente con traducción automática español-inglés usando OpenAI GPT
- **Seguimiento de Entrenamientos**: 135 deportes organizados en 19 categorías con cálculo automático de calorías basandose en los valores MET (Metabolic Equivalent of Task)
- **Dashboard Interactivo**: Gráficas y estadísticas en tiempo real con base de datos local
- **Funcionalidad Offline**: Deportes y cálculos disponibles sin conexión a internet

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
1. **Perfil**: Configura nombre, peso y objetivo(en dashboard)
2. **Comidas**: Busca alimentos en español, selecciona opción, especifica gramos
3. **Entrenamientos**: Elige categoría, deporte, duración y confirma
4. **Dashboard**: Visualiza balance calórico, macronutrientes y estadísticas

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

### Ejecutar Pruebas
```bash
cd fitness_tracker
python -m pytest tests/
```

### Pruebas Específicas
- `test_expanded_sports.py` - Base de deportes
- `test_usda_nutrition.py` - Sistema de nutrición
- `test_openai_integration.py` - Integración OpenAI
- `test_training.py` - Funcionalidades básicas

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
3. `venv\Scripts\activate` (Windows) / `source venv/bin/activate` (Linux/Mac)
4. `pip install -r requirements.txt`
5. `streamlit run app.py`
