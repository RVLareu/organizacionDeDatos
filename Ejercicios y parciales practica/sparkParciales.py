# -*- coding: utf-8 -*-
"""SparkParciales.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vU0ZvGgp88bhANoQ5i5GiK74sVdE29d0

Instalamos e importamos librerías
"""

!pip install pyspark
!pip install -U -q PyDrive
!apt update
!apt install openjdk-8-jdk-headless -qq
#!apt install default-jre
#!apt install default-jdk
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark import SparkContext
from pyspark.sql import SQLContext
import pandas as pd

"""Autenticamos con Google Drive"""

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

"""Creamos el Spark Context"""

# create the Spark Session
spark = SparkSession.builder.getOrCreate()

# create the Spark Context
sc = spark.sparkContext

"""**Ejercicio Modelo de FlatMap, join, ReduceByKey y map**

En este ejercicio queremos programar un sistema que recomiende textos a usuarios en base a sus gustos sobre ciertos términos (palabras).

Se cuenta con un RDD de textos de la forma (docId, texto) donde texto es un string de longitud variable.

Además contamos con un RDD que indica qué términos le gustan o no a cada usuario de la forma (userId, término, score) por ejemplo (23, “calesita”, -2).

Se pide programar en Spark un programa que calcule el score total de cada documento para cada usuario generando un RDD de la forma (userId, docId, score) en donde el score es simplemente la suma de los scores del usuario para los términos que aparecen en el documento.

Puede haber términos en los documentos para los cuales no exista score de algunos usuarios, en estos casos simplemente los consideramos neutros (score=0)
"""

documents = [
    (1, 'pablo honey'),
    (2, 'the bends'),
    (3, 'ok computer'),
    (4, 'kid a'),
    (5, 'amnesiac'),
    (6, 'hail to the thief'),
    (7, 'in rainbows'),
    (8, 'the king of limbs'),
    (9, 'a moon shaped pool')
]

scores = [
    ('thom', 'pablo', 1),
    ('thom', 'honey', 1),
    ('martin', 'pablo', -1),
    ('martin', 'honey', -1),
    ('martin', 'ok', 30),
    ('martin', 'computer', 30)
]

"""Se deben crear los rdd paralelizando la informacion"""

documentsRDD = sc.parallelize(documents)
scoresRDD = sc.parallelize(scores)

"""

*   MAP: transforma RDD de largo N en otro RDD de largo N
*   FLATMAP: transforma RDD de largo N en una colleccion de N collecciones, y luego los resultados en un solo RDD



En este caso uso flatMap para separar las oraciones en palabras y quedarme con cada una y su correspondiente id


"""

palabras = documentsRDD.flatMap(lambda x: [(palabra,x[0]) for palabra in x[1].split(" ")])
palabras.collect()

"""Puntaje por palabra de cada persona


"""

scores_word = scoresRDD.map(lambda x: (x[1],(x[0],x[2])))
scores_word.collect()

"""Tanto en scores_word como en palabras tengo como clave la palabra. Hago un join para que me quede: (palabra,("doc_id",("user_id","puntaje"))). Ahora le pongo el formato (("doc_id","user_id"),"puntaje") -> doc_id u user_id de claves y puntaje de valor. Ahora puedo hacer un reduceByKey y sumar los puntajes por (doc_id,user_id) y finalmente lo presento con el formato que me piden con otro map"""

palabras.join(scores_word).map(lambda x: ((x[1][0],x[1][1][0]),x[1][1][1])).reduceByKey(lambda x,y: x+y)\
.map(lambda x: (x[0][1],x[0][0],x[1])).take(10)

"""**Ejercicio Modelo Filter, map, distinct, reduceByKey, join**

Se tiene información estadística de la temporada regular de todos los jugadores de la NBA en un RDD de tuplas con el siguiente formato: (id_jugador, nombre, promedio_puntos, promedio_asistencias, promedio_robos, promedio_bloqueos, promedio_rebotes, promedio_faltas).

Un analista de la cadena ESPN está trabajando con un RDD que corresponde a la primera ronda de playoffs y que tiene el siguiente formato: (id_jugador, id_partido, timestamp, cantidad_puntos, cantidad_rebotes, cantidad_bloqueos, cantidad_robos, cantidad_asistencias, cantidad_faltas).

En base a estos RDDs se quiere programar en PySpark un programa que genere un RDD con los nombres (sin duplicados) de los jugadores que lograron en algún partido de playoffs una cantidad de asistencias mayor a su promedio histórico.
"""

