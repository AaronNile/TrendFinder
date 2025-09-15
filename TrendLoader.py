import yfinance as fin
import matplotlib.pyplot as plot
import pandas as pd



def simpleMA(closing_list):
    """This will be the long-term MA"""
    span = 50
    i = 0

    simpleMA = []
    while i < len(closing_list):

        if i < span-1:
            simpleMA.append(None)
            i += 1
            continue

        """Creating a sliced list of N elements, where N is the span, then finding the mean value"""
        slicedList = closing_list[i - span + 1:i+1]
        average = sum(slicedList)/span
        simpleMA.append(average)
        i += 1

    return simpleMA


def ExponentialMA(closing_list):

    span = 12
    """The smoothing factor is given by 2/S+1, where is the span of the EMA"""
    smoothing = 2/(span + 1)

    ExponentialMA = [closing_list[0]]
    i = 1

    while i < len(closing_list):
        """Formula for an EMA value is givne by (P * A) + (EV * (1-A))
        Where P is the current closing price, A is the smoothing factor, and EV is the
         Latest value in the EMA list
         """
        EMA_val = (closing_list[i] * smoothing) + (ExponentialMA[i-1] * (1-smoothing))
        ExponentialMA.append(EMA_val)

        i += 1
    return ExponentialMA

def Volatility(closing_list):

    returns_list = []

    i = 1

    while i < len(closing_list):

        """finding returns for each day's closing price"""
        val = (closing_list[i] - closing_list[i-1]) / closing_list[i-1]
        returns_list.append(val)
        i += 1



    returns_avg = sum(returns_list)/len(returns_list)

    variance = sum((j - returns_avg) ** 2 for j in returns_list) / (len(returns_list)-1)
    """computing variance of returns, given by (Sum of (j - returns_avg)^2)/n
    where j is each value in returns list, and n is the length of returns list
    """

    standard_dev = (variance**(1/2))
    volatility = standard_dev * (252**(1/2))
    """Annualizing volatility by multipliying it with the square root of the number of business days"""



    return volatility


def find_trend(SMA, EMA, Vol, ticker):
    Upperbound = SMA[-1] + Vol
    Lowerbound = SMA[-1] - Vol

    if EMA[-1] < SMA[-1]:
        if EMA[-1] < Lowerbound:
            print("Exponential moving average below the Simple Moving Average and the lowerbound is"
                  " a strong sign of a downtrend. ")
        else:
            print("Exponential Moving Average below the Simple Moving Average but above the lowerbound is a weak sign"
                  "for a downtrend. " + ticker + " May be in a consolidation phase.")

    if EMA[-1] > SMA[-1]:
        if EMA[-1] > Upperbound:
            print("Exponential Moving Average above the Simple Moving Average and the Upperbound is"
                  " a strong sign of an uptrend. ")
        else:
            print(
                "Exponential Moving Average above the Simple Moving Average but below the Upperbound is a weak sign"
                "for an uptrend. " + ticker + " may be in a consolidation phase.")

def create_lower_bound(SMA, Vol):
    lower_bound = []
    for i in SMA:
        if i != None:
            lower_bound.append(i - Vol)
        else:
            lower_bound.append(None)


    return lower_bound

def create_upper_bound(SMA, Vol):
    upper_bound = []
    for i in SMA:
        if i != None:
            upper_bound.append(i + Vol)
        else:
            upper_bound.append(None)


    return upper_bound




def draw_graph(SMA, EMA, lower_bound, dates, upper_bound, ticker):


    plot.figure(figsize=(12, 6))
    plot.plot(dates, SMA, label='SMA', linestyle ='-', linewidth = 2)
    plot.plot(dates, EMA, label='EMA', linestyle ='-', linewidth = 2)
    plot.plot(dates, lower_bound, label='Lower Bound', linestyle ='-', linewidth = 0.5, color="Green")
    plot.plot(dates, upper_bound, label='Upper Bound', linestyle='-', linewidth= 0.5, color="Green")

    plot.xlabel("Months")
    plot.ylabel("Prices")
    plot.title(ticker +" Trend")
    plot.grid()
    plot.legend()
    plot.show()

def main():
    #Prompt the user for a ticker symbol and normalize it
    ticker = input(
        "Enter the Ticker for a stock (Ex. AAPL, TESLA, AMZN) for an analysis of its medium-term trend:"
    ).strip().upper()

    #Build the date range: from one year ago up to today
    date_today    = pd.to_datetime("today").normalize()
    date_year_ago = date_today - pd.DateOffset(years=1)
    start = date_year_ago.strftime("%Y-%m-%d")
    end   = date_today.strftime("%Y-%m-%d")

    #Download historical price data (adjusted for splits/dividends by default)
    df = fin.download(ticker, start=start, end=end, progress=False)
    if df.empty:
        # If no rows came back, inform the user and exit
        print(f"No data returned for {ticker}. Please check the symbol or your connection.")
        return

    #Extract closing prices and their corresponding dates

    closing_list = df.iloc[:, 0].tolist()
    dates = df.index

    #Compute the moving averages and volatility
    EMA = ExponentialMA(closing_list)
    SMA = simpleMA(closing_list)


    Vol = Volatility(closing_list) * 2 
       # annualized volatility × 2 for 2σ bands

    price_vol = [ (s * Vol) if s is not None else None for s in SMA ]

    #Build the upper and lower volatility bands around the SMA
    lower_bound = create_lower_bound(SMA, price_vol)
    upper_bound = create_upper_bound(SMA, price_vol)

    #Analyze the current trend and render the chart
    find_trend(SMA, EMA, Vol, ticker)
    draw_graph(SMA, EMA, lower_bound, dates, upper_bound, ticker)







if __name__ == "__main__":
    main()