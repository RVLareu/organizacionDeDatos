# -*- coding: utf-8 -*-
"""Spark-Parcial 2020-2-1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1flBKoNcy9iE69ToPWfgzKEd58IFE3QAs

# Instalamos e importamos librerías
"""

!pip install pyspark
!pip install -U -q PyDrive
!apt update
!apt install openjdk-8-jdk-headless -qq
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

"""# 2020-02 Parcial

Tenemos un RDD con información de recetas:

(ID_Receta, Nombre, Categoría)

Y otro RDD con los ingredientes de cada receta:

(ID_Receta, Ingrediente, Cantidad_Kg)

Queremos obtener:

* a) Listar todos los ingredientes que aparecen en alguna receta que usa "pollo" indicando en
cuantas recetas el ingrediente y pollo aparecen juntos. El formato de salida es (ingrediente,
cantidad de recetas en que aparece junto con pollo). Por ejemplo, la papa aparece en 10
recetas con pollo, por lo que tendríamos (papa, 10). (50 pts)

* b) Queremos obtener todos los nombres de recetas Mediterráneas que no tengan ni papa ni
pollo entre sus ingredientes.(50 pts)

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

recetasPollo = ingredientesRDD.filter(lambda x: x[1] == 'pollo').map(lambda x: (x[0],x[1]))

recetasPollo.collect()

recetasPollo.join(ingredientesRDD.map(lambda x: (x[0],x[1]))).collect()

ingredientesByReceta = ingredientesRDD.map(lambda x: (x[0],x[1])).cache()

ingredientesConPollo = recetasPollo.join(ingredientesByReceta)\
.filter(lambda x: x[1][1] != 'pollo')

ingredientesConPollo.collect()

ingredientesCount = ingredientesConPollo.map(lambda x: (x[1][1],1)).reduceByKey(lambda x,y:x+y).cache()

ingredientesCount.collect()

ingredientesCount.filter(lambda x: x[1]>1).collect()

"""Punto b"""

mediterraneas = recetasRDD.filter(lambda x:x[2] == 'Mediterranea').map(lambda x: (x[0],x[1]))

mediterraneas.collect()

mediterraneas.join(ingredientesByReceta).collect()

mediterraneas.join(ingredientesByReceta)\
.map(lambda x: (x[0],(1 if x[1][1] in ['pollo','papa'] else 0,x[1][0]))).collect()

mediterraneas.join(ingredientesByReceta)\
.map(lambda x: (x[0],(1 if x[1][1] in ['pollo','papa'] else 0,x[1][0])))\
.reduceByKey(lambda x,y: (x[0]+y[0],x[1])).filter(lambda x: x[1][0] == 0).map(lambda x: x[1][1]).collect()

mediterraneas.join(ingredientesByReceta).map(lambda x: (x[0],1 if x[1][1] in ['pollo','papa'] else 0))\
             .reduceByKey(lambda x,y: x+y).filter(lambda x: x[1] == 0).collect()

mediterraneas.join(ingredientesByReceta).groupByKey().map(lambda x: (x[0],list(x[1]))).collect()

