from motor.validadores import (
    validar_correo, validar_telefono, validar_fecha,
    validar_url, validar_placa, validar_cedula, es_digito
)

PATRONES = {
    "correo":   validar_correo,
    "telefono": validar_telefono,
    "fecha":    validar_fecha,
    "url":      validar_url,
    "placa":    validar_placa,
    "cedula":   validar_cedula,
}

# Orden de prioridad: teléfono ANTES que cédula para evitar solapamiento
ORDEN_BUSQUEDA = ["correo", "url", "fecha", "placa", "telefono", "cedula"]

LONGITUD_MINIMA = {
    "correo":   6,
    "telefono": 10,
    "fecha":    8,
    "url":      10,
    "placa":    6,
    "cedula":   6,
}


def buscar_patron(texto: str, tipo_patron: str) -> list[dict]:
    """
    Busca un patrón específico en el texto.
    Retorna lista de dicts: { "valor", "inicio", "fin" }
    """
    if tipo_patron not in PATRONES:
        raise ValueError(f"Patrón desconocido: '{tipo_patron}'.")

    validador = PATRONES[tipo_patron]
    long_min  = LONGITUD_MINIMA.get(tipo_patron, 1)
    n         = len(texto)
    resultado = []
    i         = 0

    while i < n:
        encontrado = False

        for j in range(n, i + long_min - 1, -1):
            subcadena = texto[i:j]

            if validador(subcadena):

                # Evitar detectar fragmentos dentro de números más largos
                if tipo_patron in ["cedula", "telefono"] and not es_limite_valido(texto, i, j):
                    continue

                resultado.append({
                    "valor": subcadena,
                    "inicio": i,
                    "fin": j
                })

                i = j
                encontrado = True
                break

        if not encontrado:
            i += 1

    return resultado


def buscar_todos_los_patrones(texto: str) -> dict[str, list[dict]]:
    """
    Busca todos los patrones respetando prioridad.
    Las posiciones ya capturadas por un patrón de mayor prioridad
    no pueden ser usadas por patrones de menor prioridad.
    Esto evita que un teléfono aparezca también como cédula.
    """
    n = len(texto)
    posiciones_usadas = set()  # posiciones ya asignadas a algún patrón
    resultado = {patron: [] for patron in PATRONES}

    for tipo_patron in ORDEN_BUSQUEDA:
        validador = PATRONES[tipo_patron]
        long_min  = LONGITUD_MINIMA.get(tipo_patron, 1)
        i = 0

        while i < n:
            # Saltar posiciones ya ocupadas
            if i in posiciones_usadas:
                i += 1
                continue

            encontrado = False
            for j in range(n, i + long_min - 1, -1):
                # Verificar que ninguna posición del rango esté ocupada
                rango = set(range(i, j))
                if rango & posiciones_usadas:
                    continue

                subcadena = texto[i:j]
                if validador(subcadena):
                    resultado[tipo_patron].append({
                        "valor":  subcadena,
                        "inicio": i,
                        "fin":    j,
                    })
                    posiciones_usadas |= rango
                    i = j
                    encontrado = True
                    break

            if not encontrado:
                i += 1

    return resultado

def es_limite_valido(texto: str, inicio: int, fin: int) -> bool:
    """
    Evita detectar subcadenas dentro de secuencias numéricas más largas.
    Ejemplo:
    No permite que '310672056' salga dentro de '3106720569'
    """
    # Antes
    if inicio > 0 and es_digito(texto[inicio - 1]):
        return False

    # Después
    if fin < len(texto) and es_digito(texto[fin]):
        return False

    return True