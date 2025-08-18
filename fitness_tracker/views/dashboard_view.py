# Fitness Tracker - Vista del Dashboard
# =====================================
# Este archivo contiene la interfaz principal de la aplicación con Streamlit

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import pandas as pd
from controllers.training_controller import TrainingController
from controllers.nutrition_controller import NutritionController
from controllers.user_controller import UserController
import config

class DashboardView:
    """Vista principal del dashboard de Fitness Tracker"""
    
    def __init__(self):
        """Inicializar la vista del dashboard"""
        self.training_controller = TrainingController()
        self.nutrition_controller = NutritionController()
        self.user_controller = UserController()
        
        # Configurar página de Streamlit
        st.set_page_config(
            page_title=config.STREAMLIT_TITLE,
            layout=config.STREAMLIT_LAYOUT,
            initial_sidebar_state=config.STREAMLIT_SIDEBAR_STATE
        )
    
    def render(self):
        """Renderizar el dashboard completo"""
        # Título principal
        st.title("🏃‍♂️ Fitness Tracker")
        st.markdown("**Seguimiento de entrenamientos y nutrición**")
        
        # Sección de bienvenida personalizada (cargar desde BD si no está en sesión)
        if 'user_name' not in st.session_state or 'user_weight' not in st.session_state:
            profile = self.user_controller.get_profile()
            if profile['success']:
                st.session_state['user_name'] = profile['data']['name']
                st.session_state['user_weight'] = profile['data']['weight']
        
        # Obtener valores actuales de la sesión
        user_name = st.session_state.get('user_name', '')
        user_weight = st.session_state.get('user_weight', 70.0)
        
        # Debug: mostrar valores cargados
        if st.session_state.get('debug_profile', False):
            st.info(f"🔍 Debug - Nombre: '{user_name}', Peso: {user_weight}kg")
        
        if user_name:            
            # Mostrar información del usuario en el dashboard principal
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("👤 Usuario", user_name)
            with col2:
                st.metric("⚖️ Peso", f"{user_weight} kg")
                
            st.divider()
        
        # Sidebar para formularios
        with st.sidebar:
            # Sección de perfil del usuario
            st.header("👤 Mi Perfil")
            
            # Campo para nombre
            user_name = st.text_input(
                "Nombre:",
                value=st.session_state.get('user_name', ''),
                placeholder="Tu nombre",
                key="user_name_input"
            )
            
            # Campo para peso
            user_weight = st.number_input(
                "Peso (kg):",
                min_value=30.0,
                max_value=200.0,
                value=st.session_state.get('user_weight', 70.0),
                step=0.5,
                key="user_weight_input"
            )
            
            # Guardar automáticamente en BD cuando cambien los valores
            current_name = st.session_state.get('user_name', '')
            current_weight = st.session_state.get('user_weight', 70.0)
            
            if user_name != current_name or user_weight != current_weight:
                # Guardar automáticamente en la base de datos
                result = self.user_controller.save_profile(user_name, user_weight)
                if result['success']:
                    # Actualizar la sesión inmediatamente
                    st.session_state['user_name'] = user_name
                    st.session_state['user_weight'] = user_weight
                    st.success("✅ Perfil actualizado automáticamente")
                    # Pequeña pausa para mostrar el mensaje
                    import time
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(f"❌ Error al guardar: {result['message']}")
            
            # Mostrar información del usuario
            if user_name:
                st.success(f"👋 ¡Hola {user_name}!")
                st.info(f"⚖️ Tu peso: {user_weight} kg")
            
            # Botón de debug temporal
            if st.button("🔍 Debug perfil", key="debug_profile_btn"):
                st.session_state.debug_profile = not st.session_state.get('debug_profile', False)
                st.rerun()
            
            st.divider()
            
            st.header("📝 Añadir Registro")
            
            # Tabs para diferentes tipos de registro
            tab1, tab2 = st.tabs(["🍽️ Comida", "💪 Entrenamiento"])
            
            with tab1:
                self._render_meal_form()
            
            with tab2:
                self._render_training_form()
        
        # Contenido principal
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfica de calorías
            self._render_calories_chart()
        
        with col2:
            # Estadísticas del día
            self._render_daily_stats()
        
        # Tabla de registros recientes
        self._render_recent_records()
        
        # Gráficas adicionales
        col3, col4 = st.columns(2)
        
        with col3:
            # Gráfica de macronutrientes
            self._render_macros_chart()
        
        with col4:
            # Gráfica de actividad
            self._render_activity_chart()
    
    def _render_meal_form(self):
        """Renderizar formulario para añadir comida"""
        st.subheader("Nueva Comida")
        
        # Verificar si hay opciones de alimentos pendientes en session_state
        if 'food_options' in st.session_state and st.session_state.food_options:
            # Renderizar el selector de opciones
            self._render_food_selector(st.session_state.food_options)
        else:
            # Renderizar el formulario normal
            food = st.text_input("Alimento", placeholder="Ej: pollo, arroz, manzana...", key="food_input")
            grams = st.number_input("Gramos", min_value=1, max_value=10000, value=100, key="grams_input")
            
            if st.button("➕ Añadir Comida", type="primary", key="add_meal_button"):
                if food and grams:
                    result = self.nutrition_controller.add_meal(food, grams)
                    
                    if result['success']:
                        st.success(result['message'])
                        st.rerun()
                    elif result.get('multiple_options'):
                        # Guardar opciones en session_state para persistencia
                        st.session_state.food_options = result['options_data']
                        st.rerun()
                    else:
                        st.error(result['message'])
                else:
                    st.warning("Por favor completa todos los campos")
    
    def _render_food_selector(self, options_data: dict):
        """Renderizar selector interactivo de alimentos"""
        # SIEMPRE actualizar las opciones en session_state (no solo si no existe)
        st.session_state.food_options = options_data
        
        st.info(f"🔍 Se encontraron {len(options_data['options'])} opciones para '{options_data['search_term']}':")
        
        # Botón para cancelar y volver al formulario
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("❌ Cancelar", key="cancel_food_selection"):
                # Limpiar session_state y volver al formulario
                if 'food_options' in st.session_state:
                    del st.session_state.food_options
                # También limpiar cualquier key de radio button relacionado
                keys_to_clear = [k for k in st.session_state.keys() if k.startswith('food_radio_')]
                for key in keys_to_clear:
                    del st.session_state[key]
                st.rerun()
        
        with col2:
            st.write("")  # Espaciado
        
        # Crear lista de opciones para el selectbox
        option_labels = [opt['display_name'] for opt in options_data['options']]
        
        # Usar un key único que incluya el término de búsqueda para evitar conflictos
        radio_key = f"food_radio_{options_data['search_term']}_{len(options_data['options'])}"
        
        # Radio buttons con key único - SIN usar session_state para index (causa problemas)
        selected_index = st.radio(
            "Selecciona el producto específico:",
            options=range(len(option_labels)),
            format_func=lambda x: option_labels[x],
            key=radio_key,
            index=0  # Siempre empezar con la primera opción
        )
        
        # El selected_index viene directamente del radio button
        if selected_index is not None:
            selected_option = options_data['options'][selected_index]
            
            # Mostrar información detallada de la opción seleccionada
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"📦 **Producto:** {selected_option['name']}")
                st.info(f"🏷️ **Marca:** {selected_option['brand']}")
            
            with col2:
                st.info(f"🔥 **Calorías:** {selected_option['calories_per_100g']} cal/100g")
                st.info(f"⚖️ **Cantidad:** {options_data['grams']}g")
            
            # Calcular calorías totales para la cantidad especificada
            total_calories = round((selected_option['calories_per_100g'] * options_data['grams']) / 100)
            st.success(f"🧮 **Total:** {total_calories} calorías para {options_data['grams']}g")
            
            # Botón para confirmar la selección con key único
            confirm_key = f"confirm_food_{options_data['search_term']}_{selected_index}"
            if st.button(f"✅ Añadir {selected_option['name']}", type="primary", key=confirm_key):
                # Procesar la selección
                result = self.nutrition_controller.add_meal_from_selection(options_data, selected_index)
                
                if result['success']:
                    st.success(result['message'])
                    # Limpiar session_state relacionado con la selección
                    if 'food_options' in st.session_state:
                        del st.session_state.food_options
                    # También limpiar cualquier key de radio button relacionado
                    keys_to_clear = [k for k in st.session_state.keys() if k.startswith('food_radio_')]
                    for key in keys_to_clear:
                        del st.session_state[key]
                    st.rerun()
                else:
                    st.error(result['message'])
    
    def _render_training_form(self):
        """Renderizar formulario para añadir entrenamiento"""
        st.subheader("Nuevo Entrenamiento")
        
        # Selector de categoría de deporte
        training_api = self.training_controller.training_api
        categories = training_api.get_sport_categories()
        
        # Crear lista de categorías con nombres legibles
        category_names = {
            'deporte_equipo': '🏀 Deportes de Equipo',
            'deporte_raqueta': '🎾 Deportes de Raqueta',
            'deporte_acuatico': '🏊‍♂️ Deportes Acuáticos',
            'deporte_invierno': '⛷️ Deportes de Invierno',
            'deporte_combate': '🥊 Deportes de Combate',
            'deporte_resistencia': '🏃‍♂️ Deportes de Resistencia',
            'deporte_fuerza': '💪 Deportes de Fuerza',
            'deporte_aventura': '🧗‍♂️ Deportes de Aventura',
            'deporte_baile': '💃 Deportes de Baile',
            'deporte_precision': '🎯 Deportes de Precisión',
            'fitness': '🧘‍♀️ Fitness',
            'ejercicio_fuerza': '🏋️ Ejercicios de Fuerza',
            'actividad_diaria': '🚶‍♂️ Actividades Diarias',
            'deporte_extremo': '🪂 Deportes Extremos',
            'deporte_motor': '🏍️ Deportes Motorizados',
            'deporte_tradicional': '🏺 Deportes Tradicionales',
            'deporte_acuatico_extremo': '🏄‍♂️ Deportes Acuáticos Extremos',
            'deporte_invierno_extremo': '🎿 Deportes de Invierno Extremos'
        }
        
        # Selector de categoría
        selected_category = st.selectbox(
            "🏷️ Categoría de Deporte:",
            options=['Todas'] + list(categories.keys()),
            format_func=lambda x: category_names.get(x, x) if x != 'Todas' else 'Todas'
        )
        
        # Filtrar deportes por categoría seleccionada
        if selected_category == 'Todas':
            available_sports = training_api.get_all_sports()
        else:
            available_sports = []
            for sport in training_api.get_all_sports():
                if sport['category'] == selected_category:
                    available_sports.append(sport)
        
        # Selector de deporte específico
        if available_sports:
            sport_options = {f"{sport['name']} ({sport['met']} MET)": sport['key'] for sport in available_sports}
            selected_sport_key = st.selectbox(
                "🏃‍♂️ Selecciona el Deporte:",
                options=list(sport_options.keys()),
                help="Cada deporte muestra su valor MET para cálculo de calorías"
            )
            selected_sport = sport_options[selected_sport_key]
        else:
            selected_sport = ""
            st.warning("No hay deportes disponibles en esta categoría")
        
        # Campo de minutos
        minutes = st.number_input("⏱️ Minutos", min_value=1, max_value=1440, value=30)
        
        # Mostrar información del deporte seleccionado
        if selected_sport and selected_sport in training_api.sports_database:
            sport_data = training_api.sports_database[selected_sport]
            st.info(f"📊 **{sport_data['name']}**: {sport_data['met']} MET - {sport_data['category']}")
            
            # Obtener peso del usuario desde session_state
            user_weight = st.session_state.get('user_weight', 70.0)
            
            # Calcular calorías estimadas para el peso real del usuario
            estimated_calories = round((sport_data['met'] * user_weight * minutes) / 60)
            st.success(f"🔥 Calorías estimadas: {estimated_calories} cal en {minutes} min (peso: {user_weight} kg)")
            
            # Mostrar diferencia si el peso cambió del valor por defecto
            if user_weight != 70.0:
                default_calories = round((sport_data['met'] * 70 * minutes) / 60)
                difference = estimated_calories - default_calories
                if difference != 0:
                    st.info(f"📊 Diferencia con peso por defecto (70kg): {difference:+d} cal")
        
        # Botón para añadir entrenamiento
        if st.button("🏃‍♂️ Añadir Entrenamiento", type="primary"):
            if selected_sport and minutes:
                # Obtener peso del usuario desde session_state
                user_weight = st.session_state.get('user_weight', 70.0)
                
                result = self.training_controller.add_training(selected_sport, minutes, user_weight)
                if result['success']:
                    st.success(result['message'])
                    st.rerun()
                else:
                    st.error(result['message'])
            else:
                st.warning("Por favor selecciona un deporte y especifica los minutos")
        
        # Mostrar estadísticas de la base de datos
        st.divider()
        st.markdown("**📊 Estadísticas de la Base de Datos:**")
        total_sports = len(training_api.sports_database)
        total_categories = len(categories)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Deportes", total_sports)
        with col2:
            st.metric("Total Categorías", total_categories)
    
    def _render_calories_chart(self):
        """Renderizar gráfica de calorías consumidas vs quemadas"""
        st.subheader("📊 Balance Calórico")
        
        # Obtener datos del día actual
        today = date.today().strftime('%Y-%m-%d')
        
        nutrition_stats = self.nutrition_controller.get_nutrition_stats(today)
        training_stats = self.training_controller.get_training_stats(today)
        
        if nutrition_stats['success'] and training_stats['success']:
            calories_consumed = nutrition_stats['data']['total_calories']
            calories_burned = training_stats['data']['total_calories_burned']
            
            # Crear gráfica de barras
            fig = go.Figure(data=[
                go.Bar(name='Consumidas', x=['Calorías'], y=[calories_consumed], 
                       marker_color='#FF6B6B'),
                go.Bar(name='Quemadas', x=['Calorías'], y=[calories_burned], 
                       marker_color='#4ECDC4')
            ])
            
            fig.update_layout(
                title="Calorías del Día",
                barmode='group',
                height=config.CHART_HEIGHT,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Mostrar balance
            balance = calories_consumed - calories_burned
            if balance > 0:
                st.info(f"Balance: +{balance} calorías (superávit)")
            elif balance < 0:
                st.success(f"Balance: {balance} calorías (déficit)")
            else:
                st.success("Balance: 0 calorías (equilibrio)")
        else:
            st.info("No hay datos para mostrar")
    
    def _render_daily_stats(self):
        """Renderizar estadísticas del día"""
        st.subheader("📈 Estadísticas del Día")
        
        today = date.today().strftime('%Y-%m-%d')
        
        # Estadísticas de nutrición
        nutrition_stats = self.nutrition_controller.get_nutrition_stats(today)
        if nutrition_stats['success']:
            data = nutrition_stats['data']
            st.metric("Calorías Consumidas", f"{data['total_calories']} cal")
            st.metric("Proteínas", f"{data['total_proteins']:.1f}g")
            st.metric("Carbohidratos", f"{data['total_carbs']:.1f}g")
            st.metric("Grasas", f"{data['total_fats']:.1f}g")
        
        # Estadísticas de entrenamiento
        training_stats = self.training_controller.get_training_stats(today)
        if training_stats['success']:
            data = training_stats['data']
            st.metric("Calorías Quemadas", f"{data['total_calories_burned']} cal")
            st.metric("Minutos Activo", f"{data['total_minutes']} min")
    
    def _render_recent_records(self):
        """Renderizar registros con selector de fecha"""
        st.subheader("📋 Registros por Fecha")
        
        # Selector de fecha
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_date = st.date_input(
                "📅 Selecciona una fecha:",
                value=date.today(),
                key="date_selector"
            )
        
        with col2:
            if st.button("🔄 Actualizar", key="refresh_records"):
                st.rerun()
        
        # Convertir fecha a string para la consulta
        date_str = selected_date.strftime('%Y-%m-%d')
        
        # Obtener registros de la fecha seleccionada
        meals_by_date = self.nutrition_controller.get_meals_by_date(date_str)
        trainings_by_date = self.training_controller.get_trainings_by_date(date_str)
        
        # Crear tabs para diferentes tipos de registros
        tab1, tab2 = st.tabs(["🍽️ Comidas", "💪 Entrenamientos"])
        
        with tab1:
            self._render_meals_table(meals_by_date, selected_date)
        
        with tab2:
            self._render_trainings_table(trainings_by_date, selected_date)
    
    def _render_meals_table(self, meals_result, selected_date):
        """Renderizar tabla de comidas con botones de borrar"""
        if meals_result['success'] and meals_result['data']:
            st.info(f"🍽️ Comidas del {selected_date.strftime('%d/%m/%Y')} ({len(meals_result['data'])} registros)")
            
            # Crear DataFrame con columnas traducidas
            meals_df = pd.DataFrame(meals_result['data'])
            
            # Traducir columnas
            meals_display = meals_df[['id', 'food', 'grams', 'calories', 'proteins', 'carbs', 'fats', 'created_at']].copy()
            meals_display.columns = ['ID', 'Alimento', 'Gramos', 'Calorías', 'Proteínas', 'Carbohidratos', 'Grasas', 'Hora']
            
            # Formatear la hora para mostrar solo HH:MM
            meals_display['Hora'] = pd.to_datetime(meals_df['created_at']).dt.strftime('%H:%M')
            
            # Mostrar cada fila con botón de borrar
            for idx, row in meals_df.iterrows():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    # Mostrar información de la comida
                    st.write(f"🍽️ **{row['food']}** - {row['grams']}g - {row['calories']} cal - {row['proteins']}g prot - {pd.to_datetime(row['created_at']).strftime('%H:%M')}")
                
                with col2:
                    # Botón de borrar
                    if st.button("🗑️", key=f"delete_meal_{row['id']}", help="Borrar comida"):
                        result = self.nutrition_controller.delete_meal(row['id'])
                        if result['success']:
                            st.success("Comida eliminada")
                            st.rerun()
                        else:
                            st.error(result['message'])
        else:
            st.info(f"📭 No hay comidas registradas para el {selected_date.strftime('%d/%m/%Y')}")
    
    def _render_trainings_table(self, trainings_result, selected_date):
        """Renderizar tabla de entrenamientos con botones de borrar"""
        if trainings_result['success'] and trainings_result['data']:
            st.info(f"💪 Entrenamientos del {selected_date.strftime('%d/%m/%Y')} ({len(trainings_result['data'])} registros)")
            
            # Crear DataFrame con columnas traducidas
            trainings_df = pd.DataFrame(trainings_result['data'])
            
            # Mostrar cada fila con botón de borrar
            for idx, row in trainings_df.iterrows():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    # Mostrar información del entrenamiento
                    st.write(f"💪 **{row['activity']}** - {row['minutes']} min - {row['calories_burned']} cal - {pd.to_datetime(row['created_at']).strftime('%H:%M')}")
                
                with col2:
                    # Botón de borrar
                    if st.button("🗑️", key=f"delete_training_{row['id']}", help="Borrar entrenamiento"):
                        result = self.training_controller.delete_training(row['id'])
                        if result['success']:
                            st.success("Entrenamiento eliminado")
                            st.rerun()
                        else:
                            st.error(result['message'])
        else:
            st.info(f"📭 No hay entrenamientos registrados para el {selected_date.strftime('%d/%m/%Y')}")
    
    def _render_macros_chart(self):
        """Renderizar gráfica de macronutrientes"""
        st.subheader("🥗 Macronutrientes")
        
        today = date.today().strftime('%Y-%m-%d')
        nutrition_stats = self.nutrition_controller.get_nutrition_stats(today)
        
        if nutrition_stats['success']:
            data = nutrition_stats['data']
            
            # Crear gráfica de dona
            fig = go.Figure(data=[go.Pie(
                labels=['Proteínas', 'Carbohidratos', 'Grasas'],
                values=[data['total_proteins'], data['total_carbs'], data['total_fats']],
                hole=0.4,
                marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1']
            )])
            
            fig.update_layout(
                title="Distribución de Macronutrientes",
                height=config.CHART_HEIGHT,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos nutricionales")
    
    def _render_activity_chart(self):
        """Renderizar gráfica de actividad"""
        st.subheader("🏃‍♂️ Actividad Física")
        
        # Obtener todos los entrenamientos para el gráfico
        all_trainings = self.training_controller.get_all_trainings()
        
        if all_trainings['success'] and all_trainings['data']:
            trainings_df = pd.DataFrame(all_trainings['data'])
            
            # Agrupar por fecha
            daily_activity = trainings_df.groupby('date').agg({
                'calories_burned': 'sum',
                'minutes': 'sum'
            }).reset_index()
            
            # Crear gráfica de líneas
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=daily_activity['date'],
                y=daily_activity['calories_burned'],
                mode='lines+markers',
                name='Calorías Quemadas',
                line=dict(color='#4ECDC4', width=3)
            ))
            
            fig.update_layout(
                title="Actividad por Día",
                xaxis_title="Fecha",
                yaxis_title="Calorías Quemadas",
                height=config.CHART_HEIGHT,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de actividad")
