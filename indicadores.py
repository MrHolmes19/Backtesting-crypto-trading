# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 19:12:31 2021

@author: Gabriel Kubat Jacques, Macarena Alonso
"""
#Analizador

import pandas as pd
import os
import numpy as np

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

#-----------------------------------------------------------------------------
def DIFF(df,cicles=1, column='close', addToDf=True):
    #Diferencia de precios de una columna en X cant de ciclos
    
    #Column check
    if column not in df.columns:
        print('Error: There is no ' + str(column) + ' column in dataframe')
        return
    
    #Calcula la diferencia operando con columnas
    W_col = df[column]
    diff = W_col - W_col.shift(-cicles)
    
    if addToDf==True:
        #Arma un nombre para la columna que se va a agregar al dataframe
        name = 'Diff_'+str(cicles)+'c_'+column
        #Agrega la columna al dataframe
        df[name] = diff
        return df
    else:
        #Retorna el columna de valores resultados
        return diff
#-----------------------------------------------------------------------------
def DIFF_PORCENT(df,cicles=1, column='close', addToDf=True):
    #Diferencia de precios de una columna en X cant de ciclos
    
    #Column check
    if column not in df.columns:
        print('Error: There is no ' + str(column) + ' column in dataframe')
        return
    
    #Calcula la diferencia operando con columnas
    W_col = df[column]
    diff = (W_col - W_col.shift(-cicles))/W_col.shift(-cicles)
    
    if addToDf==True:
        #Arma un nombre para la columna que se va a agregar al dataframe
        name = '%Diff_'+str(cicles)+'c_'+column
        #Agrega la columna al dataframe
        df[name] = diff
        return df
    else:
        #Retorna el columna de valores resultados
        return diff
#-----------------------------------------------------------------------------
def DERIVATE(df, cicles=1, column='close', addToDf=True):
    #INDICADOR DE PENDIENTE DE GRÁFICO
    
    #Column check
    if column not in df.columns:
        print('Error: There is no ' + str(column) + ' column in dataframe')
        return
    
    name = 'Diff_'+str(cicles)+'c_'+column
    if name in df.columns:
        Diff_col = df[name]
    else:
        Diff_col = DIFF(df,cicles=cicles, column=column, addToDf=False)

        


    deriv = Diff_col/float(cicles)
    
    
    
    '''
    REFERENCIA:
    x1 = atPoint-1
    if x1 < 0:
        return None
    y1 = func[x1]
    x2 = atPoint
    y2 = func[x2]

    deriv = (y1-y2)/(x1-x2)
    deriv = (y2-y1)/(x2-x1)
    deriv = diff(ciclos) / ciclos
    '''
    
    if addToDf==True:
        #Arma un nombre para la columna que se va a agregar al dataframe
        name = 'Deriv_'+str(cicles)+'c_'+column
        
        #Agrega columna al dataframe
        df[name] = deriv
        return df
    
    else:
      #Retorna el columna de valores resultados
      return deriv 
#-----------------------------------------------------------------------------
def SMA(df,cicles=1, addToDf=True):
    #MEDIA MÓVIL SIMPLE - INDICADOR DE TENDENCIA
    
    #Calcula la media móvil operando con columnas
    sma = 0
    for i in range(cicles):
        sma += df.close.shift(periods=-i)
    sma /= float(cicles)
    

    
    if addToDf==True:
        #Arma un nombre para la columna que se va a agregar al dataframe
        name = 'ma_'+str(cicles)
        
        #Agrega columna al dataframe
        df[name] = sma
        return df
    
    else:
        #Retorna el columna de valores resultados
        return sma
#-----------------------------------------------------------------------------
def EMA(df,cicles=1, addToDf=True, addNewSMAToDf=False, SMA_cicles=None):
    #MEDIA MÓVIL EXPONENCIAL - INDICADOR DE TENDENCIA
    
    #Multiplicador = [2 ÷ (cantidad de períodos seleccionados + 1)] 
    EMA_multiplicator = 2.0/(float(cicles) + 1.0)
    
    if addNewSMAToDf == True:
        #Este código utiliza el SMA existente o arma uno nuevo con la misma 
        #cantidad de ciclos que el EMA y lo agrega al dataframe
        
        #Armar SMA
        if SMA_cicles == None:
            SMA_cicles = cicles
        SMA_name = 'SMA_'+str(SMA_cicles)+'c'
        if SMA_name in df.columns:
            #print("Using existing SMA")
            sma = df[SMA_name]
        else:
            SMA(df,cicles=SMA_cicles)
            #print("Creating new SMA")
            sma = df[SMA_name]
        ema = sma
    
    else:
        #Este código utiliza el SMA existente o arma uno nuevo con la misma 
        #cantidad de ciclos que el EMA y pero NO lo agrega al dataframe 
        
        #Armar SMA
        if SMA_cicles == None:
            SMA_cicles = cicles
        SMA_name = 'SMA_'+str(SMA_cicles)+'c'
        if SMA_name in df.columns:
            ema = df[SMA_name]
        else:
            ema = SMA(df,cicles=SMA_cicles, addToDf=False)
    
    
    #EMA actual = Precio de cierre * multiplicador + (1–multiplicador)*EMA (día anterior)
    
    ema = df.close * EMA_multiplicator + ema.shift(periods=-1) * (1.0-EMA_multiplicator)
    

    
    if addToDf==True:
        #Arma un nombre para la columna que se va a agregar al dataframe
        name = 'EMA_'+str(cicles)+'c'
        
        #Agrega columna al dataframe
        df[name] = ema
        return df
    
    else:
      #Retorna el columna de valores resultados
      return ema  
#-----------------------------------------------------------------------------
def RSI(df,cicles=1, addToDf=True):
    #INDICE DE FUERZA RELATIVA - OSCILADOR
    
    #RS = EMA de ‘N’ períodos alcistas / EMA de ‘N’ períodos bajistas (en valor absoluto)
    column = 'close' #CAMBIAR A EMA_Xc
    diff = DIFF(df, column=column, addToDf=False)

    
    '''
    comp = diff > 0
    pos_diff = diff[comp]
    neg_diff = diff[~comp]
    print('pos_diff:--------------------')
    print(pos_diff)
    print('neg_diff:--------------------')
    print(neg_diff)

    pos_sum = pos_diff.sum()
    neg_sum = -neg_diff.sum()
    print('pos_sum:',pos_sum)
    print('neg_sum:',neg_sum)
    '''
    mask = diff < 0
    pos_diff = diff.copy()
    pos_diff.loc[mask] = 0
    #print('POS DIFF:--------------------')
    #print(pos_diff)
    
    pos_sum = 0
    for i in range(cicles):
        pos_sum += pos_diff.shift(periods=-i)
    
    #print('POS SUM:--------------------')
    #print(pos_sum)
    
    neg_diff = diff.copy()
    neg_diff.loc[~mask] = 0
    #print('NEG DIFF:--------------------')
    #print(neg_diff)

    neg_sum = 0
    for i in range(cicles):
        neg_sum += neg_diff.shift(periods=-i)
    neg_sum *= -1.0
    #print('NEG SUM:--------------------')
    #print(neg_sum)
    
    rs = pos_sum/neg_sum
    #print('RS:',rs)

    #RSI = 100 – 100/(1 + RS)
    rsi = 100.0 - (100.0/(1.0 + rs))
    #print('RSI:--------------------')
    #print(rsi)
    
    if addToDf==True:
        #Arma un nombre para la columna que se va a agregar al dataframe
        name = 'RSI_'+str(cicles)
        
        #Agrega columna al dataframe
        df[name] = rsi
        return df
    
    else:
      #Retorna el columna de valores resultados
      return rsi
  
    
    
    '''
    DOCUMENTACIÓN DE UTILIZACIÓN:
    
    -Entre los 50 y 30 puntos: Camino niveles de sobre venta, por lo que el 
    precio podría caer bruscamente debido a la pérdida de fuerza de la tendencia
    
    -Entre los 50 y 70 puntos: Dirección hacia niveles de sobre compra, el precio 
    ha subido con fuerza pero está perdiendo potencia la tendencia alcista
    
    -Cruce 30,50 y 70: La superación de estos niveles será la que nos dará una 
    señal de trading para entrar o salir del mercado
    '''
#-----------------------------------------------------------------------------

def BolingerBands(df, window_size=21, num_of_sd=2):
    '''
    Parameters
    ----------
    close : Close price in DataSeries format
    window_size : windows for mean calculation
        DESCRIPTION. The default is 21.
    num_of_sd : standar deviation multiplication
        DESCRIPTION. The default is 2.

    Returns
    -------
    x : dataframe with close price index, with the following columns:
        "mean", "up", "down"

    '''
    close = df["close"]
    mean = close.rolling(window=window_size).mean() 
    sd = close.rolling(window=window_size).std() 
    upper_band = mean + (sd*num_of_sd) 
    lower_band = mean - (sd*num_of_sd)
    "bBandP_"+str(window_size)
    df["bBandP_"+str(window_size)]=mean
    df["bBandUp_"+str(window_size)]=upper_band
    df["bBandDown_"+str(window_size)]=lower_band
    return df


def getIndicadores(inicio='2021-03-01 00:00:00', fin='2021-11-02 00:00:00', rsi=False, ma=[], bBand=[], file='Binance_BTCUSDT_d.csv'):
    '''
    Parameters
    ----------
    inicio : Str con fecha en formato YYYY-MM-DD, optional
        DESCRIPTION. The default is '2021-03-01 00:00:00'.
    fin : Str con fecha en formato YYYY-MM-DD, optional
        DESCRIPTION. The default is '2021-11-02 00:00:00'.
    rsi : int, optional
        DESCRIPTION. Especifica el periodo del RSI. The default is False.
    ma : list, optional
        DESCRIPTION. Lista con el valor del periodo de cada media movil. The default is [].
    bBand : list, optional
        DESCRIPTION. Lista con 2 parametros, el primero fija el periodo, el segundo las desviaciones estandar. The default is [].
    file : str, optional
        DESCRIPTION. String con el nombre del archivo .csv con datos historicos del cual se quieran calcular indicadores.
        The default is 'Binance_BTCUSDT_d.csv'.

    Returns
    -------
    DataFrame con datos historicos mas indicadores
    csv con datos historicos mas indicadores
        DESCRIPTION.

    '''
    
    #Levanta el dataframe.csv como serie temporal
    archivo = 'Binance_BTCUSDT_d.csv'
    fname = os.path.join(archivo)
    df_raw = pd.read_csv(fname, index_col=['date'], parse_dates=True)
    
    #Filtrar por lapso de tiempo
    df_timed = df_raw[inicio:fin]
    
    #Filtra por columnas de interés
    columnasDeInteres = ['open', 'high', 'low', 'close']
    #columnasDeInteres = ['close']
    df_filtered = df_timed[columnasDeInteres]
    if rsi:
        df_filtered = RSI(df_filtered,cicles=rsi)
    if ma:
        for i in ma:
            df_filtered = SMA(df_filtered,cicles=i)
    if bBand:
       BolingerBands(df_filtered, bBand[0], bBand[1])
    df_filtered.to_csv("indicadores.csv")
    return df_filtered.iloc[::-1]
