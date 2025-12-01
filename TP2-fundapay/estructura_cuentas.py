"""
Estructura de datos de una cuenta en el diccionario `cuentas`:

    "12.345.678": {
        "nombre_apellido": "Pepe Pepito",
        "dni": "12.345.678",
        "saldo_disponible": 1500,
        "next_prestamo_id": 3,
        "prestamos": [
            {
                "id_prestamo": 2,
                "monto_capital_original": 1400, # monto original del préstamo
                "tasa_interes": 15,
                "impuestos_total_original": 280, # 20% del monto original
                "intereses_total_original": 210, # 15% del monto original
                "capital_pendiente": 1300,
                "intereses_pendientes": 0,
                "impuestos_pendientes": 0,
                "total_pagado_impuestos": 280,
                "total_pagado_intereses": 210,
                "total_pagado_capital": 100,
            }
        ],
        "transferencias": [
            {
                "monto": 500,
                "tipo": "recibe", # puede ser "envia" o "recibe"
                "nombre_contraparte": "Pepe Pepito Jr", # nombre de la cuenta contraria
                "dni_contraparte": "23.456.789",
            }
        ]
    }
"""
