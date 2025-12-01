"""
Este módulo contiene las constantes que se usan en el programa.
"""

MSG_INPUT_INVALIDO = "Input inválido"
MSG_FIN = "Finalizando..."
MSG_CUENTA_CREADA = "Cuenta creada correctamente"
MSG_DNI_INVALIDO = "Formato de DNI incorrecto"
MSG_CUENTA_EXISTE = "Ya existe una cuenta con ese DNI: {nombre}"
MSG_PRESTAMO_PAGADO = "Préstamo pagado correctamente"
MSG_PRESTAMO_CREADO = (
    "Préstamo acreditado correctamente. "
    "El balance de la cuenta de {nombre} es de ${balance}"
)
MSG_MONTO_NO_DISPONIBLE = "Monto no disponible en la cuenta de origen"
MSG_TRANSFERENCIA_EXITOSA = (
    "Los ${monto} fueron transferidos desde la cuenta de {nombre_origen} "
    "a la de {nombre_destino} correctamente"
)
MSG_MONTO_INVALIDO = "Monto inválido"
MSG_INGRESO_ACREDITADO = (
    "Los ${monto} fueron acreditados en la cuenta de {nombre} correctamente"
)
MSG_PRESTAMO_NO_ACTIVO = "No hay préstamos activos"
MSG_NO_CUENTAS_DISPONIBLES = "No hay cuentas disponibles"
MSG_SALDO_INSUFICIENTE = "Saldo insuficiente"
MSG_TASA_INTERES_INVALIDA = "La tasa de interés debe ser de al menos 5%"
MSG_NOMBRE_INVALIDO = "Formato de nombre y apellido incorrecto"
MSG_NO_EXISTE_CUENTA = "No existe cuenta con ese DNI"
MSG_SELECCION_INVALIDA = "Selección inválida"

PRESTAMO_TEMPLATE = """{id_prestamo}) Monto total: ${monto_total}
Interés: {tasa_interes}%
Total pendiente de pago: ${total_pendiente}
- Impuestos: ${total_impuestos} (pagado ${total_pagado_impuestos})
- Intereses: ${total_intereses} (pagado ${total_pagado_intereses})
- Capital: ${capital_total} (pagado ${total_pagado_capital})"""

SALDO_DISPONIBLE_TEMPLATE = """Saldo disponible: ${monto}"""
PRESTAMOS_PENDIENTES = """Préstamos:"""

RESUMEN_TEMPLATE = """Nombre: {nombre}
Saldo: {saldo}
Últimas 5 transferencias:"""

TRANSFERENCIA_ENTRANTE_TEMPLATE = "- Recibe ${monto} de {nombre} (DNI {dni})"
TRANSFERENCIA_SALIENTE_TEMPLATE = "- Envía ${monto} a {nombre} (DNI {dni})"

COMANDO_RETROCEDER = "**"

PRIORIDADES_PAGO = [
    ("impuestos_pendientes", "total_pagado_impuestos"),
    ("intereses_pendientes", "total_pagado_intereses"),
    ("capital_pendiente", "total_pagado_capital"),
]

OPCION_CREAR_CUENTA = 1
OPCION_INGRESAR_DINERO = 2
OPCION_TRANSFERIR_DINERO = 3
OPCION_OTORGAR_PRESTAMO = 4
OPCION_PAGAR_PRESTAMO = 5
OPCION_VER_RESUMEN = 6
OPCION_SALIR = 7

IMPUESTOS_PRESTAMO = 20

TRANSFERENCIAS_A_MOSTRAR = 5
