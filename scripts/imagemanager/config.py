"""
Configuración global del Gestor de Imágenes
"""

from pathlib import Path
from dataclasses import dataclass

# Rutas del proyecto
SCRIPT_DIR = Path(__file__).parent.parent.resolve()
PROJECT_DIR = SCRIPT_DIR.parent
IMAGES_DIR = PROJECT_DIR / "es" / "imagenes"
CHAPTERS_DIR = PROJECT_DIR / "es" / "capitulos"

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

    # Prompts para traducción
    SYSTEM_INSTRUCTION = """In the context of Gliding and Soaring, generate an image visually identical to the attached input, preserving its exact style and composition. Replace all English text visible in the image with accurate technical Spanish translations."""

    DEFAULT_PROMPT = "Translate this gliding/soaring image to Spanish."
