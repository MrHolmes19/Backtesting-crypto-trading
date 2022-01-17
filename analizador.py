import indicadores
import graficar
import os
import pandas as pd
import criterios

def getIndicadores():
    #Levanta el dataframe.csv como serie temporal
    archivo = 'Binance_BTCUSDT_d.csv'
    fname = os.path.join(archivo)
    df_raw = pd.read_csv(fname, index_col=['date'], parse_dates=True)
    
    #Filtrar por lapso de tiempo
    df_timed = df_raw['2021-01-01 00:00:00':'2021-11-03 00:00:00']
    
    #Filtra por columnas de interés
    columnasDeInteres = ['open', 'high', 'low', 'close']
    #columnasDeInteres = ['close']
    df_filtered = df_timed[columnasDeInteres]
    df_filtered = indicadores.DIFF(df_filtered,cicles=1)
    df_filtered = indicadores.SMA(df_filtered,cicles=15)
    df_filtered = indicadores.SMA(df_filtered,cicles=30)
    df_filtered = indicadores.RSI(df_filtered,cicles=10)
    indicadores.BolingerBands(df_filtered)
    return df_filtered

                            ### OJO ACA ANDY QUE ESTO SE DISPARA CUANDO LLAMO LA FUNCION DESDE EJECUTOR
#df=getIndicadores()
#df = df.iloc[::-1]



#%%

def generarIterador(df):
    for i in range(len(df)):
        yield df.iloc[i]
    


def mirarRSI(row, bot):
    '''
    Parameters
    ----------
    row : Pandas.DataSeries
        Fila de un dataseries
    bot : dict
        Diccionario con criterios de compra/venta
        Ej: "RSI": (14,25,75)  (periodo, limite sobrecompra, limite sobreventa)

    Returns
    -------
    "Compra", "Venta" o "Holdear"
        
    La fila donde se toman los parametros debe tener una columna llamada:
        "RSI_p" donde p es el periodo
        

    '''
    rsi = "RSI_"+str(bot["RSI"][0])
    minimo = bot["RSI"][1]
    maximo = bot["RSI"][2]

# tuve que agregar un [0] adelante de row[rsi] porq me tira que sino es ambiguo. Esto lo repeti en todas las funciones
# hay una incompatibilidad de formatos de como viene el row a como lo tenia pensado anteriorimente

    if row[rsi][0] > maximo:
        return "Vender"
    if row[rsi][0] < minimo:
        return "Comprar"


def mirarBbands(row, bot):
    '''
    row : Pandas.DataSeries
        Fila de un dataseries
    bot : dict
        Diccionario con criterios de compra/venta
        Ej: "bBands": (20,2,0.1)  (periodo, desviaciones estandar, tolerancia)
        La tolerancia es un valor opcional, se mueve entre 0-1 y por defecto es 0
        Una tolerancia de 0.1 resulta en que si el precio se acerca a un 10%
        de la banda activa el criterio, sin necesidad de cruzarla
    Returns
    -------
    "Compra", "Venta" o "Holdear"
    
    La fila donde se toman los parametros debe tener 3 columnas llamadas:
        "bBandsP_p"     donde p es el periodo
        "bBandUP_p"     donde p es el periodo
        "bBandsDOWN_p"  donde p es el periodo

    '''
    
    if len(bot["bBands"])==3:
        tolerancia = bot["bBands"][2]
    else:
        tolerancia = 0
    up = "bBandUp_"+ str(bot["bBands"][0])
    down = "bBandDown_"+ str(bot["bBands"][0])
   
    
    if row["close"][0] > row[up][0]*(1-tolerancia):
        return "Vender"
    if row["close"][0] < row[down][0]/(1-tolerancia):
        return "Comprar"
         
def ma_cross(row, bot):
    '''
    Parameters
    ----------
    row : Pandas.DataSeries
        Fila de un dataseries
    bot : dict
        Diccionario con criterios de compra/venta
        Ej: "maCross": (20,40)  (ma_rapida, ma_lenta)

    "Compra" o "Venta"
        
    La fila donde se toman los parametros debe tener dos columnas llamadas:
        "ma_x", "ma_y" donde x,y son ma_rapida y ma_lenta 

    '''
    fast = "ma_" + str(bot["maCross"][0])
    slow = "ma_" + str(bot["maCross"][1])

    
    if row[slow][0]>row[fast][0]:
        return "Comprar"
    if row[slow][0]<row[fast][0]:
        return "Vender"
         
def analizador(row, bot):
    '''
    row : Pandas.DataSeries
        Fila de un dataseries
    bot : dict
        Diccionario con criterios de compra/venta
        Ej: {"RSI": (10,25,75),
                "maCross": (15,30),
                "bBands": (21,2,0.1)}

    Returns
    "Compra", "Venta" o "Holdear"

    '''
    rsi = mirarRSI(row, bot)
    bband= mirarBbands(row, bot)
    ma = ma_cross(row, bot)
    if rsi == "Comprar" and bband == "Comprar" and ma == "Comprar":
        return "Comprar"
    elif rsi == "Vender" and bband == "Vender" and ma == "Vender":
        return"Vender"
    else:
        return "Holdear"
    


        
        
        
        
        
        
        
        
        
        