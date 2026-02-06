"""
Módulo de traducción de imágenes usando Google Gemini API

Integra la funcionalidad de traducción automática de imágenes de vuelo a vela.
"""

from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Optional, Union

from PIL import Image

from .config import TranslationConfig
from .clipboard_handler import ClipboardHandler, get_clipboard_handler, NoImageInClipboardError


class GeminiModel(Enum):
    """Modelos de Gemini disponibles."""
    FLASH = "gemini-2.5-flash-image"  # Económico y rápido
    PRO = "gemini-3-pro-image-preview"  # Mayor calidad


class TranslationError(Exception):
    """Error base para operaciones de traducción."""
    pass


class TranslationConfigError(TranslationError):
    """Error de configuración (API key no encontrada)."""
    pass


class TranslationAPIError(TranslationError):
    """Error en la llamada a la API."""
    pass


class TranslationGenerationError(TranslationError):
    """Error en la generación de contenido."""
    pass


@dataclass
class ModelInfo:
    """Información de un modelo disponible."""
    name: str
    value: str
    description: str


class TranslationManager:
    """
    Gestor de traducción de imágenes usando Google Gemini API.
    
    Proporciona una interfaz simplificada para traducir imágenes
    desde archivos o desde el portapapeles.
    """
    
    # Modelos de fallback cuando la API no está disponible
    FALLBACK_MODELS = [
        ModelInfo("Gemini 2.0 Flash Image (rápido)", "gemini-2.0-flash-preview-image-generation", "Rápido y económico"),
        ModelInfo("Gemini 2.0 Flash Exp (experimental)", "gemini-2.0-flash-exp", "Experimental"),
    ]
    
    # Cache de modelos obtenidos de la API
    _cached_models: list[ModelInfo] | None = None
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Union[GeminiModel, str] = None,
        system_instruction: Optional[str] = None
    ):
        """
        Inicializa el gestor de traducción.
        
        Args:
            api_key: Clave de API de Google Gemini. Si no se proporciona,
                    se busca en la variable de entorno GEMINI_API_KEY.
            model: Modelo a usar (GeminiModel o string)
            system_instruction: Instrucción del sistema personalizada
        
        Raises:
            TranslationConfigError: Si no se puede inicializar el cliente
        """
        # Importar aquí para que el módulo cargue sin dependencias si no se usa
        try:
            from google import genai
            from google.genai import types
            self._genai = genai
            self._types = types
        except ImportError:
            raise TranslationConfigError(
                "google-genai no está instalado. Instala: pip install google-genai"
            )
        
        # Obtener API key
        self._api_key = api_key or self._get_api_key_from_env()
        if not self._api_key or self._api_key == 'tu_api_key_aqui':
            raise TranslationConfigError(
                "API key no configurada.\n"
                "1. Crea un archivo .env con GEMINI_API_KEY=tu_key\n"
                "2. O pasa api_key directamente"
            )
        
        # Crear cliente
        self._client = genai.Client(api_key=self._api_key)
        
        # Determinar modelo (usar el guardado o el predeterminado)
        if model is None:
            # Cargar modelo guardado desde configuración
            from .config import ConfigManager
            saved_model = ConfigManager.get_default_model()
            model = saved_model
        self._model = model
        self._model_name = model.value if isinstance(model, GeminiModel) else model
        
        # Instrucción del sistema
        self._system_instruction = system_instruction or TranslationConfig.SYSTEM_INSTRUCTION
        
        # Configuración de generación
        self._config = TranslationConfig()
        
        # Clipboard handler
        self._clipboard = get_clipboard_handler()
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Obtiene la API key desde variables de entorno."""
        import os
        
        # Primero buscar en el entorno
        api_key = os.environ.get('GEMINI_API_KEY')
        if api_key:
            return api_key
        
        # Luego buscar en archivo .env
        env_paths = [
            Path('.env'),
            Path(__file__).parent.parent.parent / '.env',
            Path.home() / '.config' / 'faa-gfh' / '.env',
        ]
        
        for env_path in env_paths:
            if env_path.exists():
                content = env_path.read_text()
                for line in content.split('\n'):
                    if line.startswith('GEMINI_API_KEY='):
                        return line.split('=', 1)[1].strip().strip('"\'')
        
        return None
    
    def change_model(self, model: Union[GeminiModel, str]):
        """Cambia el modelo de Gemini utilizado."""
        self._model = model
        self._model_name = model.value if isinstance(model, GeminiModel) else model
    
    @property
    def current_model(self) -> str:
        """Devuelve el nombre del modelo actual."""
        return self._model_name
    
    @property
    def current_model_friendly_name(self) -> str:
        """Devuelve un nombre amigable del modelo actual."""
        model_map = {
            GeminiModel.FLASH.value: "Gemini 2.5 Flash",
            GeminiModel.PRO.value: "Gemini 3 Pro",
        }
        return model_map.get(self._model_name, self._model_name)
    
    def is_configured(self) -> bool:
        """Verifica si la API está configurada correctamente."""
        try:
            response = self._client.models.generate_content(
                model=self._model_name,
                contents="Hello",
                config=self._types.GenerateContentConfig(max_output_tokens=10)
            )
            return response is not None
        except Exception:
            return False
    
    def check_connection_status(self) -> dict:
        """
        Verifica el estado de conexión con la API de Gemini.
        
        Returns:
            Diccionario con información detallada del estado:
            - status: 'ok', 'error', 'unconfigured'
            - api_key_present: bool
            - api_key_source: str ('env', '.env', 'parameter', 'none')
            - api_key_preview: str (últimos 4 caracteres)
            - endpoint: str
            - models_available: int
            - current_model: str
            - model_valid: bool
            - response_time_ms: float
            - error_message: str (si aplica)
        """
        import time
        import os
        
        result = {
            'status': 'unconfigured',
            'api_key_present': False,
            'api_key_source': 'none',
            'api_key_preview': None,
            'endpoint': 'generativelanguage.googleapis.com',
            'models_available': 0,
            'current_model': self._model_name,
            'model_valid': False,
            'response_time_ms': 0,
            'error_message': None
        }
        
        # Verificar API key
        if self._api_key and self._api_key != 'tu_api_key_aqui':
            result['api_key_present'] = True
            result['api_key_preview'] = f"...{self._api_key[-4:]}"
            
            # Determinar fuente
            if os.environ.get('GEMINI_API_KEY'):
                result['api_key_source'] = 'env'
            else:
                result['api_key_source'] = '.env'
        else:
            result['error_message'] = "API key no configurada"
            return result
        
        # Intentar conexión
        start_time = time.time()
        try:
            # Listar modelos disponibles
            models = list(self._client.models.list())
            result['models_available'] = len(models)
            
            # Verificar que el modelo actual existe
            model_names = [m.name for m in models]
            result['model_valid'] = any(self._model_name in name for name in model_names)
            
            result['response_time_ms'] = round((time.time() - start_time) * 1000, 2)
            result['status'] = 'ok'
            
        except Exception as e:
            result['response_time_ms'] = round((time.time() - start_time) * 1000, 2)
            result['status'] = 'error'
            result['error_message'] = str(e)
        
        return result
    
    def ping_endpoint(self) -> tuple[bool, str]:
        """
        Hace un ping simple al endpoint de Gemini.
        
        Returns:
            Tuple (success, message)
        """
        try:
            # Intentar una operación simple
            models = list(self._client.models.list())
            return True, f"✅ Conexión exitosa. {len(models)} modelos disponibles."
        except Exception as e:
            return False, f"❌ Error de conexión: {str(e)}"
    
    def translate_image(
        self,
        image: Union[Image.Image, str, Path, bytes],
        custom_prompt: Optional[str] = None
    ) -> Image.Image:
        """
        Traduce una imagen de vuelo a vela del inglés al español.
        
        Args:
            image: Imagen a traducir (PIL.Image, ruta, o bytes)
            custom_prompt: Prompt personalizado opcional
            
        Returns:
            Image.Image: La imagen generada con texto traducido
        """
        # Preparar la imagen
        pil_image = self._prepare_image(image)
        prompt = custom_prompt or TranslationConfig.DEFAULT_PROMPT
        
        try:
            print(f"[Debug] Enviando imagen a Gemini con modelo: {self._model_name}")
            print(f"[Debug] Dimensiones de imagen de entrada: {pil_image.size}")
            print(f"[Debug] Prompt: {prompt}")
            
            # Configurar para generación de imagen
            config = self._types.GenerateContentConfig(
                system_instruction=self._system_instruction,
                temperature=self._config.temperature,
                top_p=self._config.top_p,
                top_k=self._config.top_k,
                max_output_tokens=self._config.max_output_tokens,
                # Especificar que queremos respuesta de imagen
                response_modalities=['image', 'text'],
            )
            
            response = self._client.models.generate_content(
                model=self._model_name,
                contents=[prompt, pil_image],
                config=config
            )
            
            print(f"[Debug] Respuesta recibida de Gemini")
            return self._extract_image_from_response(response)
            
        except Exception as e:
            error_msg = str(e).lower()
            if "api key" in error_msg or "authentication" in error_msg:
                raise TranslationAPIError(f"Error de autenticación: {e}") from e
            elif "quota" in error_msg or "rate limit" in error_msg:
                raise TranslationAPIError(f"Límite de API excedido: {e}") from e
            else:
                raise TranslationGenerationError(f"Error en generación: {e}") from e
    
    def _prepare_image(
        self, image: Union[Image.Image, str, Path, bytes]
    ) -> Image.Image:
        """Convierte la entrada a PIL.Image.Image."""
        try:
            if isinstance(image, Image.Image):
                return image
            elif isinstance(image, (str, Path)):
                return Image.open(image)
            elif isinstance(image, bytes):
                return Image.open(BytesIO(image))
            else:
                raise TranslationGenerationError(f"Tipo no soportado: {type(image)}")
        except Exception as e:
            raise TranslationGenerationError(f"Error al procesar imagen: {e}") from e
    
    def _extract_image_from_response(self, response) -> Image.Image:
        """Extrae la imagen de la respuesta de Gemini."""
        try:
            # Debug: Imprimir estructura de la respuesta
            print(f"[Debug] Respuesta recibida. Candidatos: {len(response.candidates) if response.candidates else 0}")
            
            if response.candidates:
                candidate = response.candidates[0]
                print(f"[Debug] Candidate finish reason: {candidate.finish_reason if hasattr(candidate, 'finish_reason') else 'N/A'}")
                
                if candidate.content and candidate.content.parts:
                    print(f"[Debug] Número de parts: {len(candidate.content.parts)}")
                    
                    for i, part in enumerate(candidate.content.parts):
                        has_inline = hasattr(part, 'inline_data') and part.inline_data is not None
                        has_blob = hasattr(part, 'blob') and part.blob is not None
                        has_text = hasattr(part, 'text') and part.text is not None
                        print(f"[Debug] Part {i}: inline_data={has_inline}, blob={has_blob}, text={has_text}")
                        
                        # Intentar obtener imagen de inline_data
                        if hasattr(part, 'inline_data') and part.inline_data:
                            print(f"[Debug] Extrayendo de inline_data, mime_type: {part.inline_data.mime_type if hasattr(part.inline_data, 'mime_type') else 'N/A'}")
                            image_data = part.inline_data.data
                            return Image.open(BytesIO(image_data))
                        
                        # Intentar obtener de blob
                        if hasattr(part, 'blob') and part.blob:
                            print(f"[Debug] Extrayendo de blob")
                            image_data = part.blob.data
                            return Image.open(BytesIO(image_data))
                        
                        # Verificar si hay texto (para debug)
                        if hasattr(part, 'text') and part.text:
                            print(f"[Debug] Texto recibido: {part.text[:100]}...")
            
            # Si llegamos aquí, no encontramos imagen
            if response.text:
                raise TranslationGenerationError(
                    f"La API devolvió texto en lugar de imagen: {response.text[:200]}..."
                )
            
            raise TranslationGenerationError(
                "No se pudo extraer imagen de la respuesta. "
                "La API no devolvió datos de imagen."
            )
            
        except TranslationGenerationError:
            raise
        except Exception as e:
            import traceback
            print(f"[Debug] Error extrayendo imagen: {e}")
            print(traceback.format_exc())
            raise TranslationGenerationError(f"Error procesando respuesta: {e}") from e
    
    def translate_from_file(self, image_path: Union[str, Path]) -> Image.Image:
        """Traduce una imagen desde un archivo."""
        return self.translate_image(image_path)
    
    def translate_from_clipboard(self) -> Image.Image:
        """Traduce una imagen desde el portapapeles."""
        if not self._clipboard.has_image():
            raise NoImageInClipboardError("No hay imagen en el portapapeles")
        
        image = self._clipboard.get_image()
        return self.translate_image(image)
    
    def get_clipboard_image(self) -> Optional[Image.Image]:
        """Obtiene la imagen del portapapeles sin traducir."""
        try:
            if self._clipboard.has_image():
                return self._clipboard.get_image()
        except Exception:
            pass
        return None
    
    def set_clipboard_image(self, image: Image.Image):
        """Coloca una imagen en el portapapeles."""
        self._clipboard.set_image(image)
    
    @classmethod
    def get_available_models(cls) -> list[tuple[str, str]]:
        """
        Obtiene lista de modelos disponibles.
        Usa cache si está disponible, sino devuelve fallback.
        """
        if cls._cached_models:
            return [(info.name, info.value) for info in cls._cached_models]
        return [(info.name, info.value) for info in cls.FALLBACK_MODELS]
    
    def fetch_models_from_api(self) -> list[ModelInfo]:
        """
        Obtiene modelos desde la API de Google en tiempo real.
        Filtra modelos que soporten generación/procesamiento de imágenes.
        
        Returns:
            Lista de ModelInfo con modelos disponibles para imagen
        """
        try:
            models_list = []
            
            for model in self._client.models.list():
                model_name = model.name if hasattr(model, 'name') else str(model)
                
                # Extraer el ID del modelo (ej: "models/gemini-2.0-flash" -> "gemini-2.0-flash")
                if model_name.startswith('models/'):
                    model_id = model_name.replace('models/', '')
                else:
                    model_id = model_name
                
                # Filtrar modelos que soporten imágenes
                # Criterios: nombre contiene 'image', 'flash', 'pro', 'exp'
                # y NO contiene 'embedding', 'aqa', 'thinking'
                lower_id = model_id.lower()
                
                # Excluir modelos sin soporte de imagen
                if any(x in lower_id for x in ['embedding', 'aqa', 'thinking', 'learnlm']):
                    continue
                
                # Incluir modelos con capacidad de imagen
                is_image_model = any(x in lower_id for x in ['image', 'flash', 'pro', 'exp'])
                
                # También verificar supported_generation_methods si está disponible
                if hasattr(model, 'supported_generation_methods'):
                    methods = model.supported_generation_methods or []
                    if 'generateContent' in methods:
                        is_image_model = True
                
                if is_image_model:
                    # Crear nombre amigable
                    display_name = model_id.replace('-', ' ').title()
                    if 'image' in lower_id:
                        display_name += ' (imagen)'
                    elif 'flash' in lower_id:
                        display_name += ' (rápido)'
                    elif 'pro' in lower_id:
                        display_name += ' (calidad)'
                    
                    models_list.append(ModelInfo(
                        name=display_name,
                        value=model_id,
                        description=f"Modelo: {model_id}"
                    ))
            
            # Ordenar: primero los que tienen 'image' en el nombre
            models_list.sort(key=lambda m: (
                0 if 'image' in m.value.lower() else 1,
                m.value
            ))
            
            # Actualizar cache
            if models_list:
                TranslationManager._cached_models = models_list
                print(f"[Debug] Cargados {len(models_list)} modelos desde API")
                return models_list
            
            print("[Debug] No se encontraron modelos de imagen, usando fallback")
            return self.FALLBACK_MODELS
            
        except Exception as e:
            print(f"[Debug] Error obteniendo modelos de API: {e}")
            return self.FALLBACK_MODELS


def is_translation_available() -> bool:
    """Verifica si la funcionalidad de traducción está disponible."""
    try:
        from google import genai
        return True
    except ImportError:
        return False
