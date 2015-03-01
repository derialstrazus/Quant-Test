from flask import render_template, redirect, url_for, request, session
from app import app
from .forms import SecurityForm
from .f_pull import pullData, printStock
from .f_analyze import prepFile, runMACD, tradeLocations, runBollinger
from .f_trade import Trading, buildPortfolioDF, AnnualizeReturn, Benchmark
import os

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
    return render_template('more.html')

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
    sourceCode = pullData(security)
    print sourceCode[:20]
    previewData = sourceCode.splitlines()[:6]
    # plotData = printStock(sourceCode)
    fileDir = os.path.dirname(__file__) + '\\TempData'
    fileName = "Output" + security + ".txt"
    filePath = os.path.join(fileDir, fileName)

    # readLine = "Output" + security +".txt"
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
    AnnualReturn, totalAnnualReturn = AnnualizeReturn(0, len(portfolio), portfolio)
    resultYears = [2011, 2012, 2013]
    print portfolio.head(10)
    return render_template('results.html',
                           security=security,
                           data=previewData,
                           #tradeat=tradeat,
                           netWorth=portfolio.NetWorth[len(portfolio)-1],
                           AnnualReturn=AnnualReturn,
                           totalAnnualReturn=totalAnnualReturn,
                           resultYears=resultYears)


@app.route('/aftermoreresults', methods=['GET', 'POST'])
def afterMoreResults():
    security = session['security']
    print security
    return render_template('aftermoreresults.html',
                           security=security)

@app.route('/results/<security>', methods=['GET', 'POST'])
def results(security):
    sourceCode = pullData(security)
    print sourceCode[:20]
    previewData = sourceCode.splitlines()[:6]
    # plotData = printStock(sourceCode)
    fileDir = os.path.dirname(__file__) + '\\TempData'
    fileName = "Output" + security + ".txt"
    filePath = os.path.join(fileDir, fileName)

    # readLine = "Output" + security +".txt"
    quotes = prepFile(filePath)
    portfolio = buildPortfolioDF(quotes)
    quotes = runBollinger(quotes)
    print quotes.tail(10)
    #tradeat = tradeLocations(quotes)
    #print tradeat
    portfolio = Trading(quotes, 'BollingerTrigger', 0, len(portfolio), portfolio)
    portfolio = Benchmark(quotes, 0, len(portfolio), portfolio)
    netWorthAnnualReturn, benchmarkAnnualReturn, totalNetWorthReturn, totalBenchmarkReturn = AnnualizeReturn(0, len(portfolio), portfolio)
    resultYears = [2011, 2012, 2013]
    print portfolio.head(10)
    return render_template('results.html',
                           jsonname='Output' + security + '.json',
                           security=security,
                           data=previewData,
                           #tradeat=tradeat,
                           netWorth=portfolio.NetWorth[len(portfolio)-1],
                           netWorthAnnualReturn=netWorthAnnualReturn,
                           benchmarkAnnualReturn=benchmarkAnnualReturn,
                           totalNetWorthReturn=totalNetWorthReturn,
                           totalBenchmarkReturn=totalBenchmarkReturn,
                           Benchmark= portfolio.Benchmark[len(portfolio)-1],
                           resultYears=resultYears)
