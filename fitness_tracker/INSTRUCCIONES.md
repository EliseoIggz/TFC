# 🚀 Instrucciones Rápidas - Limen

## ⚡ Ejecución Rápida

### Windows
1. **Doble clic en:** `run_app.bat` ⭐ **RECOMENDADO**
   - Hace TODO automáticamente: verifica, instala y ejecuta
   
2. **Alternativa manual:**
   - Doble clic en: `activate_venv.bat`
   - Ejecutar: `streamlit run app.py`

### Linux/Mac
1. **Ejecutar:** `./run_app.sh` ⭐ **RECOMENDADO**
   - Hace TODO automáticamente: verifica, instala y ejecuta
   
2. **Alternativa manual:**
   - Ejecutar: `./activate_venv.sh`
   - Ejecutar: `streamlit run app.py`

## 🔧 Instalación Manual

### 1. Crear entorno virtual
```bash
python -m venv venv
```

### 2. Activar entorno virtual
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar aplicación
```bash
streamlit run app.py
```

## 📱 Uso de la Aplicación

1. **Añadir Comida**: Barra lateral → Pestaña "🍽️ Comida"
2. **Añadir Entrenamiento**: Barra lateral → Pestaña "💪 Entrenamiento"
3. **Ver Estadísticas**: Dashboard principal con gráficas
4. **Registros Recientes**: Tabla inferior con últimos registros

## 🗄️ Base de Datos

- **Ubicación**: `./data/fitness_tracker.db`
- **Se crea automáticamente** al ejecutar la aplicación
- **Datos**: Entrenamientos y comidas registrados

## 🧪 Ejecutar Pruebas

```bash
# Con entorno virtual activado
python -m pytest tests/
```

## 📦 Archivos Importantes

- `app.py` - Punto de entrada principal
- `requirements.txt` - Dependencias del proyecto
- `requirements-lock.txt` - Versiones exactas instaladas
- `venv/` - Entorno virtual (no incluir en entrega)
- `.gitignore` - Archivos a excluir del control de versiones

## 🚀 Scripts Automáticos

### `run_app.bat` / `run_app.sh` ⭐ **PRINCIPAL**
- **Verifica** si Python está instalado
- **Crea** entorno virtual si no existe
- **Instala** dependencias si es necesario
- **Ejecuta** la aplicación automáticamente
- **Solo necesitas hacer doble clic** (Windows) o ejecutar (Linux/Mac)

### `activate_venv.bat` / `activate_venv.sh`
- Solo activa el entorno virtual
- Para uso manual o desarrollo

## 🚨 Solución de Problemas

### Error: "Module not found"
- Asegúrate de que el entorno virtual esté activado
- Ejecuta: `pip install -r requirements.txt`

### Error: "Streamlit not found"
- Verifica que estés en el entorno virtual: `(venv)` en el prompt
- Reinstala: `pip install streamlit`

### Error: "Database error"
- Verifica permisos de escritura en el directorio
- La base de datos se crea automáticamente

## 🎯 Para Evaluación

1. **Entregar todo el proyecto** excepto la carpeta `venv/`
2. **Incluir** `requirements.txt` y `requirements-lock.txt`
3. **Documentar** cómo ejecutar el proyecto
4. **Probar** que funcione en una máquina limpia

---

**¡El proyecto está listo para usar! 🎉**
