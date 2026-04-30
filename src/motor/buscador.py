from motor.validadores import (
    validar_correo,
    validar_telefono,
    validar_fecha,
    validar_url,
    validar_placa,
    validar_cedula,
)

# Mapa de patrones disponibles
PATRONES = {
    "correo":    validar_correo,
    "telefono":  validar_telefono,
    "fecha":     validar_fecha,
    "url":       validar_url,
    "placa":     validar_placa,
    "cedula":    validar_cedula,
}

# Longitudes mínimas para cada patrón (optimiza el motor)
LONGITUD_MINIMA = {
    "correo":   6,   # a@b.co
    "telefono": 10,  # 3XXXXXXXXX
    "fecha":    8,   # D/M/AAAA mínimo no aplica, pero 8 es razonable
    "url":      10,  # http://a.co
    "placa":    6,   # ABC123
    "cedula":   6,
}


def buscar_patron(texto: str, tipo_patron: str) -> list[dict]:
    """
    Recorre `texto` carácter a carácter buscando subcadenas que el
    validador del patrón indicado acepte.
    """
    if tipo_patron not in PATRONES:
        raise ValueError(f"Patrón desconocido: '{tipo_patron}'. "
                         f"Opciones: {list(PATRONES.keys())}")

    validador  = PATRONES[tipo_patron]
    long_min   = LONGITUD_MINIMA.get(tipo_patron, 1)
    n          = len(texto)
    resultado  = []
    i          = 0

    while i < n:
        encontrado = False
        # Probar subcadenas de mayor a menor longitud
        for j in range(n, i + long_min - 1, -1):
            subcadena = texto[i:j]
            if validador(subcadena):
                resultado.append({
                    "valor":  subcadena,
                    "inicio": i,
                    "fin":    j,
                })
                i = j          # saltar al siguiente carácter tras la coincidencia
                encontrado = True
                break
        if not encontrado:
            i += 1

    return resultado


def buscar_todos_los_patrones(texto: str) -> dict[str, list[dict]]:
    """
    Ejecuta la búsqueda para todos los patrones disponibles y
    retorna un diccionario   { tipo_patron: [coincidencias] }.
    """
    return {patron: buscar_patron(texto, patron) for patron in PATRONES}