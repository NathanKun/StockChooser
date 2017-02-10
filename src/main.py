'''
Created on 2017年2月9日

@author: Junyang HE
'''

'''
 pip install pandas
 pip install pandas-datareader
 pip install matplotlib
 pip install statsmodels
'''


import pandas as pd                     # data structures and data analysis tools
from pandas_datareader import data      # for importing data
import datetime
import matplotlib.pyplot as plt         # 2D plotting library
import numpy as np                      # fundamental package for scientific computing

















if __name__ == '__main__':
    print("Start!")
    
    #plt.rcParams['figure.figsize'] = (15, 9)   # Change the size of plots
    
    # period of 2 year
    start = datetime.datetime(datetime.datetime.now().year-2,datetime.datetime.now().month,datetime.datetime.now().day-1)
    end = datetime.date.today()
    startShowing = datetime.datetime(datetime.datetime.now().year-1,datetime.datetime.now().month,datetime.datetime.now().day-1)



    # get 5 stocks data
    airbus = data.DataReader("AIR.PA", "yahoo", start, end)
    sopra = data.DataReader("SOP.PA", "yahoo", start, end)
    total = data.DataReader("FP.PA", "yahoo", start, end)
    oreal = data.DataReader("OR.PA", "yahoo", start, end)
    biome = data.DataReader("BIM.PA", "yahoo", start, end)
    
    #print(airbus.head(5))
    #oreal["Adj Close"].plot(grid = True)
    
    import statsmodels.formula.api as sm
    fit = sm.ols(formula="AdjClose ~ Day", data=airbus).fit()
    print(fit.summary())
    predict = fit.predict(airbus)
    airbus['fitted'] = predict
    airbus['fitted'].plot()
    
    # calculate moving average
    ma_day = [10,20,50]
    for ma in ma_day:
        column_name = "MA for %s days" %(str(ma))
        airbus[column_name] = airbus['Adj Close'].rolling(center=False,window=ma).mean()
        sopra[column_name] = sopra['Adj Close'].rolling(center=False,window=ma).mean()
        total[column_name] = total['Adj Close'].rolling(center=False,window=ma).mean()
        oreal[column_name] = oreal['Adj Close'].rolling(center=False,window=ma).mean()
        biome[column_name] = biome['Adj Close'].rolling(center=False,window=ma).mean()
    
    #airbus.loc[startShowing : end, ['Adj Close','MA for 10 days','MA for 20 days','MA for 50 days']].plot(subplots=False,figsize=(14,6))
    
    
    # calculate bollinger bands. MA20 +- 2*std
    def bbands(price, length=20, numsd=2):
        """ returns average, upper band, and lower band"""
        ave = price.rolling(center=False,window=length).mean()
        std = price.rolling(center=False,window=length).std()
        upband = ave + (std*numsd)
        dnband = ave - (std*numsd)
        return np.round(ave,3), np.round(upband,3), np.round(dnband,3)

    airbus['bollinger ave'], airbus['bollinger upper'], airbus['bollinger lower'] = bbands(airbus['Adj Close'])
    airbus['bollinger ave'], airbus['bollinger upper'], airbus['bollinger lower'] = bbands(airbus['Adj Close'])
    
    #airbus.loc[startShowing : end, ['Adj Close','bollinger upper','bollinger ave','bollinger lower']].plot(subplots=False,figsize=(14,6))
    
    
    z = np.polyfit()
    p = np.poly1d(airbus.iloc[startShowing : end, 'Open'])
    plt.plot(airbus.iloc[startShowing : end, 'Close'],p(airbus.iloc[startShowing : end, 'Close']),"r–")

    
    plt.show()
    
    print("End!")