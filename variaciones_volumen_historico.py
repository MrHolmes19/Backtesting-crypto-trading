from datetime import datetime
from functools import partial
from pprint import pprint
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import graficador_generico

## ----------------- PARAMETROS DE ENTRADA ------------------- ##  
cripto = "BTC"
frec_velas = "m"
columna = ['volume']

historico = [
  "2018-2022", 
  '01/01/2018 00:00:00', 
  '01/02/2022 00:00:00'
]       
    
periodos = [ 
  ["1min", 1],  
  ["3min", 3],    
  ["5min", 5],
  ["10min", 10], 
  ["15min", 15],
  ["30min", 30],
  ["1h", 60],
  ["3h", 180],
  ["6h", 360],
  ["12h", 720],
  ["1d", 1440],
  ["3d", 4320],
  ["7d", 10080],
] 
 
## ----------------- GENERACION DE CSV y DF --------------------- ## 

print("Generando Dataframe de volumenes...")

BBDD = f'Binance_{cripto}USDT_{frec_velas}.csv'
fuente = f'{os.path.dirname(os.path.realpath(__file__))}/{BBDD}'
  
df = pd.read_csv(fuente, index_col=['date'], parse_dates=True)
df = df[columna]
df = df[~df.index.duplicated()] #   QUITAR CUANDO SE ARREGLE EL DATASET

volume = df["volume"]
for i, p in enumerate(periodos):
  df[f'dif_vol_{p[0]}'] = round(abs(volume.rolling(window=p[1]).max()/volume.rolling(window=p[1]).min() - 1),4)
  
#print(df)
print("Guardando CSV de variacion de volumen de transacciones...")
df.to_csv(f"variacion volumenes de transacciones.csv", encoding='utf-8', index=True)

print("CSV guardado exitosamente!")

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
  media = df2[f'dif_vol_{p[0]}'].mean().round(4)
  mediana = df2[f'dif_vol_{p[0]}'].median()
  max = df2[f'dif_vol_{p[0]}'].max()
  min = df2[f'dif_vol_{p[0]}'].min()
  moda = df2[f'dif_vol_{p[0]}'].mode()[0]
  desv_std = df2[f'dif_vol_{p[0]}'].std().round(4)
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

writer = pd.ExcelWriter('Variacion en vol de transac. historicos.xlsx', engine = "xlsxwriter")

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
'''
inicio = datetime.strptime(historico[1], "%d/%m/%Y %H:%M:%S")
fin = datetime.strptime(historico[2], "%d/%m/%Y %H:%M:%S")
df2 = df[inicio : fin]
'''
os.chdir(os.path.dirname(os.path.realpath(__file__)))
try:
  os.mkdir(f"Variacion en volumenes de transac historicos")
except:
  pass
os.chdir(f"Variacion en volumenes de transac historicos")

for j, p in enumerate(df_est.index):
  vela = df_est.at[j, "periodo"]
  media = df_est.at[j, "media"]
  mediana = df_est.at[j, "mediana"]
  min = df_est.at[j, "min"]
  max = df_est.at[j, "max"]
  desv_std = df_est.at[j, "media"]      
  
  label = "Variacion Volumen de transacciones"
  
  lista_graficos = [
    partial(graficador_generico.lineal, df2, df2.index, df2[f'dif_vol_{vela}'], 
            label, f"Serie temporal - {vela}",media, desv_std, porcent = True),    
    partial(graficador_generico.caja_y_bigotes,
            df2[f'dif_vol_{vela}'], label, f"Caja y bigotes - {vela}", porcent = True),
    partial(graficador_generico.histograma, df2[f'dif_vol_{vela}'], label, f"Histograma - {vela}", 
            media, mediana, min, max, desv_std, porcent = True),
    partial(graficador_generico.distribucion_acumulada, df2[f'dif_vol_{vela}'], label, 
            f"Distribucion acumulada - {vela}", media, min, max, desv_std, porcent = True)
  ]    
  
  graficador_generico.multiplot(2, 2, 
                                f"Variaciones en Vol. de transacciones - Velas de {vela} - Histórico", 
                                lista_graficos, 
                                imprimir = False, guardar=True)  

