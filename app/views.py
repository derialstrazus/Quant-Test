from flask import render_template, redirect, url_for, request, session
from app import app
from .forms import SecurityForm
from .f_pull import pullData, printStock, parseNetWorth
from .f_analyze import prepFile, runMACD, tradeLocations, runBollinger
from .f_trade import Trading, buildPortfolioDF, AnnualizeReturn, Benchmark, gainNLoss
import os
import datetime
import locale

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SecurityForm()
    if form.validate_on_submit():
        security = form.security.data
        return redirect(url_for('results', security=security))
    return render_template('index.html',
                           form=form)

@app.route('/more')
def more():
    today = datetime.date.today()
    return render_template('more.html',
                           today=today)

# @app.route('/moreresults', methods=['POST'])
# def moreResults():
#     session['security'] = request.form['security']
#     print session['security']
#     print '%s.txt' % session['security']
#     session['strategy'] = request.form['strategy']
#     session['datestart'] = request.form['datestart']
#     session['dateend'] = request.form['dateend']
#     # import pdb
#     # pdb.set_trace()
#     return render_template('moreresults.html',
#                            security=session['security'],
#                            strategy=session['strategy'],
#                            datestart=session['datestart'],
#                            dateend=session['dateend'])

@app.route('/moreresults', methods=['GET','POST'])
def moreResults():
    session['security'] = request.form['security']
    session['strategy'] = request.form['strategy']
    session['datestart'] = request.form['datestart']
    session['dateend'] = request.form['dateend']

    security = session['security']
    strategy = session['strategy']
    start = session['datestart']
    end = session['dateend']
    sourceCode = pullData(security, start, end)

    shortData = sourceCode.splitlines()[:6]
    previewData = []
    for eachLine in shortData:
        previewData.append(eachLine.split(','))

    fileDir = os.path.dirname(__file__) + '\\TempData'
    fileName = "Output" + security + ".txt"
    filePath = os.path.join(fileDir, fileName)
    listjsons = ('Benchmark'+security+strategy+'.json', 'NetWorth'+security+strategy+'.json')
    listnames = ('Benchmark', 'Strategic Net Worth')

    quotes = prepFile(filePath)
    portfolio = buildPortfolioDF(quotes)
    if strategy == 'MACD':
        quotes = runMACD(quotes)
    elif strategy == 'Bollinger':
        quotes = runBollinger(quotes)
    else:
        quotes = runMACD(quotes)
    print quotes.tail(10)
    #tradeat = tradeLocations(quotes)
    #print tradeat
    trigger = strategy + 'Trigger'
    portfolio = Trading(quotes, trigger, 0, len(portfolio), portfolio)
    portfolio = Benchmark(quotes, 0, len(portfolio), portfolio)
    startyear = int(start[0:4])
    endyear = int(end[0:4])
    gainLoss = gainNLoss(startyear, endyear, portfolio)

    fileDir = os.path.dirname(__file__) + '\\TempData'
    fileName = "portfolio" + security + strategy +".txt"
    filePath = os.path.join(fileDir, fileName)
    portfolio.to_csv(filePath)
    parseNetWorth(fileName, security+strategy)

    netWorthAnnualReturn, benchmarkAnnualReturn, totalNetWorthReturn, totalBenchmarkReturn = AnnualizeReturn(startyear, endyear, portfolio)
    resultYears = range(startyear,endyear)      #the cheating method
    numYears = len(resultYears)
    locale.setlocale(locale.LC_ALL, '')
    netWorth = locale.currency(portfolio.NetWorth[len(portfolio)-1], grouping=True)
    gainLoss = locale.currency(gainLoss, grouping=True)
    print portfolio.head(10)
    return render_template('results.html',
                           jsonname='Output' + security + '.json',
                           security=security,
                           data=previewData,
                           #tradeat=tradeat,
                           netWorth=netWorth,
                           gainLoss = gainLoss,
                           netWorthAnnualReturn=netWorthAnnualReturn,
                           benchmarkAnnualReturn=benchmarkAnnualReturn,
                           totalNetWorthReturn=totalNetWorthReturn,
                           totalBenchmarkReturn=totalBenchmarkReturn,
                           Benchmark= portfolio.Benchmark[len(portfolio)-1],
                           resultYears=resultYears,
                           numYears=numYears,
                           namelist=listnames,
                           jsonlist=listjsons)


