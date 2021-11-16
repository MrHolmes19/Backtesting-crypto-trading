import pandas as pd


nombre_archivo = "historial-BTC"
archivo = f'C:/Users/SUSTENTATOR SA/Desktop/Documentos/Programacion/Curso Python UNSAM/Proyecto final - Bot trading/Repo Github/TradeingBot/{nombre_archivo}.csv'

df = pd.read_csv(archivo)
df = df.loc[::-1].reset_index(drop=True)
df.to_csv("historial-BTC-invertido.csv", encoding='utf-8', index=False)