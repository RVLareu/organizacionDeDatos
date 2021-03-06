# -*- coding: utf-8 -*-
"""Segundo Cuatrimestre de 2019.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GzQS5pnu91tAuB2TezJp3NDhUNDIzkaL

Tokyo Telemessage se encuentra analizando la posibilidad de dar
finalmente de baja su servicio de pager que mantiene desde la década de
1980 . Los pagers son un dispositivo de mensajería que realiza un ‘beep’ al
recibir un mensaje de texto de un número limitado de caracteres. Para
poder enviar un mensaje, uno debe llamar a un número telefónico que
representa al pager dejando el mensaje a una operadora.
Para el analisis se cuenta con dos csv’s: clientes.csv del siguiente formato
(id_pager, numero_telefono, codigo_de_area,
fecha_creacion_cuenta, nombre_cliente, region,
categoria_cliente) y eventos.csv
(año,mes,dia,hora,minutos,segundos, id_pager, mensaje,
numero_origen).
Como parte del análisis se desea responder:

a. ¿Cuál es la región que aún tiene activos la mayor cantidad de
pagers, entendiendo como activo aquellos que recibieron por lo
menos un mensaje en el último mes?

b. ¿Cuál es el porcentaje de pagers activos que solamente reciben
mensajes únicamente de una persona (es decir, siempre desde
el mismo número de origen)?
"""

import pandas as pd

clientes = pd.DataFrame({"id_pager":["A01","B02","A02","C02","A52","A03","A04","B05","A06","C07","A54","A42"],
                         "numero_telefono":[1,2,3,4,5,3,1,2,3,4,5,3],
                         "codigo_de_area":[11,22,33,44,55,11,11,22,33,44,55,11],
                         "nombre_cliente":["A","B","L","K","J","C","A","B","L","K","J","C"],
                         "region":["USA","USA","FRA","GF","FD","GR","USA","USA","FRA","GF","FD","GR"]
                         })

eventos = pd.DataFrame({"mes":["noviembre","noviembre","junio","noviembre","noviembre","enero","noviembre","noviembre"], "id_pager":["A01","B02","A02","C02","A52","A02","A01","B02"],"numero_origen":[2,4,3,8,2,1,2,6]})

#en coumn el id_page

clientes

eventos

"""¿Cuál es la región que aún tiene activos la mayor cantidad de pagers, entendiendo como activo aquellos que recibieron por lo menos un mensaje en el último mes?"""

eventos_ultimo_mes = eventos[eventos["mes"]=="noviembre"]
eventos_ultimo_mes

clientes_activos_ultimo_mes = eventos_ultimo_mes.merge(clientes,how="left")
clientes_activos_ultimo_mes

clientes_activos_ultimo_mes.drop_duplicates("id_pager")["region"].value_counts()

"""¿Cuál es el porcentaje de pagers activos que solamente reciben mensajes únicamente de una persona (es decir, siempre desde el mismo número de origen)?"""

clientes_activos_ultimo_mes=clientes_activos_ultimo_mes[["id_pager","numero_origen"]]
clientes_activos_ultimo_mes = clientes_activos_ultimo_mes.drop_duplicates(["id_pager","numero_origen"])
clientes_activos_ultimo_mes
serie = clientes_activos_ultimo_mes.groupby('id_pager').agg({'numero_origen': 'nunique'})
serie[serie['numero_origen']==1].index

serie = clientes_activos_ultimo_mes["id_pager"].value_counts()
serie = serie[serie == 1]
serie.index