# usamos para simplificar el formato, que puede obtenerse con un map.
# (id_jugador, nombre, promedio_asistencias)
players_all_time_stats = [
    (1, 'Manu Ginobili', 800),
    (2, 'Kobe Bryant', 100),
    (3, 'Marc Gasol', 25),
    (4, 'James Harden', 1000)]

# usamos para simplificar el formato, que puede obtenerse con un map.
# (id_jugador, id_partido, timestamp, cantidad_asistencias)
scores = [
  (1, 1, 1, 100),
  (1, 1, 3, 100),
  (2, 1, 1, 150),
  (2, 1, 3, 150),
  (3, 2, 2, 50),
  (3, 2, 3, 50),      
  (1, 2, 1, 150),
  (1, 2, 3, 150),
]

players_all_time_stats_rdd = sc.parallelize(players_all_time_stats)
scores_rdd = sc.parallelize(scores)

players_all_time_stats_rdd_wn = players_all_time_stats_rdd.map(lambda x:(x[0],x[2]))

players_all_time_stats_rdd_wn.take(10)

scores_rdd = scores_rdd.map(lambda x: ((x[0],x[1]),(x[3]))).reduceByKey(lambda x,y: x+y)

scores_rdd.take(10)

scores_rdd = scores_rdd.map(lambda x: (x[0][0],(x[0][1],x[1])))

scores_rdd.take(5)

scores_by_player_and_hist =scores_rdd.join(players_all_time_stats_rdd_wn)

scores_by_player_and_hist.take(5)

players_all_time_stats_rdd_wp = players_all_time_stats_rdd.map(lambda x: (x[0],x[1]))
r = scores_by_player_and_hist.filter(lambda x: x[1][1]<x[1][0][1]).join(players_all_time_stats_rdd_wp)

r.map(lambda x: x[1][1]).distinct().take(5)

"""**Ejercicio Modelo groupByKey, join, filter**

Tenemos un RDD con información de recetas:

(ID_Receta, Nombre, Categoría)

Y otro RDD con los ingredientes de cada receta:

(ID_Receta, Ingrediente, Cantidad_Kg)

Queremos obtener:

a) Listar todos los ingredientes que aparecen en alguna receta que usa "pollo" indicando en cuantas recetas el ingrediente y pollo aparecen juntos. El formato de salida es (ingrediente, cantidad de recetas en que aparece junto con pollo). Por ejemplo, la papa aparece en 10 recetas con pollo, por lo que tendríamos (papa, 10). (50 pts)

b) Queremos obtener todos los nombres de recetas Mediterráneas que no tengan ni papa ni pollo entre sus ingredientes.(50 pts)

Resolver los puntos usando la API de RDDs de PySpark.
"""

recetas = [
    (1, 'wok', 'China'),
    (2, 'estofado', 'Italiana'),
    (3, 'tortilla', 'Mediterranea'),
    (4, 'Pollo al horno', 'Mediterranea'),
    (5, 'Ni Pollo ni papa', 'Mediterranea')
]

ingredientes = [
    (1, 'pollo', 0.4),
    (1, 'zanahoria', 0.2),
    (1, 'papa', 0.2),
    (2, 'carne', 1),
    (3, 'papa', 0.5),
    (4, 'pollo', 0.3),
    (4, 'papa', 0.2),
    (4, 'cebolla', 0.1),
    (5, 'carne', 0.1),
    (5, 'sal', 0.01)
]

recetasRDD = sc.parallelize(recetas)
ingredientesRDD = sc.parallelize(ingredientes)

recetasPollo = ingredientesRDD.filter(lambda x: x[1]=="pollo").map(lambda x: (x[0],x[1]))
recetasPollo.collect()

