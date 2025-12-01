"""
Este módulo contiene funciones que solicitan y validan las entradas del usuario.
"""

import constantes
import presentacion


def _es_solo_letras_y_espacios(cadena: str) -> bool:
    """
    Verifica si una cadena contiene solamente letras o espacios.

    Pre:
        - `cadena` es una cadena de texto.
    Post:
        - Devuelve True si la cadena contiene solo caracteres alfabéticos o espacios.
        - Devuelve False en cualquier otro caso.
    """
    if not cadena:
        return False

    for caracter in cadena:
        if not (caracter.isalpha() or caracter == " "):
            return False

    return True


def es_nombre_apellido_valido(nombre_apellido: str) -> bool:
    """
    Valida que el nombre/apellido cumpla con los criterios.

    Pre:
        - `nombre_apellido` es una cadena de texto.
    Post:
        - Devuelve True si el nombre/apellido:
            - No está vacío o no contiene únicamente espacios.
            - Tiene una longitud máxima de 30 caracteres.
            - Está compuesto únicamente por letras y espacios.
        - Devuelve False en caso contrario.
    """
    # si es vacío o solo contiene espacios
    if not nombre_apellido or not nombre_apellido.strip():
        return False

    if len(nombre_apellido) > 30:
        return False

    if not _es_solo_letras_y_espacios(nombre_apellido):
        return False

    return True


def validar_formato_dni(dni: str) -> bool:
    """
    Valida que el DNI cumpla con el formato XX.YYY.ZZZ y contenga
    exactamente 8 dígitos numéricos.

    Pre:
        - `dni` es una cadena de texto.
    Post:
        - Devuelve True si `dni_str` tiene la longitud correcta (10 caracteres),
          los puntos en las posiciones esperadas (2 y 6), y las partes numéricas
          suman 8 dígitos en total.
        - Devuelve False en cualquier otro caso.
    """
    if len(dni) != 10:
        return False

    if dni[2] != "." or dni[6] != ".":
        return False

    partes = dni.split(".")
    for parte in partes:
        if not parte.isdigit():
            return False

    dni_numerico = "".join(partes)
    if len(dni_numerico) != 8:
        return False

    return True


def solicitar_nombre_apellido(mensaje: str) -> str | None:
    """
    Solicita al usuario el nombre y apellido repetidamente hasta que sea válido
    o se ingrese el COMANDO_RETROCEDER.

    Pre:
        - `mensaje` es una cadena de texto a mostrar como prompt.
    Post:
        - Imprime `MSG_NOMBRE_INVALIDO` si el formato es incorrecto.
        - Devuelve la cadena de texto del nombre y apellido validado.
        - Devuelve None si el usuario ingresa `COMANDO_RETROCEDER`.
    """
    while True:
        nombre_apellido = input(mensaje)

        if nombre_apellido == constantes.COMANDO_RETROCEDER:
            return None

        if es_nombre_apellido_valido(nombre_apellido):
            return nombre_apellido

        print(constantes.MSG_NOMBRE_INVALIDO)


def solicitar_dni(cuentas: dict, mensaje: str, debe_existir: bool) -> str | None:
    """
    Solicita al usuario un DNI, valida su formato y su existencia/unicidad
    en el diccionario `cuentas`, según el parámetro `debe_existir`.

    Pre:
        - `cuentas` es el diccionario de cuentas.
        - `mensaje` es una cadena de texto a mostrar como prompt.
        - `debe_existir` es un booleano: True si el DNI debe existir, False si no debe existir.
    Post:
        - Imprime `MSG_DNI_INVALIDO` si el formato es incorrecto.
        - Imprime `MSG_NO_EXISTE_CUENTA` si el DNI no existe cuando se esperaba.
        - Imprime `MSG_CUENTA_EXISTE` si el DNI ya existe cuando no se esperaba.
        - Devuelve la cadena de texto del DNI validado.
        - Devuelve None si el usuario ingresa `COMANDO_RETROCEDER`, o si el DNI
          no cumple con la condición `debe_existir` tras la primera validación.
    """
    while True:
        dni = input(mensaje)

        if dni == constantes.COMANDO_RETROCEDER:
            return None

        if not validar_formato_dni(dni):
            print(constantes.MSG_DNI_INVALIDO)
            continue

        # caso donde el DNI debe existir - debe_existir == True
        if debe_existir:
            if dni not in cuentas:
                print(constantes.MSG_NO_EXISTE_CUENTA)
                return None
            return dni

        # caso donde el DNI NO debe existir (para crear cuenta) - debe_existir == False
        if dni in cuentas:
            nombre_existente = cuentas[dni]["nombre_apellido"]
            print(constantes.MSG_CUENTA_EXISTE.format(nombre=nombre_existente))
            return None

        return dni


def solicitar_entero_minimo(
    mensaje: str, min_valor: int, mensaje_error: str
) -> int | None:
    """
    Solicita un valor entero al usuario, y valida que sea un número entero
    y que cumpla con un valor mínimo. Permite retroceder con el COMANDO_RETROCEDER.

    Pre:
        - `mensaje` es una cadena de texto a mostrar como prompt.
        - `min_valor` es un número entero no negativo.
        - `mensaje_error` es una cadena de texto a mostrar como error.
    Post:
        - Devuelve el valor validado como int.
        - Devuelve None si el usuario retrocede o ingresa un valor inválido.
    """
    while True:
        entero_str = input(mensaje)

        if entero_str == constantes.COMANDO_RETROCEDER:
            return None

        try:
            entero_int = int(entero_str)
            if entero_int < min_valor:
                print(mensaje_error)
            else:
                return entero_int
        except ValueError:
            print(mensaje_error)


