import os
import numpy as np
import pandas as pd
import random
from pprint import pprint
from timeit import default_timer as timer
import exchange

## -------------- PARAMETROS QUE LLEGARIAN DESDE SIMULADOR.PY: ---------------
bot = "bot1"
cripto = "BTC"

df = pd.read_csv("C:/Users/SUSTENTATOR SA/Desktop/Documentos/Programacion/Curso Python UNSAM/Proyecto final - Bot trading/Repo Github/TradeingBot/historial-BTC.csv")
df = df.loc[::-1].reset_index(drop=True) # Doy vuelta el dataframe
#df = df.loc[1:10080] # Una semana
#df = df.loc[1:43200] # Un mes
#df = df.loc[1:525960] # Un año            
#df = df['date'].to_frame().head(10) # Algunos registros para prueba

# Hasta que jack me arregle el csv de indicadores:
indice_inicio = df[df['date'] == "12/11/2021 00:00"].index[0]
indice_fin = df[df['date'] == "12/11/2021 01:35"].index[0]
df = df.loc[indice_inicio: indice_fin]

periodo = df['date'].to_numpy().tolist()
inicio = periodo[0]
fin = periodo[-1]
print(periodo)

# QUITAR - ES DE PRUEBA (SIMULA EL ANALIZADOR)
def analizador(indicadores, criteriosBot):
    lista = ["comprar", "vender", "holdear"]
    return lista[random.randint(0, 1)]

## ----------------------------------------------------------------------------

def ejecutar(periodo, bot, cripto):
    
    ## Genero Dataframe de indicadores
    df_indicadores = pd.read_csv("C:/Users/SUSTENTATOR SA/Desktop/Documentos/Programacion/Curso Python UNSAM/Proyecto final - Bot trading/Repo Github/TradeingBot/indicadores.csv")    
    df = df_indicadores.loc[::-1].reset_index(drop=True) # Doy vuelta el dataframe (Esto deberia venir ordenado ya)
    df = df[df['date'].between(inicio, fin)]  # Filtro entre las 2 fechas del periodo
    df = df.set_index('date')
    #df = df.loc[fin:inicio]
    df["criterio"] = ""
    df["transaccion"] = ""
    df["monto"] = ""
    print(df)
    ## Creo una billetera para la cripto en cuestion
    cex = exchange.Exchange("billetera", cripto)
    cex.crearBilletera()    
        
    ## Ciclo fecha por fecha
    for i in periodo:
        ## METER ACA LOGICA DE ENTRADA (En lugar de comprar al minuto 0)
        #   Una opcion podria ser que ingrese dinero en lugar de la primera compra
        if periodo.index(i) == 0:
            cex.ingresar("USDT", 1000, i)
        
        criterio = analizador(periodo, bot)
        print("criterio: ", criterio)
        df.at[i, 'criterio'] = criterio
        
        #precio = df.get_value(i, 'close')
        precio = df['close'][i]
        
        if criterio != "holdear":
            tenencia_usdt = cex.tenencia("USDT")
            print("usdt: ", tenencia_usdt)
            tenencia_cripto = cex.tenencia(cripto)
            print("btc: ", tenencia_cripto)
        
            if criterio == "comprar" and tenencia_usdt > 0:
                monto_usdt = tenencia_usdt # Construir logica de fraccionado
                cex.comprar(cripto, monto_usdt, precio, i)
                df.at[i, 'transaccion'] = "compra"
                
            if criterio == "vender" and tenencia_cripto > 0:
                "Entré"
                monto_cripto = tenencia_cripto # Construir logica de fraccionado
                cex.vender(cripto, monto_cripto, precio, i)
                df.at[i, 'transaccion'] = "venta"  
                      
        else:
            df.at[i, 'transaccion'] = "NA"

    ## Guardo Dataframe en un csv

start = timer()
ejecutar(periodo, bot, cripto)
stop = timer()
time = stop-start
print("Tiempo en recorrer: ", time)