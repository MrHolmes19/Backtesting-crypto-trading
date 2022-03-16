from datetime import datetime
from unicodedata import name
from urllib import parse
import pyreadline
import pandas as pd
import os
import recortar_CSV
import graficador
import recortar_CSV
#import indicadores
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
from pprint import pprint
import json

def convertirDataset():
  '''
  Lee el archivo txt de precios cada 2 seg aprox. filtrando solo que interesa y lo convierte en csv
  '''
  
  with open('price_live.txt') as f:
    lines = f.readlines()

  with open(f'Binance_BTCUSDT_2s.csv', "w", newline="") as intraminuto:
    writer = csv.writer(intraminuto)
    writer.writerow(["date", "price", "volume"])
    for i in lines:
      i = i.replace("'",'"').replace('False','"False"').replace('True','"True"')
      i = json.loads(i)
      date = datetime.fromtimestamp(i['E']/1000)
      price = round(float(i['k']['c']),2)
      volume = round(float(i['k']['v']),2)
      writer.writerow([date, price, volume])


def crearIntraminuto(csv = False):
  '''
  Mezcla el dataset de minutos con el creado anteriormente de 2 seg.
  Devuelve un nuevo Dataset con indices cada 2 seg e informacion de la vela de 1 min
  '''
  
  carpeta_actual = os.path.dirname(os.path.realpath(__file__))
  df = pd.read_csv(f'{carpeta_actual}/Binance_BTCUSDT_2s.csv', parse_dates=True)
  df2 = pd.read_csv(f'{carpeta_actual}/Binance_BTCUSDT_m.csv')

  #print(df)
  #print(df2)

  df2['date'] = pd.to_datetime(df2['date'], format='%Y-%m-%d %H:%M:%S')

  df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')
  df['date_min'] = pd.to_datetime(df['date'].dt.strftime('%Y-%m-%d %H:%M'))

  #df['close_1min'] = df2[df2['close'].index == df['date_min']]
  df = df.merge(df2,left_on="date_min",right_on="date")

  df = df[['date_x', 'price', 'open', 'close', 'high', 'low']]

  print(df)
  if csv == True:
    df.to_csv(f"BTCUSDT_intraminuto.csv", encoding='utf-8', index=False)  
    
  return df
  
def plotearIntraminuto(guardar = False):
  '''
  Genera un grafico de la variacion del precio cada 2 seg y lo superpone con la vela envolvente de 1 min
  '''
  carpeta_actual = os.path.dirname(os.path.realpath(__file__))
  df = pd.read_csv(f'{carpeta_actual}/BTCUSDT_intraminuto.csv', parse_dates=True, index_col='date_x')

  print(df)
  graficador.transparentCandlestick(df, 'BTC variacion de precio dentro de velas de 1 min')


def convertirDataset2():
  '''
  Lee el archivo txt de precios cada 2 seg aprox. filtrando solo que interesa y lo convierte en csv
  '''
  
  with open('price_live.txt') as f:
    lines = f.readlines()

  with open(f'Binance_BTCUSDT_2s.csv', "w", newline="") as intraminuto:
    writer = csv.writer(intraminuto)
    writer.writerow(["date", "price"])
    for i in lines:
      i = i.replace("'",'"').replace('False','"False"').replace('True','"True"')
      i = json.loads(i)
      date = datetime.fromtimestamp(i['E']/1000)
      price = round(float(i['k']['c']),2)
      writer.writerow([date, price])


if __name__ == '__main__':  
  
  ## -- Variacion del precio dentro de vela de 1 minuto --
  convertirDataset()  
  crearIntraminuto(csv = True)  
  plotearIntraminuto()
  
  ## -- Variacion del precio dentro de vela de 1 minuto --
  #convertirDataset2()  


