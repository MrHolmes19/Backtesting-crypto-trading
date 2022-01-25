from datetime import datetime, timedelta
import os
import dateutil
import pandas as pd
from timeit import default_timer as timer
from random import randrange
import graficador

fecha_informe = "2021-01-28 11:00:00"
print(fecha_informe)
fecha_informe_date = datetime. strptime(fecha_informe, '%Y-%m-%d %H:%M:%S')
print(fecha_informe_date)
fecha_pro = datetime.strftime(fecha_informe_date, '%d %b %Y %H:%M')
print(fecha_pro)

#from babel.dates import format_date
import locale
locale.setlocale(locale.LC_TIME, "es_ES")
fecha_informe_date = datetime. strptime(fecha_informe, '%Y-%m-%d %H:%M:%S')
fecha_pro = datetime.strftime(fecha_informe_date, '%d %b %Y')
print(fecha_pro)