# BACKTESTING FOR TRADING PLATFORM


## RESUMEN DEL PROYECTO

### <ins>Presentación</ins>

Esta plataforma sirve para probar distintas estrategias de trading, sobre cualquier activo financieros (criptomonedas), sobre datos pasados (Desde 2017 hasta el presente). Está basado en indicadores, aunque el código puede modificarse permitiendo complejizar las estrategias.


### <ins>Tecnologías aplicadas</ins>

Fue desarrollado integramente en Python y sus librerias para manejo de datos (Pandas, Numpy, Matplotlib, etc).


### <ins>Autores</ins>

Trabajo realizado en colaboración, por:
- Leandro Márquez (lnmarquez19@gmail.com)
- Andrés Muzlera (amuzlera@gmail.com)


## CONSTRUCCION DE LA PLATAFORMA

### Esquemas de funcionamiento

#### <ins>Capa de ejecución</ins>

Permite correr una simulación en particular, pudiendo elegir:
* Criptomoneda
* Frecuencia de velas
* Monto inicial
* Bot (que contiene los criterios de compra y venta)
* Fechas de inicio y fin

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/images/diagrama-ejecutor.png?raw=true" width="800" align="center"> </p>


#### <ins>Capa de simulación</ins>

Permite correr una serie de simulaciones en simultaneo, pudiendo elegir:
* Criptomoneda
* Frecuencia de velas
* Monto inicial
* Lista de Bots (que contienen los criterios de compra y venta)
* Cantidad de escenarios a simular
* Método de muestreo
* Fechas de inicio y fin

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/images/diagrama-capa-simulacion.png?raw=true" width="800" align="center"> </p>


### Explicacion del código

| Archivo  | Función |
| ------------- | :------------- |
| generadorHistorico.py:  | Permite descargar de la API de Binance un dataset con valores de mercado de alguna cripto, entre ciertas fechas y con cierto intervalo de velas. Este dataset es el tomado por el archivo ejecutor.py |
| indicadores.py:  | Recibe un dataframe de con valores de mercado y devuelve otro con distintos indicadores por cada registro |
| analizador.py:  | Es el cerebro del bot. Para cada registro, cruza los valores de indicadores con los valores referenciales de cada criterio, y decide una acción: holdear, comprar o vender  |
| criterios.py:  | Contiene un diccionario donde figuran los distintos bots, y los criterios de compra y venta de cada uno. Para cada estrategia deben modificarse los valores de este archivo y la interpretación del analizador|
| exchange.py:  | Simula el funcionamiento de un exchange. Permite crear billeteras, ingresar y retirar dinero y ejecutar transacciones, como si fuera una plataforma de trading |
| graficador.py:  | Contiene funciones para ilustrar la variacion de precios (traducido en grafico de velas), asi como indicadores varios (medias moviles, medias cuadraticas, RSI, bandas de Bollinger, etc) y marcas de compra y venta ejecutadas  |
| ejecutor.py:  | Realiza un ciclado registro a registro a traves del dataset de valores de mercado e indicadores y en cada uno ejecuta la acción que le dicta el analizador, a traves de las funciones del exchange. Cuando termina el ciclo registra los movimientos (transacciones, montos en la billetera virtual e historial de criterios). Opcionalmente permite imprimir un grafico. Puede ser ejecutado desde el mismo archivo en caso de querer ejecutar un criterio en particular |
| settings.py:  | Contiene la configuración de la simulación |
| comparador.py:  | Analiza los resultados de una serie de ejecuciones en el marco de una simulación y entrega un archivo de excel indicando el rendimiento de cada bot. |
| simulador.py:  | Tomando la configuración del archivo settings, corre varias ejecuciones en distintos escenarios y con distintos criterios (o bots). Organiza todos los registros en una estructura de carpetas y luego ejecuta el archivo comparador para generar las conclusiones. |

## RESULTADOS ENTREGADOS

### Registros de transacciones, tenencia e historial de decisiones

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/images/resultados-carpetas.png?raw=true" width="600" align="center"> </p>

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/images/resultados-csv.png?raw=true" width="600" align="center"> </p>

### tabla comparativa de resultados

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/images/resultados-comparacion-xls.png?raw=true" width="800" align="center"> </p>

### Graficos

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/images/resultados-plot2.png?raw=true" width="800" align="center"> </p>


## USO

1) Correr archivo generadorHistorico.py entre ciertas fechas (Esto puede tardar).
2) Modificar el archivo criterios.py con los valores umbrales de compra y venta, asi como los indicadores. (Asi como está el código, solo reconocerá RSI, medias y Bandas de Bollinger). Si se quiere agregar otras, debe modificarse el codigo en indicadores.py y en analizador.py.
4) Modificar el archivo settings.py eligiendo la combinacion de parametros que se desea probar
(Tener en cuenta que el intervalo de prueba debe estar dentro del rango existente en el dataset descargado).
5) Correr el archivo simulador.py (Puede tardar si se eligen fechas muy extensas, velas muy chicas, muchos escenarios, intervalos grandes o muchos bots distintos).
5.alt) Correr el archivo ejecutor.py para testear un solo caso.
6) Observar los resultados


## BACKTESTING PLATFORM 2.0

Desarrollamos una nueva versión de esta plataforma, que hace lo mismo pero 10, 20, 50 o 100 veces más rápido, usando Numpy en lugar de ciclar registro por registro. No es un trabajo que podamos compartir, pero dejamos la idea.