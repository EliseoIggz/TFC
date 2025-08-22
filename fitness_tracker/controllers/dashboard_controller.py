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
    
    def init_user_profile(self, user_controller):
        """Inicializar perfil de usuario"""
        if 'user_profile' not in st.session_state:
            profile = user_controller.get_profile()
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
    
    def get_sport_selector_data(self, sports_data, selected_category):
        """Obtener datos del selector de deportes"""
        all_sports = sports_data['all_sports']
        
        # Si la categoría es "Todas", mostrar todos los deportes
        if selected_category == 'Todas':
            available_sports = all_sports
        else:
            # Filtrar por categoría específica
            available_sports = [s for s in all_sports if s['category'] == selected_category]
        
        if not available_sports:
            return {
                'has_sports': False,
                'warning_message': "No hay deportes disponibles en esta categoría"
            }
        
        sport_options = {sport['name']: sport['key'] for sport in available_sports}
        sport_options_list = [''] + list(sport_options.keys())
        
        return {
            'has_sports': True,
            'available_sports': available_sports,
            'sport_options': sport_options,
            'sport_options_list': sport_options_list
        }
    
    def set_training_toast(self, message):
        """Guardar mensaje de toast para entrenamiento"""
        st.session_state['pending_training_toast'] = message
    
    def get_training_toast(self):
        """Obtener y limpiar toast de entrenamiento"""
        if st.session_state.get('pending_training_toast'):
            message = st.session_state['pending_training_toast']
            del st.session_state['pending_training_toast']
            return message
        return None



