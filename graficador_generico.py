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

## --------------- SERIE DE TIEMPO LINEAL  ---------- ##

def lineal(df, dataX, dataY, labelY, titulo, media, desv_std, porcent = False, imprimir = False, guardar = False):

  ax = sns.lineplot(x=dataX, y=dataY, data=df)

  ax.set(xlabel = "Fecha", 
          ylabel = labelY, 
          title = "A lo largo del tiempo")
  
  plt.xlim(df.index[0],df.index[-1])
  plt.ylim(0)  
  
  min_xlim, max_xlim = plt.xlim()
  ax.axhline(media, color='orange', linestyle='dashed', linewidth=1)
  plt.text(min_xlim+10, media * 1.1, 'Media', color="orange")
  ax.axhline(media + 3*desv_std, color='red', linestyle='dashed', linewidth=1)
  plt.text(min_xlim+10, media + 3*desv_std * 1.1, 'Limite inliers', color="red")
  
  if porcent:
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
  
  if guardar == True:
    plt.savefig(f"{titulo}.pdf")
  if imprimir == True:
    plt.show()
    
## --------------- CAJA Y BIGOTES ---------- ##

def caja_y_bigotes(dataX, labelX, titulo, porcent = False, imprimir = False, guardar = False):

  ax = sns.boxplot(x=dataX)
  ax.set(xlabel = labelX, 
          title = "Caja y bigotes")
  
  if porcent:
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
  
  if guardar == True:
    plt.savefig(f"{titulo}.pdf")
  if imprimir == True:
    plt.show()
    
        
## --------------- HISTOGRAMA Y DIST SUAVE (Con Seaborn) ---------- ##

def histograma(datosX, labelX, titulo, media, mediana, min, max, desv_std, porcent = False, imprimir = False, guardar = False):
 
  ax = sns.histplot(datosX,
                  color="pink", 
                  stat="percent",
                  kde = True,
                  )
  ax.lines[0].set_color('crimson')
  ax.set(xlabel = labelX, 
          ylabel = "Frecuencia", 
          title = "Distribución")
  
  if media + 3 * desv_std > max:
    ax.set_xlim(min, max)
  else:
    ax.set_xlim(min, media + 3 * desv_std)
  
  ax.axvline(mediana, color='blue', linestyle='dashed', linewidth=1)
  ax.axvline(media, color='green', linestyle='dashed', linewidth=1)
  min_ylim, max_ylim = plt.ylim()
  plt.text(media*1.1, max_ylim*0.9, f'Media: {media}', color="green")
  plt.text(media*1.1, max_ylim*0.8, f'Mediana: {mediana}', color="blue")

  if porcent:
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1)) # Formato % eje X
    plt.text(media*1.1, max_ylim*0.9, 'Media: {0:.2%}'.format(media), color="green")
    plt.text(media*1.1, max_ylim*0.8, 'Mediana: {0:.2%}'.format(mediana), color="blue")
  
  if guardar == True:
    plt.savefig(f"{titulo}.pdf")
  if imprimir == True:
    plt.show()
  


## --------------- DISTRIBUCION ACUMULADA ---------- ##

def distribucion_acumulada(dataY, labelX, titulo, media, min, max, desv_std, porcent = False, imprimir = False, guardar = False):

  ax = sns.histplot(dataY,
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
    
  ax.set(xlabel = labelX, 
          ylabel = "Frecuencia acumulada", 
          title = "Distribución acumulada"
        )
  
  min_xlim, max_xlim = plt.xlim()
  ax.axhline(0.98, color='green', linestyle='dashed', linewidth=1)
  plt.text(max_xlim/20, 0.99, '98 %', color="green")
  
  if porcent:
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1)) # Formato % eje X
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1)) # Formato % eje Y
  
  if guardar == True:
    plt.savefig(f"{titulo}.pdf")
  if imprimir == True:
    plt.show()
  
  
## --------------- SERIE DE TIEMPO LINEAL DE DATOS ESTADISTICOS  ---------- ##

def lineal_est(df, labelY, titulo, imprimir = False, guardar = False):
  
  fig, ax = plt.subplots(figsize = (18,10))
    
  ax = sns.lineplot(x=df.index, y=df['media'], data=df, color = "orange")
  ax = sns.lineplot(x=df.index, y=df['min_prob'], data=df, color = "blue")
  ax = sns.lineplot(x=df.index, y=df['max_prob'], data=df, color = "red")
  ax = sns.lineplot(x=df.index, y=df['moda'], data=df, color = "brown")
  ax = sns.lineplot(x=df.index, y=df['mediana'], data=df, color = "black")
  
  min_xlim, max_xlim = plt.xlim()
  min_ylim, max_ylim = plt.ylim()
  plt.text(min_xlim*1.005, max_ylim*0.96, 'Media', color="orange")
  plt.text(min_xlim*1.005, max_ylim*0.93, 'Minimo probable', color="blue")
  plt.text(min_xlim*1.005, max_ylim*0.90, 'Maximo probable', color="red")
  plt.text(min_xlim*1.005, max_ylim*0.87, 'Moda', color="brown")
  plt.text(min_xlim*1.005, max_ylim*0.84, 'Mediana', color="black")
  
  #sns.set(rc={'figure.figsize':(11.7,8.27)})    

  ax.set(xlabel = "Semestres", 
          ylabel = labelY, 
          title = "Datos estadisticos a lo largo del tiempo",
        )
  
  plt.xlim(df.index[0],df.index[-1])
  plt.ylim(0)  
  
  plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
  plt.grid()
  
  if guardar == True:
    plt.savefig(f"{titulo}.pdf")
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
  