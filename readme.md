
[*Leer esto en español*](https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/leeme.md)

# BACKTESTING FOR TRADING PLATFORM

## PROJECT SUMMARY

### <ins>Presentation</ins>

This platform is used to test different trading strategies, on any financial asset (cryptocurrencies), on past data (From 2017 to the present). It is based on indicators, although the code can be modified allowing the strategies to become more complex.


### <ins>Applied technologies</ins>

It was developed entirely in Python and its data management libraries (Pandas, Numpy, Matplotlib, etc).


### <ins>Authors</ins>

Work done in collaboration, by:
- Leandro Marquez (lnmarquez19@gmail.com)
- Andres Muzlera (amuzlera@gmail.com)


## BUILDING OF THE PLATFORM

### Operating diagrams

#### <ins>Execution layer</ins>

It allows running a particular simulation, being able to choose:
* Cryptocurrency
* Candle frequency
* Starting amount
* Bot (containing buy and sell criteria)
* Start and end dates

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/images/execution-diagram.png?raw=true" width="800" align="center"> </p>

#### <ins>Simulation Layer</ins>

It allows running a series of simulations simultaneously, being able to choose:
* Cryptocurrency
* Candle frequency
* Starting amount
* List of Bots (containing buy and sell criteria)
* Number of scenarios to simulate
* Sampling method
* Start and end dates

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/images/simulation-layer-diagram.png?raw=true" width="800" align="center"> </p>

### Code explanation

| File | Function |
| ------------- | :------------- |
| generadorHistorico.py: | It allows downloading from the Binance API a dataset with market values ​​of some crypto, between certain dates and with a certain interval of candles. This dataset is the one taken by the file ejecutor.py |
| indicadores.py: | Receives a dataframe with market values ​​and returns another with different indicators for each record |
| analizador.py: | It is the brain of the bot. For each record, it crosses the indicator values ​​with the reference values ​​of each criterion, and decides an action: hold, buy or sell |
| criterios.py: | It contains a dictionary where the different bots appear, and the buying and selling criteria for each one. For each strategy the values ​​of this file and the interpretation of the analyzer must be modified|
| exchange.py: | Simulate the operation of an exchange. It allows to create wallets, enter and withdraw money and execute transactions, as if it were a trading platform |
| graficador.py: | It contains functions to illustrate the variation of prices (translated into a candlestick chart), as well as various indicators (moving averages, square averages, RSI, Bollinger bands, etc.) and buy and sell marks executed |
| ejecutor.py: | It cycles record by record through the dataset of market values ​​and indicators and in each one it executes the action dictated by the analyzer, through the functions of the exchange. When the cycle ends, it registers the movements (transactions, amounts in the virtual wallet and criteria history). Optionally allows you to print a graph. It can be executed from the same file in case you want to execute a particular criterion |
| settings.py: | Contains simulation settings |
| comparador.py: | Analyze the results of a series of executions within the framework of a simulation and deliver an excel file indicating the performance of each bot. |
| simulador.py: | Taking the configuration from the settings file, it runs various executions in different scenarios and with different criteria (or bots). Organize all the logs into a folder structure and then run the comparer file to generate the findings. |

## RESULTS DELIVERED

### Records of transactions, holding and decision history

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/images/resultados-carpetas.png?raw=true" width="400" align="center"> </p>

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/images/resultados-csv.png?raw=true" width="400" align="center"> </p>

### comparative table of results

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/images/resultados-comparacion-xls.png?raw=true" width="800" align="center"> </p>

### Graphics

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/images/resultados-plot2.png?raw=true" width="800" align="center"> </p>


## USAGE

1) Run generadorHistorico.py file between certain dates (This may take a while).
2) Modify the file criterios.py with the buy and sell threshold values, as well as the indicators. (As the code is, it will only recognize RSI, averages and Bollinger Bands). If you want to add others, you must modify the code in indicadores.py and analizador.py.
4) Modify the file settings.py choosing the combination of parameters that you want to test
(Note that the test interval must be within the existing range in the downloaded dataset).
5) Run the file simulador.py (It may take a long time if very long dates, very small candles, many scenarios, large intervals or many different bots are chosen).
5.alt) Run the file ejecutor.py to test a single case.
6) Observe the results


## BACKTESTING PLATFORM 2.0

We developed an new version of this platform, which does the same but 10, 20, 50 or 100 times faster, using Numpy instead of a loop. Not a job we can share, but we leave you the some ideas.

