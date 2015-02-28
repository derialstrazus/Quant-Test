from flask import render_template, redirect, url_for, request, session
from app import app
from .forms import SecurityForm
from .f_pull import pullData, printStock
from .f_analyze import runMACD, tradeLocations
from .f_trade import MACDTrading
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

@app.route('/moreresults', methods=['POST'])
def moreResults():
    session['security'] = request.form['security']
    session['strategy'] = request.form['strategy']
    return render_template('moreresults.html', security=session['security'], strategy=session['strategy'])


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
    quotes = runMACD(filePath)
    print quotes.tail(10)
    tradeat = tradeLocations(quotes)
    print tradeat
    netWorth = MACDTrading(quotes, 'MACDTrigger', 200, 2000)
    return render_template('results.html',
                           security=security,
                           data=previewData,
                           tradeat=tradeat,
                           netWorth=netWorth)
