"""
Este módulo contiene la lógica de negocio.
"""

import os
import csv
import constantes
import validaciones


def crear_agencia() -> dict:
    """
    Crea la estructura de datos.

    Post: devuelve un diccionario con claves: 'peliculas', 'ventas',
     'talentos', 'nombres_originales'.
    """

    return {
        "peliculas": {},
        "ventas": {},
        "talentos": {},
        "nombres_originales": {},
    }


# Funciones de manejo de archivos


def leer_csv_lineas(ruta: str) -> list[str]:
    """
    Lee un archivo CSV línea por línea.

    Pre:
    - `ruta` es la ruta a un archivo CSV.
    Post:
    - Devuelve lista de líneas sin saltos de línea, o lista vacía si falla.
    """
    lineas = []
    try:
        with open(ruta, "r", encoding="utf8") as f:
            for linea in f:
                lineas.append(linea.rstrip("\n"))
    except (FileNotFoundError, IOError):
        return []

    return lineas


def _recorrer_directorio_recursivo(ruta_dir: str) -> list[str]:
    """
    Devuelve recursivamente todos los archivos CSV en un directorio.

    Pre:
    - `ruta_dir` es una ruta a directorio.
    Post:
    - Lista de rutas a archivos CSV encontrados, vacía si no hay o falla.
    """
    archivos = []

    try:
        for nombre_archivo in os.listdir(ruta_dir):
            ruta_completa = os.path.join(ruta_dir, nombre_archivo)

            if os.path.isdir(ruta_completa):
                archivos.extend(_recorrer_directorio_recursivo(ruta_completa))
                continue

            if ruta_completa.lower().endswith(".csv"):
                archivos.append(ruta_completa)

    except FileNotFoundError:
        return []

    return archivos


def listar_archivos_csv_en_ruta(ruta: str) -> list[str]:
    """
    Lista archivos CSV a partir de una ruta.

    Pre:
    - `ruta` es archivo o directorio.
    Post:
    - Devuelve lista de rutas a archivos CSV.
    """
    if os.path.exists(ruta) and not os.path.isdir(ruta):
        return [ruta]

    if os.path.isdir(ruta):
        return _recorrer_directorio_recursivo(ruta)

    return []


def obtener_csv_desde_rutas(rutas: list[str]) -> list[str]:
    """
    Devuelve una lista con todas las rutas a archivos CSV encontradas
    a partir de una lista de rutas de entrada.

    Pre:
    - `rutas` es una lista de strings, donde cada elemento puede ser
      una ruta a archivo CSV o un directorio que los contenga.

    Post:
    - Devuelve una lista con las rutas de todos los archivos CSV encontrados.
    - Si no se encuentra ningún archivo o hay errores de acceso, devuelve una lista vacía.
    """
    archivos = []
    for ruta in rutas:
        archivos.extend(listar_archivos_csv_en_ruta(ruta))
    return archivos


# Procesamiento de películas y ventas


def extraer_datos_pelicula(linea: str) -> tuple[str, int, list[str]] | None:
    """
    Extrae los datos de una línea CSV correspondiente a una película.

    Pre:
    - `linea` es una cadena con el formato: nombre,precio,talentos.
    - Las posiciones de los campos se definen en `el módulo de las constantes.

    Post:
    - Si la línea es válida, devuelve una tupla (nombre, precio, lista_talentos).
    - Si la línea es inválida o faltan datos, devuelve None.
    """
    partes = linea.split(",", constantes.CANTIDAD_MINIMA_PARTES - 1)
    if len(partes) < constantes.CANTIDAD_MINIMA_PARTES:
        return None

    try:
        nombre = partes[constantes.INDICE_NOMBRE].strip()
        precio = int(partes[constantes.INDICE_PRECIO].strip())
        talentos_texto = partes[constantes.INDICE_TALENTOS]
    except (ValueError, IndexError):
        return None

    talentos = []
    for talento in talentos_texto.split(";"):
        talento = talento.strip()
        if talento:
            talentos.append(talento)

    if not talentos:
        return None

    return nombre, precio, talentos


