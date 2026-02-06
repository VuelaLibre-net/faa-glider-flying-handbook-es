"""
Manejo del portapapeles multiplataforma (Linux Wayland/X11, macOS, Windows)
"""

import os
import subprocess
import tempfile
from enum import Enum, auto
from pathlib import Path
from typing import Optional

from PIL import Image


class DesktopEnvironment(Enum):
    """Entornos de escritorio soportados."""
    WAYLAND = auto()
    X11 = auto()
    MACOS = auto()
    WINDOWS = auto()
    UNKNOWN = auto()


class ClipboardError(Exception):
    """Error base para operaciones de portapapeles."""
    pass


class NoImageInClipboardError(ClipboardError):
    """No hay imagen en el portapapeles."""
    pass


class ClipboardNotAvailableError(ClipboardError):
    """Las utilidades de portapapeles no están disponibles."""
    pass


class ClipboardHandler:
    """
    Gestor de portapapeles multiplataforma.
    
    Detecta automáticamente el entorno y utiliza las herramientas apropiadas.
    """
    
    def __init__(self):
        self.env = self._detect_environment()
        self._validate_tools()
    
    def _detect_environment(self) -> DesktopEnvironment:
        """Detecta el entorno de escritorio."""
        import platform
        
        system = platform.system()
        
        if system == "Darwin":
            return DesktopEnvironment.MACOS
        elif system == "Windows":
            return DesktopEnvironment.WINDOWS
        elif system == "Linux":
            wayland_display = os.environ.get('WAYLAND_DISPLAY')
            x11_display = os.environ.get('DISPLAY')
            
            if wayland_display:
                return DesktopEnvironment.WAYLAND
            elif x11_display:
                return DesktopEnvironment.X11
        
        return DesktopEnvironment.UNKNOWN
    
    def _validate_tools(self) -> None:
        """Valida que las herramientas necesarias estén instaladas."""
        if self.env == DesktopEnvironment.WAYLAND:
            if not self._command_exists('wl-copy') or not self._command_exists('wl-paste'):
                raise ClipboardNotAvailableError(
                    "Herramientas Wayland no encontradas. Instala: sudo apt install wl-clipboard"
                )
        elif self.env == DesktopEnvironment.X11:
            if not self._command_exists('xclip'):
                raise ClipboardNotAvailableError(
                    "Herramienta X11 no encontrada. Instala: sudo apt install xclip"
                )
    
    @staticmethod
    def _command_exists(command: str) -> bool:
        """Verifica si un comando existe en el sistema."""
        result = subprocess.run(['which', command], capture_output=True, text=True)
        return result.returncode == 0
    
    def get_image(self) -> Image.Image:
        """
        Obtiene una imagen del portapapeles.
        
        Returns:
            Image.Image: La imagen del portapapeles
            
        Raises:
            NoImageInClipboardError: Si no hay imagen en el portapapeles
        """
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            if self.env == DesktopEnvironment.WAYLAND:
                self._get_image_wayland(tmp_path)
            elif self.env == DesktopEnvironment.X11:
                self._get_image_x11(tmp_path)
            elif self.env == DesktopEnvironment.MACOS:
                self._get_image_macos(tmp_path)
            elif self.env == DesktopEnvironment.WINDOWS:
                self._get_image_windows(tmp_path)
            else:
                raise ClipboardNotAvailableError("Entorno no soportado")
            
            if os.path.getsize(tmp_path) == 0:
                raise NoImageInClipboardError("No hay imagen en el portapapeles")
            
            return Image.open(tmp_path)
            
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
    
    def _get_image_wayland(self, output_path: str) -> None:
        """Obtiene imagen del portapapeles en Wayland."""
        mime_types = ['image/png', 'image/jpeg', 'image/webp', 'image/bmp']
        result = None
        
        for mime_type in mime_types:
            result = subprocess.run(
                ['wl-paste', '--type', mime_type],
                capture_output=True
            )
            if result.returncode == 0 and result.stdout:
                break
        
        if result is None or result.returncode != 0 or not result.stdout:
            raise subprocess.CalledProcessError(1, 'wl-paste', stderr='No image in clipboard')
        
        with open(output_path, 'wb') as f:
            f.write(result.stdout)
    
    def _get_image_x11(self, output_path: str) -> None:
        """Obtiene imagen del portapapeles en X11."""
        subprocess.run(
            ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-o'],
            stdout=open(output_path, 'wb'),
            check=True
        )
    
    def _get_image_macos(self, output_path: str) -> None:
        """Obtiene imagen del portapapeles en macOS."""
        script = f'''
        set pngData to the clipboard as «class PNGf»
        set outFile to open for access POSIX path of POSIX file "{output_path}" with write permission
        write pngData to outFile
        close access outFile
        '''
        subprocess.run(['osascript', '-e', script], check=True, capture_output=True)
    
    def _get_image_windows(self, output_path: str) -> None:
        """Obtiene imagen del portapapeles en Windows."""
        from PIL import ImageGrab
        img = ImageGrab.grabclipboard()
        if img:
            img.save(output_path, "PNG")
        else:
            raise NoImageInClipboardError("No hay imagen en el portapapeles")
    
    def set_image(self, image: Image.Image) -> None:
        """Copia una imagen al portapapeles."""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            image.save(tmp_path, 'PNG')
            
            if self.env == DesktopEnvironment.WAYLAND:
                self._set_image_wayland(tmp_path)
            elif self.env == DesktopEnvironment.X11:
                self._set_image_x11(tmp_path)
            elif self.env == DesktopEnvironment.MACOS:
                self._set_image_macos(tmp_path)
            elif self.env == DesktopEnvironment.WINDOWS:
                self._set_image_windows(image)
                
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
    
    def _set_image_wayland(self, image_path: str) -> None:
        """Copia imagen al portapapeles en Wayland."""
        with open(image_path, 'rb') as f:
            subprocess.run(['wl-copy', '--type', 'image/png'], input=f.read(), check=True)
    
    def _set_image_x11(self, image_path: str) -> None:
        """Copia imagen al portapapeles en X11."""
        subprocess.run([
            'xclip', '-selection', 'clipboard', '-t', 'image/png', '-i', image_path
        ], check=True)
    
    def _set_image_macos(self, image_path: str) -> None:
        """Copia imagen al portapapeles en macOS."""
        subprocess.run(['osascript', '-e', f'set the clipboard to (read (POSIX file "{image_path}") as PNG picture)'])
    
    def _set_image_windows(self, image: Image.Image) -> None:
        """Copia imagen al portapapeles en Windows."""
        import io
        output = io.BytesIO()
        image.convert('RGB').save(output, format='BMP')
        data = output.getvalue()[14:]  # Remove BMP header
        output.close()
        
        import win32clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
    
    def has_image(self) -> bool:
        """Verifica si hay una imagen en el portapapeles."""
        try:
            self.get_image()
            return True
        except (NoImageInClipboardError, ClipboardError):
            return False
    
    @property
    def environment_name(self) -> str:
        """Nombre del entorno detectado."""
        return self.env.name.capitalize()


# Singleton
_clipboard_handler: Optional[ClipboardHandler] = None


def get_clipboard_handler() -> ClipboardHandler:
    """Obtiene la instancia singleton del ClipboardHandler."""
    global _clipboard_handler
    if _clipboard_handler is None:
        _clipboard_handler = ClipboardHandler()
    return _clipboard_handler
