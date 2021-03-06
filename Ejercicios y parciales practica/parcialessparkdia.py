# -*- coding: utf-8 -*-
"""ParcialesSparkDia.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/194sEdR-2qs6E98ZD35W_01NH-d-ehaQf
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

spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

"""## Primer Cuatrimestre de 2018. Examen parcial, primera oportunidad.

Nintendo of America (EEUU) tiene
información de ventas de videojuegos
físicas mensuales totalizadas en EEUU
las cuales se realizan en cadenas de
tiendas de videojuegos en el siguiente
RDD: (id_videojuego, id_tienda, mes,
anio, total_ventas_mensuales).

Por otro lado tenemos un RDD con
información de las tiendas y de su
ubicación (id_tienda, direccion, latitud,
longitud, codigo_postal, estado).
Con esta información escribir un
programa en pySpark para obtener la
tienda que realizó menor cantidad de
ventas en el estado de "Georgia" en todo
el año 2017. 
"""

sales = [
    (1, 1, '01', '2017', 500), # sera la minima
    (1, 2, '01', '2017', 500),
    (1, 2, '01', '2017', 500),
    (1, 2, '01', '2017', 500),
    (1, 2, '01', '2017', 500),
    (1, 1, '01', '2016', 500),
    (1, 2, '01', '2016', 500),
    (1, 2, '01', '2016', 500),
    (1, 2, '01', '2016', 500),
    (1, 2, '01', '2016', 500),
    (2, 3, '01', '2017', 500),
    (2, 3, '01', '2017', 500),
    (2, 3, '01', '2017', 500),
    (2, 3, '01', '2017', 500),
    (2, 3, '01', '2017', 500),
    (4, 3, '01', '2017', 500),
    (4, 3, '01', '2017', 500),
    (4, 3, '02', '2017', 500),
    (4, 3, '03', '2017', 500),    

]

stores = [
    (1 , 'address 1', -1, -1, '30002', 'Georgia'),
    (2 , 'address 2', -2, -2, '30003', 'Georgia'),
    (3 , 'address 2', -3, -3, '30004', 'Georgia'),
    (4 , 'address 2', -4, -4, '10119', 'New York')    
]

salesRdd = sc.parallelize(sales)
storesRdd = sc.parallelize(stores)

sales2017 = salesRdd.filter(lambda x: x[3] == "2017")\
            .map(lambda x: (x[1],x[4])).reduceByKey(lambda x,y: x+y)
sales2017.collect()

storesGeorgia = storesRdd.filter(lambda x: x[5] == "Georgia")\
            .map(lambda x: (x[0],x[1]))
storesGeorgia.collect()

sales2017Georgia = sales2017.join(storesGeorgia).map(lambda x: (x[0],x[1][0])).reduce(lambda x,y: x if x[1]<y[1] else y)
sales2017Georgia

"""#Primer Cuatrimestre de 2018. Examen parcial, tercera oportunidad
El GCPD (Gotham City Police Dept) recolecta la información de casos policiales que acontecen en Ciudad Gótica. Esta información se encuentra guardada en un archivo con el siguiente formato: (fecha, id_caso, descripción, estado_caso, categoría, latitud, longitud).

Los posibles estados que puede tener un caso son 1: caso abierto, 2: caso resuelto, 3: cerrado sin resolución. Las fechas se encuentran en el formato YYYY-MM-DD.

Por otro lado el comisionado Gordon guarda un registro detallado sobre en cuáles casos fue activada la batiseñal para pedir ayuda del vigilante, Batman. Esta información se encuentra en un archivo con el siguiente formato (id_caso, respuesta), siendo campo respuesta si la señal tuvo una respuesta positiva (1) o negativa (0) de parte de él. El sector encargado de las estadísticas oficiales del GCPD quiere analizar las siguientes situaciones:

