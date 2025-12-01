"""
Logica del juego Sixteen
"""

import random

ITERACIONES_RANDOM = 111


def crear_tablero(n_filas: int, n_columnas: int) -> list[list[int]]:
    tablero = []
    numero = 1
    for _ in range(n_filas):
        fila = []
        for _ in range(n_columnas):
            fila.append(numero)
            numero += 1
        tablero.append(fila)
    return tablero


def rotar_izquierda(tablero: list[list[int]], fila: int) -> bool:
    if fila < 0 or fila >= len(tablero):
        return False
    if len(tablero[fila]) < 2:
        return False
    tablero[fila] = tablero[fila][1:] + [tablero[fila][0]]
    return True


def rotar_derecha(tablero: list[list[int]], fila: int) -> bool:
    if fila < 0 or fila >= len(tablero):
        return False
    if len(tablero[fila]) < 2:
        return False
    tablero[fila] = tablero[fila][-1:] + tablero[fila][:-1]
    return True


def rotar_arriba(tablero: list[list[int]], columna: int) -> bool:
    if columna < 0 or columna >= len(tablero[0]):
        return False
    if len(tablero) < 2:
        return False
    numeros_columna = [fila[columna] for fila in tablero]
    numeros_columna = numeros_columna[1:] + numeros_columna[:1]
    for i in range(len(tablero)):
        tablero[i][columna] = numeros_columna[i]
    return True


def rotar_abajo(tablero: list[list[int]], columna: int) -> bool:
    if columna < 0 or columna >= len(tablero[0]):
        return False
    if len(tablero) < 2:
        return False
    numeros_columna = [fila[columna] for fila in tablero]
    numeros_columna = numeros_columna[-1:] + numeros_columna[:-1]
    for i in range(len(tablero)):
        tablero[i][columna] = numeros_columna[i]
    return True


def esta_ordenado(tablero: list[list[int]]) -> bool:
    numero_esperado = 1
    for fila in tablero:
        for numero_actual in fila:
            if numero_actual != numero_esperado:
                return False
            numero_esperado += 1
    return True


def mover_izquierda(tablero):
    filas = len(tablero)
    rotar_izquierda(tablero, random.randint(0, filas - 1))


def mover_derecha(tablero):
    filas = len(tablero)
    rotar_derecha(tablero, random.randint(0, filas - 1))


def mover_arriba(tablero):
    columnas = len(tablero[0])
    rotar_arriba(tablero, random.randint(0, columnas - 1))


def mover_abajo(tablero):
    columnas = len(tablero[0])
    rotar_abajo(tablero, random.randint(0, columnas - 1))


def mezclar_tablero(tablero: list[list[int]]):
    movimientos = [mover_izquierda, mover_derecha, mover_arriba, mover_abajo]
    for _ in range(ITERACIONES_RANDOM):
        random.choice(movimientos)(tablero)
