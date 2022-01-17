from binance.client import Client
import config
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from matplotlib import gridspec



# Esta funcion trae un DataFrame directo de binance, por el momento no se utiliza
# Sirvio para el testeo, y en un futuro servira para tomar datos on-line

def getHistoric(crypto="ETHUSDT", kline=Client.KLINE_INTERVAL_1HOUR, periodo="1 day ago UTC-3"):
    '''
    Parameters
    ----------
    crypto : String
        Moneda a recuperar datos. Ej "ETHUSDT"
    periodo: String
        Delta de tiempo de los datos. Default: "1day ago UTC-3"

    Returns
    -------
    df : Pandas.DataFrame
        Devuelve un dataframe con el siguiente formato
        index = DateTime
        Columns = "Open", "High", "Low", "Close", "Volume"

    '''
    client = Client(config.API_KEY, config.API_SECRET)
    klines = client.get_historical_klines(crypto, kline, periodo)
    
    df = pd.DataFrame(klines,  columns=['date',
                                        'open',
                                        'high',
                                        'low',
                                        'close',
                                        'volume',
                                        'close time',
                                        'quote asset volume',
                                        'number of trades',
                                        'taker buy base asset volume',
                                        'taker buy quote asset volume',
                                        'ignore'])
    
    df = df.drop(df.columns[[6, 7, 8, 9, 10, 11]], axis=1)
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df.set_index('date', inplace=True, drop=True)
    
    df['open']   = df['open'].astype(float)
    df['high']   = df['high'].astype(float)
    df['low']    = df['low'].astype(float)
    df['close']  = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    
    return df



def candlestickGraph(df, title="", *args):
    '''
    Parameters
    ----------
    df : Pandas.DataFrame o String con ruta de csv
        Index = DateTime
        Columns Necesarias = "Open", "High", "Low", "Close"
    HistorialReal: str con ruta del archivo billetera.csv
    Si se pasa la ruta se grafican las transacciones reales.
    Si no por defaul, grafica cuando el criterio indica
        
    args: Str o List
        -Si se pasa un string para una media movil, se busca una columna que
         contenga dicho string y se graficara junto con velas.
         
        -Si el string es "bBand", Se graficas las bandas de bollinger.
        
        -Si se pasa una lista, debera cumplir el formato ["RSI", 20,80]. Se agrega 
         un subplot abajo y se grafica el RSI con los limites indicados.

    Plotea un grafico de velas con opcion a indicadores. Tambien marca eventos
    de compra o venta
    
    '''
    if type(df)== str:
        archivo = df
        fname = os.path.join(archivo)
        df = pd.read_csv(fname, index_col=['date'], parse_dates=True)
        
    #Se toman los valores de mercado en variables sencillas para graficar las velas
    t = df.index
    o = df["open"]
    h = df["high"]
    l = df["low"]
    c = df["close"] 
    
    RSI = False
    # Se chequea si hay que graficar RSI, se toman sus valores y se arma un subplot
    try:
        for i in args:
            if type(i) == list:
                for z in df.columns:
                    if "RSI" in z:
                        RSI = i
                        RSI[0]=z
    except:
        print("error al intentar graficar RSI, formato correcto : ['RSI',20,80]")            

    
    plt.figure()
    gs = gridspec.GridSpec(1, 1)            #Setea un grid inutil pero para que se pueda sobreescribir en el condicional
    ancho = 0.9*(df.index[0]-df.index[1])   # Define un ancho de vela como 0.9*invervalo X

    if RSI:                           # Si se agrega un RSI se generan subplots
        gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])          # Setea el ratio entre subplots
        ax1 = plt.subplot(gs[1])                # Setea el subplot abajo
        ax1.set_ylim(0,100)                     # Limites del eje Y
        ax1.get_yaxis().set_visible(False)      # Elimina el texto del eje Y
        plt.subplots_adjust(hspace=.0)          # Elimina el espacio entre subplots
  
        plt.plot(df[RSI[0]], color="b",linestyle="-")   # Grafica la curva de RSI
        plt.axhline(RSI[1], color="r", linestyle="--")  # Limite de sobrecompra
        plt.text(df.index[-1], RSI[1]+3, f"RSI {RSI[1]}")   
        plt.axhline(RSI[2], color="g", linestyle="--")  # Limite de sobreventa
        plt.text(df.index[-1], RSI[2]+3, f"RSI {RSI[2]}")
        plt.xticks(rotation=45, ha='right')
        ax0 = plt.subplot(gs[0], sharex = ax1)            # defino el sublot aqui, para eliminar el eje X
        ax0.get_xaxis().set_visible(False)                # Elimina el texto del eje X

        
    ax0 = plt.subplot(gs[0])            # Setea el subplot de arriba
    
    # Se generan 2 barras, una mas ancha que representa la apertura y cierre de la vela
    # La barra mas finita representa el maximo y el minimo de la vela
    # El ancho entre ambas en relacion 1:4
    color = ["green" if close_price > open_price else "red" for close_price, open_price in zip(c, o)]
    plt.bar(x=t, height=np.abs(o-c), bottom=np.min((o,c), axis=0), width=ancho, color=color)  #Esto arma el open-close con su width definido
    plt.bar(x=t, height=h-l, bottom=l, width=ancho/4, color=color) #esto arma el high-low con su width definido
    plt.xticks(rotation=45, ha='right')
    
    #Se revisan los parametros ingresados por *args y se grafican las medias y/o las bandas de bollinger
    # ES HORRIBLE este doble loop con 3 condicionales, hay q pensarlo 2 min y hacerlo lindo
    operaciones = df.index

    for i in args:
        if "ma" in i:
            plt.plot(df[i], Label=i)
            bbox_props = dict(boxstyle="square", fc=(0.6, 0.7, 0.7, 0.5), lw=1)     
            plt.text(df.index[-1], df[i][-1], i,ha="left", va="center", size=9, bbox=bbox_props)
        if "bBand" in i:
            for z in df.columns:
                if "bBand" in z:
                    plt.plot(df[z])
        if ".csv" in i:
            fname = os.path.join(i)
            transacciones = pd.read_csv(fname)
            operaciones = pd.to_datetime(transacciones["Ultima modificacion"])
        
        
    # Recorre toda la columna transacciones en busca de "Comprar" o "Vender"
    # Si encuentra un valor setea el color correspondiente, grafica una vline
    # y agrega una flecha a 45° indicando el precio
    
        
    try:
        for i in operaciones:
            if df.loc[i]["criterio"] in ["Comprar", "Vender"]:
                if df.loc[i]["criterio"] == "Vender":
                    colores = "r"
                if df.loc[i]["criterio"] == "Comprar":
                    colores = "g"
                plt.axvline(i, color=colores,linestyle="-")
                bbox_props = dict(boxstyle="rarrow", fc=(0.6, 0.7, 0.7, 0.5), ec=colores, lw=1)     # Define las propiedades de la flecha
                plt.text(i, df.loc[i]["close"], f'{df.loc[i]["close"]}', color=colores,rotation=45, ha="right", va="top", size=8, bbox=bbox_props)
    except:
        print("no hay transacciones registradas")

    plt.title(title, loc="center")
   #plt.xlabel('xlabel', fontsize=18)
    plt.ylabel('BTC/USDT', fontsize=12)
    plt.grid(alpha=0.2)
    plt.show()


