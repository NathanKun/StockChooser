'''
Created on 2017 2 11 

@author: Junyang HE
'''
from matplotlib.pyplot import grid

# generate line function
def genLineInDataframe(y, df):
    import pandas as pd     # data structures and data analysis tools
    series = pd.Series()
    series.set_value(0, 0)
    for i in range(0, df.size) :
        series.set_value(value = y, label = i)  # calculate difference between two days\
    series.index = df.index
    return series


# generate useful lines
def genLines(df):
    #df['0.2 Line'] = genLineInDataframe(0.2, df['Close'])
    #df['0.8 Line'] = genLineInDataframe(0.8, df['Close'])
    df['20 Line'] = genLineInDataframe(20, df['Close'])
    df['30 Line'] = genLineInDataframe(30, df['Close'])
    df['70 Line'] = genLineInDataframe(70, df['Close'])
    df['80 Line'] = genLineInDataframe(80, df['Close'])
    
    
# calculate moving average
def genMA(df, maDays = [5, 10, 20, 40]):
    for ma in maDays:
        column_name = "MA for %s days" %(str(ma))
        df[column_name] = df['Adj Close'].rolling(center=False,window=ma).mean()
        
    
# calculate bollinger bands. MA20 +- 2*std
def genBollinger(df, length = 20, numsd = 2):
    import numpy as np      # fundamental package for scientific computing
    """ returns average, upper band, and lower band"""
    ave = df['Adj Close'].rolling(window=length).mean()
    std = df['Adj Close'].rolling(window=length).std()
    upband = ave + (std * numsd)
    dnband = ave - (std * numsd)
    df['bollinger ave'] = np.round(ave,3)
    df['bollinger upper'] = np.round(upband,3)
    df['bollinger lower'] = np.round(dnband,3)
    
    
    
def gentrends(x, window=1/3.0, charts=True):
    ''' https://github.com/dysonance/Trendy    Numerical trendline Python algorithms '''
    """
    Returns a Pandas dataframe with support and resistance lines.

    :param x: One-dimensional data set
    :param window: How long the trendlines should be. If window < 1, then it
                   will be taken as a percentage of the size of the data
    :param charts: Boolean value saying whether to print chart to screen
    """

    import numpy as np      # fundamental package for scientific computing
    import pandas as pd     # data structures and data analysis tools

    x = np.array(x)

    if window < 1:
        window = int(window * len(x))

    max1 = np.where(x == max(x))[0][0]  # find the index of the abs max
    min1 = np.where(x == min(x))[0][0]  # find the index of the abs min

    # First the max
    if max1 + window > len(x):
        max2 = max(x[0:(max1 - window)])
    else:
        max2 = max(x[(max1 + window):])

    # Now the min
    if min1 - window < 0:
        min2 = min(x[(min1 + window):])
    else:
        min2 = min(x[0:(min1 - window)])

    # Now find the indices of the secondary extrema
    max2 = np.where(x == max2)[0][0]  # find the index of the 2nd max
    min2 = np.where(x == min2)[0][0]  # find the index of the 2nd min

    # Create & extend the lines
    maxslope = (x[max1] - x[max2]) / (max1 - max2)  # slope between max points
    minslope = (x[min1] - x[min2]) / (min1 - min2)  # slope between min points
    a_max = x[max1] - (maxslope * max1)  # y-intercept for max trendline
    a_min = x[min1] - (minslope * min1)  # y-intercept for min trendline
    b_max = x[max1] + (maxslope * (len(x) - max1))  # extend to last data pt
    b_min = x[min1] + (minslope * (len(x) - min1))  # extend to last data point
    maxline = np.linspace(a_max, b_max, len(x))  # Y values between max's
    minline = np.linspace(a_min, b_min, len(x))  # Y values between min's

    # OUTPUT
    trends = np.transpose(np.array((x, maxline, minline)))
    trends = pd.DataFrame(trends, index=np.arange(0, len(x)),
                          columns=['Data', 'Max Line', 'Min Line'])

    if charts is True:
        from matplotlib.pyplot import plot, grid, show
        plot(trends)
        grid()
        show()

    return trends, maxline, minline, maxslope, minslope
    
