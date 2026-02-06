"""
Gestión de archivos y capítulos
"""

import re
from pathlib import Path
from typing import Optional

from .config import CHAPTERS_DIR, IMAGES_DIR, IMAGE_EXTENSIONS, BACKUP_PATTERNS


class FileManager:
    """Gestor de archivos del proyecto."""
    
    def __init__(self):
        self.chapters_dir = CHAPTERS_DIR
        self.images_dir = IMAGES_DIR
    
    def get_chapters(self) -> list[tuple[str, str, Path]]:
        """
        Obtiene la lista de capítulos disponibles.
        
        Returns:
            Lista de tuplas (número, título, ruta_archivo)
        """
        chapters = []
        
        if not self.chapters_dir.exists():
            return chapters
        
        for adoc_file in sorted(self.chapters_dir.glob("*.adoc")):
            name = adoc_file.stem
            match = re.match(r'(\d+)-(.+)', name)
            if match:
                num = match.group(1)
                title = match.group(2).replace('-', ' ').title()
                chapters.append((num, f"Cap. {num}: {title}", adoc_file))
        
        return chapters
    
    def extract_images_from_adoc(self, adoc_file: Path) -> list[dict]:
        """
        Extrae las imágenes referenciadas en un archivo .adoc.
        
        Args:
            adoc_file: Ruta al archivo .adoc
            
        Returns:
            Lista de diccionarios con información de las imágenes
        """
        images = []
        
        try:
            content = adoc_file.read_text(encoding='utf-8')
            # Patrón: image::NN/nombre_archivo[
            pattern = r'image::(\d+)/(\S+?)\['
            matches = re.findall(pattern, content)
            
            for match in matches:
                chapter_num = match[0]
                img_name = match[1]
                img_path = self.images_dir / chapter_num / img_name
                
                if img_path.exists():
                    images.append({
                        'path': img_path,
                        'name': img_name,
                        'chapter': chapter_num,
                    })
        except Exception as e:
            print(f"Error leyendo {adoc_file}: {e}")
        
        return images
    
    def find_new_images(
        self,
        chapter_dir: Path,
        referenced_names: Optional[set] = None
    ) -> list[dict]:
        """
        Encuentra imágenes en un directorio que no están referenciadas.
        
        Args:
            chapter_dir: Directorio del capítulo
            referenced_names: Set con nombres de imágenes ya referenciadas
            
        Returns:
            Lista de diccionarios con información de imágenes no referenciadas
        """
        if referenced_names is None:
            referenced_names = set()
        
        images = []
        
        for ext in IMAGE_EXTENSIONS:
            for img_path in sorted(chapter_dir.glob(ext)):
                # Excluir backups
                if any(pattern in img_path.name for pattern in BACKUP_PATTERNS):
                    continue
                
                # Excluir webp (versiones web)
                if img_path.suffix.lower() == '.webp':
                    continue
                
                # Excluir referenciadas
                if img_path.name in referenced_names:
                    continue
                
                images.append({
                    'path': img_path,
                    'name': img_path.name,
                    'chapter': chapter_dir.name,
                })
        
        return images
    
    def get_chapter_dir(self, chapter_num: str) -> Path:
        """Obtiene el directorio de imágenes de un capítulo."""
        return self.images_dir / chapter_num.zfill(2)
    
    def get_next_backup_path(self, image_path: Path) -> Path:
        """
        Obtiene la siguiente ruta de backup disponible.
        
        Args:
            image_path: Ruta de la imagen original
            
        Returns:
            Path: Ruta disponible para el backup
        """
        backup_path = image_path.with_suffix(".png.bak")
        counter = 1
        
        while backup_path.exists():
            backup_path = image_path.with_suffix(f".png.bak{counter}")
            counter += 1
        
        return backup_path
