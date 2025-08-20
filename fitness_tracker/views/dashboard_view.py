# Fitness Tracker - Vista del Dashboard
# Este archivo contiene la interfaz principal de la aplicación con Streamlit

import streamlit as st
import plotly.graph_objects as go
from datetime import date
import pandas as pd
from controllers.training_controller import TrainingController
from controllers.nutrition_controller import NutritionController
from controllers.user_controller import UserController
import config
from utils.helpers import format_date, format_date_display

class DashboardView:
    """Vista principal del dashboard de Fitness Tracker"""
    
    def __init__(self):
        """Inicializar la vista del dashboard"""
        self.training_controller = TrainingController()
        self.nutrition_controller = NutritionController()
        self.user_controller = UserController()
        
        st.set_page_config(
            page_title=config.STREAMLIT_TITLE,
            layout=config.STREAMLIT_LAYOUT,
            initial_sidebar_state=config.STREAMLIT_SIDEBAR_STATE
        )
    
    def render(self):
        """Renderizar el dashboard completo"""
        st.title("🏃‍♂️ Fitness Tracker")
        st.markdown("**Seguimiento de entrenamientos y nutrición**")
        
        # Obtener perfil UNA SOLA VEZ y almacenarlo en session_state
        if 'user_profile' not in st.session_state:
            profile = self.user_controller.get_profile()
            if profile['success']:
                st.session_state['user_profile'] = profile['data']
                st.session_state['user_name'] = profile['data']['name']
                st.session_state['user_weight'] = profile['data']['weight']
            else:
                st.session_state['user_profile'] = {'name': '', 'weight': 70.0, 'objetivo': 'mantener_peso'}
                st.session_state['user_name'] = ''
                st.session_state['user_weight'] = 70.0
        
        # Usar perfil del session_state
        user_profile = st.session_state['user_profile']
        user_name = user_profile.get('name', '')
        user_weight = user_profile.get('weight', 70.0)
        
        if user_name:            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("👤 Usuario", user_name)
            with col2:
                st.metric("⚖️ Peso", f"{user_weight} kg")
            st.divider()
        
        with st.sidebar:
            st.header("👤 Mi Perfil")
            
            # Mostrar mensaje de perfil actualizado si existe
            if 'profile_updated' in st.session_state and st.session_state.profile_updated:
                st.success("✅ Perfil actualizado automáticamente")
                # Limpiar del session_state
                del st.session_state.profile_updated
            
            user_name = st.text_input(
                "Nombre:",
                value=st.session_state.get('user_name', ''),
                placeholder="Tu nombre",
                key="user_name_input"
            )
            user_weight = st.number_input(
                "Peso (kg):",
                min_value=30.0,
                max_value=200.0,
                value=st.session_state.get('user_weight', 70.0),
                step=0.5,
                key="user_weight_input"
            )
            
            current_name = st.session_state.get('user_name', '')
            current_weight = st.session_state.get('user_weight', 70.0)
            
            if user_name != current_name or user_weight != current_weight:
                result = self.user_controller.save_profile(user_name, user_weight)
                if result['success']:
                    st.session_state['user_name'] = user_name
                    st.session_state['user_weight'] = user_weight
                    st.session_state['profile_updated'] = True
                    st.rerun()
                else:
                    st.error(f"❌ Error al guardar: {result['message']}")
            
            if user_name:
                st.success(f"👋 ¡Hola {user_name}!")
                st.info(f"⚖️ Tu peso: {user_weight} kg")
            
            st.divider()
            st.header("📝 Añadir Registro")
            tab1, tab2 = st.tabs(["🍽️ Comida", "💪 Entrenamiento"])
            
            with tab1:
                self._render_meal_form()
            with tab2:
                self._render_training_form()
        
        col1, col2 = st.columns([2, 1])
        with col1:
            self._render_calories_chart()
        with col2:
            self._render_daily_stats()
        

        
        self._render_macros_section()
        self._render_recent_records()
    
    def _render_meal_form(self):
        """Renderizar formulario para añadir comida"""
        st.subheader("Nueva Comida")
        
        if 'food_options' in st.session_state and st.session_state.food_options:
            self._render_food_selector(st.session_state.food_options)
        else:
            food = st.text_input("Alimento", placeholder="Ej: pollo, arroz, manzana...", key="food_input")
            grams = st.number_input("Gramos", min_value=1, max_value=10000, value=100, key="grams_input")
            
            if st.button("➕ Añadir Comida", type="primary", key="add_meal_button"):
                if food and grams:
                    search_placeholder = st.empty()
                    with search_placeholder.container():
                        st.info(f"🔍 Buscando información nutricional para '{food}'...")
                        result = self.nutrition_controller.add_meal(food, grams)
                    search_placeholder.empty()
                    
                    if result['success']:
                        # Mostrar mensaje temporal de éxito
                        st.session_state['meal_added'] = True
                        st.session_state['meal_message'] = result['message']
                        st.rerun()
                    elif result.get('multiple_options'):
                        st.session_state.food_options = result['options_data']
                        st.rerun()
                    else:
                        st.error(result['message'])
                else:
                    st.warning("Por favor completa todos los campos")
    
    def _render_food_selector(self, options_data: dict):
        """Renderizar selector interactivo de alimentos"""
        st.session_state.food_options = options_data
        st.info(f"🔍 Se encontraron {len(options_data['options'])} opciones para '{options_data['search_term']}':")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("❌ Cancelar", key="cancel_food_selection"):
                st.session_state.pop('food_options', None)
                for key in list(st.session_state.keys()):
                    if key.startswith('food_radio_'):
                        del st.session_state[key]
                st.rerun()
        with col2:
            st.write("")
        
        option_labels = [opt['display_name'] for opt in options_data['options']]
        radio_key = f"food_radio_{options_data['search_term']}_{len(options_data['options'])}"
        selected_index = st.radio(
            "Selecciona el producto específico:",
            options=range(len(option_labels)),
            format_func=lambda x: option_labels[x],
            key=radio_key,
            index=0
        )
        
        if selected_index is not None:
            selected_option = options_data['options'][selected_index]
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"📦 **Producto:** {selected_option['name']}")
                st.info(f"🏷️ **Marca:** {selected_option.get('brand_owner', selected_option.get('brand', 'Sin marca'))}")
                if 'data_type' in selected_option and selected_option['data_type'] != 'Desconocido':
                    st.info(f"📊 **Tipo:** {selected_option['data_type']}")
            
            with col2:
                st.info(f"🔥 **Calorías:** {selected_option['calories_per_100g']} cal/100g")
                st.info(f"⚖️ **Cantidad:** {options_data['grams']}g")
                if 'proteins_per_100g' in selected_option:
                    st.info(f"🥩 **Proteínas:** {selected_option['proteins_per_100g']}g/100g")
                if 'carbs_per_100g' in selected_option:
                    st.info(f"🍞 **Carbohidratos:** {selected_option['carbs_per_100g']}g/100g")
                if 'fats_per_100g' in selected_option:
                    st.info(f"🧈 **Grasas:** {selected_option['fats_per_100g']}g/100g")
            
            total_calories = round((selected_option['calories_per_100g'] * options_data['grams']) / 100)
            st.success(f"🧮 **Total:** {total_calories} calorías para {options_data['grams']}g")
            
            if 'category' in selected_option and selected_option['category'] != 'Sin categoría':
                st.info(f"📂 **Categoría USDA:** {selected_option['category']}")
            
            confirm_key = f"confirm_food_{options_data['search_term']}_{selected_index}"
            if st.button(f"✅ Añadir {selected_option['name']}", type="primary", key=confirm_key):
                process_placeholder = st.empty()
                with process_placeholder.container():
                    st.info(f"⚙️ Procesando selección de '{selected_option['name']}'...")
                    result = self.nutrition_controller.add_meal_from_selection(options_data, selected_index)
                process_placeholder.empty()
                
                if result['success']:
                    st.success(result['message'])
                    st.session_state.pop('food_options', None)
                    for key in list(st.session_state.keys()):
                        if key.startswith('food_radio_'):
                            del st.session_state[key]
                    # Mostrar mensaje temporal de éxito
                    st.session_state['meal_added'] = True
                    st.session_state['meal_message'] = result['message']
                    st.rerun()
                else:
                    st.error(result['message'])
    
    def _render_training_form(self):
        """Renderizar formulario para añadir entrenamiento"""
        st.subheader("Nuevo Entrenamiento")
        
        training_service = self.training_controller.training_service
        categories = training_service.get_sport_categories()
        emojis = {
            'deporte_equipo': '🏀', 'deporte_raqueta': '🎾', 'deporte_acuatico': '🏊‍♂️',
            'deporte_invierno': '⛷️', 'deporte_combate': '🥊', 'deporte_resistencia': '🏃‍♂️',
            'deporte_fuerza': '💪', 'deporte_aventura': '🧗‍♂️', 'deporte_baile': '💃',
            'deporte_precision': '🎯', 'fitness': '🧘‍♀️', 'ejercicio_fuerza': '🏋️',
            'actividad_diaria': '🚶‍♂️', 'deporte_extremo': '🪂', 'deporte_motor': '🏍️',
            'deporte_tradicional': '🏺', 'deporte_acuatico_extremo': '🏄‍♂️', 'deporte_invierno_extremo': '🎿'
        }
        category_names = {k: f"{v} {k.replace('_', ' ').title()}" for k, v in emojis.items()}
        
        # Agregar opción vacía para simular placeholder
        category_options = [''] + ['Todas'] + list(categories.keys())
        selected_category = st.selectbox(
            "🏷️ Categoría de Deporte:",
            options=category_options,
            format_func=lambda x: "Escoge una categoría" if x == '' else (category_names.get(x, x) if x != 'Todas' else 'Todas'),
            index=st.session_state.get('training_category_index', 1),  # Usar session_state
            key="training_category_selector"
        )
        
        all_sports = training_service.get_all_sports()
        # Solo mostrar deportes si se seleccionó una categoría válida
        if selected_category and selected_category != '':
            available_sports = all_sports if selected_category == 'Todas' else [
                sport for sport in all_sports if sport['category'] == selected_category
            ]
        else:
            available_sports = []
        
        if available_sports:
            sport_options = {f"{sport['name']}": sport['key'] for sport in available_sports}
            # Agregar opción vacía para simular placeholder
            sport_options_list = [''] + list(sport_options.keys())
            selected_sport_key = st.selectbox(
                "🏃‍♂️ Selecciona el Deporte:",
                options=sport_options_list,
                format_func=lambda x: "Escoge un deporte" if x == '' else x,
                help="Selecciona el deporte que realizaste",
                key="training_sport_selector"
            )
            # Solo obtener el deporte si se seleccionó uno válido
            if selected_sport_key and selected_sport_key in sport_options:
                selected_sport = sport_options[selected_sport_key]
            else:
                selected_sport = ""
        else:
            selected_sport = ""
            st.warning("No hay deportes disponibles en esta categoría")
        
        # Usar text_input con validación para simular placeholder
        minutes_input = st.text_input("⏱️ Minutos", value=st.session_state.get('training_minutes', ''), placeholder="Introduce el tiempo", help="Valor entre 1 y 1440 minutos", key="training_minutes_input")
        
        # Mostrar mensaje de éxito si existe
        if 'training_success_shown' in st.session_state:
            if selected_sport and selected_sport in training_service.sports_database:
                sport_data = training_service.sports_database[selected_sport]
                calories_burned = round((sport_data['met'] * user_weight * minutes) / 60)
                st.success(f"✅ Entrenamiento añadido exitosamente! Has quemado {calories_burned} calorías.")
            else:
                st.success("✅ Entrenamiento añadido exitosamente!")
            
            # Limpiar el mensaje después de mostrarlo
            del st.session_state['training_success_shown']
        
        # Validar y convertir el input
        try:
            if minutes_input and minutes_input.strip():
                minutes = int(minutes_input)
                if minutes < 1 or minutes > 1440:
                    st.error("Los minutos deben estar entre 1 y 1440")
                    minutes = 30
            else:
                minutes = 30
        except ValueError:
            st.error("Por favor introduce un número válido")
            minutes = 30
        
        if selected_sport and selected_sport in training_service.sports_database:
            sport_data = training_service.sports_database[selected_sport]
            st.info(f"📊 **{sport_data['name']}** - {sport_data['category']}")
            user_weight = st.session_state.get('user_weight', 70.0)
            estimated_calories = round((sport_data['met'] * user_weight * minutes) / 60)
        
        if st.button("🏃‍♂️ Añadir Entrenamiento", type="primary"):
            if selected_sport and minutes:
                user_weight = st.session_state.get('user_weight', 70.0)
                result = self.training_controller.add_training(selected_sport, minutes, user_weight)
                if result['success']:
                    # Marcar que se mostró el mensaje de éxito
                    st.session_state['training_success_shown'] = True
                    
                    # Limpiar campos del formulario
                    st.session_state['training_category_index'] = 1  # 'Todas'
                    st.session_state['training_minutes'] = ''
                    
                    # Hacer rerun para limpiar los campos visualmente
                    st.rerun()
                else:
                    st.error(result['message'])
            else:
                st.warning("Por favor selecciona un deporte y especifica los minutos")
        
        st.divider()
        st.markdown("**📊 Estadísticas de la Base de Datos:**")
        total_sports = len(training_service.sports_database)
        total_categories = len(categories)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Deportes", total_sports)
        with col2:
            st.metric("Total Categorías", total_categories)
    
    def _render_calories_chart(self):
        """Renderizar gráfica de calorías consumidas vs quemadas"""
        today = date.today()
        today_display = format_date_display(today)
        if today_display == "hoy":
            st.subheader(f"📊 Balance Calórico de {today_display}")
        else:
            st.subheader(f"📊 Balance Calórico del {today_display}")
        today_str = today.strftime('%Y-%m-%d')
        
        nutrition_stats = self.nutrition_controller.get_nutrition_stats(today_str)
        training_stats = self.training_controller.get_training_stats(today_str)
        
        if nutrition_stats['success'] and training_stats['success']:
            calories_consumed = nutrition_stats['data']['calories']
            calories_burned = training_stats['data']['total_calories_burned']
            
            # Solo mostrar gráfico y balance si hay datos reales (no solo comidas recién añadidas)
            if calories_consumed > 0 or calories_burned > 0:
                fig = go.Figure(data=[
                    go.Bar(name='Consumidas', x=['Calorías'], y=[calories_consumed], marker_color='#45B7D1'),
                    go.Bar(name='Quemadas', x=['Calorías'], y=[calories_burned], marker_color='#FF6B6B')
                ])
                fig.update_layout(
                    title=f"Calorías de {today_display}" if today_display == "hoy" else f"Calorías del {today_display}",
                    barmode='group',
                    height=config.CHART_HEIGHT,
                    showlegend=True
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos para mostrar")
        else:
            st.info("No hay datos para mostrar")
    
    def _render_macros_section(self):
        """Renderizar sección de macronutrientes"""
        self._render_macros_chart()
    
    def _render_daily_stats(self):
        """Renderizar estadísticas del día"""
        today = date.today()
        today_display = format_date_display(today)
        if today_display == "hoy":
            st.subheader(f"📈 Estadísticas de {today_display}")
        else:
            st.subheader(f"📈 Estadísticas del {today_display}")
        today_str = today.strftime('%Y-%m-%d')
        
        nutrition_stats = self.nutrition_controller.get_nutrition_stats(today_str)
        if nutrition_stats['success']:
            data = nutrition_stats['data']
            st.metric("Calorías Consumidas", f"{data['calories']} cal")
            st.metric("Proteínas", f"{data['proteins']:.1f}g")
            st.metric("Carbohidratos", f"{data['carbs']:.1f}g")
            st.metric("Grasas", f"{data['fats']:.1f}g")
        
        training_stats = self.training_controller.get_training_stats(today_str)
        if training_stats['success']:
            data = training_stats['data']
            st.metric("Calorías Quemadas", f"{data['total_calories_burned']} cal")
            st.metric("Minutos Activo", f"{data['total_minutes']} min")
    
    def _render_recent_records(self):
        """Renderizar registros con selector de fecha"""
        st.subheader("📋 Registros por Fecha")
        col1, col2 = st.columns([1, 3])
        with col1:
            selected_date = st.date_input(
                "📅 Fecha:",
                value=date.today(),
                key="date_selector",
                format="DD/MM/YYYY",
                label_visibility="collapsed"
            )
        with col2:
            st.write("")
        
        date_str = selected_date.strftime('%Y-%m-%d')
        meals_by_date = self.nutrition_controller.get_meals_by_date(date_str)
        trainings_by_date = self.training_controller.get_trainings_by_date(date_str)
        
        tab1, tab2, tab3 = st.tabs(["⚖️ Balance", "🍽️ Comidas", "💪 Entrenamientos"])
        with tab1:
            self._render_balance_tab(selected_date)
        with tab2:
            self._render_meals_table(meals_by_date, selected_date)
        with tab3:
            self._render_trainings_table(trainings_by_date, selected_date)
    
    def _render_balance_tab(self, selected_date):
        """Renderizar pestaña de balance calórico del día"""
        date_str = selected_date.strftime('%Y-%m-%d')
        
        # Obtener estadísticas del día seleccionado
        nutrition_stats = self.nutrition_controller.get_nutrition_stats(date_str)
        training_stats = self.training_controller.get_training_stats(date_str)
        
        date_display = format_date_display(selected_date)
        if date_display == "hoy":
            st.subheader(f"⚖️ Balance Calórico de {date_display}")
        else:
            st.subheader(f"⚖️ Balance Calórico del {date_display}")
        
        if nutrition_stats['success'] and training_stats['success']:
            calories_consumed = nutrition_stats['data']['calories']
            calories_burned = training_stats['data']['total_calories_burned']
            
            # Calcular balance
            balance = calories_consumed - calories_burned
            
            # Crear columnas para mostrar la información
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "🔥 Calorías Consumidas",
                    f"{calories_consumed} cal",
                    help="Total de calorías ingeridas en el día"
                )
            
            with col2:
                st.metric(
                    "🏃‍♂️ Calorías Quemadas",
                    f"{calories_burned} cal",
                    help="Total de calorías quemadas en entrenamientos"
                )
            
            with col3:
                # Determinar color y símbolo del balance
                if balance > 0:
                    balance_color = "🔴"  # Rojo para superávit
                    balance_text = f"+{balance} cal"
                    balance_help = "Superávit calórico (ganancia de peso)"
                elif balance < 0:
                    balance_color = "🟢"  # Verde para déficit
                    balance_text = f"{balance} cal"
                    balance_help = "Déficit calórico (pérdida de peso)"
                else:
                    balance_color = "🟡"  # Amarillo para equilibrio
                    balance_text = "0 cal"
                    balance_help = "Equilibrio calórico (mantenimiento de peso)"
                
                st.metric(
                    f"{balance_color} Balance del Día",
                    balance_text,
                    help=balance_help
                )
             
            # Solo mostrar las métricas principales, sin gráfico ni mensajes adicionales
        else:
            st.warning("📊 No hay suficientes datos para mostrar el balance calórico")
            if not nutrition_stats['success']:
                st.info("💡 Añade comidas para ver las calorías consumidas")
            if not training_stats['success']:
                st.info("💡 Añade entrenamientos para ver las calorías quemadas")
    
    def _render_meals_table(self, meals_result, selected_date):
        """Renderizar tabla de comidas con botones de borrar"""
        if meals_result['success'] and meals_result['data']:
            date_display = format_date_display(selected_date)
            if date_display == "hoy":
                st.info(f"🍽️ Comidas de {date_display} ({len(meals_result['data'])} registros)")
            else:
                st.info(f"🍽️ Comidas del {date_display} ({len(meals_result['data'])} registros)")
            meals_df = pd.DataFrame(meals_result['data'])
            meals_display = meals_df[['id', 'food', 'grams', 'calories', 'proteins', 'carbs', 'fats', 'created_at']].copy()
            meals_display.columns = ['ID', 'Alimento', 'Gramos', 'Calorías', 'Proteínas', 'Carbohidratos', 'Grasas', 'Hora']
            meals_display['Hora'] = pd.to_datetime(meals_df['created_at']).dt.strftime('%H:%M')
            
            for idx, row in meals_df.iterrows():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"🍽️ **{row['food']}** - {row['grams']}g - {row['calories']} cal - {row['proteins']}g prot - {pd.to_datetime(row['created_at']).strftime('%H:%M')}")
                with col2:
                    if st.button("🗑️", key=f"delete_meal_{row['id']}", help="Borrar comida"):
                        result = self.nutrition_controller.delete_meal(row['id'])
                        if result['success']:
                            st.success("Comida eliminada")
                            st.rerun()
                        else:
                            st.error(result['message'])
        else:
            date_display = format_date_display(selected_date)
            if date_display == "hoy":
                st.info(f"📭 No hay comidas registradas para {date_display}")
            else:
                st.info(f"📭 No hay comidas registradas para el {date_display}")
    
    def _render_trainings_table(self, trainings_result, selected_date):
        """Renderizar tabla de entrenamientos con botones de borrar"""
        if trainings_result['success'] and trainings_result['data']:
            date_display = format_date_display(selected_date)
            if date_display == "hoy":
                st.info(f"💪 Entrenamientos de {date_display} ({len(trainings_result['data'])} registros)")
            else:
                st.info(f"💪 Entrenamientos del {date_display} ({len(trainings_result['data'])} registros)")
            trainings_df = pd.DataFrame(trainings_result['data'])
            
            for idx, row in trainings_df.iterrows():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"💪 **{row['activity']}** - {row['minutes']} min - {row['calories_burned']} cal - {pd.to_datetime(row['created_at']).strftime('%H:%M')}")
                with col2:
                    if st.button("🗑️", key=f"delete_training_{row['id']}", help="Borrar entrenamiento"):
                        result = self.training_controller.delete_training(row['id'])
                        if result['success']:
                            st.success("Entrenamiento eliminado")
                            st.rerun()
                        else:
                            st.error(result['message'])
        else:
            date_display = format_date_display(selected_date)
            if date_display == "hoy":
                st.info(f"📭 No hay entrenamientos registrados para {date_display}")
            else:
                st.info(f"📭 No hay entrenamientos registrados para el {date_display}")
    
    def _render_macros_chart(self):
        """Renderizar gráfica de macronutrientes con recomendaciones"""
        st.subheader("🥗 Macronutrientes")
        
        # Mostrar mensaje de éxito si existe
        if 'objetivo_updated' in st.session_state and st.session_state.objetivo_updated:
            st.success("✅ Objetivo actualizado correctamente")
            # Limpiar del session_state
            del st.session_state.objetivo_updated
        
        # Obtener objetivo del session_state (ya cargado)
        user_profile = st.session_state.get('user_profile', {})
        saved_objetivo = user_profile.get('objetivo', 'mantener_peso')
        
        # Selector de objetivo con persistencia en BD
        objetivo = st.selectbox(
            "🎯 ¿Cuál es tu objetivo principal?",
            options=[
                "mantener_peso",
                "perdida_grasa",
                "ganancia_musculo",
                "resistencia_cardio",
                "fuerza_maxima"
            ],
            index=[
                "mantener_peso",
                "perdida_grasa",
                "ganancia_musculo",
                "resistencia_cardio",
                "fuerza_maxima"
            ].index(saved_objetivo),
            format_func=lambda x: {
                "mantener_peso": "⚖️ Mantener peso actual",
                "perdida_grasa": "🔥 Pérdida de grasa",
                "ganancia_musculo": "💪 Ganancia de músculo",
                "resistencia_cardio": "🏃‍♂️ Resistencia y cardio",
                "fuerza_maxima": "🏋️ Fuerza máxima"
            }[x],
            help="Selecciona tu objetivo para ver recomendaciones personalizadas",
            key="objetivo_selector"
        )
        
        # Guardar el objetivo en la base de datos si cambió
        if objetivo != saved_objetivo:
            # Usar perfil del session_state (ya cargado)
            current_data = st.session_state.get('user_profile', {})
            # Mantener los datos existentes y añadir/actualizar el objetivo
            result = self.user_controller.save_profile(
                current_data.get('name', ''),
                current_data.get('weight', 70.0),
                objetivo
            )
            if result['success']:
                # Actualizar el perfil en session_state
                st.session_state['user_profile']['objetivo'] = objetivo
                # Guardar mensaje en session_state para mostrarlo en el siguiente render
                st.session_state.objetivo_updated = True
                st.rerun()
            else:
                st.error(f"❌ Error al guardar objetivo: {result['message']}")
        
        today = date.today().strftime('%Y-%m-%d')
        nutrition_stats = self.nutrition_controller.get_nutrition_stats(today)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Distribución Actual**")
            if nutrition_stats['success']:
                data = nutrition_stats['data']
                fig_actual = go.Figure(data=[go.Pie(
                    labels=['Proteínas', 'Carbohidratos', 'Grasas'],
                    values=[data['proteins'], data['carbs'], data['fats']],
                    hole=0.4,
                    marker_colors=['#FF6B6B', '#FFD93D', '#45B7D1'],
                    textinfo='percent',
                    textposition='outside'
                )])
                fig_actual.update_layout(
                    title=f"Consumido el {format_date(date.today())}",
                    height=300,
                    showlegend=True
                )
                st.plotly_chart(fig_actual, use_container_width=True)
            else:
                st.info(f"No hay datos nutricionales para el {format_date(date.today())}")
        
        with col2:
            st.markdown("**🎯 Distribución Recomendada**")
            recomendacion = self._get_macro_recommendation(objetivo)
            
            # Crear gráfica de dona para recomendaciones con rangos exactos
            # Usar valores que suman 100% para que el gráfico se vea completo
            fig_recomendado = go.Figure(data=[go.Pie(
                labels=[
                    recomendacion["protein"],
                    recomendacion["carbs"],
                    recomendacion["fat"]
                ],
                values=[25, 50, 25],  # Valores fijos que suman 100% para mostrar distribución visual correcta
                hole=0.4,
                marker_colors=['#FF6B6B', '#FFD93D', '#45B7D1'],
                textinfo='percent',  # Mostrar porcentajes en lugar de nombres
                textposition='outside'
            )])
            
            fig_recomendado.update_layout(
                title=f"Recomendado: {recomendacion['nombre']}",
                height=300,
                showlegend=False  # Ocultar leyenda para evitar duplicación
            )
            
            st.plotly_chart(fig_recomendado, use_container_width=True)
    
    def _get_macro_recommendation(self, objetivo):
        """Obtener recomendaciones de macronutrientes según el objetivo"""
        recomendaciones = {
            "mantener_peso": {
                "nombre": "Mantener Peso",
                "protein": "15-25%",
                "carbs": "45-55%",
                "fat": "25-35%"
            },
            "perdida_grasa": {
                "nombre": "Pérdida de Grasa",
                "protein": "25-35%",
                "carbs": "30-40%",
                "fat": "25-30%"
            },
            "ganancia_musculo": {
                "nombre": "Ganancia de Músculo",
                "protein": "20-30%",
                "carbs": "45-55%",
                "fat": "20-30%"
            },
            "resistencia_cardio": {
                "nombre": "Resistencia y Cardio",
                "protein": "15-20%",
                "carbs": "55-65%",
                "fat": "20-25%"
            },
            "fuerza_maxima": {
                "nombre": "Fuerza Máxima",
                "protein": "25-30%",
                "carbs": "40-50%",
                "fat": "20-30%"
            }
        }
        return recomendaciones.get(objetivo, recomendaciones["mantener_peso"])

