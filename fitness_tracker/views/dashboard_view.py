import streamlit as st
import plotly.graph_objects as go
from datetime import date
import base64
from controllers.training_controller import TrainingController
from controllers.nutrition_controller import NutritionController
from controllers.user_controller import UserController
from controllers.statistics_controller import StatisticsController
import config
from utils.helpers import format_date, format_date_display, show_success_message

class DashboardView:
    """Vista principal del dashboard"""
    
    def __init__(self):
        """Inicializar controladores"""
        self.training_controller = TrainingController()
        self.nutrition_controller = NutritionController(training_controller=self.training_controller)
        self.user_controller = UserController()
        self.statistics_controller = StatisticsController(
            nutrition_controller=self.nutrition_controller,
            training_controller=self.training_controller
        )
        
        st.set_page_config(
            page_title="Limen - Fitness Tracker",
            page_icon="./assets/images/logo_sharp.png",
            layout=config.STREAMLIT_LAYOUT,
            initial_sidebar_state=config.STREAMLIT_SIDEBAR_STATE
        )
    
    def render(self):
        """Renderizar dashboard completo"""
        self._init_user_profile()
        
        with st.sidebar:
            # Logo y título "LIMEN" uno al lado del otro, pegados al borde izquierdo
            st.markdown("""
            <div style="display: flex; align-items: center; margin-bottom: 20px; margin-left: 0;">
                <img src="data:image/png;base64,{}" width="80" style="margin-right: 15px;">
                <img src="data:image/png;base64,{}" width="120" style="margin: 0;">
            </div>
            """.format(self._get_image_base64("assets/images/logo_sharp.png"), self._get_image_base64("assets/images/title.png")), unsafe_allow_html=True)
            
            self._render_profile_form()
            self._render_input_forms()
        
        # Descripción principal en el área central
        st.markdown("**Seguimiento de entrenamientos y nutrición**")
        
        self._render_main_content()
    
    def _init_user_profile(self):
        """Inicializar perfil de usuario"""
        if 'user_profile' not in st.session_state:
            profile = self.user_controller.get_profile()
            if profile['success']:
                data = profile['data']
                st.session_state.update({
                    'user_profile': data,
                    'user_name': data['name'],
                    'user_weight': data['weight']
                })
            else:
                st.session_state.update({
                    'user_profile': {'name': '', 'weight': 70.0, 'objetivo': 'mantener_peso'},
                    'user_name': '',
                    'user_weight': 70.0
                })
    
    def _render_profile_form(self):
        """Renderizar formulario de perfil"""
        st.header("👤 Mi Perfil")
        
        # Inputs de perfil
        user_name = st.text_input("Nombre:", value=st.session_state.get('user_name', ''), 
                                 placeholder="Tu nombre", key="user_name_input")
        user_weight = st.number_input("Peso (kg):", min_value=30.0, max_value=200.0,
                                     value=st.session_state.get('user_weight', 70.0), 
                                     step=0.5, key="user_weight_input")
        
        # Guardar si hay cambios
        current_name = st.session_state.get('user_name', '')
        current_weight = st.session_state.get('user_weight', 70.0)
        
        if user_name != current_name or user_weight != current_weight:
            validation = self.user_controller.validate_profile_input(user_name, user_weight)
            if validation['valid']:
                result = self.user_controller.save_profile(user_name, user_weight)
                if result['success']:
                    st.session_state.update({
                        'user_name': user_name,
                        'user_weight': user_weight
                    })
                    st.rerun()
                else:
                    st.error(f"❌ Error al guardar: {result['message']}")
            else:
                st.error(validation['error'])
        
        # Mostrar toast solo para el dato que cambió
        self._show_profile_change_toasts(user_name)
    
    def _render_input_forms(self):
        """Renderizar formularios de entrada"""
        st.divider()
        st.header("📝 Añadir Registro")
        tab1, tab2 = st.tabs(["🍽️ Comida", "💪 Entrenamiento"])
        
        with tab1:
            self._render_meal_form()
        with tab2:
            self._render_training_form()
    
    def _render_meal_form(self):
        """Formulario de comidas"""
        st.subheader("Nueva Comida")
        
        if st.session_state.get('food_options'):
            self._render_food_selector(st.session_state.food_options)
        else:
            food = st.text_input("Alimento", placeholder="Ej: pollo, arroz, manzana...", key="food_input")
            grams = st.number_input("Gramos", min_value=1, max_value=10000, value=100, key="grams_input")
            
            if st.button("➕ Añadir Comida", type="primary", key="add_meal_button") and food and grams:
                self._process_meal_submission(food, grams)
    
    def _process_meal_submission(self, food, grams):
        """Procesar envío de comida"""
        # Mostrar búsqueda
        search_placeholder = st.empty()
        with search_placeholder.container():
            st.info(f"🔍 Buscando información nutricional para '{food}'...")
        
        # Procesar usando ViewModel
        result = self.nutrition_controller.get_meal_form_submission_result(food, grams)
        search_placeholder.empty()
        
        if result['success']:
            # Mostrar mensaje de éxito cuando se añade directamente
            show_success_message(f"{result['message']}")
            
            st.session_state.update({
                'meal_added': True,
                'meal_message': result['message']
            })
            if result.get('should_rerun'):
                st.rerun()
        elif result.get('multiple_options'):
            # Asegurar que food_options se actualice antes del rerun
            st.session_state.food_options = result.get('options_data', {})
            st.rerun()
        else:
            st.error(result['message'])
    
    def _render_food_selector(self, options_data):
        """Selector de alimentos múltiples"""
        selector_vm = self.nutrition_controller.get_food_selector_viewmodel(options_data)
        if not selector_vm['success']:
            st.error(selector_vm['error'])
            return
        
        data = selector_vm['selector_data']
        st.info(f"🔍 Se encontraron {data['options_count']} opciones para '{data['search_term']}'")
        
        # Botón cancelar - Sin limitaciones de columnas para que no se corte el texto
        if st.button("❌ Cancelar", key="cancel_food_selection"):
            self._clear_food_selection()
            st.rerun()
        
        # Selector de opciones
        select_key = f"food_selector_{data['search_term']}_{id(data['search_term'])}"
        
        selected_index = st.selectbox(
            "Selecciona el alimento:",
            options=list(range(len(data['option_labels']))),
            format_func=lambda x: data['option_labels'][x],
            key=select_key,
            help="Selecciona el alimento que quieres añadir"
        )
        
        # Mostrar detalles de la opción seleccionada
        if selected_index is not None:
            self._render_food_option_details(options_data, selected_index, data)
    
    def _render_food_option_details(self, options_data, selected_index, selector_data):
        """Mostrar detalles de opción seleccionada"""
        option = options_data['options'][selected_index]
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📦 **Producto:** {option['name']}")
        
        with col2:
            st.info(f"🔥 **Calorías:** {option['calories_per_100g']} cal/100g")
            st.info(f"⚖️ **Cantidad:** {options_data['grams']}g")
            for nutrient, emoji in [('proteins_per_100g', '🥩'), ('carbs_per_100g', '🍞'), ('fats_per_100g', '🧈')]:
                if nutrient in option:
                    name = nutrient.replace('_per_100g', '').replace('carbs', 'carbohidratos').replace('proteins', 'proteínas').replace('fats', 'grasas')
                    st.info(f"{emoji} **{name.title()}:** {option[nutrient]}g/100g")
        
        st.info(f"🧮 **Total:** {option['calories_per_100g']} cal/100g × {options_data['grams']}g")
        
        # Botón confirmar
        confirm_key = f"{selector_data['confirm_key']}_{selected_index}"
        if st.button(f"✅ Añadir {option['name']}", type="primary", key=confirm_key):
            self._process_food_selection(options_data, selected_index)
    
    def _process_food_selection(self, options_data, selected_index):
        """Procesar selección de alimento"""
        result = self.nutrition_controller.get_food_selection_result(options_data, selected_index)
        
        if result['success']:
            show_success_message(result['message'])
            if result.get('should_clear_selector'):
                self._clear_food_selection()
            st.session_state.update({
                'meal_added': True,
                'meal_message': result['message']
            })
            if result.get('should_rerun'):
                st.rerun()
        else:
            st.error(result['message'])
    
    def _clear_food_selection(self):
        """Limpiar selección de alimentos"""
        # Limpiar todas las claves relacionadas con la selección de alimentos
        keys_to_remove = ['food_options', 'food_search_term']
        for key in keys_to_remove:
            st.session_state.pop(key, None)
        
        # Limpiar claves de widgets de Streamlit
        for key in list(st.session_state.keys()):
            if key.startswith('food_selector_') or key.startswith('food_radio_'):
                del st.session_state[key]
    
    def _render_training_form(self):
        """Formulario de entrenamientos"""
        st.subheader("Nuevo Entrenamiento")
        
        user_weight = st.session_state.get('user_weight', 70.0)
        
        # Obtener ViewModel inicial
        initial_vm = self.training_controller.get_training_form_viewmodel("", "", user_weight)
        if not initial_vm['success']:
            st.error(initial_vm['error'])
            return
        
        form_data = initial_vm['form_data']
        
        # Generar claves únicas para forzar recreación de widgets
        form_counter = st.session_state.get('training_form_counter', 0)
        
        # 1. Categoría
        categories = form_data['categories']
        selected_category = st.selectbox("🏷️ Categoría de Deporte:", 
                                       options=categories['options'],
                                       format_func=categories['format_func'],
                                       index=0,  # Siempre empezar con "Todas" (primer índice)
                                       key=f"training_category_selector_{form_counter}")
        
        # 2. Deporte
        selected_sport = self._render_sport_selector(form_data['sports'], selected_category, form_counter)
        
        # 3. Minutos
        minutes_input = st.text_input("⏱️ Minutos", 
                                     value="",  # Siempre empezar vacío
                                     placeholder="Introduce el tiempo",
                                     help="Valor entre 1 y 1440 minutos",
                                     key=f"training_minutes_input_{form_counter}",
                                     autocomplete="off")
        
        # Generar ViewModel completo
        vm = self.training_controller.get_training_form_viewmodel(minutes_input, selected_sport, user_weight)
        if not vm['success']:
            st.error(vm['error'])
            return
        
        self._render_training_validation_and_submit(vm['form_data'], selected_sport, user_weight)
    
    def _render_sport_selector(self, sports_data, selected_category, form_counter=0):
        """Renderizar selector de deportes"""
        # SIEMPRE mostrar el selector de deportes
        all_sports = sports_data['all_sports']
        
        # Si la categoría es "Todas", mostrar todos los deportes
        if selected_category == 'Todas':
            available_sports = all_sports
        else:
            # Filtrar por categoría específica
            available_sports = [s for s in all_sports if s['category'] == selected_category]
        
        if not available_sports:
            st.warning("No hay deportes disponibles en esta categoría")
            return ""
        
        sport_options = {sport['name']: sport['key'] for sport in available_sports}
        sport_options_list = [''] + list(sport_options.keys())
        
        selected_sport_key = st.selectbox("🏃‍♂️ Selecciona el Deporte:",
                                        options=sport_options_list,
                                        format_func=lambda x: "Escoge un deporte" if x == '' else x,
                                        help="Selecciona el deporte que realizaste",
                                        key=f"training_sport_selector_{form_counter}")
        
        return sport_options.get(selected_sport_key, "")
    
    
    
    def _render_training_validation_and_submit(self, form_data, selected_sport, user_weight):
        """Validación y envío de entrenamiento"""
        validation = form_data['validation']
        
        # Mostrar errores
        if validation['show_error']:
            st.error(validation['error_message'])
        
        # Mostrar mensaje de éxito
        if st.session_state.get('training_success_message'):
            show_success_message(st.session_state['training_success_message'])
            del st.session_state['training_success_message']
        
        # Preview (solo mostrar si no hay mensaje de éxito)
        if form_data['preview'] and not st.session_state.get('training_success_message'):
            preview = form_data['preview']
            st.info(preview['display_text'])
            st.info(preview['calories_text'])
        
        # Botones de acción
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.button("🏃‍♂️ Añadir Entrenamiento", type="primary"):
                if validation['is_valid']:
                    result = self.training_controller.get_training_form_submission_result(
                        selected_sport, validation['minutes'], user_weight)
                    
                    if result['success']:
                        st.session_state['training_success_message'] = result['message']
                        
                        # Incrementar contador para forzar recreación de widgets
                        st.session_state.training_form_counter = st.session_state.get('training_form_counter', 0) + 1
                        
                        if result.get('should_rerun'):
                            st.rerun()
                    else:
                        st.error(result['message'])
                else:
                    if not selected_sport:
                        st.warning("❌ Por favor selecciona un deporte")
                    if not validation['minutes']:
                        st.warning("❌ Por favor especifica una cantidad válida de minutos")
        
        with col2:
            if st.button("🧹 Limpiar", help="Limpiar selectores y mensajes"):
                # Limpiar mensaje de éxito
                if 'training_success_message' in st.session_state:
                    del st.session_state['training_success_message']
                
                # Incrementar contador para forzar recreación de widgets
                st.session_state.training_form_counter = st.session_state.get('training_form_counter', 0) + 1
                
                # Forzar rerun para limpiar la interfaz
                st.rerun()
        

    
    def _render_main_content(self):
        """Contenido principal del dashboard"""
        col1, col2 = st.columns([2, 1])
        with col1:
            self._render_calories_chart()
        with col2:
            self._render_daily_stats()
        
        self._render_macros_chart()
        self._render_recent_records()
    
    def _render_calories_chart(self):
        """Gráfica de calorías"""
        today = date.today()
        today_display = format_date_display(today)
        title = f"📊 Balance Calórico de {today_display}" if today_display == "hoy" else f"📊 Balance Calórico del {today_display}"
        st.subheader(title)
        
        today_str = today.strftime('%Y-%m-%d')
        chart_data = self.statistics_controller.get_chart_data_for_date(today_str)
        
        if chart_data['success'] and chart_data['data']['has_data']:
            data = chart_data['data']
            fig = go.Figure(data=[
                go.Bar(name='Consumidas', x=['Calorías'], y=[data['calories_consumed']], marker_color='#45B7D1'),
                go.Bar(name='Quemadas', x=['Calorías'], y=[data['calories_burned']], marker_color='#FF6B6B')
            ])
            fig.update_layout(
                title=f"Calorías de {today_display}" if today_display == "hoy" else f"Calorías del {today_display}",
                barmode='group', height=config.CHART_HEIGHT, showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos para mostrar")
    
    def _render_daily_stats(self):
        """Estadísticas diarias"""
        today = date.today().strftime('%Y-%m-%d')
        daily_summary = self.statistics_controller.get_daily_summary(today)
        
        if not daily_summary['success']:
            st.error("Error al cargar estadísticas del día")
            return
        
        data = daily_summary['data']
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🍽️ Nutrición del Día**")
            nutrition_data = data['nutrition']
            for label, key in [("Calorías Consumidas", "calories_formatted"), ("Proteínas", "proteins_formatted"),
                             ("Carbohidratos", "carbs_formatted"), ("Grasas", "fats_formatted")]:
                st.metric(label, nutrition_data[key])
        
        with col2:
            st.markdown("**🏃‍♂️ Entrenamiento del Día**")
            training_data = data['training']
            st.metric("Calorías Quemadas", training_data['calories_formatted'])
            st.metric("Minutos Activo", training_data['minutes_formatted'])
    
    def _render_recent_records(self):
        """Registros por fecha"""
        st.subheader("📋 Registros por Fecha")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            selected_date = st.date_input("📅 Fecha:", value=date.today(), key="date_selector",
                                        format="DD/MM/YYYY", label_visibility="collapsed")
        
        date_str = selected_date.strftime('%Y-%m-%d')
        meals_data = self.nutrition_controller.get_meals_by_date(date_str)
        trainings_data = self.training_controller.get_trainings_by_date(date_str)
        
        tab1, tab2, tab3 = st.tabs(["⚖️ Balance", "🍽️ Comidas", "💪 Entrenamientos"])
        
        with tab1:
            self._render_balance_tab(selected_date)
        with tab2:
            self._render_table(meals_data, selected_date, 'nutrition')
        with tab3:
            self._render_table(trainings_data, selected_date, 'training')
    
    def _render_balance_tab(self, selected_date):
        """Balance calórico"""
        date_str = selected_date.strftime('%Y-%m-%d')
        balance_result = self.statistics_controller.get_daily_calories_balance(date_str)
        
        date_display = format_date_display(selected_date)
        title = f"⚖️ Balance Calórico de {date_display}" if date_display == "hoy" else f"⚖️ Balance Calórico del {date_display}"
        st.subheader(title)
        
        if balance_result['success']:
            data = balance_result['data']
            col1, col2, col3 = st.columns(3)
            
            metrics = [
                ("🔥 Calorías Consumidas", f"{data['calories_consumed']} cal", "Total de calorías ingeridas en el día"),
                ("🏃‍♂️ Calorías Quemadas", f"{data['calories_burned']} cal", "Total de calorías quemadas en entrenamientos"),
                (f"{data['balance_color']} Balance del Día", data['balance_text'], data['balance_help'])
            ]
            
            for col, (label, value, help_text) in zip([col1, col2, col3], metrics):
                with col:
                    st.metric(label, value, help=help_text)
        else:
            st.warning("📊 No hay suficientes datos para mostrar el balance calórico")
            st.info("💡 Añade comidas y entrenamientos para ver el balance calórico")
    
    def _render_table(self, data_result, selected_date, table_type):
        """Renderizar tabla genérica"""
        controller = self.nutrition_controller if table_type == 'nutrition' else self.training_controller
        vm_method = 'get_meals_table_viewmodel' if table_type == 'nutrition' else 'get_trainings_table_viewmodel'
        delete_method = 'delete_meal_with_feedback' if table_type == 'nutrition' else 'delete_training_with_feedback'
        display_key = 'food_display' if table_type == 'nutrition' else 'display_text'
        
        table_vm = getattr(controller, vm_method)(data_result, selected_date)
        
        if not table_vm['success']:
            st.error(table_vm.get('error', f'Error al procesar {table_type}'))
            return
        
        if not table_vm['has_data']:
            st.info(table_vm['message'])
            return
        
        table_data = table_vm['table_data']
        st.info(table_data['header_message'])
        
        for row_data in table_data['rows']:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{row_data[display_key]} - {row_data['time_formatted']}")
            with col2:
                if st.button("🗑️", key=row_data['delete_key'], help=f"Borrar {'comida' if table_type == 'nutrition' else 'entrenamiento'}"):
                    delete_result = getattr(controller, delete_method)(row_data['id'])
                    
                    if delete_result['feedback_type'] == 'success':
                        show_success_message(delete_result['message'])
                    else:
                        st.error(delete_result['message'])
                    
                    if delete_result['should_rerun']:
                        st.rerun()
    
    def _render_macros_chart(self):
        """Gráfica de macronutrientes"""
        st.subheader("🥗 Macronutrientes")
        
        # Mensaje de actualización
        if st.session_state.get('objetivo_updated'):
            from utils.helpers import show_success_message
            show_success_message("Objetivo actualizado correctamente")
            del st.session_state.objetivo_updated
        
        # Selector de objetivo
        user_profile = st.session_state.get('user_profile', {})
        saved_objetivo = user_profile.get('objetivo', 'mantener_peso')
        
        objetivo_options = self.user_controller.get_objetivo_options()
        if not objetivo_options['success']:
            st.error("Error al cargar opciones de objetivo")
            return
        
        options = objetivo_options['data']['options']
        current_index = options.index(saved_objetivo) if saved_objetivo in options else 0
        
        objetivo = st.selectbox("🎯 ¿Cuál es tu objetivo principal?", options=options,
                              index=current_index, format_func=objetivo_options['data']['format_func'],
                              help="Selecciona tu objetivo para ver recomendaciones personalizadas",
                              key="objetivo_selector")
        
        # Guardar objetivo si cambió
        if objetivo != saved_objetivo:
            current_data = st.session_state.get('user_profile', {})
            result = self.user_controller.save_profile(
                current_data.get('name', ''), current_data.get('weight', 70.0), objetivo)
            
            if result['success']:
                st.session_state['user_profile']['objetivo'] = objetivo
                st.session_state.objetivo_updated = True
                st.rerun()
            else:
                st.error(f"❌ Error al guardar objetivo: {result['message']}")
        
        # Gráficas
        today = date.today().strftime('%Y-%m-%d')
        macros_data = self.statistics_controller.get_macros_distribution(today)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Distribución Actual**")
            if macros_data['success'] and macros_data['data']['has_data']:
                data = macros_data['data']['distribution']
                fig = go.Figure(data=[go.Pie(
                    labels=data['chart_data']['labels'],
                    values=data['chart_data']['values'],
                    hole=0.4, marker_colors=data['chart_data']['colors'],
                    textinfo='percent', textposition='outside'
                )])
                fig.update_layout(title=f"Consumido el {format_date(date.today())}", 
                                height=300, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"No hay datos nutricionales para el {format_date(date.today())}")
        
        with col2:
            st.markdown("**🎯 Distribución Recomendada**")
            recomendacion_vm = self.nutrition_controller.get_macro_recommendations_viewmodel(objetivo)
            if recomendacion_vm['success']:
                chart_data = recomendacion_vm['chart_data']
                
                fig = go.Figure(data=[go.Pie(
                    labels=chart_data['labels'],
                    values=chart_data['values'], 
                    hole=0.4,
                    marker_colors=chart_data['colors'],
                    textinfo='label', textposition='outside'
                )])
                fig.update_layout(title=chart_data['title'], 
                                height=300, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(recomendacion_vm.get('error', 'Error al obtener recomendaciones de macronutrientes'))
    
    def _get_image_base64(self, image_path):
        """Convertir imagen a base64 para HTML"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
        except Exception:
            return ""
    
    def _show_profile_change_toasts(self, user_name):
        """Mostrar toasts SOLO cuando realmente cambien los datos"""
        if not user_name:
            return
            
        current_weight = st.session_state.get('user_weight', 70.0)
        
        # Obtener valores anteriores guardados en session_state
        previous_name = st.session_state.get('previous_user_name')
        previous_weight = st.session_state.get('previous_user_weight')
        
        # Solo mostrar toasts si hay valores anteriores Y son diferentes
        # (No mostrar en primera carga ni en renders normales)
        if previous_name is not None and previous_name != user_name:
            st.toast(f"¡Hola {user_name}!")
        
        if previous_weight is not None and previous_weight != current_weight:
            st.toast(f"Peso actualizado a {current_weight} kg")
        
        # Actualizar valores anteriores para la próxima comparación
        st.session_state['previous_user_name'] = user_name
        st.session_state['previous_user_weight'] = current_weight