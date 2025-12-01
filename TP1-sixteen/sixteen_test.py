import pprint
import sys
import traceback
from typing import List

import sixteen

# Si las pruebas se ven mal en tu terminal, probá cambiando el valor
# de esta constante a True para desactivar los colores ANSI.
TERMINAL_SIN_COLOR = False


def validar_estado(desc: List[List[int]], tablero: List[List[int]]):
    """Asegura que `tablero` tenga un estado similar a `desc`. Se prueba que:
    - El tipo de cada elemento, en todos sus niveles, sea el mismo
    - Las dimensiones sean las mismas
    - El contenido sea el mismo
    """
    x = None
    y = None
    ancho, alto = len(desc[0]), len(desc)
    try:
        assert type(desc) is type(tablero), "Valor en `tablero` no es del tipo lista"
        assert len(tablero) > 0, "Lista en `tablero` está vacía"
        assert (ancho, alto) == (len(tablero[0]), len(tablero)), (
            f"Dimension obtenida ({ancho}, {alto}) no es la esperada "
            f"({len(desc[0])}, {len(desc)})"
        )
        for y in range(alto):
            assert type(desc[y]) is type(
                tablero[y]
            ), f"Valor en `tablero[{y}]` no es del tipo lista"
            for x in range(ancho):
                assert type(desc[y][x]) is type(
                    tablero[y][x]
                ), f"Valor en `tablero[{y}][{x}]` no es del tipo entero"
                assert desc[y][x] == tablero[y][x]
    except AssertionError as exc:
        error_msg = "Estado esperado:\n"
        error_msg += pprint.pformat(desc) + "\n"
        error_msg += "\n"
        error_msg += "Estado actual:\n"
        error_msg += pprint.pformat(tablero) + "\n\n"
        if x is not None and y is not None:
            error_msg += f"Error en columna = {x}, fila = {y}:\n"
            error_msg += f"\tValor esperado: {desc[y][x]}\n"
            error_msg += f"\tValor encontrado: {tablero[y][x]}\n"
        raise AssertionError(error_msg + str(exc)) from exc


def test_01_crear_tablero_cuadrado():
    """Crea un nuevo tablero básico de sixteen de dimensiones simétricas 4x4"""
    desc = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]
    tablero = sixteen.crear_tablero(4, 4)
    validar_estado(desc, tablero)


def test_02_crear_tablero_rectangular():
    """Crea un nuevo juego básico de sixteen de dimensiones 3x6"""
    desc = [
        [1, 2, 3, 4, 5, 6],
        [7, 8, 9, 10, 11, 12],
        [13, 14, 15, 16, 17, 18],
    ]
    tablero = sixteen.crear_tablero(3, 6)
    validar_estado(desc, tablero)


def test_03_rotar_izquierda_tablero_cuadrado():
    """Valida el funcionamiento de la función `rotar_izquierda` considerando un
    tablero cuadrado."""
    desc = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [10, 11, 12, 9],
        [13, 14, 15, 16],
    ]
    tablero = sixteen.crear_tablero(4, 4)
    assert sixteen.rotar_izquierda(tablero, 2), (
        "Llamada válida a función de rotar con índice " "fila=2 devolvió `False`"
    )
    validar_estado(desc, tablero)


def test_04_rotar_izquierda_con_fila_invalida():
    """Asegura que rotar a la izquierda no pueda completarse si el indice
    indicado es inválido"""
    desc = [
        [1, 2, 3, 4, 5, 6],
        [7, 8, 9, 10, 11, 12],
        [13, 14, 15, 16, 17, 18],
    ]
    tablero = sixteen.crear_tablero(3, 6)
    assert not sixteen.rotar_izquierda(tablero, 5), (
        "Llamada inválida a función de rotar con índice " "fila=5 devolvió `True`"
    )
    assert not sixteen.rotar_izquierda(tablero, -1), (
        "Llamada inválida a función de rotar con índice " "fila=-1 devolvió `True`"
    )
    validar_estado(desc, tablero)


def test_05_rotar_derecha_tablero_cuadrado():
    """Valida el funcionamiento de la función `rotar_derecha` considerando un
    tablero cuadrado."""
    desc = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [12, 9, 10, 11],
        [13, 14, 15, 16],
    ]
    tablero = sixteen.crear_tablero(4, 4)
    assert sixteen.rotar_derecha(tablero, 2), (
        "Llamada válida a función de rotar con índice " "fila=2 devolvió `False`"
    )
    validar_estado(desc, tablero)


def test_06_rotar_arriba_tablero_cuadrado():
    """Valida el funcionamiento de la función `rotar_arriba` considerando un
    tablero cuadrado."""
    desc = [
        [1, 2, 7, 4],
        [5, 6, 11, 8],
        [9, 10, 15, 12],
        [13, 14, 3, 16],
    ]
    tablero = sixteen.crear_tablero(4, 4)
    assert sixteen.rotar_arriba(tablero, 2), (
        "Llamada válida a función de rotar con índice " "columna=2 devolvió `False`"
    )
    validar_estado(desc, tablero)


