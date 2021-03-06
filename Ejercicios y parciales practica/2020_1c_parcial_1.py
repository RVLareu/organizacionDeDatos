# -*- coding: utf-8 -*-
"""2020_1C_Parcial_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VN3CAqsCjMGLR9NEDYxbrA_JvE8ZynTI

2) Un importante servicio de monitoreo de aplicaciones cloud, sufrió un importante incidente en las últimas semanas por lo cual está conduciendo una investigación. Nuestro equipo participa en el análisis de forma externa para lo cual nos provee los siguientes dataframes en csv:
- metrics.csv describiendo información de métricas obtenidas. El mismo tiene el formato ('client_id', 'integration_id' ,'metric', 'timestamp', 'value') donde la columna ‘metric’ indica el nombre de una métrica que se registra en un cierto momento ('timestamp') cuyo valor se guarda en la columna 'value'.
- clients.csv con información sobre el cliente, con el formato ('client_id, 'account_number', 'name') donde 'account_number' indica el número de cuenta de cliente y 'name' el nombre del mismo.
Como miembro de nuestro equipo es necesario que obtengas las siguientes métricas para aportar insights a nuestro análisis:
-a) Calcular el valor promedio de las metricas 'aws.vpc.network_out', 'aws.vpc.network_in', 'aws.vpc.network_rate' para los clientes de ‘account_number’ mayor al '3' devolviendo el resultado en el siguiente formato (account_number, 'aws.vpc.network_out_mean', 'aws.vpc.network_in_mean', 'aws.vpc.network_rate_mean')(15pts)
-b) Calcular la diferencia entre el valor promedio obtenido en cada métrica por cada cliente, y el valor promedio general de esa métrica (sin utilizar group by) (10pts)
"""

import pandas as pd

metrics = pd.DataFrame({ "client_id":[10,20,30,40,50,60,60,50,40,30,20,10],
           "integration_id":[1,2,3,4,5,6,3,4,2,5,3,1],
           "metric":["aws.vpc.network_out","aws.vpc.network_in","aws.vpc.network_rate","aws.vpc.network_out","aws.vpc.network_in","aws.vpc.network_rate","aws.vpc.network_in","aws.vpc.network_in","aws.vpc.network_out","aws.vpc.network_out","aws.vpc.network_rate","aws.vpc.network_in"],
           "timestamp":["13:05","11:00","04:00","23:00","13:20","14:20","13:50","13:10","13:01","13:11","13:11","17:00"],
           "value":[1,2,3,4,5,6,3,5,2,1,4,6]})
clients = pd.DataFrame({"client_id":[10,20,30,40,50,60],"account_number":[1,2,3,4,5,6],"name":["Ca","Cb","Cc","Cd","Ce","Cf"]})

metrics

clients

clientes_account_mayor = clients[clients["account_number"]>3]
clientes_account_mayor

clientes_mayor_metric = clientes_account_mayor.merge(metrics,how="inner")
clientes_mayor_metric = clientes_mayor_metric[["account_number","metric","value"]]

res = clientes_mayor_metric.groupby(["account_number","metric"]).agg({"value":"mean"})
res = res.unstack()
res.columns = [["aws.vpc.network_in_mean","aws.vpc.network_out_mean","aws.vpc.network_rate_mean"]]
res.reset_index(inplace=True)

res

res = res[["account_number","aws.vpc.network_out_mean","aws.vpc.network_in_mean","aws.vpc.network_rate_mean"]]
res

"""Calcular la diferencia entre el valor promedio obtenido en cada métrica por cada cliente, y el valor promedio general de esa métrica (sin utilizar group by) (10pts)"""

metrics_client_mean = metrics.pivot_table(index="client_id",columns="metric",values="value",aggfunc="mean")
metrics_client_mean.reset_index(inplace=True)

metrics.pivot_table(columns="metric",values="value",aggfunc="mean")
network_in_mean = metrics.pivot_table(columns="metric",values="value",aggfunc="mean")["aws.vpc.network_in"][0]
network_out_mean = metrics.pivot_table(columns="metric",values="value",aggfunc="mean")["aws.vpc.network_out"][0]
network_rate_mean = metrics.pivot_table(columns="metric",values="value",aggfunc="mean")["aws.vpc.network_rate"][0]

metrics_client_mean["net_in_diff"] = metrics_client_mean["aws.vpc.network_in"]-network_in_mean
metrics_client_mean["net_out_diff"] = metrics_client_mean["aws.vpc.network_out"]-network_out_mean
metrics_client_mean["net_rate_diff"] = metrics_client_mean["aws.vpc.network_rate"]-network_rate_mean

metrics_client_mean