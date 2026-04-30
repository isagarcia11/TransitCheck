import customtkinter as ctk # type: ignore
from ui.ventana_analizador import TabAnalizador
from ui.ventana_formulario import TabFormulario

# ── Tema global ──────────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Paleta de colores TransitCheck
COLORES = {
    "primario":     "#1A56DB",   # azul institucional
    "primario_h":   "#1648C0",   # hover
    "exito":        "#057A55",   # verde validación OK
    "error":        "#C81E1E",   # rojo validación error
    "fondo":        "#F9FAFB",   # gris muy claro (fondo app)
    "superficie":   "#FFFFFF",   # blanco (tarjetas)
    "borde":        "#E5E7EB",   # gris borde
    "texto":        "#111827",   # casi negro
    "texto_sec":    "#6B7280",   # gris secundario
    "acento":       "#EFF6FF",   # azul muy claro (highlights)
}


class VentanaPrincipal(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ── Configuración de la ventana ──────────────────────
        self.title("TransitCheck — Oficina de Tránsito y Movilidad")
        self.geometry("1000x700")
        self.minsize(860, 600)
        self.configure(fg_color=COLORES["fondo"])

        # ── Layout principal ─────────────────────────────────
        self._construir_header()
        self._construir_tabs()

    # ─────────────────────────────────────────────────────────
    def _construir_header(self):
        """Barra superior con logo y título."""
        header = ctk.CTkFrame(
            self,
            fg_color=COLORES["primario"],
            corner_radius=0,
            height=64,
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        # Ícono (emoji como placeholder visual)
        ctk.CTkLabel(
            header,
            text="🚦",
            font=ctk.CTkFont(size=28),
            text_color="#FFFFFF",
        ).pack(side="left", padx=(20, 8), pady=14)

        # Título
        ctk.CTkLabel(
            header,
            text="TransitCheck",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFFFFF",
        ).pack(side="left", pady=14)

        # Subtítulo
        ctk.CTkLabel(
            header,
            text="  |  Sistema de Búsqueda y Validación de Patrones",
            font=ctk.CTkFont(size=13),
            text_color="#BFDBFE",
        ).pack(side="left", pady=14)

    # ─────────────────────────────────────────────────────────
    def _construir_tabs(self):
        """TabView con las dos pestañas principales."""
        self.tabs = ctk.CTkTabview(
            self,
            fg_color=COLORES["fondo"],
            segmented_button_fg_color=COLORES["borde"],
            segmented_button_selected_color=COLORES["primario"],
            segmented_button_selected_hover_color=COLORES["primario_h"],
            segmented_button_unselected_color=COLORES["borde"],
            segmented_button_unselected_hover_color="#D1D5DB",
            text_color=COLORES["texto"],
            text_color_disabled=COLORES["texto_sec"],
        )
        self.tabs.pack(fill="both", expand=True, padx=16, pady=(10, 16))

        # Crear pestañas
        self.tabs.add("Analizador de texto")
        self.tabs.add("Formulario de registro")

        # Instanciar módulos de cada pestaña
        TabAnalizador(
            self.tabs.tab("Analizador de texto"),
            colores=COLORES,
        )
        TabFormulario(
            self.tabs.tab("Formulario de registro"),
            colores=COLORES,
        )