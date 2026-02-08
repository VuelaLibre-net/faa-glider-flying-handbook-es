"""
Diálogo de configuración del Gestor de Imágenes

Permite configurar:
- Modelo de Gemini por omisión
- Prompt de traducción editable
- Estado de conexión con API
"""

import tkinter as tk
from tkinter import ttk, messagebox

from ..config import TranslationConfig, AVAILABLE_MODELS, ConfigManager
from ..translation import TranslationManager, is_translation_available


class SettingsDialog:
    """Diálogo de configuración del gestor de imágenes."""
    
    def __init__(self, parent, translation_manager: TranslationManager = None):
        """
        Inicializa el diálogo de configuración.
        
        Args:
            parent: Ventana padre
            translation_manager: Instancia del gestor de traducción
        """
        self.parent = parent
        self.translation_manager = translation_manager
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("⚙️ Configuración del Gestor de Imágenes")
        self.dialog.geometry("700x600")
        self.dialog.transient(parent)
        # grab_set se aplicará después de que la ventana sea visible
        self.dialog.resizable(True, True)
        
        # Centrar la ventana
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Cargar configuración guardada
        self.saved_config = ConfigManager.load_config()
        
        # Variables (usar valores guardados o predeterminados)
        self.model_var = tk.StringVar(value=self.saved_config.get('default_model', TranslationConfig.DEFAULT_MODEL))
        self.prompt_var = tk.StringVar(value=self.saved_config.get('prompt', TranslationConfig.EDITABLE_PROMPT))
        self.auto_translate_var = tk.BooleanVar(value=self.saved_config.get('auto_translate', TranslationConfig.AUTO_TRANSLATE_CONTEXT))
        self.status_text = tk.StringVar(value="Verificando conexión...")
        
        # Diccionario de modelos (se llenará al cargar desde API)
        self.model_values = {}
        
        self._create_ui()
        self._check_connection()
    
    def _create_ui(self):
        """Crea la interfaz del diálogo."""
        # Aplicar grab después de que la ventana sea visible
        self.dialog.after_idle(self.dialog.grab_set)
        
        # Notebook (pestañas)
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña 1: Configuración de Traducción
        translation_frame = ttk.Frame(notebook, padding="10")
        notebook.add(translation_frame, text="🌍 Traducción")
        self._create_translation_tab(translation_frame)
        
        # Pestaña 2: Estado de Conexión
        status_frame = ttk.Frame(notebook, padding="10")
        notebook.add(status_frame, text="🔌 Estado API")
        self._create_status_tab(status_frame)
        
        # Botones inferiores
        buttons_frame = ttk.Frame(self.dialog, padding="10")
        buttons_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Button(
            buttons_frame,
            text="💾 Guardar",
            command=self._save_settings
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="🔄 Verificar conexión",
            command=self._check_connection
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="❌ Cancelar",
            command=self.dialog.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def _create_translation_tab(self, parent):
        """Crea el contenido de la pestaña de traducción."""
        # Frame para modelo
        model_frame = ttk.LabelFrame(parent, text="Modelo de Gemini", padding="10")
        model_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Label para mostrar modelo por defecto actual
        self.default_model_label = ttk.Label(
            model_frame,
            text=f"⭐ Modelo por defecto actual: {self._get_model_display_name(TranslationConfig.DEFAULT_MODEL)}",
            font=("Helvetica", 9, "bold"),
            foreground="#2563EB"
        )
        self.default_model_label.pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Separator(model_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        ttk.Label(
            model_frame,
            text="Seleccionar modelo:",
            font=("Helvetica", 9)
        ).pack(anchor=tk.W)
        
        # Frame para combobox y botón de actualizar
        model_select_frame = ttk.Frame(model_frame)
        model_select_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Combobox con modelos (inicialmente vacío o con valores por defecto)
        self.model_combo = ttk.Combobox(
            model_select_frame,
            textvariable=self.model_var,
            values=[],  # Se llenará al cargar
            state="readonly",
            width=45
        )
        self.model_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Botón para cargar modelos desde API
        ttk.Button(
            model_select_frame,
            text="🔄 Cargar",
            command=self._fetch_models_from_api,
            width=10
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Descripción del modelo seleccionado
        self.model_desc_label = ttk.Label(
            model_frame,
            text="Carga los modelos disponibles desde la API de Google",
            font=("Helvetica", 8, "italic"),
            foreground="gray"
        )
        self.model_desc_label.pack(anchor=tk.W, pady=(5, 0))
        
        self.model_combo.bind("<<ComboboxSelected>>", self._on_model_change)
        
        # Botón para establecer como predeterminado
        ttk.Button(
            model_frame,
            text="⭐ Establecer como modelo por defecto",
            command=self._set_as_default_model
        ).pack(anchor=tk.W, pady=(10, 0))
        
        # Cargar modelos automáticamente si hay conexión
        self._fetch_models_from_api()
        
        # Frame para prompt
        prompt_frame = ttk.LabelFrame(parent, text="Prompt de Traducción", padding="10")
        prompt_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        ttk.Label(
            prompt_frame,
            text="Prompt editable (se envía a Gemini junto con la imagen):",
            font=("Helvetica", 9)
        ).pack(anchor=tk.W)
        
        # Text widget para el prompt
        self.prompt_text = tk.Text(
            prompt_frame,
            wrap=tk.WORD,
            height=6,
            width=60,
            font=("Helvetica", 9)
        )
        self.prompt_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        self.prompt_text.insert("1.0", TranslationConfig.EDITABLE_PROMPT)
        
        # Scrollbar para el prompt
        prompt_scroll = ttk.Scrollbar(prompt_frame, command=self.prompt_text.yview)
        prompt_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.prompt_text.config(yscrollcommand=prompt_scroll.set)
        
        # Frame para opciones adicionales
        options_frame = ttk.LabelFrame(parent, text="Opciones Adicionales", padding="10")
        options_frame.pack(fill=tk.X)
        
        ttk.Checkbutton(
            options_frame,
            text="Activar traducción automática en menú contextual",
            variable=self.auto_translate_var
        ).pack(anchor=tk.W)
        
        ttk.Label(
            options_frame,
            text="Muestra opción 'Traducir automáticamente' al hacer clic derecho en imágenes",
            font=("Helvetica", 8),
            foreground="gray"
        ).pack(anchor=tk.W, padx=(20, 0))
    
    def _create_status_tab(self, parent):
        """Crea el contenido de la pestaña de estado."""
        # Frame para información de conexión
        info_frame = ttk.LabelFrame(parent, text="Estado de Conexión", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Status label grande
        self.status_big_label = ttk.Label(
            info_frame,
            textvariable=self.status_text,
            font=("Helvetica", 12, "bold")
        )
        self.status_big_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Treeview para detalles
        columns = ("propiedad", "valor")
        self.status_tree = ttk.Treeview(
            info_frame,
            columns=columns,
            show="headings",
            height=10
        )
        self.status_tree.heading("propiedad", text="Propiedad")
        self.status_tree.heading("valor", text="Valor")
        self.status_tree.column("propiedad", width=200)
        self.status_tree.column("valor", width=400)
        
        self.status_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        tree_scroll = ttk.Scrollbar(info_frame, command=self.status_tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_tree.config(yscrollcommand=tree_scroll.set)
        
        # Frame para acciones
        actions_frame = ttk.Frame(parent)
        actions_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            actions_frame,
            text="🔄 Refrescar estado",
            command=self._check_connection
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            actions_frame,
            text="📋 Copiar diagnóstico",
            command=self._copy_diagnostic
        ).pack(side=tk.LEFT, padx=5)
    
    def _get_model_display_name(self, model_value: str) -> str:
        """Obtiene el nombre descriptivo de un modelo a partir de su valor."""
        # Buscar en modelos cargados
        for name, value in self.model_values.items():
            if value == model_value:
                return name
        # Si no se encuentra, devolver el valor truncado
        if len(model_value) > 40:
            return model_value[:40] + "..."
        return model_value
    
    def _fetch_models_from_api(self):
        """Carga los modelos disponibles desde la API de Gemini."""
        if not self.translation_manager:
            self.model_desc_label.config(
                text="❌ Traducción no disponible. Verifica la API key.",
                foreground="red"
            )
            return
        
        self.model_desc_label.config(
            text="🔄 Cargando modelos desde API...",
            foreground="blue"
        )
        self.dialog.update_idletasks()
        
        try:
            # Obtener modelos desde API
            models = self.translation_manager.fetch_models_from_api()
            
            if not models:
                self.model_desc_label.config(
                    text="⚠️ No se encontraron modelos. Usando lista por defecto.",
                    foreground="orange"
                )
                return
            
            # Actualizar diccionario de modelos
            self.model_values = {model.name: model.value for model in models}
            
            # Actualizar combobox
            model_names = list(self.model_values.keys())
            self.model_combo['values'] = model_names
            
            # Seleccionar el modelo actual por defecto si está en la lista
            current_default = TranslationConfig.DEFAULT_MODEL
            selected_name = None
            for name, value in self.model_values.items():
                if value == current_default:
                    selected_name = name
                    break
            
            # Si no se encontró el default, seleccionar el primero
            if selected_name:
                self.model_combo.set(selected_name)
            elif model_names:
                self.model_combo.set(model_names[0])
            
            self.model_desc_label.config(
                text=f"✅ {len(models)} modelos cargados desde API",
                foreground="green"
            )
            
        except Exception as e:
            self.model_desc_label.config(
                text=f"❌ Error cargando modelos: {str(e)[:50]}",
                foreground="red"
            )
    
    def _set_as_default_model(self):
        """Establece el modelo seleccionado como modelo por defecto."""
        selected_name = self.model_combo.get()
        if not selected_name:
            messagebox.showwarning(
                "Sin selección",
                "Por favor, selecciona un modelo primero."
            )
            return
        
        model_value = self.model_values.get(selected_name)
        if not model_value:
            return
        
        # Guardar en archivo de configuración
        if ConfigManager.set_default_model(model_value):
            # Actualizar configuración en memoria
            TranslationConfig.DEFAULT_MODEL = model_value
            
            # Actualizar label
            self.default_model_label.config(
                text=f"⭐ Modelo por defecto actual: {selected_name}"
            )
            
            # Cambiar el modelo en el translation manager si está disponible
            if self.translation_manager:
                try:
                    self.translation_manager.change_model(model_value)
                    messagebox.showinfo(
                        "Modelo actualizado",
                        f"'{selected_name}' se ha guardado como modelo por defecto."
                    )
                except Exception as e:
                    messagebox.showwarning(
                        "Advertencia",
                        f"Modelo guardado pero no se pudo cambiar activamente: {e}"
                    )
            else:
                messagebox.showinfo(
                    "Modelo guardado",
                    f"'{selected_name}' se ha guardado como modelo por defecto.\n"
                    "Se aplicará al reiniciar la aplicación."
                )
        else:
            messagebox.showerror(
                "Error",
                "No se pudo guardar el modelo por defecto."
            )
    
    def _on_model_change(self, event=None):
        """Maneja el cambio de modelo seleccionado."""
        selected = self.model_combo.get()
        if not selected:
            return
        
        # Mostrar información del modelo seleccionado
        model_value = self.model_values.get(selected, "")
        if "image" in model_value.lower():
            desc = "Modelo optimizado para generación/procesamiento de imágenes"
        elif "flash" in model_value.lower():
            desc = "Modelo rápido y económico"
        elif "pro" in model_value.lower():
            desc = "Modelo de alta calidad (puede ser más lento)"
        else:
            desc = "Modelo estándar"
        
        self.model_desc_label.config(text=f"{desc}\nID: {model_value}", foreground="gray")
    
    def _check_connection(self):
        """Verifica el estado de conexión con la API."""
        self.status_text.set("Verificando...")
        self.status_tree.delete(*self.status_tree.get_children())
        
        if not self.translation_manager:
            self.status_text.set("❌ No inicializado")
            self._add_status_row("Estado", "Gestor de traducción no inicializado")
            self._add_status_row("API Key", "No configurada")
            return
        
        try:
            status = self.translation_manager.check_connection_status()
            
            # Actualizar label principal
            if status['status'] == 'ok':
                self.status_text.set(f"✅ Conectado ({status['response_time_ms']}ms)")
            elif status['status'] == 'error':
                self.status_text.set("❌ Error de conexión")
            else:
                self.status_text.set("⚠️ No configurado")
            
            # Añadir filas al treeview
            self._add_status_row("Estado general", status['status'].upper())
            self._add_status_row("API Key presente", "Sí" if status['api_key_present'] else "No")
            self._add_status_row("Fuente API Key", status['api_key_source'])
            self._add_status_row("API Key (preview)", status['api_key_preview'] or "N/A")
            self._add_status_row("Endpoint", status['endpoint'])
            self._add_status_row("Modelo actual", status['current_model'])
            self._add_status_row("Modelo válido", "Sí" if status['model_valid'] else "No")
            self._add_status_row("Modelos disponibles", str(status['models_available']))
            self._add_status_row("Tiempo de respuesta", f"{status['response_time_ms']} ms")
            
            if status['error_message']:
                self._add_status_row("Error", status['error_message'])
                
        except Exception as e:
            self.status_text.set("❌ Error al verificar")
            self._add_status_row("Error", str(e))
    
    def _add_status_row(self, propiedad, valor):
        """Añade una fila al treeview de estado."""
        self.status_tree.insert("", tk.END, values=(propiedad, valor))
    
    def _copy_diagnostic(self):
        """Copia el diagnóstico al portapapeles."""
        diagnostic = []
        for item in self.status_tree.get_children():
            values = self.status_tree.item(item, "values")
            diagnostic.append(f"{values[0]}: {values[1]}")
        
        text = "\n".join(diagnostic)
        self.parent.clipboard_clear()
        self.parent.clipboard_append(text)
        messagebox.showinfo("Copiado", "Diagnóstico copiado al portapapeles")
    
    def _save_settings(self):
        """Guarda la configuración."""
        # Obtener prompt
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        
        # Guardar prompt en archivo
        ConfigManager.set_prompt(prompt)
        ConfigManager.set_auto_translate(self.auto_translate_var.get())
        
        # Actualizar configuración en memoria
        TranslationConfig.EDITABLE_PROMPT = prompt
        TranslationConfig.AUTO_TRANSLATE_CONTEXT = self.auto_translate_var.get()
        
        messagebox.showinfo(
            "Configuración guardada",
            f"Prompt y configuración guardados en:\n{ConfigManager.CONFIG_FILE}\n\n"
            f"Traducción automática: {'Sí' if self.auto_translate_var.get() else 'No'}"
        )
        self.dialog.destroy()
