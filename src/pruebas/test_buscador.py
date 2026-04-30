import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from motor.buscador import buscar_patron, buscar_todos_los_patrones

# ── Textos de prueba ─────────────────────────────────────────
TEXTO_TRANSITO = (
    "Estimado funcionario, le informamos que el vehículo con placa ABC123 "
    "realizó una infracción el 25/04/2025. El propietario, con cédula 1094823456, "
    "puede ser contactado al 3201234567 o al correo juan.perez@gmail.com. "
    "También puede consultar el trámite en https://www.transito.gov.co/tramites. "
    "Moto XYZ45K, cédula 987654, tel +57 311 456 7890, fecha 2024-12-31, "
    "correo soporte_01@transito.edu.co."
)

TEXTO_VACIO = ""

TEXTO_SIN_PATRONES = (
    "El día fue soleado y el funcionario atendió 15 personas en la oficina principal. "
    "Todo estuvo en orden y no hubo inconvenientes durante la jornada laboral."
)

# ── Casos del buscador ───────────────────────────────────────
CASOS_BUSCADOR = [
    {
        "descripcion": "Texto de tránsito — buscar correos",
        "texto": TEXTO_TRANSITO,
        "patron": "correo",
        "valores_esperados": ["juan.perez@gmail.com", "soporte_01@transito.edu.co"],
    },
    {
        "descripcion": "Texto de tránsito — buscar teléfonos",
        "texto": TEXTO_TRANSITO,
        "patron": "telefono",
        "valores_esperados": ["3201234567", "+57 311 456 7890"],
    },
    {
        "descripcion": "Texto de tránsito — buscar fechas",
        "texto": TEXTO_TRANSITO,
        "patron": "fecha",
        "valores_esperados": ["25/04/2025", "2024-12-31"],
    },
    {
        "descripcion": "Texto de tránsito — buscar placas",
        "texto": TEXTO_TRANSITO,
        "patron": "placa",
        "valores_esperados": ["ABC123", "XYZ45K"],
    },
    {
        "descripcion": "Texto de tránsito — buscar cédulas",
        "texto": TEXTO_TRANSITO,
        "patron": "cedula",
        "valores_esperados": ["1094823456", "3201234567", "987654"],
        # Nota: 3201234567 también es cédula válida (10 dígitos); el contexto
        # semántico (prefijo "cel") no lo puede distinguir el motor sintáctico.
    },
    {
        "descripcion": "Texto de tránsito — buscar URLs",
        "texto": TEXTO_TRANSITO,
        "patron": "url",
        "valores_esperados": ["https://www.transito.gov.co/tramites"],
    },
    {
        "descripcion": "Texto vacío — sin resultados",
        "texto": TEXTO_VACIO,
        "patron": "correo",
        "valores_esperados": [],
    },
    {
        "descripcion": "Texto sin patrones — sin resultados",
        "texto": TEXTO_SIN_PATRONES,
        "patron": "placa",
        "valores_esperados": [],
    },
]


def correr_pruebas_buscador():
    total = 0
    aprobados = 0
    fallidos = []

    print(f"\n{'═'*60}")
    print("  TEST BUSCADOR — Motor de búsqueda en texto libre")
    print(f"{'═'*60}")

    for caso in CASOS_BUSCADOR:
        total += 1
        print(f"\n  [{total}] {caso['descripcion']}")

        resultados = buscar_patron(caso["texto"], caso["patron"])
        valores_obtenidos = [r["valor"] for r in resultados]

        # Comparar conjuntos (orden puede variar)
        esperados = set(caso["valores_esperados"])
        obtenidos = set(valores_obtenidos)

        if esperados == obtenidos:
            aprobados += 1
            print(f"    Encontrados: {valores_obtenidos if valores_obtenidos else '(ninguno)'}")
        else:
            fallidos.append(caso["descripcion"])
            print(f"          Esperados : {caso['valores_esperados']}")
            print(f"          Obtenidos : {valores_obtenidos}")

    # ── Prueba: buscar todos los patrones ────────────────────
    total += 1
    print(f"\n  [{total}] Buscar todos los patrones en texto de tránsito")
    todos = buscar_todos_los_patrones(TEXTO_TRANSITO)
    tiene_resultados = any(len(v) > 0 for v in todos.values())
    if tiene_resultados:
        aprobados += 1
        print("       Resultados por patrón:")
        for patron, coincidencias in todos.items():
            if coincidencias:
                print(f"          {patron:10}: {[r['valor'] for r in coincidencias]}")
    else:
        fallidos.append("Buscar todos los patrones")
        print("       No se encontró ningún patrón")

    # ── Resumen ──────────────────────────────────────────────
    print(f"\n{'═'*60}")
    print(f"  RESUMEN: {aprobados}/{total} pruebas aprobadas")
    if fallidos:
        print(f"  FALLIDOS ({len(fallidos)}):")
        for f in fallidos:
            print(f"    • {f}")
    else:
        print("  Todas las pruebas pasaron correctamente ")
    print(f"{'═'*60}\n")

    return len(fallidos) == 0


if __name__ == "__main__":
    exito = correr_pruebas_buscador()
    sys.exit(0 if exito else 1)