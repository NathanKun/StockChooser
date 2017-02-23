'''
Created on 2017 2 22

@author: Junyang HE
'''

import csv
import datetime
import re

import pandas as pd
from urllib.request import urlopen
from _datetime import date

def get_yahoo_finance_intraday(ticker, days=1):
    """
    Retrieve intraday stock data from Google Finance.
    Parameters
    ----------
    ticker : str
        Company ticker symbol.
    days : int
        Number of days of data to retrieve.
    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing the opening price, high price, low price,
        closing price, and volume. The index contains the times associated with
        the retrieved price values.
    """
    
    
    uri = 'https://chartapi.finance.yahoo.com/instrument/'\
                        '1.0/{ticker}/chartdata;type=quote;range={days}d/csv'.format(ticker=ticker,
                                                                          days=days)
    
    
    page = urlopen(uri)
    data = page.read().decode('utf-8').split('\n')
    
    columns = ['Close', 'High', 'Low', 'Open', 'Volume'] 
    
    rows = []
    times = []
    
    
    
    for row in data:
        row = row.split(',')
        if row[0].startswith('1'):
            time = datetime.datetime.fromtimestamp(int(row[0]))
            times.append(time)
            rows.append(map(float, row[1:]))
            #print(row)
        
    if len(rows):   # save data as dataframe
        longTermDf = pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'),
                    columns=columns)
    else:
        longTermDf = pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'))
    
    import genIndicator as gi
    gi.genAll(longTermDf)   # generate all indicators before split
    
    dfList = []
    dfOneDay = pd.DataFrame(columns=list(longTermDf))
    lastIndex = None
    for index, row in longTermDf.iterrows():    # split data day by day
        row.name=index
        if lastIndex != None:
            if index.day != lastIndex.day:
                dfList.append(dfOneDay)
                dfOneDay = pd.DataFrame(columns=list(longTermDf))
        
        dfOneDay.loc[index] = row
        lastIndex = index
    dfList.append(dfOneDay) # the last day
    
    return dfList

if __name__ == '__main__':
    intradayList = get_yahoo_finance_intraday('SOP.PA', 5)
    for item in intradayList:
        print(item.index[0])

