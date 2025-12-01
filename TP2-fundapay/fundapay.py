"""
Este módulo contiene la función principal `main()` que gestiona el flujo
de FundaPay. Incluye el menú principal y la lógica para dirigir a las diferentes funcionalidades
según la opción seleccionada por el usuario.
"""

import presentacion
import constantes
import operaciones


def main():
    """
    Gestiona el menú principal, captura y valida la entrada del usuario,
    y dirige la ejecución a la funcionalidad seleccionada.
    El programa se ejecuta en un bucle interactivo hasta que el usuario elige la opción "Salir".

    Pre:
        - El entorno Python está configurado correctamente.
        - Los módulos `presentacion`, `operaciones` y `constantes` existen y son accesibles.
    Post:
        - Muestra el menú principal y solicita una opción al usuario.
        - Se crea un diccionario `cuentas` vacío.
        - Si se elige una opción inválida o se ingresa el COMANDO_RETROCEDER,
          se imprime `MSG_INPUT_INVALIDO` y se vuelve a mostrar el menú.
        - Si la opción seleccionada está en el diccionario de acciones (1 a 6),
          se llama a la función correspondiente en `operaciones`.
        - Si se elige la opción 7, se imprime `MSG_FIN` y el programa termina.
    """
    cuentas = {}

    acciones = {
        constantes.OPCION_CREAR_CUENTA: operaciones.crear_cuenta,
        constantes.OPCION_INGRESAR_DINERO: operaciones.ingresar_dinero,
        constantes.OPCION_TRANSFERIR_DINERO: operaciones.transferir_dinero,
        constantes.OPCION_OTORGAR_PRESTAMO: operaciones.otorgar_prestamo,
        constantes.OPCION_PAGAR_PRESTAMO: operaciones.pagar_prestamo,
        constantes.OPCION_VER_RESUMEN: operaciones.ver_resumen,
    }

    while True:
        opcion_str = presentacion.pedir_opcion_menu()

        if opcion_str == constantes.COMANDO_RETROCEDER:
            print(constantes.MSG_INPUT_INVALIDO)
            continue

        try:
            opcion = int(opcion_str)
        except ValueError:
            print(constantes.MSG_INPUT_INVALIDO)
            continue

        # si la opción existe en el diccionario, ejecutar la función correspondiente
        if opcion in acciones:
            acciones[opcion](cuentas)
        elif opcion == constantes.OPCION_SALIR:
            print(constantes.MSG_FIN)
            break
        else:
            print(constantes.MSG_INPUT_INVALIDO)


if __name__ == "__main__":
    main()
