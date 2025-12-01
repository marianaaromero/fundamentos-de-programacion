"""
Módulo principal del programa.

Coordina la interacción entre las capas de presentación, operaciones }
y lógica de negocio.
"""

import constantes
import operaciones
import negocio
import presentacion


def main():
    """
    Función principal del programa.

    Post:
    - Crea la estructura principal de la agencia.
    - Muestra un menú de opciones y ejecuta la acción correspondiente según
      la entrada del usuario.
    - Finaliza cuando se elige la opción de salir.
    """
    agencia = negocio.crear_agencia()
    acciones = {
        constantes.OPCION_CARGAR_PELICULAS: operaciones.cargar_peliculas,
        constantes.OPCION_CARGAR_VENTAS: operaciones.cargar_ventas,
        constantes.OPCION_LISTAR_COLAB_DIRECTAS: operaciones.listar_colaboraciones_directas,
        constantes.OPCION_LISTAR_TALENTOS_COMP: operaciones.listar_compatibles,
        constantes.OPCION_LISTAR_TALENTOS_INCOMP: operaciones.listar_incompatibles,
        constantes.OPCION_EXPORTAR_TALENTOS_MAYOR_REC: operaciones.exportar_recaudacion,
    }

    while True:
        opcion_str = presentacion.pedir_opcion_menu()
        if opcion_str == constantes.COMANDO_RETROCEDER:
            print(constantes.OPCION_INVALIDA)
            continue
        try:
            opcion = int(opcion_str)
        except ValueError:
            print(constantes.OPCION_INVALIDA)
            continue

        if opcion in acciones:
            acciones[opcion](agencia)
        elif opcion == constantes.OPCION_SALIR:
            break
        else:
            print(constantes.OPCION_INVALIDA)


if __name__ == "__main__":
    main()
