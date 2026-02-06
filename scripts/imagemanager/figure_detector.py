"""
Módulo para detección de figuras en páginas de PDF.
Proporciona detección manual y automática (vía IA) de regiones de figuras.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import re
from PIL import Image


@dataclass
class DetectedFigure:
    """Representa una figura detectada en una página."""
    
    # Bounding box (x1, y1, x2, y2) en coordenadas de imagen
    bbox: tuple[int, int, int, int]
    
    # Pie de foto original (ej: "Figure 2-1. Glider Components")
    caption: str = ""
    
    # Número de figura extraído (ej: "2-1")
    figure_number: str = ""
    
    # Nombre de archivo sugerido (ej: "figura-02-01-componentes.png")
    suggested_filename: str = ""
    
    # Archivo de traducción asociado (path completo si existe)
    associated_file: Optional[Path] = None
    
    # Página fuente donde se encontró
    source_page: int = 0
    
    # Estado de la figura
    is_exported: bool = False
    
    def __post_init__(self):
        """Extrae número de figura y genera nombre sugerido."""
        if self.caption and not self.figure_number:
            self._parse_caption()
    
    def _parse_caption(self):
        """Parsea el pie de foto para extraer número y descripción."""
        # Primero intentar extraer solo el número de figura (siempre funciona)
        num_match = re.search(r'Figure\s+(\d+)-(\d+)', self.caption, re.IGNORECASE)
        if num_match:
            chapter = num_match.group(1).zfill(2)
            fig_num = num_match.group(2).zfill(2)
            self.figure_number = f"{chapter}-{fig_num}"
            
            # Intentar extraer descripción (opcional)
            # Patrones: "Figure 2-1. Description" o "Figure 2-1 Description"
            desc_match = re.match(
                r'Figure\s+\d+-\d+[.\s]+(.+)', 
                self.caption, 
                re.IGNORECASE
            )
            
            if desc_match:
                description = desc_match.group(1).strip()
                # Normalizar descripción: minúsculas, sin puntuación, guiones
                desc_clean = re.sub(r'[^\w\s]', '', description.lower())
                desc_clean = re.sub(r'\s+', '-', desc_clean.strip())
                # Limitar longitud
                if len(desc_clean) > 30:
                    desc_clean = desc_clean[:30].rsplit('-', 1)[0]
                self.suggested_filename = f"figura-{chapter}-{fig_num}-{desc_clean}.png"
            else:
                # Sin descripción, solo número
                self.suggested_filename = f"figura-{chapter}-{fig_num}.png"
    
    def crop_from_image(self, source_image: Image.Image) -> Image.Image:
        """Recorta esta figura de la imagen fuente."""
        x1, y1, x2, y2 = self.bbox
        return source_image.crop((x1, y1, x2, y2))


class FigureDetector:
    """
    Detecta figuras en páginas de PDF.
    Soporta detección manual (marcado por usuario) y automática (IA).
    """
    
    def __init__(self, translation_manager=None):
        """
        Args:
            translation_manager: Opcional, TranslationManager para usar IA
        """
        self._translation_manager = translation_manager
        self._detected_figures: list[DetectedFigure] = []
    
    @property
    def figures(self) -> list[DetectedFigure]:
        """Lista de figuras detectadas."""
        return self._detected_figures
    
    def clear(self):
        """Limpia todas las figuras detectadas."""
        self._detected_figures.clear()
    
    def add_manual_figure(
        self,
        bbox: tuple[int, int, int, int],
        caption: str,
        source_page: int = 0
    ) -> DetectedFigure:
        """
        Añade una figura marcada manualmente.
        
        Args:
            bbox: Bounding box (x1, y1, x2, y2)
            caption: Pie de foto (ej: "Figure 2-1. Description")
            source_page: Número de página fuente
        
        Returns:
            DetectedFigure creada
        """
        figure = DetectedFigure(
            bbox=bbox,
            caption=caption,
            source_page=source_page
        )
        self._detected_figures.append(figure)
        return figure
    
    def detect_figures_with_ai(
        self,
        page_image: Image.Image,
        source_page: int = 0
    ) -> list[DetectedFigure]:
        """
        Detecta figuras automáticamente usando IA.
        
        Args:
            page_image: Imagen de la página
            source_page: Número de página
        
        Returns:
            Lista de figuras detectadas
        """
        if not self._translation_manager:
            print("[FigureDetector] No hay TranslationManager para detección IA")
            return []
        
        try:
            # Prompt para detección de figuras
            prompt = """Analyze this page from the FAA Glider Flying Handbook.
            
Identify ALL figures/images on this page. For each figure found, provide:
1. The bounding box coordinates as percentages of the image (left, top, right, bottom)
2. The figure caption exactly as written (e.g., "Figure 2-1. Glider Components")

Respond in this exact format for each figure:
FIGURE:
  BBOX: left%, top%, right%, bottom%
  CAPTION: [exact caption text]

If no figures are found, respond with: NO_FIGURES

