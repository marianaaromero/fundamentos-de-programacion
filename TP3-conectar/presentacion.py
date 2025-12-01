"""
Módulo para la capa de interacción con el usuario, input/output
"""

import constantes
import validaciones


def pedir_opcion_menu() -> str:
    """
    Solicita al usuario una opción del menú principal.

    Pre:
    - El menú principal está definido en `constantes.MENU_PRINCIPAL`.
    Post:
    - Devuelve la opción ingresada por el usuario como string.
    """
    return input(constantes.MENU_PRINCIPAL)


def solicitar_rutas_para_carga(tipo: str) -> str:
    """
    Solicita al usuario una o más rutas de archivos CSV según el tipo de carga.

    Pre:
    - `tipo` es un string que indica el tipo de datos a cargar:
      puede ser "peliculas" o "ventas".
    Post:
    - Devuelve una cadena con las rutas ingresadas separadas por espacio,
    o una cadena vacía si el usuario no ingresa nada.
    """
    if tipo == "peliculas":
        return input("Ingrese el archivo de películas a cargar: ")

    if tipo == "ventas":
        return input("Ingrese el archivo de ventas a cargar: ")

    return input("Ingrese la ruta: ")


def solicitar_nombre_talento() -> str:
    """
    Solicita al usuario el nombre de un talento.

    Post:
    - Devuelve el texto ingresado por el usuario como string.
    """
    return input("Ingrese el nombre de un talento: ")


def solicitar_ruta_exportacion() -> str:
    """
    Solicita al usuario la ruta del archivo de destino para exportar datos.

    Post:
    - Devuelve la ruta ingresada como string.
    """
    return input("Ingrese la ruta del archivo a guardar: ")


def pedir_nombre_talento_validado():
    """
    Solicita al usuario un nombre de talento y valida su formato.

    Pre:
        - El usuario ingresa un nombre o el comando de retroceso.
    Post:
        - Devuelve el nombre validado si es correcto.
        - Devuelve None si el usuario ingresa el comando de retroceso.
        - Muestra mensajes de error si el formato es inválido.
    """
    while True:
        nombre = solicitar_nombre_talento()
        if nombre == constantes.COMANDO_RETROCEDER:
            return None
        if not validaciones.tiene_formato_nombre_valido(nombre):
            print(constantes.ERROR_NOMBRE_TALENTO_INVALIDO)
            continue
        return nombre


def mostrar_lista(titulo: str, lista: list):
    """
    Muestra una lista numerada con un titulo. Luego utilizada para listar
    colab. directos, compatibles e incompatibles.

    Pre:
    - `titulo` es un string que describe el contenido de la lista.
    - `lista` es una lista de strings con los elementos a mostrar.
    Post:
    - Muestra por consola el titulo y los elementos numerados.
    """
    print(titulo)
    for indice, nombre in enumerate(lista, start=1):
        print(f"{indice}. {nombre}")
