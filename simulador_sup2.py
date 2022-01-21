import settings
import ejecutor
import comparador
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


def simular(cripto, fuente, n, dt, inicio, desplazamiento, metodo, monto_inicial, freq, *bots):
    '''
    Recibe parametros de simulacion definidos en setting.py
    Genera escenarios de simulación y corre los ejecutores en cada uno
    Devuelve resultados en respectivos CSV
    '''
    
    ## 1) Creo un dataframe del archivo fuente, y filtro por los campos de interes
    
    print("Importando base de datos...")
    
    df_base = pd.read_csv(fuente)

    try:
        cols = ['date', 'open', 'high', 'low', 'close',f"Volume {cripto}","Volume USDT","tradecount"]
        df = df_base[cols]
    except:
        return print("|---- Simulación abortada --> La base de datos ingerida no posee los campos necesarios")
    
    df = df.loc[::-1].reset_index(drop=True) # Lo doy vuelta

    ## 2) Acoto el df segun método de simulación y frecuencia para evitar errores de indexación
    sub_df = df.copy()
    
    if freq == "m":
        multiplicador = 24 * 60
    elif freq == "h":
        multiplicador = 60
    elif freq == "d":
        multiplicador = 1
    else:
        return print("|---- Simulación abortada --> Definí frecuencia de velas")    
    
    if metodo == "cascada":
        registros = n * dt * multiplicador
    elif metodo == "desplazamiento":
        registros = n * desplazamiento + multiplicador
    else:
        registros = dt * multiplicador 
    
    if registros > len(df.index):
        return print("|---- Simulación abortada --> No hay suficientes registros. Revisar frecuncia e intervalo de tiempo") 

    sub_df.drop(df.tail(registros).index, inplace = True) # recorto los ultimos registros del DF
    
    ## 3) Creación de escenarios, de acuerdo a método elegido

    ultimo = len(sub_df.index)-2
    comienzo = random.randint(1, ultimo) if inicio == False or metodo == "spot" else df.index[df["date"] == inicio][0]
    
    escenarios_df = []
    intervalos_escenarios = []
    
    for i in range(n):
        if metodo == "spot":
            final = comienzo + registros
        elif metodo == "cascada":
            final = comienzo + registros/(n-i)
        elif metodo == "desplazamiento":
            comienzo += desplazamiento * multiplicador if i > 0 else 0
            final = comienzo + registros    
        
        # Guardo lista de Dataframes
        df_escenario = df.loc[comienzo:final]
        df_escenario['date'] = pd.to_datetime(df_escenario.date)    
        df_escenario = df_escenario.set_index('date')
        escenarios_df.append(df_escenario)        
        
        # Guardo lista intervalos
        fecha_inicio = df["date"][comienzo]
        fecha_final = df["date"][final]
        intervalos_escenarios.append([fecha_inicio, fecha_final])
    
    ## 4) Creo lista de iterables para optimizar eficiencia de ciclado en ejecución
    lista_iterable = []
    for escenario_df in escenarios_df:
        #iterable = escenario_df['date'].to_numpy().tolist()
        #iterable = escenario_df.index.to_numpy().tolist()
        iterable = escenario_df.index
        lista_iterable.append(iterable)

    ## 5) Ejecución de las simulaciones
    
    print("Inicio de simulación...")

    for i, iterable in enumerate(lista_iterable):
        for bot in bots:
            df_escenario = escenarios_df[i]
            print(f"---> Ejecuciones sobre escenario: {iterable[0]} al {iterable[-1]} <---")
            ejecutor.ejecutar(bot, cripto, monto_inicial, df_escenario, iterable)
            
    print("Ejecuciones realizadas exitosamente =)")
    
    ## 6) Creo estructura de carpetas y muevo
    
    print("Ordenando en carpetas...")
        
    carpeta_simulacion = f"Simulacion-{datetime.now().strftime('%d-%m-%Y %Hh-%Mm')}"
    os.mkdir(carpeta_simulacion)
    
    carpetas_escenarios = []
    for i, iterable in enumerate(lista_iterable):
        fecha_inicial = iterable[0].strftime("%d-%m-%Y")   
        fecha_final = iterable[-1].strftime("%d-%m-%Y")    
        carpeta_escenario = f'Escenario-{fecha_inicial}_{fecha_final}'
        carpetas_escenarios.append(carpeta_escenario)
        os.mkdir(f"{carpeta_simulacion}/{carpeta_escenario}")
        
        for bot in bots:
            raiz = os.path.dirname(os.path.realpath(__file__))   
            carpeta_ejecucion = f'Ejecucion-{bot}_{fecha_inicial}_{fecha_final}'
            shutil.move(os.path.join(raiz,carpeta_ejecucion), os.path.join(raiz,carpeta_simulacion, 
                                                                           carpeta_escenario, bot))
        
    ## 7) Genero archivo con los resultados y las conclusiones
        
    print("Generando comparativa de resultados...")
    
    comparador.Comparar(carpeta_simulacion, carpetas_escenarios, intervalos_escenarios, cripto, bots)
            
    return print("Simulación finalizada. Vuelva pronto")


## ---------------------------------- Ejecucion de simulacro --------------------------------------------

start = timer() 

simular(cripto, fuente, n, dt, inicio, desplazamiento, metodo, monto_inicial, freq, *bots)
stop = timer()
time = stop-start
print(f"Tiempo invertido en realizar {n * len(bots)} simulaciones, con el metodo {metodo}: ", time)

