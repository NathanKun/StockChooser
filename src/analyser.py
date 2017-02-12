'''
Created on 2017 2 12 

@author: NathanKun
'''
def analyseRS(df):
    '''
    delta = resistance - support
    price(t1) - support(t1) < 0 => Going down, sell
    price(t1) - resistance(t1) > 0 => Going up, buy
    
    '''
    import genIndicator as gi
    import constDaytime as cd
    _, _, _, maxslope, minslope = gi.gentrends(df.loc[cd.trendLinesStartDate : cd.end, 'Adj Close'], window = 1.0/2, charts = False)
    if maxslope > 0 and minslope > 0 :
        print('ok')
    return 0