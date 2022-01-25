import os

## 0) Notificaciones por terminal (De compra y venta)

notificaciones = True  # Booleano

## 1) Cripto con la que vamos a trabajar
cripto = "BTC"

## 2) Base de datos con historial en estudio (Seleccion de velas)

frequencia = "m"  # Frecuencia de velas (m: minuto / h: hora / d: dia)

BBDD = f'Binance_{cripto}USDT_{frequencia}.csv'
fuente = f'{os.path.dirname(os.path.realpath(__file__))}/{BBDD}'

## 3) Cantidad de escenarios en los que vamos a correr la simulación (Cant. de intervalos de tiempo)
escenarios = 1

## 4) Longitud del intervalo de tiempo (En dias)
intervalo_tiempo = 365

## 5) Fecha de inicio preseteada (Pasar String o False)
fecha_inicio = "01/01/2021 00:00:00"  # Formato d/m/a h:m:s
#fecha_inicio = False

## 6) Metodo de muestreo 
    #   --> Spot: intervalos independientes tomados al azar
    #   --> cascada: intervalos en aumento desde fecha inicio
    #   --> Desplazamiento: Intervalo fijo que se desplaza un delta T por vez
#metodo = "spot"
#metodo = "cascada"
metodo = "desplazamiento"

## Desplazamiento en dias (Siempre activo, solo hace efecto en el metodo desplazamiento)
desplazamiento = 30

## 7) Lista de bots que participan en la simulacion
bots = [
    "bot1",
    "bot2",
    "bot3",
    # "bot4",
    # "bot5",
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

## ---- LAS SIGUIENTES AUN NO SE USAN -----

## 9) Cantidad de fracciones del monto a operar en cada operación
fraccion = 5