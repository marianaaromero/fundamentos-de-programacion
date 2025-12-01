"""
Contiene las funciones que gestionan las operaciones de la aplicación.
"""

import presentacion
import constantes
import validaciones
import negocio


def crear_cuenta(cuentas: dict) -> None:
    """
    Permite registrar una nueva cuenta en el sistema FundaPay.
    Solicita nombre y apellido, y DNI, y valida su formato y unicidad.

    Pre:
        - `cuentas` es el diccionario de cuentas.
    Post:
        - Si la operación es exitosa (nombre y DNI válidos y DNI no duplicado):
            - Se añade una nueva entrada al diccionario `cuentas` con el DNI como clave.
            - La nueva cuenta se inicializa con saldo 0, listas vacías para préstamos
              y transferencias, y `next_prestamo_id` en 1.
            - Se imprime `MSG_CUENTA_CREADA`.
        - Si el usuario retrocede, el DNI es inválido o duplicado, o el nombre es inválido:
            - `cuentas` no es modificado.
            - Se imprimen mensajes de error específicos.
            - La función retorna None (vuelve al menú principal).
    """
    nombre = validaciones.solicitar_nombre_apellido("Ingrese nombre y apellido: ")
    if nombre is None:
        return

    dni = validaciones.solicitar_dni(cuentas, "Ingrese DNI: ", debe_existir=False)
    if dni is None:
        return

    negocio.registrar_cuenta(cuentas, nombre, dni)

    print(constantes.MSG_CUENTA_CREADA)


def ingresar_dinero(cuentas: dict) -> None:
    """
    Permite acreditar un monto de dinero a una cuenta existente.
    Solicita un DNI y el monto a ingresar, y los valida.
    El monto mínimo de ingreso es de $100.

    Pre:
        - `cuentas` es el diccionario de cuentas.
    Post:
        - Si la operación es exitosa (DNI válido y existente, monto válido):
            - El `saldo_disponible` de la cuenta correspondiente se incrementa
              con el `monto_a_acreditar`.
            - Se imprime `MSG_INGRESO_ACREDITADO`.
        - Si el usuario retrocede, el DNI es inválido o no existe, o el monto es inválido:
            - `cuentas` no es modificado.
            - Se imprimen mensajes de error específicos.
            - La función retorna None.
    """
    dni = validaciones.solicitar_dni(cuentas, "Ingrese DNI: ", debe_existir=True)
    if dni is None:
        return

    monto_a_acreditar = validaciones.solicitar_monto_minimo("Ingrese monto: ", 100)
    if monto_a_acreditar is None:
        return

    negocio.acreditar_dinero(cuentas, dni, monto_a_acreditar)

    print(
        constantes.MSG_INGRESO_ACREDITADO.format(
            monto=monto_a_acreditar, nombre=cuentas[dni]["nombre_apellido"]
        )
    )


def transferir_dinero(cuentas: dict) -> None:
    """
    Permite transferir dinero entre dos cuentas existentes.
    Solicita DNI de origen, DNI de destino y el monto a transferir.
    Valida la existencia de las cuentas, que sean diferentes y que haya saldo suficiente.
    Registra las transferencias en ambas cuentas.

    Pre:
        - `cuentas` es el diccionario de cuentas.
    Post:
        - Si la operación es exitosa:
            - Se ejecuta la función `negocio.transferir_dinero`, que actualiza los saldos
              y registra las transferencias en ambas cuentas.
            - Se imprime `MSG_TRANSFERENCIA_EXITOSA`.
        - Si alguna validación falla (DNIs inválidos o iguales, monto insuficiente, etc.):
            - `cuentas` no es modificado.
            - Se imprimen mensajes de error específicos.
            - La función retorna None.
    """
    dni_origen = validaciones.solicitar_dni(
        cuentas, "Ingrese DNI origen: ", debe_existir=True
    )
    if dni_origen is None:
        return

    dni_destino = validaciones.solicitar_dni(
        cuentas, "Ingrese DNI destino: ", debe_existir=True
    )

    if dni_destino is None:
        return

    if dni_destino == dni_origen:
        print(constantes.MSG_INPUT_INVALIDO)
        return

    monto_a_transferir = validaciones.solicitar_monto_minimo("Ingrese monto: ", 100)
    if monto_a_transferir is None:
        return

    transferencia_realizada = negocio.transferir_dinero(
        cuentas, dni_origen, dni_destino, monto_a_transferir
    )

    if not transferencia_realizada:
        print(constantes.MSG_MONTO_NO_DISPONIBLE)
        return

    print(
        constantes.MSG_TRANSFERENCIA_EXITOSA.format(
            monto=monto_a_transferir,
            nombre_origen=cuentas[dni_origen]["nombre_apellido"],
            nombre_destino=cuentas[dni_destino]["nombre_apellido"],
        )
    )


