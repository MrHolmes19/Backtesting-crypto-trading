from datetime import datetime, timedelta
import os
import dateutil
import pandas as pd
from timeit import default_timer as timer
from random import randrange
import graficador
from timeit import timeit

fecha_informe = "2021-01-28 11:00:00"

fecha_informe_date = datetime. strptime(fecha_informe, '%Y-%m-%d %H:%M:%S')

'''
print(fecha_informe_date)
fecha_pro = datetime.strftime(fecha_informe_date, '%d %b %Y %H:%M')
print(fecha_pro)

#from babel.dates import format_date
import locale
locale.setlocale(locale.LC_TIME, "es_ES")
fecha_informe_date = datetime. strptime(fecha_informe, '%Y-%m-%d %H:%M:%S')
fecha_pro = datetime.strftime(fecha_informe_date, '%d %b %Y')
print(fecha_pro)
'''
'''fecha_informe2 = "2021-01-27 11:00:00"
fecha_informe2_date = datetime. strptime(fecha_informe2, '%Y-%m-%d %H:%M:%S')
print(fecha_informe2_date)

proyeccion_anual = datetime.timestamp(fecha_informe_date) - datetime.timestamp(fecha_informe2_date)
print(proyeccion_anual/60/60)   

proyeccion_anual = (fecha_informe_date - fecha_informe2_date).total_seconds()
print(proyeccion_anual/60/60)  
'''

# fecha_inicio_max = "2021-01-28 11:00:00"

# fecha_inicio_max = datetime. strptime(fecha_inicio_max, '%Y-%m-%d %H:%M:%S')

# primera_fecha = "2021-01-27 11:00:00"
# primera_fecha = datetime. strptime(primera_fecha, '%Y-%m-%d %H:%M:%S')

# rango_disp = (fecha_inicio_max - primera_fecha).total_seconds()
# random_second = randrange(int(rango_disp))    
# print(random_second)  
# inicio = start + timedelta(seconds=random_second).replace(hour = 0, minute = 0, second = 0)
# final = inicio + timedelta(days=dt)

carpeta_actual = os.path.dirname(os.path.realpath(__file__))

df_resultados = pd.read_csv(f"{carpeta_actual}/resultados.csv", encoding='latin-1')
print(df_resultados)



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