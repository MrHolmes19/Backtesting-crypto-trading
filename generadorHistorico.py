from sqlite3 import Timestamp
import time
from binance.client import Client
import config
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from matplotlib import gridspec
from timeit import default_timer as timer
import pytz
from datetime import datetime, timedelta

def getHistoric(crypto, velas, inicio, fin, periodo = False):
  '''
  Recibe:
  - crypto : Moneda a recuperar datos. Ej "ETHUSDT"
  - periodo: Delta de tiempo de los datos.  Ej: "30 day ago UTC-3"
  - inicio/fin: Fechas de partida y final . Ej: "15 Jan, 2022"
  
  Devuelve:
  - Dataframe con el siguiente formato: index = DateTime || Columns = "Open", "High", "Low", "Close", "Volume"
  - Archivo .CSV del dataframe
  '''
  
  print("Descargando los datos de Binance...")
  
  kline = {
    "m": Client.KLINE_INTERVAL_1MINUTE,
    "3m": Client.KLINE_INTERVAL_3MINUTE,
    "5m": Client.KLINE_INTERVAL_5MINUTE,
    "15m": Client.KLINE_INTERVAL_15MINUTE,
    "30m": Client.KLINE_INTERVAL_30MINUTE,
    "h": Client.KLINE_INTERVAL_1HOUR,
    "d": Client.KLINE_INTERVAL_1DAY,
  }  
  
  client = Client(config.API_KEY, config.API_SECRET)
  par = f"{crypto}USDT"
  if periodo:
    klines = client.get_historical_klines(par, kline[velas], periodo)
  else:
    klines = client.get_historical_klines(par, kline[velas], inicio, fin)
  
  df = pd.DataFrame(klines,  columns=['date', # 'Open Time', CREO QUE HAY QUE TOMAR EL CLOSE TIME
                                      'open',
                                      'high',
                                      'low',
                                      'close',
                                      'volume',
                                      'close time',
                                      'quote asset volume',
                                      'number of trades',
                                      'taker buy base asset volume',
                                      'taker buy quote asset volume',
                                      'ignore'])
  
  df = df.drop(df.columns[[6, 7, 9, 10, 11]], axis=1)
  
  df['date'] = pd.to_datetime(df['date'], unit='ms')
  
  df.set_index('date', inplace=True, drop=True)
  
  df['open']   = df['open'].astype(float).round(1)
  df['high']   = df['high'].astype(float).round(1)
  df['low']    = df['low'].astype(float).round(1)
  df['close']  = df['close'].astype(float).round(1)
  df['volume'] = df['volume'].astype(float).round(1)
  
  timezone = pytz.timezone('America/Argentina/Buenos_Aires')
  df.index = df.index.tz_localize(pytz.utc).tz_convert(timezone)
  df.index = df.index.tz_localize(None)

  print(df)
  df.to_csv(f"Binance_{crypto}USDT_{velas}.csv", encoding='utf-8', index=True)
  
  return df

def updateHistoric(crypto, velas):
  '''
  Recibe: Mismos datos que getHistoric Y el dataset historico que se busca actualizar
  Devuelve: Nuevo dataset que sobreescribe el existente  
  '''
  fuente = f'{os.path.dirname(os.path.realpath(__file__))}/Binance_{crypto}USDT_{velas}.csv'
  df_existente = pd.read_csv(fuente, index_col=['date'], parse_dates=True)
  

  ultima_fecha = df_existente.iloc[-1:].index[0]
  
  nuevo_inicio = ultima_fecha + timedelta(minutes = 1)
  ahora = datetime.now()
  nuevo_inicio = datetime.strftime(nuevo_inicio, "%d %b, %Y")
  ahora = datetime.strftime(ahora, "%d %b, %Y")
  
  df_actualizado = getHistoric(crypto = cripto, 
                   velas = velas, 
                   inicio = nuevo_inicio, 
                   fin = ahora)

  #print(df_actualizado)
  df= pd.concat([df_existente, df_actualizado])
  df = df.drop_duplicates('date')   # No deberia ser necesario
  
  print(df)
  df.to_csv(f"Binance_{crypto}USDT_{velas}.csv", encoding='utf-8', index=True)
  
  return df



if __name__=="__main__":
  start = timer()
  
  ## DATOS DE ENTRADA
  cripto = "BTC"
  velas = "m"
  inicio = "15 Jan, 2017"
  fin = "22 Feb, 2022"
  periodo = False # "365 day ago UTC-3"
  '''
  df = getHistoric(crypto = cripto, 
                   velas = velas, 
                   inicio = inicio, 
                   fin = fin,
                   periodo = periodo)
  '''
  updateHistoric(crypto = cripto, velas = velas)
  
  stop = timer()
  time = stop-start
  print("Tiempo en generar historicos: ", time)