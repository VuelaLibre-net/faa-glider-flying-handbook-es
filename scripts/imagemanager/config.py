"""
Configuración global del Gestor de Imágenes
"""

import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional

# Rutas del proyecto
SCRIPT_DIR = Path(__file__).parent.parent.resolve()
PROJECT_DIR = SCRIPT_DIR.parent
IMAGES_DIR = PROJECT_DIR / "es" / "imagenes"
CHAPTERS_DIR = PROJECT_DIR / "es" / "capitulos"

# Archivo de configuración persistente
CONFIG_FILE = PROJECT_DIR / ".image_manager_config.json"

# Configuración de UI
DEFAULT_WINDOW_SIZE = "1500x900"
MIN_WINDOW_SIZE = (1400, 850)
THUMBNAIL_SIZE = (140, 100)
THUMBNAIL_COLS = 3

# Configuración de compresión
DEFAULT_QUALITY = 85
DEFAULT_MAX_WIDTH = 1400  # Optimizado para A4 con márgenes a 200 DPI

# Configuración de backup
DEFAULT_CREATE_BACKUP = True

# Extensiones de imagen soportadas
IMAGE_EXTENSIONS = [
    "*.jpg",
    "*.jpeg",
    "*.png",
    "*.webp",
    "*.gif",
    "*.bmp",
    "*.JPG",
    "*.JPEG",
    "*.PNG",
    "*.WEBP",
    "*.GIF",
    "*.BMP",
]

# Patrones de backup a excluir
BACKUP_PATTERNS = [".bak", ".png.bak"]

# Estilos de badges para el editor
BADGE_STYLES = {
    "Gris (Gray)": ({"bg": "#F3F4F6", "fg": "#374151", "border": "#D1D5DB"}),
    "Rojo (Red)": ({"bg": "#FEE2E2", "fg": "#DC2626", "border": "#FECACA"}),
    "Naranja (Orange)": ({"bg": "#FFEDD5", "fg": "#EA580C", "border": "#FED7AA"}),
    "Ámbar (Amber)": ({"bg": "#FEF3C7", "fg": "#D97706", "border": "#FDE68A"}),
    "Verde (Green)": ({"bg": "#D1FAE5", "fg": "#059669", "border": "#A7F3D0"}),
    "Esmeralda (Emerald)": ({"bg": "#D1FAE5", "fg": "#047857", "border": "#6EE7B7"}),
    "Azul (Blue)": ({"bg": "#DBEAFE", "fg": "#2563EB", "border": "#BFDBFE"}),
    "Índigo (Indigo)": ({"bg": "#E0E7FF", "fg": "#4F46E5", "border": "#C7D2FE"}),
    "Violeta (Violet)": ({"bg": "#EDE9FE", "fg": "#7C3AED", "border": "#DDD6FE"}),
    "Rosa (Pink)": ({"bg": "#FCE7F3", "fg": "#DB2777", "border": "#FBCFE8"}),
    "Negro (Black)": ({"bg": "#1F2937", "fg": "#F9FAFB", "border": "#374151"}),
}


