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
import config

class DashboardView:
    """Vista principal del dashboard de Fitness Tracker"""
    
    def __init__(self):
        """Inicializar la vista del dashboard"""
        self.training_controller = TrainingController()
        self.nutrition_controller = NutritionController()
        
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
        
        # Sidebar para formularios
        with st.sidebar:
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
        
        food = st.text_input("Alimento", placeholder="Ej: pollo, arroz, manzana...")
        grams = st.number_input("Gramos", min_value=1, max_value=10000, value=100)
        
        if st.button("➕ Añadir Comida", type="primary"):
            if food and grams:
                result = self.nutrition_controller.add_meal(food, grams)
                if result['success']:
                    st.success(result['message'])
                    st.rerun()
                else:
                    st.error(result['message'])
            else:
                st.warning("Por favor completa todos los campos")
    
    def _render_training_form(self):
        """Renderizar formulario para añadir entrenamiento"""
        st.subheader("Nuevo Entrenamiento")
        
        activity = st.text_input("Actividad", placeholder="Ej: running, gym, yoga...")
        minutes = st.number_input("Minutos", min_value=1, max_value=1440, value=30)
        
        if st.button("🏃‍♂️ Añadir Entrenamiento", type="primary"):
            if activity and minutes:
                result = self.training_controller.add_training(activity, minutes)
                if result['success']:
                    st.success(result['message'])
                    st.rerun()
                else:
                    st.error(result['message'])
            else:
                st.warning("Por favor completa todos los campos")
    
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
        """Renderizar registros recientes"""
        st.subheader("📋 Registros Recientes")
        
        # Obtener registros recientes
        recent_meals = self.nutrition_controller.get_recent_meals(5)
        recent_trainings = self.training_controller.get_recent_trainings(5)
        
        # Crear tabs para diferentes tipos de registros
        tab1, tab2 = st.tabs(["🍽️ Comidas", "💪 Entrenamientos"])
        
        with tab1:
            if recent_meals['success'] and recent_meals['data']:
                meals_df = pd.DataFrame(recent_meals['data'])
                st.dataframe(meals_df[['food', 'grams', 'calories', 'date']], 
                           use_container_width=True)
            else:
                st.info("No hay comidas registradas")
        
        with tab2:
            if recent_trainings['success'] and recent_trainings['data']:
                trainings_df = pd.DataFrame(recent_trainings['data'])
                st.dataframe(trainings_df[['activity', 'minutes', 'calories_burned', 'date']], 
                           use_container_width=True)
            else:
                st.info("No hay entrenamientos registrados")
    
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
