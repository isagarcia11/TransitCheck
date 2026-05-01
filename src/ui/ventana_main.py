import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import customtkinter as ctk
from ui.ventana_analizador import TabAnalizador
from ui.ventana_formulario import TabFormulario

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COLORES = {
    "primario":   "#1A56DB",
    "primario_h": "#1648C0",
    "exito":      "#057A55",
    "error":      "#C81E1E",
    "fondo":      "#F9FAFB",
    "superficie": "#FFFFFF",
    "borde":      "#E5E7EB",
    "texto":      "#111827",
    "texto_sec":  "#6B7280",
    "acento":     "#EFF6FF",
}


class VentanaPrincipal(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("TransitCheck — Oficina de Tránsito y Movilidad")
        self.geometry("1100x720")
        self.minsize(900, 620)
        self.configure(fg_color=COLORES["fondo"])

        self._tab_activo = "analizador"
        self._frames = {}

        self._construir_header()
        self._construir_nav()
        self._construir_contenido()
        self._mostrar_tab("analizador")

    # ── Header ───────────────────────────────────────────────
    def _construir_header(self):
        header = ctk.CTkFrame(self, fg_color=COLORES["primario"],
                              corner_radius=0, height=56)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="TransitCheck",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#FFFFFF").pack(side="left", padx=(20, 0), pady=14)

        ctk.CTkLabel(header,
                     text="  |  Sistema de Búsqueda y Validación de Patrones",
                     font=ctk.CTkFont(size=13),
                     text_color="#BFDBFE").pack(side="left", pady=14)

    # ── Barra de navegación (simula tabs) ────────────────────
    def _construir_nav(self):
        nav = ctk.CTkFrame(self, fg_color=COLORES["superficie"],
                           corner_radius=0, height=44)
        nav.pack(fill="x", side="top")
        nav.pack_propagate(False)

        self.btn_analizador = ctk.CTkButton(
            nav, text="Analizador de texto",
            command=lambda: self._mostrar_tab("analizador"),
            fg_color=COLORES["primario"],
            hover_color=COLORES["primario_h"],
            text_color="#FFFFFF",
            corner_radius=0,
            font=ctk.CTkFont(size=13),
            height=44, width=200,
        )
        self.btn_analizador.pack(side="left")

        self.btn_formulario = ctk.CTkButton(
            nav, text="Formulario de registro",
            command=lambda: self._mostrar_tab("formulario"),
            fg_color=COLORES["borde"],
            hover_color="#D1D5DB",
            text_color=COLORES["texto"],
            corner_radius=0,
            font=ctk.CTkFont(size=13),
            height=44, width=200,
        )
        self.btn_formulario.pack(side="left")

        # Línea separadora
        ctk.CTkFrame(self, fg_color=COLORES["borde"],
                     height=1, corner_radius=0).pack(fill="x", side="top")

    # ── Área de contenido ────────────────────────────────────
    def _construir_contenido(self):
        self.contenedor = ctk.CTkFrame(self, fg_color=COLORES["fondo"],
                                       corner_radius=0)
        self.contenedor.pack(fill="both", expand=True, side="top")

        # Frame analizador
        frame_a = ctk.CTkFrame(self.contenedor, fg_color=COLORES["fondo"],
                                corner_radius=0)
        TabAnalizador(frame_a, colores=COLORES)
        self._frames["analizador"] = frame_a

        # Frame formulario
        frame_f = ctk.CTkFrame(self.contenedor, fg_color=COLORES["fondo"],
                                corner_radius=0)
        TabFormulario(frame_f, colores=COLORES)
        self._frames["formulario"] = frame_f

    # ── Cambio de pestaña ────────────────────────────────────
    def _mostrar_tab(self, nombre):
        # Ocultar todos
        for frame in self._frames.values():
            frame.place_forget()

        # Mostrar el seleccionado
        self._frames[nombre].place(x=0, y=0, relwidth=1, relheight=1)
        self._tab_activo = nombre

        # Actualizar estilos de botones nav
        if nombre == "analizador":
            self.btn_analizador.configure(fg_color=COLORES["primario"],
                                          text_color="#FFFFFF")
            self.btn_formulario.configure(fg_color=COLORES["borde"],
                                          text_color=COLORES["texto"])
        else:
            self.btn_formulario.configure(fg_color=COLORES["primario"],
                                          text_color="#FFFFFF")
            self.btn_analizador.configure(fg_color=COLORES["borde"],
                                          text_color=COLORES["texto"])