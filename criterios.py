import indicadores
from graficarDinamico import candlestick_Graph_Dinamic
import os
import pandas as pd
import matplotlib.pyplot as plt


def getIndicadores():
    #Levanta el dataframe.csv como serie temporal
    archivo = 'Binance_BTCUSDT_d.csv'
    fname = os.path.join(archivo)
    df_raw = pd.read_csv(fname, index_col=['date'], parse_dates=True)
    
    #Filtrar por lapso de tiempo
    df_timed = df_raw['2021-09-01 00:00:00':'2021-11-03 00:00:00']
    
    #Filtra por columnas de interés
    columnasDeInteres = ['open', 'high', 'low', 'close']
    #columnasDeInteres = ['close']
    df_filtered = df_timed[columnasDeInteres]
    df_filtered = indicadores.DIFF(df_filtered,cicles=1)
    df_filtered = indicadores.DIFF_PORCENT(df_filtered,cicles=1)
    df_filtered = indicadores.SMA(df_filtered,cicles=3)
    df_filtered = indicadores.EMA(df_filtered,cicles=5)
    df_filtered = indicadores.DERIVATE(df_filtered, column='EMA_5c',cicles=1)
    df_filtered = indicadores.RSI(df_filtered,cicles=10)
    
    return df_filtered


df=getIndicadores()
df = df.iloc[::-1]


#%%

def generarIterador(df):
    for i in range(len(df)):
        yield df.iloc[i]
    


def mirarRSI(row, maximo, minimo):
    if row["RSI_10c"] > maximo:
        row["transaccion"] = "Vender"
        vender(row)
    elif row["RSI_10c"] < minimo:
        row["transaccion"] = "Comprar"
        comprar(row)
    else:
        row["transaccion"] = None
    return row


    

def comprar(row):
    print(f"Se realizo una compra la fecha {row.name}")
def vender(row):
    print(f"Se realizo una venta la fecha {row.name}")


if __name__=="__main__":
    
    binance = generarIterador(df)
    dff = pd.DataFrame()
    # Simulacion de una variable con la info de transacciones
    transacciones= df.index[[0]] # Toma x cantidad de puntos del tiempo
    transacciones=zip(transacciones,("g"))  # Los une con la data para elegir el color de compra o venta
    
    dff = dff.append(next(binance)) #Genero el primer valor, asi en el loop el primer ciclo tiene 2 valores. Sino tira error al calcular el ancho como x0-x1
    for i in binance:
        i = mirarRSI(i, 80, 20)
        dff = dff.append(i)
        candlestick_Graph_Dinamic(dff, 0.1)
        

    
    
    
    
    
    
    
    
    
    
    
    
    