@dataclass
class TranslationConfig:
    """Configuración para la traducción de imágenes."""

    temperature: float = 0.4
    top_p: float = 0.95
    top_k: int = 40
    max_output_tokens: int = 8192
    
    # Modelo por omisión - Nano Banana Pro preview
    DEFAULT_MODEL: str = "nano-banana-pro-preview"
    
    # Prompt editable por el usuario (prompt por omisión hardcodificado)
    EDITABLE_PROMPT: str = """### SYSTEM ROLE
Act as a Senior Technical Illustrator and Aviation Subject Matter Expert for an educational Glider Pilot Manual.
Your task is to modernize the visual style of the provided input image and translate all textual elements into Spanish, ensuring technical accuracy across different domains (Mechanics, Meteorology, and Flight Procedures).

### VISUAL STYLE & MODERNIZATION (STRICT)
- **Aesthetic:** "Modern Vector Illustration" style. Clean, flat design with subtle shadows for depth (2.5D). No photorealism.
- **Consistency:** Maintain a uniform look across the book. Use a cohesive color palette (e.g., cool blues for air/sky, clean greys for hardware, distinct colors for arrows/vectors).
- **Typography:** Replace all original text with a modern Sans-Serif font (like Roboto or Helvetica). Text must be crisp, legible, and perfectly aligned with original pointers or zones.
- **Composition:** Strictly preserve the original spatial layout, diagrams, arrow directions, and proportions. Do not distort flight paths or meteorological formations.

### DYNAMIC TRANSLATION PROTOCOL (ENGLISH -> SPANISH)
Analyze the context of the image to select the correct terminology:
1. **If Aircraft Components:** Use "Vuelo a Vela" mechanics terms (e.g., Spoiler -> Aerofreno, Fin -> Deriva).
2. **If Meteorology:** Use standard meteorological terms (e.g., Lapse rate -> Gradiente térmico, Lee wave -> Onda de montaña).
3. **If Flight Patterns/Traffic:** Use standard ICAO/EASA phraseology (e.g., Downwind leg -> Tramo de viento en cola, Base leg -> Tramo base, Touchdown -> Toma de contacto).

**CRITICAL:** Do not translate literally. Use the professional aviation term used in Spain/South America.

### OUTPUT GENERATION
Generate the modernized image in high fidelity. The final result should look like a premium vector diagram from a 2024 aviation textbook."""
    
    # Si está habilitada la traducción automática en menú contextual
    AUTO_TRANSLATE_CONTEXT: bool = True

    # Prompts para traducción (sistema - no editable por usuario)
    SYSTEM_INSTRUCTION = """In the context of Gliding and Soaring, generate an image visually identical to the attached input, preserving its exact style and composition. Replace all English text visible in the image with accurate technical Spanish translations."""

    DEFAULT_PROMPT = "Translate this gliding/soaring image to Spanish."


# Modelos disponibles para selección
AVAILABLE_MODELS = [
    ("Nano Banana Pro preview - calidad", "nano-banana-pro-preview"),
    ("Gemini 2.0 Flash Image", "gemini-2.0-flash-preview-image-generation"),
    ("Gemini 2.0 Flash Exp", "gemini-2.0-flash-exp"),
    ("Gemini 2.5 Flash", "gemini-2.5-flash-image"),
    ("Gemini 3 Pro", "gemini-3-pro-image-preview"),
]


class ConfigManager:
    """Gestiona la carga y guardado de configuración persistente."""
    
    @staticmethod
    def load_config() -> dict:
        """Carga la configuración desde el archivo JSON."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[ConfigManager] Error cargando configuración: {e}")
                return {}
        return {}
    
    @staticmethod
    def save_config(config: dict) -> bool:
        """Guarda la configuración en el archivo JSON."""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[ConfigManager] Error guardando configuración: {e}")
            return False
    
    @classmethod
    def get_default_model(cls) -> str:
        """Obtiene el modelo por defecto guardado o el predeterminado."""
        config = cls.load_config()
        return config.get('default_model', TranslationConfig.DEFAULT_MODEL)
    
    @classmethod
    def set_default_model(cls, model: str) -> bool:
        """Guarda el modelo por defecto."""
        config = cls.load_config()
        config['default_model'] = model
        return cls.save_config(config)
    
    @classmethod
    def get_prompt(cls) -> str:
        """Obtiene el prompt guardado o el predeterminado."""
        config = cls.load_config()
        return config.get('prompt', TranslationConfig.EDITABLE_PROMPT)
    
    @classmethod
    def set_prompt(cls, prompt: str) -> bool:
        """Guarda el prompt."""
        config = cls.load_config()
        config['prompt'] = prompt
        return cls.save_config(config)
    
    @classmethod
    def get_auto_translate(cls) -> bool:
        """Obtiene si la traducción automática está habilitada."""
        config = cls.load_config()
        return config.get('auto_translate', TranslationConfig.AUTO_TRANSLATE_CONTEXT)
    
    @classmethod
    def set_auto_translate(cls, enabled: bool) -> bool:
        """Guarda el estado de traducción automática."""
        config = cls.load_config()
        config['auto_translate'] = enabled
        return cls.save_config(config)
