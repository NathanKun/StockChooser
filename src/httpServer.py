'''
Created on 2017 2 11 

@author: Junyang HE
'''
from genIndicator import plotIndicator
from flask import Flask, url_for, redirect, render_template, request
#app = Flask(__name__, root_path = '/home/wwwroot/catprogrammer.com/stockchooser')
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    import pandas as pd
    tickerSymbolsFile = pd.ExcelFile('../data/Yahoo Ticker Symbols.xlsx')   # (ticker - name) list in a sheet for each country
    sheetsName = tickerSymbolsFile.sheet_names                              # list of sheet name (country name)
    tickerSymbolSheets = []
    selectCountryHtml = []
    for sheetName in sheetsName :
        tickerSymbolSheets.append(tickerSymbolsFile.parse(sheetName).to_json(orient='records')[1:-1])   # parse each sheet in json
        selectCountryHtml.append('<option value="%(val)s">%(text)s</option>' % 
                                    {'val': sheetName, 'text': sheetName})                              # add in a list

    return render_template('index.html', countryList = selectCountryHtml, tickerSymbolSheets = tickerSymbolSheets)  # send to the template

@app.route('/stockchooser')
def sc():
#    return render_template('index.html')
    return 'stockchooser'

@app.route('/submit', methods=['POST', 'GET'])
def submit(name=None):
    if request.method == 'POST':
        if 'stockName' in request.form :
            name = request.form['stockName']
        else :
            name = request.form['stockList']
        
        import genIndicator as gi
        df = gi.getAndGen(name)
        
        
        if not isinstance(df, str) :
            import matplotlib.pyplot as plt, mpld3  # 2D plotting library
            plotIndicator(df, 'RS')
            rs = mpld3.fig_to_html(plt.gcf())
            plt.close()
            plotIndicator(df, 'Bollinger')
            bollinger= mpld3.fig_to_html(plt.gcf())
            plt.close()
            plotIndicator(df, 'MA')
            ma = mpld3.fig_to_html(plt.gcf())
            plt.close()
            plotIndicator(df, 'MACD')
            macd = mpld3.fig_to_html(plt.gcf())
            plt.close()
            plotIndicator(df, 'RSI')
            rsi = mpld3.fig_to_html(plt.gcf())
            plt.close()
            plotIndicator(df, 'Stochastic')
            stoschastic = mpld3.fig_to_html(plt.gcf())
            plt.close()
            fig = [bollinger, ma, macd, rsi, stoschastic, rs]
            
            return render_template('stock.html', name = name, fig = fig)
        
        else :
            return render_template('readError.html', name = name)
    

if __name__ == '__main__':
    app.run(debug=True)