ingredientes_recetasPollo = recetasPollo.join(ingredientesRDD).filter(lambda x: x[1][1]!= "pollo").map(lambda x: (x[1][1],1))

ingredientes_recetasPollo.take(5)

ingredientes_recetasPollo.reduceByKey(lambda x,y: x+y).take(5)

"""PUNTO B"""

recetas_sin_pollo_papa = ingredientesRDD.map(lambda x: (x[0],x[1])).groupByKey().mapValues(tuple).filter(lambda x: (("pollo" not in x[1]) & ("papa" not in x[1])))

recetas_sin_pollo_papa.take(5)

recetas_mediterraneas = recetasRDD.filter(lambda x: x[2]=="Mediterranea").map(lambda x: (x[0],x[1]))
recetas_mediterraneas.collect()

recetas_sin_pollo_papa_mediterranea = recetas_sin_pollo_papa.join(recetas_mediterraneas)

recetas_sin_pollo_papa_mediterranea.collect()

"""**EJERCICIO MODELO**

Spark 2020-2C - 1er Recuperatorio
Se tiene un RDD con la información de libros:
(id_libro, nombre, género, autor)
y otro con las ventas de distintos ejemplares de esos libros.
(id_venta, id_libro, dia_venta, mes_venta, año_venta, hora_venta, precio)

a) Indicar el género con más ventas de agosto de 2020.

b) Para los libros de los 5 géneros más vendidos en agosto de 2020, indicar el nombre del libro

que presenta mayor aumento en el número de ventas con respecto al mes anterior.
Por ejemplo, si se considerara:

(1, Crónicas marcianas, ciencia ficción, Ray Bradbury)

(2, La vuelta al mundo en ochenta días, aventura, Julio Verne)



(100, 1, 10, julio, 2020, 13:00:24, 300)

(101, 1, 20, julio, 2020, 15:04:00, 300)

(102, 2, 23, julio, 2020, 16:01:01, 250)

(103, 1, 8, agosto, 2020, 16:22:23, 300)

(104, 1, 12, agosto, 2020, 17:00:00, 300)

(105, 1, 12, agosto, 2020, 17:07:07, 300)

(106, 2, 18, agosto, 2020, 11:02:00, 250)

(107, 2, 19, agosto, 2020, 11:42:00, 250)

(108, 2, 22, agosto, 2020, 18:33:00, 250)


El libro que más aumentó sus ventas es “La vuelta al mundo en ochenta días”, ya que tuvo un
aumento de 2 frente al aumento de 1 de “Crónicas marcianas”.
Resolver los siguientes puntos usando la API de RDDs de PySpark.
Para ambos casos, asumir que no hay “empates” al buscar el máximo (no hay más de un género
con máxima cantidad de ventas en agosto, ni más uno con máxima diferencia de ventas con el
mes anterior).
"""

libros = [(1, "Crónicas marcianas","ciencia ficción","Ray Bradbury"),
           (2, "La vuelta al mundo en ochenta días","aventura", "Julio Verne"),
           (3, "Libro de accion","accion", "Jorge Cortazar")]
ventas = [(100, 1, 10, "julio", 2020, "13:00:24", 300),
(116, 3, 22,"julio", 2020, "18:33:00", 150),
(117, 3, 22,"julio", 2020, "18:33:00", 150),
(101, 1, 20,"julio", 2020, "15:04:00", 300),
(102, 2, 23,"julio", 2020, "16:01:01", 250),
(103, 1, 8,"agosto", 2020, "16:22:23", 300),
(104, 1, 12,"agosto", 2020,"17:00:00", 300),
(105, 1, 12,"agosto", 2020, "17:07:07", 300),
(106, 2, 18,"agosto", 2020, "11:02:00", 250),
(107, 2, 19,"agosto", 2020, "11:42:00", 250),
(109, 2, 19,"agosto", 2020, "11:42:00", 250),
(110, 3, 22,"agosto", 2020, "18:33:00", 150),
(111, 3, 22,"agosto", 2020, "18:33:00", 150),
(112, 3, 22,"agosto", 2020, "18:33:00", 150),
(113, 3, 22,"agosto", 2020, "18:33:00", 150),
(114, 3, 22,"agosto", 2020, "18:33:00", 150),
(115, 3, 22,"agosto", 2020, "18:33:00", 150)]


