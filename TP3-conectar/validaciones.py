"""
Módulo de validaciones.
"""

import os


def tiene_espacios(texto: str) -> bool:
    """
    Verifica si un texto contiene espacios.

    Pre:
    - `texto` es un string que contiene cualquier caracter o está vacío.
    Post:
    - Devuelve True si `texto` contiene al menos un espacio o False
    en caso contrario.
    """
    for caracter in texto:
        if caracter == " ":
            return True
    return False


def tiene_formato_ruta_valida(ruta: str) -> bool:
    """
    Verifica si una ruta de archivo o directorio es válida.

    Pre:
    - `ruta` es un string con una posible ruta del sistema.
    Post:
    - Devuelve True si:
        - No contiene espacios.
        - Existe en el sistema.
        - Es un directorio o un archivo con extensión `.csv`.
    - Devuelve False si no cumple alguna de las condiciones anteriores.
    """

    if tiene_espacios(ruta):
        return False

    if not os.path.exists(ruta):
        return False

    if ruta.lower().endswith(".csv"):
        return True

    if os.path.isdir(ruta):
        return True

    return False


def tiene_formato_nombre_valido(nombre: str) -> bool:
    """
    Verifica si un nombre de talento tiene un formato válido.

    Pre:
    - `nombre` es un string (puede tener espacios y letras).
    Post:
    - Devuelve True si:
        - No está vacío ni compuesto solo por espacios.
        - Contiene solo letras y espacios.
    - Devuelve False si incluye números, símbolos u otros caracteres inválidos.
    """
    if not nombre:
        return False

    nombre = nombre.strip()
    if nombre == "":
        return False

    for caracter in nombre:
        if not (caracter.isalpha() or caracter == " "):
            return False

    return True


def normalizar_nombre(nombre: str) -> str:
    """
    Normaliza un nombre: eimina mayúsculas, tildes y espacios extra.

    Pre:
    - `nombre` es un string (puede contener letras, espacios y tildes).
    Post:
    - Devuelve el nombre en minúsculas, sin tildes y sin espacios iniciales ni finales.
    - Si `nombre` está vacío, devuelve una cadena vacía.
    Ejemplo:
        " José Álvarez " -> "jose alvarez"
    """
    if not nombre:
        return ""

    nombre = nombre.strip().lower()
    acentuadas = "áàäâãéèëêíìïîóòöôõúùüû"
    sin_tilde = "aaaaaeeeeiiiiooooouuuu"
    tabla = str.maketrans(acentuadas, sin_tilde)
    return nombre.translate(tabla)
