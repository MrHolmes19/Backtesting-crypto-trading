from datetime import datetime, timedelta
import os
import dateutil
import pandas as pd
from timeit import default_timer as timer
from random import randrange
import graficador
from timeit import timeit
from pprint import pprint

# fecha_informe = "2021-01-28 11:00:00"

# fecha_informe_date = datetime. strptime(fecha_informe, '%Y-%m-%d %H:%M:%S')

# '''
# print(fecha_informe_date)
# fecha_pro = datetime.strftime(fecha_informe_date, '%d %b %Y %H:%M')
# print(fecha_pro)

# #from babel.dates import format_date
# import locale
# locale.setlocale(locale.LC_TIME, "es_ES")
# fecha_informe_date = datetime. strptime(fecha_informe, '%Y-%m-%d %H:%M:%S')
# fecha_pro = datetime.strftime(fecha_informe_date, '%d %b %Y')
# print(fecha_pro)
# '''
# '''fecha_informe2 = "2021-01-27 11:00:00"
# fecha_informe2_date = datetime. strptime(fecha_informe2, '%Y-%m-%d %H:%M:%S')
# print(fecha_informe2_date)

# proyeccion_anual = datetime.timestamp(fecha_informe_date) - datetime.timestamp(fecha_informe2_date)
# print(proyeccion_anual/60/60)   

# proyeccion_anual = (fecha_informe_date - fecha_informe2_date).total_seconds()
# print(proyeccion_anual/60/60)  
# '''

# # fecha_inicio_max = "2021-01-28 11:00:00"

# # fecha_inicio_max = datetime. strptime(fecha_inicio_max, '%Y-%m-%d %H:%M:%S')

# # primera_fecha = "2021-01-27 11:00:00"
# # primera_fecha = datetime. strptime(primera_fecha, '%Y-%m-%d %H:%M:%S')

# # rango_disp = (fecha_inicio_max - primera_fecha).total_seconds()
# # random_second = randrange(int(rango_disp))    
# # print(random_second)  
# # inicio = start + timedelta(seconds=random_second).replace(hour = 0, minute = 0, second = 0)
# # final = inicio + timedelta(days=dt)

# carpeta_actual = os.path.dirname(os.path.realpath(__file__))

# df = pd.read_csv(f"{carpeta_actual}/Binance_BTCUSDT_m.csv", encoding='latin-1')
# # print(df)
# df = df[0:100]

# # print(df)

# columns=['date', 'open', 'high', 'low', 'close', 'volume']

# fila = df.loc[df["date"] == "2017-08-17 01:00:00"]
# fila = fila[columns]
# #print(fila)
# fila2 = df.loc[df["date"] == "2017-08-17 01:01:00"]
# fila2 = fila2[columns]
# #print(fila2)
# fila3 = df.loc[df["date"] == "2017-08-17 01:02:00"]
# fila3 = fila3[columns]

# filas = [fila, fila2, fila3]

# # print(fila)

# df2 = pd.DataFrame(columns = columns)
# df2 = df2.append(fila)
# df2 = df2.append(fila2)
# df2 = df2.append(fila3)

# #df2 = df2(filas, columns=columns)

# print(df2)
# #df2["nuevo"] = 5
# df2.at[0, "nuevo"] = 4
# print(df2)

txt = "+15min"
#print([int(s) for s in txt if s.isdigit()])
#print(int(numero+=i) for i in txt if i.isdigit())
#numero = ""
# for i in txt:
#   if i.isdigit():
#     numero += i
# print(int(numero))
# print(type(int(numero)))
numero = int(''.join(filter(str.isdigit, txt)))
print(numero)
print(type(numero))