def procesar_linea_pelicula(linea: str, agencia: dict) -> tuple[bool, str | None]:
    """
    Procesa una línea CSV correspondiente a una película.

    Pre:
    - `linea` es una línea de texto con formato CSV: nombre,precio,talentos.
    - `agencia` es el diccionario de la agencia.
    Post:
    - Si la línea es válida, agrega la película y sus talentos a `agencia`.
    - Devuelve (True, None) si se agregó correctamente.
    - Devuelve (False, nombre) si la película estaba duplicada.
    - Devuelve (False, None) si la línea es inválida.
    """
    info_pelicula = extraer_datos_pelicula(linea)
    if info_pelicula is None:
        return False, None

    nombre, precio, talentos = info_pelicula
    if nombre in agencia["peliculas"]:
        return False, nombre

    agencia["peliculas"][nombre] = {"precio": precio, "talentos": talentos}
    registrar_talentos_y_colab(talentos, agencia)
    return True, None


def procesar_linea_venta(linea: str, agencia: dict) -> tuple[bool, str | None]:
    """
    Procesa una línea CSV correspondiente a una venta.

    Pre:
    - `linea` es una línea CSV con nombre de película y entradas vendidas.
    - `agencia` es el diccionario de la agencia.
    Post:
    - Si la película existe, suma las entradas en `agencia["ventas"]`.
    - Devuelve (True, None) si se procesó correctamente.
    - Devuelve (False, nombre) si la película no existe.
    - Devuelve (False, None) si la línea es inválida.
    """
    partes = linea.split(",", constantes.CANTIDAD_MINIMA_PARTES_VENTA - 1)
    if len(partes) < constantes.CANTIDAD_MINIMA_PARTES_VENTA:
        return False, None

    try:
        nombre = partes[constantes.INDICE_NOMBRE_VENTA].strip()
        entradas = int(partes[constantes.INDICE_ENTRADAS_VENTA].strip())
    except (ValueError, IndexError):
        return False, None

    if nombre not in agencia["peliculas"]:
        return False, nombre

    agencia["ventas"][nombre] = agencia["ventas"].get(nombre, 0) + entradas
    return True, None


def procesar_lineas_csv(
    lineas: list[str], agencia: dict, procesar_linea
) -> tuple[int, list[str]]:
    """
    Procesa las líneas de un archivo CSV genérico (películas o ventas).

    Pre:
    - `lineas` es una lista de cadenas, donde la primera corresponde al encabezado.
    - `agencia` es el diccionario de la agencia.
    - `procesar_linea` es una función que recibe (linea, agencia)
      y devuelve una tupla (bool, nombre_ignorado).

    Post:
    - Devuelve una tupla (cantidad_procesadas, lista_ignoradas),
      donde `cantidad_procesadas` es el número de líneas válidas agregadas
      y `lista_ignoradas` contiene los nombres de los registros duplicados o inexistentes.
    - Ignora líneas vacías o con formato inválido.
    """
    cantidad = 0
    ignoradas = []

    for linea in lineas[constantes.INDICE_ENCABEZADO :]:
        if not linea.strip():
            continue
        ok, nombre_ignorado = procesar_linea(linea, agencia)
        if ok:
            cantidad += 1
        elif nombre_ignorado:
            ignoradas.append(nombre_ignorado)

    return cantidad, ignoradas


def procesar_carga_csv_generico(
    rutas: list[str], agencia: dict, procesar_linea
) -> tuple[int, list[str]]:
    """
    Procesa archivos CSV genéricamente (películas o ventas).

    Pre:
    - `rutas` es una lista de rutas (archivos o directorios).
    - `agencia` es el diccionario de la agencia.
    - `procesar_linea` es una función que recibe (linea, agencia)
     y devuelve (bool, nombre_ignorado).
    Post:
    - Devuelve (cantidad_registros_agregados, lista_nombres_ignorados).
    """
    archivos = obtener_csv_desde_rutas(rutas)

    cantidad = 0
    ignoradas = []

    for archivo in archivos:
        lineas = leer_csv_lineas(archivo)
        if not lineas:
            continue

        cantidad_archivo, ignoradas_archivo = procesar_lineas_csv(
            lineas, agencia, procesar_linea
        )
        cantidad += cantidad_archivo
        ignoradas.extend(ignoradas_archivo)

    return cantidad, ignoradas


def procesar_carga_peliculas(rutas: list[str], agencia: dict) -> tuple[int, list[str]]:
    """
    Carga películas desde archivos CSV en la agencia.

    Pre:
    - `rutas` es lista de archivos o directorios.
    - `agencia` es el diccionario de la agencia.
    Post:
    - Agrega películas y talentos a `agencia`.
    - Devuelve (cantidad agregadas, lista de duplicadas).
    """
    return procesar_carga_csv_generico(
        rutas, agencia, procesar_linea=procesar_linea_pelicula
    )


