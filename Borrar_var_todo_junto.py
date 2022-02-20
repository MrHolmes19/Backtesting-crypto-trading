from datetime import datetime
from functools import partial
from pprint import pprint
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import graficos_variacion

## ----------------- PARAMETROS DE ENTRADA ------------------- ##  
cripto = "BTC"
frec_velas = "m"
inicio = '01/01/2021 00:00:00'
fin = '01/08/2021 00:00:00'
#fin = '31/12/2021 00:00:00'
valor = "close"
#columnasDeInteres = ['open', 'high', 'low', 'close']
columnasDeInteres = ['close']

    
## ----------------- TRANSFORMACIONES ------------------- ##  

inicio = datetime.strptime(inicio, "%d/%m/%Y %H:%M:%S")
fin = datetime.strptime(fin, "%d/%m/%Y %H:%M:%S")

BBDD = f'Binance_{cripto}USDT_{frec_velas}.csv'
fuente = f'{os.path.dirname(os.path.realpath(__file__))}/{BBDD}'
  
df = pd.read_csv(fuente, index_col=['date'], parse_dates=True)

df = df[columnasDeInteres]

## ----------------- GENERACION DE DATOS ESTADISTICOS --------------------- ##

close = df["close"]
# dif_1min = round(abs(close / close.shift(1) - 1), 4)
# df["dif_1min"] = dif_1min

semestres = [ 
  ["2021-1S", '01/01/2021 00:00:00', '01/06/2021 00:00:00'],
  ["2021-2S", '01/06/2021 00:00:00', '01/01/2022 00:00:00'],
]       
    
periodos = [ 
  ["1min", 2],          
  ["5min", 5],
  ["15min", 15],
  ["30min", 30],
  ["1h", 60],
  ["3h", 180],
  ["6h", 360],
  ["12h", 720],
  ["1d", 1440],
  ["3d", 4320],
  ["7d", 10080],
  ["14d", 20160],
  ["1m", 43200],
  ["2m", 86400],
  ["3m", 129600],
  ["6m", 259200],
] 

list_df_est = []
list_list_df = []
for j, s in enumerate(semestres):
  
  ## Ciclo por cada semestre en estudio
  
  inicio = datetime.strptime(s[1], "%d/%m/%Y %H:%M:%S")
  fin = datetime.strptime(s[2], "%d/%m/%Y %H:%M:%S")
  
  ## Ciclo por cada periodo analizable (velas)
  
  list_est = []
  list_df = []
  for i, p in enumerate(periodos):
    #print("Vuelta N° ", i," - ", p)
    df[f'dif_{p[0]}'] = round(abs(close.rolling(window=p[1]).max()/close.rolling(window=p[1]).min() - 1),4)
    # print(df)
    df2 = df[inicio : fin]
    # print(df2)
    media = df2[f'dif_{p[0]}'].mean().round(4)
    #print("media -->", media)
    mediana = df2[f'dif_{p[0]}'].median()
    #print("mediana -->", mediana)
    max = df2[f'dif_{p[0]}'].max()
    #print("max -->", max)
    min = df2[f'dif_{p[0]}'].min()
    #print("min -->", min)
    moda = df2[f'dif_{p[0]}'].mode()[0]
    #print("moda -->", moda)
    desv_std = df2[f'dif_{p[0]}'].std().round(4)
    #print("desv -->", desv_std)
    rango_probable = [min, round(media + 3 * desv_std, 4)]
    
    dic_est = {"periodo": p[0], "min": min, "max": max, "media":media, "mediana":mediana, "moda":moda,
              "desv_std":desv_std, "rango":rango_probable}
    list_est.append(dic_est)
    list_df.append(df2)
    #print(list_est)
  
  ## Armo dataframe con las estadisticas de cada periodo y lo enlisto por cada semestre  
  df_est = pd.DataFrame.from_dict(list_est)   
  #print(df_est)
  list_df_est.append(df_est)
  #print(list_df_est)
  list_list_df.append(list_df)


## ----------------------- REGISTRO DE DATOS EN XSLS ----------------------- ##
  
## Creo una hoja de excel y en cada ciclo armo una solapa por cada semestre

writer = pd.ExcelWriter('variacion de precios.xlsx', engine = "xlsxwriter")

for i, s in enumerate(semestres):
  # Convierto el dataframe a un objeto de excel

  list_df_est[i].to_excel(writer, sheet_name=f'{s[0]}', index=False, startrow=1, header=False)

  # Genero un objeto Workbook y un Worksheet de xslwriter
  wb = writer.book
  ws = writer.sheets[f'{s[0]}']

  # Defino formato de celdas
  fmt_encabezados = wb.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold':True})
  fmt_gral = wb.add_format({'align': 'center', 'text_wrap': True})
  fmt_porcentaje = wb.add_format({'num_format': '0.0 %', 'align': 'center', 'text_wrap': True})

  # Aplico formatos a las columnas
  ws.set_column('A:A', 20, fmt_gral)
  ws.set_column('B:G', 8.9, fmt_porcentaje)
  ws.set_column('G:H', 12, fmt_gral)
  # Agrego encabezados (Los saqué para poder formatearlos con startrow=1, header=False)
  for col_num, value in enumerate(df_est.columns.values):
    ws.write(0, col_num, value, fmt_encabezados)

writer.save()

## ----------------------- GRAFICOS ESTADISTICOS ----------------------- ##

for i, df_est in enumerate(list_df_est):
  print(semestres[i])
  print(df_est)
  
  for p in df_est.index:
    df_est
    
    lista_graficos = [
      partial(graficos_variacion.lineal_sns, df, vela, media, desv_std),    
      partial(graficos_variacion.caja_y_bigotes, df, vela),
      partial(graficos_variacion.histograma_sns, df, vela, media, mediana, desv_std),
      partial(graficos_variacion.distribucion_acumulada, df, vela, media, mediana, desv_std)
    ]    
  
    graficos_variacion.multiplot(2, 2, f"Gráficos de variación de precios - Velas de {vela}", df, vela, media, mediana, desv_std, semestre, lista_graficos, imprimir = True, guardar=True)
  

# df.to_csv(f"variaciones_por_periodo.csv", encoding='utf-8', index=True)

