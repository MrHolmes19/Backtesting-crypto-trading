from binance.client import Client
import config
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import graficar
from timeit import default_timer as timer



def criterio_estadistico(df, compra, venta, Max_Velas):
    
    #df = pd.read_csv("28days_1Minute_Kline.csv", index_col=['date'], parse_dates=True)
    
    df = df.drop(df.columns[[0, 1, 2, 4]], axis=1)
    
    
    # El cociente de vela0/vela1, relativizado a %
    df["dif_1Kline"] = ((df["close"]/df["close"].shift(1))-1)*100
    df["dif_1Kline"].round(3)
    
    # Define una compra, segun el umbral
    df["comprar"] = np.where(df["dif_1Kline"] < compra, "comprar", None)
    df["vender"] = np.where(df["dif_1Kline"] > venta, "vender", None)
    
    conditions = [
        (df["comprar"] == "comprar"),
        ((df["vender"] == "vender") & (df["comprar"] != "comprar"))]
    choices = ['comprar', 'vender']
    df['criterio'] = np.select(conditions, choices, default=None)
    
    # le doy un criterio de venta luego de Max_Velas velas de comprar
    df["criterio"] = np.where((df["criterio"].shift(Max_Velas) == "comprar") & (df["criterio"] != "comprar"), "vender", df["criterio"])
    
    # Completo todos los espacios vacios, que corresponderian a "holdear", con el dato mas proximo que tenga por encima
    df["criterio"] = df["criterio"].ffill()
    # Elimino cualquier valor, que tenga por encima un valor identico a si mismo
    df["criterio"] = np.where(df["criterio"] != df["criterio"].shift(1), df["criterio"], None)
    
    # Elimino ventas generadas por ser las vela maxima luego de una compra, pero de una orden de compra q se elimino por duplicacion
    df["criterio"] = np.where(((df["criterio"] == "vender") & (df["dif_1Kline"] < venta) & (df["criterio"].shift(Max_Velas) != "comprar")), None, df["criterio"])
    
    # le doy un criterio de venta luego de Max_Velas velas de comprar. Si otra vez lo mismo, es necesario
    df["criterio"] = np.where((df["criterio"].shift(Max_Velas) == "comprar") & (df["criterio"] != "comprar"), "vender", df["criterio"])
 
# No se si hace falta repetir esto. Chequear cuando estes mas fresco
    # Completo todos los espacios vacios, que corresponderian a "holdear", con el dato mas proximo que tenga por encima
    df["criterio"] = df["criterio"].ffill()
    # Elimino cualquier valor, que tenga por encima un valor identico a si mismo
    df["criterio"] = np.where(df["criterio"] != df["criterio"].shift(1), df["criterio"], None)
    return df


def ejecutar(monto_inicial, criterios, inicio, fin, file):
    
    try:
        file = file.loc[inicio:fin]
    except:
        raise Exception("Error en las fechas del intervalo")
    
# Genero un df con una columna de compra y venta segun criterio estadistico
    df = criterio_estadistico(file, criterios[0], criterios[1], criterios[2])
    

    # Genero un slice del dataframe, eliminando los valores vacios
    df_transacciones = df[df["criterio"].notnull()]
    # Me quedo solo con las columnas que me interesan y genero las que voy a utilizar
    df_transacciones = df_transacciones[["close", "criterio"]]
    df_transacciones["USDT"] = ""
    df_transacciones["BTC"] = ""
    df_transacciones["tenencia_USD"] = ""


    for i in df_transacciones.index:
        if df_transacciones.loc[i]["criterio"] == "comprar":
            break
        if df_transacciones.loc[i]["criterio"] == "vender":
            #df_transacciones.loc[i]["criterio"] = None
            df_transacciones.drop(index=i, inplace=True)

    # Realizo un ciclado sobre el dataframe de las operaciones, simulando las conversiones de dinero
    USDT = monto_inicial
    for i in df_transacciones.index:
        if df_transacciones["criterio"][i] == "comprar":
            BTC = 0.99925*USDT/df_transacciones["close"][i]
            USDT = 0
            df_transacciones.at[i, "BTC"] = BTC
            df_transacciones.at[i, "USDT"] = USDT
            df_transacciones.at[i, "tenencia_USD"] = BTC*df_transacciones["close"][i]
        
        if df_transacciones["criterio"][i] == "vender":
            USDT= 0.99925*BTC*df_transacciones["close"][i]
            BTC = 0
            df_transacciones.at[i, "BTC"] = BTC
            df_transacciones.at[i, "USDT"] = USDT
            df_transacciones.at[i, "tenencia_USD"] = USDT
    #return df_transacciones, df
    try:
        return df_transacciones.iloc[-1]["tenencia_USD"]
    except:
        return monto_inicial
    
