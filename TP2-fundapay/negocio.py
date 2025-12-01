"""
Este módulo contiene la lógica de negocio.
"""

import constantes


def registrar_cuenta(cuentas: dict, nombre: str, dni: str) -> None:
    """
    Crea una cuenta nueva y actualiza `cuentas`.

    Pre:
        - `cuentas` es el diccionario de cuentas.
        - `nombre` es el nombre y apellido del titular.
        - `dni` es un identificador único no repetido en `cuentas`.
    Post:
        - Se agrega una nueva cuenta con saldo inicial 0, sin préstamos ni transferencias.
    """
    nueva_cuenta = {
        "nombre_apellido": nombre,
        "dni": dni,
        "saldo_disponible": 0,
        "next_prestamo_id": 1,
        "prestamos": [],
        "transferencias": [],
    }
    cuentas[dni] = nueva_cuenta


def acreditar_dinero(cuentas: dict, dni: str, monto: int) -> None:
    """
    Acredita un monto en la cuenta indicada.
    Pre:
        - `cuentas` es el diccionario de cuentas.
        - `monto` es un número entero mayor que cero.
    Post:
        - Se incrementa el saldo disponible de la cuenta por el monto recibido.
    """
    cuenta = cuentas[dni]
    cuenta["saldo_disponible"] += monto


def transferir_dinero(cuentas, dni_origen, dni_destino, monto_a_transferir):
    """Realiza la transferencia entre dos cuentas si hay fondos suficientes.

    Pre:
        - `cuentas` es el diccionario de cuentas.
        - `monto_a_transferir` es un entero positivo.
    Post:
        - Si el saldo de la cuenta de origen es suficiente:
            - Se debita el monto en la cuenta de origen y se acredita en la cuenta destino.
            - Se registran las transferencias en ambas cuentas (envío y recepción).
            - Devuelve True.
        - Si el saldo es insuficiente:
            - No se modifican los saldos ni los registros.
            - Devuelve False.
    """

    cuenta_origen = cuentas[dni_origen]
    cuenta_destino = cuentas[dni_destino]

    if cuenta_origen["saldo_disponible"] < monto_a_transferir:
        return False

    cuenta_origen["saldo_disponible"] -= monto_a_transferir
    cuenta_destino["saldo_disponible"] += monto_a_transferir

    transferencia_origen = {
        "monto": monto_a_transferir,
        "tipo": "envia",
        "nombre_contraparte": cuenta_destino["nombre_apellido"],
        "dni_contraparte": dni_destino,
    }
    cuenta_origen["transferencias"].append(transferencia_origen)

    transferencia_destino = {
        "monto": monto_a_transferir,
        "tipo": "recibe",
        "nombre_contraparte": cuenta_origen["nombre_apellido"],
        "dni_contraparte": dni_origen,
    }
    cuenta_destino["transferencias"].append(transferencia_destino)

    return True


def otorgar_prestamo(cuentas, dni, interes, monto):
    """
    Crea un nuevo préstamo para la cuenta indicada, aplicando los impuestos
    e intereses correspondientes.

    Pre:
        - `cuentas` es el diccionario de cuentas.
        - `interes` es un porcentaje entero mayor o igual al mínimo permitido.
        - `monto` es un número entero mayor o igual al mínimo permitido.
    Post:
        - Se calcula el total de impuestos e intereses sobre el monto original.
        - Se crea un nuevo préstamo y se agrega a la lista de préstamos de la cuenta.
        - Se actualiza el saldo disponible con el monto prestado.
    """
    cuenta = cuentas[dni]
    impuestos_calculados = (constantes.IMPUESTOS_PRESTAMO * monto) // 100
    intereses_calculados = (interes * monto) // 100
    siguiente_id = cuenta["next_prestamo_id"]

    nuevo_prestamo = {
        "id_prestamo": siguiente_id,
        "monto_capital_original": monto,
        "tasa_interes": interes,
        "impuestos_total_original": impuestos_calculados,
        "intereses_total_original": intereses_calculados,
        "capital_pendiente": monto,
        "intereses_pendientes": intereses_calculados,
        "impuestos_pendientes": impuestos_calculados,
        "total_pagado_impuestos": 0,
        "total_pagado_intereses": 0,
        "total_pagado_capital": 0,
    }

    cuenta["prestamos"].append(nuevo_prestamo)
    cuenta["next_prestamo_id"] += 1
    cuenta["saldo_disponible"] += monto


def aplicar_pago_a_componente(
    prestamo: dict, monto_restante: int, clave_pendiente: str, clave_pagado: str
) -> int:
    """
    Aplica el monto restante al componente de deuda pendiente e incrementa el monto pagado.

    Pre:
        - `prestamo` es el diccionario de un préstamo.
        - `monto_restante` es el monto restante del pago.
        - `clave_pendiente` la clave del componente de deuda pendiente (interes/impuestos/capital).
        - `clave_pagado` es la clave del componente pagado (interes, impuestos o capital).
    Post:
        - Devuelve el monto restante del pago.
    """

    # se verifica que todavía haya monto disponible del pago y deuda pendiente
    if monto_restante > 0 and prestamo[clave_pendiente] > 0:

        # se calcula lo que se debe pagar de este componente
        pago_aplicado = min(monto_restante, prestamo[clave_pendiente])

        prestamo[clave_pendiente] -= pago_aplicado
        prestamo[clave_pagado] += pago_aplicado

        # se actualiza el monto restante del pago
        monto_restante -= pago_aplicado

    return monto_restante


def distribuir_pago(prestamo: dict, monto: int) -> None:
    """Aplica el pago a los componentes pendientes en orden de prioridad.

    Pre:
        - `prestamo` es el diccionario de un préstamo.
        - `monto` es el monto a distribuir.
    """
    monto_restante = monto

    for clave_pendiente, clave_pagado in constantes.PRIORIDADES_PAGO:
        monto_restante = aplicar_pago_a_componente(
            prestamo, monto_restante, clave_pendiente, clave_pagado
        )

        if monto_restante <= 0:
            break


def pagar_prestamo(cuentas, prestamo_a_pagar, monto_a_aplicar):
    """
    Aplica un pago a un préstamo existente, descontando del saldo de la cuenta.

    Pre:
        - `cuentas` es el diccionario de cuentas.
        - `prestamo_a_pagar` es el préstamo seleccionado dentro de esa cuenta.
        - `monto_a_aplicar` es el monto total que se desea pagar.
    Post:
        - Se descuenta del saldo de la cuenta el monto aplicado.
        - Se distribuye el pago entre impuestos, intereses y capital.
        - Si el monto excede la deuda total, solo se aplica lo necesario para saldarla.
    """
    deuda_total = (
        prestamo_a_pagar["capital_pendiente"]
        + prestamo_a_pagar["intereses_pendientes"]
        + prestamo_a_pagar["impuestos_pendientes"]
    )

    # caso de un monto mayor a la deuda total, solo se aplica lo necesario para saldarla
    monto_restante = min(monto_a_aplicar, deuda_total)
    cuentas["saldo_disponible"] -= monto_restante
    distribuir_pago(prestamo_a_pagar, monto_restante)