librosRDD = sc.parallelize(libros)
ventasRDD = sc.parallelize(ventas)

ventas_agosto_2020 = ventasRDD.filter(lambda x: ((x[3]=="agosto") & (x[4]==2020))).map(lambda x: (x[1],1))

ventas_agosto_2020.collect()

ventas_por_libro_agosto_2020 = ventas_agosto_2020.reduceByKey(lambda x,y: x+y)

ventas_por_libro_agosto_2020.collect()

libros_genero = librosRDD.map(lambda x: (x[0],(x[1],x[2])))

libros_genero.collect()

ventas_genero_libro = ventas_por_libro_agosto_2020.join(libros_genero).map(lambda x: x[1])
ventas_genero_libro.collect()

genero_mas_vendido = ventas_genero_libro.reduce(lambda x,y: x if x[0]>y[0] else y)
genero_mas_vendido

genero_mas_vendido[1][1]

"""Punto B"""

generos_mas_vendidos = sc.parallelize(ventas_genero_libro.sortByKey(ascending=False).map(lambda x: (x[1][1],(x[1][0],x[0]))).take(2))
generos_mas_vendidos.collect()

libros_genero = librosRDD.map(lambda x: (x[2],x[0]))
libros_genero.collect()

libros_id_ventas_agosto = generos_mas_vendidos.join(libros_genero).map(lambda x: (x[1][1],(x[1][0][0],x[1][0][1])))
libros_id_ventas_agosto.collect()

ventas_libro_julio = ventasRDD.filter(lambda x: ((x[3]=="julio") & (x[4]==2020))).map(lambda x: (x[1],1))
ventas_por_libro_julio_2020 = ventas_libro_julio.reduceByKey(lambda x,y: x+y)
ventas_por_libro_julio_2020.collect()

ventas_libro_por_mes =  libros_id_ventas_agosto.fullOuterJoin(ventas_por_libro_julio_2020).filter(lambda x: x[1][0] != None)
ventas_libro_por_mes.collect()

ventas_contra_mes_anterior = ventas_libro_por_mes.map(lambda x: (x[1][0][0],(x[1][0][1]/x[1][1] if x[1][1] != None else x[1][0][1])))
ventas_contra_mes_anterior.collect()

libro_con_mayor_aumento = ventas_contra_mes_anterior.reduce(lambda x,y: x if x[1]>y[1] else y)
libro_con_mayor_aumento

"""1) Dado los acontecimientos en USA, deseamos obtener datos que nos den mayor información sobre las muertes de personas de raza negra por parte de oficiales de policía.
Para ello, tenemos un csv con información sobre las muertes por parte de oficiales de policía en USA desde 2015 hasta 2017: 

(name, date, race, city, state)

Y otro csv con información sobre el porcentaje de cada raza en las ciudades de USA: 

(state, city, share_white, share_black, share_native_american, share_asian, share_hispanic)

Se pide:

a) Obtener el estado con mayor porcentaje de muertes de personas de raza negra teniendo en cuenta la cantidad total de muertes por parte de oficiales en ese estado. (10 pts)

b) Obtener los 10 estados con mayor diferencia entre el porcentaje de muertes y el porcentaje de gente de raza negra en ese estado. Para ello, considerar el porcentaje de raza de un estado como el promedio de los valores de sus ciudades.  Por ejemplo si en Texas el porcentaje de muertes de personas de raza negra por parte de la policía es del 36% y el promedio de share_black para Texas es 24% la diferencia es 0.12. (15 pts)
Resolver ambos puntos usando la API de RDDs de PySpark. 

"""

