from datetime import datetime, timedelta
import os
import dateutil
import pandas as pd
from timeit import default_timer as timer
from random import randrange
'''
fecha = datetime.today()

print(fecha)

fecha2 = fecha.strftime("%d-%m-%Y")

print(fecha2)

#fecha2 = fecha.date()

ahora = datetime.now().strftime("%d-%m-%Y %Hh-%Mm")
print(ahora)

os.mkdir("Carpeta-prueba")
os.mkdir("Carpeta-prueba/Subcarpeta")

os.mkdir("Carpeta-prueba2")
os.mkdir(os.path.join('Carpeta-prueba2', 'Subcarpeta2'))
'''

inicio = '2021-01-01 00:00:00'
final = '2021-04-01 00:00:00'

#inicio_fecha = datetime.strptime(inicio, "%Y-%m-%d H:M:S")
inicio_fecha = datetime.fromisoformat(inicio)
print(inicio_fecha)
print(type(inicio_fecha))

inicio_fecha_str = datetime.strftime(inicio_fecha, "%d/%m/%Y %H:%M")
print(inicio_fecha_str)
final_fecha = datetime.fromisoformat(final)

# diferencia = final_fecha - inicio_fecha
# print(diferencia.years)

from dateutil.relativedelta import relativedelta

diferencia = relativedelta(final_fecha,inicio_fecha)
print(float(diferencia.years))


'''
BBDD = 'Binance_BTCUSDT_d.csv'
fuente = f'{os.path.dirname(os.path.realpath(__file__))}/{BBDD}'
df = pd.read_csv(fuente)


index = df.index[df["date"] == "2021-10-05 00:00:00"]
print(index[0])
print(df.at[index[0],'close'])
#print(df.loc[df["date" == "2021-10-05 00:00:00"].index,'close'])
'''

'''
BBDD = 'Binance_BTCUSDT_m.csv'
fuente = f'{os.path.dirname(os.path.realpath(__file__))}/{BBDD}'
df = pd.read_csv(fuente)

# print(df)

start = timer() 

df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')
df2 = df.head(60)

if len(df2[df2["date"].dt.minute == 0].index)<2:
  print("Es base de datos min a min")
  df3 = df.loc[::-1].reset_index(drop=True)
  
elif len(df2[df2["date"].dt.hour == 0].index)<2:
  print("Es base de datos hora a hora")
  df3 = df[df["date"].dt.minute == 0]
  df3 = df3.loc[::-1].reset_index(drop=True)
  
else:
  print("Es base de datos diario")
  df3 = df.loc[::-1].reset_index(drop=True)
  
  
#print(df3) 


## Caso de desplazamiento

fecha_inicio = "12/5/2021 05:10:00"
fecha_inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y %H:%M:%S")
intervalo = 30
desplazamiento = 7
n = 10  
metodo = "desplazamiento"

if metodo == "desplazamiento":
  dias_limite = intervalo + desplazamiento * n
elif metodo == "cascada":
  dias_limite = intervalo * n
elif metodo == "spot":
  dias_limite = intervalo
else:
  print(f"Simulacion abortada --> Falta definir método de estudio de escenarios")

primera_fecha = df3["date"].iloc[1]  
ultima_fecha = df3["date"].iloc[-1]
fecha_inicio_max = ultima_fecha - timedelta(days=dias_limite)

if fecha_inicio > fecha_inicio_max:
  print(f"Simulacion abortada --> Para el escenario elegido, la fecha maxima de inicio es:{fecha_inicio_max}. Modifique la fecha")

fecha_final = fecha_inicio + timedelta(days=dias_limite)

df4 = df3.set_index('date')
df4 = df4[fecha_inicio : fecha_final]

print("----------------")
print(fecha_inicio)
print(fecha_final)
print("----------------")
print(df4)

iterable = df4.index.to_numpy()
inicio = iterable[0]
print(iterable)
print(inicio)

stop = timer()
time = stop-start
print("Tiempo invertido: ", time)

'''





#fecha = datetime.strptime("2021-10-05 00:00:00", "%Y-%m-%d H:M:S")
#fecha = datetime.fromisoformat("2021-01-05 00:00:00").date()
#print(fecha)
#index = df.index[df["date"] == str(fecha)]
#print(index)
#print(index[0])
#print(df.at[index[0],'close'])