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

def getHistoric(crypto, kline, periodo, inicio, fin):
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
  print("Descargando los datos de Binance...")
  
  client = Client(config.API_KEY, config.API_SECRET)
  if periodo:
    klines = client.get_historical_klines(crypto, kline, periodo)
  else:
    klines = client.get_historical_klines(crypto, kline, inicio, fin)
  
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
  
  df['date'] = pd.to_datetime(df['date'], unit='ms') #format='%Y-%m-%d %H:%M:%S'

  ''' METODO LEANDRO

  df = df.drop(df.columns[[0]], axis=1)
  inicio = datetime. strptime(inicio, '%d %b, %Y')
  fin = datetime. strptime(fin, '%d %b, %Y')
  # print(inicio, fin)
  registros = int((fin - inicio).total_seconds()/60)
  # print(registros)
  fechas = []
  for i in range(registros+1):
    fecha = inicio + timedelta(seconds=60*(i))
    fechas.append(fecha)    
  #print(fechas)

  df["date"] = fechas
  print(df)
  '''
  
  ''' METODO NUMPY
  numpy_dates = df['date'].values
  dates = numpy_dates.astype('datetime64[ms]') # Tarda 3 seg mas Conchatumareee
  df['date'] = dates.tolist()
  '''
  
  df.set_index('date', inplace=True, drop=True)
  
  df['open']   = df['open'].astype(float).round(1)
  df['high']   = df['high'].astype(float).round(1)
  df['low']    = df['low'].astype(float).round(1)
  df['close']  = df['close'].astype(float).round(1)
  df['volume'] = df['volume'].astype(float).round(1)

  print(df)
  
  timezone = pytz.timezone('America/Argentina/Buenos_Aires')
  df.index = df.index.tz_localize(pytz.utc).tz_convert(timezone)
  df.index = df.index.tz_localize(None)

  return df


if __name__=="__main__":
  start = timer()
  
  cripto = "BTC"
  velas = "m"
  inicio = "15 Jan, 2022"
  fin = "1 Feb, 2022"
  periodo = False # "365 day ago UTC-3"
  
  df = getHistoric(crypto = f"{cripto}USDT", 
                   kline=Client.KLINE_INTERVAL_1MINUTE, 
                   periodo = periodo,
                   inicio = inicio, 
                   fin = fin)

  df.to_csv(f"Binance_{cripto}USDT_{velas}2.csv", encoding='utf-8', index=True)
  
  stop = timer()
  time = stop-start
  print("Tiempo en generar historicos: ", time)