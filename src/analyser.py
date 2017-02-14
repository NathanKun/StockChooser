'''
Created on 2017 2 12 

@author: NathanKun
'''
def analyseRS(df):
    '''
    Analyse:
    1. both trends going up => price going up
    2. price is going to touch resistance => price will go down
    3. price is going to touch support => price will go up
    4. price is over resistance => price will go up
    5. price is under support => price will go down
    
    Math:
    delta = resistance - support
    1. maxslope > 0 and minslope > 0 => price going up
       maxslope < 0 and minslope < 0 => price going down
    2. (price(t) - support(t)) / delta > 90% => price is going to touch resistance => price will go down
    3. (price(t) - support(t)) / delta < 10% => price is going to touch support => price will go up
    4. price(t) > resistance(t) && price is going up => price is over resistance => price will go up
    5. price(t) < resistance(t) && price is going down  => price is under support => price will go down
    
    '''
    
    import genIndicator as gi
    import constDaytime as cd
    _, resistance, support, maxslope, minslope = gi.gentrends(df.loc[cd.trendLinesStartDate : cd.end, 'Adj Close'], window = 1.0/2, charts = False)
    delta = df['resistance'] - df['support']
    
    result = 0
    
    # rule 1
    if maxslope > 0 and minslope > 0 :
        print('trends going up')
        result += 0.3
    elif maxslope < 0 and minslope < 0 :
        print('trends going down')
        result -= 0.3
        
    # rule 2
    if (0.9 <= df['Adj close'][cd.end] - df['resistance'][cd.end]) / delta[cd.end] <= 1 :
        print('price is going to touch resistance => price will go down')
        result -= 0.6
    
    # rule 3
    if (0 <= df['Adj close'][cd.end] - df['support'][cd.end]) / delta[cd.end] <= 0.1 :
        print('price is going to touch support => price will go up')
        result += 0.6
        
    # rule 4
    if df['Adj close'][cd.end] > df['resistance'][cd.end]
        print('price is over resistance')
        if df.iat[len(df.index), ['Adj close']] > df.iat[len(df.index) - 1, ['Adj close']] :
            print('and price is still going up')
            result += 0.7
        else :
            print('but price is going down')
            result += 0.2
    go up')
        
    # rule 5
    if df['Adj close'][cd.end] < df['support'][cd.end]
        print('price is under support')
        if df.iat[len(df.index), ['Adj close']] < df.iat[len(df.index) - 1, ['Adj close']] :
            print('and price is still going down')
            result -= 0.7
        else :
            print('but price is going up')
            result += 0.3
    
    return result
