import pandas as pd
from pandas import Series, DataFrame

def userPortfolio():
    portfolio = DataFrame()
    portfolio.columns = ['Date','Capital','Shares','SharePrice','NetWorth']
    return portfolio