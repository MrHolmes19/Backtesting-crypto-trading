import os
import pandas as pd
from timeit import default_timer as timer
import shutil
import exchange
import analizador
import criterios
import graficador
import indicadores_sup

def ejecutar(bot, cripto, monto_inicial, inicio, fin, BBDD):
    
    print (f"{bot} - Comienzo de ejecución...")
    ## 1) Obtengo el diccionario con los criterios del bot
    criterioBot = criterios.bots[bot]
    
    # 2) Obtengo los parametros necesarios para calcular indicadores, a partir de los criterios del bot
    rsi = criterioBot["RSI"][0]   
    ma = criterioBot["maCross"]
    bBand = criterioBot["bBands"]
    
    ## JUNTAR PUNTOS 3 Y 4
    
    ## 3) Genero el CSV donde luego se consultaran los indicadores y valores de mercado
    indicadores_sup.getIndicadores(inicio, fin, BBDD, rsi=rsi, ma=ma, bBand=bBand)
    
    ## 4) Genero Dataframe desde el CSV de indicadores
    archivo = 'indicadores.csv'
    fname = os.path.join(archivo)
    df_indicadores = pd.read_csv(fname)
    df = df_indicadores.loc[::-1].reset_index(drop=True) # Doy vuelta el dataframe
    print (f"{bot} - DF indicadores creado")
    
    ## -------- QUITAR
    ## Aca transformo el csv para igualar formato de fecha del archivo historial y el de indicadores de Jacks
    #df['date'] = df['date'].dt.strftime('%d/%m/%Y %H:%M')   # cambiar a este formato '%Y/%m/%d %H:%M'
    # Filtro entre las 2 fechas del periodo a ciclar, para no trabajar con un dataframe enorme
    #df = df[df['date'].between(inicio, fin)]  
    #df = df.iloc[1:periodo] # Acoto a una hora
    
    ## 5) Genero iterable (CAMBIAR A NP ARRAY, MAS EFICIENTE --- TOMAR ITERABLE DE SIMULADOR)
    print(df)
    df['date'] = pd.to_datetime(df.date)    
    df = df.set_index('date')
    print(df)
    df= df.iloc[0:-30] # ????
    periodo = df.index
    
    ## Sumo nuevas columnas a ese Dataframe  (Esto CREO que podria no estar)
    df["criterio"] = ""
    df["transaccion"] = ""
    df["monto"] = ""
    
    ## 6) Creo una billetera para la cripto en cuestion, e ingreso el monto inicial
    print (f"{bot} - Creación y carga de billetera")
    cex = exchange.Exchange("billetera", cripto)
    cex.crearBilletera() 
    fecha_inicial = periodo[0]   
    cex.ingresar("USDT", monto_inicial, fecha_inicial)
                   
    ## 7) Ciclo fecha por fecha, tomando decisiones
    print (f"{bot} - Empezando el ciclo...")
    for i in periodo:
        ## METER ACA LOGICA DE ENTRADA (SI CORRESPONDE) --> Primera compra de BTC estrategica
        
        ## 8) Llamo a la funcion analizador pasandole una fila del df y un diccionario con los criterios del bot
        df_fila = df.loc[[i]]                            
        criterio = analizador.analizar(df_fila, criterioBot)
        df.at[i, 'criterio'] = criterio
        
        ## 9) Con el valor del criterio y la disponibilidad en billetera: compro, vendo o holdeo
        
        if criterio != "Holdear":
            tenencia_usdt = cex.tenencia("USDT")
            #print("usdt: ", tenencia_usdt)
            tenencia_cripto = cex.tenencia(cripto)
            #print("btc: ", tenencia_cripto)
            precio = df['close'][i]
            
            if criterio == "Comprar" and tenencia_usdt > 0:
                monto_usdt = tenencia_usdt # Construir logica de fraccionado
                cex.comprar(cripto, monto_usdt, precio, i)
                df.at[i, 'transaccion'] = "compra"
                df.at[i, 'monto'] = monto_usdt
                
            if criterio == "Vender" and tenencia_cripto > 0:
                "Entré"
                monto_cripto = tenencia_cripto # Construir logica de fraccionado
                cex.vender(cripto, monto_cripto, precio, i)
                df.at[i, 'transaccion'] = "venta"  
                df.at[i, 'monto'] = monto_cripto
                      
        else:
            df.at[i, 'transaccion'] = "NA"
    
    print (f"{bot} - Fin del ciclo. Guardando resultados")
    
    ## 10) Guardo Dataframe en un csv
    nombre_historia = f'historia-{bot}.csv'
    df = df.iloc[::-1]
    #df.index = pd.to_datetime(df.index)
    #df.index = df.index.strftime('%Y/%m/%d %H:%M')
    # aqui hacer cambio de formato a '%Y/%m/%d %H:%M'
    df.to_csv(nombre_historia)
    
    ## 11) Creo carpeta de la ejecucion y llevo todos los CSVs allí    
    try:    
        carpeta = f'Ejecucion-{bot}'
        os.mkdir(carpeta)
    except:
        pass
    raiz = os.path.dirname(os.path.realpath(__file__))       
    historia = f'historia-{bot}.csv' # corregir esta parte, no deberia estar hardcodeado
    transacciones = f'Transacciones-{cripto}.csv'
    billetera = 'billetera.csv'
    
    csvs = [historia, transacciones, billetera]
    for csv in csvs:
        shutil.move(os.path.join(raiz,csv), os.path.join(raiz,carpeta,csv))
    
    # Al principio de todo deberia estar la logica que borre la carpeta ejecucion-bot 
    # (Para permitirle ejecutar el archivo sin borrar antes a mano la carpeta)
    print (f"{bot} - ¡ Ejecucion finalizada !")    
   
    
if __name__=="__main__":
    '''
    Permite correr el ejecutor desde este archivo, para hacer pruebas.
    '''
    bot = "bot2"
    cripto = "BTC"
    monto_inicial = 1000
    inicio='2021-01-01 00:00:00'
    fin='2021-12-31 00:00:00'
    #BBDD = 'historial-BTC.csv'
    BBDD = 'Binance_BTCUSDT_d.csv'

    start = timer()
    ejecutar(bot, cripto, monto_inicial,inicio, fin, BBDD)
    stop = timer()
    time = stop-start
    print("Tiempo en recorrer: ", time)
    
    # GRAFICOS (PARA PRUEBA)
    '''
    criterioBot = criterios.bots[bot]
    archivo = f'ejecucion-{bot}/historia-{bot}.csv'
    fname = os.path.join(archivo)
    graficador.candlestickGraph(fname, f'{bot}', ["RSI", criterioBot["RSI"][1], criterioBot["RSI"][2] ], "bBands")
    
    
    graficador.candlestickGraph(fname, f'{bot}')

    graficador.candlestickGraph(fname, f'{bot}', "bBands")

    graficador.candlestickGraph(fname, f'{bot}', ["RSI", criterioBot["RSI"][1], criterioBot["RSI"][2] ], "bBands")
    
    graficador.candlestickGraph(fname, f'{bot}', ["RSI", criterioBot["RSI"][1], criterioBot["RSI"][2] ], "bBands", f'ejecucion-{bot}/billetera.csv')
    '''
    
    
    
    
    
    