def solicitar_monto_minimo(mensaje: str, min_monto: int) -> int | None:
    """
    Solicita al usuario un monto.
    Valida el formato con la función `solicitar_entero_minimo`.
    """
    return solicitar_entero_minimo(mensaje, min_monto, constantes.MSG_MONTO_INVALIDO)


def solicitar_interes_minimo(mensaje: str, min_interes: int) -> int | None:
    """
    Solicita al usuario una tasa de interés.
    Valida el formato con la función `solicitar_entero_minimo`.
    """
    return solicitar_entero_minimo(
        mensaje, min_interes, constantes.MSG_TASA_INTERES_INVALIDA
    )


def solicitar_indice_prestamo(
    mensaje: str, num_prestamos_disponibles: int
) -> int | None:
    """
    Solicita al usuario el id de un préstamo a seleccionar,
    y valida que sea un número entero y esté dentro del rango de préstamos disponibles.

    Pre:
        - `mensaje` es una cadena de texto a mostrar como prompt.
        - `num_prestamos_disponibles` es un número entero positivo que indica
          la cantidad total de préstamos para validar el rango de selección.
    Post:
        - Solicita el índice repetidamente hasta que sea válido o se ingrese el COMANDO_RETROCEDER.
        - Imprime `MSG_SELECCION_INVALIDA` si la entrada no es un entero
          o está fuera del rango de 1 a `num_prestamos_disponibles`.
        - Devuelve el índice del préstamo validado.
        - Devuelve None si el usuario ingresa `COMANDO_RETROCEDER`.
    """
    while True:
        seleccion_str = input(mensaje)

        if seleccion_str == constantes.COMANDO_RETROCEDER:
            return None

        try:
            seleccion_int = int(seleccion_str)
            if 1 <= seleccion_int <= num_prestamos_disponibles:
                # ajusta la selección del usuario (id que comienza desde 1) a la posición
                # de una lista, donde el indice del primer elemento es 0.
                return seleccion_int - 1
            print(constantes.MSG_SELECCION_INVALIDA)

        except ValueError:
            print(constantes.MSG_SELECCION_INVALIDA)


def hay_prestamos_pendientes(cuenta: dict) -> bool:
    """
    Verifica si la cuenta tiene al menos un préstamo con deuda pendiente.

    Pre:
        - `cuenta` es el diccionario de cuentas.
    Post:
        - Devuelve True si hay algún préstamo con deuda pendiente, False en caso contrario.
    """
    tiene_prestamos_pendientes = False

    for prestamo in cuenta["prestamos"]:
        deuda_restante = (
            prestamo["capital_pendiente"]
            + prestamo["intereses_pendientes"]
            + prestamo["impuestos_pendientes"]
        )

        if deuda_restante > 0:
            tiene_prestamos_pendientes = True
            break

    return tiene_prestamos_pendientes


def seleccionar_prestamo(cuenta: dict) -> dict | None:
    """
    Muestra los préstamos de la cuenta y permite seleccionar uno.
    Devuelve el préstamo elegido o None si la selección es inválida.

    Pre:
        - `cuenta` es el diccionario de cuentas.
    Post:
        - Si la operación es exitosa, devuelve el diccionario de un préstamo.
        - Devuelve None si la selección es inválida.
    """
    presentacion.mostrar_prestamos_cuenta(cuenta)
    indice_seleccionado = solicitar_indice_prestamo(
        "Seleccione préstamo: ", len(cuenta["prestamos"])
    )

    if indice_seleccionado is None:
        return None

    return cuenta["prestamos"][indice_seleccionado]


def obtener_deuda_total_valida(prestamo: dict) -> int | None:
    """
    Calcula la deuda total pendiente de un préstamo y verifica que sea mayor a cero.

    Pre:
        - `prestamo` es el diccionario de un préstamo (con `capital_pendiente`).
    Post:
        - Devuelve el monto total pendiente del préstamo o None si ya está saldado,
        e imprime `MSG_PRESTAMO_NO_ACTIVO` en ese caso.
    """
    deuda_total_prestamo = (
        prestamo["impuestos_pendientes"]
        + prestamo["intereses_pendientes"]
        + prestamo["capital_pendiente"]
    )

    if deuda_total_prestamo <= 0:
        print(constantes.MSG_PRESTAMO_NO_ACTIVO)
        return None

    return deuda_total_prestamo


def solicitar_monto_pago(cuenta: dict, deuda_total_prestamo: int) -> int | None:
    """
    Solicita un monto a pagar y valida que el saldo sea suficiente.

    Pre:
        - `cuenta` es el diccionario de cuentas.
        - `deuda_total_prestamo` es el monto total pendiente del préstamo seleccionado.
    Post:
        - Devuelve el monto a aplicar o None si es inválido.
    """
    monto_pago = solicitar_monto_minimo("Ingrese monto a abonar: ", 1)

    if monto_pago is None:
        return None

    if cuenta["saldo_disponible"] < monto_pago:
        print(constantes.MSG_SALDO_INSUFICIENTE)
        return None

    return min(monto_pago, deuda_total_prestamo)
