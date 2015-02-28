
def MACDTrading(quotes, trigger, start, end):
    shares = 0
    sharesValue = 0
    capital = 10000
    netWorth = capital + sharesValue
    for n in range(start, end):
        indicator = quotes[trigger][n]
        if indicator == 1:                                  #Strong buy; Commit all money
            sharesBought = int(capital/quotes.AdjClose[n])  #Number of share to buy
            sharesCost = sharesBought * quotes.AdjClose[n]  #Amount spend
            shares = shares + sharesBought                  #Number of shares brought
            netWorth = netWorth - sharesCost
        elif indicator == 0:
            pass
        else:
            sharesQuantity = int(shares)
            shares = shares - sharesQuantity
            if shares != 0:
                print 'something wrong!'
            sharesSold = sharesQuantity * quotes.AdjClose[n]
            netWorth = netWorth + sharesSold

    performance = 100.0 * netWorth/capital
    return netWorth