@app.route('/aftermoreresults', methods=['GET', 'POST'])
def afterMoreResults():
    security = session['security']
    print security
    return render_template('aftermoreresults.html',
                           security=security)

@app.route('/results/<security>', methods=['GET', 'POST'])
def results(security):
    start = '2000-01-01'
    end = '2015-02-28'
    sourceCode = pullData(security, start, end)
    print sourceCode[:20]
    shortData = sourceCode.splitlines()[:6]
    previewData = []
    for eachLine in shortData:
        previewData.append(eachLine.split(','))
    # print previewData
    # previewData = sourceCode.splitlines()[:6]
    fileDir = os.path.dirname(__file__) + '\\TempData'
    fileName = "Output" + security + ".txt"
    filePath = os.path.join(fileDir, fileName)

    listjsons = ('Benchmark'+security+'.json', 'NetWorth'+security+'.json')
    listnames = ('Benchmark', 'Strategic Net Worth')

    # readLine = "Output" + security +".txt"
    quotes = prepFile(filePath)
    portfolio = buildPortfolioDF(quotes)
    quotes = runBollinger(quotes)
    print quotes.tail(10)
    #tradeat = tradeLocations(quotes)
    #print tradeat
    portfolio = Trading(quotes, 'BollingerTrigger', 0, len(portfolio), portfolio)
    portfolio = Benchmark(quotes, 0, len(portfolio), portfolio)
    startyear = int(start[0:4])
    endyear = int(end[0:4])
    gainLoss = gainNLoss(startyear, endyear, portfolio)
    fileDir = os.path.dirname(__file__) + '\\TempData'
    fileName = "portfolio" + security + ".txt"
    filePath = os.path.join(fileDir, fileName)
    portfolio.to_csv(filePath)

    parseNetWorth(fileName, security)

    netWorthAnnualReturn, benchmarkAnnualReturn, totalNetWorthReturn, totalBenchmarkReturn = AnnualizeReturn(startyear, endyear, portfolio)

    resultYears = range(startyear,endyear)      #the cheating method
    numYears = len(resultYears)
    locale.setlocale(locale.LC_ALL, '')
    netWorth = locale.currency(portfolio.NetWorth[len(portfolio)-1], grouping=True)
    gainLoss = locale.currency(gainLoss, grouping=True)
    print portfolio.head(10)
    return render_template('results.html',
                           jsonname='Output' + security + '.json',
                           security=security,
                           data=previewData,
                           #tradeat=tradeat,
                           netWorth=netWorth,
                           gainLoss = gainLoss,
                           netWorthAnnualReturn=netWorthAnnualReturn,
                           benchmarkAnnualReturn=benchmarkAnnualReturn,
                           totalNetWorthReturn=totalNetWorthReturn,
                           totalBenchmarkReturn=totalBenchmarkReturn,
                           Benchmark= portfolio.Benchmark[len(portfolio)-1],
                           resultYears=resultYears,
                           numYears=numYears,
                           namelist=listnames,
                           jsonlist=listjsons)


@app.route('/compare', methods=['GET', 'POST'])
def compare():

    #listjsons = ('OutputMSFT.json', 'OutputF.json', 'OutputGM.json')
    #listnames = ('MSFT', 'F', 'GM')

    listjsons = ('Benchmark.json', 'NetWorth.json')
    listnames = ('Benchmark', 'Strategic Net Worth')

    parseNetWorth("PortfolioTCKOutput.txt","test")

    return render_template('compare.html',
                           names=listnames,
                           jsonname=listjsons)
