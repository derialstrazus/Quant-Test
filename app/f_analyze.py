import pandas as pd
from numpy import std

MA_SHORT = 12
MA_LONG = 26
MACD_AVG = 9

# pd.options.mode.chained_assignment = None

def prepFile(sourceFile):
    quotes = pd.read_csv(sourceFile)
    quotes.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'AdjClose']
    return quotes

def runBuyHold(quotes):
    quotes['BuyHoldTrigger'] = 1
    return quotes

def runMACDDiff(quotes):
    quotes['MAShort'] = float('NaN')
    Sum = 0
    for n in range(0,MA_SHORT):
        Sum = Sum + quotes.AdjClose[n]
    MvgAvg = Sum / MA_SHORT
    quotes['MAShort'][n] = float('%.4f' % MvgAvg)
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

    quotes['MACD9DayAvg'] = float('NaN')
    Sum = 0
    for n in range(MA_LONG, MACD_AVG + MA_LONG):
        Sum = Sum + quotes.MACD[n]
    MACDAvg = Sum / MACD_AVG
    quotes['MACD9DayAvg'][n] = float('%.4f' % (MACDAvg))
    for n in range(MACD_AVG + MA_LONG, len(quotes)):
        Sum = Sum - quotes.MACD[n-MACD_AVG] + quotes.MACD[n]
        MACDAvg = Sum / MACD_AVG
        quotes['MACD9DayAvg'][n] = float('%.4f' % (MACDAvg))

    quotes['Diff'] = float('NaN')
    for n in range(0, len(quotes)):
        quotes['Diff'][n] = quotes['MACD'][n] - quotes['MACD9DayAvg'][n]

    quotes['MACDDiffTrigger'] = float('NaN')
    for n in range(MA_LONG + MACD_AVG,len(quotes)):
        diff = quotes.MACD[n] - quotes['MACD9DayAvg'][n]
        diffprev = quotes.MACD[n-1] - quotes['MACD9DayAvg'][n-1]
        slope = diff - diffprev
        if ((diff - diffprev) <= 0.01) and (diff > 0):
            quotes.MACDDiffTrigger[n] = 1
        elif ((diff - diffprev) >= 0.02) and (diff < 0):
            quotes.MACDDiffTrigger[n] = -1
        else:
            quotes.MACDDiffTrigger[n] = 0

    return quotes

def runMACD(quotes):
    quotes['MAShort'] = float('NaN')
    Sum = 0
    for n in range(0,MA_SHORT):
        Sum = Sum + quotes.AdjClose[n]
    MvgAvg = Sum / MA_SHORT
    quotes['MAShort'][n] = float('%.4f' % MvgAvg)
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

def runBollinger(quotes):
    points = 20
    pastArray = []
    quotes['DownBand'] = float('NAN')
    quotes['UpBand'] = float('NaN')
    quotes['BollingerTrigger'] = float('NaN')

    for n in range(0,points):
        pastArray.append(quotes.AdjClose[n])

    for n in range(points, len(quotes)):
        Close = quotes.AdjClose[n]
        MvgAvg = sum(pastArray) / points
        StdDev = std(pastArray)
        UpBand = MvgAvg + (2*StdDev)
        DownBand = MvgAvg - (2 * StdDev)
        quotes['DownBand'][n]= float('%.4f' % DownBand)
        quotes['UpBand'][n] = float('%.4f' % UpBand)

        if ((Close > UpBand)):
            quotes['BollingerTrigger'][n] = 1
        elif ((Close < DownBand)):
            quotes['BollingerTrigger'][n] = -1
        elif ((Close < UpBand) & (Close > DownBand)):
            quotes["BollingerTrigger"][n] = 0
        pastArray.pop(0)
        pastArray.append(quotes.AdjClose[n])
    return quotes


def tradeLocations(quotes):
    now = 0
    locations = []
    for n in range(26,len(quotes)):
        if now != quotes.MACDTrigger[n]:
            now = quotes.MACDTrigger[n]
            locations.append(quotes.Date[n])

    return locations
