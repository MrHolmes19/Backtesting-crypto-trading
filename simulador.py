import settings
import ejecutor
import comparador
import os
import numpy as np
import pandas as pd
from random import randrange
from pprint import pprint
from itertools import tee
from datetime import datetime, timedelta
from timeit import default_timer as timer
import shutil

## 0) Importo variables preseteadas

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
freq = settings.frequencia
frac = settings.fraccion
notif = settings.notificaciones

def simular(cripto, fuente, n, dt, inicio, desplazamiento, metodo, monto_inicial, freq, notif, *bots):
    '''
    Recibe parametros de simulacion definidos en setting.py
    Genera escenarios de simulación y corre los ejecutores en cada uno
    Devuelve resultados en respectivos CSV
    '''
    
    ## 1) Creo un dataframe del archivo fuente y lo acondiciono
    
    print("Importando base de datos...")
    
    df_base = pd.read_csv(fuente)
    
    # filtro por los campos de interes
    try:
        cols = ['date', 'open', 'high', 'low', 'close','volume', 'number of trades'] # f"Volume {cripto}","Volume USDT","tradecount"
        df = df_base[cols]
    except:
        return print("|---- Simulación abortada --> La base de datos ingerida no posee los campos necesarios")
    
    # Convierto columna de fecha a formato fecha
    try:    
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')
    except:
        return print("|---- Simulación abortada --> El formato de fecha del Dataset es distinto al que se espera: 'Y-M-D H:M:S'")
    
    # Lo doy vuelta
    # df = df.loc[::-1].reset_index(drop=True) # NO ES NECESARIO CON EL DATASET EXTRAIDO DE BINANCE
    
    ## 2) Acoto el df al intervalo de interés para la creación de escenarios 
    #     (Mayor eficiencia y evito errores de indexación)

    if metodo == "desplazamiento":
        dias_limite = dt + desplazamiento * n if n > 1 else dt
    elif metodo == "cascada":
        dias_limite = dt * n
    elif metodo == "spot":
        dias_limite = dt
    else:
        return print(f"|---- Simulacion abortada --> Falta definir método de estudio de escenarios")
    
    primera_fecha = df["date"].iloc[1]
    ultima_fecha = df["date"].iloc[-1]
    fecha_inicio_max = ultima_fecha - timedelta(days=dias_limite)
    if inicio and metodo !="spot":
        inicio = datetime.strptime(inicio, "%d/%m/%Y %H:%M:%S")
        if inicio > fecha_inicio_max:
            return print(f"|---- Simulacion abortada --> Para el escenario elegido, la fecha maxima de inicio es:{fecha_inicio_max}. Modifique la fecha")
    else:
        inicio = primera_fecha

    fin = inicio + timedelta(days=dias_limite)        
    
    df = df.set_index('date') # Fechas como indice
    df = df[inicio : fin]    # TOMAR QUINCE REGISTROS ANTERIORES PARA LOS INDICADORES
            
    ## 3) Creación de escenarios, de acuerdo a método elegido

    escenarios_df = []
    intervalos_escenarios = []
    
    for i in range(n):
        if metodo == "spot":
            # Fecha de comienzo aleatoria en cada caso
            rango_disp = (fecha_inicio_max - primera_fecha) * 24 * 60 * 60
            random_second = randrange(rango_disp)            
            inicio = start + timedelta(seconds=random_second).replace(hour = 0, minute = 0, second = 0)
            final = inicio + timedelta(days=dt)
        elif metodo == "cascada":
            final = inicio + timedelta(days=dt)*(i+1)
        elif metodo == "desplazamiento":
            inicio = inicio + timedelta(days=desplazamiento) if i > 0 else inicio
            final = inicio + timedelta(days=dt)   
        
        # Guardo lista de Dataframes y lista de intervalos
        df_escenario = df[inicio : final]
        escenarios_df.append(df_escenario)        
        intervalos_escenarios.append([inicio, final])
    
    ## 4) Creo lista de iterables para optimizar eficiencia de ciclado en ejecución
    lista_iterable = []
    for escenario_df in escenarios_df:
        iterable = escenario_df.index#.to_numpy() #(DEVUELVE 2021-05-12T05:10:00.000000000 VER SI SE PUEDE ARREGLAR ESTO)
        lista_iterable.append(iterable)

    ## 5) Ejecución de las simulaciones
    
    print("Inicio de simulación...")

    for i, iterable in enumerate(lista_iterable):
        for bot in bots:
            df_escenario = escenarios_df[i]
            print(f"---> Ejecuciones sobre escenario: {iterable[0]} al {iterable[-1]} <---")
            ejecutor.ejecutar(bot, cripto, monto_inicial, df_escenario, iterable, notif)
            
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

simular(cripto, fuente, n, dt, inicio, desplazamiento, metodo, monto_inicial, freq, notif, *bots)
stop = timer()
time = stop-start
print(f"Tiempo invertido en realizar {n * len(bots)} simulaciones, con el metodo {metodo}: ", time)

