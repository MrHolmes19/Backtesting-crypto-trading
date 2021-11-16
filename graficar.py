from binance.client import Client
import config
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import gridspec

Crypto = "ETHUSDT"
periodo = "1 day ago UTC-3"
def getHistoric(crypto, periodo=" day ago UTC-3"):
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
    klines = client.get_historical_klines(Crypto, Client.KLINE_INTERVAL_30MINUTE, periodo)
    
    df = pd.DataFrame(klines,  columns=['Date',
                                        'Open',
                                        'High',
                                        'Low',
                                        'Close',
                                        'Volume',
                                        'Close time',
                                        'Quote asset volume',
                                        'Number of trades',
                                        'Taker buy base asset volume',
                                        'Taker buy quote asset volume',
                                        'Ignore'])
    
    df = df.drop(df.columns[[6, 7, 8, 9, 10, 11]], axis=1)
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df.set_index('Date', inplace=True, drop=True)
    
    df['Open']   = df['Open'].astype(float)
    df['High']   = df['High'].astype(float)
    df['Low']    = df['Low'].astype(float)
    df['Close']  = df['Close'].astype(float)
    df['Volume'] = df['Volume'].astype(float)
    
    return df



def candlestick_Graph(df, transacciones, RSI=pd.DataFrame()):
    '''
    Parameters
    ----------
    df : Pandas.DataFrame
        Index = DateTime
        Columns = "Open", "High", "Low", "Close"
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
    o = df["Open"]
    h = df["High"]
    l = df["Low"]
    c = df["Close"] 


    ancho = 0.8/len(df.index)              # Define un ancho de vela segun la cantidad de datos que existan
    
    plt.figure()
        
    if not RSI.empty:        # Si se agrega un RSI se generan subplots
        gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1]) # Setea el ratio entre subplots
        ax0 = plt.subplot(gs[0])            # Setea el subplot arriba

    color = ["green" if close_price > open_price else "red" for close_price, open_price in zip(c, o)]
    plt.bar(x=t, height=np.abs(o-c), bottom=np.min((o,c), axis=0), width=ancho, color=color)  #Esto arma el open-close con su width definido
    plt.bar(x=t, height=h-l, bottom=l, width=ancho/4, color=color) #esto arma el high-low con su width definido
    
    
    
        
    for transaccion, colores in transacciones:
        # Se generan lineas verticales segun las transacciones realizadas
        # Ademas se agrega el texto con el precio en el instante de la transaccion
        plt.axvline(transaccion, color=colores,linestyle="-")
        plt.text(transaccion, df.loc[transaccion]["Close"]*1.015, f'{df.loc[transaccion]["Close"]}', color=colores, ha="center")
                 
    if not RSI.empty:           # Si se agrega un RSI se generan subplots
        ax1 = plt.subplot(gs[1], sharex = ax0)  # Setea el subplot abajo
        plt.subplots_adjust(hspace=.0)          # Elimina el espacio entre subplots

        plt.plot(RSI, color="b",linestyle="-") 
        plt.axhline(3600, color="r", linestyle="--")
        plt.text(df.index[1], 3600, "RSI 80")
        plt.axhline(3500, color="g", linestyle="--")
        plt.text(df.index[1], 3500, "RSI 20")

            
    plt.grid(alpha=0.2)
    plt.show()



dff=getHistoric(Crypto, periodo)   

# Simulacion de una variable con la info de transacciones
transacciones= dff.index[[1, 5, 20]] # Toma x cantidad de puntos del tiempo
transacciones=zip(transacciones,("g","r","g"))  # Los une con la data para elegir el color de compra o venta

#Simulacion de RSI
RSI = dff["Open"]*0.8



candlestick_Graph(dff, transacciones, RSI)

def medias(df, *ciclos):
    sma = []
    for ciclo in ciclos:
        if ciclo.find('SMA') != -1:
            media = int(ciclo.split('_')[1][:-1])
            sma.append(df["Close"].rolling(media).mean())

    plt.figure()
    for s in sma:
        plt.plot(s)
        plt.legend(ciclos)
    plt.show()


medias(dff, "SMA_15c",  "SMA_3C")

