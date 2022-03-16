from datetime import datetime
import math
import pandas as pd
import os
import recortar_CSV
import graficador
import recortar_CSV
import indicadores
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#-------------------------------
inicio = '12/03/2020 06:30:00'
fin = '12/03/2020 10:30:00'

nombre_origen = 'Binance_BTCUSDT_m' # Sin extension .csv
nombre_final = f'{nombre_origen}_{inicio[:10]}_{fin[:10]}'  # Sin extension .csv
#-------------------------------

df2 = recortar_CSV.recortar_df(nombre_origen, nombre_final, inicio, fin)

#df2 = indicadores.SMA(df2,cicles=7)

df2 = df2[["close"]]
df2['ma_7'] = df2['close'].rolling(7).mean().round(1)

df2['slope1'] = df2['ma_7']-df2['ma_7'].shift(1)
df2['slope1_deg'] = (np.arctan(df2['slope1']) * 180 / math.pi).round(1)

print(df2)
#df2.to_csv(f"pendientes.csv", encoding='utf-8', index=True)
