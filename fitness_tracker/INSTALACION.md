# Instrucciones de Instalación y Ejecución - Limen

## Ejecución Automática (Recomendado)

**Simplemente haz doble clic en:** `run_app.bat`
- El script hace todo automáticamente
- Verifica Python, crea entorno virtual, instala dependencias y ejecuta la app

## Instalación Manual (Si la automática falla)

### 1. Verificar Python
**Limen requiere Python 3.11 o superior**

Abre una terminal y ejecuta:
```bash
python --version
```

Si no funciona, prueba:
```bash
python3 --version
```

### 2. Si Python no está instalado

1. **Descarga desde:** [python.org/downloads](https://www.python.org/downloads/)
2. **Selecciona:** Python 3.11.8 (la versión que usa Limen)
3. **IMPORTANTE:** Marca la casilla "Add Python to PATH" durante la instalación
4. **Reinicia** la terminal después de instalar

### 3. Si Python está instalado pero no se reconoce

#### Configurar PATH manualmente
1. Busca "Variables de entorno" en Windows
2. Click en "Variables de entorno..."
3. En "Variables del sistema", busca "Path" y click "Editar"
4. Click "Nuevo" y añade estas rutas:
   ```
   C:\Users\[TuUsuario]\AppData\Local\Programs\Python\Python311\
   C:\Users\[TuUsuario]\AppData\Local\Programs\Python\Python311\Scripts\
   ```
5. **Reinicia** la terminal

### 4. Crear y activar entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

**Verifica que funcione:** Deberías ver `(venv)` al inicio de la línea de comandos

### 5. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 6. Ejecutar aplicación
```bash
streamlit run app.py
```

## Ejecutar Pruebas

```bash
# Con entorno virtual activado
python -m pytest tests/
```

## Solución de Problemas

### Error: "Python no se reconoce como comando"
- **Causa**: Python no está en el PATH del sistema
- **Solución**: Sigue los pasos de "Configurar PATH manualmente" arriba

### Error: "Module not found"
- **Causa**: Entorno virtual no activado o dependencias no instaladas
- **Solución**: 
  1. Activa el entorno virtual: `venv\Scripts\activate`
  2. Instala dependencias: `pip install -r requirements.txt`

### Error: "Streamlit not found"
- **Causa**: Streamlit no está instalado en el entorno virtual
- **Solución**: 
  1. Asegúrate de que el entorno virtual esté activado (debe aparecer `(venv)`)
  2. Ejecuta: `pip install streamlit`

### Error: "Database error"
- **Causa**: Problemas de permisos o directorio no accesible
- **Solución**: 
  1. Verifica permisos de escritura en el directorio del proyecto
  2. La base de datos se crea automáticamente en la primera ejecución

### Error: "Entorno virtual corrupto"
- **Causa**: Archivos del entorno virtual dañados
- **Solución**: 
  1. Elimina la carpeta `venv` manualmente
  2. Ejecuta `run_app.bat` nuevamente para recrearlo


Si tienes problemas, revisa primero la sección de "Solución de Problemas" arriba. La mayoría de errores se resuelven siguiendo esos pasos.
