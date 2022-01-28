import os
from pprint import pprint
import fechas

## 1) Cripto con la que vamos a trabajar
cripto = "BTC"

## 2) Frecuencia de velas

frequencia = "m" # (m: minuto / h: hora / d: dia)

## 3) Cantidad de escenarios en los que vamos a correr la simulación (Cant. de intervalos de tiempo)
escenarios = 1

## 4) Longitud del intervalo de tiempo (En dias)
intervalo_tiempo = 1

## 5) Fecha de inicio preseteada (sPasar String, False para aleatorio o de la lista fechas)
fecha_inicio = "01/01/2021 00:00:00"  # Formato d/m/a h:m:s
#fecha_inicio = False
#fechas.alcista_fuerte[0]

## 6) Metodo de muestreo 
    #   --> Spot: intervalos independientes tomados al azar
    #   --> cascada: intervalos en aumento desde fecha inicio
    #   --> Desplazamiento: Intervalo fijo que se desplaza un delta T por vez
#metodo = "spot"
#metodo = "cascada"
metodo = "desplazamiento"

## Desplazamiento en dias (Siempre activo, solo hace efecto en el metodo desplazamiento)
desplazamiento = 10

## 7) Lista de bots que participan en la simulacion
bots = [
    # "bot1",
    # "bot2",
    # "bot3",
    # "bot4",
     "bot5",
    # "bot6",
    # "bot7",
    # "bot8",
    # "bot9",
    # "bot10",
    # "bot11",
    # "bot12",
    # "bot13",
    # "bot14",
    # "bot15",
]

## 8) Dinero inicial que se carga a la billetera

inversion_inicial = 1000

## 9) Notificaciones por terminal (De compra y venta)

notificaciones = True  # Booleano

## ---- LAS SIGUIENTES AUN NO SE USAN -----

## 10) Cantidad de fracciones del monto a operar en cada operación
fraccion = 5


## ---- CALCULOS AUTOMATICOS -----

# registros por dia

if frequencia == "m":
    registros_por_dia = 24*60
elif frequencia == "h":
    registros_por_dia = 24
else:
    registros_por_dia = 1

# Base de datos con registros historicos

BBDD = f'Binance_{cripto}USDT_{frequencia}.csv'
fuente = f'{os.path.dirname(os.path.realpath(__file__))}/{BBDD}'

## ---- EJECUCION CON INFORMACION DE LA CONFIGURACION -----

if __name__=="__main__":
    '''
    Imprime en consola, información sobre la configuración del simulacro.
    '''
    print("Simulación seteada con los siguientes parámetros:")
    print(f"* Inversion inicial: {inversion_inicial} USDT")
    print(f"* Par: USDT/{cripto}")
    print(f"* Frecuencia de velas: {frequencia}")
    print(f"* Escenarios en estudio: {escenarios}")
    print(f"* Intervalo de tiempo: {intervalo_tiempo} dias")
    print(f"* Fecha de inicio: {fecha_inicio}") if fecha_inicio else print("* Fecha de inicio: Aleatoria")
    if metodo == "desplazamiento":
        print(f"* Método de muestreo: {metodo} con desplazamientos de {desplazamiento} dias")
    else:
        print(f"* Método de muestreo: {metodo}")
    print(f"* Bots a correr:")
    pprint(bots)
    if metodo != "cascada":
        registros = escenarios * intervalo_tiempo * len(bots) * registros_por_dia
        print(f"* Tiempo estimado del simulacro: {round(registros/45000,1)} min o {round(registros/45000/60,1)} horas")
    else:
        registros = 0
        for i in range(escenarios):
            registros += (i + 1) * intervalo_tiempo * len(bots) * registros_por_dia
        print(f"* Tiempo estimado del simulacro: {round(registros/45000,1)} min o {round(registros/45000/60,1)} horas")
    