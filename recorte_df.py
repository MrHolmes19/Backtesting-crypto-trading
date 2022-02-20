
import os
import pandas as pd

BBDD = f'variaciones_dif_historico.csv'
fuente = f'{os.path.dirname(os.path.realpath(__file__))}/{BBDD}'
  
df = pd.read_csv(fuente, index_col=['date'], parse_dates=True)

df = df.iloc[-40320:]

df.to_csv(f"prueba_borrar.csv", encoding='utf-8', index=True)