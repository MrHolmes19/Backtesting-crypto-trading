from datetime import datetime
import pandas as pd
import os
import recortar_CSV
import graficador
import recortar_CSV
import indicadores
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

'''
carpeta_actual = os.path.dirname(os.path.realpath(__file__))
#carpeta_resultados = f'{carpeta_actual}/resultados-velas-5min'
df = pd.read_csv(f'{carpeta_actual}/df_order_book_20200817.csv')

print(df.head(30))

df2 = df.iloc[2000:3000]
print(df2)

df2.to_csv(f"orderbook_2020-08-17_23-10-15.csv", encoding='utf-8', index=True)

'''

inicio = '22/04/2021 06:30:00'
fin = '25/04/2021 06:30:00'

nombre_origen = 'Binance_BTCUSDT_m' # Sin extension .csv
nombre_final = f'{nombre_origen}_{inicio[:10].replace("/","-")}_{fin[:10].replace("/","-")}.csv'  # Sin extension .csv
#-------------------------------

df2 = recortar_CSV.recortar_df(nombre_origen, nombre_final, inicio, fin) #, csv = True

df2 = indicadores.SMA(df2,cicles=7)
df2['ma_7'] = df2['close'].rolling(7).mean().round(1)
graficador.candlestickGraph(df2, f'BTC en Velas de 1 min', "ma_7")

