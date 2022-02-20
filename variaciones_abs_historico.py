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
columnasDeInteres = ['close']

historico = [
  "2018-2022", 
  '01/01/2018 00:00:00', 
  '01/01/2022 00:00:00'
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
 
## ----------------- GENERACION DE DATAFRAME CON VARIACIONES ------------------- ##  

print("Generando Dataframe de variaciones...")

BBDD = f'Binance_{cripto}USDT_{frec_velas}.csv'
fuente = f'{os.path.dirname(os.path.realpath(__file__))}/{BBDD}'
  
df = pd.read_csv(fuente, index_col=['date'], parse_dates=True)
df = df[columnasDeInteres]

close = df["close"]
for i, p in enumerate(periodos):
  df[f'dif_{p[0]}'] = round(abs(close.rolling(window=p[1]).max()/close.rolling(window=p[1]).min() - 1),4)

#print(df)
print("Guardando CSV de variaciones...")
df.to_csv(f"variaciones_abs_historico.csv", encoding='utf-8', index=True)

## ----------------- GENERACION DE DATOS ESTADISTICOS --------------------- ##

print("Generando Datos estadisticos...")    

inicio = datetime.strptime(historico[1], "%d/%m/%Y %H:%M:%S")
fin = datetime.strptime(historico[2], "%d/%m/%Y %H:%M:%S")
df2 = df[inicio : fin]

## Ciclo por cada periodo analizable (velas)  
list_est = []
list_df = []

for i, p in enumerate(periodos):
  vela = p[0]    
  media = df2[f'dif_{vela}'].mean().round(4)
  mediana = df2[f'dif_{vela}'].median()
  max = df2[f'dif_{vela}'].max()
  min = df2[f'dif_{vela}'].min()
  moda = df2[f'dif_{vela}'].mode()[0]
  desv_std = df2[f'dif_{vela}'].std().round(4)
  minimo_probable = round(media - 3 * desv_std, 4) if min < media - 3 * desv_std else min
  maximo_probable = round(media + 3 * desv_std, 4) if max > media + 3 * desv_std else max
  
  dic_est = {"periodo": p[0], "min": min, "max": max, "media":media, "mediana":mediana, "moda":moda,
            "desv_std":desv_std, "max_prob":maximo_probable, "min_prob":minimo_probable}
  list_est.append(dic_est)
  list_df.append(df2)
  #print(list_est)

## Armo dataframe con las estadisticas de cada periodo y lo enlisto por cada semestre  
df_est = pd.DataFrame.from_dict(list_est)   
#print(df_est)


## ----------------------- REGISTRO DE DATOS ESTADISTICOS EN XSLS ----------------------- ##
  
## Creo una hoja de excel y en cada ciclo armo una solapa por cada semestre

writer = pd.ExcelWriter('variacion absoluta de precios historica.xlsx', engine = "xlsxwriter")

# Convierto el dataframe a un objeto de excel

df_est.to_excel(writer, sheet_name=f'{historico[0]}', index=False, startrow=1, header=False)

# Genero un objeto Workbook y un Worksheet de xslwriter
wb = writer.book
ws = writer.sheets[f'{historico[0]}']

# Defino formato de celdas
fmt_encabezados = wb.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold':True})
fmt_gral = wb.add_format({'align': 'center', 'text_wrap': True})
fmt_porcentaje = wb.add_format({'num_format': '0.0 %', 'align': 'center', 'text_wrap': True})

# Aplico formatos a las columnas
ws.set_column('A:A', 20, fmt_gral)
ws.set_column('B:I', 10, fmt_porcentaje)

# Agrego encabezados
for col_num, value in enumerate(df_est.columns.values):
  ws.write(0, col_num, value, fmt_encabezados)

writer.save()

## ----------------------- GRAFICOS ESTADISTICOS ----------------------- ##

## Gráficos de variación de precios por periodo (velas) y por semestre

print("Imprimiendo graficos x 4...")   

inicio = datetime.strptime(historico[1], "%d/%m/%Y %H:%M:%S")
fin = datetime.strptime(historico[2], "%d/%m/%Y %H:%M:%S")
df2 = df[inicio : fin]

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.mkdir(f"Variacion historica (4 graficos)")
os.chdir(f"Variacion historica (4 graficos)")

for j, p in enumerate(df_est.index):
  vela = df_est.at[j, "periodo"]
  media = df_est.at[j, "media"]
  mediana = df_est.at[j, "mediana"]
  min = df_est.at[j, "min"]
  max = df_est.at[j, "max"]
  desv_std = df_est.at[j, "media"]      
  
  lista_graficos = [
    partial(graficos_variacion.lineal_sns, df2, vela, media, desv_std),    
    partial(graficos_variacion.caja_y_bigotes, df2, vela),
    partial(graficos_variacion.histograma_sns, df2, vela, media, mediana, min, max, desv_std),
    partial(graficos_variacion.distribucion_acumulada, df2, vela, media, min, max, desv_std)
  ]    
  
  graficos_variacion.multiplot(2, 2, 
                                f"Variación de precios - Velas de {vela} - Histórico", 
                                lista_graficos, 
                                imprimir = False, guardar=True)  

