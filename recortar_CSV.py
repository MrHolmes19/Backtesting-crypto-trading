from datetime import datetime, timedelta
import os
import pandas as pd
from timeit import default_timer as timer


def recortar_df(nombre_origen, nombre_final, inicio, fin, columnas = False, csv = False):
  '''
  Lee un archivo csv y lo devuelve seccionado entre inicio y fin (Fechas o indice)
  Opcional: filtra tambien las columnas de interés
  '''
  fuente = f'{os.path.dirname(os.path.realpath(__file__))}/{nombre_origen}.csv'

  if type(inicio) == int and type(fin) == int:
    df = pd.read_csv(fuente, parse_dates=True)
  elif type(inicio) == str and type(fin) == str:
    try:
      inicio = datetime.strptime(inicio, "%d/%m/%Y %H:%M:%S")
      fin = datetime.strptime(fin, "%d/%m/%Y %H:%M:%S")
      df = pd.read_csv(fuente, index_col=['date'], parse_dates=True)
    except:
      return print("Error. Ingresaste un string y no coincide con el formato de fechas.")
  else:
    return print("Error. Ingresar 2 fechas o 2 numeros enteros de indice")
  
  df2 = df[inicio : fin]
  
  if columnas:
    df2 = df2[columnas]

  if csv:
    df2.to_csv(f'{nombre_final}.csv', encoding='utf-8', index=True)
  
  print(df2)  
  
  return df2


if __name__=="__main__":
  
  ## DATOS DE INGRESO
  #-------------------------------
  inicio = '01/12/2021 00:00:00' # dd/mm/aaaa hh:mm:ss O indice
  fin = '01/02/2022 00:00:00'
  # inicio = 0
  # fin = -200
  columnasDeInteres = ['close']
  nombre_origen = 'Binance_BTCUSDT_m' # Sin extension .csv
  nombre_final = f'{nombre_origen}_{inicio[:10]}_{fin[:10]}'  # Sin extension .csv
  nombre_final = nombre_final.replace("/", "-")
  #-------------------------------
  
  recortar_df(nombre_origen, nombre_final, inicio, fin, columnas = columnasDeInteres, csv = True)
  
