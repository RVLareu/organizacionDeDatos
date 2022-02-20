# -*- coding: utf-8 -*-
"""Segundo Cuatrimestre de 2018.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e2y4tFGkegVGo74TwKqMMMftXS58Kv5Q

2) (***) Dada la exitosa convocatoria de los Juegos Olímpicos de la Juventud por parte del público, sus organizadores
realizan distintos análisis para planificar las jornadas finales del certamen. Es por ello que cuentan con información en
los siguientes archivos csv:
eventos.csv (id_evento, fecha, id_locacion, nombre_evento, id_categoria_deportiva, cantidad_espectadores)
locacion.csv (id_locacion, nombre, capacidad, capacidad_extendida, sede, latitud, longitud)
categorias_deportivas.csv (id_categoria_deportiva, nombre, año_de_adopcion)
El primer archivo cuenta con información de los eventos, indicando la fecha (en formato “YYYY-mm-dd hh:mm:ss”), el
lugar donde ocurrió (id_locacion) y la cantidad de espectadores que asistieron. Además se aporta información sobre la
categoría deportiva a la cual pertenece el evento.
Por otro lado se tiene información sobre las distintas locaciones en la sedes del certamen en las que ocurrieron los
eventos. Contamos con información de su capacidad total de espectadores así como de su capacidad extendida (cuantos
asientos extras se pueden brindar sobre la capacidad de la locación).
Se desea obtener:

a) Nombre de la sede que acumuló la mayor cantidad de espectadores en eventos durante el certamen del 14 al 15 de
octubre inclusive. Esto es de vital importancia para distribuir el merchandising oficial del evento, para las fechas finales.
(7 pts)

b) Nombre del evento y nombre de la categoría deportiva de aquellos eventos cuya cantidad de espectadores superó la
capacidad de la locación, más allá de la capacidad extendida. Esto es de vital importancia para detectar problemas de
seguridad o si es necesario realizar algún cambio de locación. (8 pts)
"""

import pandas as pd

eventos = pd.DataFrame({"id_evento":["A01","A02","A03","A04","A05"],
                        "fecha":["2020-10-14","2020-10-15","2020-9-14","2020-10-13","2020-10-14"],
                        "id_locacion":["b01","b02","b03","b01","b02"],
                        "nombre_evento":["a","b","c","d","e"],
                        "id_categoria_deportiva":["c01","c02","c03","c01","c03"],
                        "cantidad_espectadores":[12,22,23,17,9]})

categorias_deportivas = pd.DataFrame({"id_categoria_deportiva":["c01","c02","c03","c04"],
                                      "nombre":["aa","ab","ac","ad"],
                                      "año_de_adopcion":[1900,1902,1902,1920]})

locacion = pd.DataFrame({"id_locacion":["b01","b02","b03","b04"],
                          "nombre":["cc","dd","jj","ee"],
                          "capacidad":[10,20,15,8],
                          "capacidad_extendida":[15,24,18,12],
                          "sede":["aj","bj","aj","cj"],
                          "latitud":[1,2,3,4],
                          "longitud":[1,2,3,4]})

"""Nombre de la sede que acumuló la mayor cantidad de espectadores en eventos durante el certamen del 14 al 15 de octubre inclusive. Esto es de vital importancia para distribuir el merchandising oficial del evento, para las fechas finales. """

eventos

categorias_deportivas

locacion

eventos_en_fecha = eventos[((pd.to_datetime(eventos["fecha"]).dt.month == 10)) & ((pd.to_datetime(eventos["fecha"]).dt.day == 14) | (pd.to_datetime(eventos["fecha"]).dt.day == 15))]
eventos_en_fecha

eventos_en_fecha_locacion = eventos_en_fecha.merge(locacion,how="inner")
eventos_en_fecha_locacion

espectadores_por_sede = eventos_en_fecha_locacion.groupby("nombre").agg({"cantidad_espectadores":"sum"})
espectadores_por_sede.reset_index(inplace=True)
espectadores_por_sede.nlargest(1,"cantidad_espectadores")["nombre"]

"""Nombre del evento y nombre de la categoría deportiva de aquellos eventos cuya cantidad de espectadores superó la capacidad de la locación, más allá de la capacidad extendida. Esto es de vital importancia para detectar problemas de seguridad o si es necesario realizar algún cambio de locación. """

locacion_eventos = eventos.merge(locacion,how="inner")
locacion_eventos_colapsada = locacion_eventos[locacion_eventos["cantidad_espectadores"]>locacion_eventos["capacidad_extendida"]]
locacion_eventos_colapsada = locacion_eventos_colapsada[["nombre_evento","id_categoria_deportiva"]]
locacion_eventos_colapsada

locacion_eventos_categoria_colapsada = locacion_eventos_colapsada.merge(categorias_deportivas,how="inner")
locacion_eventos_categoria_colapsada[["nombre_evento","nombre"]]