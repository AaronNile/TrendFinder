# TrendFinder

Python program that analyzes trend for a given stock in the NYSE. 


## Analysis Approach
The technique used to identify the trend of the inputted security is a Moving-Average crossover,
commonly used in technical analysis. 
A 50 day Simple Moving Average (SMA) is used to smooth out the closing prices of the stock over
the past year, and a shorter term 12 day Exponential Moving Average (EMA) is used in conjunction as 
a tracker for the more recent price-action of the stock.
Additionally, the volatility of the security is used to identify lower and upper bounds around the SMA.
When the EMA moves above the upper bound or below the lower bound of the SMA, the program interprets this as a strong 
bullish or bearish sign. If the EMA falls between the SMA and one of its bounds, the program interprets this as a weak 
sign, and conjectures that the movement of the EMA is a function of the volatility of the stock, and thus the
price-action may be in consolidation instead of a trend. The program then plots and displays a graph displaying the SMA,
EMA, and the lower and upper bounds.

## Limitations
The library used for fetching information about stocks and their prices is yFinance. Entering an invalid Ticker will produce 
a client error, since yFinance is unable to match the string with any ticker in its databases, and prompt a program
termination. In this instance, double-check your input and rerun the program. 

## Notice about Commercial Use:
Per terms of service of yFinance, any program implementing the library is SOLELY for personal or
educational use, and cannot be used in a commercial context. 


