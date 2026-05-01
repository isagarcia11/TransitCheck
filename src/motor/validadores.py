from motor.auxiliares import (
    es_letra, es_digito, es_alfanumerico,
    es_mayuscula, es_minuscula,
    es_separador_fecha, es_caracter_url,
    es_caracter_usuario_correo, es_caracter_dominio
)


def validar_correo(s: str) -> bool:
    n = len(s)
    i = 0

    # --- Parte usuario (al menos 1 carácter válido, no puede empezar en punto) ---
    if i >= n or s[i] == '.' or not es_caracter_usuario_correo(s[i]):
        return False
    while i < n and es_caracter_usuario_correo(s[i]):
        i += 1

    # El usuario no puede terminar en punto
    if s[i - 1] == '.':
        return False

    # --- Arroba obligatoria ---
    if i >= n or s[i] != '@':
        return False
    i += 1

    # --- Parte dominio (al menos 1 carácter) ---
    if i >= n or not es_caracter_dominio(s[i]):
        return False
    while i < n and es_caracter_dominio(s[i]):
        i += 1

    # --- Al menos un punto + extensión (puede repetirse para .edu.co) ---
    extensiones = 0
    while i < n and s[i] == '.':
        i += 1  # consumir el punto
        inicio_ext = i
        while i < n and es_letra(s[i]):
            i += 1
        longitud_ext = i - inicio_ext
        if longitud_ext < 2 or longitud_ext > 6:
            return False
        extensiones += 1

    if extensiones == 0:
        return False

    # Debe haber consumido toda la cadena
    return i == n



def validar_telefono(s: str) -> bool:
    i = 0
    n = len(s)

    # Prefijo opcional +57 o 57
    if i < n and s[i] == '+':
        i += 1
    if i + 1 < n and s[i] == '5' and s[i + 1] == '7':
        i += 2
        # Separador opcional tras el prefijo
        if i < n and (s[i] == ' ' or s[i] == '-'):
            i += 1

    # El primer dígito DEBE ser '3'
    if i >= n or s[i] != '3':
        return False

    # Recolectar exactamente 10 dígitos ignorando separadores opcionales
    # El último carácter DEBE ser un dígito (no separador)
    digitos = 0
    while i < n:
        if es_digito(s[i]):
            digitos += 1
            i += 1
        elif (s[i] == ' ' or s[i] == '-') and i + 1 < n:
            # Separador solo válido si hay más caracteres después
            i += 1
        else:
            return False

    return digitos == 10


def _dos_digitos(s: str, i: int) -> tuple[int, int]:
    """Lee 2 dígitos desde la posición i. Retorna (valor, nueva_posición) o (-1, i) si falla."""
    if i + 1 < len(s) and es_digito(s[i]) and es_digito(s[i + 1]):
        return int(s[i:i + 2]), i + 2
    return -1, i

def _cuatro_digitos(s: str, i: int) -> tuple[int, int]:
    """Lee 4 dígitos desde la posición i."""
    if i + 3 < len(s) and all(es_digito(s[i + k]) for k in range(4)):
        return int(s[i:i + 4]), i + 4
    return -1, i

def validar_fecha(s: str) -> bool:
    n = len(s)
    i = 0

    # Detectar formato AAAA/MM/DD vs DD/MM/AAAA
    # Si los primeros 4 caracteres son dígitos y el 5to es separador → formato AAAA
    if n >= 5 and all(es_digito(s[k]) for k in range(4)) and es_separador_fecha(s[4]):
        # Formato AAAA/MM/DD
        año, i = _cuatro_digitos(s, 0)
        if año < 1000 or año > 9999:
            return False
        sep = s[i]
        if not es_separador_fecha(sep):
            return False
        i += 1
        mes, i = _dos_digitos(s, i)
        if mes < 1 or mes > 12:
            return False
        if i >= n or s[i] != sep:
            return False
        i += 1
        dia, i = _dos_digitos(s, i)
        if dia < 1 or dia > 31:
            return False
    else:
        # Formato DD/MM/AAAA o DD-MM-AAAA
        dia, i = _dos_digitos(s, 0)
        if dia < 1 or dia > 31:
            return False
        if i >= n or not es_separador_fecha(s[i]):
            return False
        sep = s[i]
        i += 1
        mes, i = _dos_digitos(s, i)
        if mes < 1 or mes > 12:
            return False
        if i >= n or s[i] != sep:
            return False
        i += 1
        año, i = _cuatro_digitos(s, i)
        if año < 1000 or año > 9999:
            return False

    return i == n