# calculate resistance and support
def genRS(df) :
    import constDaytime as cd

    _, df.loc[cd.trendLinesStartDate : cd.end, 'resistance'], df.loc[cd.trendLinesStartDate : cd.end, 'support'], _, _ \
        = gentrends(df.loc[cd.trendLinesStartDate : cd.end, 'Adj Close'], window = 1.0/2, charts = False)   #generate trend lines, ignore first return value
        
        
# calculate MACD(12, 26, 9)
def genMACD(df):
    ema12 = df['Adj Close'].ewm(min_periods = 12, span = 12).mean()
    ema26 = df['Adj Close'].ewm(min_periods = 26, span = 26).mean()
    dif = ema12 - ema26                             # DIF
    dem = dif.ewm(min_periods = 9, span = 9).mean() # MACD
    df['dif'] = dif         # DIF
    df['MACD'] = dem        # MACD
    df['osc'] = dif - dem   # histogram
        

    
# calculate RSI
    '''
    series = pd.Series()
    series.set_value(0, 0)
    for i in range(1, airbus['Adj Close'].size) :
        series.set_value(value = airbus['Adj Close'].iloc[i] - airbus['Adj Close'].iloc[i - 1], label = i)  # calculate difference between two days
    series.index = airbus.index #reset index of series to the same index as dataframe, otherwise it cannot be combine into dataframe
    '''
    #airbus['delta'] = airbus['Adj Close'].diff()    # diff() can do the same thing as above
def genRSI(df):
    df['delta'] = df['Adj Close'].diff()
    dUp, dDown = df['delta'].copy(), df['delta'].copy()
    dUp[dUp < 0] = 0        # fill NaN with 0
    dDown[dDown > 0] = 0
    
    rolUp=dUp.ewm(com = 13).mean()   # exp moving average
    rolDown=dDown.ewm(com = 13).mean().abs()
    
    rolUp = rolUp.reindex_like(df, method='ffill')      # rename index
    rolDown = rolDown.reindex_like(df, method='ffill')
    
    rs = rolUp / rolDown
    rsi = 100.0 - (100.0 / (1.0 + rs))
    df['rsi'] = rsi
        

# calculate stochastic
def stochastic(stockHigh, stockLow, stockClose, p1, p2, p3, version):
    high = stockHigh.rolling(window = p1).max()        # highest price for 9 last day
    low = stockLow.rolling(window = p1).min()          # lowest ..
    
    if version == 'fast' :
        k = (stockClose - low) / (high - low)     # calculate %k
        d = k.rolling(min_periods = p3, window = p3).mean() # calculate %d
  
    if version == 'slow' :
        k = (stockClose - low) / (high - low)     # calculate %k
        k = k.rolling(min_periods = p2, window = p2).mean() # calculate %kslow = %dfast
        d = k.rolling(min_periods = p3, window = p3).mean() # calculate %dslow
            
    k *= 100
    d *= 100
    #ds = k.ewm(min_periods = p3, alpha = 1.0/3).mean()   # calculate %d ? $d slow
        
    return k, d

# generate stochastic fast and slow
def genStochastic(df):
    df['k slow'], df['d slow'] = stochastic(df['High'], df['Low'], df['Close'], 14, 3, 5, 'slow')   # boursorama : Stochastique lent (14,3,5)
    df['k fast'], df['d fast'] = stochastic(df['High'], df['Low'], df['Close'], 1, 1, 5, 'fast') # boursorama : Stochastique rapide (1,1,5)
        

def genAll(df):
    genLines(df)
    genMA(df, [5, 10, 20, 40])
    genBollinger(df)
    genMACD(df)
    genRS(df)
    genRSI(df)
    genStochastic(df)
    

