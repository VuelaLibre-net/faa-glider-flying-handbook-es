"""
Ventana principal del Gestor de Imágenes - Versión 2 con Sidebar y Toolbar

Fase 1: Rediseño con navegación lateral y toolbar contextual.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from pathlib import Path

from PIL import Image, ImageTk, ImageDraw

from ..config import (
    DEFAULT_MAX_WIDTH,
    DEFAULT_QUALITY,
    DEFAULT_CREATE_BACKUP,
    IMAGES_DIR,
    TranslationConfig,
)
from ..image_processor import ImageProcessor, open_folder_in_explorer
from ..file_manager import FileManager
from ..translation import (
    TranslationManager,
    is_translation_available,
    TranslationError,
    TranslationConfigError,
)
from ..clipboard_handler import get_clipboard_handler, NoImageInClipboardError
from .image_editor import ImageEditor
from .translation_dialog import TranslationDialog
from .settings_dialog import SettingsDialog
from .themes import Theme, SidebarButton, ToolbarButton, ImageThumbnail, CardFrame, ShadowThumbnail, PdfPageThumbnail, PreviewModal, PdfMappingModal
from ..figure_detector import FigureDetector, DetectedFigure


class ImageManagerAppV2:
    """Aplicación principal con nuevo diseño."""

    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Imágenes - Manual de Vuelo sin Motor v3.0")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        self.root.configure(bg=Theme.BACKGROUND)

        # Cargar icono de la aplicación
        try:
            icon_path = Path(__file__).parent.parent / "manager-icon.png"
            icon_img = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_img)
            self.root.wm_iconphoto(True, icon_photo)
            self._icon_photo = (
                icon_photo  # Mantener referencia para evitar garbage collection
            )
        except Exception as e:
            print(f"[Info] No se pudo cargar icono: {e}")

        # Configurar tema
        Theme.configure_styles(root)

        # Componentes
        self.file_manager = FileManager()
        self.image_processor = ImageProcessor()
        self.clipboard = get_clipboard_handler()

        # Estado
        self.chapters = []
        self.current_chapter = None
        self.current_chapter_images = []
        self.new_images = []
        self.selected_image = None
        self.selected_thumbnail = None

        # Opciones de procesamiento
        self.rounded_corners_var = tk.BooleanVar(value=True)

        # Traducción
        self.translation_manager = None
        self.is_translating = False
        self._init_translation()

        # Menú contextual activo
        self._active_context_menu = None

        # Crear UI
        self._create_ui()
        self._setup_global_bindings()
        self._load_chapters()

    def _setup_global_bindings(self):
        """Configura los bindings globales de la aplicación."""
        # Binding global para cerrar menú contextual con Escape
        self.root.bind_all("<Escape>", self._close_context_menu)

    def _close_context_menu(self, event=None):
        """Cierra el menú contextual activo si existe."""
        if self._active_context_menu:
            try:
                self._active_context_menu.unpost()
            except tk.TclError:
                pass  # El menú ya estaba cerrado
            self._active_context_menu = None

    def _init_translation(self):
        """Inicializa el sistema de traducción."""
        if is_translation_available():
            try:
                self.translation_manager = TranslationManager()
            except TranslationConfigError as e:
                print(f"[Info] Traducción no disponible: {e}")

    def _create_ui(self):
        """Crea la interfaz de usuario principal."""
        # Layout principal: Sidebar | Contenido
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Sidebar izquierdo
        self._create_sidebar()

        # Área de contenido principal
        self._create_main_content()

        # Status bar
        self._create_statusbar()

    def _create_sidebar(self):
        """Crea el sidebar de navegación de capítulos."""
        self.sidebar = tk.Frame(self.root, bg=Theme.SIDEBAR_BG, width=200)
        self.sidebar.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W))
        self.sidebar.grid_propagate(False)
        self.sidebar.columnconfigure(0, weight=1)

        # Logo/Título
        header = tk.Frame(self.sidebar, bg=Theme.SIDEBAR_BG, padx=15, pady=20)
        header.grid(row=0, column=0, sticky=(tk.W, tk.E))

        tk.Label(
            header,
            text="🖼️",
            bg=Theme.SIDEBAR_BG,
            fg=Theme.SIDEBAR_TEXT,
            font=("Helvetica", 24),
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Image\nManager",
            bg=Theme.SIDEBAR_BG,
            fg=Theme.SIDEBAR_TEXT,
            font=("Helvetica", 14, "bold"),
            justify="left",
        ).pack(anchor="w", pady=(5, 0))

        # Separador
        separator = tk.Frame(self.sidebar, bg="#374151", height=1)
        separator.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)

        # Título sección capítulos
        tk.Label(
            self.sidebar,
            text="CAPÍTULOS",
            bg=Theme.SIDEBAR_BG,
            fg=Theme.TEXT_MUTED,
            font=("Helvetica", 9, "bold"),
            padx=15,
            pady=10,
        ).grid(row=2, column=0, sticky=tk.W)

        # Contenedor de botones de capítulos
        self.chapters_container = tk.Frame(self.sidebar, bg=Theme.SIDEBAR_BG)
        self.chapters_container.grid(row=3, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.sidebar.rowconfigure(3, weight=1)

        # Botones se llenarán dinámicamente
        self.chapter_buttons = []

        # Separador inferior
        separator2 = tk.Frame(self.sidebar, bg="#374151", height=1)
        separator2.grid(row=4, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)

        # Contador de imágenes
        self.sidebar_stats = tk.Label(
            self.sidebar,
            text="0 imágenes",
            bg=Theme.SIDEBAR_BG,
            fg=Theme.TEXT_MUTED,
            font=("Helvetica", 9),
            padx=15,
            pady=10,
        )
        self.sidebar_stats.grid(row=5, column=0, sticky=tk.W)

    def _create_main_content(self):
        """Crea el área de contenido principal con layout de 3 columnas."""
        # Contenedor principal
        container = tk.Frame(self.root, bg=Theme.BACKGROUND)
        container.grid(
            row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W), padx=10, pady=10
        )
        container.columnconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)

        # Main frame para toolbar, panels, y opciones
        self.main_frame = tk.Frame(container, bg=Theme.BACKGROUND)
        self.main_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        # Toolbar en la parte superior
        self._create_toolbar()

        # === Panel principal con 2 columnas: Imágenes (centro) | PDF (derecha) ===
        self.content_pane = tk.PanedWindow(
            self.main_frame, 
            orient=tk.HORIZONTAL, 
            bg=Theme.BACKGROUND,
            sashwidth=6,
            sashrelief=tk.RAISED
        )
        self.content_pane.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), pady=(10, 0))

        # Panel central: Galería de imágenes del capítulo
        self._create_gallery_panel_v2()
        self.content_pane.add(self.gallery_frame, minsize=400, stretch="always")

        # Panel derecho: Páginas PDF fuente
        self._create_pdf_panel()
        self.content_pane.add(self.pdf_panel, minsize=200, stretch="never")

        # Opciones en la parte inferior
        self._create_options_panel()

        # Inicializar FigureDetector (necesario para compatibilidad)
        self.figure_detector = FigureDetector(self.translation_manager)
        
        # Estado de selección (compatibilidad)
        self.selection_mode = False
        self.selection_start = None
        self.selection_rect_id = None
        self.figure_rects = []
        self.source_page_index = 0
        self.source_images_list = []
        self.current_source_image = None
        self.source_scale = 1.0

    def _create_toolbar(self):
        """Crea la toolbar contextual."""
        self.toolbar = tk.Frame(self.main_frame, bg=Theme.SURFACE, padx=10, pady=10)
        self.toolbar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

        # Sección: Acciones principales
        self.toolbar_actions = tk.Frame(self.toolbar, bg=Theme.SURFACE)
        self.toolbar_actions.pack(side=tk.LEFT)

        self.btn_replace = ToolbarButton(
            self.toolbar_actions,
            text="Reemplazar",
            icon="🔄",
            command=self._on_replace,
            state="disabled",
        )
        self.btn_replace.pack(side=tk.LEFT, padx=2)

        self.btn_translate = ToolbarButton(
            self.toolbar_actions,
            text="Traducir",
            icon="🌍",
            command=self._on_translate,
            state="disabled",
        )
        self.btn_translate.pack(side=tk.LEFT, padx=2)

        self.btn_edit = ToolbarButton(
            self.toolbar_actions,
            text="Editar",
            icon="✏️",
            command=self._on_edit,
            state="disabled",
        )
        self.btn_edit.pack(side=tk.LEFT, padx=2)

        self.btn_open_folder = ToolbarButton(
            self.toolbar_actions,
            text="Abrir carpeta",
            icon="📂",
            command=self._on_open_folder,
        )
        self.btn_open_folder.pack(side=tk.LEFT, padx=2)

        # Separador
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=15
        )

        # Sección: Portapapeles
        self.toolbar_clipboard = tk.Frame(self.toolbar, bg=Theme.SURFACE)
        self.toolbar_clipboard.pack(side=tk.LEFT)

        self.btn_paste = ToolbarButton(
            self.toolbar_clipboard, text="Pegar", icon="📌", command=self._on_paste
        )
        self.btn_paste.pack(side=tk.LEFT, padx=2)

        self.btn_copy = ToolbarButton(
            self.toolbar_clipboard,
            text="Copiar",
            icon="📋",
            command=self._on_copy,
            state="disabled",
        )
        self.btn_copy.pack(side=tk.LEFT, padx=2)

        # Separador
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=15
        )

        # Sección: Configuración
        self.btn_settings = ToolbarButton(
            self.toolbar, text="Configuración", icon="⚙️", command=self._open_settings
        )
        self.btn_settings.pack(side=tk.RIGHT, padx=2)
        
        # Separador
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=15
        )

        # Sección: Actualizar
        self.btn_refresh = ToolbarButton(
            self.toolbar, text="Actualizar", icon="🔄", command=self._refresh_chapter
        )
        self.btn_refresh.pack(side=tk.RIGHT, padx=2)

    def _create_gallery_panel(self):
        """Crea el panel de galería con preview."""
        self.gallery_frame = tk.Frame(self.main_frame, bg=Theme.BACKGROUND)
        self.gallery_frame.grid(row=2, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.gallery_frame.columnconfigure(0, weight=2)
        self.gallery_frame.columnconfigure(1, weight=1)
        self.gallery_frame.rowconfigure(0, weight=1)

        # Panel izquierdo: Galería de imágenes
        self._create_gallery_left()

        # Panel derecho: Preview
        self._create_preview_panel()

    def _create_gallery_left(self):
        """Crea el panel de galería izquierdo (imágenes del capítulo)."""
        left_container = CardFrame(self.gallery_frame)
        left_container.grid(
            row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=(0, 10)
        )
        left_container.columnconfigure(0, weight=1)
        left_container.rowconfigure(1, weight=1)

        # Header
        self.gallery_header = tk.Label(
            left_container,
            text="📚 Imágenes del capítulo",
            bg=Theme.SURFACE,
            fg=Theme.TEXT,
            font=("Helvetica", 11, "bold"),
            padx=15,
            pady=10,
            anchor="w",
        )
        self.gallery_header.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Canvas scrolleable para thumbnails
        self.gallery_canvas = tk.Canvas(
            left_container, bg=Theme.SURFACE, highlightthickness=0
        )
        self.gallery_canvas.grid(
            row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=10, pady=10
        )

        scrollbar = ttk.Scrollbar(
            left_container, orient=tk.VERTICAL, command=self.gallery_canvas.yview
        )
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.gallery_canvas.configure(yscrollcommand=scrollbar.set)

        # Frame contenedor de thumbnails
        self.thumbnails_frame = tk.Frame(self.gallery_canvas, bg=Theme.SURFACE)
        self.thumbnails_frame.columnconfigure(0, weight=1)
        self.thumbnails_frame.columnconfigure(1, weight=1)
        self.thumbnails_frame.columnconfigure(2, weight=1)
        self.thumbnails_frame.columnconfigure(3, weight=1)

        self.canvas_window = self.gallery_canvas.create_window(
            (0, 0),
            window=self.thumbnails_frame,
            anchor=tk.NW,
            width=self.gallery_canvas.winfo_width(),
        )

        def on_frame_configure(event):
            """Actualiza scrollregion cuando cambia el frame."""
            self.gallery_canvas.configure(scrollregion=self.gallery_canvas.bbox("all"))

        def on_canvas_configure(event):
            """Ajusta el ancho del frame al canvas."""
            self.gallery_canvas.itemconfig(self.canvas_window, width=event.width)

        self.thumbnails_frame.bind("<Configure>", on_frame_configure)
        self.gallery_canvas.bind("<Configure>", on_canvas_configure)

        # Bind mousewheel
        def on_mousewheel(event):
            self.gallery_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.gallery_canvas.bind_all("<MouseWheel>", on_mousewheel)

    def _create_gallery_panel_v2(self):
        """Crea el panel de galería de imágenes (sin columna preview)."""
        self.gallery_frame = CardFrame(self.main_frame)
        self.gallery_frame.columnconfigure(0, weight=1)
        self.gallery_frame.rowconfigure(0, weight=1)

        # Galería de imágenes (ocupa todo el ancho)
        left_container = tk.Frame(self.gallery_frame, bg=Theme.SURFACE)
        left_container.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        left_container.columnconfigure(0, weight=1)
        left_container.rowconfigure(1, weight=1)

        # Header
        self.gallery_header = tk.Label(
            left_container,
            text="📚 Imágenes del capítulo",
            bg=Theme.SURFACE,
            fg=Theme.TEXT,
            font=("Helvetica", 11, "bold"),
            padx=15,
            pady=10,
            anchor="w",
        )
        self.gallery_header.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Canvas scrolleable para thumbnails
        self.gallery_canvas = tk.Canvas(
            left_container, bg=Theme.SURFACE, highlightthickness=0
        )
        self.gallery_canvas.grid(
            row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=10, pady=10
        )

        scrollbar = ttk.Scrollbar(
            left_container, orient=tk.VERTICAL, command=self.gallery_canvas.yview
        )
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.gallery_canvas.configure(yscrollcommand=scrollbar.set)

        # Frame contenedor de thumbnails (5 columnas ahora que hay más espacio)
        self.thumbnails_frame = tk.Frame(self.gallery_canvas, bg=Theme.SURFACE)
        for i in range(5):
            self.thumbnails_frame.columnconfigure(i, weight=1)

        self.canvas_window = self.gallery_canvas.create_window(
            (0, 0),
            window=self.thumbnails_frame,
            anchor=tk.NW,
            width=self.gallery_canvas.winfo_width(),
        )

        def on_frame_configure(event):
            self.gallery_canvas.configure(scrollregion=self.gallery_canvas.bbox("all"))

        def on_canvas_configure(event):
            self.gallery_canvas.itemconfig(self.canvas_window, width=event.width)

        self.thumbnails_frame.bind("<Configure>", on_frame_configure)
        self.gallery_canvas.bind("<Configure>", on_canvas_configure)

        def on_mousewheel(event):
            self.gallery_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.gallery_canvas.bind_all("<MouseWheel>", on_mousewheel)

    def _create_pdf_panel(self):
        """Crea el panel de páginas PDF fuente (columna derecha)."""
        self.pdf_panel = CardFrame(self.main_frame)
        self.pdf_panel.columnconfigure(0, weight=1)
        self.pdf_panel.rowconfigure(1, weight=1)

        # Header con navegación
        header_frame = tk.Frame(self.pdf_panel, bg=Theme.SURFACE)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)

        tk.Label(
            header_frame,
            text="📄 Páginas PDF",
            bg=Theme.SURFACE,
            fg=Theme.TEXT,
            font=("Helvetica", 11, "bold"),
            anchor="w",
        ).pack(side=tk.LEFT)

        # Navegación
        nav_frame = tk.Frame(header_frame, bg=Theme.SURFACE)
        nav_frame.pack(side=tk.RIGHT)

        self.pdf_prev_btn = tk.Button(
            nav_frame, text="◀", command=self._prev_pdf_page,
            bg=Theme.SURFACE, fg=Theme.TEXT, font=("Helvetica", 8),
            relief=tk.FLAT, padx=5, cursor="hand2"
        )
        self.pdf_prev_btn.pack(side=tk.LEFT)

        self.pdf_page_label = tk.Label(
            nav_frame, text="0/0", bg=Theme.SURFACE, fg=Theme.TEXT_SECONDARY,
            font=("Helvetica", 9), width=8
        )
        self.pdf_page_label.pack(side=tk.LEFT, padx=5)

        self.pdf_next_btn = tk.Button(
            nav_frame, text="▶", command=self._next_pdf_page,
            bg=Theme.SURFACE, fg=Theme.TEXT, font=("Helvetica", 8),
            relief=tk.FLAT, padx=5, cursor="hand2"
        )
        self.pdf_next_btn.pack(side=tk.LEFT)

        # Canvas scrolleable para thumbnails de PDF
        pdf_canvas_container = tk.Frame(self.pdf_panel, bg=Theme.SURFACE)
        pdf_canvas_container.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)
        pdf_canvas_container.columnconfigure(0, weight=1)
        pdf_canvas_container.rowconfigure(0, weight=1)

        self.pdf_canvas = tk.Canvas(
            pdf_canvas_container, bg=Theme.SURFACE, highlightthickness=0, width=220
        )
        self.pdf_canvas.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        pdf_scroll = ttk.Scrollbar(
            pdf_canvas_container, orient=tk.VERTICAL, command=self.pdf_canvas.yview
        )
        pdf_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.pdf_canvas.configure(yscrollcommand=pdf_scroll.set)

        # Frame contenedor de thumbnails PDF
        self.pdf_thumbnails_frame = tk.Frame(self.pdf_canvas, bg=Theme.SURFACE)
        self.pdf_thumbnails_frame.columnconfigure(0, weight=1)
        self.pdf_thumbnails_frame.columnconfigure(1, weight=1)

        self.pdf_canvas_window = self.pdf_canvas.create_window(
            (0, 0), window=self.pdf_thumbnails_frame, anchor=tk.NW,
            width=self.pdf_canvas.winfo_width()
        )

        def on_pdf_frame_configure(event):
            self.pdf_canvas.configure(scrollregion=self.pdf_canvas.bbox("all"))

        def on_pdf_canvas_configure(event):
            self.pdf_canvas.itemconfig(self.pdf_canvas_window, width=event.width)

        self.pdf_thumbnails_frame.bind("<Configure>", on_pdf_frame_configure)
        self.pdf_canvas.bind("<Configure>", on_pdf_canvas_configure)

        # Estado
        self.pdf_page_index = 0
        self.pdf_images_list = []

    def _prev_pdf_page(self):
        """Navega a la página PDF anterior."""
        if self.pdf_page_index > 0:
            self.pdf_page_index -= 1
            self._highlight_pdf_page()

    def _next_pdf_page(self):
        """Navega a la página PDF siguiente."""
        if self.pdf_page_index < len(self.pdf_images_list) - 1:
            self.pdf_page_index += 1
            self._highlight_pdf_page()

    def _highlight_pdf_page(self):
        """Resalta la página PDF actual en la lista."""
        for widget in self.pdf_thumbnails_frame.winfo_children():
            if isinstance(widget, PdfPageThumbnail):
                widget.set_selected(widget.page_num == self.pdf_page_index + 1)
        
        if self.pdf_images_list:
            self.pdf_page_label.config(
                text=f"{self.pdf_page_index + 1}/{len(self.pdf_images_list)}"
            )

    def _load_pdf_pages(self):
        """Carga las páginas PDF del capítulo actual."""
        if not self.current_chapter:
            return

        # Limpiar thumbnails existentes
        for widget in self.pdf_thumbnails_frame.winfo_children():
            widget.destroy()

        chapter_num = self.current_chapter[0]
        project_root = IMAGES_DIR.parent.parent
        en_images_dir = project_root / "en" / "images" / chapter_num

        if en_images_dir.exists():
            # Ordenar 'page-1.png', 'page-2.png'... numeric sort
            files = sorted(
                list(en_images_dir.glob("*.png")),
                key=lambda p: int(p.stem.split('-')[-1]) if '-' in p.stem else 0
            )
            self.pdf_images_list = files
            self.source_images_list = files  # Compatibilidad con métodos existentes

            # Crear thumbnails
            for i, img_path in enumerate(files):
                try:
                    img = Image.open(img_path)
                    thumb = PdfPageThumbnail(
                        self.pdf_thumbnails_frame,
                        page_num=i + 1,
                        page_image=img.copy(),
                        on_click=self._on_pdf_thumbnail_click,
                        on_double_click=self._on_pdf_thumbnail_double_click
                    )
                    row = i // 2
                    col = i % 2
                    thumb.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
                except Exception as e:
                    print(f"[Debug] Error cargando página PDF {img_path}: {e}")

            self.pdf_page_label.config(text=f"1/{len(files)}" if files else "0/0")
            self.pdf_page_index = 0
        else:
            self.pdf_images_list = []
            self.source_images_list = []
            self.pdf_page_label.config(text="Sin PDF")

    def _on_pdf_thumbnail_click(self, page_num):
        """Maneja el click en un thumbnail de página PDF."""
        self.pdf_page_index = page_num - 1
        self._highlight_pdf_page()
        
        # Actualizar índice de página fuente para compatibilidad
        if self.pdf_images_list and 0 <= self.pdf_page_index < len(self.pdf_images_list):
            self.source_page_index = self.pdf_page_index

    def _on_pdf_thumbnail_double_click(self, page_num):
        """Maneja doble-click en un thumbnail PDF - abre modal de mapeo de figuras."""
        if self.pdf_images_list and 0 <= page_num - 1 < len(self.pdf_images_list):
            page_path = self.pdf_images_list[page_num - 1]
            PdfMappingModal(
                self.root,
                page_image_path=page_path,
                chapter_images=self.current_chapter_images
            )

    def _create_preview_panel(self):
        """Crea el panel de preview derecho."""
        self.preview_container = CardFrame(self.gallery_frame)
        self.preview_container.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.preview_container.columnconfigure(0, weight=1)

        # Header
        tk.Label(
            self.preview_container,
            text="👁️ Vista previa",
            bg=Theme.SURFACE,
            fg=Theme.TEXT,
            font=("Helvetica", 11, "bold"),
            padx=15,
            pady=10,
            anchor="w",
        ).grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Canvas para preview
        self.preview_canvas = tk.Canvas(
            self.preview_container,
            bg=Theme.BACKGROUND,
            highlightthickness=0,
            width=300,
            height=250,
        )
        self.preview_canvas.grid(row=1, column=0, padx=15, pady=10)

        # Info de la imagen
        self.preview_info = tk.Frame(
            self.preview_container, bg=Theme.SURFACE, padx=15, pady=10
        )
        self.preview_info.grid(row=2, column=0, sticky=(tk.W, tk.E))

        self.preview_info_text = tk.Label(
            self.preview_info,
            text="Selecciona una imagen\npara ver detalles",
            bg=Theme.SURFACE,
            fg=Theme.TEXT_SECONDARY,
            font=("Helvetica", 10),
            justify="left",
        )
        self.preview_info_text.pack(anchor="w")

        # Panel de traducción (si está disponible)
        if self.translation_manager:
            self._create_translation_panel()

    def _create_translation_panel(self):
        """Crea el panel de opciones de traducción."""
        translation_frame = tk.LabelFrame(
            self.preview_container,
            text=" Traducción IA ",
            bg=Theme.SURFACE,
            fg=Theme.TEXT,
            font=("Helvetica", 10, "bold"),
            padx=10,
            pady=10,
        )
        translation_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=15, pady=10)

        # Selector de modelo
        model_frame = tk.Frame(translation_frame, bg=Theme.SURFACE)
        model_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            model_frame,
            text="Modelo:",
            bg=Theme.SURFACE,
            fg=Theme.TEXT_SECONDARY,
            font=("Helvetica", 9),
        ).pack(side=tk.LEFT)

        self.model_var = tk.StringVar(value="Cargando modelos...")
        self.model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=["Cargando modelos..."],
            state="readonly",
            width=30,
        )
        self.model_combo.pack(side=tk.LEFT, padx=(5, 0))
        self.model_combo.current(0)

        self.model_combo.bind("<<ComboboxSelected>>", self._on_model_changed)

        # Botón traducir clipboard
        self.btn_translate_clipboard = tk.Button(
            translation_frame,
            text="📋 Traducir del clipboard",
            command=self._translate_from_clipboard,
            bg=Theme.PRIMARY,
            fg="white",
            font=("Helvetica", 9),
            padx=10,
            pady=5,
            cursor="hand2",
            relief=tk.FLAT,
        )
        self.btn_translate_clipboard.pack(fill=tk.X, pady=(0, 5))

        # Status
        self.translation_status = tk.Label(
            translation_frame,
            text="⏳ Cargando modelos desde API...",
            bg=Theme.SURFACE,
            fg=Theme.TEXT_SECONDARY,
            font=("Helvetica", 9),
        )
        self.translation_status.pack(anchor="w")
        
        # Cargar modelos desde API en un hilo separado
        self._load_models_async()
    
    def _load_models_async(self):
        """Carga modelos desde la API de Google en un hilo separado."""
        def fetch_and_update():
            try:
                # Obtener modelos desde la API
                models_info = self.translation_manager.fetch_models_from_api()
                models = [(m.name, m.value) for m in models_info]
                
                # Actualizar UI desde el hilo principal
                self.root.after(0, lambda: self._update_models_combobox(models))
            except Exception as e:
                print(f"[Debug] Error cargando modelos: {e}")
                # Usar fallback
                models = TranslationManager.get_available_models()
                self.root.after(0, lambda: self._update_models_combobox(models, error=True))
        
        thread = threading.Thread(target=fetch_and_update, daemon=True)
        thread.start()
    
    def _update_models_combobox(self, models: list[tuple[str, str]], error: bool = False):
        """Actualiza el combobox con los modelos obtenidos."""
        if models:
            self.model_combo['values'] = [name for name, _ in models]
            self.model_combo.current(0)
            
            # Configurar el modelo inicial
            _, initial_model_value = models[0]
            self.translation_manager.change_model(initial_model_value)
            
            if error:
                self.translation_status.config(
                    text=f"⚠️ Usando modelos predefinidos",
                    fg=Theme.WARNING if hasattr(Theme, 'WARNING') else "#FFA500",
                )
            else:
                self.translation_status.config(
                    text=f"✅ {len(models)} modelos cargados",
                    fg=Theme.SUCCESS,
                )
        else:
            self.translation_status.config(
                text="❌ No se pudieron cargar modelos",
                fg=Theme.DANGER,
            )

    def _on_model_changed(self, event):
        """Cambia el modelo de traducción cuando el usuario selecciona otro."""
        if not self.translation_manager:
            return

        selected_idx = self.model_combo.current()
        models = TranslationManager.get_available_models()

        if 0 <= selected_idx < len(models):
            _, model_value = models[selected_idx]
            try:
                self.translation_manager.change_model(model_value)
                self.translation_status.config(
                    text=f"✅ {self.translation_manager.current_model_friendly_name}",
                    fg=Theme.SUCCESS,
                )
                print(f"[Debug] Modelo cambiado a: {model_value}")
            except Exception as e:
                self.translation_status.config(
                    text=f"❌ Error: {str(e)[:30]}", fg=Theme.DANGER
                )
                messagebox.showerror("Error", f"No se pudo cambiar el modelo:\n{e}")

    def _create_options_panel(self):
        """Crea el panel de opciones de compresión."""
        self.options_frame = tk.Frame(self.main_frame, bg=Theme.BACKGROUND)
        self.options_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(15, 0))

        # Card de opciones
        options_card = CardFrame(self.options_frame)
        options_card.pack(fill=tk.X)

        tk.Label(
            options_card,
            text="⚙️ Opciones de compresión",
            bg=Theme.SURFACE,
            fg=Theme.TEXT,
            font=("Helvetica", 10, "bold"),
            padx=15,
            pady=10,
            anchor="w",
        ).pack(fill=tk.X)

        # Controles
        controls = tk.Frame(options_card, bg=Theme.SURFACE, padx=15, pady=10)
        controls.pack(fill=tk.X)

        # Calidad
        quality_frame = tk.Frame(controls, bg=Theme.SURFACE)
        quality_frame.pack(side=tk.LEFT, padx=(0, 30))

        tk.Label(
            quality_frame,
            text="Calidad:",
            bg=Theme.SURFACE,
            fg=Theme.TEXT_SECONDARY,
            font=("Helvetica", 9),
        ).pack(side=tk.LEFT)

        self.quality_var = tk.IntVar(value=DEFAULT_QUALITY)
        self.quality_scale = tk.Scale(
            quality_frame,
            from_=30,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.quality_var,
            length=150,
            bg=Theme.SURFACE,
            highlightthickness=0,
            troughcolor=Theme.BORDER,
            activebackground=Theme.PRIMARY,
        )
        self.quality_scale.pack(side=tk.LEFT, padx=(10, 0))

        self.quality_label = tk.Label(
            quality_frame,
            text=f"{DEFAULT_QUALITY}%",
            bg=Theme.SURFACE,
            fg=Theme.TEXT,
            font=("Helvetica", 9, "bold"),
            width=4,
        )
        self.quality_label.pack(side=tk.LEFT)

        self.quality_var.trace_add(
            "write",
            lambda *args: self.quality_label.config(text=f"{self.quality_var.get()}%"),
        )

        # Ancho máximo
        width_frame = tk.Frame(controls, bg=Theme.SURFACE)
        width_frame.pack(side=tk.LEFT, padx=(0, 30))

        tk.Label(
            width_frame,
            text="Ancho máx:",
            bg=Theme.SURFACE,
            fg=Theme.TEXT_SECONDARY,
            font=("Helvetica", 9),
        ).pack(side=tk.LEFT)

        self.max_width_var = tk.IntVar(value=DEFAULT_MAX_WIDTH)
        tk.Spinbox(
            width_frame,
            from_=400,
            to=2400,
            width=6,
            textvariable=self.max_width_var,
            bg=Theme.SURFACE,
        ).pack(side=tk.LEFT, padx=(5, 0))

        tk.Label(
            width_frame,
            text="px",
            bg=Theme.SURFACE,
            fg=Theme.TEXT_SECONDARY,
            font=("Helvetica", 9),
        ).pack(side=tk.LEFT)

        # Backup checkbox
        self.backup_var = tk.BooleanVar(value=DEFAULT_CREATE_BACKUP)
        tk.Checkbutton(
            controls,
            text="Crear backup",
            variable=self.backup_var,
            bg=Theme.SURFACE,
            fg=Theme.TEXT,
            font=("Helvetica", 9),
            selectcolor=Theme.SURFACE,
            activebackground=Theme.SURFACE,
        ).pack(side=tk.LEFT, padx=(30, 0))

    def _create_statusbar(self):
        """Crea la barra de estado."""
        self.statusbar = tk.Frame(self.root, bg=Theme.SURFACE, height=30)
        self.statusbar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        self.statusbar.grid_propagate(False)

        self.status_label = tk.Label(
            self.statusbar,
            text="Listo",
            bg=Theme.SURFACE,
            fg=Theme.TEXT_SECONDARY,
            font=("Helvetica", 9),
            padx=15,
        )
        self.status_label.pack(side=tk.LEFT)

        # Barra de progreso (oculta por defecto)
        self.progress_bar = ttk.Progressbar(
            self.statusbar, mode="indeterminate", length=150
        )

    # ==================== Métodos de lógica ====================

    def _load_chapters(self):
        """Carga la lista de capítulos en el sidebar."""
        self.chapters = self.file_manager.get_chapters()

        # Limpiar botones existentes
        for btn in self.chapter_buttons:
            btn.destroy()
        self.chapter_buttons = []

        # Crear botones
        for i, (num, title, path) in enumerate(self.chapters):
            # Extraer solo el nombre del capítulo sin "Cap. N:"
            display_title = title.replace(f"Cap. {num}: ", "")

            btn = SidebarButton(
                self.chapters_container,
                text=display_title,
                icon=f"{num.zfill(2)}",
                command=lambda idx=i: self._select_chapter(idx),
            )
            btn.pack(fill=tk.X, padx=5, pady=2)
            self.chapter_buttons.append(btn)

        # Seleccionar primer capítulo
        if self.chapters:
            self._select_chapter(0)

    def _select_chapter(self, index):
        """Selecciona un capítulo del sidebar."""
        # Actualizar selección visual
        for i, btn in enumerate(self.chapter_buttons):
            btn.set_selected(i == index)

        self.current_chapter = self.chapters[index]
        self._load_chapter_images()
        
        # Cargar páginas PDF si el panel existe
        if hasattr(self, 'pdf_thumbnails_frame'):
            self._load_pdf_pages()

    def _load_chapter_images(self):
        """Carga las imágenes del capítulo seleccionado."""
        chapter_num = self.current_chapter[0]
        adoc_file = self.current_chapter[2]

        self.status_label.config(text=f"Cargando capítulo {chapter_num}...")

        # Limpiar thumbnails existentes
        for widget in self.thumbnails_frame.winfo_children():
            widget.destroy()

        self.selected_image = None
        self.selected_thumbnail = None
        self._update_toolbar_state()

        # Cargar imágenes referenciadas
        self.current_chapter_images = self.file_manager.extract_images_from_adoc(
            adoc_file
        )

        # Contadores para estadísticas
        existing_count = 0
        missing_count = 0

        # Crear thumbnails en grid de 5 columnas
        for i, img_info in enumerate(self.current_chapter_images):
            row = i // 5
            col = i % 5
            
            # Verificar si la imagen existe
            if img_info['path'].exists():
                existing_count += 1
                thumb = ImageThumbnail(
                    self.thumbnails_frame,
                    img_info=img_info,
                    on_click=self._on_thumbnail_click,
                    on_double_click=self._on_thumbnail_double_click,
                    on_right_click=self._on_thumbnail_right_click,
                )
            else:
                missing_count += 1
                thumb = ShadowThumbnail(
                    self.thumbnails_frame,
                    img_info=img_info,
                    on_click=self._on_shadow_thumbnail_click,
                    on_right_click=self._on_shadow_thumbnail_right_click,
                )
            
            thumb.grid(row=row, column=col, padx=6, pady=6, sticky=(tk.W, tk.E))

        # Actualizar contador con info de pendientes
        total = len(self.current_chapter_images)
        if missing_count > 0:
            self.sidebar_stats.config(text=f"{existing_count}/{total} imágenes ({missing_count} pendientes)")
        else:
            self.sidebar_stats.config(text=f"{total} imágenes")
        self.gallery_header.config(text=f"📚 Imágenes del capítulo {chapter_num}")

        self.status_label.config(text=f"Capítulo {chapter_num} cargado")

    def _on_thumbnail_click(self, img_info):
        """Maneja el click en un thumbnail."""
        # Deseleccionar anterior
        if self.selected_thumbnail:
            self.selected_thumbnail.set_selected(False)

        # Buscar y seleccionar nuevo
        for widget in self.thumbnails_frame.winfo_children():
            if isinstance(widget, ImageThumbnail) and widget.img_info == img_info:
                widget.set_selected(True)
                self.selected_thumbnail = widget
                break

        self.selected_image = img_info
        print(f"[Debug] Imagen seleccionada: {img_info['name']}")
        self._update_toolbar_state()

    def _on_thumbnail_double_click(self, img_info):
        """Maneja doble click en un thumbnail - abre modal de preview."""
        if img_info['path'].exists():
            PreviewModal(
                self.root,
                img_info,
                on_edit=self._open_editor
                # on_compress removed - method doesn't exist yet
            )

    def _on_thumbnail_right_click(self, event, img_info):
        """Maneja click derecho en un thumbnail."""
        from PIL import Image
        from ..image_processor import ImageType
        
        # Crear menú contextual
        menu = tk.Menu(self.root, tearoff=0)

        # Variable para controlar si el menú sigue activo
        self._active_context_menu = menu
        
        # Detectar tipo de imagen para mostrar modo de compresión
        try:
            img = Image.open(img_info["path"])
            img_type = self.image_processor.detect_image_type(img)
            type_labels = {
                ImageType.PHOTO: "📷 Foto",
                ImageType.ILLUSTRATION: "📊 Diagrama",
                ImageType.MIXED: "🔄 Mixto"
            }
            compression_label = type_labels.get(img_type, "🔄 Auto")
            img.close()
        except Exception:
            compression_label = "🔄 Auto"
        
        # Mostrar modo de compresión (informativo)
        menu.add_command(
            label=f"📦 Modo: {compression_label}",
            state="disabled"
        )
        menu.add_separator()

        menu.add_command(
            label="✏️ Editar",
            command=lambda: self._exec_and_close_menu(
                menu, lambda: self._open_editor(img_info)
            ),
        )
        menu.add_command(
            label="📋 Copiar",
            command=lambda: self._exec_and_close_menu(
                menu, lambda: self._copy_image(img_info)
            ),
        )
        menu.add_command(
            label="📌 Pegar",
            command=lambda: self._exec_and_close_menu(
                menu, lambda: self._paste_image(img_info)
            ),
        )
        menu.add_separator()

        if self.translation_manager:
            # Traducción normal (con diálogo)
            menu.add_command(
                label="🌍 Traducir con opciones...",
                command=lambda: self._exec_and_close_menu(
                    menu, lambda: self._translate_image(img_info)
                ),
            )
            
            # Traducción automática (directa)
            if TranslationConfig.AUTO_TRANSLATE_CONTEXT:
                menu.add_command(
                    label="⚡ Traducir automáticamente",
                    command=lambda: self._exec_and_close_menu(
                        menu, lambda: self._auto_translate_image(img_info)
                    ),
                )
            
            menu.add_separator()

        menu.add_command(
            label="📂 Abrir carpeta",
            command=lambda: self._exec_and_close_menu(
                menu, lambda: open_folder_in_explorer(img_info["path"])
            ),
        )
        menu.add_separator()

        # Opción de esquinas redondeadas
        menu.add_checkbutton(
            label="⭕ Esquinas redondeadas (auto)",
            variable=self.rounded_corners_var,
            onvalue=True,
            offvalue=False,
            command=lambda: self._toggle_rounded_corners(),
        )
        menu.add_separator()

        # Opción para optimizar (redondear + comprimir)
        menu.add_command(
            label="🔘 Optimizar imagen (redondear+comprimir)",
            command=lambda: self._exec_and_close_menu(
                menu, lambda: self._round_corners_only(img_info)
            ),
        )

        # Cerrar menú previo si existe
        if hasattr(self, "_active_context_menu") and self._active_context_menu:
            try:
                self._active_context_menu.unpost()
            except tk.TclError:
                pass

        self._active_context_menu = menu
        menu.post(event.x_root, event.y_root)

        # Binding para cerrar con Escape
        def close_menu(event=None):
            if self._active_context_menu:
                try:
                    self._active_context_menu.unpost()
                except tk.TclError:
                    pass
                self._active_context_menu = None

        menu.bind("<Escape>", close_menu)
        menu.bind("<FocusOut>", lambda e: close_menu())

    def _on_shadow_thumbnail_click(self, img_info):
        """Maneja el click en un thumbnail de imagen faltante."""
        # Deseleccionar anterior
        if self.selected_thumbnail:
            self.selected_thumbnail.set_selected(False)

        # Buscar y seleccionar nuevo
        for widget in self.thumbnails_frame.winfo_children():
            if isinstance(widget, ShadowThumbnail) and widget.img_info == img_info:
                widget.set_selected(True)
                self.selected_thumbnail = widget
                break

        self.selected_image = img_info
        
        # Mostrar info en preview
        self.preview_canvas.delete("all")
        self.preview_canvas.create_text(
            150, 125,
            text=f"📷 Imagen pendiente\n\n{img_info['name']}\n\nRuta esperada:\n{img_info['path']}",
            font=("Helvetica", 10),
            fill=Theme.TEXT_SECONDARY,
            width=280,
            justify="center"
        )
        self.preview_info_text.config(
            text=f"⚠️ Imagen no existe\n📁 {img_info['name']}",
            fg=Theme.WARNING
        )
        self._update_toolbar_state()

    def _on_shadow_thumbnail_right_click(self, event, img_info):
        """Maneja click derecho en un thumbnail de imagen faltante."""
        menu = tk.Menu(self.root, tearoff=0)
        self._active_context_menu = menu

        menu.add_command(
            label="📌 Pegar desde clipboard",
            command=lambda: self._exec_and_close_menu(
                menu, lambda: self._create_image_from_clipboard(img_info)
            ),
        )
        menu.add_separator()
        menu.add_command(
            label="📂 Abrir carpeta destino",
            command=lambda: self._exec_and_close_menu(
                menu, lambda: open_folder_in_explorer(img_info['path'].parent)
            ),
        )

        menu.post(event.x_root, event.y_root)

        def close_menu(event=None):
            if self._active_context_menu:
                try:
                    self._active_context_menu.unpost()
                except tk.TclError:
                    pass
                self._active_context_menu = None

        menu.bind("<Escape>", close_menu)
        menu.bind("<FocusOut>", lambda e: close_menu())

    def _create_image_from_clipboard(self, img_info):
        """Crea una nueva imagen desde el clipboard para un placeholder."""
        try:
            if not self.clipboard.has_image():
                messagebox.showwarning(
                    "Clipboard vacío",
                    "No hay imagen en el portapapeles.\n\n"
                    "Copia una imagen primero (Print Screen o Ctrl+C en una imagen).",
                )
                return

            source_img = self.clipboard.get_image()
            target_path = img_info['path']

            # Crear directorio si no existe
            target_path.parent.mkdir(parents=True, exist_ok=True)

            # Guardar imagen temporalmente
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp_path = tmp.name
            source_img.save(tmp_path, "PNG")

            # Comprimir y guardar
            apply_rounded = self.rounded_corners_var.get()
            self.image_processor.max_width = self.max_width_var.get()
            new_size = self.image_processor.compress(
                tmp_path, target_path, apply_rounded_corners=apply_rounded
            )

            # Limpiar temporal
            import os
            os.unlink(tmp_path)

            self.status_label.config(
                text=f"✅ Creada: {img_info['name']} ({new_size / 1024:.1f} KB)"
            )

            messagebox.showinfo(
                "Imagen creada",
                f"✅ Nueva imagen creada exitosamente\n\n"
                f"📁 {img_info['name']}\n"
                f"💾 {new_size / 1024:.1f} KB",
            )

            # Refrescar vista
            self._refresh_chapter()

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear imagen:\n{e}")

    def _exec_and_close_menu(self, menu, callback):
        """Ejecuta un callback y cierra el menú contextual."""
        try:
            menu.unpost()
        except tk.TclError:
            pass
        self._active_context_menu = None
        callback()

    def _toggle_rounded_corners(self):
        """Activa/desactiva el efecto de esquinas redondeadas."""
        state = "activado" if self.rounded_corners_var.get() else "desactivado"
        self.status_label.config(text=f"⭕ Esquinas redondeadas: {state}")

    def _round_corners_only(self, img_info):
        """
        Aplica efecto de esquinas redondeadas con redimensionamiento y optimización.

        Args:
            img_info: Información de la imagen a procesar
        """
        target_path = img_info["path"]
        max_width = self.image_processor.max_width

        try:
            # Cargar imagen
            img = Image.open(target_path)
            original_width, original_height = img.size

            # Redimensionar si es necesario (LANCZOS para preservar nitidez)
            if original_width > max_width:
                ratio = max_width / original_width
                new_height = int(original_height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

            # Convertir a RGBA para soportar transparencia
            img_rgba = img.convert("RGBA")

            # Calcular radio proporcional (1.5% del ancho, limitado 8-24px)
            width = img_rgba.size[0]
            radius = int(width * 1.5 / 100)
            radius = max(8, min(radius, 24))

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

            # Convertir a RGB para cuantización
            img_rgb = Image.new("RGB", img_rgba.size, (255, 255, 255))
            img_rgb.paste(img_rgba, mask=img_rgba.split()[-1])

            # Backup si está habilitado
            if self.backup_var.get():
                backup_path = self.file_manager.get_next_backup_path(target_path)
                import shutil

                shutil.copy2(target_path, backup_path)

            # Guardar imagen optimizada (cuantizada a 256 colores)
            original_size = target_path.stat().st_size
            img_rgb.quantize(colors=256, method=2).save(
                target_path, "PNG", optimize=True
            )
            new_size = target_path.stat().st_size

            # Calcular diferencia
            cambio = (new_size - original_size) / original_size * 100

            self.status_label.config(
                text=f"🔘 Redondeado aplicado: {img_info['name']} ({cambio:+.1f}%)"
            )

            messagebox.showinfo(
                "Esquinas redondeadas",
                f"✅ Efecto aplicado y optimizado\n\n"
                f"📁 {img_info['name']}\n"
                f"📐 {original_width}×{original_height} → {img_rgb.size[0]}×{img_rgb.size[1]} px\n"
                f"💾 {original_size / 1024:.1f} KB → {new_size / 1024:.1f} KB\n"
                f"Cambio: {cambio:+.1f}%",
            )

            # Refrescar vista
            self._refresh_chapter()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo aplicar redondeo:\n{e}")

    def _update_preview(self, img_info):
        """Actualiza el panel de preview."""
        try:
            # Cargar imagen
            img = Image.open(img_info["path"])

            # Redimensionar para preview
            img.thumbnail((300, 250), Image.Resampling.LANCZOS)
            self.preview_photo = ImageTk.PhotoImage(img)

            # Mostrar en canvas
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(150, 125, image=self.preview_photo)

            # Actualizar info
            size_kb = img_info["path"].stat().st_size / 1024
            info_text = (
                f"📁 {img_info['name']}\n"
                f"📐 {img.size[0]}×{img.size[1]} px\n"
                f"💾 {size_kb:.1f} KB"
            )
            self.preview_info_text.config(text=info_text, fg=Theme.TEXT)

        except Exception as e:
            self.preview_info_text.config(
                text=f"Error cargando imagen:\n{e}", fg=Theme.DANGER
            )

    def _update_toolbar_state(self):
        """Actualiza el estado de los botones de la toolbar."""
        has_selection = self.selected_image is not None

        self.btn_replace.set_enabled(has_selection)
        self.btn_translate.set_enabled(
            has_selection and self.translation_manager is not None
        )
        self.btn_edit.set_enabled(has_selection)
        self.btn_copy.set_enabled(has_selection)

    # ==================== Acciones de toolbar ====================

    def _on_replace(self):
        """Reemplaza la imagen seleccionada con imagen del clipboard."""
        if not self.selected_image:
            return

        try:
            # Verificar que hay imagen en el clipboard
            if not self.clipboard.has_image():
                messagebox.showwarning(
                    "Clipboard vacío",
                    "No hay imagen en el portapapeles.\n\n"
                    "Copia una imagen primero (Print Screen o Ctrl+C en una imagen).",
                )
                return

            # Obtener imagen del clipboard
            source_img = self.clipboard.get_image()
            target_info = self.selected_image

            # Confirmar
            if not messagebox.askyesno(
                "Confirmar reemplazo",
                f"¿Reemplazar '{target_info['name']}' con la imagen del clipboard?\n\n"
                f"Imagen de origen: {source_img.size[0]}×{source_img.size[1]} px\n"
                f"Destino: {target_info['path']}",
            ):
                return

            self._do_replace(target_info, source_img)

        except NoImageInClipboardError:
            messagebox.showwarning(
                "Clipboard vacío", "No hay imagen en el portapapeles"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al reemplazar:\n{e}")

    def _do_replace(self, target_info, source_img, backup=True):
        """
        Ejecuta el reemplazo de imagen.

        Args:
            target_info: Info de la imagen destino
            source_img: PIL.Image de origen
            backup: Si True, crea backup antes de reemplazar
        """
        target_path = target_info["path"]

        try:
            # Backup si está habilitado
            if backup and self.backup_var.get():
                backup_path = self.file_manager.get_next_backup_path(target_path)
                import shutil

                shutil.copy2(target_path, backup_path)
                print(f"[Debug] Backup creado: {backup_path}")

            # Guardar imagen temporalmente
            import tempfile

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp_path = tmp.name
            source_img.save(tmp_path, "PNG")

            # Comprimir y reemplazar
            original_size = target_path.stat().st_size
            self.image_processor.max_width = self.max_width_var.get()
            apply_rounded = self.rounded_corners_var.get()
            new_size = self.image_processor.compress(
                tmp_path, target_path, apply_rounded_corners=apply_rounded
            )

            # Limpiar temporal
            import os

            os.unlink(tmp_path)

            # Calcular ahorro
            ahorro = (original_size - new_size) / original_size * 100

            self.status_label.config(
                text=f"✅ Reemplazado: {target_info['name']} ({ahorro:+.1f}%)"
            )

            # Refrescar
            self._refresh_chapter()

            messagebox.showinfo(
                "Éxito",
                f"✅ Imagen reemplazada exitosamente\n\n"
                f"{original_size / 1024:.1f} KB → {new_size / 1024:.1f} KB\n"
                f"Cambio: {ahorro:+.1f}%",
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error al reemplazar:\n{e}")

    def _on_translate(self):
        """Traduce la imagen seleccionada."""
        if self.selected_image:
            self._translate_image(self.selected_image)

    def _on_edit(self):
        """Abre el editor de imágenes."""
        if self.selected_image:
            self._open_editor(self.selected_image)

    def _on_open_folder(self):
        """Abre la carpeta del capítulo actual."""
        if self.current_chapter:
            chapter_dir = IMAGES_DIR / self.current_chapter[0].zfill(2)
            if chapter_dir.exists():
                open_folder_in_explorer(chapter_dir)

    def _open_settings(self):
        """Abre el diálogo de configuración."""
        SettingsDialog(self.root, self.translation_manager)

    def _on_paste(self):
        """Pega imagen desde clipboard reemplazando la imagen seleccionada."""
        if not self.selected_image:
            messagebox.showinfo(
                "Selecciona una imagen",
                "Por favor, selecciona una imagen primero para pegar encima.",
            )
            return

        try:
            # Verificar que hay imagen en el clipboard
            if not self.clipboard.has_image():
                messagebox.showwarning(
                    "Clipboard vacío",
                    "No hay imagen en el portapapeles.\n\n"
                    "Copia una imagen primero (Print Screen o Ctrl+C en una imagen).",
                )
                return

            # Obtener imagen del clipboard y reemplazar
            source_img = self.clipboard.get_image()
            self._do_replace(self.selected_image, source_img)

        except NoImageInClipboardError:
            messagebox.showwarning(
                "Clipboard vacío", "No hay imagen en el portapapeles"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al pegar:\n{e}")

    def _paste_image(self, img_info):
        """Pega imagen desde clipboard con redimensionamiento y optimización."""
        try:
            # Verificar que hay imagen en el clipboard
            if not self.clipboard.has_image():
                messagebox.showwarning(
                    "Clipboard vacío",
                    "No hay imagen en el portapapeles.\n\n"
                    "Copia una imagen primero (Print Screen o Ctrl+C en una imagen).",
                )
                return

            # Obtener imagen del clipboard
            source_img = self.clipboard.get_image()
            original_width, original_height = source_img.size
            max_width = self.image_processor.max_width

            # Redimensionar si es necesario (LANCZOS para preservar nitidez)
            if original_width > max_width:
                ratio = max_width / original_width
                new_height = int(original_height * ratio)
                source_img = source_img.resize(
                    (max_width, new_height), Image.Resampling.LANCZOS
                )

            # Confirmar reemplazo
            if not messagebox.askyesno(
                "Confirmar pegado",
                f"¿Reemplazar '{img_info['name']}' con la imagen del clipboard?\n\n"
                f"Imagen de origen: {original_width}×{original_height} px\n"
                f"Tamaño final: {source_img.size[0]}×{source_img.size[1]} px\n"
                f"Redondeo: {'Sí' if self.rounded_corners_var.get() else 'No'}",
            ):
                return

            # Ejecutar reemplazo
            self._do_replace(img_info, source_img)

        except NoImageInClipboardError:
            messagebox.showwarning(
                "Clipboard vacío", "No hay imagen en el portapapeles"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al pegar:\n{e}")

    def _on_copy(self):
        """Copia la imagen seleccionada al clipboard."""
        if self.selected_image:
            self._copy_image(self.selected_image)

    def _open_editor(self, img_info):
        """Abre el editor de imágenes."""
        ImageEditor(self.root, img_info)

    def _copy_image(self, img_info):
        """Copia una imagen al clipboard."""
        try:
            img = Image.open(img_info["path"])
            self.clipboard.set_image(img)
            self.status_label.config(text=f"📋 Copiado: {img_info['name']}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar: {e}")

    def _translate_image(self, img_info):
        """Traduce una imagen seleccionada."""
        if not self.translation_manager:
            return

        self._run_translation(
            source_name=img_info["name"],
            translate_func=lambda: self.translation_manager.translate_from_file(
                img_info["path"]
            ),
            on_success=lambda img: self._show_translation_result(img, img_info),
        )

    def _auto_translate_image(self, img_info):
        """
        Traduce automáticamente una imagen usando el prompt configurado.
        
        A diferencia de _translate_image, este método:
        - Usa el prompt editable de TranslationConfig
        - Guarda directamente sobre el archivo original sin mostrar diálogo
        - Usa el modelo configurado por omisión
        """
        if not self.translation_manager:
            return
        
        # Verificar que el modelo está configurado
        current_model = self.translation_manager.current_model
        target_model = TranslationConfig.DEFAULT_MODEL
        
        # Cambiar temporalmente al modelo por omisión si es diferente
        if current_model != target_model:
            try:
                self.translation_manager.change_model(target_model)
            except Exception as e:
                messagebox.showerror(
                    "Error de configuración",
                    f"No se pudo cambiar al modelo {target_model}: {e}"
                )
                return
        
        # Ejecutar traducción con el prompt personalizado
        self._run_translation(
            source_name=f"{img_info['name']} (auto)",
            translate_func=lambda: self.translation_manager.translate_image(
                img_info["path"],
                custom_prompt=TranslationConfig.EDITABLE_PROMPT
            ),
            on_success=lambda img: self._on_auto_translation_complete(img, img_info),
        )

    def _on_auto_translation_complete(self, translated_img, img_info):
        """
        Maneja la traducción automática completada.
        Guarda directamente sobre el archivo original.
        """
        try:
            from PIL import Image
            import shutil
            from datetime import datetime
            
            target_path = Path(img_info["path"])
            
            # Crear backup si está habilitado
            if DEFAULT_CREATE_BACKUP:
                backup_path = target_path.with_suffix(target_path.suffix + ".bak")
                shutil.copy2(target_path, backup_path)
            
            # Guardar la imagen traducida
            if translated_img.mode in ('RGBA', 'LA', 'P'):
                translated_img = translated_img.convert('RGB')
            
            translated_img.save(target_path, "PNG", optimize=True)
            
            # Actualizar la vista
            self._refresh_chapter()
            
            messagebox.showinfo(
                "Traducción completada",
                f"Imagen traducida y guardada:\n{target_path.name}"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error al guardar",
                f"La traducción se completó pero no se pudo guardar:\n{e}"
            )

    def _translate_from_clipboard(self):
        """Traduce imagen desde clipboard."""
        if not self.translation_manager:
            return

        try:
            # Verificar que hay imagen antes de mostrar el diálogo
            if not self.clipboard.has_image():
                messagebox.showwarning(
                    "Clipboard vacío", "No hay imagen en el portapapeles"
                )
                return
        except Exception:
            messagebox.showwarning(
                "Clipboard vacío", "No hay imagen en el portapapeles"
            )
            return

        self._run_translation(
            source_name="clipboard",
            translate_func=lambda: self.translation_manager.translate_from_clipboard(),
            on_success=lambda img: self._show_translation_result(img, None),
        )

    def _run_translation(self, source_name, translate_func, on_success):
        """
        Ejecuta la traducción con feedback visual.

        Args:
            source_name: Nombre de la fuente (para mostrar en estado)
            translate_func: Función que realiza la traducción
            on_success: Callback con la imagen traducida
        """
        # Crear ventana de progreso
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Traduciendo...")
        progress_window.geometry("400x150")
        progress_window.transient(self.root)
        progress_window.grab_set()
        progress_window.resizable(False, False)

        # Centrar en la pantalla
        progress_window.update_idletasks()
        x = (progress_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (progress_window.winfo_screenheight() // 2) - (150 // 2)
        progress_window.geometry(f"+{x}+{y}")

        # Contenido
        frame = tk.Frame(progress_window, bg=Theme.BACKGROUND, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        status_label = tk.Label(
            frame,
            text=f"Enviando imagen a Gemini...\n({source_name})",
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT,
            font=("Helvetica", 10),
            justify="center",
        )
        status_label.pack(pady=(0, 15))

        progress_bar = ttk.Progressbar(frame, mode="indeterminate", length=300)
        progress_bar.pack()
        progress_bar.start()

        # Actualizar estado periódicamente
        def update_status():
            if progress_window.winfo_exists():
                status_label.config(
                    text=f"Traduciendo... esto puede tardar unos segundos\n({source_name})"
                )

        self.root.after(3000, update_status)

        # Ejecutar traducción en hilo separado
        def do_translate():
            try:
                translated_image = translate_func()
                self.root.after(
                    0,
                    lambda: self._on_translation_complete(
                        progress_window, translated_image, on_success, None
                    ),
                )
            except Exception as e:
                error_msg = str(e)  # Capturar el mensaje inmediatamente
                self.root.after(
                    0,
                    lambda err=error_msg: self._on_translation_complete(
                        progress_window, None, on_success, err
                    ),
                )

        threading.Thread(target=do_translate, daemon=True).start()

    def _on_translation_complete(
        self, progress_window, translated_image, on_success, error
    ):
        """Maneja la finalización de la traducción."""
        progress_window.destroy()

        if error:
            messagebox.showerror(
                "Error de traducción", f"No se pudo traducir la imagen:\n{error}"
            )
            return

        if translated_image:
            # Verificar que la imagen traducida es diferente de la original
            try:
                # Comparar dimensiones
                original = self.clipboard.get_image()
                if original and original.size == translated_image.size:
                    # Las imágenes tienen el mismo tamaño, podrían ser idénticas
                    # Mostrar advertencia pero permitir continuar
                    print(
                        f"[Debug] Imagen traducida tiene mismo tamaño que original: {original.size}"
                    )
            except Exception as e:
                print(f"[Debug] Error comparando imágenes: {e}")

            on_success(translated_image)

    def _show_translation_result(self, translated_image, original_img_info):
        """Muestra el diálogo con el resultado de la traducción y comparación."""
        # Obtener imagen original del clipboard para comparar
        original_image = None
        try:
            original_image = self.clipboard.get_image()
        except Exception:
            pass

        # Determinar directorio por defecto
        if original_img_info:
            default_dir = original_img_info["path"].parent
        elif self.current_chapter:
            default_dir = IMAGES_DIR / self.current_chapter[0].zfill(2)
        else:
            default_dir = IMAGES_DIR

        # Crear diálogo personalizado - más grande para mejor preview
        dialog = tk.Toplevel(self.root)
        dialog.title("Imagen traducida - Resultado")
        dialog.geometry("1100x800")
        dialog.minsize(1000, 700)
        dialog.transient(self.root)
        dialog.grab_set()

        # Frame principal
        main_frame = tk.Frame(dialog, bg=Theme.BACKGROUND, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Título
        tk.Label(
            main_frame,
            text="✅ Traducción completada",
            bg=Theme.BACKGROUND,
            fg=Theme.SUCCESS,
            font=("Helvetica", 14, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Verificar si las imágenes son idénticas
        images_identical = False
        if original_image and original_image.size == translated_image.size:
            # Comparar píxeles (muestra de 100x100 en el centro)
            try:
                orig_sample = original_image.crop(
                    (
                        0,
                        0,
                        min(100, original_image.size[0]),
                        min(100, original_image.size[1]),
                    )
                )
                trans_sample = translated_image.crop(
                    (
                        0,
                        0,
                        min(100, translated_image.size[0]),
                        min(100, translated_image.size[1]),
                    )
                )
                if list(orig_sample.getdata()) == list(trans_sample.getdata()):
                    images_identical = True
            except Exception:
                pass

        if images_identical:
            warning_label = tk.Label(
                main_frame,
                text="⚠️ ADVERTENCIA: La imagen traducida parece ser idéntica a la original.\n"
                "La API puede no haber procesado la imagen correctamente.",
                bg=Theme.BACKGROUND,
                fg=Theme.DANGER,
                font=("Helvetica", 10, "bold"),
                justify="center",
            )
            warning_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Panel izquierdo: Original
        if original_image:
            original_frame = tk.LabelFrame(
                main_frame,
                text=" 📷 Imagen Original (Clipboard) ",
                bg=Theme.SURFACE,
                fg=Theme.TEXT,
                font=("Helvetica", 10, "bold"),
            )
            original_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 5), pady=5)
            original_frame.columnconfigure(0, weight=1)
            original_frame.rowconfigure(0, weight=1)

            # Mostrar imagen más grande con scroll si es necesario
            orig_copy = original_image.copy()
            max_preview = (450, 450)
            orig_copy.thumbnail(max_preview, Image.Resampling.LANCZOS)
            orig_photo = ImageTk.PhotoImage(orig_copy)

            # Frame scrollable para imagen grande
            orig_scroll_frame = tk.Frame(original_frame, bg=Theme.SURFACE)
            orig_scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            orig_scroll_frame.columnconfigure(0, weight=1)
            orig_scroll_frame.rowconfigure(0, weight=1)

            orig_canvas = tk.Canvas(
                orig_scroll_frame, bg=Theme.SURFACE, highlightthickness=0
            )
            orig_canvas.grid(row=0, column=0, sticky="nsew")

            orig_hscroll = ttk.Scrollbar(
                orig_scroll_frame, orient=tk.HORIZONTAL, command=orig_canvas.xview
            )
            orig_vscroll = ttk.Scrollbar(
                orig_scroll_frame, orient=tk.VERTICAL, command=orig_canvas.yview
            )
            orig_canvas.configure(
                xscrollcommand=orig_hscroll.set, yscrollcommand=orig_vscroll.set
            )

            orig_hscroll.grid(row=1, column=0, sticky="ew")
            orig_vscroll.grid(row=0, column=1, sticky="ns")

            orig_canvas.create_image(0, 0, anchor="nw", image=orig_photo)
            orig_canvas.config(
                scrollregion=(0, 0, orig_copy.size[0], orig_copy.size[1])
            )
            orig_canvas.image = orig_photo  # Mantener referencia

        # Panel derecho: Traducida
        translated_frame = tk.LabelFrame(
            main_frame,
            text=" ✨ Imagen Traducida (Gemini) ",
            bg=Theme.SURFACE,
            fg=Theme.TEXT,
            font=("Helvetica", 10, "bold"),
        )
        translated_frame.grid(row=2, column=1, sticky="nsew", padx=(5, 0), pady=5)
        translated_frame.columnconfigure(0, weight=1)
        translated_frame.rowconfigure(0, weight=1)

        # Mostrar imagen traducida más grande con scroll
        trans_copy = translated_image.copy()
        max_preview = (450, 450)
        trans_copy.thumbnail(max_preview, Image.Resampling.LANCZOS)
        trans_photo = ImageTk.PhotoImage(trans_copy)

        # Frame scrollable para imagen grande
        trans_scroll_frame = tk.Frame(translated_frame, bg=Theme.SURFACE)
        trans_scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        trans_scroll_frame.columnconfigure(0, weight=1)
        trans_scroll_frame.rowconfigure(0, weight=1)

        trans_canvas = tk.Canvas(
            trans_scroll_frame, bg=Theme.SURFACE, highlightthickness=0
        )
        trans_canvas.grid(row=0, column=0, sticky="nsew")

        trans_hscroll = ttk.Scrollbar(
            trans_scroll_frame, orient=tk.HORIZONTAL, command=trans_canvas.xview
        )
        trans_vscroll = ttk.Scrollbar(
            trans_scroll_frame, orient=tk.VERTICAL, command=trans_canvas.yview
        )
        trans_canvas.configure(
            xscrollcommand=trans_hscroll.set, yscrollcommand=trans_vscroll.set
        )

        trans_hscroll.grid(row=1, column=0, sticky="ew")
        trans_vscroll.grid(row=0, column=1, sticky="ns")

        trans_canvas.create_image(0, 0, anchor="nw", image=trans_photo)
        trans_canvas.config(scrollregion=(0, 0, trans_copy.size[0], trans_copy.size[1]))
        trans_canvas.image = trans_photo  # Mantener referencia

        # Info debajo de las imágenes
        info_frame = tk.Frame(main_frame, bg=Theme.BACKGROUND)
        info_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

        tk.Label(
            info_frame,
            text=f"Dimensiones traducida: {translated_image.size[0]}×{translated_image.size[1]} px",
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_SECONDARY,
            font=("Helvetica", 9),
        ).pack(side=tk.LEFT)

        if original_image:
            tk.Label(
                info_frame,
                text=f"| Dimensiones original: {original_image.size[0]}×{original_image.size[1]} px",
                bg=Theme.BACKGROUND,
                fg=Theme.TEXT_SECONDARY,
                font=("Helvetica", 9),
            ).pack(side=tk.LEFT, padx=(10, 0))

        # Opciones de guardado
        options_frame = tk.Frame(main_frame, bg=Theme.BACKGROUND)
        options_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)

        tk.Label(
            options_frame,
            text="Nombre del archivo:",
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT,
            font=("Helvetica", 10),
        ).pack(anchor="w")

        filename_var = tk.StringVar(value="figura_translated.png")
        filename_entry = tk.Entry(
            options_frame, textvariable=filename_var, font=("Helvetica", 10), width=50
        )
        filename_entry.pack(fill=tk.X, pady=(5, 0))

        tk.Label(
            options_frame,
            text=f"Directorio: {default_dir}",
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_SECONDARY,
            font=("Helvetica", 9),
        ).pack(anchor="w", pady=(5, 0))

        # Botones
        buttons_frame = tk.Frame(main_frame, bg=Theme.BACKGROUND)
        buttons_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)

        def save_image():
            filename = filename_var.get()
            if not filename.endswith(".png"):
                filename += ".png"

            save_path = default_dir / filename

            try:
                save_path.parent.mkdir(parents=True, exist_ok=True)
                translated_image.save(save_path, "PNG", optimize=True)
                messagebox.showinfo("Éxito", f"Imagen guardada:\n{save_path}")
                dialog.destroy()

                if original_img_info and original_img_info["path"] == save_path:
                    self._refresh_chapter()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

        def copy_to_clipboard():
            try:
                self.clipboard.set_image(translated_image)
                messagebox.showinfo("Copiado", "Imagen copiada al clipboard.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo copiar:\n{e}")

        def discard():
            dialog.destroy()

        # Botón Guardar
        tk.Button(
            buttons_frame,
            text="💾 Guardar como nuevo",
            command=save_image,
            bg=Theme.PRIMARY,
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief=tk.FLAT,
        ).pack(side=tk.RIGHT, padx=(5, 0))

        # Botón Sustituir original (si hay imagen seleccionada)
        if self.selected_image:

            def replace_original():
                if messagebox.askyesno(
                    "Confirmar sustitución",
                    f"¿Sustituir '{self.selected_image['name']}' con la imagen traducida?\n\n"
                    f"Esta acción sobreescribirá el archivo original.",
                ):
                    try:
                        self._do_replace(
                            self.selected_image, translated_image, backup=True
                        )
                        dialog.destroy()
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo sustituir:\n{e}")

            tk.Button(
                buttons_frame,
                text=f"🔄 Sustituir '{self.selected_image['name'][:20]}...'"
                if len(self.selected_image["name"]) > 20
                else f"🔄 Sustituir '{self.selected_image['name']}'",
                command=replace_original,
                bg=Theme.WARNING,
                fg="white",
                font=("Helvetica", 10, "bold"),
                padx=15,
                pady=8,
                cursor="hand2",
                relief=tk.FLAT,
            ).pack(side=tk.RIGHT, padx=(5, 0))

        # Botón Copiar al clipboard
        tk.Button(
            buttons_frame,
            text="📋 Copiar al clipboard",
            command=copy_to_clipboard,
            bg=Theme.SURFACE,
            fg=Theme.TEXT,
            font=("Helvetica", 10),
            padx=15,
            pady=8,
            cursor="hand2",
            relief=tk.FLAT,
        ).pack(side=tk.RIGHT, padx=(5, 0))

        # Botón Descartar
        tk.Button(
            buttons_frame,
            text="❌ Descartar",
            command=discard,
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_SECONDARY,
            font=("Helvetica", 10),
            padx=15,
            pady=8,
            cursor="hand2",
            relief=tk.FLAT,
        ).pack(side=tk.LEFT, padx=(0, 5))

    def _create_source_panel(self):
        """Crea el panel de extracción desde fuente original con herramientas de marcado."""
        self.source_frame.columnconfigure(0, weight=3)
        self.source_frame.columnconfigure(1, weight=1)
        self.source_frame.rowconfigure(1, weight=1)

        # Inicializar FigureDetector
        self.figure_detector = FigureDetector(self.translation_manager)
        
        # Estado de selección
        self.selection_mode = False
        self.selection_start = None
        self.selection_rect_id = None
        self.figure_rects = []  # IDs de rectángulos dibujados para figuras

        # === TOOLBAR DE FUENTE ===
        source_toolbar = tk.Frame(self.source_frame, bg=Theme.SURFACE, padx=10, pady=10)
        source_toolbar.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Navegación de páginas
        nav_frame = tk.Frame(source_toolbar, bg=Theme.SURFACE)
        nav_frame.pack(side=tk.LEFT)
        
        ToolbarButton(nav_frame, text="◀", command=self._prev_source_page, width=3).pack(side=tk.LEFT)
        self.page_label = tk.Label(
            nav_frame, text="0/0", bg=Theme.SURFACE, fg=Theme.TEXT,
            font=("Helvetica", 10, "bold"), width=8
        )
        self.page_label.pack(side=tk.LEFT, padx=5)
        ToolbarButton(nav_frame, text="▶", command=self._next_source_page, width=3).pack(side=tk.LEFT)

        # Separador
        ttk.Separator(source_toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=15)
        
        # Botones de herramientas
        tools_frame = tk.Frame(source_toolbar, bg=Theme.SURFACE)
        tools_frame.pack(side=tk.LEFT)
        
        self.btn_mark = ToolbarButton(
            tools_frame, text="✂️ Marcar", command=self._toggle_selection_mode
        )
        self.btn_mark.pack(side=tk.LEFT, padx=2)
        
        self.btn_auto_detect = ToolbarButton(
            tools_frame, text="🤖 IA", command=self._auto_detect_figures
        )
        self.btn_auto_detect.pack(side=tk.LEFT, padx=2)
        
        self.btn_ocr_detect = ToolbarButton(
            tools_frame, text="📝 OCR", command=self._ocr_detect_figures
        )
        self.btn_ocr_detect.pack(side=tk.LEFT, padx=2)
        
        ToolbarButton(
            tools_frame, text="🗑️ Limpiar", command=self._clear_detected_figures
        ).pack(side=tk.LEFT, padx=2)
        
        # Status
        self.source_status = tk.Label(
            source_toolbar, text="", bg=Theme.SURFACE, fg=Theme.TEXT_SECONDARY,
            font=("Helvetica", 9)
        )
        self.source_status.pack(side=tk.RIGHT, padx=10)
        
        # === CANVAS PRINCIPAL ===
        canvas_container = tk.Frame(self.source_frame, bg=Theme.BACKGROUND)
        canvas_container.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        canvas_container.columnconfigure(0, weight=1)
        canvas_container.rowconfigure(0, weight=1)
        
        self.source_canvas = tk.Canvas(canvas_container, bg="#202020", highlightthickness=0, cursor="arrow")
        source_scroll_y = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL, command=self.source_canvas.yview)
        source_scroll_x = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL, command=self.source_canvas.xview)
        
        self.source_canvas.configure(yscrollcommand=source_scroll_y.set, xscrollcommand=source_scroll_x.set)
        
        self.source_canvas.grid(row=0, column=0, sticky="nsew")
        source_scroll_y.grid(row=0, column=1, sticky="ns")
        source_scroll_x.grid(row=1, column=0, sticky="ew")
        
        # Eventos de canvas para selección
        self.source_canvas.bind("<ButtonPress-1>", self._on_source_canvas_press)
        self.source_canvas.bind("<B1-Motion>", self._on_source_canvas_drag)
        self.source_canvas.bind("<ButtonRelease-1>", self._on_source_canvas_release)
        
        # === PANEL LATERAL DE FIGURAS ===
        figures_panel = tk.LabelFrame(
            self.source_frame, text=" 📋 Figuras Detectadas ",
            bg=Theme.SURFACE, fg=Theme.TEXT, font=("Helvetica", 10, "bold"),
            padx=10, pady=10
        )
        figures_panel.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
        figures_panel.columnconfigure(0, weight=1)
        figures_panel.rowconfigure(0, weight=1)
        
        # Lista de figuras con scroll
        figures_list_frame = tk.Frame(figures_panel, bg=Theme.SURFACE)
        figures_list_frame.grid(row=0, column=0, sticky="nsew")
        figures_list_frame.columnconfigure(0, weight=1)
        figures_list_frame.rowconfigure(0, weight=1)
        
        self.figures_listbox = tk.Listbox(
            figures_list_frame, bg=Theme.BACKGROUND, fg=Theme.TEXT,
            selectmode=tk.SINGLE, font=("Helvetica", 9),
            selectbackground=Theme.PRIMARY, selectforeground="white",
            height=15, width=40
        )
        figures_scroll = ttk.Scrollbar(figures_list_frame, orient=tk.VERTICAL, command=self.figures_listbox.yview)
        self.figures_listbox.configure(yscrollcommand=figures_scroll.set)
        
        self.figures_listbox.grid(row=0, column=0, sticky="nsew")
        figures_scroll.grid(row=0, column=1, sticky="ns")
        
        self.figures_listbox.bind("<<ListboxSelect>>", self._on_figure_selected)
        
        # Botones de acción para figuras
        figures_actions = tk.Frame(figures_panel, bg=Theme.SURFACE)
        figures_actions.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        
        tk.Button(
            figures_actions, text="📋 Copiar", command=self._copy_selected_figure,
            bg=Theme.PRIMARY, fg="white", font=("Helvetica", 9),
            padx=8, pady=4, cursor="hand2", relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            figures_actions, text="🔗 Asociar", command=self._associate_figure_with_file,
            bg=Theme.WARNING, fg="white", font=("Helvetica", 9),
            padx=8, pady=4, cursor="hand2", relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=2)
        
        # Inicializar estado
        self.source_page_index = 0
        self.source_images_list = []
        self.current_source_image = None
        self.source_scale = 1.0  # Escala actual de la imagen

        # Cargar imágenes si hay capítulo seleccionado
        if self.current_chapter:
            self._load_source_images_list()

    def _load_source_images_list(self):
        """Busca las imágenes renderizadas del capítulo actual."""
        if not self.current_chapter: return
        
        chapter_num = self.current_chapter[0] # "02"
        
        # IMAGES_DIR apunta a es/imagenes
        project_root = IMAGES_DIR.parent.parent
        self.en_images_dir = project_root / "en" / "images" / chapter_num
        
        if self.en_images_dir.exists():
            # Ordenar 'page-1.png', 'page-2.png'... numeric sort
            files = sorted(list(self.en_images_dir.glob("*.png")), key=lambda p: int(p.stem.split('-')[-1]) if '-' in p.stem else 0)
            self.source_images_list = files
            self.source_page_index = 0
            self._load_source_page()
        else:
            self.source_images_list = []
            self.page_label.config(text="No sources")
            self.source_canvas.delete("all")
            self.source_canvas.create_text(400, 300, text=f"No se encontraron fuentes en:\n{self.en_images_dir}", fill="white")

    def _load_source_page(self):
        if not self.source_images_list: return
        
        # Limites
        if self.source_page_index < 0: self.source_page_index = 0
        if self.source_page_index >= len(self.source_images_list): self.source_page_index = len(self.source_images_list) - 1
        
        img_path = self.source_images_list[self.source_page_index]
        self.page_label.config(text=f"{self.source_page_index + 1}/{len(self.source_images_list)}")
        
        try:
            img = Image.open(img_path)
            self.current_source_image = img  # Keep original ref
            
            # Escalar imagen para ajustar al ancho del canvas (fit to width)
            self.source_canvas.update_idletasks()
            canvas_width = self.source_canvas.winfo_width()
            if canvas_width < 100:  # Fallback si el canvas aún no tiene tamaño
                canvas_width = 800
            
            img_width, img_height = img.size
            if img_width > canvas_width:
                self.source_scale = canvas_width / img_width
                new_width = canvas_width
                new_height = int(img_height * self.source_scale)
                img_scaled = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                self.source_scale = 1.0
                img_scaled = img
            
            self.source_photo = ImageTk.PhotoImage(img_scaled)
            
            self.source_canvas.delete("all")
            self.source_canvas.create_image(0, 0, anchor="nw", image=self.source_photo)
            self.source_canvas.config(scrollregion=self.source_canvas.bbox("all"))
            
            # Limpiar figuras de página anterior y redibujar las actuales si las hay
            self.figure_rects.clear()
            for figure in self.figure_detector.figures:
                if figure.source_page == self.source_page_index:
                    self._draw_figure_rect(figure)
            
        except Exception as e:
            print(f"Error loading source page: {e}")

    def _prev_source_page(self):
        if self.source_page_index > 0:
            self.source_page_index -= 1
            self._load_source_page()

    def _next_source_page(self):
        if self.source_page_index < len(self.source_images_list) - 1:
            self.source_page_index += 1
            self._load_source_page()

    def _refresh_chapter(self):
        """Refresca el capítulo actual."""
        if self.current_chapter:
            self._load_chapter_images()

    # ========== MÉTODOS DE FIGURAS ==========
    
    def _toggle_selection_mode(self):
        """Activa/desactiva el modo de marcado de figuras."""
        self.selection_mode = not self.selection_mode
        
        if self.selection_mode:
            self.btn_mark.configure(bg=Theme.SUCCESS)
            self.source_canvas.configure(cursor="crosshair")
            self.source_status.config(text="✂️ Modo marcado: arrastra para seleccionar región")
        else:
            self.btn_mark.configure(bg=Theme.SURFACE)
            self.source_canvas.configure(cursor="arrow")
            self.source_status.config(text="")
    
    def _on_source_canvas_press(self, event):
        """Handler para click inicial en el canvas."""
        if not self.selection_mode:
            return
        
        # Guardar posición inicial (convertida a coordenadas de canvas)
        self.selection_start = (
            self.source_canvas.canvasx(event.x),
            self.source_canvas.canvasy(event.y)
        )
        
        # Eliminar rectángulo de selección anterior
        if self.selection_rect_id:
            self.source_canvas.delete(self.selection_rect_id)
            self.selection_rect_id = None
    
    def _on_source_canvas_drag(self, event):
        """Handler para arrastre del mouse en el canvas."""
        if not self.selection_mode or not self.selection_start:
            return
        
        x1, y1 = self.selection_start
        x2 = self.source_canvas.canvasx(event.x)
        y2 = self.source_canvas.canvasy(event.y)
        
        # Dibujar/actualizar rectángulo de selección
        if self.selection_rect_id:
            self.source_canvas.coords(self.selection_rect_id, x1, y1, x2, y2)
        else:
            self.selection_rect_id = self.source_canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="#00FF00", width=2, dash=(5, 3)
            )
    
    def _on_source_canvas_release(self, event):
        """Handler para soltar el mouse en el canvas."""
        if not self.selection_mode or not self.selection_start:
            return
        
        x1, y1 = self.selection_start
        x2 = self.source_canvas.canvasx(event.x)
        y2 = self.source_canvas.canvasy(event.y)
        
        # Asegurar que las coordenadas están ordenadas
        if x1 > x2: x1, x2 = x2, x1
        if y1 > y2: y1, y2 = y2, y1
        
        # Verificar que la selección tiene tamaño mínimo
        if abs(x2 - x1) < 20 or abs(y2 - y1) < 20:
            self.source_canvas.delete(self.selection_rect_id)
            self.selection_rect_id = None
            self.selection_start = None
            return
        
        # Convertir coordenadas de canvas escalado a imagen original
        if hasattr(self, 'source_scale') and self.source_scale != 1.0:
            scale = self.source_scale
            bbox = (int(x1/scale), int(y1/scale), int(x2/scale), int(y2/scale))
        else:
            bbox = (int(x1), int(y1), int(x2), int(y2))
        
        # Pedir pie de foto al usuario
        self._prompt_for_caption(bbox, (x1, y1, x2, y2))
        
        self.selection_start = None
    
    def _prompt_for_caption(self, bbox: tuple, canvas_coords: tuple):
        """Muestra diálogo para introducir el pie de foto de la figura."""
        from tkinter import simpledialog
        
        caption = simpledialog.askstring(
            "Pie de foto",
            "Introduce el pie de foto de la figura:\n(ej: Figure 2-1. Glider Components)",
            parent=self.root
        )
        
        if caption:
            # Añadir figura al detector
            figure = self.figure_detector.add_manual_figure(
                bbox=bbox,
                caption=caption,
                source_page=self.source_page_index
            )
            
            # Añadir a la lista visual
            self._add_figure_to_list(figure)
            
            # Cambiar color del rectángulo a permanente
            if self.selection_rect_id:
                self.source_canvas.itemconfig(
                    self.selection_rect_id,
                    outline=Theme.SUCCESS, dash=()
                )
                self.figure_rects.append(self.selection_rect_id)
                self.selection_rect_id = None
            
            self.source_status.config(text=f"✅ Figura añadida: {figure.figure_number}")
        else:
            # Cancelado - eliminar rectángulo
            if self.selection_rect_id:
                self.source_canvas.delete(self.selection_rect_id)
                self.selection_rect_id = None
    
    def _add_figure_to_list(self, figure: DetectedFigure):
        """Añade una figura a la lista visual."""
        # Mostrar número, estado de asociación, y caption
        fig_num = figure.figure_number or "??-??"
        check = "✓" if figure.associated_file else "○"
        display_text = f"{check} {fig_num}: {figure.caption}"
        self.figures_listbox.insert(tk.END, display_text)
    
    def _auto_detect_figures(self):
        """Detecta figuras automáticamente usando IA."""
        if not self.current_source_image:
            messagebox.showwarning("Sin imagen", "Primero navega a una página con imágenes.")
            return
        
        if not self.translation_manager:
            messagebox.showwarning("Sin IA", "La traducción IA no está configurada.")
            return
        
        self.source_status.config(text="🤖 Analizando página con IA...")
        self.root.update()
        
        def detect_in_thread():
            try:
                figures = self.figure_detector.detect_figures_with_ai(
                    self.current_source_image,
                    self.source_page_index
                )
                self.root.after(0, lambda: self._on_figures_detected(figures))
            except Exception as e:
                self.root.after(0, lambda: self.source_status.config(
                    text=f"❌ Error: {str(e)[:40]}"
                ))
        
        thread = threading.Thread(target=detect_in_thread, daemon=True)
        thread.start()
    
    def _ocr_detect_figures(self):
        """Detecta figuras usando OCR local (más rápido y económico que IA)."""
        if not self.current_source_image:
            messagebox.showwarning("Sin imagen", "Primero navega a una página con imágenes.")
            return
        
        self.source_status.config(text="📝 Analizando página con OCR...")
        self.root.update()
        
        def detect_in_thread():
            try:
                figures = self.figure_detector.detect_figures_with_ocr(
                    self.current_source_image,
                    self.source_page_index
                )
                self.root.after(0, lambda figs=figures: self._on_figures_detected(figs))
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda err=error_msg: self.source_status.config(
                    text=f"❌ Error OCR: {err[:40]}"
                ))
        
        thread = threading.Thread(target=detect_in_thread, daemon=True)
        thread.start()
    
    def _on_figures_detected(self, figures: list):
        """Callback cuando se detectan figuras (IA u OCR)."""
        if not figures:
            self.source_status.config(text="⚠️ No se detectaron figuras en esta página")
            return
        
        # Obtener directorio de traducciones
        translation_dir = None
        if self.current_chapter:
            chapter_num = self.current_chapter[0].zfill(2)
            translation_dir = IMAGES_DIR / chapter_num
        
        associated_count = 0
        
        # Añadir figuras a la lista y auto-asociar
        for figure in figures:
            # Intentar auto-asociar con archivo traducido
            if translation_dir and translation_dir.exists():
                candidates = self.figure_detector.find_matching_translation_files(figure, translation_dir)
                if candidates:
                    figure.associated_file = candidates[0]
                    associated_count += 1
            
            # Añadir a lista visual con estado
            self._add_figure_to_list(figure)
            self._draw_figure_rect(figure)
        
        status = f"✅ {len(figures)} figuras detectadas"
        if associated_count > 0:
            status += f" ({associated_count} auto-asociadas)"
        self.source_status.config(text=status)
    
    def _draw_figure_rect(self, figure: DetectedFigure):
        """Dibuja un rectángulo para una figura en el canvas."""
        x1, y1, x2, y2 = figure.bbox
        
        # Aplicar escala si es necesario
        if hasattr(self, 'source_scale') and self.source_scale != 1.0:
            scale = self.source_scale
            x1, y1, x2, y2 = int(x1*scale), int(y1*scale), int(x2*scale), int(y2*scale)
        
        rect_id = self.source_canvas.create_rectangle(
            x1, y1, x2, y2,
            outline=Theme.PRIMARY, width=2
        )
        self.figure_rects.append(rect_id)
        
        # Añadir etiqueta con número
        if figure.figure_number:
            self.source_canvas.create_text(
                x1 + 5, y1 + 5,
                text=figure.figure_number,
                anchor="nw", fill=Theme.PRIMARY,
                font=("Helvetica", 10, "bold")
            )
    
    def _clear_detected_figures(self):
        """Limpia todas las figuras detectadas."""
        self.figure_detector.clear()
        self.figures_listbox.delete(0, tk.END)
        
        # Eliminar rectángulos del canvas
        for rect_id in self.figure_rects:
            self.source_canvas.delete(rect_id)
        self.figure_rects.clear()
        
        if self.selection_rect_id:
            self.source_canvas.delete(self.selection_rect_id)
            self.selection_rect_id = None
        
        self.source_status.config(text="🗑️ Figuras limpiadas")
    
    def _on_figure_selected(self, event):
        """Handler cuando se selecciona una figura de la lista."""
        selection = self.figures_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        figures = self.figure_detector.figures
        
        if 0 <= idx < len(figures):
            figure = figures[idx]
            # Resaltar el rectángulo correspondiente
            self._highlight_figure(idx)
    
    def _highlight_figure(self, idx: int):
        """Resalta una figura en el canvas."""
        # Primero restaurar todos los rectángulos a color normal
        for i, rect_id in enumerate(self.figure_rects):
            color = Theme.SUCCESS if i == idx else Theme.PRIMARY
            self.source_canvas.itemconfig(rect_id, outline=color, width=3 if i == idx else 2)
    
    def _copy_selected_figure(self):
        """Copia la figura seleccionada al clipboard."""
        selection = self.figures_listbox.curselection()
        if not selection:
            messagebox.showinfo("Selección", "Selecciona una figura de la lista primero.")
            return
        
        idx = selection[0]
        figures = self.figure_detector.figures
        
        if 0 <= idx < len(figures) and self.current_source_image:
            figure = figures[idx]
            try:
                cropped = figure.crop_from_image(self.current_source_image)
                self.clipboard.set_image(cropped)
                self.source_status.config(text=f"📋 Figura {figure.figure_number} copiada al clipboard")
            except Exception as e:
                messagebox.showerror("Error", f"Error al copiar: {e}")
    
    def _associate_figure_with_file(self):
        """Asocia la figura seleccionada con un archivo de traducción."""
        selection = self.figures_listbox.curselection()
        if not selection:
            messagebox.showinfo("Selección", "Selecciona una figura de la lista primero.")
            return
        
        if not self.current_chapter:
            return
        
        idx = selection[0]
        figures = self.figure_detector.figures
        
        if 0 <= idx < len(figures):
            figure = figures[idx]
            
            # Buscar archivos candidatos
            chapter_num = self.current_chapter[0].zfill(2)
            translation_dir = IMAGES_DIR / chapter_num
            
            candidates = self.figure_detector.find_matching_translation_files(figure, translation_dir)
            
            if candidates:
                # Mostrar diálogo de selección
                from tkinter import simpledialog
                
                options = [c.name for c in candidates]
                options.append("(Otro archivo...)")
                
                # Diálogo simple - mostrar primer candidato como sugerencia
                result = messagebox.askyesnocancel(
                    "Asociar figura",
                    f"¿Asociar '{figure.caption}' con:\n\n{candidates[0].name}?"
                )
                
                if result is True:
                    figure.associated_file = candidates[0]
                    self.source_status.config(text=f"🔗 Asociado: {candidates[0].name}")
                elif result is False and len(candidates) > 1:
                    # Mostrar otros candidatos
                    messagebox.showinfo(
                        "Otros candidatos",
                        "Candidatos disponibles:\n" + "\n".join(options[:-1])
                    )
            else:
                messagebox.showinfo(
                    "Sin coincidencias",
                    f"No se encontraron archivos para la figura {figure.figure_number}.\n\n"
                    f"Nombre sugerido: {figure.suggested_filename}"
                )


def main():
    """Punto de entrada principal."""
    root = tk.Tk()
    app = ImageManagerAppV2(root)
    root.mainloop()


if __name__ == "__main__":
    main()
