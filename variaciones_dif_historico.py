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

diferencias = [
  ["Diferencias alcistas","+"],
  ["Diferencias bajistas","-"]
  ]

historico = [
  "2018-2021", 
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
  df[f'dif_+{p[0]}'] = round(abs(close.rolling(window=p[1]).max()/close.shift(p[1]-1) - 1),5)
  df[f'dif_-{p[0]}'] = round(abs(close.rolling(window=p[1]).min()/close.shift(p[1]-1) - 1),5)
  
df.replace(0, np.nan, inplace=True)  
#print(df)
print("Guardando CSV de variaciones...")
df.to_csv(f"variaciones_dif_historico.csv", encoding='utf-8', index=True)
print("CSV guardado exitosamente!")


## ----------------- GENERACION DE DATOS ESTADISTICOS --------------------- ##

print("Generando Datos estadisticos...")    

## Ciclo por cada tipo de diferencias

list_df_est = []

for j, s in enumerate(diferencias):
    
  signo = s[1]

  ## Ciclo por cada periodo analizable (velas)  
  list_est = []
  list_df = []
  
  for i, p in enumerate(periodos):
    vela = p[0]    
    media = df[f'dif_{signo}{vela}'].mean().round(4)
    mediana = df[f'dif_{signo}{vela}'].median()
    max = df[f'dif_{signo}{vela}'].max()
    min = df[f'dif_{signo}{vela}'].min()
    moda = df[f'dif_{signo}{vela}'].mode()[0]
    desv_std = df[f'dif_{signo}{vela}'].std().round(4)
    minimo_probable = round(media - 3 * desv_std, 4) if min < media - 3 * desv_std else min
    maximo_probable = round(media + 3 * desv_std, 4) if max > media + 3 * desv_std else max
    
    dic_est = {"periodo": p[0], "min": min, "max": max, "media":media, "mediana":mediana, "moda":moda,
              "desv_std":desv_std, "max_prob":maximo_probable, "min_prob":minimo_probable}
    list_est.append(dic_est)
    list_df.append(df)
    #print(list_est)
  
  ## Armo dataframe con las estadisticas de cada periodo y lo enlisto por cada tipo de diferencia  
  df_est = pd.DataFrame.from_dict(list_est)   
  #print(df_est)
  list_df_est.append(df_est)
  #print(list_df_est)  

## ----------------------- REGISTRO DE DATOS ESTADISTICOS EN XSLS ----------------------- ##
  
## Creo una hoja de excel y en cada ciclo armo una solapa por cada tipo de diferencia

writer = pd.ExcelWriter('variacion de precios historica - diferenciados.xlsx', engine = "xlsxwriter")

for i, s in enumerate(diferencias):
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
  ws.set_column('B:I', 10, fmt_porcentaje)
  
  # Agrego encabezados (Los saqué para poder formatearlos con startrow=1, header=False)
  for col_num, value in enumerate(df_est.columns.values):
    ws.write(0, col_num, value, fmt_encabezados)

writer.save()


## ----------------------- GRAFICOS ESTADISTICOS ----------------------- ##

## Gráficos de variación de precios por periodo (velas) y por tipo de diferencia


print("Imprimiendo graficos x 4...")   

for i, df_est in enumerate(list_df_est):
  
  inicio = datetime.strptime(historico[1], "%d/%m/%Y %H:%M:%S")
  fin = datetime.strptime(historico[2], "%d/%m/%Y %H:%M:%S")
  df = df[inicio : fin]
  
  os.chdir(os.path.dirname(os.path.realpath(__file__)))
  os.mkdir(f"Variacion historica (4 graficos) - {diferencias[i][0]}")
  os.chdir(f"Variacion historica (4 graficos) - {diferencias[i][0]}")
  
  for j, p in enumerate(df_est.index):
    vela = f'{diferencias[i][1]}{df_est.at[j, "periodo"]}'
    media = df_est.at[j, "media"]
    mediana = df_est.at[j, "mediana"]
    min = df_est.at[j, "min"]
    max = df_est.at[j, "max"]
    desv_std = df_est.at[j, "media"]      
    
    lista_graficos = [
      partial(graficos_variacion.lineal_sns, df, vela, media, desv_std),    
      partial(graficos_variacion.caja_y_bigotes, df, vela),
      partial(graficos_variacion.histograma_sns, df, vela, media, mediana, min, max, desv_std),
      partial(graficos_variacion.distribucion_acumulada, df, vela, media, min, max, desv_std)
    ]    
    
    graficos_variacion.multiplot(2, 2, 
                                 f"Variación de precios - Velas de {vela} - {diferencias[i][0]}", 
                                 lista_graficos, 
                                 imprimir = False, guardar=True)  


## Gráficos de distribucion superpuestos

'''
print("Imprimiendo graficos de distribución y temporal superpuestos...")   

os.chdir(os.path.dirname(os.path.realpath(__file__)))
#os.mkdir(f"Variacion historica - distribucion superpuestos")
#os.chdir(f"Variacion historica - distribucion superpuestos")
os.mkdir(f"Variacion historica - temporal superpuestos")
os.chdir(f"Variacion historica - temporal superpuestos")

df_est_1 = list_df_est[0] 
df_est_2 = list_df_est[1]
 
for i, p in enumerate(periodos):
  vela = p[0]
  vela1 = f'{diferencias[0][1]}{p[0]}'
  vela2 = f'{diferencias[1][1]}{p[0]}'
  media1 = df_est_1.at[i, "media"]
  media2 = df_est_2.at[i, "media"]
  mediana1 = df_est_1.at[i, "mediana"]
  mediana2 = df_est_2.at[i, "mediana"]
  min_prob1 = df_est_1.at[i, "min_prob"]
  min_prob2 = df_est_2.at[i, "min_prob"]
  max_prob1 = df_est_1.at[i, "max_prob"]
  max_prob2 = df_est_2.at[i, "max_prob"]
  
  graficos_variacion.histograma_doble(df, vela, vela1, vela2, 
                                    mediana1, mediana2,
                                    min_prob1, min_prob2,
                                    max_prob1, max_prob2,
                                    guardar = True
                                    )
  print(f"Grafico distribucion con velas de {p[0]} OK")
  
  # graficos_variacion.linea_temporal(df, vela, vela1, media1, max_prob1, guardar = True)
  
  lista_graficos = [
    partial(graficos_variacion.linea_temporal, df, vela1, media1, max_prob1, titulo = "Variaciones positivas"),    
    partial(graficos_variacion.linea_temporal, df, vela2, media2, max_prob2, titulo = "Variaciones negativas", 
            periodos = periodos, lineasV=True), 
  ]    
  
  graficos_variacion.multiplot(1, 2, f"Comparacion temporal alza VS baja - {vela}", 
            lista_graficos, imprimir = False, guardar=True)
  
  print(f"Grafico temporal con velas de {p[0]} OK")


'''