def plotIndicator(df, ind, maDays = [5, 10, 20, 40]):
    import constDaytime as cd
    if ind == 'MA':
        if maDays != [5, 10, 20, 40]:   
            nameList = []
            for ma in maDays:
                columnName = "MA for %s days" %(str(ma))
                nameList.append(columnName)
            if len(nameList) == 0 :
                pass
            elif len(nameList) == 1 :
                df.loc[cd.startShowing : cd.end, ['Adj Close',nameList[0]]].plot(grid = True, figsize = (10, 5))
            elif len(nameList) == 2 :
                df.loc[cd.startShowing : cd.end, ['Adj Close',nameList[0],nameList[1]]].plot(grid = True, figsize = (10, 5))
            elif len(nameList) == 3 :
                df.loc[cd.startShowing : cd.end, ['Adj Close',nameList[0],nameList[1],nameList[2]]].plot(grid = True, figsize = (10, 5))
            elif len(nameList) == 4 :
                df.loc[cd.startShowing : cd.end, ['Adj Close',nameList[0],nameList[1],nameList[2],nameList[3]]].plot(grid = True, figsize = (10, 5))
            elif len(nameList) == 5 :
                df.loc[cd.startShowing : cd.end, ['Adj Close',nameList[0],nameList[1],nameList[2],nameList[3],nameList[4]]].plot(grid = True, figsize = (10, 5))
            elif len(nameList) == 6 :
                df.loc[cd.startShowing : cd.end, ['Adj Close',nameList[0],nameList[1],nameList[2],nameList[3],nameList[4],nameList[5]]].plot(grid = True, figsize = (10, 5))
            elif len(nameList) == 7 :
                df.loc[cd.startShowing : cd.end, ['Adj Close',nameList[0],nameList[1],nameList[2],nameList[3],nameList[4],nameList[5],nameList[6]]].plot(grid = True, figsize = (10, 5))
        else :
            df.loc[cd.startShowing : cd.end, ['Adj Close','MA for 5 days','MA for 10 days','MA for 20 days','MA for 40 days']].plot(grid = True, figsize = (10, 5))
    elif ind == 'Bollinger':
        df.loc[cd.startShowing : cd.end, ['Adj Close','bollinger upper','bollinger ave','bollinger lower']].plot(grid = True, figsize = (10, 5))
    elif ind == 'RS':
        df.loc[cd.startShowing : cd.end, ['Adj Close', 'resistance', 'support']].plot(grid = True, figsize = (10, 5))
    elif ind == 'MACD':
        df.loc[cd.startShowing : cd.end, ['Adj Close', 'dif', 'MACD']].plot(grid = True, figsize = (10, 5), secondary_y = ["dif", "MACD"])    # use different scales
    elif ind == 'RSI':
        df.loc[cd.startShowing : cd.end, ['rsi', '30 Line', '70 Line']].plot(grid = True, figsize = (10, 5))
    elif ind == 'Stoschastic':
        df.loc[cd.startShowing : cd.end, ['k fast', 'd fast', '20 Line', '80 Line']].plot(grid = True, figsize = (10, 5))
    elif ind == 'Adj close':
        df['Adj Close'].plot(grid = True, figsize = (10, 5))
    elif ind == 'Close':
        df['Close'].plot(grid = True, figsize = (10, 5))
    
# get data from yahoo api
def readDataFromNet(stock):
    from pandas_datareader import data      # for importing data
    import constDaytime as cd
    df = None
    if stock == 'airbus':
        df = data.DataReader("AIR.PA", "yahoo", cd.start, cd.end) 
    elif stock == 'sopra':
        df = data.DataReader("SOP.PA", "yahoo", cd.start, cd.end)
    elif stock == 'biomerieux':
        df = data.DataReader("FP.PA", "yahoo", cd.start, cd.end)
    elif stock == 'oreal':
        df = data.DataReader("OR.PA", "yahoo", cd.start, cd.end)
    elif stock == 'total':
        df = data.DataReader("BIM.PA", "yahoo", cd.start, cd.end)
    return df