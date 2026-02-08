"""
Procesamiento y compresión de imágenes

Algoritmo inteligente que detecta el tipo de imagen:
- Fotografías: Mantiene calidad con compresión JPEG de alta calidad
- Ilustraciones/Diagramas: Usa paleta optimizada para texto nítido
"""

import shutil
from pathlib import Path
from typing import Union

from PIL import Image, ImageDraw, ImageStat

from .config import DEFAULT_MAX_WIDTH, DEFAULT_QUALITY


class ImageType:
    """Tipos de imagen detectables."""
    PHOTO = "photo"           # Fotografía con muchos colores
    ILLUSTRATION = "illustration"  # Ilustración, diagrama con texto
    MIXED = "mixed"           # Contenido mixto


class ImageProcessor:
    """Procesador de imágenes para el manual de vuelo."""

    def __init__(
        self, max_width: int = DEFAULT_MAX_WIDTH, quality: int = DEFAULT_QUALITY
    ):
        """
        Inicializa el procesador.

        Args:
            max_width: Ancho máximo para redimensionar
            quality: Calidad de compresión (0-100)
        """
        self.max_width = max_width
        self.quality = quality

    def detect_image_type(self, img: Image.Image) -> str:
        """
        Detecta si una imagen es fotografía o ilustración/diagrama.
        
        Usa análisis de histograma y entropía de colores para determinar
        el tipo de contenido.
        
        Args:
            img: Imagen PIL
            
        Returns:
            str: ImageType.PHOTO, ImageType.ILLUSTRATION o ImageType.MIXED
        """
        # Convertir a RGB para análisis
        if img.mode not in ('RGB', 'RGBA'):
            img_rgb = img.convert('RGB')
        else:
            img_rgb = img
        
        # Muestrear para análisis rápido (máximo 800px)
        max_analysis_size = 800
        if max(img_rgb.size) > max_analysis_size:
            ratio = max_analysis_size / max(img_rgb.size)
            new_size = (int(img_rgb.size[0] * ratio), int(img_rgb.size[1] * ratio))
            img_rgb = img_rgb.resize(new_size, Image.Resampling.LANCZOS)
        
        # Contar colores únicos
        pixels = list(img_rgb.getdata())
        unique_colors = len(set(pixels))
        total_pixels = len(pixels)
        color_ratio = unique_colors / total_pixels
        
        # Calcular varianza de brillo (detecta gradientes suaves vs bordes duros)
        stat = ImageStat.Stat(img_rgb)
        variance = sum(stat.var) / 3  # Promedio de varianza RGB
        
        # Detectar bordes duros (característico de diagramas)
        edges = self._detect_edge_density(img_rgb)
        
        # Heurísticas de clasificación
        # Fotos: Muchos colores únicos (>30%), varianza media-alta, bordes suaves
        # Diagramas: Pocos colores (<15%), baja varianza, bordes duros
        
        if color_ratio > 0.30 and variance > 1000 and edges < 0.15:
            return ImageType.PHOTO
        elif color_ratio < 0.15 or (edges > 0.20 and variance < 800):
            return ImageType.ILLUSTRATION
        else:
            return ImageType.MIXED
    
    def _detect_edge_density(self, img: Image.Image) -> float:
        """
        Detecta la densidad de bordes en la imagen.
        
        Args:
            img: Imagen RGB
            
        Returns:
            float: Proporción de píxeles de borde (0-1)
        """
        # Convertir a escala de grises y aplicar filtro de Sobel simple
        gray = img.convert('L')
        pixels = list(gray.getdata())
        width, height = gray.size
        
        if width < 3 or height < 3:
            return 0.0
        
        edge_pixels = 0
        threshold = 30  # Diferencia de intensidad para considerar borde
        
        # Muestrear cada 4 píxeles para velocidad
        for y in range(1, height - 1, 2):
            for x in range(1, width - 1, 2):
                idx = y * width + x
                current = pixels[idx]
                right = pixels[idx + 1]
                below = pixels[idx + width]
                
                if abs(current - right) > threshold or abs(current - below) > threshold:
                    edge_pixels += 1
        
        sampled_pixels = ((height // 2) * (width // 2))
        return edge_pixels / sampled_pixels if sampled_pixels > 0 else 0.0

    def compress(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        apply_rounded_corners: bool = True,
        force_type: str = None,
    ) -> int:
        """
        Comprime una imagen adaptativamente según su tipo.
        
        Detecta automáticamente si es fotografía o ilustración y aplica
        el algoritmo de compresión más adecuado.

        Args:
            input_path: Ruta de la imagen de entrada
            output_path: Ruta donde guardar la imagen comprimida
            apply_rounded_corners: Si True, aplica efecto de esquinas redondeadas
            force_type: Forzar tipo ('photo', 'illustration', 'mixed' o None para auto)

        Returns:
            int: Tamaño del archivo resultante en bytes
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        # Cargar imagen
        img = Image.open(input_path)

        # Redimensionar si es necesario
        orig_width = img.size[0]
        if orig_width > self.max_width:
            ratio = self.max_width / orig_width
            new_height = int(img.size[1] * ratio)
            img = img.resize((self.max_width, new_height), Image.Resampling.LANCZOS)

        # Detectar tipo de imagen
        if force_type:
            img_type = force_type
        else:
            img_type = self.detect_image_type(img)
        
        print(f"[ImageProcessor] Tipo detectado: {img_type} para {input_path.name}")

        # Aplicar efecto de esquinas redondeadas antes de conversión RGB
        if apply_rounded_corners:
            img = self._apply_rounded_corners(img)

        # Estrategia de compresión según tipo
        if img_type == ImageType.PHOTO:
            # Fotos: JPEG de alta calidad (mejor para gradientes)
            img = self._convert_to_rgb(img)
            output_path_jpg = output_path.with_suffix('.jpg')
            img.save(
                output_path_jpg, 
                "JPEG", 
                quality=92, 
                optimize=True,
                progressive=True
            )
            # Renombrar a .png para consistencia (aunque es JPEG)
            # O mejor, mantener la extensión original
            if output_path.suffix.lower() == '.png':
                # Guardar como PNG pero sin cuantización agresiva
                img.save(output_path, "PNG", optimize=True)
            else:
                output_path = output_path_jpg
                
        elif img_type == ImageType.ILLUSTRATION:
            # Ilustraciones: PNG con paleta optimizada
            img = self._convert_to_rgb(img)
            # Cuantización adaptativa para ilustraciones
            img_optimized = img.quantize(
                colors=128,  # Menos colores suficientes para diagramas
                method=2,     # Median cut
                dither=Image.Dither.NONE  # Sin dither para texto nítido
            )
            img_optimized.save(output_path, "PNG", optimize=True)
            
        else:  # MIXED
            # Contenido mixto: PNG con cuantización moderada
            img = self._convert_to_rgb(img)
            img_optimized = img.quantize(
                colors=192,  # Más colores para contenido mixto
                method=2,
                dither=Image.Dither.FLOYDSTEINBERG  # Dither suave
            )
            img_optimized.save(output_path, "PNG", optimize=True)

        return output_path.stat().st_size

    def _convert_to_rgb(self, img: Image.Image) -> Image.Image:
        """Convierte una imagen a modo RGB."""
        if img.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            if img.mode == "RGBA":
                bg.paste(img, mask=img.split()[-1])
            else:
                bg.paste(img)
            return bg
        elif img.mode != "RGB":
            return img.convert("RGB")
        return img

    def _apply_rounded_corners(
        self, img: Image.Image, radius_percent: float = 1.5
    ) -> Image.Image:
        """
        Aplica efecto de esquinas redondeadas suaves a una imagen.

        Args:
            img: Imagen PIL
            radius_percent: Porcentaje del ancho para el radio (default: 1.5%)

        Returns:
            Image.Image: Imagen con esquinas redondeadas (modo RGBA)
        """
        # Calcular radio proporcional (1.5% del ancho)
        width = img.size[0]
        radius = int(width * radius_percent / 100)
        # Limitar entre 8-24px para estética consistente
        radius = max(8, min(radius, 24))

        # Convertir a RGBA para soportar transparencia
        img_rgba = img.convert("RGBA")

        # Crear máscara con esquinas redondeadas
        mask = Image.new("L", img_rgba.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle(
            (0, 0, img_rgba.size[0], img_rgba.size[1]), radius=radius, fill=255
        )

        # Aplicar máscara al canal alpha
        r, g, b, a = img_rgba.split()
        a = Image.composite(a, Image.new("L", img_rgba.size, 0), mask)
        img_rgba.putalpha(a)

        return img_rgba

    def create_thumbnail(
        self, image_path: Union[str, Path], size: tuple[int, int] = (140, 100)
    ) -> Image.Image:
        """
        Crea una miniatura de una imagen.

        Args:
            image_path: Ruta de la imagen
            size: Tamaño de la miniatura (ancho, alto)

        Returns:
            Image.Image: Miniatura
        """
        img = Image.open(image_path)
        img.thumbnail(size, Image.Resampling.LANCZOS)
        return img

    def get_image_info(self, image_path: Union[str, Path]) -> dict:
        """
        Obtiene información de una imagen.

        Args:
            image_path: Ruta de la imagen

        Returns:
            dict: Información de la imagen (tamaño, dimensiones, etc.)
        """
        path = Path(image_path)
        img = Image.open(path)

        return {
            "path": path,
            "name": path.name,
            "size_bytes": path.stat().st_size,
            "size_kb": path.stat().st_size / 1024,
            "width": img.size[0],
            "height": img.size[1],
            "mode": img.mode,
            "format": img.format,
        }

    @staticmethod
    def create_backup(image_path: Union[str, Path], max_backups: int = 100) -> Path:
        """
        Crea un backup de una imagen.

        Args:
            image_path: Ruta de la imagen a respaldar
            max_backups: Número máximo de backups a mantener

        Returns:
            Path: Ruta del backup creado
        """
        path = Path(image_path)
        backup_path = path.with_suffix(".png.bak")

        # Encontrar nombre disponible
        counter = 1
        while backup_path.exists() and counter < max_backups:
            backup_path = path.with_suffix(f".png.bak{counter}")
            counter += 1

        shutil.copy2(path, backup_path)
        return backup_path


def open_folder_in_explorer(path: Union[str, Path]):
    """Abre la carpeta contenedora en el explorador de archivos."""
    import platform
    import subprocess

    folder = Path(path).parent
    system = platform.system()

    try:
        if system == "Windows":
            subprocess.run(["explorer", str(folder)])
        elif system == "Darwin":  # macOS
            subprocess.run(["open", str(folder)])
        else:  # Linux
            subprocess.run(["xdg-open", str(folder)])
    except Exception as e:
        raise RuntimeError(f"No se pudo abrir la carpeta: {e}")