def otorgar_prestamo(cuentas: dict) -> None:
    """
    Permite otorgar un préstamo a una cuenta existente.
    Solicita DNI, interés (mínimo 5%) y monto (mínimo $100), y valida cada entrada.
    Calcula impuestos (20%) e intereses sobre el capital original.
    Crea el préstamo, lo agrega a la cuenta y actualiza el saldo de la cuenta.

    Pre:
        - `cuentas` es el diccionario de cuentas.
    Post:
        - Si la operación es exitosa:
            - Se crea un nuevo diccionario de préstamo con el formato detallado,
              y se calculan impuestos e intereses (división entera).
            - Este préstamo se añade a la lista "prestamos" de la cuenta.
            - El `saldo_disponible` de la cuenta se incrementa con el monto del préstamo.
            - El `next_prestamo_id` de la cuenta se incrementa.
            - Se imprime `MSG_PRESTAMO_CREADO`.
        - Si el usuario retrocede, el DNI es inválido o no existe, el interés es inválido
          o el monto es inválido:
            - `cuentas` no es modificado.
            - Se imprimen mensajes de error específicos.
            - La función retorna None.
    """
    dni = validaciones.solicitar_dni(cuentas, "Ingrese DNI: ", debe_existir=True)
    if dni is None:
        return

    interes = validaciones.solicitar_interes_minimo("Ingrese interés: ", 5)
    if interes is None:
        return

    monto = validaciones.solicitar_monto_minimo("Ingrese monto: ", 100)
    if monto is None:
        return

    negocio.otorgar_prestamo(cuentas, dni, interes, monto)

    print(
        constantes.MSG_PRESTAMO_CREADO.format(
            nombre=cuentas[dni]["nombre_apellido"],
            balance=cuentas[dni]["saldo_disponible"],
        )
    )


def pagar_prestamo(cuentas: dict) -> None:
    """
    Permite pagar un préstamo pendiente, utilizando el saldo en cuenta.
    Solicita un DNI válido, muestra una lista de préstamos, permite seleccionar uno
    e ingresar el monto a pagar. Descuenta el monto del saldo y resta los pagos pendientes.
    Maneja el orden de pago y sobrepagos.

    Pre:
        - `cuentas` es el diccionario de cuentas.
    Post:
        - Si la operación es exitosa:
            - Se crea el préstamo y se suma el monto al saldo de la cuenta.
            - Se imprime `MSG_PRESTAMO_CREADO` con el nombre y el nuevo saldo.
        - Si el usuario cancela o alguna validación falla (DNI inexistente, interés o monto inválidos):
            - No se realizan cambios en las cuentas.
            - Se muestran mensajes de error informativos.
            - La función retorna None.
    """
    dni = validaciones.solicitar_dni(cuentas, "Ingrese DNI: ", debe_existir=True)
    if dni is None:
        return

    cuenta = cuentas[dni]

    if not validaciones.hay_prestamos_pendientes(cuenta):
        print(constantes.MSG_PRESTAMO_NO_ACTIVO)
        return

    # se muestra el saldo disponible de la cuenta y los préstamos pendientes
    print(constantes.SALDO_DISPONIBLE_TEMPLATE.format(monto=cuenta["saldo_disponible"]))

    prestamo_a_pagar = validaciones.seleccionar_prestamo(cuenta)
    if prestamo_a_pagar is None:
        return

    # se calcula el monto total pendiente del préstamo y se solicita el monto a pagar
    deuda_total_prestamo = validaciones.obtener_deuda_total_valida(prestamo_a_pagar)
    if deuda_total_prestamo is None:
        return

    monto_a_aplicar = validaciones.solicitar_monto_pago(cuenta, deuda_total_prestamo)
    if monto_a_aplicar is None:
        return

    negocio.pagar_prestamo(cuenta, prestamo_a_pagar, monto_a_aplicar)

    print(constantes.MSG_PRESTAMO_PAGADO)


def ver_resumen(cuentas: dict) -> None:
    """
    Muestra el resumen de una cuenta específica.
    Solicita un DNI válido y delega la presentación a `presentacion.mostrar_resumen_cuenta`.

    Pre:
        - `cuentas` es el diccionario de cuentas.
    Post:
        - Si la operación es exitosa (DNI válido y existente):
            - Se llama a `presentacion.mostrar_resumen_cuenta` para imprimir el resumen
              completo de la cuenta en la consola.
        - Si el usuario retrocede, el DNI es inválido o no existe:
            - `cuentas` no es modificado.
            - Se imprimen mensajes de error específicos.
            - La función retorna None.
    """
    dni = validaciones.solicitar_dni(cuentas, "Ingrese DNI: ", debe_existir=True)
    if dni is None:
        return

    cuenta = cuentas[dni]
    presentacion.mostrar_resumen_cuenta(cuenta)
