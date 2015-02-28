import pandas as pd

MA_SHORT = 12
MA_LONG = 26

def prepFile(sourceFile):
    quotes = pd.read_csv(sourceFile)
    quotes.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'AdjClose']
    return quotes

def runMACD(quotes):

    quotes['MAShort'] = float('NaN')
    Sum = 0
    for n in range(0,MA_SHORT):
        Sum = Sum + quotes.AdjClose[n]
    MvgAvg = Sum / MA_SHORT
    quotes['MAShort'][n] = float('%.4f' % (MvgAvg))
    for n in range(MA_SHORT,len(quotes)):
        Sum = Sum - quotes.AdjClose[n-MA_SHORT] + quotes.AdjClose[n]
        MvgAvg = Sum / MA_SHORT
        quotes['MAShort'][n] = float('%.4f' % (MvgAvg))

    quotes['MALong'] = float('NaN')
    Sum = 0
    for n in range(0,MA_LONG):
        Sum = Sum + quotes.AdjClose[n]
    MvgAvg = Sum / MA_LONG
    quotes['MALong'][n] = float('%.4f' % (MvgAvg))
    for n in range(MA_LONG,len(quotes)):
        Sum = Sum - quotes.AdjClose[n-MA_LONG] + quotes.AdjClose[n]
        MvgAvg = Sum / MA_LONG
        quotes['MALong'][n] = float('%.4f' % (MvgAvg))

    quotes['MACD'] = float('NaN')
    for n in range(26,len(quotes)):
        MACD = quotes['MAShort'][n] - quotes['MALong'][n]
        quotes['MACD'][n] = float('%.4f' % (MACD))

    quotes['MACDTrigger'] = float('NaN')
    for n in range(26,len(quotes)):
        if quotes.MACD[n] > 0:
            quotes.MACDTrigger[n] = 1
        else:
            quotes.MACDTrigger[n] = -1

    return quotes

def tradeLocations(quotes):
    now = 0
    locations = []
    for n in range(26,len(quotes)):
        if now != quotes.MACDTrigger[n]:
            now = quotes.MACDTrigger[n]
            locations.append(quotes.Date[n])

    return locations

def trade():

    results = 0
    return results