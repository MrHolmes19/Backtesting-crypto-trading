# BACKTESTING FOR TRADING PLATFORM


## PROJECT SUMMARY

### Presentation

This platform is used to test different trading strategies, on any financial asset (cryptocurrencies), on past data (From 2017 to the present). It is based on indicators, although the code can be modified allowing the strategies to become more complex.


### Applied technologies

It was developed entirely in Python and its data management libraries (Pandas, Numpy, Matplotlib, etc).


### Authors

Work done in collaboration, by:
- Leandro Marquez (lnmarquez19@gmail.com)
- Andres Muzlera (amuzlera@gmail.com)


## OPERATION OF THE PLATFORM

### Operating diagrams

#### Execution layer

It allows running a particular simulation, being able to choose:
* Cryptocurrency
* Candle frequency
* Starting amount
* Bot (containing buy and sell criteria)
* Start and end dates

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/execution-layer-diagram.png?raw=true" width="800" align="center"> </p>

#### Simulation Layer

It allows running a series of simulations simultaneously, being able to choose:
* Cryptocurrency
* Candle frequency
* Starting amount
* List of Bots (containing buy and sell criteria)
* Number of scenarios to simulate
* Sampling method
* Start and end dates

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/simulation-layer-diagram.png?raw=true" width="800" align="center"> </p>

### Code explanation

| File | Function |
| ------------- | :------------- |
| generatorHistorical.py: | It allows downloading from the Binance API a dataset with market values ​​of some crypto, between certain dates and with a certain interval of candles. This dataset is the one taken by the file executor.py |
| flags.py: | Receives a dataframe with market values ​​and returns another with different indicators for each record |
| parser.py: | It is the brain of the bot. For each record, it crosses the indicator values ​​with the reference values ​​of each criterion, and decides an action: hold, buy or sell |
| criteria.py: | It contains a dictionary where the different bots appear, and the buying and selling criteria for each one. For each strategy the values ​​of this file and the interpretation of the analyzer must be modified|
| exchange.py: | Simulate the operation of an exchange. It allows to create wallets, enter and withdraw money and execute transactions, as if it were a trading platform |
| plotter.py: | It contains functions to illustrate the variation of prices (translated into a candlestick chart), as well as various indicators (moving averages, square averages, RSI, Bollinger bands, etc.) and buy and sell marks executed |
| executor.py: | It cycles record by record through the dataset of market values ​​and indicators and in each one it executes the action dictated by the analyzer, through the functions of the exchange. When the cycle ends, it registers the movements (transactions, amounts in the virtual wallet and criteria history). Optionally allows you to print a graph. It can be executed from the same file in case you want to execute a particular criterion |
| settings.py: | Contains simulation settings |
| comparator.py: | Analyze the results of a series of executions within the framework of a simulation and deliver an excel file indicating the performance of each bot. |
| simulator.py: | Taking the configuration from the settings file, it runs various executions in different scenarios and with different criteria (or bots). Organize all the logs into a folder structure and then run the comparer file to generate the findings. |

## RESULTS DELIVERED

### Records of transactions, holding and decision history

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/results-folders.png?raw=true" width="800" align= "center"> </p>

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/results-csv.png?raw=true" width="800" align= "center"> </p>

### comparative table of results

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/comparison-results-xls.png?raw=true" width="800" align="center"> </p>

### Graphics

<p align="center"> <img src="https://github.com/MrHolmes19/Backtesting-crypto-trading/blob/main/results-plot2.png?raw=true" width="800" align= "center"> </p> 
Más sobre el texto fuenteSe requiere el texto fuente para obtener información adicional sobre la traducción
Enviar comentarios
Paneles laterales