def procesar_carga_ventas(rutas: list[str], agencia: dict) -> tuple[int, list[str]]:
    """
    Carga ventas desde archivos CSV y actualiza recaudación.

    Pre:
    - `rutas` es lista de archivos o directorios.
    - `agencia` es el diccionario de la agencia.
    Post:
    - Actualiza `agencia["ventas"]`.
    - Devuelve (cantidad importadas, lista de inexistentes).
    """
    return procesar_carga_csv_generico(
        rutas, agencia, procesar_linea=procesar_linea_venta
    )


# Talentos y colaboraciones


def registrar_talentos(talentos: list[str], agencia: dict) -> None:
    """
    Registra talentos y colaboraciones directas.

    Pre:
    - `talentos` es una lista con los nombres originales de los
     talentos que trabajaron juntos en una película.
    - `agencia` es el diccionario de la agencia.
    Post:
    - Actualiza `agencia["talentos"]`: agrega los nombres normalizados
     de los talentos y sus colaboradores directos.
    - Actualiza `agencia["nombres_originales"]`: asocia cada nombre
     normalizado con su nombre original.
    """

    talentos_normalizados = []
    for nombre in talentos:
        nombre_normalizado = validaciones.normalizar_nombre(nombre)
        talentos_normalizados.append(nombre_normalizado)

        if nombre_normalizado not in agencia["talentos"]:
            agencia["talentos"][nombre_normalizado] = set()

        if nombre_normalizado not in agencia["nombres_originales"]:
            agencia["nombres_originales"][nombre_normalizado] = nombre

    return talentos_normalizados


def registrar_colaboraciones(talentos_normalizados: list[str], agencia: dict) -> None:
    """
    Registra las colaboraciones entre los talentos normalizados.

    Pre:
    - `talentos_normalizados` es una lista de nombres de talentos en formato normalizado.
    - `agencia` es el diccionario de la agencia.
    Post:
    - Actualiza `agencia["talentos"]` agregando relaciones de colaboración entre todos los talentos
      de la lista (A colabora con B y B con A).
    """
    for talento_a in talentos_normalizados:
        for talento_b in talentos_normalizados:
            if talento_a != talento_b:
                agencia["talentos"][talento_a].add(talento_b)


def registrar_talentos_y_colab(talentos: list[str], agencia: dict) -> None:
    """
    Registra los talentos en la agencia y sus colaboraciones directas.

    Pre:
    - `talentos` es la lista de nombres de talentos.
    - `agencia` es el diccionario de la agencia.

    Post:
    - Llama a `registrar_talentos` para registrar los nombres normalizados en la agencia.
    - Luego llama a `registrar_colaboraciones` para vincular los talentos entre sí.
    """
    talentos_normalizados = registrar_talentos(talentos, agencia)
    registrar_colaboraciones(talentos_normalizados, agencia)


# Relaciones entre talentos


def obtener_colaboradores_directos(
    nombre_talento: str, agencia: dict
) -> list[str] | None:
    """
    Devuelve colaboradores directos de un talento.

    Pre:
    - `nombre_talento` es string.
    - `agencia` es el diccionario de la agencia.
    Post:
    - Lista de nombres de colaboradores directos, o None si no existe.
    """
    nombre_normalizado = validaciones.normalizar_nombre(nombre_talento)

    nombre_real = None
    for talento in agencia["talentos"]:
        if validaciones.normalizar_nombre(talento) == nombre_normalizado:
            nombre_real = talento
            break

    if nombre_real is None:
        return None

    colaboradores = list(agencia["talentos"][nombre_real])
    colaboradores.sort()

    nombres_reales = []
    for colaborador in colaboradores:
        if colaborador in agencia["nombres_originales"]:
            nombres_reales.append(agencia["nombres_originales"][colaborador])
        else:
            nombres_reales.append(colaborador)

    return nombres_reales


def _recorrer_talentos_conectados(
    talento: str, agencia: dict, visitados: set[str]
) -> None:
    """
    Marca talentos conectados directa o indirectamente.

    Pre:
    - `talento` es nombre normalizado.
    - `visitados` es set de nombres.
    Post:
    - Devuelve `visitados` actualizado con talentos conectados.
    """
    if talento in visitados:
        return

    visitados.add(talento)
    for vecino in agencia["talentos"].get(talento, set()):
        _recorrer_talentos_conectados(vecino, agencia, visitados)


