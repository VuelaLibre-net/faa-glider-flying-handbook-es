"""
Procesamiento y compresión de imágenes
"""

import shutil
from pathlib import Path
from typing import Union

from PIL import Image, ImageDraw

from .config import DEFAULT_MAX_WIDTH, DEFAULT_QUALITY


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

    def compress(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        apply_rounded_corners: bool = True,
    ) -> int:
        """
        Comprime una imagen y la guarda como PNG optimizado.

        Args:
            input_path: Ruta de la imagen de entrada
            output_path: Ruta donde guardar la imagen comprimida
            apply_rounded_corners: Si True, aplica efecto de esquinas redondeadas

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

        # Convertir a RGB si es necesario
        img = self._convert_to_rgb(img)

        # Aplicar efecto de esquinas redondeadas suaves (si está habilitado)
        if apply_rounded_corners:
            img = self._apply_rounded_corners(img)

        # Cuantizar y guardar como PNG optimizado
        img.quantize(colors=256, method=2).save(output_path, "PNG", optimize=True)

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
