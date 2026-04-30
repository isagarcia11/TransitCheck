import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from motor.validadores import (
    validar_correo, validar_telefono, validar_fecha,
    validar_url, validar_placa, validar_cedula,
)

# ── Casos de prueba ──────────────────────────────────────────
CASOS = {
    "correo": {
        "validos": [
            "juan.perez@gmail.com",
            "estudiante_01@uni.edu.co",
            "soporte_01@transito.edu.co",
            "user.name-ok@dominio.org",
            "a@b.co",
        ],
        "invalidos": [
            "juan@",
            "@gmail.com",
            "juan@.com",
            "sinArroba.com",
            "doble@@correo.com",
            ".inicio@correo.com",
            "correo@dominio.c",
        ],
    },
    "telefono": {
        "validos": [
            "3201234567",
            "+57 320 123 4567",
            "57-311-456-7890",
            "+57 300 000 0000",
            "3109876543",
        ],
        "invalidos": [
            "123456",
            "4201234567",
            "320123456",
            "+58 320 123 4567",
            "32012345678",
        ],
    },
    "fecha": {
        "validos": [
            "01/01/2000",
            "25/04/2025",
            "25-04-2025",
            "2024/12/31",
            "2025-01-15",
        ],
        "invalidos": [
            "32/13/2020",
            "01-2020",
            "00/05/2021",
            "15/00/2021",
            "2025/13/01",
        ],
    },
    "url": {
        "validos": [
            "https://www.google.com",
            "http://mi-sitio.edu.co/pagina",
            "https://transito.gov.co",
            "http://sub.dominio.org/ruta/extra",
            "https://www.transitocolombia.gov.co/tramites",
        ],
        "invalidos": [
            "www.google.com",
            "ftp://algo.com",
            "https://.com",
            "http://nodot",
        ],
    },
    "placa": {
        "validos": [
            "ABC123",
            "XYZ45K",
            "ZZZ999",
            "AAA00A",
        ],
        "invalidos": [
            "AB1234",
            "1BC123",
            "ABCD12",
            "ABC12",
            "abc123",
        ],
    },
    "cedula": {
        "validos": [
            "1234567890",
            "987654",
            "100000",
            "9999999999",
        ],
        "invalidos": [
            "0123456",
            "12345",
            "12345678901",
            "12A456",
            "000000",
        ],
    },
}

FUNCIONES = {
    "correo":   validar_correo,
    "telefono": validar_telefono,
    "fecha":    validar_fecha,
    "url":      validar_url,
    "placa":    validar_placa,
    "cedula":   validar_cedula,
}

NOMBRES = {
    "correo":   "Correo electrónico",
    "telefono": "Número telefónico",
    "fecha":    "Fecha",
    "url":      "URL",
    "placa":    "Placa vehicular",
    "cedula":   "Cédula de ciudadanía",
}


def correr_pruebas():
    total = 0
    aprobados = 0
    fallidos = []

    for patron, grupos in CASOS.items():
        fn = FUNCIONES[patron]
        nombre = NOMBRES[patron]

        print(f"\n{'─'*55}")
        print(f"  {nombre}")
        print(f"{'─'*55}")

        # Casos válidos
        print("  Casos válidos:")
        for valor in grupos["validos"]:
            total += 1
            resultado = fn(valor)
            if resultado:
                aprobados += 1
                print(f"  {valor}")
            else:
                fallidos.append((nombre, valor, "Válido", "Inválido"))
                print(f"   {valor}  ← debería ser VÁLIDO")

        # Casos inválidos
        print("  Casos inválidos:")
        for valor in grupos["invalidos"]:
            total += 1
            resultado = fn(valor)
            if not resultado:
                aprobados += 1
                print(f"   {valor}")
            else:
                fallidos.append((nombre, valor, "Inválido", "Válido"))
                print(f"   {valor}  ← debería ser INVÁLIDO")

    # ── Resumen final ────────────────────────────────────────
    print(f"\n{'═'*55}")
    print(f"  RESUMEN: {aprobados}/{total} pruebas aprobadas")
    if fallidos:
        print(f"  FALLIDOS ({len(fallidos)}):")
        for nombre, valor, esperado, obtenido in fallidos:
            print(f"    • [{nombre}] {valor!r} → esperado: {esperado}, obtenido: {obtenido}")
    else:
        print("  Todas las pruebas pasaron correctamente  ") 
    print(f"{'═'*55}\n")

    return len(fallidos) == 0


if __name__ == "__main__":
    exito = correr_pruebas()
    sys.exit(0 if exito else 1)