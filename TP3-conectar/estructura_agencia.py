"""
Estructura de datos de la agencia en el diccionario 'agencia':

agencia = {
    "peliculas": {
        "Sueños de Libertad": {
            "precio": 1200,
            "talentos": ["Ana Torres", "Carlos Ruiz", "María López"]
        },
        "Destino Final": {
            "precio": 1500,
            "talentos": ["Carlos Ruiz", "Federico Díaz"]
        },
        ...
    },

    "ventas": {
        "Sueños de Libertad": 200,
        "Destino Final": 100,
        "Misterio Azul": 150,
        ...
    },

    "talentos": {
        "ana torres": {"carlos ruiz", "maría lópez"},
        "carlos ruiz": {"ana torres", "federico díaz", "maría lópez"},
        "federico díaz": {"carlos ruiz", "maría lópez"},
        ...
    },

    "nombres_originales": {   # primera aparición del nombre
        "ana torres": "Ana Torres",
        "carlos ruiz": "Carlos Ruiz",
        "federico díaz": "Federico Díaz",
        "maría lópez": "María López",
        ...
    }
}

"peliculas": dict con cada película cargada.
    clave = nombre original de la película
    valor = dict con:
        - "precio": precio por entrada
        - "talentos": lista de nombres originales de los talentos que participaron

"ventas": dict que guarda la cantidad de entradas vendidas por película.

"talentos": dict que representa las colaboraciones.
    clave = nombre del talento normalizado (en minúsculas, sin tildes)
    valor = set con los nombres normalizados de sus colaboradores directos.

"nombres_originales": dict que asocia el nombre normalizado al nombre original
    (para mostrarlo correctamente en informes o exportaciones).
"""
