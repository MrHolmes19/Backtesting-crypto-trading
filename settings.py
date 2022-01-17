import os

## 1) Cripto con la que vamos a trabajar
cripto = "BTC"

## 2) Fuente de la base de datos principal (Historial de valores para x cripto)
fuente = f'{os.path.dirname(os.path.realpath(__file__))}\historial-{cripto}.csv'

## 3) Cantidad de escenarios en los que vamos a correr la simulación (Cant. de intervalos de tiempo)
escenarios = 1

## 4) Longitud del intervalo de tiempo (En dias)
intervalo_tiempo = 30

## 5) Fecha de inicio preseteada (Pasar String o False)
fecha_inicio = "01/01/2021 00:00"
#fecha_inicio = False

## 6) Tipo de selección de intervalos 
    #   --> Spot: intervalos independientes
    #   --> cascada: intervalos en aumento desde fecha inicio
    #   --> Desplazamiento: Intervalo que se desplaza un delta T por vez
#metodo = "spot"
#metodo = "cascada"
metodo = "desplazamiento"

## Desplazamiento en dias (Siempre activo, solo hace efecto en el metodo desplazamiento)
desplazamiento = 7


## 7) Lista de bots que participan en la simulacion
bots = [
    "bot1",
    "bot2",
    "bot3",
    "bot4",
    "bot5",
]

## 8) Dinero inicial que se carga a la billetera
inversion_inicial = 1000