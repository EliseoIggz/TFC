# Fitness Tracker - Vista del Dashboard
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
        
        st.set_page_config(
            page_title=config.STREAMLIT_TITLE,
            layout=config.STREAMLIT_LAYOUT,
            initial_sidebar_state=config.STREAMLIT_SIDEBAR_STATE
        )
    
    def render(self):
        """Renderizar el dashboard completo"""
        st.title("🏃‍♂️ Fitness Tracker")
        st.markdown("**Seguimiento de entrenamientos y nutrición**")
        
        profile = self.user_controller.get_profile()
        if profile['success']:
            st.session_state['user_name'] = profile['data']['name']
            st.session_state['user_weight'] = profile['data']['weight']
        
        user_name = st.session_state.get('user_name', '')
        user_weight = st.session_state.get('user_weight', 70.0)
        
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
                # Limpiar el mensaje después de 5 segundos
                import time
                if 'profile_timer' not in st.session_state:
                    st.session_state.profile_timer = time.time()
                elif time.time() - st.session_state.profile_timer > 5:
                    del st.session_state.profile_updated
                    del st.session_state.profile_timer
            
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
            self._render_quick_favorites()
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
                        st.success(result['message'])
                        st.rerun()
                    elif result.get('multiple_options'):
                        st.session_state.food_options = result['options_data']
                        st.rerun()
                    else:
                        st.error(result['message'])
                else:
                    st.warning("Por favor completa todos los campos")
    
    def _render_quick_favorites(self):
        """Renderizar comidas favoritas para acceso rápido"""
        favorites_result = self.nutrition_controller.get_food_favorites()
        
        if favorites_result['success'] and favorites_result['data']:
            favorites = favorites_result['data'][:15]
            with st.expander(f"⭐ Comidas Favoritas ({len(favorites)}/15)", expanded=False):
                st.info("Haz clic en un favorito para añadirlo automáticamente")
                cols = st.columns(2)
                for i, favorite in enumerate(favorites):
                    col_idx = i % 2
                    with cols[col_idx]:
                        if st.button(
                            f"🍽️ {favorite['display_name']}",
                            key=f"quick_fav_{favorite['id']}",
                            help=f"Calorías: {favorite['calories_per_100g']} cal/100g"
                        ):
                            result = self.nutrition_controller.quick_add_from_favorite(favorite['id'], 100)
                            if result['success']:
                                st.success(f"✅ {favorite['display_name']} añadido (100g)")
                                st.rerun()
                            else:
                                st.error(f"Error: {result['message']}")
                        st.caption(f"{favorite['calories_per_100g']} cal/100g")
                
                if len(favorites_result['data']) > 15:
                    st.info(f"💡 Mostrando los primeros 15 de {len(favorites_result['data'])} favoritos")
        else:
            st.info("💡 No tienes comidas favoritas aún. ¡Añade algunas desde la búsqueda!")
    
    def _render_quick_exercise_favorites(self):
        """Renderizar ejercicios favoritos para acceso rápido"""
        favorites_result = self.training_controller.get_exercise_favorites()
        
        if favorites_result['success'] and favorites_result['data']:
            favorites = favorites_result['data'][:10]
            with st.expander(f"⭐ Ejercicios Favoritos ({len(favorites)}/10)", expanded=False):
                st.info("Haz clic en un favorito para añadirlo automáticamente")
                cols = st.columns(2)
                for i, favorite in enumerate(favorites):
                    col_idx = i % 2
                    with cols[col_idx]:
                        if st.button(
                            f"💪 {favorite['activity_name']}",
                            key=f"quick_ex_fav_{favorite['id']}",
                            help=f"MET: {favorite['met_value']} - 30 min por defecto"
                        ):
                            user_weight = st.session_state.get('user_weight', 70.0)
                            result = self.training_controller.quick_add_from_favorite(favorite['id'], 30, user_weight)
                            if result['success']:
                                st.success(f"✅ {favorite['activity_name']} añadido (30 min)")
                                st.rerun()
                            else:
                                st.error(f"Error: {result['message']}")
                        st.caption(f"MET: {favorite['met_value']} - {favorite['category']}")
                
                if len(favorites_result['data']) > 10:
                    st.info(f"💡 Mostrando los primeros 10 de {len(favorites_result['data'])} favoritos")
        else:
            st.info("💡 No tienes ejercicios favoritos aún. ¡Añade algunos desde el formulario!")
    
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
                if 'fdc_id' in selected_option and selected_option['fdc_id'] != 'Sin ID':
                    st.info(f"🆔 **FDC ID:** {selected_option['fdc_id']}")
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
            
            if 'original_name' in selected_option and selected_option['original_name'] != selected_option['name']:
                st.info(f"🌐 **Nombre original:** {selected_option['original_name']}")
            
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
                    st.rerun()
                else:
                    st.error(result['message'])
            
            st.divider()
            col1, col2 = st.columns([1, 1])
            
            with col1:
                is_favorite = self.nutrition_controller.is_food_favorite(selected_option['name'], selected_option['display_name'])
                if is_favorite:
                    st.success("⭐ Ya está en favoritos")
                elif st.button("⭐ Añadir a Favoritos", key=f"add_fav_{selected_index}"):
                    food_data = {
                        'name': selected_option['name'],
                        'display_name': selected_option['display_name'],
                        'calories_per_100g': selected_option['calories_per_100g'],
                        'proteins_per_100g': selected_option.get('proteins_per_100g', 0),
                        'carbs_per_100g': selected_option.get('carbs_per_100g', 0),
                        'fats_per_100g': selected_option.get('fats_per_100g', 0),
                        'brand_owner': selected_option.get('brand_owner', ''),
                        'category': selected_option.get('category', ''),
                        'fdc_id': selected_option.get('fdc_id', ''),
                        'data_type': selected_option.get('data_type', '')
                    }
                    result = self.nutrition_controller.add_food_favorite(food_data)
                    if result['success']:
                        st.success("⭐ Añadido a favoritos")
                        st.rerun()
                    else:
                        st.error(f"Error: {result['message']}")
            
            with col2:
                st.write("")
    
    def _render_training_form(self):
        """Renderizar formulario para añadir entrenamiento"""
        st.subheader("Nuevo Entrenamiento")
        self._render_quick_exercise_favorites()
        
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
        
        selected_category = st.selectbox(
            "🏷️ Categoría de Deporte:",
            options=['Todas'] + list(categories.keys()),
            format_func=lambda x: category_names.get(x, x) if x != 'Todas' else 'Todas'
        )
        
        all_sports = training_service.get_all_sports()
        available_sports = all_sports if selected_category == 'Todas' else [
            sport for sport in all_sports if sport['category'] == selected_category
        ]
        
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
        
        minutes = st.number_input("⏱️ Minutos", min_value=1, max_value=1440, value=30)
        
        if selected_sport and selected_sport in training_service.sports_database:
            sport_data = training_service.sports_database[selected_sport]
            st.info(f"📊 **{sport_data['name']}**: {sport_data['met']} MET - {sport_data['category']}")
            user_weight = st.session_state.get('user_weight', 70.0)
            estimated_calories = round((sport_data['met'] * user_weight * minutes) / 60)
            st.success(f"🔥 Calorías estimadas: {estimated_calories} cal en {minutes} min (peso: {user_weight} kg)")
            
            if user_weight != 70.0:
                default_calories = round((sport_data['met'] * 70 * minutes) / 60)
                difference = estimated_calories - default_calories
                if difference != 0:
                    st.info(f"📊 Diferencia con peso por defecto (70kg): {difference:+d} cal")
            
            st.divider()
            col1, col2 = st.columns([1, 1])
            
            with col1:
                is_favorite = self.training_controller.is_exercise_favorite(selected_sport)
                if is_favorite:
                    st.success("⭐ Ya está en favoritos")
                elif st.button("⭐ Añadir a Favoritos", key=f"add_ex_fav_{selected_sport}"):
                    exercise_data = {
                        'name': sport_data['name'],
                        'key': selected_sport,
                        'met': sport_data['met'],
                        'category': sport_data['category']
                    }
                    result = self.training_controller.add_exercise_favorite(exercise_data)
                    if result['success']:
                        st.success("⭐ Añadido a favoritos")
                        st.rerun()
                    else:
                        st.error(f"Error: {result['message']}")
            
            with col2:
                st.write("")
        
        if st.button("🏃‍♂️ Añadir Entrenamiento", type="primary"):
            if selected_sport and minutes:
                user_weight = st.session_state.get('user_weight', 70.0)
                result = self.training_controller.add_training(selected_sport, minutes, user_weight)
                if result['success']:
                    st.success(result['message'])
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
        st.subheader("📊 Balance Calórico")
        today = date.today().strftime('%Y-%m-%d')
        
        nutrition_stats = self.nutrition_controller.get_nutrition_stats(today)
        training_stats = self.training_controller.get_training_stats(today)
        
        if nutrition_stats['success'] and training_stats['success']:
            calories_consumed = nutrition_stats['data']['calories']
            calories_burned = training_stats['data']['total_calories_burned']
            
            fig = go.Figure(data=[
                go.Bar(name='Consumidas', x=['Calorías'], y=[calories_consumed], marker_color='#FF6B6B'),
                go.Bar(name='Quemadas', x=['Calorías'], y=[calories_burned], marker_color='#4ECDC4')
            ])
            fig.update_layout(
                title="Calorías del Día",
                barmode='group',
                height=config.CHART_HEIGHT,
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
            balance = calories_consumed - calories_burned
            if balance > 0:
                st.info(f"Balance: +{balance} calorías (superávit)")
            elif balance < 0:
                st.success(f"Balance: {balance} calorías (déficit)")
            else:
                st.success("Balance: 0 calorías (equilibrio)")
        else:
            st.info("No hay datos para mostrar")
    
    def _render_macros_section(self):
        """Renderizar sección de macronutrientes"""
        self._render_macros_chart()
    
    def _render_daily_stats(self):
        """Renderizar estadísticas del día"""
        st.subheader("📈 Estadísticas del Día")
        today = date.today().strftime('%Y-%m-%d')
        
        nutrition_stats = self.nutrition_controller.get_nutrition_stats(today)
        if nutrition_stats['success']:
            data = nutrition_stats['data']
            st.metric("Calorías Consumidas", f"{data['calories']} cal")
            st.metric("Proteínas", f"{data['proteins']:.1f}g")
            st.metric("Carbohidratos", f"{data['carbs']:.1f}g")
            st.metric("Grasas", f"{data['fats']:.1f}g")
        
        training_stats = self.training_controller.get_training_stats(today)
        if training_stats['success']:
            data = training_stats['data']
            st.metric("Calorías Quemadas", f"{data['total_calories_burned']} cal")
            st.metric("Minutos Activo", f"{data['total_minutes']} min")
    
    def _render_recent_records(self):
        """Renderizar registros con selector de fecha"""
        st.subheader("📋 Registros por Fecha")
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
        
        date_str = selected_date.strftime('%Y-%m-%d')
        meals_by_date = self.nutrition_controller.get_meals_by_date(date_str)
        trainings_by_date = self.training_controller.get_trainings_by_date(date_str)
        
        tab1, tab2 = st.tabs(["🍽️ Comidas", "💪 Entrenamientos"])
        with tab1:
            self._render_meals_table(meals_by_date, selected_date)
        with tab2:
            self._render_trainings_table(trainings_by_date, selected_date)
    
    def _render_meals_table(self, meals_result, selected_date):
        """Renderizar tabla de comidas con botones de borrar"""
        if meals_result['success'] and meals_result['data']:
            st.info(f"🍽️ Comidas del {selected_date.strftime('%d/%m/%Y')} ({len(meals_result['data'])} registros)")
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
            st.info(f"📭 No hay comidas registradas para el {selected_date.strftime('%d/%m/%Y')}")
    
    def _render_trainings_table(self, trainings_result, selected_date):
        """Renderizar tabla de entrenamientos con botones de borrar"""
        if trainings_result['success'] and trainings_result['data']:
            st.info(f"💪 Entrenamientos del {selected_date.strftime('%d/%m/%Y')} ({len(trainings_result['data'])} registros)")
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
            st.info(f"📭 No hay entrenamientos registrados para el {selected_date.strftime('%d/%m/%Y')}")
    
    def _render_macros_chart(self):
        """Renderizar gráfica de macronutrientes con recomendaciones"""
        st.subheader("🥗 Macronutrientes")
        
        # Mostrar mensaje de éxito si existe
        if 'objetivo_updated' in st.session_state and st.session_state.objetivo_updated:
            st.success("✅ Objetivo actualizado correctamente")
            # Limpiar el mensaje después de 5 segundos
            import time
            if 'objetivo_timer' not in st.session_state:
                st.session_state.objetivo_timer = time.time()
            elif time.time() - st.session_state.objetivo_timer > 5:
                del st.session_state.objetivo_updated
                del st.session_state.objetivo_timer
        
        # Obtener objetivo guardado en la base de datos
        profile = self.user_controller.get_profile()
        saved_objetivo = 'mantener_peso'  # valor por defecto
        
        if profile['success'] and 'objetivo' in profile['data']:
            saved_objetivo = profile['data']['objetivo']
        
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
            # Actualizar el perfil con el nuevo objetivo
            current_profile = self.user_controller.get_profile()
            if current_profile['success']:
                current_data = current_profile['data']
                # Mantener los datos existentes y añadir/actualizar el objetivo
                result = self.user_controller.save_profile(
                    current_data.get('name', ''),
                    current_data.get('weight', 70.0),
                    objetivo
                )
                if result['success']:
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
                    marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1'],
                    textinfo='percent',
                    textposition='outside'
                )])
                fig_actual.update_layout(
                    title="Consumido Hoy",
                    height=300,
                    showlegend=True
                )
                st.plotly_chart(fig_actual, use_container_width=True)
            else:
                st.info("No hay datos nutricionales para hoy")
        
        with col2:
            st.markdown("**🎯 Distribución Recomendada**")
            recomendacion = self._get_macro_recommendation(objetivo)
            
            # Convertir rangos a valores promedio para el gráfico
            def extract_average_from_range(range_str):
                """Extraer valor promedio de un rango como '15-25%'"""
                range_str = range_str.replace('%', '')
                if '-' in range_str:
                    min_val, max_val = range_str.split('-')
                    return (float(min_val) + float(max_val)) / 2
                else:
                    return float(range_str)
            
            protein_avg = extract_average_from_range(recomendacion['protein'])
            carbs_avg = extract_average_from_range(recomendacion['carbs'])
            fat_avg = extract_average_from_range(recomendacion['fat'])
            
            # Crear gráfica de dona para recomendaciones
            fig_recomendado = go.Figure(data=[go.Pie(
                labels=[
                    f'Proteínas ({recomendacion["protein"]})',
                    f'Carbohidratos ({recomendacion["carbs"]})',
                    f'Grasas ({recomendacion["fat"]})'
                ],
                values=[protein_avg, carbs_avg, fat_avg],
                hole=0.4,
                marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1'],
                textinfo='percent',
                textposition='outside'
            )])
            
            fig_recomendado.update_layout(
                title=f"Recomendado: {recomendacion['nombre']}",
                height=300,
                showlegend=True
            )
            
            st.plotly_chart(fig_recomendado, use_container_width=True)
    
    def _render_food_favorites(self):
        """Renderizar lista de comidas favoritas"""
        st.subheader("🍽️ Comidas Favoritas")
        favorites_result = self.nutrition_controller.get_food_favorites()
        
        if favorites_result['success'] and favorites_result['data']:
            favorites = favorites_result['data']
            st.info(f"Tienes {len(favorites)} comidas favoritas")
            
            for favorite in favorites:
                with st.expander(f"🍽️ {favorite['display_name']}"):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**Calorías:** {favorite['calories_per_100g']} cal/100g")
                        if favorite['proteins_per_100g']:
                            st.write(f"**Proteínas:** {favorite['proteins_per_100g']}g/100g")
                        if favorite['carbs_per_100g']:
                            st.write(f"**Carbohidratos:** {favorite['carbs_per_100g']}g/100g")
                        if favorite['fats_per_100g']:
                            st.write(f"**Grasas:** {favorite['fats_per_100g']}g/100g")
                        if favorite['brand_owner']:
                            st.write(f"**Marca:** {favorite['brand_owner']}")
                        if favorite['category']:
                            st.write(f"**Categoría:** {favorite['category']}")
                        st.caption(f"Usado {favorite['usage_count']} veces")
                    
                    with col2:
                        grams = st.number_input(
                            "Gramos:",
                            min_value=1,
                            max_value=1000,
                            value=100,
                            key=f"fav_grams_{favorite['id']}"
                        )
                    
                    with col3:
                        if st.button("➕ Añadir", key=f"quick_add_fav_{favorite['id']}"):
                            result = self.nutrition_controller.quick_add_from_favorite(favorite['id'], grams)
                            if result['success']:
                                st.success(result['message'])
                                st.rerun()
                            else:
                                st.error(result['message'])
                        if st.button("🗑️", key=f"remove_fav_{favorite['id']}"):
                            result = self.nutrition_controller.remove_food_favorite(favorite['id'])
                            if result['success']:
                                st.success("Eliminado de favoritos")
                                st.rerun()
                            else:
                                st.error(result['message'])
        else:
            st.info("No tienes comidas favoritas aún. ¡Añade algunas desde la búsqueda!")
    
    def _render_exercise_favorites(self):
        """Renderizar lista de ejercicios favoritos"""
        st.subheader("💪 Ejercicios Favoritos")
        favorites_result = self.training_controller.get_exercise_favorites()
        
        if favorites_result['success'] and favorites_result['data']:
            favorites = favorites_result['data']
            st.info(f"Tienes {len(favorites)} ejercicios favoritos")
            
            for favorite in favorites:
                with st.expander(f"💪 {favorite['activity_name']}"):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**MET:** {favorite['met_value']}")
                        st.write(f"**Categoría:** {favorite['category']}")
                        user_weight = st.session_state.get('user_weight', 70.0)
                        estimated_calories_30min = round((favorite['met_value'] * user_weight * 30) / 60)
                        st.write(f"**30 min:** ~{estimated_calories_30min} cal")
                        st.caption(f"Usado {favorite['usage_count']} veces")
                    
                    with col2:
                        minutes = st.number_input(
                            "Minutos:",
                            min_value=1,
                            max_value=180,
                            value=30,
                            key=f"fav_minutes_{favorite['id']}"
                        )
                    
                    with col3:
                        if st.button("➕ Añadir", key=f"quick_add_ex_fav_{favorite['id']}"):
                            result = self.training_controller.quick_add_from_favorite(favorite['id'], minutes, user_weight)
                            if result['success']:
                                st.success(result['message'])
                                st.rerun()
                            else:
                                st.error(result['message'])
                        if st.button("🗑️", key=f"remove_ex_fav_{favorite['id']}"):
                            result = self.training_controller.remove_exercise_favorite(favorite['id'])
                            if result['success']:
                                st.success("Eliminado de favoritos")
                                st.rerun()
                            else:
                                st.error(result['message'])
        else:
            st.info("No tienes ejercicios favoritos aún. ¡Añade algunos desde el formulario de entrenamiento!")
    
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