def obtener_nombre_guardado(nombre_talento: str, agencia: dict) -> str | None:
    """
    Devuelve el nombre del talento tal como está guardado en la agencia,
    comparando de forma insensible a mayúsculas, tildes o espacios.

    Pre:
    - `nombre_talento` es el nombre ingresado por el usuario.
    - `agencia` es el diccionario de la agencia.
    Post:
    - Devuelve el nombre exacto que figura en la agencia, si lo encuentra.
    Devuelve None si no hay coincidencia.
    """
    nombre_normalizado = validaciones.normalizar_nombre(nombre_talento)
    for talento in agencia["talentos"]:
        if validaciones.normalizar_nombre(talento) == nombre_normalizado:
            return talento
    return None


def convertir_a_nombres_reales(talentos: list[str], agencia: dict) -> list[str]:
    """
    Convierte una lista de nombres normalizados en sus nombres originales.

    Pre:
    - `talentos` es la lista de nombres de talentos en formato normalizado (sin tildes ni mayúsculas).
    - `agencia` es el diccionario de la agencia.

    Post:
    - Devuelve una nueva lista con los nombres originales de los talentos, según los registros
      en `agencia["nombres_originales"]`.
    - Si un nombre no tiene correspondencia, se devuelve el mismo valor que estaba en la lista.
    """
    nombres = []
    for talento in talentos:
        if talento in agencia["nombres_originales"]:
            nombres.append(agencia["nombres_originales"][talento])
        else:
            nombres.append(talento)
    return nombres


def obtener_talentos_compatibles(
    nombre_talento: str, agencia: dict
) -> list[str] | None:
    """
    Devuelve los talentos compatibles.

    Pre:
    - `nombre_talento` es string con el nobre del talento a buscar.
    - `agencia` es el diccionario de la agencia.
    Post:
    - Devuelve una lista con los nombres originales de los talentos compatibles.
    - Devuelve None si el talento no existe.
    """
    nombre_guardado = obtener_nombre_guardado(nombre_talento, agencia)
    if nombre_guardado is None:
        return None

    # relacionados = talentos conectados directa o indirectamente
    relacionados = set()
    _recorrer_talentos_conectados(nombre_guardado, agencia, relacionados)

    colaboradores_directos = agencia["talentos"].get(nombre_guardado, set())

    compatibles = []
    for talento_relacionado in relacionados:
        if (
            talento_relacionado != nombre_guardado
            and talento_relacionado not in colaboradores_directos
        ):
            compatibles.append(talento_relacionado)

    compatibles.sort()

    nombres_compatibles = convertir_a_nombres_reales(compatibles, agencia)
    return nombres_compatibles


def obtener_talentos_incompatibles(
    nombre_talento: str, agencia: dict
) -> list[str] | None:
    """
    Devuelve talentos incompatibles.

    Pre:
    - `nombre_talento` es string con el nombre del talento a buscar.
    - `agencia` es el diccionario de la agencia.
    Post:
    - Lista de nombres incompatibles, o None si no existe.
    """
    nombre_guardado = obtener_nombre_guardado(nombre_talento, agencia)
    if nombre_guardado is None:
        return None

    relacionados = set()
    _recorrer_talentos_conectados(nombre_guardado, agencia, relacionados)

    incompatibles = []
    for talento in agencia["talentos"]:
        if talento not in relacionados:
            incompatibles.append(talento)

    incompatibles.sort()

    nombres_incompatibles = convertir_a_nombres_reales(incompatibles, agencia)

    return nombres_incompatibles


# Recaudaciones de los talentos y exportación


def calcular_recaudacion_talento(agencia: dict) -> dict[str, int]:
    """
    Calcula la recaudación total por talento.

    Pre:
    - `agencia` es el diccionario de la agencia.
    Post:
    - Devuelve dict talento -> recaudación total.
    """
    recaudaciones = {}

    for pelicula in agencia["peliculas"]:
        info_pelicula = agencia["peliculas"][pelicula]
        precio = info_pelicula["precio"]
        entradas = agencia["ventas"].get(pelicula, 0)
        total = precio * entradas

        for talento in info_pelicula["talentos"]:
            if talento not in recaudaciones:
                recaudaciones[talento] = 0
            recaudaciones[talento] = recaudaciones[talento] + total

    for talento in agencia["talentos"]:
        if talento not in recaudaciones:
            recaudaciones[talento] = 0

    return recaudaciones


