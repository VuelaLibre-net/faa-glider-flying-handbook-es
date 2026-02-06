"""
Temas y estilos para el Gestor de Imágenes
"""

import tkinter as tk
from tkinter import ttk


class Theme:
    """Tema moderno para la aplicación."""
    
    # Colores principales
    PRIMARY = '#2563EB'           # Azul profesional
    PRIMARY_HOVER = '#1D4ED8'
    SUCCESS = '#10B981'           # Verde éxito
    SUCCESS_HOVER = '#059669'
    WARNING = '#F59E0B'           # Naranja advertencia
    DANGER = '#EF4444'            # Rojo error
    
    # Fondos
    BACKGROUND = '#F9FAFB'        # Fondo general
    SURFACE = '#FFFFFF'           # Superficie (cards, paneles)
    SURFACE_HOVER = '#F3F4F6'
    SIDEBAR_BG = '#1F2937'        # Fondo sidebar oscuro
    SIDEBAR_TEXT = '#F9FAFB'
    SIDEBAR_SELECTED = '#374151'
    
    # Texto
    TEXT = '#111827'
    TEXT_SECONDARY = '#6B7280'
    TEXT_MUTED = '#9CA3AF'
    
    # Bordes
    BORDER = '#E5E7EB'
    BORDER_FOCUS = '#3B82F6'
    
    # Estados
    SELECTED = '#DBEAFE'
    SELECTED_BORDER = '#2563EB'
    
    @classmethod
    def configure_styles(cls, root):
        """Configura los estilos ttk para el tema."""
        style = ttk.Style(root)
        
        # Frame general
        style.configure('TFrame', background=cls.BACKGROUND)
        style.configure('TLabel', background=cls.BACKGROUND, foreground=cls.TEXT)
        
        # Frame de superficie (cards)
        style.configure('Surface.TFrame', background=cls.SURFACE)
        style.configure('Surface.TLabel', background=cls.SURFACE, foreground=cls.TEXT)
        
        # Sidebar
        style.configure('Sidebar.TFrame', background=cls.SIDEBAR_BG)
        style.configure('Sidebar.TLabel', 
                       background=cls.SIDEBAR_BG, 
                       foreground=cls.SIDEBAR_TEXT,
                       font=('Helvetica', 10))
        style.configure('SidebarTitle.TLabel',
                       background=cls.SIDEBAR_BG,
                       foreground=cls.SIDEBAR_TEXT,
                       font=('Helvetica', 12, 'bold'))
        
        # Botones
        style.configure('TButton', 
                       font=('Helvetica', 9),
                       padding=6)
        
        # Botón primario
        style.configure('Primary.TButton',
                       font=('Helvetica', 9, 'bold'))
        
        # Botón de toolbar
        style.configure('Toolbar.TButton',
                       font=('Helvetica', 9),
                       padding=4)
        
        # Combobox
        style.configure('TCombobox', padding=4)
        
        # Scale
        style.configure('Horizontal.TScale', background=cls.BACKGROUND)
        
        # Progressbar
        style.configure('Horizontal.TProgressbar', 
                       thickness=8,
                       background=cls.PRIMARY)
        
        # Notebook (pestañas)
        style.configure('TNotebook', background=cls.BACKGROUND, tabmargins=[2, 5, 2, 0])
        style.configure('TNotebook.Tab', padding=[10, 4], font=('Helvetica', 9))
        
        # Scrollbar moderna
        style.element_create('Custom.Vertical.Scrollbar.trough', 'from', 'default')
        style.element_create('Custom.Vertical.Scrollbar.thumb', 'from', 'default')
        
        return style


