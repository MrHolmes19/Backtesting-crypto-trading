import settings
import ejecutor
import os
import numpy as np
import pandas as pd
import random
from pprint import pprint
from itertools import tee
from timeit import default_timer as timer

# Importo variables preseteadas

cripto = settings.cripto
fuente = settings.fuente
n = settings.escenarios
dt = settings.intervalo_tiempo
bots = settings.bots
inicio = settings.fecha_inicio
metodo = settings.metodo
desplazamiento = settings.desplazamiento
monto_inicial = settings.inversion_inicial

def simular(cripto, fuente, n, dt, inicio, desplazamiento, metodo, *bots, monto_inicial):
    '''
    Recibe parametros de simulacion definidos en setting.py
    Genera escenarios de simulación y corre los ejecutores en cada uno
    Devuelve resultados en respectivos CSV
    '''
    ## Creo un dataframe del archivo fuente
    df = pd.read_csv(fuente)
    df = df.loc[::-1].reset_index(drop=True) # Lo doy vuelta
    
    ## Lo acoto segun metodo de simulacion para evitar errores de indexacion
    sub_df = df.copy()
    registros = n * dt * 24 * 60 if metodo == "cascada" else dt * 24 * 60
    sub_df.drop(df.tail(registros).index, inplace = True)
    
    ## Creo lista de dataframes acotados entre fechas, de acuerdo a metodo utilizado
    ultimo = len(sub_df.index)-2
    comienzo = random.randint(1, ultimo) if inicio == False or metodo == "spot" else df.index[df["date"] == inicio][0]
    escenarios_df = []
    
    for i in range(n):
        if metodo == "spot":
            final = comienzo + registros
        elif metodo == "cascada":
            final = comienzo + registros/(n-i)
        elif metodo == "desplazamiento":
            comienzo += desplazamiento * 24 * 60 if i > 0 else 0
            final = comienzo + registros    
        
        df_escenario = df.loc[comienzo:final]
        escenarios_df.append(df_escenario)

        # Comprobacion de rango de fechas
        #fecha_comienzo = df["date"][comienzo]
        #fecha_final = df["date"][final]
        #print(f'Escenario {i+1}: ', [fecha_comienzo, fecha_final])
    
    #print(escenarios_df[-1])

    ## Creacion de lista de iterables
    lista_iterable = []
    for i in escenarios_df:
        iterable = escenarios_df['date'].to_numpy().tolist()
        lista_iterable.append(iterable)

    ## Ejecucion de las simulaciones
    for iterable in lista_iterable:
        for bot in bots:
            ejecutor.ejecutar(iterable, bot, cripto, monto_inicial)
            #print(f'----- Ejecutor en escenario {escenarios_df.index(i)} con bot: ', {j} -----')
            
    return print("Simulacion finalizada exitosamente =)")


## Ejecucion de simulacro

start = timer() 

simular(cripto, fuente, n, dt, inicio, desplazamiento, metodo, *bots, monto_inicial)

stop = timer()
time = stop-start
print(f"Tiempo invertido en realizar {n * len(bots)} simulaciones, con el metodo {metodo}: ", time)