a) Las categorías que hayan incrementado su tasa de resolución en al menos un 10% en el último trimestre, con respecto al trimestre anterior. b) Tasa de participación de Batman por categoría, para los delitos contra la propiedad (que enmarcan las categorías incendio intencional, robo, hurto, y robo de vehículos)
"""

# (fecha, id_caso, descripción, estado_caso, categoría, latitud, longitud).
cases = [("2019-01-01", 1, "case 1", 2, "otro delito", -1, -1), 
         ("2019-06-01", 2, "case 2", 2, "robo", -1, -1),
         ("2019-06-01", 3, "case 2", 3, "robo", -1, -1),         
         ("2019-06-01", 4, "case 2", 1, "robo", -1, -1),         
         ("2019-06-01", 5, "case 2", 2, "robo", -1, -1),
         ("2019-09-01", 6, "case 2", 2, "robo", -1, -1),
         ("2019-09-01", 7, "case 2", 2, "robo", -1, -1),         
         ("2019-09-01", 8, "case 2", 2, "robo", -1, -1),
         ("2019-09-01", 9, "case 2", 2, "robo", -1, -1),
         ("2019-09-01", 10, "case 2", 3, "robo", -1, -1),
         ("2019-09-01", 60, "case 2", 3, "robo", -1, -1),
         ("2019-09-01", 70, "case 2", 3, "robo", -1, -1),         
         ("2019-09-01", 80, "case 2", 1, "robo", -1, -1),
         ("2019-09-01", 90, "case 2", 2, "robo", -1, -1),
         ("2019-09-01", 100, "case 2", 2, "robo", -1, -1),
         ("2019-09-01", 600, "case 2", 2, "robo", -1, -1),
         ("2019-09-01", 700, "case 2", 3, "robo", -1, -1),         
         ("2019-09-01", 800, "case 2", 1, "robo", -1, -1),
         ("2019-09-01", 900, "case 2", 1, "robo", -1, -1),
         ("2019-09-01", 1000, "case 2", 1, "robo", -1, -1),
         ("2019-09-01", 6000, "case 2", 2, "robo", -1, -1),
         ("2019-09-01", 7000, "case 2", 2, "robo", -1, -1),         
         ("2019-09-01", 8000, "case 2", 3, "robo", -1, -1),
         ("2019-09-01", 9000, "case 2", 1, "robo", -1, -1),
         ("2019-09-01", 10000, "case 2", 2, "robo", -1, -1),
         ("2019-06-01", 92, "case 2", 2, "hurto", -1, -1),
         ("2019-06-01", 93, "case 2", 3, "hurto", -1, -1),         
         ("2019-06-01", 94, "case 2", 3, "hurto", -1, -1),         
         ("2019-06-01", 95, "case 2", 3, "hurto", -1, -1),
         ("2019-09-01", 96, "case 2", 2, "hurto", -1, -1),
 
        ]

# (id_caso, respuesta)
batsignal = [(1,1),
         (2,1),
         (3,0),
         (4,0),
         (5,1),
         (6,0),
         (7,1),
         (8,0),
         (9,1),
         (10,0),         
         (60,0),
         (70,1),
         (80,1),
         (90,1),
         (100,1),
         (600,0),
         (700,1),
         (800,0),
         (900,1),
         (1000,1),
         (6000,0),
         (7000,1),
         (8000,0),
         (9000,1),
         (10000,1),
         (92,0),
         (93,0),             
         (94,0),
         (95,0),             
         (96,1)             
        ]

casesRdd = sc.parallelize(cases)
batsignalRdd = sc.parallelize(batsignal)

casesTrim = casesRdd.filter(lambda x: x[0].split("-")[1] == "06" or x[0].split("-")[1] == "09")\
              .map(lambda x: ((x[4],1 if x[0].split("-")[1] == "06" else 0), (1 if x[3] == 2 else 0, 1) )).reduceByKey(lambda x,y: (x[0]+y[0],x[1]+y[1]))
casesTrim.collect()
#[(cat,trimestre),(resuelto,no resuelto)]

casesTrim.map(lambda x: ((x[0][0]),(x[0][1],x[1][1]/x[1][0]))   ).collect()

casesTrim.map(lambda x: ((x[0][0]),(x[0][1],x[1][1]/x[1][0]))   ).collect().reduceByKey(lambda x,y: x[1]/y[1] if (x[0]==1 and y[0]==0) else y[1]/x[1]        ).collect()

"""1) Dado los acontecimientos en USA, deseamos obtener datos que
nos den mayor información sobre las muertes de gente de raza negra
por parte de oficiales de policía.
Para ello, tenemos un csv con información sobre las muertes por
parte de oficiales de policía en USA para 2015 hasta 2017:
(name, date, race, city, state)
Y otro csv con información sobre el porcentaje de pobreza en las
ciudades de USA:
(state, city, poverty_rate)
Se pide:
a) Obtener las 10 ciudades con mayor diferencia entre el porcentaje
de pobreza de la ciudad y el porcentaje de pobreza del estado en el
que se encuentra esa ciudad. Por ejemplo si en la ciudad de Houston
la pobreza es de 15.2 y la pobreza en Texas (el estado donde se
encuentra Houston) es de 11.1, la diferencia es 4.1.(15 pts)
b) Obtener la cantidad de muertes de gente de raza negra por parte
de oficiales de policía, agrupada por estados que compartan el mismo
nivel de pobreza redondeado al entero más cercano. Por ejemplo, si
NJ tiene una pobreza de 10.33, AL una de 20.64 y AZ una de 10.44,
NJ y AZ quedarían juntos representados por el nivel de pobreza de 10
y AL en otro grupo con el nivel 21. La salida debe tener el formato:
(nivel_de_pobreza, total_de_muertes) (15 pts)
Resolver los puntos usando la API de RDDs de PySpark. (30 pts)

