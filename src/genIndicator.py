'''
Created on 2017 2 11 

@author: Junyang HE
'''

# generate line function
# deprecate, use df['new'] = level
def genLineInDataframe(y, df):
    import pandas as pd     # data structures and data analysis tools
    series = pd.Series()
    series.set_value(0, 0)
    for i in range(0, df.size) :
        series.set_value(value = y, label = i)
    series.index = df.index
    return series


# generate useful lines
def genLines(df):
    #df['0.2 Line'] = genLineInDataframe(0.2, df['Close'])
    #df['0.8 Line'] = genLineInDataframe(0.8, df['Close'])
    '''
    df['20 Line'] = genLineInDataframe(20, df['Close'])
    df['30 Line'] = genLineInDataframe(30, df['Close'])
    df['70 Line'] = genLineInDataframe(70, df['Close'])
    df['80 Line'] = genLineInDataframe(80, df['Close'])
    '''
    df['20 Line'] = 20
    df['30 Line'] = 30
    df['70 Line'] = 70
    df['80 Line'] = 80
    
    
# calculate moving average
def genMA(df, maDays = [5, 20, 40]):
    for ma in maDays:
        column_name = "MA%s" %(str(ma))
        df[column_name] = df['Close'].rolling(center=False,window=ma).mean()
        
    
# calculate bollinger bands. MA20 +- 2*std
def genBollinger(df, length = 20, numsd = 2):
    import numpy as np      # fundamental package for scientific computing
    """ returns average, upper band, and lower band"""
    ave = df['Close'].rolling(window=length).mean()
    std = df['Close'].rolling(window=length).std()
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
        = gentrends(df.loc[cd.trendLinesStartDate : cd.end, 'Close'], window = 1.0/2, charts = False)   #generate trend lines, ignore first return value
        
        
# calculate MACD(12, 26, 9)
def genMACD(df):
    ema12 = df['Close'].ewm(min_periods = 12, span = 12).mean()
    ema26 = df['Close'].ewm(min_periods = 26, span = 26).mean()
    dif = ema12 - ema26                             # DIF
    dem = dif.ewm(min_periods = 9, span = 9).mean() # MACD
    df['dif'] = dif         # DIF
    df['MACD'] = dem        # MACD
    df['osc'] = dif - dem   # histogram
        

    
# calculate RSI
    '''
    series = pd.Series()
    series.set_value(0, 0)
    for i in range(1, airbus['Close'].size) :
        series.set_value(value = airbus['Close'].iloc[i] - airbus['Close'].iloc[i - 1], label = i)  # calculate difference between two days
    series.index = airbus.index #reset index of series to the same index as dataframe, otherwise it cannot be combine into dataframe
    '''
    #airbus['delta'] = airbus['Close'].diff()    # diff() can do the same thing as above
def genRSI(df):
    df['delta'] = df['Close'].diff()
    dUp, dDown = df['delta'].copy(), df['delta'].copy()
    dUp[dUp < 0] = 0        # fill NaN with 0
    dDown[dDown > 0] = 0
    
    rolUp=dUp.ewm(com = 13).mean()   # exp moving average
    rolDown=dDown.ewm(com = 13).mean().abs()
    
    rolUp = rolUp.reindex_like(df, method='ffill')      # rename index
    rolDown = rolDown.reindex_like(df, method='ffill')
    
    rs = rolUp / rolDown
    rsi = 100.0 - (100.0 / (1.0 + rs))
    df['RSI'] = rsi
        

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
    j = 3*d - 2*k
    #ds = k.ewm(min_periods = p3, alpha = 1.0/3).mean()   # calculate %d ? $d slow
        
    return k, d, j

# generate stochastic fast and slow
def genStochastic(df):
    df['k slow'], df['d slow'], df['j slow'] = stochastic(df['High'], df['Low'], df['Close'], 14, 3, 5, 'slow')   # boursorama : Stochastique lent (14,3,5)
    df['k fast'], df['d fast'], df['j fast'] = stochastic(df['High'], df['Low'], df['Close'], 1, 1, 5, 'fast') # boursorama : Stochastique rapide (1,1,5)
        
# generate all indicators
def genAll(df):
    if not isinstance(df, str) :
        #print("generating lines")
        genLines(df)
        #print("lines done")
        genMA(df, [5, 20, 40])
        #print("ma done")
        genBollinger(df)
        #print("bo done")
        genMACD(df)
        #print("macd done")
        #genRS(df)
        #print("rs done")
        genRSI(df)
        #print("rsi done")
        genStochastic(df)
        #print("stoc done")
    else : pass
    
