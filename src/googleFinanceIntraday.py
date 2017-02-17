# https://gist.github.com/lebedov/f09030b865c4cb142af1
"""
Retrieve intraday stock data from Google Finance.
"""

import csv
import datetime
import re

import pandas as pd
from urllib.request import urlopen
from _datetime import date

def get_google_finance_intraday(ticker, period=60, days=1):
    """
    Retrieve intraday stock data from Google Finance.
    Parameters
    ----------
    ticker : str
        Company ticker symbol.
    period : int
        Interval between stock values in seconds.
    days : int
        Number of days of data to retrieve.
    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing the opening price, high price, low price,
        closing price, and volume. The index contains the times associated with
        the retrieved price values.
    """

    uri = 'https://www.google.com/finance/getprices' \
          '?i={period}&p={days}d&f=d,o,h,l,c,v&df=cpct&q={ticker}'.format(ticker=ticker,
                                                                          period=period,
                                                                          days=days)
    page = urlopen(uri)
    #reader = csv.reader(page.content.splitlines())
    data = page.read().decode('utf-8').split('\n')
    #print(data)
    columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    rows = []
    times = []
    
    dfList = []
    dayCount = 0
    dayCountTriggered = False
    
    for row in data:
        row = row.split(',')
        
        if dayCountTriggered and dayCount > 1:
            dayCountTriggered = False
            rowLast = rows[-1]      # the last element is for the next day, copy and delete it
            timeLast = times[-1]
            rows.pop()              
            times.pop()
            
            if len(rows):           # add df in list
                dfList.append(pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'),
                            columns=columns))
            else:
                dfList.append(pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date')))
            rows = []
            times = []
            rows.append(rowLast)    # put it in the new list
            times.append(timeLast)
                
        if re.match('^[a\d]', row[0]):
            if row[0].startswith('a'):
                dayCountTriggered = True
                dayCount += 1
                #print(int(row[0][1:10]))
                start = datetime.datetime.fromtimestamp(int(row[0][1:]))
                times.append(start)
            else:
                times.append(start+datetime.timedelta(seconds=period*int(row[0])))
            rows.append(map(float, row[1:]))
    
    if len(rows):
        dfList.append(pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'),
                    columns=columns))
    else:
        dfList.append(pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date')))
            
    return dfList


intradayList = get_google_finance_intraday('AIR.PA', 60, 15)
dateList = []
for item in intradayList :
    dateList.append(item.index[0].strftime('%d/%m/%Y'))
                
seletedDateTimeStr = '13/02/2017 - 13h26'
seletedDateTime = datetime.datetime.strptime(seletedDateTimeStr, '%d/%m/%Y - %Hh%M')
seletedDateStr = seletedDateTimeStr[0:10]
seletedTimeStr = seletedDateTimeStr[13:18]
df = intradayList[dateList.index(seletedDateStr)]
startShowPoint = df.index[0]    # type : timestamp
#endShowPoint = seletedDateTime.timestamp()
endShowPoint = pd.Timestamp(seletedDateTime)
print(endShowPoint)
