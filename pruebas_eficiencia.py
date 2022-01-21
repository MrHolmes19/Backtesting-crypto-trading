import numpy as np
import pandas as pd
import random
from pprint import pprint
from timeit import default_timer as timer
from itertools import tee
import os

fuente = f'{os.path.dirname(os.path.realpath(__file__))}\historial-BTC.csv'
df = pd.read_csv(fuente)
#df = df.loc[1:10080] # Una semana
#df = df.loc[1:43200] # Un mes
#df = df.loc[1:525960] # Un año            
df = df['date'].to_frame() # 2 años y quitando el resto de las columnas

# ------------------------------------ METODOS DE RECORRIDO -----------------------------------

def iterrow():
    start = timer()
    
    for index, row in df.iterrows():
        #print(row["date"])
        a = 2 + 2
        
    stop = timer()
    time = stop-start
    print("Tiempo estimado generando dataframe y iterrows: ", time)


def itertuples():
    start = timer()
    
    for i in df.itertuples():
        # print(i[1])
        a = 2 + 2
        
    stop = timer()
    time = stop-start
    print("Tiempo estimado generando dataframe y itertuples: ", time)
    
 
def nparrays():
    start = timer()
    
    columnas = df.values
    for i in range(df.shape[0]):
        #print(columnas[i][0])
        a = 2 + 2
        
    stop = timer()
    time = stop-start
    print("Tiempo estimado generando dataframe y np arrays: ", time)
    
def dict():
    start = timer()
    
    df_dict = df.to_dict('dict')
    for i in df_dict:
        # print(df_dict['date'])
        a = 2 + 2
        
    stop = timer()
    time = stop-start
    print("Tiempo estimado generando dataframe y diccionarios: ", time)

    
def arraysList():
    start = timer()
    
    df_lista = df['date'].to_numpy().tolist()
    for i in df_lista:
        # print(i)
        a = 2 + 2
        
    stop = timer()
    time = stop-start
    print("Tiempo estimado recorriendo un lista de numpy array: ", time)


def generadorIterador():
    start = timer()

    def generarIterador(df):
        for i in range(len(df)):
            yield df.iloc[i]

    binance = generarIterador(df)

    for i in binance:
        # print(i["date"])
        a = 2 + 2
    
    stop = timer()
    time = stop-start
    print("Tiempo estimado recorriendo in iterador generador: ", time)

def dataframeIndex():
    df = pd.read_csv(fuente)
    df['date'] = pd.to_datetime(df.date)    
    df = df.set_index('date')
    start = timer()
    
    df_index = df.index
    for i in df_index:
        # print(i)
        a = 2 + 2
        
    stop = timer()
    time = stop-start
    print("Tiempo estimado recorriendo indices de un DF: ", time)
    
# TEST DE VELOCIDAD PARA CICLAR FECHAS

'''
#iterrow()
itertuples()
nparrays()
dict()
arraysList()
dataframeIndex()
#generadorIterador()  
'''

# ------------------------------------ METODOS DE CONVERSION FECHAS -----------------------------------

df = pd.read_csv(fuente)
'''
start = timer() 
df['date'] = pd.to_datetime(df['date'])
stop = timer()
time = stop-start
print("Tiempo invertido en pasar todo a Datetime: ", time)
'''

'''
start = timer() 
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M')
stop = timer()
time = stop-start
print("Tiempo invertido en pasar todo a Datetime CON formato: ", time)
'''

start = timer() 
dates = pd.date_range(pd.Timestamp.min, pd.Timestamp.max)
date_mappings = pd.Series(dates, index=dates.strftime('%d/%m/%Y %H:%M'), name='date')
#date_mappings = pd.to_datetime(df.set_index('date', drop=True).date.drop_duplicates(), format='%d/%m/%Y %H:%M')
df = df.join(date_mappings, on='date', lsuffix='_str')
stop = timer()
time = stop-start
print("Tiempo invertido en pasar todo a Datetime CON hack: ", time)
print(df)