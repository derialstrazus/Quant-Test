import math
import os
import pdb

def buildPortfolioDF(quotes):
    portfolio = quotes
    portfolio = portfolio.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'AdjClose'], 1)
    portfolio['Cash'] = float(0.0)
    portfolio['Shares'] = float(0.0)
    portfolio['SharePrice'] = float(0.0)
    portfolio['NetWorth'] = float(0.0)
    portfolio['Benchmark'] = float(0.0)
    return portfolio

def Trading(quotes, trigger, start, end, portfolio):
    shares = 0
    sharesValue = 0
    capital = 10000
    cash = capital
    netWorth = capital + sharesValue
    for n in range(start, end):
        indicator = quotes[trigger][n]
        if indicator == 1:                                  #Strong buy; Commit all money
            sharesBought = int(cash/quotes.AdjClose[n])     #Number of share to buy
            sharesCost = sharesBought * quotes.AdjClose[n]  #Amount spend
            cash = cash - sharesCost

            shares = shares + sharesBought                  #total shares held
            sharesValue = shares * quotes.AdjClose[n]
            netWorth = cash + sharesValue
            # print '%s: Bought %d shares, giving net worth of  %.2f' % (quotes.Date[n], sharesBought, netWorth )
        elif indicator == 0:
            pass
        else:
            sharesQuantity = int(shares)        #Number of shares to sell
            shares = shares - sharesQuantity    #Currently holding shares
            if shares != 0:
                print 'something wrong!'
            sharesValueSold = sharesQuantity * quotes.AdjClose[n]   #How much you sold everything for
            cash = cash + sharesValueSold
            sharesValue = shares * quotes.AdjClose[n]               #current value of shares

            netWorth = cash + sharesValue
            # print '%s: Sold %d shares, giving net worth of  %.2f' % (quotes.Date[n], sharesQuantity, netWorth )

        portfolio.Cash[n] = cash
        portfolio.Shares[n] = shares
        portfolio.SharePrice[n] = quotes.AdjClose[n]
        portfolio.NetWorth[n] = netWorth

    performance = 100.0 * netWorth/capital
    portfolio = portfolio[start:end]
    return portfolio

def Benchmark(quotes, start, end, portfolio):
    shares = 0
    sharesValue = 0
    sharesBought = 0
    capital = 10000
    cash = capital
    netWorth = capital + sharesValue
    for n in range (0,len(quotes)):
        if n == 0:
            sharesBought = int(cash/quotes.AdjClose[n])     #Number of share to buy
            sharesCost = sharesBought * quotes.AdjClose[n]  #Amount spend
            cash = cash - sharesCost

            shares = shares + sharesBought                  #total shares held
            sharesValue = shares * quotes.AdjClose[n]
            netWorth = cash + sharesValue
            # print '%s: Bought %d shares, giving net worth of  %.2f' % (quotes.Date[n], sharesBought, netWorth )
        elif n == len(quotes):
            sharesQuantity = int(shares)        #Number of shares to sell
            shares = shares - sharesQuantity    #Currently holding shares
            if shares != 0:
                print 'something wrong!'
            sharesValueSold = sharesQuantity * quotes.AdjClose[n]   #How much you sold everything for
            cash = cash + sharesValueSold
            sharesValue = shares * quotes.AdjClose[n]               #current value of shares

            netWorth = cash + sharesValue
            # print '%s: Sold %d shares, giving net worth of  %.2f' % (quotes.Date[n], sharesValueSold, netWorth )
            return portfolio
        else:
            pass
        marketValues = sharesBought * quotes.AdjClose[n]
        netWorth = cash + marketValues
        portfolio.Benchmark[n] = netWorth
    portfolio = portfolio[start:end]
    return portfolio


def gainNLoss(start, end, portfolio):
    initialNetWorth = 10000
    finalNetWorth = 0
    for n in range (0, len(portfolio.NetWorth)):
        if n == len(portfolio)-1:
            finalNetWorth = portfolio.NetWorth[n]
        else:
            pass

    gainLoss = finalNetWorth - initialNetWorth
    return gainLoss


def AnnualizeReturn(start, end, portfolio):
    netWorthAnnualReturn=[]
    benchmarkAnnualReturn=[]
    netWorthProduct = 1
    benchmarkProduct = 1
    yearlyNetWorthReturn = 0
    yearlyBenchmarkReturn = 0
    startNetWorth = portfolio.NetWorth[0]
    endNetWorth = startNetWorth
    startBenchmark = portfolio.Benchmark[0]
    endBenchmark = startBenchmark
    for i in range(start,end):          #years
        # print "Year %d:" % i
        startStop = 0
        endStop = 0
        for n in range(0, len(portfolio)):          #whole index
            if (portfolio.Date[n][:4] == str(i)) & (startStop == 0):
                startNetWorth = portfolio.NetWorth[n]
                startBenchmark = portfolio.Benchmark[n]
                startStop = 1
                # print 'Start at index %d at date %s with benchmark: %d' % (n, portfolio.Date[n], portfolio.Benchmark[n])
            elif (portfolio.Date[n][:4] == str(i+1)) & (endStop == 0):
                endNetWorth = portfolio.NetWorth[n]
                endBenchmark = portfolio.Benchmark[n]
                endStop =1
                # print 'End at index %d at date %s with benchmark: %d' % (n, portfolio.Date[n], portfolio.Benchmark[n])
        yearlyNetWorthReturn = (endNetWorth-startNetWorth)/startNetWorth *100  #Calculate yearly return for net worth
        yearlyBenchmarkReturn = (endBenchmark-startBenchmark)/startBenchmark *100 #Calculate yearly return for benchmark
        netWorthAnnualReturn.append(yearlyNetWorthReturn)                       #Add each annual net worth return to a list
        benchmarkAnnualReturn.append(yearlyBenchmarkReturn)                     #Add each annual benchmark return to a list
        netWorthProduct = netWorthProduct * (yearlyNetWorthReturn + 100)        #Getting the product of each year annual net worth return
        benchmarkProduct = benchmarkProduct * (yearlyBenchmarkReturn + 100)     #Getting the product of each year annual benchmark return

        # pdb.set_trace()
    totalNetWorthReturn = math.pow(netWorthProduct, 1.0/(len(netWorthAnnualReturn))) - 100
    totalBenchmarkReturn = math.pow(benchmarkProduct, 1.0/(len(benchmarkAnnualReturn))) - 100
    # import pdb
    # pdb.set_trace()
    return netWorthAnnualReturn, benchmarkAnnualReturn, totalNetWorthReturn, totalBenchmarkReturn




