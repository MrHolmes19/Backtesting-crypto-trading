
import csv
import os
from datetime import datetime
import pandas as pd
from pprint import pprint

def Comparar(dir_simulacion, carpetas_escenarios, intervalos_escenarios, cripto, bots):
  
  ## 1) Me muevo a la carpeta de la simulación

  carpeta_actual = os.path.dirname(os.path.realpath(__file__))
  carpeta_simulacion = f"{carpeta_actual}/{dir_simulacion}"
  os.chdir(carpeta_simulacion)

  ## 2) Inicializo diccionario con encabezados que representan los indicadores que me interesan
  
  dict_resultados = {"Escenario": "", "Desde": "", "Hasta": "", "Bot": "", "Par": "","Tenencia Inicial": "", 
                     "Tenencia Final": "", "Rendimiento % Periodo": "", "Rendimiento % Anualizado": "",
                     "Cant. transacciones": "", "Cant. señales": "", "Tenencia Min": "", "Tenencia Max": ""}
  
  #encabezados = list(dict_resultados.keys())
  
  ## 3) Ciclo cada una de las ejecuciones durante la simulacion
  
  list_dict_resultados = []
  
  for i, carpeta_escenario in enumerate(carpetas_escenarios):
    
    for bot in bots:

      dict_resultados = dict_resultados.copy()
      
      ## 4) Convierto a dataframe cada CSV involucrado
      
      carpeta_resultados = f'{carpeta_simulacion}/{carpeta_escenario}/{bot}'
      df_billetera = pd.read_csv(f"{carpeta_resultados}/billetera.csv")
      df_historia = pd.read_csv(f"{carpeta_resultados}/historia.csv")
      df_transacciones = pd.read_csv(f"{carpeta_resultados}/transacciones-BTC.csv") # Cambiar nombre de archivo transacciones
      
      ## 5) Completo diccionario con los indicadores de cada CSV
      
      dict_resultados["Escenario"] = i + 1      
      
      fecha_inicial = intervalos_escenarios[i][0]
      fecha_final = intervalos_escenarios[i][-1]
      
      dict_resultados["Desde"] = datetime.strftime(fecha_inicial, "%d/%m/%Y %H:%M")
      dict_resultados["Hasta"] = datetime.strftime(fecha_final, "%d/%m/%Y %H:%M")
      
      dict_resultados["Bot"] = bot
      dict_resultados["Par"] = f"USDT/{cripto}"
      
      tenencia_inicial = df_billetera["Tenencia en USDT"].iloc[0]           
      dict_resultados["Tenencia Inicial"] = tenencia_inicial
      
      tenencia_final_usdt = df_billetera["Tenencia en USDT"].iloc[-1]
      tenencia_final_cripto = df_billetera[f"Tenencia en {cripto}"].iloc[-1]
      
      index = df_historia[df_historia["date"] == str(fecha_final)].index
      cierre_fecha_final = df_historia.at[index[0],'close']
      tenencia_final = tenencia_final_usdt + tenencia_final_cripto * cierre_fecha_final      
      dict_resultados["Tenencia Final"] = round(float(tenencia_final),2)
      
      rendimiento_periodo = round((float(tenencia_final)/float(tenencia_inicial) - 1) * 100, 2)
      dict_resultados["Rendimiento % Periodo"] = rendimiento_periodo
             
      proyeccion_anual = rendimiento_periodo * (365/(fecha_final - fecha_inicial).days)      
      dict_resultados["Rendimiento % Anualizado"] = round(float(proyeccion_anual),2)
      
      dict_resultados["Cant. transacciones"] = len(df_transacciones.index)      
      dict_resultados["Cant. señales"] = len(df_historia[df_historia["criterio"] != "Holdear"].index)
      
      ## 6) Agrego a la lista de diccionarios
      list_dict_resultados.append(dict_resultados)
      
  ## 7) Convierto lista de diccionarios a dataframe (Forma mas eficiente)
 
  df_resultados = pd.DataFrame.from_dict(list_dict_resultados)    
      
  ## 8) Guardo dataframe de resultados en un CSV
          
  df_resultados.to_csv("resultados.csv", encoding='utf-8', index=False)
  
  '''
  with open(f'resultados.csv', "w", newline="") as resultados:
  writer = csv.writer(resultados)
  writer.writerow(encabezados)
  ''' 
  
if __name__=="__main__":
    '''
    Permite correr el comparador, para hacer pruebas.
    '''
    pass