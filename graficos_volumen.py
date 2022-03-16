from datetime import datetime
from pprint import pprint
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from sqlite3 import Timestamp
import time
import config
from matplotlib import gridspec
from matplotlib.ticker import FuncFormatter, PercentFormatter
from functools import partial

def datos(vela, semestre, df):
  
  close = df["close"]

  semestres = { 
    "2021-1S": ['01/01/2021 00:00:00', '01/06/2021 00:00:00'],
    "2021-2S": ['01/06/2021 00:00:00', '01/01/2022 00:00:00'],
  } 
  
  periodos = { 
    "1min": 2,          
    "5min": 5,
    "15min": 15,
    "30min": 30,
    "1h": 60,
    "3h": 180,
    "6h": 360,
    "12h": 720,
    "1d": 1440,
    "3d": 4320,
    "7d": 10080,
    "14d": 20160,
    "1m": 43200,
    "2m": 86400,
    "3m": 129600,
    "6m": 259200,
  } 

  dif = close.rolling(window=periodos[vela]).max()/close.rolling(window=periodos[vela]).min() - 1
  df[f'dif_{vela}'] = round(abs(dif),4)

  inicio = datetime.strptime(semestres[semestre][0], "%d/%m/%Y %H:%M:%S")
  fin = datetime.strptime(semestres[semestre][1], "%d/%m/%Y %H:%M:%S")
  
  df2 = df[inicio : fin]

  media = df2[f'dif_{vela}'].mean().round(4)
  mediana = df2[f'dif_{vela}'].median()
  max = df2[f'dif_{vela}'].max()
  min = df2[f'dif_{vela}'].min()
  moda = df2[f'dif_{vela}'].mode()[0]
  desv_std = df2[f'dif_{vela}'].std().round(4)
  
  datos = {"df": df2, 
           "periodo": vela, 
           "min": min, "max": max, "media":media, "mediana":mediana, "moda":moda, "desv_std":desv_std
          }
  #print(df2)
  #print(df2[f'dif_1min'])

  return datos


## --------------- HISTOGRAMA CON MATPLOTLIB ------------- ##

def histograma_mpl(df, vela):
  
  ## Configuro el grafico

  mpl.style.use('bmh')
  fig, ax = plt.subplots(figsize = (12,4))

  ax.set_title("Histograma variaciones porcentuales - Frequencia 30 min")
  ax.set_xlabel("Variación %")
  ax.set_ylabel("Frecuencia")
  ax.legend('No se que poner aca')

  ## Creo un array de valores de variaciones:

  array_variaciones = df[f'dif_{vela}'].values#.flatten()

  ## Defino los rangos porcentuales (Para que salga demarcado en el eje X)

  min_variacion = array_variaciones.min()
  max_variacion = array_variaciones.max()

  bins = 20 # Cantidad de barras
  intervalo = (max_variacion - min_variacion) / bins
  lista_bins = []

  for i in range(bins+1):
      variacion = min_variacion + i * intervalo
      #variacion = '{:.1%}'.format(min_variacion + i * intervalo)
      #variacion = (min_variacion + i * intervalo)*100
      #variacion = f"{(min_variacion + i * intervalo):.0%}"
      lista_bins.append(variacion)

  ## Ploteo el histograma

  ax.set_xticks(lista_bins)
  ax.xaxis.set_major_formatter(PercentFormatter(1)) # Tambien sirve: FuncFormatter('{0:.1%}'.format
  #ax.set_xlim(min_variacion,max_variacion)
  ax.hist(array_variaciones, bins=lista_bins) 
  plt.show()


## --------------- HISTOGRAMA Y DIST SUAVE (Con Seaborn) ---------- ##

def histograma_sns(df, campo, media, mediana, min, max, desv_std, imprimir = False, guardar = False):
     
  ax = sns.histplot(df[campo],
                  color="pink", 
                  stat="percent",
                  kde = True,
                  )
  ax.lines[0].set_color('crimson')
  ax.set(xlabel = "Variación de precio", 
          ylabel = "Frecuencia", 
          title = "Distribución")
  
  if media + 3 * desv_std > max:
    ax.set_xlim(min, max)
  else:
    ax.set_xlim(min, media + 3 * desv_std)
  
  ax.axvline(mediana, color='blue', linestyle='dashed', linewidth=1)
  ax.axvline(media, color='green', linestyle='dashed', linewidth=1)
  min_ylim, max_ylim = plt.ylim()
  plt.text(media*1.1, max_ylim*0.9, 'Media: {0:.2%}'.format(media), color="green")
  plt.text(media*1.1, max_ylim*0.8, 'Mediana: {0:.2%}'.format(mediana), color="blue")

  plt.gca().xaxis.set_major_formatter(PercentFormatter(1)) # Formato % eje X
  
  if guardar == True:
    plt.savefig("Distribucion de volumenes de transaccion.pdf")
  if imprimir == True:
    plt.show()
  

## --------------- SERIE DE TIEMPO LINEAL  ---------- ##