"""

muertes = [("Aron","2015-06-01","negro","ciudad1","california"),
           ("ROm","2015-06-01","negro","ciudad2","california"),
           ("Alia","2016-06-01","negro","ciudad3","Georgia"),
           ("TLban","2016-06-01","negro","ciudad4","Georgia"),
           ("Aroonian","2017-06-01","negro","ciudad5","nyc"),
           ("Carlsen","2017-06-01","negro","ciudad6","nyc")
           

]

pobreza = [("californa","ciudad1",15),
           ("californa","ciudad2",25),
           ("Georgia","ciudad3",20),
           ("Georgia","ciudad4",10),
           ("nyc","ciudad5",30),
           ("nyc","ciudad6",12),
           
]

muertesRdd = sc.parallelize(muertes)
pobrezaRdd = sc.parallelize(pobreza)

"""En Mercadodesregulado se registran en un RDD todas las ventas (id_producto,o,
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
          (1,10,100,"Arg",1,2020,"junio",)

]

productos = [
             (1,"titulo1","cat1"),
             (2,"titulo2","cat1"),
             (3,"titulo3","cat2"),
             (4,"titulo4","cat2"),
             (5,"titulo5","cat3"),
             (6,"titulo6","cat3"),
             (7,"titulo7","cat4")

]

"""1) El servicio meteorológico registra datos del
tiempo para todas las ciudades donde posee
una base de medición.
Esta información se encuentra en dos RDD.
En el primero se tiene información de las
bases de medición: (ID_BASE, NOMBRE,
PCIA, CIUDAD, LAT, LON).
El segundo posee información sobre las
mediciones en sí: (TIMESTAMP, ID_BASE,
TEMPERATURA, HUMEDAD, PRESIÓN,
DIRECCIÓN VIENTO, VELOCIDAD VIENTO).
Se desea obtener un reporte para las bases de
la Provincia de Buenos Aires. El mismo debe
informar los ID y nombre de bases de
medición que hayan registrado una variación
de temperatura promedio mensual mayor al
30% en el año 2018 (dada la temperatura
promedio de un mes, esta se debe comparar
con el promedio del mes anterior, para
determinar la variación porcentual).
Resolver utilizando el API de RDD de
PySpark, dando el reporte en un RDD. (***) (
15pts)

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

libros = [(1, "Crónicas marcianas","ciencia ficción", "Ray Bradbury"),
(2, "La vuelta al mundo en ochenta días", "aventura", "Julio Verne")
]

ventas = [(100, 1, 10, "julio", 2020, "13:00:24", 300),
(101, 1, 20, "julio", 2020, "15:04:00", 300),
(102, 2, 23, "julio", 2020, "16:01:01", 250),
(103, 1, 8, "agosto", 2020, "16:22:23", 300),

(104, 1, 12, "agosto", 2020,"17:00:00", 300),
(104, 1, 12, "agosto", 2020,"17:00:00", 300),

(106, 2, 18, "agosto", 2020, "11:02:00", 250),
(107, 2, 19, "agosto", 2020, "11:42:00", 250),
(108, 2, 22, "agosto", 2020, "18:33:00", 250)]

librosRdd = sc.parallelize(libros)
ventasRdd = sc.parallelize(ventas)

ventasAgosto2020 = ventasRdd.filter(lambda x: x[3]=="agosto" and x[4]==2020).map(lambda x: (x[1],1))
ventasAgosto2020.collect()

librosGenero = librosRdd.map(lambda x: (x[0],x[2]))
librosGenero.collect()

ventasGenero = ventasAgosto2020.join(librosGenero).map(lambda x: (x[1][1],x[1][0])).reduceByKey(lambda x,y: x+y).reduce(lambda x,y: x if x[0]>y[0] else y)
ventasGenero



ventasMeses = ventasRdd.filter(lambda x: x[3]=="julio" or x[3]=="agosto").map(lambda x: (x[1],(0,1)) if x[3]=="agosto" else (x[1],(1,0)))
ventasMeses.collect()

diferenciaMesesId = ventasMeses.reduceByKey(lambda x,y: (x[0]+y[0],x[1]+y[1])).map(lambda x: (x[0],x[1][1]-x[1][0]))
diferenciaMesesId.collect()

mayorDiferencia = diferenciaMesesId.reduce(lambda x,y: x if x[1]>y[1] else y)
mayorDiferencia

librosRdd.lookup(mayorDiferencia[0])

"""1) Spotify cuenta con un log de todas las canciones que fueron escuchadas en
su plataforma, esta información se encuentra en un RDD que está
paralelizado por día, es decir cada día es una partición. Los campos del RDD
son los siguientes: (date, user_id, song_id, song_title, artist).
Se cuenta por otro lado con un RDD que asigna "tags" a las canciones, por
ejemplo "rock, punk, actual, top-10, acoustic, etc). Una canción puede tener
asociados "n" tags. El RDD tiene el formato (song_id, tag).
Cada día se corre un proceso para asignar el tag "rising" a las canciones que
se escucharon mas veces el día de hoy que el día de ayer. Estos nuevos tags
pasan a formar parte del RDD de tags para futuros usos. Programar en
PySpark usando el API de RDD lo solicitado. 

