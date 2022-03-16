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
df2 = df2.dropna()
df2 = df2.reset_index()

xData = np.array(df2.index)
yData = np.array(df2["ma_7"])    

# Curva polinómica ajustada a los datos de las cotizaciones.
param_ajust = np.polyfit(xData, yData, 117)

# polynomial derivative from numpy
deriv = np.polyder(param_ajust)

# valor de la derivada (pendiente) en cada valor específico de x
pendientes = []
i = 0

while i <= df2.shape[0]-1:
    # print(i)
    # print(df2.shape[0]-1)
    valor_y_del_punto = np.polyval(param_ajust, df2.index[i])
    # print(valor_y_del_punto)
    pendiente_en_el_punto = np.polyval(deriv, df2["close"][i])
    pendiente_en_el_punto = np.round(pendiente_en_el_punto, 1)
    # print(pendiente_en_el_punto)
    pendientes.append(pendiente_en_el_punto)
    i+=1
    
df2["pendientes"] =  pendientes  
print(df2)

## GRAFICO

def ModelAndScatterPlot(graphWidth, graphHeight):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    axes = f.add_subplot(111)

    # first the raw data as a scatter plot
    axes.plot(xData, yData, '.')

    # create data for the fitted equation plot
    xModel = np.linspace(min(xData), max(xData))
    yModel = np.polyval(param_ajust, xModel)

    # now the model as a line plot
    axes.plot(xModel, yModel)

    axes.set_xlabel('minutos') # X axis data label
    axes.set_ylabel('media de precios') # Y axis data label

    # for plotting
    minX = min(xData)
    maxX = max(xData)

    # value of derivative (slope) at a specific X value, so
    # that a straight line tangent can be plotted at the point
    # you might place this code in a loop to animate
    pointVal = 150 # example X value
    y_value_at_point = np.polyval(param_ajust, pointVal)
    slope_at_point = np.polyval(deriv, pointVal)
    print("La Pendiente es: ", slope_at_point)
    slope_deg = math.atan(slope_at_point) * 180 / math.pi
    print("La Pendiente es: ", slope_deg)
    ylow = (minX - pointVal) * slope_at_point + y_value_at_point
    yhigh = (maxX - pointVal) * slope_at_point + y_value_at_point

    # now the tangent as a line plot
    axes.plot([minX, maxX], [ylow, yhigh])

    plt.show()
    plt.close('all') # clean up after using pyplot

graphWidth = 800
graphHeight = 600
ModelAndScatterPlot(graphWidth, graphHeight)



#df2.to_csv(f"pendientes.csv", encoding='utf-8', index=True)
