import numpy as np
import pandas as pd
import os
from pprint import pprint
import leo

baja = np.arange(-1, -5, -0.2)
compra = np.arange(0.0, 3, 0.25)
velas = np.arange(0, 19, 1)

muchos_criterios = []
for b in baja:
    for c in compra:
        for v in velas:
            muchos_criterios.append([b.round(2),c.round(2),v.round(2)])
            
df = pd.DataFrame(muchos_criterios, columns=['umbral caida compra','umbral recup venta','velas que espera'])

#df.to_csv(f"indice_combinaciones.csv", encoding='utf-8', index=True)

carpeta_actual = os.path.dirname(os.path.realpath(__file__))
carpeta_resultados = f'{carpeta_actual}/resultados-velas-1h'

lista_resultados = []
for i in os.walk(carpeta_resultados):
  for j in i[2]:
    if j[-4:] in [".csv"]:
      lista_resultados.append(j)

for i in lista_resultados:
  #df2 = pd.read_csv(f'{carpeta_resultados}/{i}', skiprows=1, header=None, names = [i[11:-4]]) #, names = [i[11:-4]]
  #df2 = df2[i[11:-4]]
  df2 = pd.read_csv(f'{carpeta_resultados}/{i}', index_col=0, header=None, skiprows=1)
  df[i[11:-4]] = df2

#print(df)    
df2 = df.drop(df.columns[[0,1,2]], axis = 1)
df2 = df2.multiply(0.001)
df2 = df2.product(axis=1)
df2 = df2.multiply((len(df.columns)-3)/12)
df['Rend. Anual'] = df2 - 1
print(df)  
os.chdir(carpeta_resultados)
df.to_csv(f"resultados.csv", encoding='utf-8', index=True)

## REGISTRO DE DATOS ESTADISTICOS EN XSLS
  
# Creo una hoja de excel y en cada ciclo armo una solapa por cada semestre
writer = pd.ExcelWriter('resultados.xlsx', engine = "xlsxwriter")

# Convierto el dataframe a un objeto de excel
df.to_excel(writer, sheet_name=f'resultados', index=False, startrow=1, header=False)

# Genero un objeto Workbook y un Worksheet de xslwriter
wb = writer.book
ws = writer.sheets[f'resultados']

# Defino formato de celdas
fmt_encabezados = wb.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold':True})
fmt_gral = wb.add_format({'align': 'center', 'text_wrap': True})
fmt_porcentaje = wb.add_format({'num_format': '0.0 %', 'align': 'center', 'text_wrap': True})
fmt_num = wb.add_format({'num_format': '0.000', 'align': 'center', 'text_wrap': True})
fmt_precio = wb.add_format({'num_format': '0.0', 'align': 'center', 'text_wrap': True})
fmt_mejores = wb.add_format({'bold': 1})
fmt_peores = wb.add_format({'bold': 1})
fmt_positivos = wb.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
fmt_negativos = wb.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
  
# Aplico formatos a las columnas
columnas = len(df.columns)
if columnas < 27:
  ultima_letra = chr(ord('@')+len(df.columns))
  anteultima_letra = chr(ord('@')+len(df.columns)-1)
else:
  cociente = columnas // 26
  resto = columnas % 26
  ultima_letra = chr(ord('@')+cociente) + chr(ord('@')+resto)
  resto = 27 if resto == 1 else resto
  if cociente == 1:
    anteultima_letra = chr(ord('@')+cociente-1) + chr(ord('@')+resto-1)
  anteultima_letra = chr(ord('@')+resto-1)

ws.set_column('A:C', 12, fmt_num)
ws.set_column(f'D:{anteultima_letra}', 10, fmt_precio)
ws.set_column(f'{ultima_letra}:{ultima_letra}', 12, fmt_porcentaje)

# Resalto los valores mas grandes de rendimiento

number_rows = len(df.index)
totales_range = f"D2:{anteultima_letra}{number_rows+1}"
rend_range = f"{ultima_letra}2:{ultima_letra}{number_rows+1}"
maximos = 50  

ws.conditional_format(totales_range, {'type': 'cell', 'criteria' : '>=', 'value': 1000, 'format': fmt_positivos})  
ws.conditional_format(totales_range, {'type': 'cell', 'criteria' : '<', 'value': 1000, 'format': fmt_negativos})  
ws.conditional_format(totales_range, {'type': 'top','value': f'{maximos}', 'format': fmt_mejores})
ws.conditional_format(totales_range, {'type': 'bottom','value': f'{maximos}', 'format': fmt_peores})
ws.conditional_format(rend_range, {'type': 'cell', 'criteria' : '>=', 'value': 0, 'format': fmt_positivos})  
ws.conditional_format(rend_range, {'type': 'cell', 'criteria' : '<', 'value': 0, 'format': fmt_negativos})  
ws.conditional_format(rend_range, {'type': 'top','value': f'{maximos}', 'format': fmt_mejores})
ws.conditional_format(rend_range, {'type': 'bottom','value': f'{maximos}', 'format': fmt_peores})
  
# Agrego encabezados
for col_num, value in enumerate(df.columns.values):
  ws.write(0, col_num, value, fmt_encabezados)

writer.save()
