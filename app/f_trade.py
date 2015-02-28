def buildPortfolioDF(quotes):
    portfolio = quotes
    portfolio = portfolio.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'AdjClose'], 1)
    portfolio['Cash'] = float(0.0)
    portfolio['Shares'] = float(0.0)
    portfolio['SharePrice'] = float(0.0)
    portfolio['NetWorth'] = float(0.0)
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
            sharesBought = int(cash/quotes.AdjClose[n])  #Number of share to buy
            sharesCost = sharesBought * quotes.AdjClose[n]  #Amount spend
            cash = cash - sharesCost

            shares = shares + sharesBought                  #total shares held
            sharesValue = shares * quotes.AdjClose[n]
            netWorth = cash + sharesValue
            print '%s: Bought %d shares, giving net worth of  %.2f' % (quotes.Date[n], sharesBought, netWorth )
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
            print '%s: Sold %d shares, giving net worth of  %.2f' % (quotes.Date[n], sharesValueSold, netWorth )

        portfolio.Cash[n] = cash
        portfolio.Shares[n] = shares
        portfolio.SharePrice[n] = quotes.AdjClose[n]
        portfolio.NetWorth[n] = netWorth

    performance = 100.0 * netWorth/capital
    portfolio = portfolio[start:end]
    return portfolio




