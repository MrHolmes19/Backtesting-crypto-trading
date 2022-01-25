from datetime import datetime
import os
import sys
from typing import Iterable
import pandas as pd
from timeit import default_timer as timer
import shutil
import exchange
import analizador
import criterios
import graficador
import indicadores

def ejecutar(bot, cripto, monto_inicial, df_base, iterable, notif):
    
    print (f"{bot} - Comienzo de ejecución...")
    ## 1) Obtengo el diccionario con los criterios del bot
    criterioBot = criterios.bots[bot]
    
    # 2) Obtengo los parametros necesarios para calcular indicadores, a partir de los criterios del bot
    rsi = criterioBot["RSI"][0]   
    ma = criterioBot["maCross"]
    bBand = criterioBot["bBands"]
    
    ## 3) Genero el DF con los indicadores correspondientes que demanda el bot
    df = indicadores.getIndicadores(df_base, rsi=rsi, ma=ma, bBand=bBand)    

    ## Sumo nuevas columnas a ese Dataframe  (Esto CREO que podria no estar)
    df["criterio"] = ""
    df["transaccion"] = ""
    df["monto"] = ""
    
    ## 4) Creo una billetera para la cripto en cuestion, e ingreso el monto inicial
    print (f"{bot} - Creación y carga de billetera")
    cex = exchange.Exchange("billetera", cripto)
    cex.crearBilletera() 
    fecha_inicial = iterable[0]   
    fecha_final = iterable[-1] 
    cex.ingresar("USDT", monto_inicial, fecha_inicial)
                   
    ## 5) Ciclo fecha por fecha
    print (f"{bot} - Empezando el ciclo...")
    
    for i in iterable:
        
        ## 6) Llamo a la funcion analizador pasandole una fila del df y un diccionario con los criterios del bot
        df_fila = df.loc[[i]]                            
        criterio = analizador.analizar(df_fila, criterioBot)
        df.at[i, 'criterio'] = criterio
        
        ## 7) Con el valor del criterio y la disponibilidad en billetera: compro, vendo o holdeo        
        if criterio != "Holdear":
            tenencia_usdt = cex.tenencia("USDT")
            tenencia_cripto = cex.tenencia(cripto)
            precio = df['close'][i]
            
            if criterio == "Comprar" and tenencia_usdt > 0:
                monto_usdt = tenencia_usdt # Construir logica de fraccionado
                cex.comprar(cripto, monto_usdt, precio, i, notif)
                df.at[i, 'transaccion'] = "compra"
                df.at[i, 'monto'] = monto_usdt
                
            if criterio == "Vender" and tenencia_cripto > 0:
                monto_cripto = tenencia_cripto # Construir logica de fraccionado
                cex.vender(cripto, monto_cripto, precio, i, notif)
                df.at[i, 'transaccion'] = "venta"  
                df.at[i, 'monto'] = monto_cripto
                      
        else:
            df.at[i, 'transaccion'] = "NA"
    
    print (f"{bot} - Fin del ciclo. Guardando resultados...")
    
    ## 8) Guardo Dataframe en un csv
    nombre_historia = f'historia.csv'
    #df = df.iloc[::-1]
    df.to_csv(nombre_historia)
    
    ## 9) Creo carpeta de la ejecucion y llevo todos los CSVs allí    
    try:
        fecha_inicial = iterable[0].strftime("%d-%m-%Y")   
        fecha_final = iterable[-1].strftime("%d-%m-%Y")    
        carpeta = f'Ejecucion-{bot}_{fecha_inicial}_{fecha_final}'
        print("carpeta: ",carpeta)
        os.mkdir(carpeta)
    except Exception as e:
        print(f"!! Error al crear carpeta Ejecucion-{bot}_{fecha_inicial}_{fecha_final}")
        sys.exit("|---- Simulación abortada --> Eliminar carpeta existente")
    
    raiz = os.path.dirname(os.path.realpath(__file__))       
    historia = f'historia.csv' # corregir esta parte, no deberia estar hardcodeado
    transacciones = f'Transacciones-{cripto}.csv'
    billetera = 'billetera.csv'
    
    csvs = [historia, transacciones, billetera]
    for csv in csvs:
        shutil.move(os.path.join(raiz,csv), os.path.join(raiz,carpeta,csv))
    
    print (f"{bot} - ¡ Ejecucion finalizada !")    
   
    
if __name__=="__main__":
    '''
    Permite correr el ejecutor desde este archivo, para hacer pruebas unitarias.
    '''
    ## Variables:
    bot = "bot5"
    cripto = "BTC"
    monto_inicial = 1000
    inicio='27/09/2021 00:00:00'
    fin='20/10/2021 17:00:00'
    frequencia = "m"  # Frecuencia de velas (m: minuto / h: hora / d: dia)
    notif = True # Muestra o no notificaciones de compra y venta
    BBDD = f'Binance_{cripto}USDT_{frequencia}.csv'
    
    ## Transformación de parámetros
    fuente = f'{os.path.dirname(os.path.realpath(__file__))}/{BBDD}'
    df_base = pd.read_csv(fuente)
    cols = ['date', 'open', 'high', 'low', 'close', 'volume', 'number of trades'] # f"Volume {cripto}","Volume USDT","tradecount"
    df = df_base[cols]
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')
    #df = df.loc[::-1].reset_index(drop=True) #(NO ES NECESARIO CON NUEVO DATASET, VIENE ORDENADO)
    inicio = datetime.strptime(inicio, "%d/%m/%Y %H:%M:%S")
    fin = datetime.strptime(fin, "%d/%m/%Y %H:%M:%S")
    df = df.set_index('date')
    df = df[inicio : fin]
    iterable = df.index
    
    ## Ejecución
    start = timer()
    ejecutar(bot, cripto, monto_inicial, df, iterable, notif)
    stop = timer()
    time = stop-start
    print("Tiempo en ejecutar: ", time)
    
    # GRAFICOS (PARA PRUEBA)
    
    
    print("Armando grafico...")
    start = timer()
    criterioBot = criterios.bots[bot]
    fecha_inicial = inicio.strftime('%d-%m-%Y')
    fecha_final = fin.strftime('%d-%m-%Y')
    archivo = f"Ejecucion-{bot}_{fecha_inicial}_{fecha_final}/historia.csv"
    archivo2 = f"Ejecucion-{bot}_{fecha_inicial}_{fecha_final}/billetera.csv"
    fname = os.path.join(archivo)
    
    #graficar.candlestickGraph(fname, f'{bot}', ["RSI", criterioBot["RSI"][1], criterioBot["RSI"][2] ], "bBands")    
    
    #graficar.candlestickGraph(fname, f'{bot}')

    #graficar.candlestickGraph(fname, f'{bot}', "bBands")   
    
    #graficar.candlestickGraph(fname, f'{bot}', ["RSI", criterioBot["RSI"][1], criterioBot["RSI"][2] ], "bBands", archivo2)
    
    print("Graficos finalizados. Fin del Test")
    
    stop = timer()
    time = stop-start
    print("Tiempo en graficar: ", time)
    
    
    