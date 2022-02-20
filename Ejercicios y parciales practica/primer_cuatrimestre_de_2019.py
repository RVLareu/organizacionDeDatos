# -*- coding: utf-8 -*-
"""Primer Cuatrimestre de 2019.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rJ60l1ajhqsJWHiXfail5L4oFgdPMPQi

Un importante broker de compra y venta de vehiculos online se encuentra dando sus primeros
pasos en la preparación de su algoritmo de pricing, es por eso que se encuentra generando
algunos features iniciales para experimentar con distintos algoritmos de machine learning.
Para ello cuenta con un archivo con información de todas las transacciones que tuvo en su primer
año de operación en el formato (transaction_id, timestamp, vehicle_model_id,
price).
Por otro lado cuenta con información que fue extrayendo a partir de scrapping durante el último
año en el formato (timestamp, source, vehicle_model_id, price). La información
puede venir de múltiples fuentes (source), que pueden ser por ejemplo distintos sitios de
marketplace o clasificados.
Luego de un intenso trabajo previo ha podido unificar los modelos de vehículos que utiliza para
sus transacciones con la información que ha podido obtener de otros competidores mediante
scrapping. Muchos de los modelos disponibles en la información de scrapping no han sido aún
comercializados por la empresa, pero se sabe que se cuenta con precios scrapeados de todos los
modelos que se vendieron.
Se pide generar utilizando Pandas un dataframe que tenga el siguiente formato
(vehicle_model_id, ext_mean_price, ext_std_price, int_mean_price,
int_std_price), siendo:
- mean_price: precio promedio para ese vehículo.
- std_price: desvío estándar del precio para ese vehículo.
y los prefijo ext_ y int_ indicando que deben ser calculado sobre respectivamente datos
externos (los obtenido vía scraping) y datos internos (los de las transacciones). (***) (15pts)
"""

import pandas as pd

transacciones = pd.DataFrame({"transaction_id":["A01","A02","A03","A04","A05","A06"],
                              "timestamp":["18:20","18:30","18:31","18:34","18:38","18:39"],
                              "vehicle_model_id":["AA","BB","CC","CC","AA","BB"],
                              "price":[1,2,3,4,5,6]})
scrapping = pd.DataFrame({"timestamp":["19:20","19:30","19:31","19:34","19:38","19:39","19:38","19:39"],
                          "source":["a","b","c","b","c","c","a","b"],
                          "vehicle_model_id":["AA","BB","DD","KK","AA","BB","AA","BB"],
                          "price":[1,2,3,8,5,9,3,5]})

scrapping

"""(vehicle_model_id, ext_mean_price, ext_std_price, int_mean_price, int_std_price)"""

statistics = pd.DataFrame({})
#statistics para el int
grouped_int = transacciones.groupby("vehicle_model_id").agg({"price":["mean","std"]})
grouped_int.reset_index(inplace=True)
grouped_int.columns = [["vehicle_model_id","int_mean_price","int_std_price"]]
statistics = grouped_int
statistics

grouped_ext = scrapping.groupby("vehicle_model_id").agg({"price":["mean","std"]})
grouped_ext.reset_index(inplace=True)
grouped_ext.columns = [["vehicle_model_id","ext_mean_price","ext_std_price"]]
grouped_ext

statistics = statistics.merge(grouped_ext,how="outer")
statistics