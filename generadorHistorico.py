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

def getHistoric(crypto="ETHUSDT", kline=Client.KLINE_INTERVAL_1MINUTE, periodo="1 day ago UTC-3"):
  '''
  Parameters
  ----------
  crypto : String
      Moneda a recuperar datos. Ej "ETHUSDT"
  periodo: String
      Delta de tiempo de los datos. Default: "1day ago UTC-3"

  Returns
  -------
  df : Pandas.DataFrame
      Devuelve un dataframe con el siguiente formato
      index = DateTime
      Columns = "Open", "High", "Low", "Close", "Volume"

  '''
  print("Inicio - Antes de hacer la conexion con client y get historical")
  start = time.process_time() 
  client = Client(config.API_KEY, config.API_SECRET)
  klines = client.get_historical_klines(crypto, kline, periodo)
  print("Luego de hacer la conexion y get historical. Antes de dropear columnas inservibles")
  print(time.process_time() - start) 
  df = pd.DataFrame(klines,  columns=['date',
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
  df['date'] = pd.to_datetime(df['date'], unit='ms') #format='%Y-%m-%d %H:%M:%S'
  
  print("Luego de dropear. Antes de setear como indice la fecha")
  print(time.process_time() - start) 
  
  df.set_index('date', inplace=True, drop=True)
  
  print("Despues de indexar fecha. Antes de cambiar tipo de dato en  columnas")
  print(time.process_time() - start) 
  
  df['open']   = df['open'].astype(float).round(1)
  df['high']   = df['high'].astype(float).round(1)
  df['low']    = df['low'].astype(float).round(1)
  df['close']  = df['close'].astype(float).round(1)
  df['volume'] = df['volume'].astype(float).round(1)
  
  print("Fin")
  print(time.process_time() - start) 
  
  #df.tz_localize('UTC-3', level=0)
  print(df)
  # print(type(df.index))
  #df.index = df.index.tz_localize('UTC').tz_convert('America/Argentina/Buenos_Aires')
  
  timezone = pytz.timezone('America/Argentina/Buenos_Aires')
  df.index = df.index.tz_localize(pytz.utc).tz_convert(timezone)
  df.index = df.index.tz_localize(None)
  return df


if __name__=="__main__":
  start = timer()
  
  df = getHistoric(crypto = "BTCUSDT", kline=Client.KLINE_INTERVAL_1MINUTE, periodo = "388 day ago UTC-3")

  print(df)
  df.to_csv("Binance_BTCUSDT_m.csv", encoding='utf-8', index=True)
  
  stop = timer()
  time = stop-start
  print("Tiempo en generar historicos: ", time)