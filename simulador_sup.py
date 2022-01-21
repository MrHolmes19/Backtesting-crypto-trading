import settings
import ejecutor_sup
import os
import numpy as np
import pandas as pd
import random
from pprint import pprint
from itertools import tee
from datetime import datetime
from timeit import default_timer as timer
import shutil

# Importo variables preseteadas

BBDD = settings.BBDD
cripto = settings.cripto
fuente = settings.fuente
n = settings.escenarios
dt = settings.intervalo_tiempo
inicio = settings.fecha_inicio
metodo = settings.metodo
desplazamiento = settings.desplazamiento
bots = settings.bots
monto_inicial = settings.inversion_inicial
frac = settings.fraccion
freq = settings.frequencia


def simular(cripto, fuente, n, dt, inicio, desplazamiento, metodo, monto_inicial, *bots):
    '''
    Recibe parametros de simulacion definidos en setting.py
    Genera escenarios de simulación y corre los ejecutores en cada uno
    Devuelve resultados en respectivos CSV
    '''
    ## -->>> ESTA Todo PENSADO EN EN REGISTROS - CAMBIAR A FECHAS (MAS PRECISO Y SENCILLO DE ENTENDER)
    
    ## Creo un dataframe del archivo fuente
    df = pd.read_csv(fuente)
    try:
        df.drop(['unix', "symbol"], axis=1, inplace=True)
    except:
        pass
    df = df.loc[::-1].reset_index(drop=True) # Lo doy vuelta
    
    ## Lo acoto segun metodo de simulacion para evitar errores de indexacion
    sub_df = df.copy()
    #registros = n * dt * 24 * 60 if metodo == "cascada" else dt * 24 * 60
    registros = n * dt if metodo == "cascada" else dt
    sub_df.drop(df.tail(registros).index, inplace = True)
    
    ## Creo lista de dataframes acotados entre fechas, de acuerdo a método elegido
    ultimo = len(sub_df.index)-2
    # print("-------------------")
    # print(df)
    # print("-------------------")
    # print(df.index[df["date"] == inicio])
    comienzo = random.randint(1, ultimo) if inicio == False or metodo == "spot" else df.index[df["date"] == inicio][0]
    escenarios_df = []
    
    for i in range(n):
        if metodo == "spot":
            final = comienzo + registros
        elif metodo == "cascada":
            final = comienzo + registros/(n-i)
        elif metodo == "desplazamiento":
            #comienzo += desplazamiento * 24 * 60 if i > 0 else 0
            comienzo += desplazamiento if i > 0 else 0
            final = comienzo + registros    
        
        df_escenario = df.loc[comienzo:final]
        print("----------- Escenario antes de meter fecha como indice ------------")
        print(df_escenario)
        df_escenario['date'] = pd.to_datetime(df_escenario.date)    
        df_escenario = df_escenario.set_index('date')
        print("----------- Escenario LUEGO de meter fecha como indice ------------")
        print(df_escenario)
        escenarios_df.append(df_escenario)

        # Comprobacion de rango de fechas
        #fecha_comienzo = df["date"][comienzo]
        #fecha_final = df["date"][final]
        #print(f'Escenario {i+1}: ', [fecha_comienzo, fecha_final])
    
    #print(escenarios_df[-1])

    ## Creo de lista de iterables
    lista_iterable = []
    for escenario_df in escenarios_df:
        #iterable = escenario_df['date'].to_numpy().tolist()
        #iterable = escenario_df.index.to_numpy().tolist()
        iterable = escenario_df.index
        print("------ITERABLE:---------")
        print(iterable)
        print("---------------")
        lista_iterable.append(iterable)

    ## Ejecucion de las simulaciones
    for i, iterable in enumerate(lista_iterable):
        for bot in bots:
            escenario = escenarios_df[i]
            print(f"----------- Ejecuciones sobre escenario: {iterable[0]} al {iterable[-1]}:")
            ejecutor2.ejecutar(bot, cripto, monto_inicial, escenario, iterable)
            
    print("Ejecuciones realizadas exitosamente =)")
    
    print("Ordenando en carpetas...")
    
    ## Creacion de estructura de carpetas
    
    carpeta_simulacion = f"Simulacion-{datetime.now().strftime('%d-%m-%Y %Hh-%Mm')}"
    os.mkdir(carpeta_simulacion)
    
    for i, iterable in enumerate(lista_iterable):
        fecha_inicial = iterable[0].strftime("%d-%m-%Y")   
        fecha_final = iterable[-1].strftime("%d-%m-%Y")    
        carpeta_escenario = f'Escenario-{fecha_inicial}_{fecha_final}'
        os.mkdir(f"{carpeta_simulacion}/{carpeta_escenario}")
        
        for bot in bots:
            raiz = os.path.dirname(os.path.realpath(__file__))   
            carpeta_ejecucion = f'Ejecucion-{bot}_{fecha_inicial}_{fecha_final}'
            shutil.move(os.path.join(raiz,carpeta_ejecucion), os.path.join(raiz,carpeta_simulacion, 
                                                                           carpeta_escenario,carpeta_ejecucion))
            
    print("Generando comparativa de resultados...")
            
    return print("Simulación finalizada. Vuelva pronto")


## Ejecucion de simulacro

start = timer() 

simular(cripto, fuente, n, dt, inicio, desplazamiento, metodo, monto_inicial, *bots)
stop = timer()
time = stop-start
print(f"Tiempo invertido en realizar {n * len(bots)} simulaciones, con el metodo {metodo}: ", time)

