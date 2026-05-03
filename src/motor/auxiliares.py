def es_letra(c: str) -> bool:
    """Retorna True si el carácter es una letra (a-z / A-Z)."""
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z')

def es_digito(c: str) -> bool:
    """Retorna True si el carácter es un dígito (0-9)."""
    return '0' <= c <= '9'

def es_alfanumerico(c: str) -> bool:
    """Retorna True si el carácter es letra o dígito."""
    return es_letra(c) or es_digito(c)

def es_mayuscula(c: str) -> bool:
    """Retorna True si el carácter es una letra mayúscula (A-Z)."""
    return 'A' <= c <= 'Z'

def es_minuscula(c: str) -> bool:
    """Retorna True si el carácter es una letra minúscula (a-z)."""
    return 'a' <= c <= 'z'

def es_separador_fecha(c: str) -> bool:
    """Retorna True si el carácter es un separador válido de fecha (/ o -)."""
    return c == '/' or c == '-'

def es_caracter_url(c: str) -> bool:
    """Retorna True si el carácter es válido dentro de una URL."""
    return es_alfanumerico(c) or c in '-._~:/?#[]@!$&\'()*+,;=%'

def es_caracter_usuario_correo(c: str) -> bool:
    """Retorna True si el carácter es válido en la parte de usuario de un correo."""
    return es_alfanumerico(c) or c in '._-'

def es_caracter_dominio(c: str) -> bool:
    """Retorna True si el carácter es válido en un dominio (letras, dígitos, guion)."""
    return es_alfanumerico(c) or c == '-'

def es_letra_especial(c: str) -> bool:
    """Letras con tilde y ñ del español."""
    return c in "áéíóúüñÁÉÍÓÚÜÑ"