muertes = [("N1","18-10-2016","white","C1","S1"),
            ("N2","18-11-2016","black","C1","S1"),
            ("N3","18-10-2016","white","C4","S1"),
            ("N4","18-10-2017","asian","C1","S1"),
            ("N5","18-10-2017","white","C5","S2"),
            ("N6","19-10-2017","black","C3","S3"),
            ("N7","18-10-2016","black","C1","S1"),
            ("N8","15-10-2016","black","C3","S3"),
            ("N9","12-10-2016","black","C6","S3"),
            ("N10","18-10-2017","american","C8","S5")        
 ]

 razas = [("S1","C1",0.20,0.50,0.10,0.10,0.10),
          ("S1","C4",0.50,0.20,0.10,0.10,0.10),
          ("S2","C5",0.10,0.20,0.50,0.10,0.10),
          ("S3","C3",0.20,0.10,0.10,0.10,0.50),
          ("S3","C6",0.20,0.15,0.45,0.10,0.10),
          ("S3","C11",0.20,0.30,0.30,0.10,0.10),
          ("S5","C8",0.20,0.20,0.30,0.10,0.10),
          ("S5","C10",0.25,0.45,0.15,0.5,0.10),
          ("S9","C8",0.20,0.50,0.10,0.10,0.10),
          
 ]

 muertesRDD = sc.parallelize(muertes)
 razasRDD = sc.parallelize(razas)

muertes_estado = muertesRDD.map(lambda x: (x[4],x[4]))
muertes_totales_por_estado = muertes_estado.groupByKey().mapValues(len)
muertes_totales_por_estado.collect()

muertes_negras_por_estado = muertesRDD.filter(lambda x: x[2]=="black").map(lambda x: (x[4],1)).reduceByKey(lambda x,y: x + y)
muertes_negras_por_estado.collect()

muertes_negras_totales_estado = muertes_totales_por_estado.join(muertes_negras_por_estado)
muertes_negras_totales_estado.collect()

muertes_negras_totales_estado_porcentaje = muertes_negras_totales_estado.map(lambda x: (x[1][1]/x[1][0],x[0]))
muertes_negras_totales_estado_porcentaje.collect()

estado_mas_muertes_negras_porcentaje = muertes_negras_totales_estado_porcentaje.reduce(lambda x,y: x if x[0]>y[0] else y)
estado_mas_muertes_negras_porcentaje[1]

"""PUNTO B"""

porcentaje_negra_estado = razasRDD.map(lambda x: (x[0],x[3]))
porcentaje_negra_estado.collect()

porcentaje_negra_estado = porcentaje_negra_estado.reduceByKey(lambda x,y: x+y)
porcentaje_negra_estado.collect()

ciudades_por_estado = razasRDD.map(lambda x: (x[0],1)).reduceByKey(lambda x,y: x+y)
ciudades_por_estado.collect()

porcentaje_negra_estado = porcentaje_negra_estado.join(ciudades_por_estado).map(lambda x: (x[0],x[1][0]/x[1][1]))
porcentaje_negra_estado.collect()

muertes_negras_totales_estado_porcentaje.map(lambda x: (x[1],x[0])).join(porcentaje_negra_estado).map(lambda x: (x[0],x[1][0]-x[1][1])).max()

"""**EJERCICIO PARCIAL**

1) En Mercadodesregulado se registran en un RDD todas las ventas (id_producto,o,
id_comprador, id_vendedor, pais, tiene_reclamo, año, mes, precio_local) y uno de
productos (id_producto, titulo, categoria).
Mercadodesregulado tiene una muy buena relación con el gobierno argentino y el INDEC
pidió su ayuda para medir la inflación entre diciembre de 2018 y diciembre de 2019. Para
esto se quiere conocer:

a) El precio promedio para cada producto de categoría “smartphone” vendido en
diciembre de 2018 y diciembre de 2019 en argentina (10 ptos)

b) El promedio de la relación entre el precio de los productos (siempre para la categoría
smartphone) que se vendieron en diciembre de 2018 y después en diciembre de 2019 en
argentina. La relación puede calcularse como promedio_dic_2019 / promedio_dic_2018
para cada uno de los product_ids. Luego se pide el promedio de las relaciones (20 ptos)

Un ejemplo de ambos puntos para los siguientes datos:

[(1,10,25,"AR",0,2018,"Diciembre",10000),

(1,45,27,"AR",0,2018,"Diciembre",11000),

(1,21,25,"AR",0,2019,"Diciembre",25000),

(2,78,26,"AR",1,2018,"Diciembre",30000),

(2,31,26,"AR",1,2019,"Diciembre",50000),

(3,103,14,"AR",0,2018,"Diciembre",40000),

(3,542,54,"BR",0,2019,"Diciembre",42000)]

Para el punto a)

Promedio diciembre 2018:

(1, 10500)

(2, 30000)

(3, 40000)

Promedio diciembre 2019:

(1, 25000)

(2, 50000)

Para el punto b)

((25000/10500)+(50000/30000))/2 = 2.02...

Resolver los puntos usando la API de RDDs de PySpark. (30 pts)
"""

