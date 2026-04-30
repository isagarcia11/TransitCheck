import customtkinter as ctk # type: ignore
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from motor.validadores import (
    validar_correo, validar_telefono, validar_fecha,
    validar_url, validar_placa, validar_cedula,
)

# Configuración de cada campo del formulario
CAMPOS = [
    {
        "id":          "cedula",
        "label":       "Cédula de ciudadanía",
        "icono":       "🪪",
        "placeholder": "Ej: 1094823456",
        "validador":   validar_cedula,
        "hint":        "6–10 dígitos, sin cero al inicio",
    },
    {
        "id":          "nombre",
        "label":       "Nombre completo",
        "icono":       "👤",
        "placeholder": "Ej: Juan Pérez García",
        "validador":   lambda s: len(s.strip()) >= 3,
        "hint":        "Mínimo 3 caracteres",
    },
    {
        "id":          "telefono",
        "label":       "Número telefónico",
        "icono":       "📞",
        "placeholder": "Ej: 3201234567",
        "validador":   validar_telefono,
        "hint":        "10 dígitos, empieza en 3 (prefijo +57 opcional)",
    },
    {
        "id":          "correo",
        "label":       "Correo electrónico",
        "icono":       "📧",
        "placeholder": "Ej: juan.perez@gmail.com",
        "validador":   validar_correo,
        "hint":        "usuario@dominio.ext",
    },
    {
        "id":          "placa",
        "label":       "Placa del vehículo",
        "icono":       "🚗",
        "placeholder": "Ej: ABC123 o XYZ45K",
        "validador":   validar_placa,
        "hint":        "Carro: 3 letras + 3 dígitos  |  Moto: 3 letras + 2 dígitos + 1 letra",
    },
    {
        "id":          "fecha",
        "label":       "Fecha del trámite",
        "icono":       "📅",
        "placeholder": "Ej: 25/04/2025",
        "validador":   validar_fecha,
        "hint":        "DD/MM/AAAA  |  DD-MM-AAAA  |  AAAA/MM/DD",
    },
    {
        "id":          "url",
        "label":       "URL de referencia",
        "icono":       "🌐",
        "placeholder": "Ej: https://www.transito.gov.co",
        "validador":   validar_url,
        "hint":        "Debe iniciar con http:// o https://",
    },
]


