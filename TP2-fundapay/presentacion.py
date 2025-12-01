"""
Este módulo contiene funciones que construyen la interfaz de usuario.
"""

import constantes


def pedir_opcion_menu() -> str:
    """
    Construye el string completo del menú principal y lo usa como prompt para un input().

    Post:
        - Muestra el menú principal de opciones en la consola.
        - Devuelve la entrada del usuario como una cadena de texto.
    """
    menu_str = (
        "1) Crear cuenta\n"
        "2) Ingresar dinero\n"
        "3) Transferir dinero\n"
        "4) Otorgar préstamo\n"
        "5) Pagar préstamo\n"
        "6) Ver resumen\n"
        "7) Salir\n"
        ">>> "
    )
    return input(menu_str)


def mostrar_prestamos_cuenta(cuentas: dict) -> None:
    """
    Muestra todos los préstamos de una cuenta en el formato especificado.

    Pre:
        - `cuentas` es el diccionario de las cuentas.
    Post:
        - Imprime el encabezado `PRESTAMOS_PENDIENTES`.
        - Si hay préstamos, imprime cada uno siguiendo `PRESTAMO_TEMPLATE`,
          y muestra los IDs de préstamo desde 1 y en el orden original de otorgamiento.
    """
    print(constantes.PRESTAMOS_PENDIENTES)

    lista_prestamos = cuentas["prestamos"]

    if not lista_prestamos:
        return

    for i in range(len(lista_prestamos)):
        prestamo = lista_prestamos[i]

        monto_total_original = (
            prestamo["monto_capital_original"]
            + prestamo["intereses_total_original"]
            + prestamo["impuestos_total_original"]
        )
        total_pendiente = (
            prestamo["capital_pendiente"]
            + prestamo["intereses_pendientes"]
            + prestamo["impuestos_pendientes"]
        )

        print(
            constantes.PRESTAMO_TEMPLATE.format(
                id_prestamo=i + 1,
                monto_total=monto_total_original,
                tasa_interes=prestamo["tasa_interes"],
                total_pendiente=total_pendiente,
                total_impuestos=prestamo["impuestos_total_original"],
                total_pagado_impuestos=prestamo["total_pagado_impuestos"],
                total_intereses=prestamo["intereses_total_original"],
                total_pagado_intereses=prestamo["total_pagado_intereses"],
                capital_total=prestamo["monto_capital_original"],
                total_pagado_capital=prestamo["total_pagado_capital"],
            )
        )


def mostrar_resumen_cuenta(cuentas: dict) -> None:
    """
    Muestra el resumen completo de una cuenta, incluyendo nombre, saldo,
    últimas 5 transferencias y todos los préstamos.

    Pre:
        - `cuentas` es el diccionario de las cuentas.
    Post:
        - Imprime el nombre y saldo de la cuenta usando `RESUMEN_TEMPLATE`.
        - Si hay transferencias, imprime las últimas 5 transferencias (enviadas o recibidas)
          desde la más reciente a la más antigua.
        - Si no hay transferencias, solo se imprime el título de la sección de transferencias.
        - Luego, llama a `mostrar_prestamos_cuenta` para imprimir la lista de préstamos.
    """
    print(
        constantes.RESUMEN_TEMPLATE.format(
            nombre=cuentas["nombre_apellido"], saldo=cuentas["saldo_disponible"]
        )
    )

    if cuentas["transferencias"]:
        ultimas_transferencias = cuentas["transferencias"][
            -constantes.TRANSFERENCIAS_A_MOSTRAR :
        ][::-1]
        for transferencia in ultimas_transferencias:
            if transferencia["tipo"] == "recibe":
                print(
                    constantes.TRANSFERENCIA_ENTRANTE_TEMPLATE.format(
                        monto=transferencia["monto"],
                        nombre=transferencia["nombre_contraparte"],
                        dni=transferencia["dni_contraparte"],
                    )
                )
            elif transferencia["tipo"] == "envia":
                print(
                    constantes.TRANSFERENCIA_SALIENTE_TEMPLATE.format(
                        monto=transferencia["monto"],
                        nombre=transferencia["nombre_contraparte"],
                        dni=transferencia["dni_contraparte"],
                    )
                )
    else:
        # RESUMEN_TEMPLATE ya incluye "Últimas 5 transferencias:",
        # por lo que no se necesita un print acá.
        pass

    mostrar_prestamos_cuenta(cuentas)