ventas = [
             (1,10,25,"AR",0,2018,"Diciembre",10000),
              (2,45,27,"AR",0,2018,"Diciembre",11000),
              (1,21,25,"AR",0,2019,"Diciembre",25000),
              (2,78,26,"AR",1,2018,"Diciembre",30000),
              (2,31,26,"AR",1,2019,"Diciembre",50000),
              (3,103,14,"AR",0,2018,"Diciembre",40000),
              (3,542,54,"BR",0,2019,"Diciembre",42000)
]

productos =[
            (1,"a","smartphone"),
            (2,"b","tv"),
            (4,"c","food"),
            (3,"d","smartphone")
]

ventasRDD = sc.parallelize(ventas)
productosRDD = sc.parallelize(productos)

id_smarthone = productosRDD.filter(lambda x: x[2]=="smartphone").map(lambda x: (x[0],x[2]))
id_smarthone.collect()

ventas_diciembre_2018 = ventasRDD.filter(lambda x: ((x[6]=="Diciembre") & (x[5]==2018))).map(lambda x: (x[0],x[7]))
ventas_diciembre_2018.collect()

ventas_diciembre_2019 = ventasRDD.filter(lambda x: ((x[6]=="Diciembre") & (x[5]==2019))).map(lambda x: (x[0],x[7]))
ventas_diciembre_2019.collect()

ventas_diciembre_2018_smartphone = ventas_diciembre_2018.join(id_smarthone).map(lambda x: (x[0],x[1][0]))
ventas_diciembre_2018_smartphone.collect()

ventas_diciembre_2019_smartphone = ventas_diciembre_2019.join(id_smarthone).map(lambda x: (x[0],x[1][0]))
ventas_diciembre_2019_smartphone.collect()

promedio_diciembre_2018 = ventas_diciembre_2018_smartphone.map(lambda x: (x[0],(x[1],1))).reduceByKey(lambda x,y: (x[0]+y[0],x[1]+y[1])).reduce(lambda x,y: (x[1][0]+y[1][0],x[1][1]+y[1][1]))
promedio_diciembre_2018 = promedio_diciembre_2018[0]/promedio_diciembre_2018[1]
promedio_diciembre_2018

promedio_diciembre_2019 = ventas_diciembre_2019_smartphone.map(lambda x: (x[0],(x[1],1))).reduceByKey(lambda x,y: (x[0]+y[0],x[1]+y[1])).reduce(lambda x,y: (x[1][0]+y[1][0],x[1][1]+y[1][1]))
promedio_diciembre_2019 = promedio_diciembre_2019[0]/promedio_diciembre_2019[1]
promedio_diciembre_2019

"""PUNTO B"""

relacion_entre_productos_2018_2019 = ventas_diciembre_2019_smartphone.join(ventas_diciembre_2018_smartphone).map(lambda x: ((x[1][0])/(x[1][1]),1))
relacion_entre_productos_2018_2019.collect()

relacion_entre_productos_2018_2019_promedio = relacion_entre_productos_2018_2019.reduce(lambda x,y: (x[0]+y[0],x[1]+y[1]))
promedio_relacion = relacion_entre_productos_2018_2019_promedio[0]/relacion_entre_productos_2018_2019_promedio[1]
promedio_relacion