class CardFrame(tk.Frame):
    """Frame con estilo de card (sombra, bordes redondeados)."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=Theme.SURFACE, **kwargs)
        self.configure(highlightbackground=Theme.BORDER, highlightthickness=1)


class SidebarButton(tk.Frame):
    """Botón personalizado para el sidebar."""
    
    def __init__(self, parent, text, icon='', command=None, **kwargs):
        super().__init__(parent, bg=Theme.SIDEBAR_BG, cursor='hand2', **kwargs)
        
        self.command = command
        self.selected = False
        
        self.label = tk.Label(
            self,
            text=f'{icon}  {text}',
            bg=Theme.SIDEBAR_BG,
            fg=Theme.SIDEBAR_TEXT,
            font=('Helvetica', 10),
            padx=15,
            pady=8,
            anchor='w',
            cursor='hand2'
        )
        self.label.pack(fill=tk.X, expand=True)
        
        # Bindings
        for widget in (self, self.label):
            widget.bind('<Enter>', self._on_enter)
            widget.bind('<Leave>', self._on_leave)
            widget.bind('<Button-1>', self._on_click)
        
        self.label.bind('<Button-1>', self._on_click)
    
    def _on_enter(self, event):
        if not self.selected:
            self.configure(bg=Theme.SIDEBAR_SELECTED)
            self.label.configure(bg=Theme.SIDEBAR_SELECTED)
    
    def _on_leave(self, event):
        if not self.selected:
            self.configure(bg=Theme.SIDEBAR_BG)
            self.label.configure(bg=Theme.SIDEBAR_BG)
    
    def _on_click(self, event):
        if self.command:
            self.command()
    
    def set_selected(self, selected):
        """Marca el botón como seleccionado."""
        self.selected = selected
        if selected:
            self.configure(bg=Theme.PRIMARY)
            self.label.configure(bg=Theme.PRIMARY, fg='white')
        else:
            self.configure(bg=Theme.SIDEBAR_BG)
            self.label.configure(bg=Theme.SIDEBAR_BG, fg=Theme.SIDEBAR_TEXT)


class ToolbarButton(tk.Frame):
    """Botón para la toolbar con icono y tooltip."""
    
    def __init__(self, parent, text, icon='', command=None, state='normal', **kwargs):
        super().__init__(parent, bg=Theme.SURFACE, **kwargs)
        
        self.command = command
        self.enabled = state == 'normal'
        
        self.label = tk.Label(
            self,
            text=f'{icon} {text}',
            bg=Theme.SURFACE,
            fg=Theme.TEXT if self.enabled else Theme.TEXT_MUTED,
            font=('Helvetica', 9),
            padx=10,
            pady=5,
            cursor='hand2' if self.enabled else 'arrow'
        )
        self.label.pack()
        
        if self.enabled:
            for widget in (self, self.label):
                widget.bind('<Enter>', self._on_enter)
                widget.bind('<Leave>', self._on_leave)
                widget.bind('<Button-1>', self._on_click)
    
    def _on_enter(self, event):
        self.configure(bg=Theme.SURFACE_HOVER, highlightbackground=Theme.PRIMARY, highlightthickness=1)
        self.label.configure(bg=Theme.SURFACE_HOVER, fg=Theme.PRIMARY)
    
    def _on_leave(self, event):
        self.configure(bg=Theme.SURFACE, highlightthickness=0)
        self.label.configure(bg=Theme.SURFACE, fg=Theme.TEXT)
    
    def _on_click(self, event):
        if self.command and self.enabled:
            self.command()
    
    def set_enabled(self, enabled):
        """Habilita o deshabilita el botón."""
        self.enabled = enabled
        self.label.configure(
            fg=Theme.TEXT if enabled else Theme.TEXT_MUTED,
            cursor='hand2' if enabled else 'arrow'
        )


class ImageThumbnail(tk.Frame):
    """Thumbnail de imagen con información."""
    
    THUMB_SIZE = (140, 105)
    
    def __init__(self, parent, img_info, on_click=None, on_double_click=None, 
                 on_right_click=None, **kwargs):
        super().__init__(parent, bg=Theme.SURFACE, **kwargs)
        
        self.img_info = img_info
        self.on_click = on_click
        self.on_double_click = on_double_click
        self.on_right_click = on_right_click
        self.selected = False
        
        self.configure(
            highlightbackground=Theme.BORDER,
            highlightthickness=1,
            padx=5,
            pady=5
        )
        
        # Canvas para la imagen
        self.canvas = tk.Canvas(
            self,
            width=self.THUMB_SIZE[0],
            height=self.THUMB_SIZE[1],
            bg=Theme.BACKGROUND,
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Cargar imagen
        self._load_image()
        
        # Info
        self.info_frame = tk.Frame(self, bg=Theme.SURFACE)
        self.info_frame.pack(fill=tk.X, pady=(5, 0))
        
        name = img_info['name'][:18] + '...' if len(img_info['name']) > 18 else img_info['name']
        tk.Label(
            self.info_frame,
            text=name,
            bg=Theme.SURFACE,
            fg=Theme.TEXT,
            font=('Helvetica', 8),
            anchor='w'
        ).pack(fill=tk.X)
        
        size_kb = img_info['path'].stat().st_size / 1024
        tk.Label(
            self.info_frame,
            text=f"{size_kb:.0f} KB",
            bg=Theme.SURFACE,
            fg=Theme.TEXT_SECONDARY,
            font=('Helvetica', 7),
            anchor='w'
        ).pack(fill=tk.X)
        
        # Bindings
        for widget in (self, self.canvas, self.info_frame):
            widget.bind('<Button-1>', self._on_click)
            widget.bind('<Double-Button-1>', self._on_double_click)
            widget.bind('<Button-3>', self._on_right_click)
            widget.bind('<Enter>', self._on_enter)
            widget.bind('<Leave>', self._on_leave)
    
    def _load_image(self):
        """Carga la miniatura de la imagen."""
        try:
            from PIL import Image, ImageTk
            img = Image.open(self.img_info['path'])
            img.thumbnail(self.THUMB_SIZE, Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(
                self.THUMB_SIZE[0] // 2,
                self.THUMB_SIZE[1] // 2,
                image=self.photo
            )
        except Exception:
            self.canvas.create_text(
                self.THUMB_SIZE[0] // 2,
                self.THUMB_SIZE[1] // 2,
                text="Error",
                fill=Theme.DANGER
            )
    
    def _on_enter(self, event):
        if not self.selected:
            self.configure(highlightbackground=Theme.PRIMARY)
    
    def _on_leave(self, event):
        if not self.selected:
            self.configure(highlightbackground=Theme.BORDER)
    
    def _on_click(self, event):
        self.set_selected(True)
        if self.on_click:
            self.on_click(self.img_info)
    
    def _on_double_click(self, event):
        if self.on_double_click:
            self.on_double_click(self.img_info)
    
    def _on_right_click(self, event):
        if self.on_right_click:
            self.on_right_click(event, self.img_info)
    
    def set_selected(self, selected):
        """Marca el thumbnail como seleccionado."""
        self.selected = selected
        if selected:
            self.configure(
                highlightbackground=Theme.SELECTED_BORDER,
                highlightthickness=2,
                bg=Theme.SELECTED
            )
            self.info_frame.configure(bg=Theme.SELECTED)
            for widget in self.info_frame.winfo_children():
                widget.configure(bg=Theme.SELECTED)
        else:
            self.configure(
                highlightbackground=Theme.BORDER,
                highlightthickness=1,
                bg=Theme.SURFACE
            )
            self.info_frame.configure(bg=Theme.SURFACE)
            for widget in self.info_frame.winfo_children():
                widget.configure(bg=Theme.SURFACE)


class ShadowThumbnail(tk.Frame):
    """Placeholder para imagen referenciada pero inexistente."""
    
    THUMB_SIZE = (140, 105)
    
    def __init__(self, parent, img_info, on_click=None, on_right_click=None, **kwargs):
        super().__init__(parent, bg=Theme.SURFACE, **kwargs)
        
        self.img_info = img_info
        self.on_click = on_click
        self.on_right_click = on_right_click
        self.selected = False
        
        self.configure(
            highlightbackground=Theme.BORDER,
            highlightthickness=1,
            padx=5,
            pady=5
        )
        
        # Canvas para el placeholder
        self.canvas = tk.Canvas(
            self,
            width=self.THUMB_SIZE[0],
            height=self.THUMB_SIZE[1],
            bg='#E5E7EB',  # Gris claro
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Dibujar icono de cámara
        self.canvas.create_text(
            self.THUMB_SIZE[0] // 2,
            self.THUMB_SIZE[1] // 2 - 10,
            text="📷",
            font=('Helvetica', 24),
            fill='#9CA3AF'
        )
        self.canvas.create_text(
            self.THUMB_SIZE[0] // 2,
            self.THUMB_SIZE[1] // 2 + 20,
            text="No existe",
            font=('Helvetica', 8),
            fill='#6B7280'
        )
        
        # Info
        self.info_frame = tk.Frame(self, bg=Theme.SURFACE)
        self.info_frame.pack(fill=tk.X, pady=(5, 0))
        
        name = img_info['name'][:18] + '...' if len(img_info['name']) > 18 else img_info['name']
        tk.Label(
            self.info_frame,
            text=name,
            bg=Theme.SURFACE,
            fg=Theme.TEXT_MUTED,
            font=('Helvetica', 8, 'italic'),
            anchor='w'
        ).pack(fill=tk.X)
        
        tk.Label(
            self.info_frame,
            text="Pendiente",
            bg=Theme.SURFACE,
            fg=Theme.WARNING,
            font=('Helvetica', 7),
            anchor='w'
        ).pack(fill=tk.X)
        
        # Bindings
        for widget in (self, self.canvas, self.info_frame):
            widget.bind('<Button-1>', self._on_click)
            widget.bind('<Button-3>', self._on_right_click)
            widget.bind('<Enter>', self._on_enter)
            widget.bind('<Leave>', self._on_leave)
    
    def _on_enter(self, event):
        if not self.selected:
            self.configure(highlightbackground=Theme.WARNING)
    
    def _on_leave(self, event):
        if not self.selected:
            self.configure(highlightbackground=Theme.BORDER)
    
    def _on_click(self, event):
        self.set_selected(True)
        if self.on_click:
            self.on_click(self.img_info)
    
    def _on_right_click(self, event):
        if self.on_right_click:
            self.on_right_click(event, self.img_info)
    
    def set_selected(self, selected):
        """Marca el thumbnail como seleccionado."""
        self.selected = selected
        if selected:
            self.configure(
                highlightbackground=Theme.WARNING,
                highlightthickness=2,
                bg='#FEF3C7'  # Amarillo claro
            )
            self.canvas.configure(bg='#FDE68A')
            self.info_frame.configure(bg='#FEF3C7')
            for widget in self.info_frame.winfo_children():
                widget.configure(bg='#FEF3C7')
        else:
            self.configure(
                highlightbackground=Theme.BORDER,
                highlightthickness=1,
                bg=Theme.SURFACE
            )
            self.canvas.configure(bg='#E5E7EB')
            self.info_frame.configure(bg=Theme.SURFACE)
            for widget in self.info_frame.winfo_children():
                widget.configure(bg=Theme.SURFACE)


class PdfPageThumbnail(tk.Frame):
    """Thumbnail de página PDF."""
    
    THUMB_SIZE = (100, 140)
    
    def __init__(self, parent, page_num, page_image=None, on_click=None, on_double_click=None, **kwargs):
        super().__init__(parent, bg=Theme.SURFACE, **kwargs)
        
        self.page_num = page_num
        self.on_click = on_click
        self.on_double_click = on_double_click
        self.selected = False
        
        self.configure(
            highlightbackground=Theme.BORDER,
            highlightthickness=1,
            padx=3,
            pady=3
        )
        
        # Canvas para la página
        self.canvas = tk.Canvas(
            self,
            width=self.THUMB_SIZE[0],
            height=self.THUMB_SIZE[1],
            bg='white',
            highlightthickness=0
        )
        self.canvas.pack()
        
        if page_image:
            self._load_image(page_image)
        else:
            # Placeholder
            self.canvas.create_text(
                self.THUMB_SIZE[0] // 2,
                self.THUMB_SIZE[1] // 2,
                text=f"Pág {page_num}",
                font=('Helvetica', 9),
                fill=Theme.TEXT_SECONDARY
            )
        
        # Número de página
        tk.Label(
            self,
            text=f"Página {page_num}",
            bg=Theme.SURFACE,
            fg=Theme.TEXT_SECONDARY,
            font=('Helvetica', 7)
        ).pack()
        
        # Bindings
        for widget in (self, self.canvas):
            widget.bind('<Button-1>', self._on_click)
            widget.bind('<Double-Button-1>', self._on_double_click)
            widget.bind('<Enter>', self._on_enter)
            widget.bind('<Leave>', self._on_leave)
    
    def _load_image(self, page_image):
        """Carga la imagen de la página."""
        try:
            from PIL import ImageTk
            page_image.thumbnail(self.THUMB_SIZE)
            self.photo = ImageTk.PhotoImage(page_image)
            self.canvas.create_image(
                self.THUMB_SIZE[0] // 2,
                self.THUMB_SIZE[1] // 2,
                image=self.photo
            )
        except Exception:
            self.canvas.create_text(
                self.THUMB_SIZE[0] // 2,
                self.THUMB_SIZE[1] // 2,
                text="Error",
                fill=Theme.DANGER
            )
    
    def _on_enter(self, event):
        if not self.selected:
            self.configure(highlightbackground=Theme.PRIMARY)
    
    def _on_leave(self, event):
        if not self.selected:
            self.configure(highlightbackground=Theme.BORDER)
    
    def _on_click(self, event):
        self.set_selected(True)
        if self.on_click:
            self.on_click(self.page_num)
    
    def _on_double_click(self, event):
        if self.on_double_click:
            self.on_double_click(self.page_num)
    
    def set_selected(self, selected):
        """Marca el thumbnail como seleccionado."""
        self.selected = selected
        if selected:
            self.configure(
                highlightbackground=Theme.SELECTED_BORDER,
                highlightthickness=2
            )
        else:
            self.configure(
                highlightbackground=Theme.BORDER,
                highlightthickness=1
            )


class PreviewModal(tk.Toplevel):
    """Modal para vista previa de imagen ampliada."""
    
    def __init__(self, parent, img_info, on_edit=None, on_compress=None):
        super().__init__(parent)
        self.img_info = img_info
        self.on_edit = on_edit
        self.on_compress = on_compress
        
        print(f"[Debug] Abriendo PreviewModal para: {img_info['name']}")
        self.title(f"Vista previa: {img_info['name']}")
        self.configure(bg=Theme.BACKGROUND)
        self.geometry("800x600")
        self.transient(parent)
        
        self._create_ui()
        self._load_image()
        
        # Centrar en pantalla
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 800) // 2
        y = (self.winfo_screenheight() - 600) // 2
        self.geometry(f"+{x}+{y}")
        
        # Cerrar con Escape
        self.bind("<Escape>", lambda e: self.destroy())
        
        # Focus modal (después de que sea visible)
        self.after(100, self._safe_grab)
    
    def _create_ui(self):
        """Crea la interfaz del modal."""
        # Contenedor principal
        main_frame = tk.Frame(self, bg=Theme.BACKGROUND, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header con nombre
        header = tk.Label(
            main_frame,
            text=f"📷 {self.img_info['name']}",
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT,
            font=("Helvetica", 14, "bold"),
        )
        header.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Canvas para imagen
        self.canvas = tk.Canvas(
            main_frame, bg=Theme.SURFACE, highlightthickness=1,
            highlightbackground=Theme.BORDER
        )
        self.canvas.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Info panel
        info_frame = tk.Frame(main_frame, bg=Theme.BACKGROUND)
        info_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.info_label = tk.Label(
            info_frame,
            text="Cargando...",
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_SECONDARY,
            font=("Helvetica", 10),
        )
        self.info_label.pack(side=tk.LEFT)
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=Theme.BACKGROUND)
        btn_frame.grid(row=3, column=0, sticky=tk.E, pady=(10, 0))
        
        if self.on_compress:
            tk.Button(
                btn_frame, text="📦 Comprimir", command=self._on_compress,
                bg=Theme.PRIMARY, fg="white", font=("Helvetica", 10),
                padx=15, pady=5, relief=tk.FLAT, cursor="hand2"
            ).pack(side=tk.LEFT, padx=5)
        
        if self.on_edit:
            tk.Button(
                btn_frame, text="✏️ Editar", command=self._on_edit,
                bg=Theme.SUCCESS, fg="white", font=("Helvetica", 10),
                padx=15, pady=5, relief=tk.FLAT, cursor="hand2"
            ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame, text="Cerrar", command=self.destroy,
            bg=Theme.SURFACE, fg=Theme.TEXT, font=("Helvetica", 10),
            padx=15, pady=5, relief=tk.FLAT, cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
    
    def _load_image(self):
        """Carga y muestra la imagen."""
        try:
            from PIL import Image, ImageTk
            
            path = self.img_info['path']
            if not path.exists():
                self.info_label.config(text="⚠️ Imagen no encontrada", fg=Theme.WARNING)
                return
            
            img = Image.open(path)
            orig_size = img.size
            file_size = path.stat().st_size / 1024
            
            # Escalar para caber en canvas
            self.update_idletasks()
            canvas_w = self.canvas.winfo_width() or 700
            canvas_h = self.canvas.winfo_height() or 400
            
            ratio = min(canvas_w / img.size[0], canvas_h / img.size[1], 1.0)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            self.tk_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(
                canvas_w // 2, canvas_h // 2,
                image=self.tk_img, anchor=tk.CENTER
            )
            
            self.info_label.config(
                text=f"📐 {orig_size[0]}×{orig_size[1]} px  |  💾 {file_size:.1f} KB",
                fg=Theme.TEXT_SECONDARY
            )
        except Exception as e:
            self.info_label.config(text=f"Error: {e}", fg=Theme.DANGER)
    
    def _on_edit(self):
        if self.on_edit:
            self.destroy()
            self.on_edit(self.img_info)
    
    def _on_compress(self):
        if self.on_compress:
            self.destroy()
            self.on_compress(self.img_info)
    
    def _safe_grab(self):
        """Intenta hacer grab de forma segura."""
        try:
            self.grab_set()
            print("[Debug] PreviewModal grab_set exitoso")
        except Exception as e:
            print(f"[Debug] PreviewModal grab_set falló: {e}")


class PdfMappingModal(tk.Toplevel):
    """Modal para mapear figuras de página PDF a imágenes del capítulo."""
    
    def __init__(self, parent, page_image_path, chapter_images, on_assign=None):
        super().__init__(parent)
        self.page_image_path = page_image_path
        self.chapter_images = chapter_images  # Lista de img_info del capítulo
        self.on_assign = on_assign
        
        print(f"[Debug] Abriendo PdfMappingModal para: {page_image_path}")
        self.title("Mapeo de Figuras PDF")
        self.configure(bg=Theme.BACKGROUND)
        self.geometry("1000x700")
        self.transient(parent)
        
        self.selected_region = None
        
        self._create_ui()
        self._load_page()
        
        # Centrar en pantalla
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 1000) // 2
        y = (self.winfo_screenheight() - 700) // 2
        self.geometry(f"+{x}+{y}")
        
        self.bind("<Escape>", lambda e: self.destroy())
        
        # Focus modal (después de que sea visible)
        self.after(100, self._safe_grab)
    
    def _create_ui(self):
        """Crea la interfaz del modal de mapeo."""
        # Layout: izquierda=PDF, derecha=lista imágenes
        main_frame = tk.Frame(self, bg=Theme.BACKGROUND, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Panel izquierdo: Página PDF
        pdf_frame = tk.LabelFrame(
            main_frame, text=" 📄 Página PDF ",
            bg=Theme.SURFACE, fg=Theme.TEXT,
            font=("Helvetica", 11, "bold"), padx=10, pady=10
        )
        pdf_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=(0, 10))
        pdf_frame.columnconfigure(0, weight=1)
        pdf_frame.rowconfigure(0, weight=1)
        
        self.pdf_canvas = tk.Canvas(
            pdf_frame, bg=Theme.BACKGROUND, highlightthickness=0
        )
        self.pdf_canvas.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        pdf_scroll = tk.Scrollbar(pdf_frame, orient=tk.VERTICAL, command=self.pdf_canvas.yview)
        pdf_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.pdf_canvas.configure(yscrollcommand=pdf_scroll.set)
        
        # Panel derecho: Lista de imágenes del capítulo
        images_frame = tk.LabelFrame(
            main_frame, text=" 📚 Imágenes del capítulo ",
            bg=Theme.SURFACE, fg=Theme.TEXT,
            font=("Helvetica", 11, "bold"), padx=10, pady=10
        )
        images_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        images_frame.columnconfigure(0, weight=1)
        images_frame.rowconfigure(0, weight=1)
        
        # Lista scrolleable
        list_container = tk.Frame(images_frame, bg=Theme.SURFACE)
        list_container.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(0, weight=1)
        
        self.images_canvas = tk.Canvas(list_container, bg=Theme.SURFACE, highlightthickness=0)
        self.images_canvas.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        img_scroll = tk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.images_canvas.yview)
        img_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.images_canvas.configure(yscrollcommand=img_scroll.set)
        
        self.images_list_frame = tk.Frame(self.images_canvas, bg=Theme.SURFACE)
        self.images_canvas.create_window((0, 0), window=self.images_list_frame, anchor=tk.NW)
        
        self.images_list_frame.bind("<Configure>", 
            lambda e: self.images_canvas.configure(scrollregion=self.images_canvas.bbox("all")))
        
        # Llenar lista de imágenes
        self._populate_images_list()
        
        # Barra inferior con botón de detección y status
        footer = tk.Frame(main_frame, bg=Theme.BACKGROUND)
        footer.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Botón detectar
        self.detect_btn = tk.Button(
            footer, text="🔍 Detectar", command=self._detect_figures,
            bg=Theme.PRIMARY, fg="white", font=("Helvetica", 10),
            padx=12, pady=5, relief=tk.FLAT, cursor="hand2"
        )
        self.detect_btn.pack(side=tk.LEFT)
        
        # Botón selección manual
        self.manual_btn = tk.Button(
            footer, text="✏️ Manual", command=self._toggle_manual_mode,
            bg=Theme.SURFACE, fg=Theme.TEXT, font=("Helvetica", 10),
            padx=12, pady=5, relief=tk.FLAT, cursor="hand2"
        )
        self.manual_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Botón enlazar (inicialmente deshabilitado)
        self.link_btn = tk.Button(
            footer, text="🔗 Enlazar", command=self._link_selected,
            bg=Theme.SUCCESS, fg="white", font=("Helvetica", 10),
            padx=12, pady=5, relief=tk.FLAT, cursor="hand2",
            state=tk.DISABLED
        )
        self.link_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Estado de modo manual
        self.manual_mode = False
        self.drawing_rect = None
        self.draw_start = None
        
        # Status label
        self.status_label = tk.Label(
            footer, text="💡 Click 'Detectar' para buscar figuras",
            bg=Theme.BACKGROUND, fg=Theme.TEXT_SECONDARY,
            font=("Helvetica", 9)
        )
        self.status_label.pack(side=tk.LEFT, padx=15)
        
        # Estado de selección
        self.detected_regions = []
        self.selected_region_idx = None  # Índice de la figura detectada seleccionada
        self.selected_image_idx = None   # Índice de la imagen del capítulo seleccionada
        self.image_list_items = []       # Lista de frames de imágenes para selección
    
    def _populate_images_list(self):
        """Llena la lista de imágenes del capítulo (clickeables)."""
        self.image_list_items = []
        
        for i, img_info in enumerate(self.chapter_images):
            item_frame = tk.Frame(
                self.images_list_frame, bg=Theme.SURFACE,
                highlightthickness=2, highlightbackground=Theme.BORDER,
                cursor="hand2"
            )
            item_frame.pack(fill=tk.X, pady=2)
            
            exists = img_info['path'].exists()
            icon = "✅" if exists else "⚠️"
            color = Theme.TEXT if exists else Theme.WARNING
            
            label = tk.Label(
                item_frame,
                text=f"{icon} {img_info['name']}",
                bg=Theme.SURFACE, fg=color,
                font=("Helvetica", 9),
                anchor="w", padx=5, pady=5
            )
            label.pack(fill=tk.X)
            
            # Click handler para seleccionar
            idx = i  # Capturar índice
            for widget in (item_frame, label):
                widget.bind("<Button-1>", lambda e, idx=idx: self._select_image(idx))
            
            # Guardar referencia
            self.image_list_items.append({
                'frame': item_frame,
                'label': label,
                'img_info': img_info,
                'exists': exists
            })
    
    def _load_page(self):
        """Carga la página PDF en el canvas."""
        try:
            from PIL import Image, ImageTk
            
            if not self.page_image_path.exists():
                return
            
            img = Image.open(self.page_image_path)
            
            # Escalar para caber
            self.update_idletasks()
            canvas_w = max(self.pdf_canvas.winfo_width(), 600)
            ratio = canvas_w / img.size[0]
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            self.page_tk_img = ImageTk.PhotoImage(img)
            self.pdf_canvas.config(scrollregion=(0, 0, new_size[0], new_size[1]))
            self.pdf_canvas.create_image(0, 0, image=self.page_tk_img, anchor=tk.NW)
            
            # Guardar ratio para convertir coordenadas
            self.display_ratio = ratio
            
        except Exception as e:
            print(f"[Error] Cargando página PDF: {e}")
    
    def _detect_figures(self):
        """Inicia detección de figuras usando ImageDetector (en thread separado)."""
        print(f"[Debug] Iniciando detección de figuras en: {self.page_image_path}")
        
        self.status_label.config(text="⏳ Detectando figuras...", fg=Theme.PRIMARY)
        self.detect_btn.config(state=tk.DISABLED)
        
        # Importar ImageDetector
        try:
            from ..image_detector import ImageDetector
        except ImportError:
            print("[Error] No se pudo importar ImageDetector")
            self.status_label.config(text="❌ Error: módulo image_detector no encontrado", fg=Theme.DANGER)
            self.detect_btn.config(state=tk.NORMAL)
            return
        
        # Crear detector y ejecutar async
        detector = ImageDetector(debug=True)
        
        def on_complete(regions):
            # Programar actualización en thread principal
            self.after(0, lambda: self._on_detection_complete(regions, detector))
        
        def on_error(e):
            self.after(0, lambda: self._on_detection_error(e))
        
        detector.detect_async(
            self.page_image_path,
            callback=on_complete,
            error_callback=on_error
        )
    
    def _on_detection_complete(self, regions, detector):
        """Callback cuando la detección termina (ejecutado en thread principal)."""
        self.detected_regions = regions
        count = len(regions)
        
        print(f"[Debug] Detección completada: {count} figuras encontradas")
        
        if count > 0:
            self.status_label.config(
                text=f"✅ {count} figuras detectadas",
                fg=Theme.SUCCESS
            )
            # Dibujar rectángulos sobre la página
            self._draw_detected_regions(regions)
        else:
            self.status_label.config(
                text="⚠️ No se detectaron figuras",
                fg=Theme.WARNING
            )
        
        self.detect_btn.config(state=tk.NORMAL, text="🔄 Re-detectar")
    
    def _on_detection_error(self, error):
        """Callback cuando hay error en la detección."""
        print(f"[Error] Detección fallida: {error}")
        self.status_label.config(
            text=f"❌ Error: {error}",
            fg=Theme.DANGER
        )
        self.detect_btn.config(state=tk.NORMAL)
    
    def _draw_detected_regions(self, regions):
        """Dibuja rectángulos sobre las figuras detectadas."""
        if not hasattr(self, 'display_ratio'):
            print("[Debug] No display_ratio disponible")
            return
        
        ratio = self.display_ratio
        
        # Limpiar rectángulos anteriores
        self.pdf_canvas.delete("detection_rect")
        self.pdf_canvas.delete("detection_label")
        
        for i, region in enumerate(regions, 1):
            # Escalar coordenadas al tamaño mostrado
            x1 = int(region.x * ratio)
            y1 = int(region.y * ratio)
            x2 = int((region.x + region.w) * ratio)
            y2 = int((region.y + region.h) * ratio)
            
            # Rectángulo verde
            self.pdf_canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="#00FF00", width=2,
                tags="detection_rect"
            )
            
            # Etiqueta con número
            self.pdf_canvas.create_text(
                x1 + 5, y1 + 5,
                text=f"Fig {i}",
                anchor=tk.NW,
                fill="#00FF00",
                font=("Helvetica", 10, "bold"),
                tags=("detection_label", f"region_{i-1}")
            )
            
            # Crear área clickeable invisible sobre la región
            rect_id = self.pdf_canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="", fill="",  # Invisible pero clickeable
                tags=("region_hitbox", f"hitbox_{i-1}")
            )
        
        # Bind click a las hitboxes
        self.pdf_canvas.tag_bind("region_hitbox", "<Button-1>", self._on_hitbox_click)
        
        # También bind general al canvas como fallback
        self.pdf_canvas.bind("<Button-1>", self._on_canvas_click)
        
        print(f"[Debug] Dibujados {len(regions)} rectángulos de detección (clickeables)")
    
    def _on_hitbox_click(self, event):
        """Click en hitbox de región."""
        # Encontrar qué hitbox fue clickeada
        current = self.pdf_canvas.find_withtag(tk.CURRENT)
        if current:
            tags = self.pdf_canvas.gettags(current[0])
            for tag in tags:
                if tag.startswith("hitbox_"):
                    idx = int(tag.split("_")[1])
                    print(f"[Debug] Hitbox click en región {idx}")
                    self._select_region(idx)
                    return
    
    def _on_canvas_click(self, event):
        """Click general en canvas - detecta región por coordenadas."""
        if not hasattr(self, 'display_ratio') or not self.detected_regions:
            return
        
        # Verificar si ya se manejó por hitbox
        current = self.pdf_canvas.find_withtag(tk.CURRENT) 
        if current:
            tags = self.pdf_canvas.gettags(current[0])
            if any(t.startswith("hitbox_") for t in tags):
                return  # Ya manejado por _on_hitbox_click
        
        # Detectar por coordenadas
        canvas_x = self.pdf_canvas.canvasx(event.x)
        canvas_y = self.pdf_canvas.canvasy(event.y)
        
        ratio = self.display_ratio
        orig_x = canvas_x / ratio
        orig_y = canvas_y / ratio
        
        print(f"[Debug] Canvas click en ({orig_x:.0f}, {orig_y:.0f})")
        
        # Buscar qué región contiene el click
        for i, region in enumerate(self.detected_regions):
            if (region.x <= orig_x <= region.x + region.w and
                region.y <= orig_y <= region.y + region.h):
                print(f"[Debug] Click detectado en región {i}")
                self._select_region(i)
                return
        
        print("[Debug] Click fuera de regiones detectadas")
    
    def _select_region(self, idx):
        """Selecciona una figura detectada por índice."""
        print(f"[Debug] Figura detectada seleccionada: {idx + 1}")
        
        self.selected_region_idx = idx
        
        # Actualizar visualización
        self._highlight_selected_region()
        self._update_link_button_state()
        self._update_status()
    
    def _highlight_selected_region(self):
        """Resalta la figura seleccionada."""
        if not hasattr(self, 'display_ratio') or self.selected_region_idx is None:
            return
        
        ratio = self.display_ratio
        
        # Limpiar selección anterior
        self.pdf_canvas.delete("selection_rect")
        
        # Dibujar nuevo rectángulo de selección
        region = self.detected_regions[self.selected_region_idx]
        x1 = int(region.x * ratio)
        y1 = int(region.y * ratio)
        x2 = int((region.x + region.w) * ratio)
        y2 = int((region.y + region.h) * ratio)
        
        self.pdf_canvas.create_rectangle(
            x1, y1, x2, y2,
            outline="#FFFF00", width=4,
            tags="selection_rect"
        )
    
    def _select_image(self, idx):
        """Selecciona una imagen del capítulo por índice."""
        print(f"[Debug] Imagen del capítulo seleccionada: {idx}")
        
        self.selected_image_idx = idx
        
        # Actualizar visualización de la lista
        for i, item in enumerate(self.image_list_items):
            if i == idx:
                item['frame'].configure(highlightbackground=Theme.PRIMARY, highlightthickness=3)
                item['label'].configure(bg=Theme.PRIMARY, fg="white")
            else:
                item['frame'].configure(highlightbackground=Theme.BORDER, highlightthickness=2)
                bg = Theme.SURFACE
                fg = Theme.TEXT if item['exists'] else Theme.WARNING
                item['label'].configure(bg=bg, fg=fg)
        
        self._update_link_button_state()
        self._update_status()
    
    def _update_link_button_state(self):
        """Actualiza estado del botón enlazar."""
        if self.selected_region_idx is not None and self.selected_image_idx is not None:
            self.link_btn.config(state=tk.NORMAL)
        else:
            self.link_btn.config(state=tk.DISABLED)
    
    def _update_status(self):
        """Actualiza el mensaje de estado."""
        region_str = f"Fig {self.selected_region_idx + 1}" if self.selected_region_idx is not None else "?"
        image_str = self.chapter_images[self.selected_image_idx]['name'] if self.selected_image_idx is not None else "?"
        
        if self.selected_region_idx is not None and self.selected_image_idx is not None:
            self.status_label.config(
                text=f"📌 {region_str} → 📁 {image_str} | Click 'Enlazar'",
                fg=Theme.SUCCESS
            )
        elif self.selected_region_idx is not None:
            self.status_label.config(
                text=f"📌 {region_str} seleccionada | Ahora selecciona imagen destino",
                fg=Theme.PRIMARY
            )
        elif self.selected_image_idx is not None:
            self.status_label.config(
                text=f"📁 {image_str} | Ahora selecciona figura en PDF",
                fg=Theme.PRIMARY
            )
    
    def _link_selected(self):
        """Enlaza la figura detectada con la imagen del capítulo."""
        if self.selected_region_idx is None or self.selected_image_idx is None:
            return
        
        region = self.detected_regions[self.selected_region_idx]
        img_info = self.chapter_images[self.selected_image_idx]
        target_path = img_info['path']
        
        print(f"[Debug] Enlazando Fig {self.selected_region_idx + 1} → {target_path}")
        
        try:
            from ..image_detector import ImageDetector
            
            detector = ImageDetector()
            
            # Recortar y guardar
            success = detector.save_cropped_region(
                self.page_image_path,
                region,
                target_path,
                padding=5
            )
            
            if success:
                self.status_label.config(
                    text=f"✅ Imagen guardada: {img_info['name']}",
                    fg=Theme.SUCCESS
                )
                
                # Marcar imagen como existente en la lista (con bounds check)
                if self.image_list_items and 0 <= self.selected_image_idx < len(self.image_list_items):
                    self.image_list_items[self.selected_image_idx]['exists'] = True
                    self.image_list_items[self.selected_image_idx]['label'].configure(
                        text=f"✅ {img_info['name']}"
                    )
                
                # Resetear selección
                self.selected_region_idx = None
                self.selected_image_idx = None
                self._update_link_button_state()
                
                print(f"[Debug] Enlace completado exitosamente")
            else:
                self.status_label.config(
                    text=f"❌ Error guardando imagen",
                    fg=Theme.DANGER
                )
        except Exception as e:
            print(f"[Error] Enlazando imagen: {e}")
            self.status_label.config(
                text=f"❌ Error: {e}",
                fg=Theme.DANGER
            )
    
    def _toggle_manual_mode(self):
        """Activa/desactiva modo de selección manual."""
        self.manual_mode = not self.manual_mode
        
        if self.manual_mode:
            # Activar modo manual
            self.manual_btn.config(bg=Theme.WARNING, fg="white", text="✏️ Dibujando...")
            self.status_label.config(
                text="✏️ Click y arrastra para seleccionar región",
                fg=Theme.WARNING
            )
            # Cambiar cursor y binds
            self.pdf_canvas.config(cursor="crosshair")
            self.pdf_canvas.bind("<ButtonPress-1>", self._on_manual_start)
            self.pdf_canvas.bind("<B1-Motion>", self._on_manual_drag)
            self.pdf_canvas.bind("<ButtonRelease-1>", self._on_manual_end)
            print("[Debug] Modo manual activado")
        else:
            # Desactivar modo manual
            self.manual_btn.config(bg=Theme.SURFACE, fg=Theme.TEXT, text="✏️ Manual")
            self.status_label.config(
                text="💡 Click 'Detectar' o selecciona una región",
                fg=Theme.TEXT_SECONDARY
            )
            self.pdf_canvas.config(cursor="")
            # Restaurar bind normal
            self.pdf_canvas.bind("<Button-1>", self._on_canvas_click)
            self.pdf_canvas.unbind("<B1-Motion>")
            self.pdf_canvas.unbind("<ButtonRelease-1>")
            print("[Debug] Modo manual desactivado")
    
    def _on_manual_start(self, event):
        """Inicia dibujo de rectángulo manual."""
        if not self.manual_mode:
            return
        
        self.draw_start = (
            self.pdf_canvas.canvasx(event.x),
            self.pdf_canvas.canvasy(event.y)
        )
        
        # Crear rectángulo temporal
        self.pdf_canvas.delete("manual_rect")
        self.drawing_rect = self.pdf_canvas.create_rectangle(
            self.draw_start[0], self.draw_start[1],
            self.draw_start[0], self.draw_start[1],
            outline="#FF00FF", width=3, dash=(5, 3),
            tags="manual_rect"
        )
    
    def _on_manual_drag(self, event):
        """Actualiza rectángulo mientras se arrastra."""
        if not self.manual_mode or self.draw_start is None:
            return
        
        current_x = self.pdf_canvas.canvasx(event.x)
        current_y = self.pdf_canvas.canvasy(event.y)
        
        self.pdf_canvas.coords(
            self.drawing_rect,
            self.draw_start[0], self.draw_start[1],
            current_x, current_y
        )
    
    def _on_manual_end(self, event):
        """Finaliza dibujo y crea región manual."""
        if not self.manual_mode or self.draw_start is None:
            return
        
        end_x = self.pdf_canvas.canvasx(event.x)
        end_y = self.pdf_canvas.canvasy(event.y)
        
        # Calcular coordenadas normalizadas (min/max)
        x1 = min(self.draw_start[0], end_x)
        y1 = min(self.draw_start[1], end_y)
        x2 = max(self.draw_start[0], end_x)
        y2 = max(self.draw_start[1], end_y)
        
        # Verificar tamaño mínimo
        if (x2 - x1) < 20 or (y2 - y1) < 20:
            self.pdf_canvas.delete("manual_rect")
            self.status_label.config(
                text="⚠️ Región muy pequeña, intenta de nuevo",
                fg=Theme.WARNING
            )
            self.draw_start = None
            return
        
        # Convertir a coordenadas originales
        if not hasattr(self, 'display_ratio'):
            return
        
        ratio = self.display_ratio
        orig_x = int(x1 / ratio)
        orig_y = int(y1 / ratio)
        orig_w = int((x2 - x1) / ratio)
        orig_h = int((y2 - y1) / ratio)
        
        # Crear región usando dataclass del detector
        try:
            from ..image_detector import DetectedRegion
            manual_region = DetectedRegion(
                x=orig_x, y=orig_y, w=orig_w, h=orig_h,
                area=orig_w * orig_h,
                density=1.0,  # Densidad irrelevante para manual
                is_image=True
            )
        except ImportError:
            # Fallback: crear objeto simple
            class SimpleRegion:
                def __init__(self, x, y, w, h):
                    self.x, self.y, self.w, self.h = x, y, w, h
            manual_region = SimpleRegion(orig_x, orig_y, orig_w, orig_h)
        
        # Añadir a regiones detectadas
        self.detected_regions.append(manual_region)
        idx = len(self.detected_regions) - 1
        
        # Cambiar color del rectángulo a verde (detectado)
        self.pdf_canvas.delete("manual_rect")
        self.pdf_canvas.create_rectangle(
            x1, y1, x2, y2,
            outline="#00FF00", width=2,
            tags="detection_rect"
        )
        self.pdf_canvas.create_text(
            x1 + 5, y1 + 5,
            text=f"Fig {idx + 1}",
            anchor=tk.NW,
            fill="#00FF00",
            font=("Helvetica", 10, "bold"),
            tags="detection_label"
        )
        
        # Seleccionar automáticamente
        self._select_region(idx)
        
        # Resetear estado de dibujo
        self.draw_start = None
        
        self.status_label.config(
            text=f"✅ Región manual añadida (Fig {idx + 1})",
            fg=Theme.SUCCESS
        )
        
        print(f"[Debug] Región manual creada: ({orig_x}, {orig_y}, {orig_w}x{orig_h})")
    
    def _safe_grab(self):
        """Intenta hacer grab de forma segura."""
        try:
            self.grab_set()
            print("[Debug] PdfMappingModal grab_set exitoso")
        except Exception as e:
            print(f"[Debug] PdfMappingModal grab_set falló: {e}")