# ─────────────────────────────────────────────
#  4. URL
#     http:// o https:// + dominio.ext + ruta opcional
# ─────────────────────────────────────────────
def validar_url(s: str) -> bool:
    i = 0
    n = len(s)

    # Protocolo: http o https
    if s[i:i + 5] == 'https':
        i += 5
    elif s[i:i + 4] == 'http':
        i += 4
    else:
        return False

    # ://
    if s[i:i + 3] != '://':
        return False
    i += 3

    # www. opcional
    if s[i:i + 4] == 'www.':
        i += 4

    # Host completo: segmentos separados por puntos (sub.dominio.ext)
    # Debe tener al menos un punto y la última parte (TLD) entre 2-6 letras
    if i >= n or not es_caracter_dominio(s[i]):
        return False

    # Leer todos los segmentos del host hasta que aparezca / ? # o fin
    segmentos = []
    inicio_seg = i
    while i < n and s[i] not in ('/', '?', '#'):
        if s[i] == '.':
            segmentos.append(s[inicio_seg:i])
            i += 1
            inicio_seg = i
        elif es_caracter_dominio(s[i]):
            i += 1
        else:
            return False
    segmentos.append(s[inicio_seg:i])  # último segmento (TLD)

    # Validar: mínimo 2 segmentos (dominio + TLD), TLD entre 2-6 letras
    if len(segmentos) < 2:
        return False
    tld = segmentos[-1]
    if len(tld) < 2 or len(tld) > 6 or not all(es_letra(c) for c in tld):
        return False
    # Ningún segmento puede estar vacío
    if any(len(seg) == 0 for seg in segmentos):
        return False

    # Ruta opcional: / seguido de caracteres válidos (incluye /ruta/extra)
    if i < n and s[i] == '/':
        i += 1
        while i < n and es_caracter_url(s[i]):
            i += 1

    # La URL no puede terminar en punto (sería puntuación de oración, no parte de la URL)
    if i > 0 and s[i - 1] == '.':
        return False

    return i == n



def validar_placa(s: str) -> bool:
    if len(s) != 6:
        return False

    # Primeras 3: mayúsculas
    if not all(es_mayuscula(s[k]) for k in range(3)):
        return False

    # Carro: posiciones 3,4,5 son dígitos
    if all(es_digito(s[k]) for k in range(3, 6)):
        return True

    # Moto: posiciones 3,4 son dígitos y posición 5 es mayúscula
    if es_digito(s[3]) and es_digito(s[4]) and es_mayuscula(s[5]):
        return True

    return False


def validar_cedula(s: str) -> bool:
    # Permitir puntos como separadores visuales
    cedula = ""

    for c in s:
        # Ignorar puntos (ej: 1.234.567)
        if c == ".":
            continue

        # Si aparece cualquier carácter distinto a dígito o punto → inválido
        if not es_digito(c):
            return False

        cedula += c

    n = len(cedula)

    # Longitud entre 6 y 10 dígitos reales
    if n < 6 or n > 10:
        return False

    # No puede iniciar en 0
    if cedula[0] == '0':
        return False

    # Regla contextual:
    # Si tiene 10 dígitos y empieza en 3, probablemente es celular colombiano
    # (evita que 3201234567 se detecte como cédula)
    if n == 10 and cedula[0] == '3':
        return False

    return True

def validar_nombre(s: str) -> bool:
    """
    Valida nombres:
    - mínimo 3 caracteres
    - solo letras y espacios
    """
    nombre = s.strip()

    # Longitud mínima real
    if len(nombre) < 3:
        return False

    for c in nombre:
        if not (es_letra(c) or c == " "):
            return False

    return True