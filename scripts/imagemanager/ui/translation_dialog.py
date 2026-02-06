"""
Diálogos para la funcionalidad de traducción
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from PIL import Image, ImageTk

from ..translation import TranslationManager, TranslationError


class TranslationDialog:
    """Diálogo para guardar imágenes traducidas."""
    
    def __init__(
        self,
        parent,
        image: Image.Image,
        default_dir: Path,
        translation_manager: TranslationManager,
        on_save_callback=None
    ):
        """
        Inicializa el diálogo.
        
        Args:
            parent: Ventana padre
            image: Imagen traducida
            default_dir: Directorio por defecto para guardar
            translation_manager: Instancia del gestor de traducción
            on_save_callback: Callback a llamar cuando se guarde
        """
        self.parent = parent
        self.image = image
        self.default_dir = default_dir
        self.translation_manager = translation_manager
        self.on_save_callback = on_save_callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Guardar imagen traducida")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_ui()
    
    def _create_ui(self):
        """Crea la interfaz del diálogo."""
        # Preview
        preview_frame = ttk.Frame(self.dialog, padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Redimensionar para preview
        img_copy = self.image.copy()
        img_copy.thumbnail((550, 350), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img_copy)
        
        preview_label = ttk.Label(preview_frame, image=photo)
        preview_label.image = photo
        preview_label.pack()
        
        ttk.Label(
            preview_frame,
            text="Vista previa de la imagen traducida",
            font=("Helvetica", 10, "italic"),
            foreground="gray"
        ).pack(pady=(5, 0))
        
        # Opciones de guardado
        options_frame = ttk.LabelFrame(self.dialog, text="Opciones de guardado", padding="10")
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Nombre de archivo
        name_frame = ttk.Frame(options_frame)
        name_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(name_frame, text="Nombre:").pack(side=tk.LEFT)
        self.filename_var = tk.StringVar(value="figura_translated.png")
        ttk.Entry(name_frame, textvariable=self.filename_var, width=40).pack(side=tk.LEFT, padx=5)
        
        # Directorio
        ttk.Label(options_frame, text=f"Directorio: {self.default_dir}").pack(anchor=tk.W)
        
        # Botones
        buttons_frame = ttk.Frame(self.dialog, padding="10")
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="💾 Guardar", command=self._save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="📋 Copiar", command=self._copy_to_clipboard).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="❌ Cancelar", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _save(self):
        """Guarda la imagen."""
        filename = self.filename_var.get()
        if not filename.endswith('.png'):
            filename += '.png'
        
        save_path = self.default_dir / filename
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.image.save(save_path, "PNG", optimize=True)
        messagebox.showinfo("Éxito", f"Imagen guardada:\n{save_path}")
        
        if self.on_save_callback:
            self.on_save_callback()
        
        self.dialog.destroy()
    
    def _copy_to_clipboard(self):
        """Copia la imagen al portapapeles."""
        try:
            self.translation_manager.set_clipboard_image(self.image)
            messagebox.showinfo("Copiado", "Imagen copiada al clipboard.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar: {e}")


class TranslationProgressDialog:
    """Diálogo de progreso para traducciones."""
    
    def __init__(self, parent, title: str = "Traduciendo..."):
        """
        Inicializa el diálogo de progreso.
        
        Args:
            parent: Ventana padre
            title: Título del diálogo
        """
        self.parent = parent
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x150")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        self._create_ui()
    
    def _create_ui(self):
        """Crea la interfaz."""
        frame = ttk.Frame(self.dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_label = ttk.Label(
            frame,
            text="Enviando imagen a Gemini...",
            font=("Helvetica", 10)
        )
        self.status_label.pack(pady=(0, 20))
        
        self.progress = ttk.Progressbar(frame, mode='indeterminate', length=300)
        self.progress.pack()
        self.progress.start()
    
    def set_status(self, text: str):
        """Actualiza el texto de estado."""
        self.status_label.config(text=text)
        self.parent.update_idletasks()
    
    def close(self):
        """Cierra el diálogo."""
        self.progress.stop()
        self.dialog.destroy()