if __name__=="__main__":
    
    #df = graficar.getHistoric(crypto="BTCUSDT", kline=Client.KLINE_INTERVAL_1MINUTE, periodo="5-1-2018 0:00:00 - 4-2-2018 14:01:00")
    #df.to_csv("28days_1Minute_Kline.csv")
    #file = "28days_1Minute_Kline.csv"
    file = "Binance_BTCUSDT_5m.csv"
    
    df_total = pd.read_csv(file, index_col=['date'], parse_dates=True)
    #df_total = df_total[::-1]

    
    baja = np.arange(-1, -5, -0.2)
    compra = np.arange(0.0, 3, 0.25)
    velas = np.arange(0, 19, 1)
    
    muchos_criterios = []
    for b in baja:
        for c in compra:
            for v in velas:
                muchos_criterios.append([b.round(2),c.round(2),v.round(2)])
    
    
    # meses = ["01-01-2020","01-02-2020","01-03-2020","01-04-2020","01-05-2020","01-06-2020",
    #          "01-07-2020","01-08-2020","01-09-2020","01-10-2020","01-11-2020","01-12-2020",
    #          "01-01-2021","01-02-2021","01-03-2021","01-04-2021","01-05-2021","01-06-2021",
    #          "01-07-2021","01-08-2021","01-09-2021","01-10-2021","01-11-2021","01-12-2021",]
    
    meses = ["01-01-2021","01-02-2021","01-03-2021","01-04-2021","01-05-2021","01-06-2021",
             "01-07-2021","01-08-2021","01-09-2021","01-10-2021","01-11-2021","01-12-2021",]
    
    ''' # Correr un solo periodo
    inicio = meses[11]
    fin = meses[11+1]
    
    start = timer()
    result= np.array([])
    for i, crit in enumerate(muchos_criterios):
        result = np.append(result, ejecutar(1000, crit, inicio, fin, df_total))
        if i % 100 == 0:
            print(f'Simulacion {i} de {len(muchos_criterios)}')
    
    df_results = pd.DataFrame(result)
    df_results.round(2).to_csv(f'resultados2/resultados_{inicio}-{fin}.csv')
    stop = timer()
    time = stop-start
    print("Tiempo de ejecucion: ", time)
    '''
    
    for i in range(0,11):
        if i+1 != len(meses):
            inicio = meses[i]
            fin = meses[i+1]
            
            start = timer()
            result= np.array([])
            for i, crit in enumerate(muchos_criterios):
                result = np.append(result, ejecutar(1000, crit, inicio, fin, df_total))
                if i % 100 == 0:
                    print(f'Simulacion {i} de {len(muchos_criterios)}')
            
            df_results = pd.DataFrame(result)
            df_results.round(2).to_csv(f'resultados-velas-1h/resultados_{inicio}_{fin}.csv')
            stop = timer()
            time = stop-start
            print("Tiempo de ejecucion: ", time)
        
    
    '''
    for i in range(15,23):
        if i+1 != len(meses):
            inicio = meses[i]
            fin = meses[i+1]
            
            start = timer()
            result= np.array([])
            for i, crit in enumerate(muchos_criterios):
                result = np.append(result, ejecutar(1000, crit, inicio, fin, df_total))
                if i % 100 == 0:
                    print(f'Simulacion {i} de {len(muchos_criterios)}')
            
            df_results = pd.DataFrame(result)
            df_results.round(2).to_csv(f'resultados2/resultados_{inicio}-{fin}.csv')
            stop = timer()
            time = stop-start
            print("Tiempo de ejecucion: ", time)
    '''

