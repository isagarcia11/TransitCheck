# motor/__init__.py
from motor.auxiliares import *
from motor.validadores import (
    validar_correo,
    validar_telefono,
    validar_fecha,
    validar_url,
    validar_placa,
    validar_cedula,
)
from motor.buscador import buscar_patron, buscar_todos_los_patrones, PATRONES