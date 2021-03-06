'''
Created on 2017 2 11 

@author: Junyang HE
'''
from genIndicator import plotIndicator
from flask import Flask, render_template, request
from _datetime import datetime
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    # choose country and stock
    return render_template('index.html')


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
              
            # get 30 days intraday data, periode 60s
            if name == 'airbus':
                intradayList = gfi.get_google_finance_intraday('AIR', 60, 30)
            elif name == 'sopra':
                intradayList = gfi.get_google_finance_intraday('SOP', 60, 30)
            elif name == 'biomerieux':
                intradayList = gfi.get_google_finance_intraday('BIM', 60, 30)
            elif name == 'oreal':
                intradayList = gfi.get_google_finance_intraday('OR', 60, 30)
            elif name == 'total':
                intradayList = gfi.get_google_finance_intraday('FP', 60, 30)
            
            dateList = []
            for item in intradayList :
                dateList.append(item.index[0].strftime('%d/%m/%Y'))  # copy all dates in a list
                print(item.index[0].strftime('%d/%m/%Y'))             
                            
            seletedDateTimeStr = showPeriod  # the date and time selected by user
            seletedDateTime = datetime.strptime(seletedDateTimeStr, '%d/%m/%Y - %Hh%M')  # parse to datetime object
            seletedDateStr = seletedDateTimeStr[0:10]
            # seletedTimeStr = seletedDateTimeStr[13:18]
            
            # print(seletedDateStr)
            # print(dateList.index(seletedDateStr))
            try:
                df = intradayList[dateList.index(seletedDateStr)]  # target dataframe, because intradayList and dateList have the same index
                # gi.genAll(df)   # generate indicators
                # print(df['Close'])
                
                # set start and end point
                startShowPoint = df.index[0]  # type : timestamp
                # endShowPoint = seletedDateTime.timestamp()
                import pandas as pd
                endShowPoint = pd.Timestamp(seletedDateTime)
                # print(df.loc[startShowPoint:endShowPoint])
            except ValueError:
                df = "Intraday history no more available.</br>"
                startShowPoint = 0  # type : timestamp
                endShowPoint = 0
                
    
        # read scores from file
        import readFromFile as rff          
        # print(name)
        ssList = rff.analyseScoreFile(rff.readScoreFile(name))  # list of scoreStructure by date, containing tables, date, time and final score
                                                    
        intradayTime = []  # list of datetime when give score
        intradayTimeHtml = []  # list of html code for short term option
        
        
        ssToShow = None
        intradayTimeHtml.append('<option value="longTerm">longTerm</option>')
        for ss in ssList :              
            if showPeriod != 'longTerm' :  # target seleted date's scoreStructure
                if ss.date == seletedDateTimeStr[:10].replace("/", " "):
                    ssToShow = ss
            if not ss.date == 'model' :  # generate option list for short term
                tempDateTime = datetime(int(ss.date[6:10]), int(ss.date[3:5]), int(ss.date[:2]),
                                        hour=int(ss.time[:2]), minute=int(ss.time[3:5]))
                intradayTime.append(tempDateTime)
                intradayTimeHtml.append('<option value="%(val)s">%(text)s</option>' % 
                                        {'val': tempDateTime.strftime('%d/%m/%Y - %Hh%M'), 'text': tempDateTime.strftime('%d/%m/%Y - %Hh%M')})
        
        if showPeriod == 'longTerm' :
            ssToShow = ssList[0]  # for showing finance score in long term page
        
        if not isinstance(df, str) :
            import matplotlib.pyplot as plt, mpld3  # 2D plotting library
            # plotIndicator(df, 'RS')
            # rs = mpld3.fig_to_html(plt.gcf())
            # plt.close()
            plotIndicator(df, 'Bollinger', startShowPoint=startShowPoint, endShowPoint=endShowPoint, title=showPeriod)
            bollinger = mpld3.fig_to_html(plt.gcf())
            plt.close()
            plotIndicator(df, 'MA', startShowPoint=startShowPoint, endShowPoint=endShowPoint, title=showPeriod)
            ma = mpld3.fig_to_html(plt.gcf())
            plt.close()
            plotIndicator(df, 'MACD', startShowPoint=startShowPoint, endShowPoint=endShowPoint, title=showPeriod)
            macd = mpld3.fig_to_html(plt.gcf())
            plt.close()
            plotIndicator(df, 'RSI', startShowPoint=startShowPoint, endShowPoint=endShowPoint, title=showPeriod)
            rsi = mpld3.fig_to_html(plt.gcf())
            plt.close()
            plotIndicator(df, 'Stochastic', startShowPoint=startShowPoint, endShowPoint=endShowPoint, title=showPeriod)
            stoschastic = mpld3.fig_to_html(plt.gcf())
            plt.close()
            fig = [bollinger, ma, macd, rsi, stoschastic]

            if showPeriod == 'longTerm' :  # long term use a different template
                return render_template('stockLongTerm.html', name=name, fig=fig, shortTermDateTimeOption=intradayTimeHtml,
                                        financeScore=ssToShow.finance['Score'].as_matrix())
            else :
                return render_template('stock.html', name=name, fig=fig, score=ssToShow.graphic['Score'].as_matrix(),
                                   raison=ssToShow.graphic['Reason'].as_matrix(), shortTermDateTimeOption=intradayTimeHtml,
                                   seletedDateTimeStr=seletedDateTimeStr, criterionScore=ssToShow.criterion['Result'].as_matrix(),
                                   finalScore=ssToShow.finalScore)
        elif df == "Intraday history no more available.</br>":
            return render_template('stock.html', name=name, fig=[df, df, df, df, df], score=ssToShow.graphic['Score'].as_matrix(),
                                   raison=ssToShow.graphic['Reason'].as_matrix(), shortTermDateTimeOption=intradayTimeHtml,
                                   seletedDateTimeStr=seletedDateTimeStr, criterionScore=ssToShow.criterion['Result'].as_matrix(),
                                   finalScore=ssToShow.finalScore)
        else :
            return render_template('readError.html', name=name)
    

if __name__ == '__main__':
    app.run(debug=True)
