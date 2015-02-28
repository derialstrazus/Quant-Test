import urllib2
import time
import datetime
import os

def getStocks():
    SnP100File = 'S&P100.txt'
    SnPData = open(SnP100File,'r').read()
    splitSnPData = SnPData.split('\n')
    
    stocksToPull = []
    for eachLine in splitSnPData:
        splitLine = eachLine.split('\t')
        stocksToPull.append(splitLine[0])
        
    print stocksToPull
    return stocksToPull


def pullData(stock):
    try:
        today = datetime.date.today()
        print '\nCurrently pulling',stock
        urlToVisit = 'http://real-chart.finance.yahoo.com/table.csv?s=%s&d=%d&e=%d&f=%d&g=d&a=11&b=12&c=2000&ignore=.csv' % (stock, today.month - 1, today.day, today.year)
        # end: d is month-1, e is day, f is year
        # start: a is month-1, b is day, c is year

        sourceCode = urllib2.urlopen(urlToVisit).read().splitlines()
        print 'Pulled',stock
        return sourceCode
                
    except Exception,e:
        print 'main loop', str(e)

                
def csvFlipper(readFileName, saveFileName):
    readFilePath = os.path.join(saveDir, readFileName)
    readFile = open(readFilePath,'r')
    saveFilePath = os.path.join(saveDir, saveFileName)
    saveFile = open(saveFilePath, 'w')
    saveFile.write(readFile.readline())  #To keep header
    
    for line in reversed(readFile.readlines()):
        saveFile.write(line)
    
    readFile.close()
    saveFile.close()


def printStock(sourceCode):
    dates = []
    for lines in sourceCode[1:]:
        dates.append(lines.split(',')[0])
    close = []
    for lines in sourceCode[1:]:
        close.append(float(lines.split(',')[-1]))

    # plt.plot(dates,close)
    # plt.ylabel('Adj Close')
    # plt.xlabel('Dates')