Be precise with the bounding boxes - they should tightly encompass each figure including its caption."""

            # Usar el cliente existente para llamar a la API
            client = self._translation_manager._client
            model = self._translation_manager._model_name
            
            response = client.models.generate_content(
                model=model,
                contents=[prompt, page_image]
            )
            
            # Parsear respuesta
            return self._parse_ai_response(response.text, page_image.size, source_page)
            
        except Exception as e:
            print(f"[FigureDetector] Error en detección IA: {e}")
            return []
    
    def _parse_ai_response(
        self,
        response_text: str,
        image_size: tuple[int, int],
        source_page: int
    ) -> list[DetectedFigure]:
        """Parsea la respuesta de la IA y crea DetectedFigures."""
        figures = []
        width, height = image_size
        
        if "NO_FIGURES" in response_text.upper():
            return figures
        
        # Buscar bloques FIGURE:
        figure_blocks = re.split(r'FIGURE:', response_text, flags=re.IGNORECASE)
        
        for block in figure_blocks[1:]:  # Saltar el primero (antes del primer FIGURE:)
            try:
                # Extraer BBOX
                bbox_match = re.search(
                    r'BBOX:\s*(\d+(?:\.\d+)?)%?,?\s*(\d+(?:\.\d+)?)%?,?\s*(\d+(?:\.\d+)?)%?,?\s*(\d+(?:\.\d+)?)%?',
                    block,
                    re.IGNORECASE
                )
                # Extraer CAPTION
                caption_match = re.search(
                    r'CAPTION:\s*(.+?)(?:\n|$)',
                    block,
                    re.IGNORECASE
                )
                
                if bbox_match:
                    # Convertir porcentajes a píxeles
                    left = int(float(bbox_match.group(1)) / 100 * width)
                    top = int(float(bbox_match.group(2)) / 100 * height)
                    right = int(float(bbox_match.group(3)) / 100 * width)
                    bottom = int(float(bbox_match.group(4)) / 100 * height)
                    
                    caption = caption_match.group(1).strip() if caption_match else ""
                    
                    figure = DetectedFigure(
                        bbox=(left, top, right, bottom),
                        caption=caption,
                        source_page=source_page
                    )
                    figures.append(figure)
                    self._detected_figures.append(figure)
                    
            except Exception as e:
                print(f"[FigureDetector] Error parseando bloque: {e}")
                continue
        
        return figures
    
    def detect_figures_with_ocr(
        self,
        page_image: Image.Image,
        source_page: int = 0
    ) -> list[DetectedFigure]:
        """
        Detecta figuras usando OCR (pytesseract) buscando pies de foto.
        
        Busca patrones 'Figure X-X' en el texto de la página y crea
        DetectedFigures con las coordenadas del texto encontrado.
        
        Args:
            page_image: Imagen de la página
            source_page: Número de página
        
        Returns:
            Lista de figuras detectadas
        """
        try:
            import pytesseract
        except ImportError:
            print("[FigureDetector] pytesseract no instalado. Instala con: pip install pytesseract")
            return []
        
        figures = []
        
        try:
            # Obtener datos de OCR con posiciones
            ocr_data = pytesseract.image_to_data(
                page_image, 
                output_type=pytesseract.Output.DICT,
                lang='eng'
            )
            
            # Buscar patrones "Figure X-X" en el texto
            n_boxes = len(ocr_data['text'])
            
            for i in range(n_boxes):
                text = ocr_data['text'][i].strip()
                if not text:
                    continue
                
                # Buscar "Figure" seguido de número
                if text.lower() == 'figure':
                    # Buscar el número en las siguientes palabras
                    caption_parts = [text]
                    bbox_left = ocr_data['left'][i]
                    bbox_top = ocr_data['top'][i]
                    bbox_right = ocr_data['left'][i] + ocr_data['width'][i]
                    bbox_bottom = ocr_data['top'][i] + ocr_data['height'][i]
                    
                    # Buscar las siguientes palabras en la misma línea
                    for j in range(i + 1, min(i + 10, n_boxes)):
                        next_text = ocr_data['text'][j].strip()
                        if not next_text:
                            continue
                        
                        # Verificar que está en la misma línea (similar top)
                        if abs(ocr_data['top'][j] - bbox_top) > 20:
                            break
                        
                        caption_parts.append(next_text)
                        
                        # Actualizar bbox
                        bbox_right = max(bbox_right, ocr_data['left'][j] + ocr_data['width'][j])
                        bbox_bottom = max(bbox_bottom, ocr_data['top'][j] + ocr_data['height'][j])
                        
                        # Si encontramos punto, terminar caption
                        if '.' in next_text:
                            break
                    
                    caption = ' '.join(caption_parts)
                    
                    # Verificar que tiene formato Figure X-X
                    if re.search(r'Figure\s+\d+-\d+', caption, re.IGNORECASE):
                        # Expandir bbox hacia arriba para incluir la imagen
                        # Asumimos que la imagen está encima del caption
                        img_height = page_image.size[1]
                        estimated_top = max(0, bbox_top - 300)  # 300px arriba
                        
                        figure = DetectedFigure(
                            bbox=(bbox_left, estimated_top, bbox_right + 50, bbox_bottom),
                            caption=caption,
                            source_page=source_page
                        )
                        figures.append(figure)
                        self._detected_figures.append(figure)
            
            print(f"[FigureDetector] OCR encontró {len(figures)} figuras")
            return figures
            
        except Exception as e:
            print(f"[FigureDetector] Error en OCR: {e}")
            return []
    
    def find_matching_translation_files(
        self,
        figure: DetectedFigure,
        translation_dir: Path
    ) -> list[Path]:
        """
        Busca archivos de traducción que coincidan con una figura.
        
        Args:
            figure: Figura a buscar
            translation_dir: Directorio de imágenes traducidas
        
        Returns:
            Lista de archivos candidatos
        """
        if not translation_dir.exists():
            return []
        
        candidates = []
        
        # Buscar por número de figura
        if figure.figure_number:
            chapter, num = figure.figure_number.split('-')
            pattern = f"figura-{chapter}-{num}*.png"
            candidates = list(translation_dir.glob(pattern))
        
        # Si no hay coincidencias exactas, buscar por descripción
        if not candidates and figure.suggested_filename:
            # Buscar archivos similares
            base_name = figure.suggested_filename.replace('.png', '')
            all_files = list(translation_dir.glob("figura-*.png"))
            for f in all_files:
                if any(part in f.stem for part in base_name.split('-')[2:4]):
                    candidates.append(f)
        
        return candidates
