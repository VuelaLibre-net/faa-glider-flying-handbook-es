"""
Editor de imágenes con etiquetado
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from PIL import Image, ImageTk, ImageDraw, ImageFont

from ..config import BADGE_STYLES


class ImageEditor:
    """Editor de imágenes con funcionalidad de etiquetado."""
    
    def __init__(self, parent, img_info: dict):
        """
        Inicializa el editor.
        
        Args:
            parent: Ventana padre (Tk o Toplevel)
            img_info: Diccionario con información de la imagen
        """
        self.img_info = img_info
        self.img_path = img_info['path']
        
        # Crear ventana
        self.window = tk.Toplevel(parent)
        self.window.title(f"Editor de Imagen - {img_info['name']}")
        self.window.geometry("1000x700")
        self.window.minsize(800, 600)
        
        # Referencias para etiquetas
        self.labels = []
        self.original_img = None
        self.display_img = None
        self.canvas = None
        
        self._create_ui()
        self._load_image()
    
    def _create_ui(self):
        """Crea la interfaz de usuario."""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Info de la imagen
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(info_frame, text=f"📁 {self.img_info['name']}",
                 font=("Helvetica", 12, "bold")).pack(side=tk.LEFT)
        
        # Canvas con scrollbars
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#2b2b2b")
        h_scroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Panel de herramientas
        tools_frame = ttk.LabelFrame(main_frame, text="Herramientas de etiquetado", padding="10")
        tools_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Texto de etiqueta
        ttk.Label(tools_frame, text="Texto:").pack(side=tk.LEFT)
        self.label_text = ttk.Entry(tools_frame, width=30)
        self.label_text.pack(side=tk.LEFT, padx=(5, 10))
        self.label_text.insert(0, "Etiqueta traducida")
        
        # Estilo
        ttk.Label(tools_frame, text="Estilo:").pack(side=tk.LEFT, padx=(10, 0))
        self.badge_style = ttk.Combobox(
            tools_frame,
            values=list(BADGE_STYLES.keys()),
            width=15,
            state="readonly"
        )
        self.badge_style.pack(side=tk.LEFT, padx=5)
        self.badge_style.set("Azul (Blue)")
        
        # Tamaño
        ttk.Label(tools_frame, text="Tamaño:").pack(side=tk.LEFT, padx=(10, 0))
        self.font_size = ttk.Spinbox(tools_frame, from_=8, to=72, width=5)
        self.font_size.pack(side=tk.LEFT, padx=5)
        self.font_size.set("14")
        
        # Botones
        ttk.Button(tools_frame, text="➕ Añadir", command=self._add_label).pack(side=tk.LEFT, padx=(20, 5))
        ttk.Button(tools_frame, text="🗑️ Limpiar", command=self._clear_labels).pack(side=tk.LEFT, padx=5)
        
        # Botones de acción
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(buttons_frame, text="💾 Guardar", command=self._save_image).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="❌ Cerrar", command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Instrucciones
        ttk.Label(main_frame,
                 text="💡 Doble click en la imagen para posicionar etiqueta | Arrastra para mover",
                 font=("Helvetica", 9, "italic"),
                 foreground="gray").pack(fill=tk.X, pady=(5, 0))
    
    def _load_image(self):
        """Carga la imagen en el canvas."""
        try:
            self.original_img = Image.open(self.img_path)
            
            # Redimensionar para pantalla
            max_size = (800, 600)
            self.display_img = self.original_img.copy()
            self.display_img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Mostrar
            photo = ImageTk.PhotoImage(self.display_img)
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW, tags="image")
            self.canvas.image = photo  # Mantener referencia
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{e}")
            self.window.destroy()
    
    def _create_rounded_rect(self, x1, y1, x2, y2, radius=8, **kwargs):
        """Crea un rectángulo con esquinas redondeadas."""
        points = [
            x1+radius, y1,
            x2-radius, y1, x2, y1,
            x2, y1+radius, x2, y2-radius,
            x2, y2, x2-radius, y2,
            x1+radius, y2, x1, y2,
            x1, y2-radius, x1, y1+radius,
            x1, y1,
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    
    def _add_label(self):
        """Añade una etiqueta a la imagen."""
        text = self.label_text.get()
        if not text:
            messagebox.showwarning("Aviso", "Introduce un texto para la etiqueta")
            return
        
        style = BADGE_STYLES.get(self.badge_style.get(), BADGE_STYLES["Azul (Blue)"])
        size = int(self.font_size.get())
        
        # Posición inicial
        x, y = 100, 100
        
        # Crear texto
        label_id = self.canvas.create_text(
            x, y, text=text, fill=style["fg"],
            font=("Helvetica", size, "bold"),
            tags=("label", f"label_{len(self.labels)}")
        )
        
        # Crear fondo (badge)
        bbox = self.canvas.bbox(label_id)
        if bbox:
            padding_x, padding_y = 12, 6
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            badge_width = text_width + (padding_x * 2)
            badge_height = text_height + (padding_y * 2)
            
            x1 = x - badge_width // 2
            y1 = y - badge_height // 2
            x2 = x1 + badge_width
            y2 = y1 + badge_height
            
            rect_id = self._create_rounded_rect(
                x1, y1, x2, y2, radius=8,
                fill=style["bg"], outline=style["border"], width=1,
                tags=("label_bg", f"label_bg_{len(self.labels)}")
            )
            
            self.canvas.tag_raise(label_id, rect_id)
        else:
            rect_id = None
        
        # Guardar referencia
        label_index = len(self.labels)
        self.labels.append({
            'text': text, 'x': x, 'y': y,
            'bg': style["bg"], 'fg': style["fg"],
            'border': style["border"], 'size': size,
            'padding_x': 12, 'padding_y': 6,
            'label_id': label_id, 'rect_id': rect_id
        })
        
        # Hacer arrastrable
        def on_drag(event, idx=label_index, lid=label_id, rid=rect_id):
            self.labels[idx]['x'] = event.x
            self.labels[idx]['y'] = event.y
            self.canvas.coords(lid, event.x, event.y)
            
            if rid:
                bbox = self.canvas.bbox(lid)
                if bbox:
                    px = self.labels[idx]['padding_x']
                    py = self.labels[idx]['padding_y']
                    text_w = bbox[2] - bbox[0]
                    text_h = bbox[3] - bbox[1]
                    badge_w = text_w + px * 2
                    badge_h = text_h + py * 2
                    
                    bx1 = event.x - badge_w // 2
                    by1 = event.y - badge_h // 2
                    bx2 = bx1 + badge_w
                    by2 = by1 + badge_h
                    self.canvas.coords(rid, bx1, by1, bx2, by2)
        
        self.canvas.tag_bind(label_id, "<B1-Motion>", on_drag)
        if rect_id:
            self.canvas.tag_bind(rect_id, "<B1-Motion>", on_drag)
        
        self.label_text.delete(0, tk.END)
    
    def _clear_labels(self):
        """Elimina todas las etiquetas."""
        self.canvas.delete("label", "label_bg")
        self.labels = []
    
    def _save_image(self):
        """Guarda la imagen con las etiquetas."""
        if not self.labels:
            messagebox.showinfo("Info", "No hay etiquetas para guardar")
            return
        
        try:
            # Copia de la imagen original
            result_img = self.original_img.copy()
            
            # Convertir a RGB
            if result_img.mode in ('P', 'LA', 'L'):
                result_img = result_img.convert('RGB')
            elif result_img.mode == 'RGBA':
                background = Image.new('RGB', result_img.size, (255, 255, 255))
                background.paste(result_img, mask=result_img.split()[3])
                result_img = background
            
            # Factor de escala
            scale_x = result_img.width / self.display_img.width
            scale_y = result_img.height / self.display_img.height
            
            # Dibujar etiquetas
            draw = ImageDraw.Draw(result_img)
            
            for label in self.labels:
                x = int(label['x'] * scale_x)
                y = int(label['y'] * scale_y)
                size = int(label['size'] * scale_x)
                padding_x = int(label['padding_x'] * scale_x)
                padding_y = int(label['padding_y'] * scale_y)
                
                # Fuente
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", max(8, size))
                except:
                    font = ImageFont.load_default()
                
                # Calcular dimensiones
                bbox = draw.textbbox((0, 0), label['text'], font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                badge_width = text_width + (padding_x * 2)
                badge_height = text_height + (padding_y * 2)
                
                x1 = x - badge_width // 2
                y1 = y - badge_height // 2
                x2 = x1 + badge_width
                y2 = y1 + badge_height
                
                # Dibujar badge
                radius = min(8 * scale_x, badge_width // 4, badge_height // 4)
                draw.rounded_rectangle(
                    [x1, y1, x2, y2],
                    radius=int(radius),
                    fill=label['bg'],
                    outline=label.get('border', label['bg']),
                    width=1
                )
                
                # Texto centrado
                text_x = x - text_width // 2
                text_y = y - text_height // 2
                draw.text((text_x, text_y), label['text'], fill=label['fg'], font=font)
            
            # Guardar
            result_img.save(self.img_path, 'PNG', optimize=True)
            messagebox.showinfo("Éxito", f"Imagen guardada:\n{self.img_info['name']}")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando:\n{e}")
