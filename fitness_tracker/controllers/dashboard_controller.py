import streamlit as st

class DashboardController:
    """Controlador para manejar la lógica del dashboard"""
    
    def __init__(self):
        """Inicializar controlador"""
        pass
    
    def get_training_form_state(self):
        """Obtener estado actual del formulario de entrenamiento"""
        return {
            'form_counter': st.session_state.get('training_form_counter', 0),
            'success_message': st.session_state.get('training_success_message'),
            'user_weight': st.session_state.get('user_weight', 70.0)
        }
    
    def reset_training_form(self):
        """Resetear formulario de entrenamiento"""
        st.session_state.training_form_counter = st.session_state.get('training_form_counter', 0) + 1
        if 'training_success_message' in st.session_state:
            del st.session_state['training_success_message']
    
    def validate_form_inputs(self, selected_sport, minutes_input):
        """Validar inputs del formulario antes de mostrar errores"""
        errors = []
        if not selected_sport:
            errors.append("❌ Por favor selecciona un deporte")
        if not minutes_input:
            errors.append("❌ Por favor especifica una cantidad válida de minutos")
        return errors
    
    def should_show_preview(self, form_data):
        """Determinar si mostrar preview del entrenamiento"""
        return (form_data.get('preview') and 
                not st.session_state.get('training_success_message'))
    
    def get_form_validation_status(self, validation_data):
        """Procesar estado de validación del formulario"""
        return {
            'has_errors': validation_data.get('show_error', False),
            'error_message': validation_data.get('error_message', ''),
            'is_valid': validation_data.get('is_valid', False)
        }



