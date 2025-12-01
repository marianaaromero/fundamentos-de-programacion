"""
Módulo para la lógica de las operaciones
"""

import constantes
import presentacion
import validaciones
import negocio


def _obtener_lista_rutas(rutas_texto: str):
    """
    Convierte la cadena ingresada por el usuario (con rutas separadas por espacio)
    en una lista de rutas válidas.

    Pre:
    - `rutas_texto` es un string con rutas separadas por espacio.
    Post:
    - Devuelve una lista con rutas válidas o una lista vacía si hay error.
    """
    rutas = rutas_texto.split(" ")
    rutas_validas = []

    for ruta in rutas:
        if validaciones.tiene_formato_ruta_valida(ruta):
            rutas_validas.append(ruta)
        else:
            return []

    return rutas_validas


def cargar_csv_generico(agencia: dict, tipo: str, procesar_funcion, mensajes: dict):
    """
    Función genérica para cargar datos (películas o ventas) desde archivos CSV.

    Parámetros:
    - agencia (dict): Estructura principal de la agencia.
    - tipo (str): Tipo de dato a cargar ('peliculas' o 'ventas').
    - procesar_funcion (func): Función encargada de procesar los datos.
    - mensajes (dict): Diccionario con los textos personalizados para mensajes.
        Ejemplo:
        {
            "error": constantes.ERROR_IMPORTACION,
            "ok": constantes.MSG_OK,
            "aviso": constantes.PELICULA_DUPLICADA,
        }

    Post:
    - Solicita rutas de archivos CSV al usuario.
    - Procesa los datos usando `procesar_funcion`.
    - Muestra los mensajes correspondientes según el resultado.
    """
    while True:
        rutas_texto = presentacion.solicitar_rutas_para_carga(tipo)
        if rutas_texto == constantes.COMANDO_RETROCEDER:
            return

        rutas = _obtener_lista_rutas(rutas_texto)
        if not rutas:
            print(mensajes["error"])
            continue

        cantidad, nombres_aviso = procesar_funcion(rutas, agencia)
        if cantidad == -1:
            print(mensajes["error"])
            continue

        for nombre in nombres_aviso:
            print(mensajes["aviso"].format(nombre))

        print(f"{mensajes['ok']} {cantidad}")
        return


def cargar_peliculas(agencia: dict):
    """
    Permite cargar películas desde archivos CSV.

    Pre:
    - `agencia` es el diccionario de la agencia.
    Post:
    - Llama a `negocio.procesar_carga_peliculas` para actualizar el dict.
    - Muestra en pantalla la cantidad de películas cargadas o mensajes de error.
    """
    mensajes = {
        "error": constantes.ERROR_IMPORTACION,
        "ok": constantes.MSG_OK,
        "aviso": constantes.PELICULA_DUPLICADA,
    }

    cargar_csv_generico(
        agencia=agencia,
        tipo="peliculas",
        procesar_funcion=negocio.procesar_carga_peliculas,
        mensajes=mensajes,
    )


def cargar_ventas(agencia: dict):
    """
    Permite cargar ventas desde archivos CSV.

    Pre:
    - `agencia` es el diccionario de la agencia.
    Post:
    - Llama a `negocio.procesar_carga_ventas` para actualizar `agencia["ventas"]`.
    - Muestra en pantalla la cantidad de ventas cargadas o mensajes de error.
    """
    mensajes = {
        "error": constantes.ERROR_IMPORTACION,
        "ok": constantes.MSG_OK,
        "aviso": constantes.PELICULA_INEXISTENTE,
    }

    cargar_csv_generico(
        agencia=agencia,
        tipo="ventas",
        procesar_funcion=negocio.procesar_carga_ventas,
        mensajes=mensajes,
    )


def listar_colaboraciones_directas(agencia: dict):
    """
    Lista los colaboradores directos de un talento.

    Pre:
    - `agencia` es el diccionario de la agencia.
    Post:
    - Muestra la lista de colaboradores directos, un msj si no existen
     o error si no encuentra el talento pedido.
    """
    while True:
        nombre = presentacion.pedir_nombre_talento_validado()

        if nombre is None:
            return

        colaboradores_directos = negocio.obtener_colaboradores_directos(nombre, agencia)
        if colaboradores_directos is None:
            print(constantes.ERROR_TALENTO_NO_ENCONTRADO)
            continue

        colaboradores = colaboradores_directos
        if not colaboradores:
            print(constantes.COLABORADORES_DIRECTOS_INEXISTENTES)
            return

        presentacion.mostrar_lista(constantes.COLABORADORES_DIRECTOS, colaboradores)
        return


def listar_compatibles(agencia: dict):
    """
    Lista los talentos compatibles con un talento dado.

    Pre:
    - `agencia` es el diccionario de la agencia.
    Post:
    - Muestra la lista de talentos compatibles, un mensaje si no existen
     o error si no encuentra el talento pedido.
    """
    while True:
        nombre = presentacion.pedir_nombre_talento_validado()

        if nombre is None:
            return

        compatibles = negocio.obtener_talentos_compatibles(nombre, agencia)
        if compatibles is None:
            print(constantes.ERROR_TALENTO_NO_ENCONTRADO)
            continue

        if not compatibles:
            print(constantes.TALENTOS_COMPATIBLES_INEXISTENTES)
            return

        presentacion.mostrar_lista(constantes.TALENTOS_COMPATIBLES, compatibles)
        return


def listar_incompatibles(agencia: dict):
    """
    Lista los talentos incompatibles con un talento dado.

    Pre:
    - `agencia` es el diccionario de la agencia.
    Post:
    - Muestra la lista de talentos incompatibles, un mensaje si no existen
     o error si no encuentra el talento pedido.
    """
    while True:
        nombre = presentacion.pedir_nombre_talento_validado()
        if nombre is None:
            return

        talentos_incompatibles = negocio.obtener_talentos_incompatibles(nombre, agencia)
        if talentos_incompatibles is None:
            print(constantes.ERROR_TALENTO_NO_ENCONTRADO)
            continue

        incompatibles = talentos_incompatibles
        if not incompatibles:
            print(constantes.TALENTOS_INCOMPATIBLES_INEXISTENTES)
            return

        presentacion.mostrar_lista(constantes.TALENTOS_INCOMPATIBLES, incompatibles)
        return


def exportar_recaudacion(agencia: dict):
    """
    Exporta la recaudación total de las películas a un archivo CSV.

    Pre:
    - `agencia` es el diccionario de la agencia.
    - El usuario ingresa una ruta de destino válida o el comando de retroceso.
    Post:
    - Llama a `negocio.exportar_recaudacion_a_csv` para generar el archivo.
    - Muestra un mensaje de éxito o error según el resultado.
    """
    while True:
        ruta = presentacion.solicitar_ruta_exportacion()
        if ruta == constantes.COMANDO_RETROCEDER:
            return

        ok = negocio.exportar_recaudacion_a_csv(ruta, agencia)
        if ok:
            print(constantes.MSG_OK)
            return

        print(constantes.ERROR_EXPORTACION)
        continue
