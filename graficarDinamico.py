from binance.client import Client
import config
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import gridspec

Crypto = "BTCUSDT"
periodo = "3 day ago UTC-3"
def getHistoric(crypto="ETHUSDT", periodo="1 day ago UTC-3"):
    '''
    Parameters
    ----------
    crypto : String
        Moneda a recuperar datos. Ej "ETHUSDT"
    periodo: String
        Delta de tiempo de los datos. Default: "1 day ago UTC-3"

    Returns
    -------
    df : Pandas.DataFrame
        Devuelve un dataframe con el siguiente formato
        index = DateTime
        Columns = "open", "high", "low", "close", "Volume"


    '''
    client = Client(config.API_KEY, config.API_SECRET)
    klines = client.get_historical_klines(Crypto, Client.KLINE_INTERVAL_30MINUTE, periodo)
    
    df = pd.DataFrame(klines,  columns=['Date',
                                        'open',
                                        'high',
                                        'low',
                                        'close',
                                        'Volume',
                                        'close time',
                                        'Quote asset volume',
                                        'Number of trades',
                                        'Taker buy base asset volume',
                                        'Taker buy quote asset volume',
                                        'Ignore'])
    
    df = df.drop(df.columns[[6, 7, 8, 9, 10, 11]], axis=1)
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df.set_index('Date', inplace=True, drop=True)
    
    df['open']   = df['open'].astype(float)
    df['high']   = df['high'].astype(float)
    df['low']    = df['low'].astype(float)
    df['close']  = df['close'].astype(float)
    df['Volume'] = df['Volume'].astype(float)
    
    return df



def candlestick_Graph_Dinamic(df, pause=None, RSI=False):
    '''
    Parameters
    ----------
    df : Pandas.DataFrame
        Index = DateTime
        Columns = "open", "high", "low", "close"
    transacciones : List of Tuples
        [(Date of transaction, Color of line)]
        Use "g" for sells actions (green vline)
        Use "r" for buys actiones (red vline)
    RSI (Optional): Pandas.DataFrame
        Index = DateTime
        Subplot RSI indicator

    Plot with vlines indicateing sell/buy operations
    -------
    None.

    '''
    
    t = df.index
    o = df["open"]
    h = df["high"]
    l = df["low"]
    c = df["close"] 


    ancho = 0.9*(df.index[0]-df.index[1])   # Define un ancho de vela como 0.9*invervalo X
    #plt.figure()
        
    if RSI:        # Si se agrega un RSI se generan subplots
        gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1]) # Setea el ratio entre subplots
        ax0 = plt.subplot(gs[0])            # Setea el subplot arriba
        plt.xticks([])  # Si hay RSI se elimina el eje X del grafico superior

    color = ["green" if close_price > open_price else "red" for close_price, open_price in zip(c, o)]
    plt.bar(x=t, height=np.abs(o-c), bottom=np.min((o,c), axis=0), width=ancho, color=color)  #Esto arma el open-close con su width definido
    plt.bar(x=t, height=h-l, bottom=l, width=ancho/4, color=color) #esto arma el high-low con su width definido
    
    
    
    if not RSI:       # Si no hay RSI se define un eje X a 45
        plt.xticks(rotation=45, ha='right')
    
    orden =df["transaccion"][-1]
    if orden:
        if orden=="Vender":
            colores = "g"
        if orden == "Comprar":
            colores = "r"
    
        plt.axvline(df.index[-1], color=colores,linestyle="-")    
        bbox_props = dict(boxstyle="rarrow", fc=(0.6, 0.7, 0.7, 0.5), ec=colores, lw=1)     # Define las propiedades de la flecha
        plt.text(df.index[-1], df["close"][-1], f'{int(df["close"][-1])}', color=colores,rotation=45, ha="right", va="top", size=8, bbox=bbox_props)
        
                 
    if RSI:           # Si se agrega un RSI se generan subplots
        ax1 = plt.subplot(gs[1]) # Setea el subplot abajo
        ax1.set_ylim(0,100)      # Limites del eje Y
        ax1.get_yaxis().set_visible(False)  # Elimina el texto del eje Y
        plt.subplots_adjust(hspace=.0)          # Elimina el espacio entre subplots

        plt.plot(df["RSI_10c"], color="b",linestyle="-") 
        plt.axhline(RSI[0], color="r", linestyle="--")
        plt.text(df.index[-1], RSI[0], f"RSI {RSI[0]}")        # No entiendo el comportamiento del valor en X, asiq quedo asi
        plt.axhline(RSI[1], color="g", linestyle="--")
        plt.text(df.index[-1], RSI[1], f"RSI {RSI[1]}")
        plt.xticks(rotation=45, ha='right')     # se define un eje X a 45
            
    plt.grid(alpha=0.2)
    if pause:
        plt.pause(pause)

    #plt.show()

    
if __name__=="__main__":
   
    dff=getHistoric(Crypto, periodo)   
    
    # Simulacion de una variable con la info de transacciones
    transacciones= dff.index[[1, 5, 20]] # Toma x cantidad de puntos del tiempo
    transacciones=zip(transacciones,("g","r","g"))  # Los une con la data para elegir el color de compra o venta
    
    #Simulacion de RSI
    RSI = dff["open"]*0.8
    
    
    
    #candlestick_Graph_Dinamic(dff)