class TabFormulario:

    def __init__(self, parent: ctk.CTkFrame, colores: dict):
        self.colores   = colores
        self.parent    = parent
        self.estados   = {}   # id_campo → True/False/None
        self.entradas  = {}   # id_campo → CTkEntry widget
        self.iconos_estado = {}  # id_campo → CTkLabel (✓ o ✗)

        parent.configure(fg_color=colores["fondo"])
        self._construir_layout()

    # ─────────────────────────────────────────────────────────
    def _construir_layout(self):
        C = self.colores

        # Contenedor centrado con scroll
        scroll = ctk.CTkScrollableFrame(
            self.parent,
            fg_color=C["fondo"],
            scrollbar_button_color=C["borde"],
        )
        scroll.pack(fill="both", expand=True)

        # Tarjeta central
        tarjeta = ctk.CTkFrame(
            scroll,
            fg_color=C["superficie"],
            border_color=C["borde"],
            border_width=1,
            corner_radius=12,
        )
        tarjeta.pack(fill="x", padx=60, pady=16)

        # Encabezado tarjeta
        enc = ctk.CTkFrame(tarjeta, fg_color=C["primario"], corner_radius=0,
                           height=52)
        enc.pack(fill="x")
        enc.pack_propagate(False)
        enc.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            enc,
            text="Registro de trámite — Oficina de Tránsito",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFFFFF",
        ).pack(side="left", padx=20, pady=14)

        # Campos
        cuerpo = ctk.CTkFrame(tarjeta, fg_color="transparent")
        cuerpo.pack(fill="x", padx=24, pady=16)

        for cfg in CAMPOS:
            self._agregar_campo(cuerpo, cfg)

        # Separador
        sep = ctk.CTkFrame(tarjeta, fg_color=C["borde"], height=1)
        sep.pack(fill="x", padx=24, pady=(0, 16))

        # Botones
        pie = ctk.CTkFrame(tarjeta, fg_color="transparent")
        pie.pack(fill="x", padx=24, pady=(0, 20))

        self.btn_guardar = ctk.CTkButton(
            pie,
            text="Guardar registro",
            command=self._guardar,
            fg_color=C["primario"],
            hover_color=C["primario_h"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=42,
            state="disabled",
        )
        self.btn_guardar.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            pie,
            text="Limpiar formulario",
            command=self._limpiar,
            fg_color=C["borde"],
            hover_color="#D1D5DB",
            text_color=C["texto"],
            font=ctk.CTkFont(size=12),
            height=42,
            width=150,
        ).pack(side="left")

        # Barra de estado global
        self.lbl_estado_global = ctk.CTkLabel(
            scroll,
            text="Complete todos los campos correctamente para habilitar el guardado.",
            font=ctk.CTkFont(size=12),
            text_color=C["texto_sec"],
        )
        self.lbl_estado_global.pack(pady=(0, 16))

    # ─────────────────────────────────────────────────────────
    def _agregar_campo(self, parent, cfg: dict):
        C = self.colores
        campo_id = cfg["id"]
        self.estados[campo_id] = None  # None = sin tocar

        # Fila completa
        fila = ctk.CTkFrame(parent, fg_color="transparent")
        fila.pack(fill="x", pady=6)

        # Etiqueta con ícono
        ctk.CTkLabel(
            fila,
            text=f"{cfg['icono']}  {cfg['label']}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=C["texto"],
            anchor="w",
            width=220,
        ).pack(side="left", padx=(0, 12))

        # Entrada + ícono de estado
        contenedor = ctk.CTkFrame(fila, fg_color="transparent")
        contenedor.pack(side="left", fill="x", expand=True)

        entrada = ctk.CTkEntry(
            contenedor,
            placeholder_text=cfg["placeholder"],
            font=ctk.CTkFont(size=12, family="Courier"),
            fg_color=C["superficie"],
            border_color=C["borde"],
            border_width=1,
            text_color=C["texto"],
            height=38,
        )
        entrada.pack(side="left", fill="x", expand=True)

        # Ícono de estado (✓ / ✗ / vacío)
        icono = ctk.CTkLabel(
            contenedor,
            text="",
            font=ctk.CTkFont(size=16),
            width=28,
        )
        icono.pack(side="left", padx=(6, 0))

        # Hint debajo
        ctk.CTkLabel(
            parent,
            text=f"   {cfg['hint']}",
            font=ctk.CTkFont(size=11),
            text_color=C["texto_sec"],
            anchor="w",
        ).pack(fill="x", padx=(232, 0), pady=(0, 2))

        # Guardar referencias
        self.entradas[campo_id]      = entrada
        self.iconos_estado[campo_id] = icono

        # Validación en tiempo real (al escribir)
        def al_escribir(event, cid=campo_id, val=cfg["validador"], ent=entrada, ico=icono):
            texto = ent.get().strip()
            if texto == "":
                self.estados[cid] = None
                ent.configure(border_color=C["borde"])
                ico.configure(text="", text_color=C["texto_sec"])
            elif val(texto):
                self.estados[cid] = True
                ent.configure(border_color=C["exito"])
                ico.configure(text="✓", text_color=C["exito"])
            else:
                self.estados[cid] = False
                ent.configure(border_color=C["error"])
                ico.configure(text="✗", text_color=C["error"])
            self._actualizar_boton()

        entrada.bind("<KeyRelease>", al_escribir)

    # ─────────────────────────────────────────────────────────
    def _actualizar_boton(self):
        C = self.colores
        todos_validos = all(v is True for v in self.estados.values())
        alguno_invalido = any(v is False for v in self.estados.values())
        vacios = sum(1 for v in self.estados.values() if v is None)

        if todos_validos:
            self.btn_guardar.configure(state="normal", fg_color=C["exito"])
            self.lbl_estado_global.configure(
                text="Todo correcto. Puede guardar el registro.",
                text_color=C["exito"],
            )
        elif alguno_invalido:
            self.btn_guardar.configure(state="disabled", fg_color=C["borde"])
            errores = sum(1 for v in self.estados.values() if v is False)
            self.lbl_estado_global.configure(
                text=f"{errores} campo(s) con formato incorrecto.",
                text_color=C["error"],
            )
        else:
            self.btn_guardar.configure(state="disabled", fg_color=C["borde"])
            self.lbl_estado_global.configure(
                text=f"Faltan {vacios} campo(s) por completar.",
                text_color=self.colores["texto_sec"],
            )

    # ─────────────────────────────────────────────────────────
    def _guardar(self):
        C = self.colores
        datos = {cid: ent.get().strip() for cid, ent in self.entradas.items()}

        # Ventana de confirmación
        ventana = ctk.CTkToplevel(self.parent)
        ventana.title("Registro guardado")
        ventana.geometry("440x360")
        ventana.configure(fg_color=C["superficie"])
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text="Registro guardado exitosamente",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=C["exito"],
        ).pack(pady=(24, 8), padx=24)

        ctk.CTkLabel(
            ventana,
            text="Resumen del trámite registrado:",
            font=ctk.CTkFont(size=12),
            text_color=C["texto_sec"],
        ).pack(pady=(0, 12))

        for cfg in CAMPOS:
            fila = ctk.CTkFrame(ventana, fg_color=C["fondo"], corner_radius=6)
            fila.pack(fill="x", padx=24, pady=3)
            ctk.CTkLabel(
                fila,
                text=f"{cfg['icono']}  {cfg['label']}:",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=C["texto_sec"],
                width=180,
                anchor="w",
            ).pack(side="left", padx=(10, 4), pady=6)
            ctk.CTkLabel(
                fila,
                text=datos[cfg["id"]],
                font=ctk.CTkFont(size=11, family="Courier"),
                text_color=C["texto"],
                anchor="w",
            ).pack(side="left", padx=4, pady=6)

        ctk.CTkButton(
            ventana,
            text="Cerrar",
            command=ventana.destroy,
            fg_color=C["primario"],
            hover_color=C["primario_h"],
            text_color="#FFFFFF",
            width=100,
            height=36,
        ).pack(pady=(16, 24))

    # ─────────────────────────────────────────────────────────
    def _limpiar(self):
        C = self.colores
        for campo_id, entrada in self.entradas.items():
            entrada.delete(0, "end")
            entrada.configure(border_color=C["borde"])
            self.iconos_estado[campo_id].configure(text="", text_color=C["texto_sec"])
            self.estados[campo_id] = None
        self.btn_guardar.configure(state="disabled", fg_color=C["borde"])
        self.lbl_estado_global.configure(
            text="Complete todos los campos correctamente para habilitar el guardado.",
            text_color=C["texto_sec"],
        )