'''
Created on 2017年2月11日

@author: Junyang HE
'''

    
import datetime

start = datetime.datetime(datetime.datetime.now().year-2,datetime.datetime.now().month,datetime.datetime.now().day) # data start day
end = datetime.date.today() # data end day, period of 2 year
startShowing = datetime.datetime(datetime.datetime.now().year-1,datetime.datetime.now().month,datetime.datetime.now().day)  # start showing graph day, period 1 year

trendLinesStartYear = datetime.datetime.now().year;     # trend lines for 4 month, calculate start day and month
trendLinesStartMonth = datetime.datetime.now().month;
if trendLinesStartMonth <= 4 :
    trendLinesStartMonth = trendLinesStartMonth + 8
    trendLinesStartYear -= 1
    trendLinesStartDate = datetime.datetime(trendLinesStartYear,trendLinesStartMonth,datetime.datetime.now().day)   # start drawing date