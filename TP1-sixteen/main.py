"""
Interfaz e interacción con el usuario para el juego Sixteen
"""

import sixteen

PAD = 3

def pedir_entero(mensaje: str) -> int:
    """Solicita al usuario un número entero positivo y valida la entrada.

    La función continúa solicitando entrada hasta que se proporcione
    un número entero válido mayor que cero.

    PRECONDICIONES:
        - `mensaje` es una cadena de texto que se muestra al usuario.

    POSTCONDICIONES:
        - La función devuelve un entero positivo.
        - La función no retorna hasta que se ingrese un valor válido.
    """
    op = input(mensaje)
    while not op.isdigit() or int(op) <= 0:
        op = input("Entrada erronea, vuelva a ingresar un numero: ")
    return int(op)


def pedir_movimiento(mensaje: str) -> tuple[str, int] | None:
    """Solicita al usuario un movimiento en formato 'n,direccion' y valida la entrada.

    Formato esperado: 'n,direccion' donde n es un índice y direccion es w/a/s/d.
    Las direcciones válidas son: w (arriba), a (izquierda), s (abajo), d (derecha).
    El índice debe ser un entero no negativo. Ingresar 'q' permite salir.

    PRECONDICIONES:
        - `mensaje` es una cadena de texto que se muestra al usuario.

    POSTCONDICIONES:
        - Si la entrada es válida, devuelve una tupla (direccion, n).
        - Si se ingresa 'q', devuelve None.
        - La función no retorna hasta que se ingrese un valor válido o 'q'.
    """
    while True:
        op = input(mensaje)
        if op == "q":
            return

        entrada = op.split(",")
        if len(entrada) != 2:
            print("Cantidad de argumentos erronea, se esperaban dos")
            continue

        n, direccion = entrada
        if not n.isdigit() or not int(n) >= 0:
            print("El índice especificado no es un entero positivo")
            continue

        if direccion not in "wasd":
            print("Dirección desconocida")
            continue

        return direccion, int(n)


def mostrar_tablero(tablero: list[list[int]]) -> None:
    """Muestra el tablero del juego en formato tabular con índices.

    El tablero se muestra con índices de columnas en la parte superior,
    índices de filas en el lado izquierdo, y cada celda centrada con
    un ancho de PAD caracteres. Usa separadores visuales para mejorar
    la legibilidad.

    PRECONDICIONES:
        - `tablero` es una lista de listas de enteros de cualquier dimensión.

    POSTCONDICIONES:
        - La función imprime el tablero en la consola.
        - No modifica el tablero original.
    """
    indice = []
    for col in range(len(tablero[0])):
        indice.append(str(col).center(PAD))
    print(" " * PAD + "|" + "|".join(indice))
    print(" " * PAD + "=" * len(tablero[0]) * (PAD + 1))

    for fil in range(len(tablero)):
        fila = []
        for col in range(len(tablero[fil])):
            fila.append(str(tablero[fil][col]).center(PAD))
        print(str(fil).center(PAD) + "‖" + "|".join(fila))


def aplicar_movimiento(tablero: list[list[int]], direccion: str, n: int) -> None:
    """Aplica un movimiento de rotación al tablero según la dirección e índice especificados.

    Las direcciones de rotación son:
    - w: rota la columna n hacia arriba
    - a: rota la fila n hacia la izquierda
    - s: rota la columna n hacia abajo
    - d: rota la fila n hacia la derecha

    PRECONDICIONES:
        - `tablero` es una lista de listas de enteros de cualquier dimensión.
        - `direccion` es una de las letras: 'w', 'a', 's', 'd'.
        - `n` es un entero que representa el índice de fila o columna.

    POSTCONDICIONES:
        - Si el índice es válido, se aplica la rotación al tablero.
        - Si el índice es inválido, se muestra un mensaje de error.
        - El tablero se modifica in-place si la operación es exitosa.
    """
    aplicado = True
    if direccion == "w":
        aplicado = sixteen.rotar_arriba(tablero, n)
    if direccion == "s":
        aplicado = sixteen.rotar_abajo(tablero, n)
    if direccion == "a":
        aplicado = sixteen.rotar_izquierda(tablero, n)
    if direccion == "d":
        aplicado = sixteen.rotar_derecha(tablero, n)
    if not aplicado:
        print("Indice invalido")


def main() -> None:
    """Función principal del juego Sixteen.

    Ejecuta el flujo completo del juego. Solicita dimensiones del tablero,
    crea y mezcla el tablero inicial, muestra el tablero, y permite al
    jugador realizar movimientos hasta ordenar el tablero. Muestra mensaje
    de victoria al completar el juego.

    PRECONDICIONES:
        - No requiere parámetros de entrada.

    POSTCONDICIONES:
        - El juego se ejecuta completamente o el usuario sale.
        - Al finalizar, el tablero estará ordenado o el usuario habrá salido.
        - Se valida que todas las entradas del usuario sean correctas.
    """
    ancho = pedir_entero("Ingrese el ancho del juego: ")
    alto = pedir_entero("Ingrese el alto del juego: ")
    tablero = sixteen.crear_tablero(alto, ancho)

    print("=== Sixteen ===")
    sixteen.mezclar_tablero(tablero)
    mostrar_tablero(tablero)
    while not sixteen.esta_ordenado(tablero):
        print(f"Direcciones: w (arriba), a (abajo), s (izquierda), d (derecha)")
        entrada = pedir_movimiento("Ingrese el movimiento <n, dir> o 'q' para salir: ")
        if not entrada:
            return
        direccion, n = entrada
        aplicar_movimiento(tablero, direccion, n)
        mostrar_tablero(tablero)

    print("Ganaste! :)")


if __name__ == "__main__":
    main()
