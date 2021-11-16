import os
import numpy as np
import pandas as pd
from pprint import pprint
from timeit import default_timer as timer

bot = "bot1"

df = pd.read_csv("C:/Users/SUSTENTATOR SA/Desktop/Documentos/Programacion/Curso Python UNSAM/Proyecto final - Bot trading/Repo Github/TradeingBot/historial-BTC.csv")
#df = df.loc[1:10080] # Una semana
#df = df.loc[1:43200] # Un mes
#df = df.loc[1:525960] # Un año            
df = df['date'].to_frame().head() # 2 años y quitando el resto de las columnas
periodo = df['date'].to_numpy().tolist()

def ejecutar(periodo, bot):
    
    df_indicadores = pd.read_csv("C:/Users/SUSTENTATOR SA/Desktop/Documentos/Programacion/Curso Python UNSAM/Proyecto final - Bot trading/Repo Github/TradeingBot/indicadores.csv")    
    df = df_indicadores.set_index('date')
    df["criterio"] = ""
    df["transaccion"] = ""
    df["monto"] = ""
    
    for i in periodo:
        df["criterio"].loc[i] = "comprar "


ejecutar(periodo, bot)