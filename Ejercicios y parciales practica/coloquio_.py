# -*- coding: utf-8 -*-
"""Coloquio.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zOiYgRJjV6va4Oue0YkIB6--j9uvGkhF
"""

tests = [("2021-01-15",4000, "l1",0),
         ("2021-01-15",4000, "l1",0),
         ("2021-01-15",4000, "l4",0),
         ("2021-02-15",4000, "l2",1),
         ("2021-02-15",3000, "l2",1),
         ("2021-03-13",5000, "l1",0),
         ("2021-03-15",3000, "l1",0),
         ("2021-03-15",4000, "l3",1),
         ("2021-03-15",5000, "l3",1),
         ("2021-03-15",4000, "l1",0),
         ("2021-03-11",1000, "l4",1),
         ("2021-03-11",5000, "l1",0),
         ("2021-10-12",5000, "l1",0),
         ("2021-02-12",5000, "l5",0)           
         ]

localidades = [("l1","n1","BsAs"),
               ("l2","n2","p2"),
               ("l3","n3","p3"),
               ("l4","n4","BsAs"),
               ("l5","n5","p5")
               ]


testsRdd = sc.parallelize(tests)
localidadesRdd = sc.parallelize(localidades)

"""###a)"""

tests_localidades_primer_trimestre = testsRdd.filter(lambda x: (x[0].split("-")[0]=="2021") & (x[0].split("-")[1] in ["01","02","03"])).cache()

id_localides_bsas = localidadesRdd.filter(lambda x: x[2]=="BsAs").map(lambda x: (x[0],x[2]) )

tests_to_join = tests_localidades_primer_trimestre.map(lambda x: (x[2],x[1]) )

tests_bsas = tests_to_join.join(id_localides_bsas).map(lambda x: (x[1][0],1) ).reduceByKey(lambda x,y: x+y).reduce(lambda x,y: x if x[1]>y[1] else y)[0]
tests_bsas

"""###b)"""

tests_localidades_primer_trimestre_positividad_nula = tests_localidades_primer_trimestre.map(lambda x: (x[2],(1,1)  if x[3] == 1 else (0,1) ) )\
                                                    .reduceByKey(lambda x,y: (x[0]+y[0],x[1]+y[1]) ).filter(lambda x: (x[1][0]==0) )
tests_localidades_primer_trimestre_positividad_nula.map(lambda x: (1,1)).reduceByKey(lambda x,y: x+y).collect()[0][1]

"""###c)"""

from datetime import datetime
def diferencia_entre_fechas(fecha1,fecha2):
    fecha1 = datetime.strptime(fecha1, "%Y-%m-%d")
    fecha2 = datetime.strptime(fecha2, "%Y-%m-%d")

    return abs((fecha2 - fecha1).days)

tests_localidades_primer_trimestre_por_localidad = tests_localidades_primer_trimestre.map(lambda x: (x[2],(x[0],x[3])))

tests_localidades_primer_trimestre_por_localidad.reduceByKey(lambda x,y: (1 if (diferencia_entre_fechas(x[0],y[0])<=2 & (x[0]==1 | y[0]==1) )  else 0 ) )\
                                                                                                              .filter(lambda x: x[1] == 1 ).collect()