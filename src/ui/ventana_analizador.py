import customtkinter as ctk # type: ignore
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from motor.buscador import buscar_patron, buscar_todos_los_patrones, PATRONES

# Etiquetas amigables para cada patrón
ETIQUETAS = {
    "correo":   "Correo electrónico",
    "telefono": "Número telefónico",
    "fecha":    "Fecha",
    "url":      "URL",
    "placa":    "Placa vehicular",
    "cedula":   "Cédula de ciudadanía",
}

TEXTO_EJEMPLO = (
    "Estimado funcionario,\n\n"
    "Le informamos que el vehículo con placa ABC123 realizó una infracción el 25/04/2025. "
    "El propietario, con cédula 1094823456, puede ser contactado al 3201234567 o al "
    "correo juan.perez@gmail.com. También puede consultar el trámite en "
    "https://www.transitcolombia.gov.co/tramites. "
    "Otro contacto: soporte_01@transito.edu.co — moto XYZ45K, cédula 987654, "
    "tel +57 311 456 7890, fecha 2024-12-31."
)


class TabAnalizador:

    def __init__(self, parent: ctk.CTkFrame, colores: dict):
        self.colores = colores
        self.parent  = parent
        parent.configure(fg_color=colores["fondo"])

        self._construir_layout()

    # ─────────────────────────────────────────────────────────
    def _construir_layout(self):
        C = self.colores

        # ── Columna izquierda: entrada ────────────────────────
        col_izq = ctk.CTkFrame(self.parent, fg_color="transparent")
        col_izq.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # Título sección
        ctk.CTkLabel(
            col_izq,
            text="Texto a analizar",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=C["texto"],
            anchor="w",
        ).pack(fill="x", pady=(4, 4))

        # Selector de patrón
        fila_selector = ctk.CTkFrame(col_izq, fg_color="transparent")
        fila_selector.pack(fill="x", pady=(0, 6))

        ctk.CTkLabel(
            fila_selector,
            text="Buscar patrón:",
            font=ctk.CTkFont(size=12),
            text_color=C["texto_sec"],
        ).pack(side="left", padx=(0, 8))

        self.var_patron = ctk.StringVar(value="Todos los patrones")
        opciones = ["Todos los patrones"] + [ETIQUETAS[k] for k in PATRONES]
        self.combo_patron = ctk.CTkOptionMenu(
            fila_selector,
            values=opciones,
            variable=self.var_patron,
            fg_color=C["superficie"],
            button_color=C["primario"],
            button_hover_color=C["primario_h"],
            dropdown_fg_color=C["superficie"],
            text_color=C["texto"],
            font=ctk.CTkFont(size=12),
            width=220,
        )
        self.combo_patron.pack(side="left")

        # Área de texto
        self.txt_entrada = ctk.CTkTextbox(
            col_izq,
            font=ctk.CTkFont(size=12, family="Courier"),
            fg_color=C["superficie"],
            border_color=C["borde"],
            border_width=1,
            text_color=C["texto"],
            wrap="word",
        )
        self.txt_entrada.pack(fill="both", expand=True, pady=(0, 6))
        self.txt_entrada.insert("1.0", TEXTO_EJEMPLO)

        # Botones
        fila_botones = ctk.CTkFrame(col_izq, fg_color="transparent")
        fila_botones.pack(fill="x")

        ctk.CTkButton(
            fila_botones,
            text="🔍  Analizar texto",
            command=self._analizar,
            fg_color=C["primario"],
            hover_color=C["primario_h"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            fila_botones,
            text="Limpiar",
            command=self._limpiar,
            fg_color=C["borde"],
            hover_color="#D1D5DB",
            text_color=C["texto"],
            font=ctk.CTkFont(size=12),
            height=38,
            width=90,
        ).pack(side="left")

        ctk.CTkButton(
            fila_botones,
            text="Ejemplo",
            command=self._cargar_ejemplo,
            fg_color=C["acento"],
            hover_color="#DBEAFE",
            text_color=C["primario"],
            font=ctk.CTkFont(size=12),
            height=38,
            width=90,
        ).pack(side="right")

        # ── Columna derecha: resultados ───────────────────────
        col_der = ctk.CTkFrame(self.parent, fg_color="transparent")
        col_der.pack(side="left", fill="both", expand=True, padx=(8, 0))

        ctk.CTkLabel(
            col_der,
            text="Resultados",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=C["texto"],
            anchor="w",
        ).pack(fill="x", pady=(4, 4))

        # Contador de resultados
        self.lbl_conteo = ctk.CTkLabel(
            col_der,
            text="Sin analizar aún",
            font=ctk.CTkFont(size=12),
            text_color=C["texto_sec"],
            anchor="w",
        )
        self.lbl_conteo.pack(fill="x", pady=(0, 6))

        # Panel scrollable de resultados
        self.frame_resultados = ctk.CTkScrollableFrame(
            col_der,
            fg_color=C["superficie"],
            border_color=C["borde"],
            border_width=1,
            scrollbar_button_color=C["borde"],
        )
        self.frame_resultados.pack(fill="both", expand=True)

        # Mensaje inicial
        self._mostrar_placeholder()

    # ─────────────────────────────────────────────────────────
    def _analizar(self):
        texto = self.txt_entrada.get("1.0", "end").strip()
        if not texto:
            return

        seleccion = self.var_patron.get()

        # Determinar qué patrones buscar
        if seleccion == "Todos los patrones":
            resultados = buscar_todos_los_patrones(texto)
        else:
            # Buscar la clave interna a partir de la etiqueta
            clave = next(k for k, v in ETIQUETAS.items() if v == seleccion)
            resultados = {clave: buscar_patron(texto, clave)}

        self._mostrar_resultados(resultados)

    # ─────────────────────────────────────────────────────────
    def _mostrar_resultados(self, resultados: dict):
        C = self.colores

        # Limpiar panel
        for w in self.frame_resultados.winfo_children():
            w.destroy()

        total = sum(len(v) for v in resultados.values())
        encontrados = {k: v for k, v in resultados.items() if v}

        if total == 0:
            self.lbl_conteo.configure(text="No se encontraron coincidencias")
            ctk.CTkLabel(
                self.frame_resultados,
                text="Sin resultados para el texto ingresado.",
                text_color=C["texto_sec"],
                font=ctk.CTkFont(size=12),
            ).pack(pady=30)
            return

        self.lbl_conteo.configure(
            text=f"{total} coincidencia{'s' if total != 1 else ''} en {len(encontrados)} patrón/es"
        )

        for clave, coincidencias in resultados.items():
            if not coincidencias:
                continue

            # Encabezado del grupo
            encabezado = ctk.CTkFrame(
                self.frame_resultados,
                fg_color=C["acento"],
                corner_radius=8,
            )
            encabezado.pack(fill="x", pady=(6, 2), padx=4)

            ctk.CTkLabel(
                encabezado,
                text=f"{ETIQUETAS[clave]}   ({len(coincidencias)})",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=C["primario"],
                anchor="w",
            ).pack(fill="x", padx=10, pady=6)

            # Tarjetas individuales
            for item in coincidencias:
                tarjeta = ctk.CTkFrame(
                    self.frame_resultados,
                    fg_color=C["superficie"],
                    border_color=C["borde"],
                    border_width=1,
                    corner_radius=6,
                )
                tarjeta.pack(fill="x", padx=4, pady=2)

                ctk.CTkLabel(
                    tarjeta,
                    text=item["valor"],
                    font=ctk.CTkFont(size=12, family="Courier"),
                    text_color=C["texto"],
                    anchor="w",
                ).pack(side="left", padx=10, pady=6)

                ctk.CTkLabel(
                    tarjeta,
                    text=f"pos. {item['inicio']}–{item['fin']}",
                    font=ctk.CTkFont(size=11),
                    text_color=C["texto_sec"],
                    anchor="e",
                ).pack(side="right", padx=10)

    # ─────────────────────────────────────────────────────────
    def _mostrar_placeholder(self):
        C = self.colores
        ctk.CTkLabel(
            self.frame_resultados,
            text="Escribe o pega un texto y presiona\n\"Analizar texto\" para ver los resultados.",
            text_color=C["texto_sec"],
            font=ctk.CTkFont(size=12),
            justify="center",
        ).pack(expand=True, pady=40)

    def _limpiar(self):
        self.txt_entrada.delete("1.0", "end")
        for w in self.frame_resultados.winfo_children():
            w.destroy()
        self._mostrar_placeholder()
        self.lbl_conteo.configure(text="Sin analizar aún")

    def _cargar_ejemplo(self):
        self.txt_entrada.delete("1.0", "end")
        self.txt_entrada.insert("1.0", TEXTO_EJEMPLO)