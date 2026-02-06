"""
Módulo de detección de imágenes en páginas PDF.

Utiliza OpenCV para detectar regiones de imágenes en páginas PDF,
ignorando bloques de texto mediante análisis de densidad de píxeles.

Uso:
    from imagemanager.image_detector import ImageDetector
    
    detector = ImageDetector()
    regions = detector.detect(path_to_png)
    
    # O con threading para no bloquear UI:
    detector.detect_async(path, callback=on_detection_complete)
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Callable, Optional
import threading

import cv2
import numpy as np


@dataclass
class DetectedRegion:
    """Región detectada en la página."""
    x: int
    y: int
    w: int
    h: int
    area: int
    density: float
    is_image: bool  # True = imagen, False = texto/descartado
    
    @property
    def bbox(self) -> Tuple[int, int, int, int]:
        """Retorna bounding box como tupla (x, y, w, h)."""
        return (self.x, self.y, self.w, self.h)
    
    def __repr__(self):
        type_str = "IMG" if self.is_image else "TXT"
        return f"<{type_str} ({self.x},{self.y}) {self.w}x{self.h} d={self.density:.2f}>"


class ImageDetector:
    """
    Detector de imágenes en páginas PDF/PNG.
    
    Utiliza operaciones morfológicas y análisis de densidad para
    distinguir imágenes de bloques de texto.
    
    Parámetros de configuración:
        min_area: Área mínima en píxeles² para considerar una región
        min_density: Densidad mínima de píxeles (imágenes > 0.3, texto < 0.2)
        dilation_kernel_size: Tamaño del kernel para dilatación
        dilation_iterations: Número de iteraciones de dilatación
    """
    
    # Configuración por defecto
    DEFAULT_MIN_AREA = 5000           # Mínimo ~70x70 px
    DEFAULT_MIN_DENSITY = 0.25        # Imágenes tienen mayor densidad
    DEFAULT_MAX_DENSITY = 0.95        # Evitar bloques sólidos (separadores)
    DEFAULT_DILATION_KERNEL = 5       # Kernel para fusionar texto
    DEFAULT_DILATION_ITER = 3         # Iteraciones de dilatación
    DEFAULT_MIN_ASPECT_RATIO = 0.1    # Mínimo w/h (evitar líneas)
    DEFAULT_MAX_ASPECT_RATIO = 10.0   # Máximo w/h
    
    def __init__(
        self,
        min_area: int = DEFAULT_MIN_AREA,
        min_density: float = DEFAULT_MIN_DENSITY,
        max_density: float = DEFAULT_MAX_DENSITY,
        dilation_kernel: int = DEFAULT_DILATION_KERNEL,
        dilation_iterations: int = DEFAULT_DILATION_ITER,
        min_aspect_ratio: float = DEFAULT_MIN_ASPECT_RATIO,
        max_aspect_ratio: float = DEFAULT_MAX_ASPECT_RATIO,
        debug: bool = False
    ):
        self.min_area = min_area
        self.min_density = min_density
        self.max_density = max_density
        self.dilation_kernel = dilation_kernel
        self.dilation_iterations = dilation_iterations
        self.min_aspect_ratio = min_aspect_ratio
        self.max_aspect_ratio = max_aspect_ratio
        self.debug = debug
        
        # Estado interno
        self._last_debug_image: Optional[np.ndarray] = None
        self._last_all_regions: List[DetectedRegion] = []
    
    def detect(self, image_path: str | Path) -> List[DetectedRegion]:
        """
        Detecta imágenes en una página PNG.
        
        Args:
            image_path: Ruta al archivo PNG de la página
            
        Returns:
            Lista de DetectedRegion con is_image=True (solo imágenes)
        """
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {path}")
        
        print(f"[ImageDetector] Procesando: {path.name}")
        
        # 1. Cargar imagen
        img = cv2.imread(str(path))
        if img is None:
            raise ValueError(f"No se pudo cargar la imagen: {path}")
        
        original = img.copy()
        height, width = img.shape[:2]
        print(f"[ImageDetector] Tamaño: {width}x{height}")
        
        # 2. Convertir a escala de grises
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 3. Binarización (invertida: fondo negro, objetos blancos)
        # Usar umbral adaptativo para manejar variaciones de iluminación
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # 4. Guardar binaria original para cálculo de densidad
        binary_original = binary.copy()
        
        # 5. Operaciones morfológicas para fusionar texto
        # Kernel rectangular para fusionar texto horizontal
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, 
            (self.dilation_kernel * 3, self.dilation_kernel)
        )
        dilated = cv2.dilate(binary, kernel, iterations=self.dilation_iterations)
        
        # Segundo paso: kernel cuadrado para consolidar
        kernel_square = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (self.dilation_kernel, self.dilation_kernel)
        )
        dilated = cv2.dilate(dilated, kernel_square, iterations=2)
        
        # 6. Encontrar contornos
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        print(f"[ImageDetector] Contornos encontrados: {len(contours)}")
        
        # 7. Analizar cada contorno
        all_regions: List[DetectedRegion] = []
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            aspect_ratio = w / h if h > 0 else 0
            
            # Calcular densidad de píxeles en la región original
            roi = binary_original[y:y+h, x:x+w]
            white_pixels = cv2.countNonZero(roi)
            density = white_pixels / area if area > 0 else 0
            
            # Clasificar: ¿es imagen o texto?
            is_image = self._classify_region(area, density, aspect_ratio, w, h)
            
            region = DetectedRegion(
                x=x, y=y, w=w, h=h,
                area=area,
                density=density,
                is_image=is_image
            )
            all_regions.append(region)
            
            if self.debug:
                status = "✓ IMAGEN" if is_image else "✗ descartado"
                print(f"[ImageDetector]   {status}: {region}")
        
        # Ordenar por posición (arriba a abajo, izquierda a derecha)
        all_regions.sort(key=lambda r: (r.y, r.x))
        self._last_all_regions = all_regions
        
        # Generar imagen de debug si está habilitado
        if self.debug:
            self._generate_debug_image(original, all_regions)
        
        # Filtrar solo imágenes
        images = [r for r in all_regions if r.is_image]
        print(f"[ImageDetector] Imágenes detectadas: {len(images)} de {len(all_regions)} regiones")
        
        return images
    
    def _classify_region(
        self, 
        area: int, 
        density: float, 
        aspect_ratio: float,
        width: int,
        height: int
    ) -> bool:
        """
        Clasifica si una región es imagen o texto.
        
        Las imágenes típicamente tienen:
        - Mayor área
        - Mayor densidad de píxeles (bloques más sólidos)
        - Aspect ratio razonable (no muy alargado)
        
        El texto tiene:
        - Menor densidad (muchos huecos entre letras)
        - A veces muy alargado horizontalmente
        """
        # Filtro 1: Área mínima
        if area < self.min_area:
            return False
        
        # Filtro 2: Aspect ratio (evitar líneas y separadores)
        if aspect_ratio < self.min_aspect_ratio or aspect_ratio > self.max_aspect_ratio:
            return False
        
        # Filtro 3: Densidad de píxeles
        # Imágenes: densidad media-alta (0.25-0.95)
        # Texto: densidad baja (<0.20)
        # Separadores sólidos: densidad muy alta (>0.95)
        if density < self.min_density or density > self.max_density:
            return False
        
        # Filtro 4: Tamaño mínimo absoluto
        # Las imágenes suelen ser al menos 100x100
        if width < 80 or height < 80:
            return False
        
        return True
    
    def _generate_debug_image(
        self, 
        original: np.ndarray, 
        regions: List[DetectedRegion]
    ) -> np.ndarray:
        """Genera imagen con rectángulos de debug."""
        debug_img = original.copy()
        
        for region in regions:
            if region.is_image:
                # Verde para imágenes detectadas
                color = (0, 255, 0)
                thickness = 3
            else:
                # Rojo para regiones descartadas
                color = (0, 0, 255)
                thickness = 1
            
            cv2.rectangle(
                debug_img,
                (region.x, region.y),
                (region.x + region.w, region.y + region.h),
                color,
                thickness
            )
            
            # Etiqueta
            label = f"d={region.density:.2f}"
            cv2.putText(
                debug_img,
                label,
                (region.x, region.y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1
            )
        
        self._last_debug_image = debug_img
        return debug_img
    
    def save_debug_image(self, output_path: str | Path) -> bool:
        """
        Guarda la última imagen de debug generada.
        
        Returns:
            True si se guardó exitosamente
        """
        if self._last_debug_image is None:
            print("[ImageDetector] No hay imagen de debug disponible")
            return False
        
        output = Path(output_path)
        cv2.imwrite(str(output), self._last_debug_image)
        print(f"[ImageDetector] Debug guardado: {output}")
        return True
    
    def get_debug_image(self) -> Optional[np.ndarray]:
        """Retorna la última imagen de debug (BGR format)."""
        return self._last_debug_image
    
    def crop_region(
        self, 
        image_path: str | Path, 
        region: DetectedRegion,
        padding: int = 0
    ) -> np.ndarray:
        """
        Recorta una región de la imagen.
        
        Args:
            image_path: Ruta a la imagen original
            region: Región a recortar
            padding: Píxeles de margen adicional
            
        Returns:
            Imagen recortada (BGR format)
        """
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"No se pudo cargar: {image_path}")
        
        h, w = img.shape[:2]
        x1 = max(0, region.x - padding)
        y1 = max(0, region.y - padding)
        x2 = min(w, region.x + region.w + padding)
        y2 = min(h, region.y + region.h + padding)
        
        return img[y1:y2, x1:x2]
    
    def save_cropped_region(
        self,
        image_path: str | Path,
        region: DetectedRegion,
        output_path: str | Path,
        padding: int = 0
    ) -> bool:
        """
        Recorta y guarda una región como archivo PNG.
        
        Returns:
            True si se guardó exitosamente
        """
        try:
            cropped = self.crop_region(image_path, region, padding)
            cv2.imwrite(str(output_path), cropped)
            print(f"[ImageDetector] Recorte guardado: {output_path}")
            return True
        except Exception as e:
            print(f"[ImageDetector] Error guardando recorte: {e}")
            return False
    
    # ========== Threading Support ==========
    
    def detect_async(
        self,
        image_path: str | Path,
        callback: Callable[[List[DetectedRegion]], None],
        error_callback: Optional[Callable[[Exception], None]] = None
    ) -> threading.Thread:
        """
        Ejecuta detección en un hilo separado (no bloquea UI).
        
        Args:
            image_path: Ruta a la imagen
            callback: Función llamada con resultados al completar
            error_callback: Función llamada si hay error
            
        Returns:
            Thread object (ya iniciado)
            
        Ejemplo:
            def on_complete(regions):
                for r in regions:
                    print(r)
            
            detector.detect_async(path, callback=on_complete)
        """
        def worker():
            try:
                results = self.detect(image_path)
                callback(results)
            except Exception as e:
                print(f"[ImageDetector] Error en thread: {e}")
                if error_callback:
                    error_callback(e)
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        return thread


# ========== Funciones de conveniencia ==========

def detect_images(
    image_path: str | Path,
    debug: bool = False,
    **kwargs
) -> List[Tuple[int, int, int, int]]:
    """
    Función simple para detectar imágenes.
    
    Args:
        image_path: Ruta al archivo PNG
        debug: Si True, habilita logging detallado
        **kwargs: Parámetros adicionales para ImageDetector
        
    Returns:
        Lista de tuplas (x, y, w, h) de las imágenes detectadas
    """
    detector = ImageDetector(debug=debug, **kwargs)
    regions = detector.detect(image_path)
    return [r.bbox for r in regions]


def detect_and_save_debug(
    image_path: str | Path,
    output_path: str | Path,
    **kwargs
) -> List[DetectedRegion]:
    """
    Detecta imágenes y guarda imagen de debug.
    
    Returns:
        Lista de DetectedRegion con imágenes detectadas
    """
    detector = ImageDetector(debug=True, **kwargs)
    regions = detector.detect(image_path)
    detector.save_debug_image(output_path)
    return regions


# ========== CLI para testing ==========

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python image_detector.py <imagen.png> [--debug]")
        print("     python image_detector.py <imagen.png> --save-debug output.png")
        sys.exit(1)
    
    input_path = sys.argv[1]
    debug_mode = "--debug" in sys.argv
    
    if "--save-debug" in sys.argv:
        idx = sys.argv.index("--save-debug")
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]
            regions = detect_and_save_debug(input_path, output_path)
            print(f"\nResultados guardados en: {output_path}")
        else:
            print("Error: --save-debug requiere ruta de salida")
            sys.exit(1)
    else:
        bboxes = detect_images(input_path, debug=debug_mode)
        print(f"\n=== Imágenes detectadas: {len(bboxes)} ===")
        for i, (x, y, w, h) in enumerate(bboxes, 1):
            print(f"  {i}. ({x}, {y}, {w}, {h})")