def lineal_sns(df, campo, media, desv_std, imprimir = False, guardar = False):

  ax = sns.lineplot(x=df.index, y=df[campo], data=df)

  ax.set(xlabel = "Fecha", 
          ylabel = "volumen de transaccion", 
          title = "A lo largo del tiempo")
  
  plt.xlim(df.index[0],df.index[-1])
  plt.ylim(0)  
  
  min_xlim, max_xlim = plt.xlim()
  ax.axhline(media, color='orange', linestyle='dashed', linewidth=1)
  plt.text(min_xlim+10, media * 1.1, 'Media', color="orange")
  ax.axhline(media + 3*desv_std, color='red', linestyle='dashed', linewidth=1)
  plt.text(min_xlim+10, media + 3*desv_std * 1.1, 'Limite inliers', color="red")
  
  plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
  
  if guardar == True:
    plt.savefig("Serie temporal de volumenes de transacciones.pdf")
  if imprimir == True:
    plt.show()
    
    
## --------------- CAJA Y BIGOTES ---------- ##

def caja_y_bigotes(df, campo, imprimir = False, guardar = False):

  ax = sns.boxplot(x=df[campo])
  ax.set(xlabel = "volumen de transaccion", 
          title = "Caja y bigotes")
  
  plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
  
  if guardar == True:
    plt.savefig("Caja y bigotes Volumen de transaccion.pdf")
  if imprimir == True:
    plt.show()
    

## --------------- DISTRIBUCION ACUMULADA ---------- ##

def distribucion_acumulada(df, campo, media, min, max, desv_std, imprimir = False, guardar = False):
  
  ax = sns.histplot(df[campo],
                  color="pink", 
                  stat="density",
                  cumulative = True,
                  kde = True,
                  )
  ax.lines[0].set_color('crimson')
  
  if media + 3 * desv_std > max:
    ax.set_xlim(min, max)
  else:
    ax.set_xlim(min, media + 3 * desv_std)
    
  ax.set(xlabel = "Volumen de transaccion", 
          ylabel = "Frecuencia acumulada", 
          title = "Distribución acumulada"
        )
  
  min_xlim, max_xlim = plt.xlim()
  ax.axhline(0.98, color='green', linestyle='dashed', linewidth=1)
  plt.text(max_xlim/20, 0.99, '98 %', color="green")
  
  plt.gca().xaxis.set_major_formatter(PercentFormatter(1)) # Formato % eje X
  plt.gca().yaxis.set_major_formatter(PercentFormatter(1)) # Formato % eje Y
  
  if guardar == True:
    plt.savefig("Distribucion acumulada de volumenes de transacciones.pdf")
  if imprimir == True:
    plt.show()

    
## ---------------- Varios graficos distintos en una figura ----------------##

def multiplot(n, m, titulo, lista_graficos, imprimir = False, guardar = False):
  '''
  Imprime en un mismo plot una matriz de m x n con los graficos que interese mostrar
  '''
  
  if len(lista_graficos) > n*m:
    return print("|---> Operación de impresión abortada. La matriz es pequeña para la cant. de gráficos")
  
  print("Ajustando parametros...")    
  
  fig, ax = plt.subplots(n,m,figsize=(18,8))
  plt.suptitle(titulo)
  plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)
  
  for i in range(m*n):
    print(f"Preparando grafico {i+1}...")
    plt.subplot(int(f'{m}{n}{i+1}'))
    lista_graficos[i]()

  if guardar == True:
    print("Guardando...")
    plt.savefig(f"{titulo}.pdf")
    
  if imprimir == True:
    print("Imprimiendo...")
    plt.show()

    
if __name__=="__main__": 
  '''
  Pruebas de cada gráfico y/o todos juntos
  '''
  ## PARAMETROS DE ENTRADA:  
  cripto = "BTC"
  frec_velas = "1h"
  semestre = "2021-1S"
  columnasDeInteres = ['close']
      
  ## TRANSFORMACIONES:

  BBDD = f'Binance_{cripto}USDT_m.csv'
  fuente = f'{os.path.dirname(os.path.realpath(__file__))}/{BBDD}'    
  df_base = pd.read_csv(fuente, index_col=['date'], parse_dates=True)
  df_base = df_base[columnasDeInteres]

  data = datos(vela = frec_velas, semestre = semestre, df = df_base)
  df = data["df"]
  min = data["min"]
  max = data["max"]
  media = data["media"]
  mediana = data["mediana"]
  desv_std = data["desv_std"]
  vela = data["periodo"]
  
  ## GRAFICOS:
  
  #histograma_sns(df, vela, media, mediana, min, max, desv_std, imprimir = True)
  #lineal_sns(df, vela, media, desv_std, imprimir = True)
  #caja_y_bigotes(df, vela, imprimir = True)
  #distribucion_acumulada(df, vela, media, mediana, desv_std, imprimir = True)
  #graficosx4(df, vela, media, mediana, desv_std, semestre = "2021-1S", imprimir = True)  
'''
  lista_graficos = [
    partial(lineal_sns, df, vela, media, desv_std),    
    partial(caja_y_bigotes, df, vela),
    partial(histograma_sns, df, vela, media, mediana, min, max, desv_std),
    partial(distribucion_acumulada, df, vela, media, min, max, desv_std)
  ]    
  
  multiplot(1, 1, f"Volumen de transaccion - Velas de {vela} - Semestre {semestre}", 
            lista_graficos, imprimir = True, guardar=True)
  '''