def criterio_orden(registro: tuple[str, int]) -> tuple[int, str]:
    """
    Ordena primero por recaudación descendente, luego alfabéticamente.

    Pre:
    - `registro` es una tupla (nombre, recaudacion).
    Post:
    - Devuelve (-recaudacion, nombre_en_minusculas) para ordenar
      primero por recaudación descendente y luego alfabéticamente.
    """
    nombre, recaudacion = registro
    return (-recaudacion, nombre.lower())


def validar_ruta_csv(ruta_destino: str) -> bool:
    """
    Valida que la ruta proporcionada sea válida para crear un archivo CSV.

    Pre:
    - `ruta_destino` es una cadena que indica la ruta del archivo.
    Post:
    - Devuelve True si la ruta es válida (termina en .csv, sin espacios
      y con directorio existente si corresponde), False en caso contrario.
    """
    ruta_destino = ruta_destino.strip()

    if not ruta_destino or " " in ruta_destino:
        return False

    if not ruta_destino.lower().endswith(".csv"):
        return False

    # si se especifica un directorio, tiene que existir
    directorio = os.path.dirname(ruta_destino)
    if directorio and not os.path.isdir(directorio):
        return False

    return True


def escribir_recaudaciones_csv(
    ruta_destino: str, registros: list[tuple[str, int]] | None = None
) -> bool:
    """
    Escribe un archivo CSV con encabezado 'actor,recaudacion' y, si hay datos, los agrega debajo.

    Pre:
    - `ruta_destino` es una ruta válida para escritura.
    - `registros` es una lista de tuplas (nombre, total) o None.
    Post:
    - Crea el archivo CSV con encabezado y los registros (si existen).
    - Devuelve True si la operación fue exitosa, False si ocurrió un error.
    """
    try:
        with open(ruta_destino, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["actor", "recaudacion"])
            if registros:
                for nombre, total in registros:
                    writer.writerow([nombre, total])
        return True
    except (FileNotFoundError, IOError):
        return False


def combinar_recaudaciones_unicas(
    recaudaciones: dict[str, int], agencia: dict
) -> list[tuple[str, int]]:
    """
    Combina las recaudaciones por talento, evitando duplicados por normalización.

    Pre:
    - `recaudaciones` es un diccionario {nombre_talento_normalizado: total}.
    - `agencia` es el diccionario de la agencia.
    Post:
    - Devuelve una lista de tuplas (nombre_real, total)
      ordenadas por recaudación descendente y nombre alfabético.
    """
    unicos = {}

    for nombre_talento_normalizado, total in recaudaciones.items():
        nombre_real = agencia.get("nombres_originales", {}).get(
            nombre_talento_normalizado, nombre_talento_normalizado
        )
        nombre_sin_tildes = validaciones.normalizar_nombre(nombre_real)

        if nombre_sin_tildes not in unicos:
            unicos[nombre_sin_tildes] = {"nombre": nombre_real, "total": total}
        else:
            unicos[nombre_sin_tildes]["total"] += total

    registros = []
    for talento in unicos.values():
        nombre = talento["nombre"]
        total = talento["total"]
        registros.append((nombre, total))

    registros.sort(key=criterio_orden)
    return registros


def exportar_recaudacion_a_csv(ruta_destino: str, agencia: dict) -> bool:
    """
    Exporta recaudación de talentos a CSV.

    Pre:
    - `ruta_destino` es la ruta de salida del archivo CSV.
    - `agencia` es el diccionario de la agencia.
    Post:
    - Crea un archivo con encabezado 'actor,recaudacion' y los totales calculados.
    - Si no hay películas cargadas, genera solo el encabezado.
    - Devuelve True si el archivo se creó correctamente, False si hubo errores o ruta inválida.
    """

    if not validar_ruta_csv(ruta_destino):
        return False

    recaudaciones = calcular_recaudacion_talento(agencia)

    if not agencia["peliculas"]:
        return escribir_recaudaciones_csv(ruta_destino)

    registros = combinar_recaudaciones_unicas(recaudaciones, agencia)
    return escribir_recaudaciones_csv(ruta_destino, registros)