"""

escuchas = [
            ("2020-08-01",1,3,"clandestino","Manu Chao"),
            ("2020-08-01",1,5,"esperanza","Manu Chao"),
            ("2020-08-01",2,3,"clandestino","Manu Chao"),
            ("2020-08-01",2,5,"esperanza","Manu Chao"),
            ("2020-08-01",3,3,"clandestino","Manu Chao"),
            ("2020-08-01",3,6,"depende","Jarabe"),
            ("2020-08-01",4,7,"ahora","Anuel"),

            ("2020-08-02",1,3,"clandestino","Manu Chao"),
             ("2020-08-02",1,3,"clandestino","Manu Chao"),
             ("2020-08-02",1,3,"clandestino","Manu Chao"),
            ("2020-08-02",1,5,"esperanza","Manu Chao"),
            ("2020-08-02",2,3,"clandestino","Manu Chao"),
            ("2020-08-02",2,5,"esperanza","Manu Chao"),
            ("2020-08-02",3,3,"clandestino","Manu Chao"),
            ("2020-08-02",2,5,"esperanza","Manu Chao"),
            ("2020-08-02",3,3,"clandestino","Manu Chao"),
            ("2020-08-02",3,6,"depende","Jarabe"),
            ("2020-08-02",4,7,"ahora","Anuel"),
                        ("2020-08-02",4,7,"ahora","Anuel"),
                        ("2020-08-02",4,7,"ahora","Anuel"),
                        ("2020-08-02",4,7,"ahora","Anuel"),
                        ("2020-08-02",4,7,"ahora","Anuel")

]

tags = [
        (3,"viejo,acoustic,reagge,top-10"),
        (5,"viejo,acoustic,reagge"),
        (6,"viejo,acoustic"),
        (7,"trap,actual")

]

escuchasRdd = sc.parallelize(escuchas)
tagsRdd = sc.parallelize(tags)

escuchasConsecutivas = escuchasRdd.filter(lambda x: x[0].split("-")[2] == "01" or x[0].split("-")[2] == "02").map(lambda x: (x[2],(0,1) if  x[0].split("-")[2] == "01" else (1,0))).reduceByKey(lambda x,y: (x[0]+y[0],x[1]+y[1])).filter(lambda x: x[1][0]-x[1][1]>0)
escuchasConsecutivas.collect()

tagsRdd.join(escuchasConsecutivas).map(lambda x: (x[0],x[1][0]+",rising")).collect()