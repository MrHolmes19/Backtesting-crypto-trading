import csv
import os
from datetime import datetime
import pandas as pd
from pprint import pprint
#from openpyxl.workbook import openpyxl
#from openpyxl import workbook


def Comparar(dir_simulacion, carpetas_escenarios, intervalos_escenarios, cripto, bots):
  
  ## 1) Me muevo a la carpeta de la simulación

  carpeta_actual = os.path.dirname(os.path.realpath(__file__))
  carpeta_simulacion = f"{carpeta_actual}/{dir_simulacion}"
  os.chdir(carpeta_simulacion)

  ## 2) Inicializo diccionario con encabezados que representan los indicadores que me interesan
  
  dict_resultados = {"Escenario": "", "Desde": "", "Hasta": "", "Bot": "", "Par": "","Tenencia Inicial": 0, 
                     "Tenencia Final": 0, "Rend % Periodo": 0, "Rend % Anualizado": 0,
                     "Cant. transacciones": 0, "Total señales": 0, "Señales de compra": 0, "Señales de venta": 0,
                     "Tenencia Min": 0, "Tenencia Max": 0, "Rend Hold": 0}
  
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
      
      cierre_fecha_final = df_historia['close'].iloc[-1]
      tenencia_final = tenencia_final_usdt + tenencia_final_cripto * cierre_fecha_final      
      dict_resultados["Tenencia Final"] = round(float(tenencia_final),2)
      
      rendimiento_periodo = round(float(tenencia_final)/float(tenencia_inicial) - 1, 2)
      dict_resultados["Rend % Periodo"] = rendimiento_periodo
             
      rendimiento_anual = rendimiento_periodo * (365/((fecha_final - fecha_inicial).total_seconds()/(60*60*24)))  
      dict_resultados["Rend % Anualizado"] = round(float(rendimiento_anual),2)
      
      dict_resultados["Cant. transacciones"] = len(df_transacciones.index)      
      dict_resultados["Total señales"] = len(df_historia[df_historia["criterio"] != "Holdear"].index)
      dict_resultados["Señales de compra"] = len(df_historia[df_historia["criterio"] == "Comprar"].index)
      dict_resultados["Señales de venta"] = len(df_historia[df_historia["criterio"] == "Vender"].index)
      
      interes_anual = 5   # % anual por ahorro flexible en Binance
      vs_interes = rendimiento_anual/interes_anual
      
      cierre_fecha_inicial = df_historia['close'].iloc[0]
      rendimiento_holdeando = round(cierre_fecha_final / cierre_fecha_inicial - 1, 1)
      dict_resultados["Rend Hold"] = rendimiento_holdeando
      
      ## 6) Agrego a la lista de diccionarios
      
      list_dict_resultados.append(dict_resultados)
      
  ## 7) Convierto lista de diccionarios a dataframe (Forma mas eficiente)
 
  df_resultados = pd.DataFrame.from_dict(list_dict_resultados)    
  
  ## 8) Guardo dataframe de resultados en un CSV
          
  df_resultados.to_csv("resultados.csv", encoding='latin-1', index=False)
  
  ## 9) Guardo en un .xlsx
  
  # Creo un Writer de excel con Pandas

  writer = pd.ExcelWriter('resultados.xlsx', engine = "xlsxwriter")

  # Convierto el dataframe a un objeto de excel

  df_resultados.to_excel(writer, sheet_name='resultados', index=False, startrow=1, header=False)

  # Genero un objeto Workbook y uno Worksheet de xslwriter
  wb  = writer.book
  ws = writer.sheets['resultados']
  # ws.set_zoom(90)

  # Defino formato de celdas

  fmt_encabezados = wb.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold':True})
  fmt_gral = wb.add_format({'align': 'center', 'text_wrap': True})
  fmt_numero = wb.add_format({'num_format': '0.0', 'align': 'center'})
  fmt_moneda = wb.add_format({'num_format': '$ #,##0.0', 'align': 'center', 'text_wrap': True})
  fmt_porcentaje = wb.add_format({'num_format': '0.0 %', 'align': 'center', 'text_wrap': True})
  fmt_mejores = wb.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
  fmt_peores = wb.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})

  # Aplico formatos a las columnas

  ws.set_column('A:A', 8.7, fmt_gral)
  ws.set_column('B:C', 15.6, fmt_gral)
  ws.set_column('D:D', 5.14, fmt_gral)
  ws.set_column('E:E', 9.29, fmt_gral) 
  ws.set_column('F:G', 8.71, fmt_moneda)
  ws.set_column('H:H', 8.71, fmt_porcentaje)
  ws.set_column('I:I', 10.71, fmt_porcentaje)
  ws.set_column('J:J', 12.4, fmt_gral)
  ws.set_column('K:K', 8, fmt_gral)
  ws.set_column('L:M', 9.57, fmt_gral)
  ws.set_column('N:O', 8.43, fmt_numero)
  ws.set_column('P:P', 7.43, fmt_porcentaje)

  # Resalto los valores mas grandes de rendimiento

  number_rows = len(df_resultados.index)
  color_range = f"H2:H{number_rows+1}"
  if number_rows < 5:
    resaltados = 1
  elif number_rows < 10:
    resaltados = 2
  else:
    resaltados = 3  
    
  ws.conditional_format(color_range, {'type': 'top','value': f'{resaltados}', 'format': fmt_mejores})
  ws.conditional_format(color_range, {'type': 'bottom','value': f'{resaltados}', 'format': fmt_peores})

  # Agrego encabezados (Los saqué para poder formatearlos con startrow=1, header=False)

  for col_num, value in enumerate(df_resultados.columns.values):

    ws.write(0, col_num, value, fmt_encabezados)

  # Close the Pandas Excel writer and output the Excel file.
  writer.save()
  
  '''
  with open(f'resultados.csv', "w", newline="") as resultados:
  writer = csv.writer(resultados)
  writer.writerow(encabezados)
  ''' 
  
if __name__=="__main__":
    '''
    Permite correr el comparador, para hacer pruebas.
    '''
    # carpeta_simulacion = "Simulacion-25-01-2022 17h-44m"
    # Comparar(carpeta_simulacion, carpetas_escenarios, intervalos_escenarios, cripto, bots)
    
    pass