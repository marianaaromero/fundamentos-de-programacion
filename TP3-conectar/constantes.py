"""
Módulo para las constantes.
"""

COMANDO_RETROCEDER = "**"

MENU_PRINCIPAL = (
    "1) Cargar películas\n"
    "2) Cargar información de ventas\n"
    "3) Listar colaboraciones directas\n"
    "4) Listar talentos compatibles\n"
    "5) Listar talentos incompatibles\n"
    "6) Exportar talentos con mayor recaudación\n"
    "7) Salir\n"
    ">>> "
)


OPCION_CARGAR_PELICULAS = 1
OPCION_CARGAR_VENTAS = 2
OPCION_LISTAR_COLAB_DIRECTAS = 3
OPCION_LISTAR_TALENTOS_COMP = 4
OPCION_LISTAR_TALENTOS_INCOMP = 5
OPCION_EXPORTAR_TALENTOS_MAYOR_REC = 6
OPCION_SALIR = 7

OPCION_INVALIDA = "Seleccione una opción válida"
ERROR_IMPORTACION = "El/los archivos a importar deben existir y ser CSV válidos"
MSG_OK = "OK"
ERROR_EXPORTACION = "Error en la exportación"
ERROR_TALENTO_NO_ENCONTRADO = "Talento no existente"
ERROR_NOMBRE_TALENTO_INVALIDO = (
    "El nombre ingresado no debe estar vacío y debe "
    "estar compuesto por caracteres alfabéticos"
)

PELICULA_DUPLICADA = "Ignorando película duplicada: {}"
PELICULA_INEXISTENTE = "Ignorando película inexistente: {}"

COLABORADORES_DIRECTOS = "Colaboradores directos:"
COLABORADORES_DIRECTOS_INEXISTENTES = (
    "No existen colaboradores directos para el talento ingresado"
)

TALENTOS_COMPATIBLES = "Talentos compatibles:"
TALENTOS_COMPATIBLES_INEXISTENTES = (
    "No existen talentos compatibles para el talento ingresado"
)

TALENTOS_INCOMPATIBLES = "Talentos incompatibles:"
TALENTOS_INCOMPATIBLES_INEXISTENTES = (
    "No existen talentos incompatibles para el talento ingresado"
)

EXPORT_HEADER = "actor,recaudacion"

INDICE_ENCABEZADO = 1
CANTIDAD_MINIMA_PARTES = 3  # película, precio, talentos_involucrados
INDICE_NOMBRE = 0
INDICE_PRECIO = 1
INDICE_TALENTOS = 2

CANTIDAD_MINIMA_PARTES_VENTA = 2  # pelicula, entradas_vendidas
INDICE_NOMBRE_VENTA = 0
INDICE_ENTRADAS_VENTA = 1