def test_07_tablero_esta_ordenado():
    """Verifica algunos casos donde la función `esta_ordenado` devuelva `True`."""
    tablero = sixteen.crear_tablero(3, 3)
    tablero2 = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
    ]
    assert sixteen.esta_ordenado(tablero), (
        "`esta_ordenado` devolvió `False` para el siguiente tablero:"
        f"{pprint.pformat(tablero)}"
    )
    assert sixteen.esta_ordenado(tablero2), (
        "`esta_ordenado` devolvió `False` para el siguiente tablero:"
        f"{pprint.pformat(tablero2)}"
    )


def test_08_tablero_no_esta_ordenado():
    """Verifica algunos casos donde la función `esta_ordenado` devuelva `False`."""
    tablero = sixteen.crear_tablero(3, 3)
    sixteen.rotar_izquierda(tablero, 1)
    tablero2 = [
        [1, 2, 3, 9, 5],
        [6, 7, 8, 14, 10],
        [11, 12, 13, 4, 15],
    ]
    assert not sixteen.esta_ordenado(tablero), (
        "`esta_ordenado` devolvió `True` para el siguiente tablero:"
        f"{pprint.pformat(tablero)}"
    )
    assert not sixteen.esta_ordenado(tablero2), (
        "`esta_ordenado` devolvió `True` para el siguiente tablero:"
        f"{pprint.pformat(tablero2)}"
    )


# Sólo se van a correr aquellos tests que estén mencionados dentro de la
# siguiente constante
TESTS = (
    test_01_crear_tablero_cuadrado,
    test_02_crear_tablero_rectangular,
    test_03_rotar_izquierda_tablero_cuadrado,
    test_04_rotar_izquierda_con_fila_invalida,
    test_05_rotar_derecha_tablero_cuadrado,
    test_06_rotar_arriba_tablero_cuadrado,
    test_07_tablero_esta_ordenado,
    test_08_tablero_no_esta_ordenado,
)

# El código que viene abajo tiene algunas *magias* para simplificar la corrida
# de los tests y proveer la mayor información posible sobre los errores que se
# produzcan. ¡No te preocupes si no lo entendés completamente!

# Colores ANSI para una salida más agradable en las terminales que lo permitan
COLOR_OK = "\033[1m\033[92m"
COLOR_ERR = "\033[1m\033[91m"
COLOR_RESET = "\033[0m"


def print_color(color: str, *args, **kwargs):
    """
    Mismo comportamiento que `print` pero con un
    primer parámetro para indicar de qué color se
    imprimirá el texto.

    Si la constante TERMINAL_SIN_COLOR es True,
    esta función será exactamente equivalente
    a utilizar `print`.
    """
    if TERMINAL_SIN_COLOR:
        print(*args, **kwargs)
    else:
        print(color, end="")
        print(*args, **kwargs)
        print(COLOR_RESET, end="", flush=True)


def main():
    tests_fallidos = []
    tests_a_correr = [int(t) for t in sys.argv[1:]]
    for i, test in [
        (i, test)
        for i, test in enumerate(TESTS)
        if not tests_a_correr or i + 1 in tests_a_correr
    ]:
        print(f"Prueba {i + 1 :02} - {test.__name__}: ", end="", flush=True)
        try:
            test()
            print_color(COLOR_OK, "[OK]")
        except AssertionError as e:
            tests_fallidos.append(test.__name__)
            print_color(COLOR_ERR, "[ERROR]")
            print_color(COLOR_ERR, " >", *e.args)
            break
        except Exception:
            tests_fallidos.append(test.__name__)
            print_color(COLOR_ERR, "[BOOM - Explotó]")
            print("\n--------------- Python dijo: ---------------")
            traceback.print_exc()
            print("--------------------------------------------\n")
            break

    if not tests_fallidos:
        print()
        print_color(COLOR_OK, "###########")
        print_color(COLOR_OK, "# TODO OK #")
        print_color(COLOR_OK, "###########")
        print()
    else:
        print()
        print_color(COLOR_ERR, "##################################")
        print_color(COLOR_ERR, "              ¡ERROR!             ")
        print_color(COLOR_ERR, "Falló el siguiente test:")
        for test_con_error in tests_fallidos:
            print_color(COLOR_ERR, " - " + test_con_error)
        print_color(COLOR_ERR, "##################################")
        print(
            "TIP: Si la información de arriba no es suficiente para entender "
            "el error, revisá el código de las pruebas que fallaron en el "
            "archivo tests_reduced.py."
        )


main()
