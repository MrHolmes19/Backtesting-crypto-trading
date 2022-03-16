from datetime import datetime
from math import inf
import pandas as pd
import os


def calcular_prob(dataset, columna, desde = False, hasta = False,
                  mayor_que = False, menor_que = False, valor_exacto = False):
  '''
  Para un cierto dataset, acotado entre ciertas fechas (o no), y dentro de una determinada columna...
  Devuelve la probabilidad de aparición de cierto valor o rango de valores
  '''

  fuente = f'{os.path.dirname(os.path.realpath(__file__))}/{dataset}'
  df = pd.read_csv(fuente, index_col=['date'], parse_dates=True)

  if desde and hasta:
    inicio = datetime.strptime(desde, "%d/%m/%Y %H:%M")
    fin = datetime.strptime(hasta, "%d/%m/%Y %H:%M")
    df = df[inicio : fin]

  df = df[[columna]]

  mayor_que = float(-inf) if not mayor_que else mayor_que
  menor_que = float(inf) if not menor_que else menor_que
  
  total_registros = len(df)
  
  if valor_exacto:
    apariciones = len(df[df[f'{columna}'] == valor_exacto])
  else:
    #apariciones = len(df[df[f'{columna}'].between(mayor_que, menor_que)])
    apariciones = len(df[(df[f'{columna}'] >= mayor_que) & (df[f'{columna}'] <= menor_que)])
    #apariciones = len(df.query(f'{mayor_que} <= {columna} <= {menor_que}'))
  
  probabilidad = apariciones / total_registros
  
  print("*********************************************************")
  print("Apariciones: ", apariciones)
  print(f"Probabilidad: {round(probabilidad*100, 5)} %")
  print("Frecuencia esperada:")  
  print(f" > 1 vez cada {round(1/probabilidad,1)} registros")
  print(f" > 1 vez cada {round(1/probabilidad,1)} minutos")
  print(f" > 1 vez cada {round(1/probabilidad/60,2)} horas")
  print(f" > 1 vez cada {round(1/probabilidad/(60*24),2)} dias")
  print(f" > 1 vez cada {round(1/probabilidad/(60*24*30),2)} meses")
  print("")
  print(f" > En una hora: {round(probabilidad*60,2)} apariciones")
  print(f" > En un dia: {round(probabilidad*60*24,2)} apariciones")
  print(f" > En una semana: {round(probabilidad*60*24*7,2)} apariciones")
  print(f" > En un mes: {round(probabilidad*60*24*30,2)} apariciones")
  print(f" > En un año: {round(probabilidad*60*24*365,2)} apariciones")
  print("*********************************************************")
  
  return probabilidad
  
  
if __name__=="__main__":
  
  ## DATOS DE INGRESO
  #-------------------------------
  inicio = '01/09/2017 00:00'
  fin = '20/01/2022 00:00'
  mayor_que = 0.03 #( % por 100 para porcentaje)
  menor_que = False
  valor_exacto = False
  columnaDeInteres = 'dif_-5min'
  dataset = f'variaciones_dif_historico.csv'
  #columnaDeInteres = 'dif_1min'
  #dataset = f'variaciones_abs_historico.csv'
  #-------------------------------
  
  calcular_prob(dataset, columna = columnaDeInteres, 
                desde = inicio, hasta = fin,
                mayor_que = mayor_que, menor_que = menor_que, valor_exacto = valor_exacto)
