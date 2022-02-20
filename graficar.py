from datetime import datetime
from sqlite3 import Timestamp
import time
from binance.client import Client
import config
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from matplotlib import gridspec

def grafico_lineal(fuente, inicio, fin, valor):
  
  df = pd.read_csv(fuente, index_col=['date'], parse_dates=True)
  
  df = df[inicio : fin]
  
  plt.figure(figsize=(10,5))
  plt.plot(df[f"{valor}"], label = f"Valor de cierre de la vela")
  plt.title("Variación del precio del BTC")
  plt.xlabel("Fecha")
  plt.ylabel(f"Valor de {valor}")
  plt.legend(loc = "upper left")
  plt.show()



if __name__=="__main__":
  '''
  Grafica cualquier conjunto de datos de acuerdo a múltiples parámetros
  '''
  
  ## PARAMETROS:  
  cripto = "BTC"
  frec_velas = "m"
  inicio = '01/01/2021 00:00:00'
  fin = '10/01/2021 00:00:00'
  valor = "close"
  
  ## TRANSFORMACIONES:
  
  inicio = datetime.strptime(inicio, "%d/%m/%Y %H:%M:%S")
  fin = datetime.strptime(fin, "%d/%m/%Y %H:%M:%S")
  
  BBDD = f'Binance_{cripto}USDT_{frec_velas}.csv'
  fuente = f'{os.path.dirname(os.path.realpath(__file__))}/{BBDD}'
  
  grafico_lineal(fuente, inicio, fin, valor)

  