# plot a indicator
import constDaytime as cd
def plotIndicator(df, ind, maDays = [5, 20, 40], startShowPoint = cd.startShowing, endShowPoint = cd.end, title = None):
    if not isinstance(df, str) :
        if ind == 'MA':
            if maDays != [5, 20, 40]:   
                nameList = []
                for ma in maDays:
                    columnName = "MA%s" %(str(ma))
                    nameList.append(columnName)
                if len(nameList) == 0 :
                    pass
                elif len(nameList) == 1 :
                    df.loc[startShowPoint : endShowPoint, ['Close',nameList[0]]].plot(
                        grid = True, figsize = (10, 5), title = title)
                elif len(nameList) == 2 :
                    df.loc[startShowPoint : endShowPoint, ['Close',nameList[0],nameList[1]]].plot(
                        grid = True, figsize = (10, 5), title = title)
                elif len(nameList) == 3 :
                    df.loc[startShowPoint : endShowPoint, ['Close',nameList[0],nameList[1],nameList[2]]].plot(
                        grid = True, figsize = (10, 5), title = title)
                elif len(nameList) == 4 :
                    df.loc[startShowPoint : endShowPoint, ['Close',nameList[0],nameList[1],nameList[2],nameList[3]]].plot(
                        grid = True, figsize = (10, 5), title = title)
                elif len(nameList) == 5 :
                    df.loc[startShowPoint : endShowPoint, ['Close',nameList[0],nameList[1],nameList[2],nameList[3],nameList[4]]].plot(
                        grid = True, figsize = (10, 5), title = title)
                elif len(nameList) == 6 :
                    df.loc[startShowPoint : endShowPoint, ['Close',nameList[0],nameList[1],nameList[2],nameList[3],nameList[4],nameList[5]]].plot(
                        grid = True, figsize = (10, 5), title = title)
                elif len(nameList) == 7 :
                    df.loc[startShowPoint : endShowPoint, ['Close',nameList[0],nameList[1],nameList[2],nameList[3],nameList[4],nameList[5],nameList[6]]].plot(
                        grid = True, figsize = (10, 5), title = title)
            else :
                #df.loc[startShowPoint : endShowPoint, ['Close', 'MA5', 'MA20', 'MA40']].plot(grid = True, figsize = (10, 5))
                df.loc[startShowPoint : endShowPoint, ['Close', 'MA5', 'MA20']].plot(
                    grid = True, figsize = (10, 5), title = title)
        elif ind == 'Bollinger':
            df.loc[startShowPoint : endShowPoint, ['Close','bollinger upper','bollinger ave','bollinger lower']].plot(
                grid = True, figsize = (10, 5), title = title)
        elif ind == 'RS':
            df.loc[startShowPoint : endShowPoint, ['Close', 'resistance', 'support']].plot(
                grid = True, figsize = (10, 5), title = title)
        elif ind == 'MACD':
            df.loc[startShowPoint : endShowPoint, ['dif', 'MACD']].plot(
                grid = True, figsize = (10, 5), title = title)
        elif ind == 'RSI':
            df.loc[startShowPoint : endShowPoint, ['RSI', '30 Line', '70 Line']].plot(
                grid = True, figsize = (10, 5), title = title)
        elif ind == 'Stochastic':
            df.loc[startShowPoint : endShowPoint, ['k slow', 'd slow', 'j slow', '20 Line', '80 Line']].plot(
                grid = True, figsize = (10, 5), title = title)
        elif ind == 'Adj Close':
            df['Adj Close'].plot(grid = True, figsize = (10, 5), title = title)
        elif ind == 'Close':
            df['Close'].plot(grid = True, figsize = (10, 5), title = title)
    else : pass
    
# get data from yahoo api
def readDataFromNet(stock):
    from pandas_datareader import data      # for importing data
    import fix_yahoo_finance
    if stock == 'airbus':
        df = data.get_data_yahoo("AIR.PA", cd.start, cd.end) 
    elif stock == 'sopra':
        df = data.get_data_yahoo("SOP.PA", cd.start, cd.end)
    elif stock == 'biomerieux':
        df = data.get_data_yahoo("BIM.PA", cd.start, cd.end)
    elif stock == 'oreal':
        df = data.get_data_yahoo("OR.PA", cd.start, cd.end)
    elif stock == 'total':
        df = data.get_data_yahoo("FP.PA", cd.start, cd.end)
    else:
        try :
            df = data.get_data_yahoo(stock, cd.start, cd.end)
        except :
            df = "Read data failed."    # read from yahoo failed
    return df

# get data from Internet and generate all indicators
def getAndGen(stock):
    df = readDataFromNet(stock)
    if not isinstance(df, str) :
        genAll(df)
    return df