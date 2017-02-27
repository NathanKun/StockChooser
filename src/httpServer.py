'''
Created on 2017 2 11 

@author: Junyang HE
'''
from genIndicator import plotIndicator
from flask import Flask, url_for, redirect, render_template, request
from _datetime import datetime
#app = Flask(__name__, root_path = '/home/wwwroot/catprogrammer.com/stockchooser')
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    # choose country and stock
    '''
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
    '''
    return render_template('index.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    '''
    if request.method == 'POST':
        bbandsText = request.form['bbandsText']
        maText = request.form['maText']
        macdText = request.form['macdText']
        rsiText = request.form['rsiText']
        rsText = request.form['rsText']
        stochasticText = request.form['stochasticText']
    '''  
    return "ok"

@app.route('/show', methods=['POST', 'GET'])
def show(name=None):
    # get selected stock name
    if request.method == 'POST':
        name = request.form['stockName']
        showPeriod = request.form['showPeriod']
        
        import genIndicator as gi
        
        if showPeriod == 'longTerm' :
            # get long term stock data and generate indicators
            df = gi.getAndGen(name)
            
            import constDaytime as cd
            startShowPoint = cd.startShowing
            endShowPoint = cd.end 
        else :
            # get short term intraday data and generate indicators
            import googleFinanceIntraday as gfi
              
            # get 15 days intraday data, periode 60s
            if name == 'airbus':
                intradayList = gfi.get_google_finance_intraday('AIR', 60, 20)
            elif name == 'sopra':
                intradayList = gfi.get_google_finance_intraday('SOP', 60, 20)
            elif name == 'biomerieux':
                intradayList = gfi.get_google_finance_intraday('BIM', 60, 20)
            elif name == 'oreal':
                intradayList = gfi.get_google_finance_intraday('OR', 60, 20)
            elif name == 'total':
                intradayList = gfi.get_google_finance_intraday('FP', 60, 20)
            
            dateList = []
            for item in intradayList :
                dateList.append(item.index[0].strftime('%d/%m/%Y')) # copy all dates in a list
                #print(item.index[0].strftime('%d/%m/%Y'))             
                            
            seletedDateTimeStr = showPeriod                         # the date and time selected by user
            seletedDateTime = datetime.strptime(seletedDateTimeStr, '%d/%m/%Y - %Hh%M') # parse to datetime object
            seletedDateStr = seletedDateTimeStr[0:10]
            #seletedTimeStr = seletedDateTimeStr[13:18]
            
            #print(seletedDateStr)
            #print(dateList.index(seletedDateStr))
            df = intradayList[dateList.index(seletedDateStr)]   # target dataframe, because intradayList and dateList have the same index
            #gi.genAll(df)   # generate indicators
            #print(df['Close'])
            
            # set start and end point
            startShowPoint = df.index[0]    # type : timestamp
            #endShowPoint = seletedDateTime.timestamp()
            import pandas as pd
            endShowPoint = pd.Timestamp(seletedDateTime)
            #print(df.loc[startShowPoint:endShowPoint])
    
        # read scores from file
        import readFromFile as rff          
        #print(name)
        ssList = rff.analyseScoreFile(rff.readScoreFile(name))    # list of scoreStructure by date, containing tables, date, time and final score
                                                    
        intradayTime = []                           # list of datetime when give score
        intradayTimeHtml = []                       # list of html code for short term option
        
        
        ssToShow = None
        intradayTimeHtml.append('<option value="longTerm">longTerm</option>')
        for ss in ssList :              
            if showPeriod != 'longTerm' :   # target seleted date's scoreStructure
                if ss.date == seletedDateTimeStr[:10].replace("/", " "):
                    ssToShow = ss
            if not ss.date == 'model' :     # generate option list for short term
                tempDateTime = datetime(int(ss.date[6:10]), int(ss.date[3:5]), int(ss.date[:2]), 
                                        hour=int(ss.time[:2]), minute=int(ss.time[3:5]))
                intradayTime.append(tempDateTime)
                intradayTimeHtml.append('<option value="%(val)s">%(text)s</option>' % 
                                        {'val': tempDateTime.strftime('%d/%m/%Y - %Hh%M'), 'text': tempDateTime.strftime('%d/%m/%Y - %Hh%M')})

        
        if not isinstance(df, str) :
            import matplotlib.pyplot as plt, mpld3  # 2D plotting library
            #plotIndicator(df, 'RS')
            #rs = mpld3.fig_to_html(plt.gcf())
            #plt.close()
            plotIndicator(df, 'Bollinger', startShowPoint = startShowPoint, endShowPoint = endShowPoint)
            bollinger= mpld3.fig_to_html(plt.gcf())
            plt.close()
            plotIndicator(df, 'MA', startShowPoint = startShowPoint, endShowPoint = endShowPoint)
            ma = mpld3.fig_to_html(plt.gcf())
            plt.close()
            plotIndicator(df, 'MACD', startShowPoint = startShowPoint, endShowPoint = endShowPoint)
            macd = mpld3.fig_to_html(plt.gcf())
            plt.close()
            plotIndicator(df, 'RSI', startShowPoint = startShowPoint, endShowPoint = endShowPoint)
            rsi = mpld3.fig_to_html(plt.gcf())
            plt.close()
            plotIndicator(df, 'Stochastic', startShowPoint = startShowPoint, endShowPoint = endShowPoint)
            stoschastic = mpld3.fig_to_html(plt.gcf())
            plt.close()
            fig = [bollinger, ma, macd, rsi, stoschastic]

            if showPeriod == 'longTerm' :   # long term use a different template
                return render_template('stockLongTerm.html', name = name, fig = fig, shortTermDateTimeOption = intradayTimeHtml)
            else :
                return render_template('stock.html', name = name, fig = fig, score = ssToShow.graphic['Score'].as_matrix(), 
                                   raison = ssToShow.graphic['Reason'].as_matrix(), shortTermDateTimeOption = intradayTimeHtml, 
                                   seletedDateTimeStr = seletedDateTimeStr)
            
        else :
            return render_template('readError.html', name = name)
    

if __name__ == '__main__':
    app.run(debug=True)
