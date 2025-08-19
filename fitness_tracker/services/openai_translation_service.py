# Fitness Tracker - Servicio de Traducción OpenAI
# ==============================================
# Este archivo maneja las traducciones usando OpenAI GPT

import openai
import config
import logging
from typing import Optional

# Configurar logging
logger = logging.getLogger(__name__)

class OpenAITranslationService:
    """Servicio para traducir texto usando OpenAI GPT"""
    
    def __init__(self):
        """Inicializar el servicio de traducción OpenAI"""
        self.api_key = config.OPENAI_API_KEY
        self.model = config.OPENAI_MODEL
        
        if self.api_key:
            # Configurar el cliente OpenAI con la nueva sintaxis
            self.client = openai.OpenAI(api_key=self.api_key)
            logger.info("Servicio de traducción OpenAI inicializado")
        else:
            logger.warning("OpenAI API key no configurada - traducción deshabilitada")
    
    def translate_to_english(self, spanish_text: str) -> Optional[str]:
        """Traducir texto del español al inglés"""
        try:
            if not self.api_key:
                logger.warning("OpenAI API key no configurada")
                return None
            
            if not spanish_text or not spanish_text.strip():
                logger.warning("Texto vacío para traducir")
                return None
            
            logger.info(f"Traduciendo a inglés con OpenAI: '{spanish_text}'")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "Eres un traductor profesional español-inglés. Traduce solo el texto proporcionado, sin añadir explicaciones ni contexto adicional."
                    },
                    {
                        "role": "user", 
                        "content": f"Traduce al inglés: {spanish_text}"
                    }
                ],
                max_tokens=100,
                temperature=0.1  # Baja temperatura para traducciones consistentes
            )
            
            translated_text = response.choices[0].message.content.strip()
            
            if translated_text:
                logger.info(f"Traducción exitosa: '{spanish_text}' → '{translated_text}'")
                return translated_text
            else:
                logger.warning("Respuesta vacía de OpenAI")
                return None
                
        except openai.AuthenticationError:
            logger.error("Error de autenticación en OpenAI - verificar API key")
            return None
        except openai.RateLimitError:
            logger.error("Rate limit alcanzado en OpenAI")
            return None
        except openai.APIError as e:
            logger.error(f"Error de API de OpenAI: {e}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado en traducción OpenAI: {e}")
            return None
    
    def translate_to_spanish(self, english_text: str) -> Optional[str]:
        """Traducir texto del inglés al español"""
        try:
            if not self.api_key:
                logger.warning("OpenAI API key no configurada")
                return None
            
            if not english_text or not english_text.strip():
                logger.warning("Texto vacío para traducir")
                return None
            
            logger.info(f"Traduciendo a español con OpenAI: '{english_text}'")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "Eres un traductor profesional inglés-español. Traduce solo el texto proporcionado, sin añadir explicaciones ni contexto adicional."
                    },
                    {
                        "role": "user", 
                        "content": f"Traduce al español: {english_text}"
                    }
                ],
                max_tokens=100,
                temperature=0.1  # Baja temperatura para traducciones consistentes
            )
            
            translated_text = response.choices[0].message.content.strip()
            
            if translated_text:
                logger.info(f"Traducción exitosa: '{english_text}' → '{translated_text}'")
                return translated_text
            else:
                logger.warning("Respuesta vacía de OpenAI")
                return None
                
        except openai.AuthenticationError:
            logger.error("Error de autenticación en OpenAI - verificar API key")
            return None
        except openai.RateLimitError:
            logger.error("Rate limit alcanzado en OpenAI")
            return None
        except openai.APIError as e:
            logger.error(f"Error de API de OpenAI: {e}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado en traducción OpenAI: {e}")
            return None
    
    def is_available(self) -> bool:
        """Verificar si el servicio está disponible"""
        return bool(self.api_key)
