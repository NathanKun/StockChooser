'''
Created on 2017 2 12 

@author: NathanKun
'''
from genIndicator import stochastic
from audioop import cross
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
    _, _, _, maxslope, minslope = gi.gentrends(df.loc[cd.trendLinesStartDate : cd.yesterday, 'Adj Close'], window = 1.0/2, charts = False)
    delta = df['resistance'] - df['support']
    #print(delta)
    result = 0
    
    # rule 1
    if maxslope > 0 and minslope > 0 :
        print('trends going up')
        result += 0.3
    elif maxslope < 0 and minslope < 0 :
        print('trends going down')
        result -= 0.3
        
    # rule 2
    if 0.85 <= (df.at[cd.yesterday, 'Adj Close'] - df.at[cd.yesterday, 'support']) / delta.get(cd.yesterday) <= 1 :
        print('price is going to touch resistance => price will go down')
        result -= 0.6
    
    # rule 3
    if 0 <= (df.at[cd.yesterday, 'Adj Close'] - df.at[cd.yesterday, 'support']) / delta.get(cd.yesterday) <= 0.15 :
        print('price is going to touch support => price will go up')
        result += 0.6
        
    # rule 4
    if df.at[cd.yesterday, 'Adj Close'] > df.at[cd.yesterday, 'resistance'] :
        print('price is over resistance')
        if df['Adj Close'].get(cd.yesterday) > df['Adj Close'][len(df.index) - 2] :
            print('and price is still going up')
            result += 0.7
        else :
            print('but price is going down')
            result += 0.2
        
    # rule 5
    if df.at[cd.yesterday, 'Adj Close'] < df.at[cd.yesterday, 'support'] :
        print('price is under support')
        if df['Adj Close'].get(cd.yesterday) < df['Adj Close'][len(df.index) - 2] :
            print('and price is still going down')
            result -= 0.7
        else :
            print('but price is going up')
            result += 0.3
    
    return result

def analyseRSI(df):
    '''
    Si RSI < 30 : 
    Excès baissier : le cours a bien chuté et devrait rebondir.
    Si 30 < RSI < 50 :
    Courant vendeur, sans excès (zone de vente)
    Si 50 < RSI < 70 :
    Le cours a bien chuté et devrait rebondir.
    SI RSI > 70 :
    Le cours a bien progressé et devrait corriger.
    '''
    result = 0
    rsi = df['RSI']
    import constDaytime as cd
    rsiT1 = rsi.get(cd.yesterday)
    rsiT0 = rsi[len(df.index) - 2] # rsi[len(df.index) - 1] is the last term
    
    if rsiT1 <= 20 :
        print('RSI <= 20, oversold')
        result = 1
        
    elif 20 < rsiT1 <= 30 :
        print('RSI <= 30, maybe oversold')
        result = 0.7
        if rsiT1 < rsiT0 :
            print('and still going down')
            result = 0.85
            
    elif 30 < rsiT1 <= 45 :
        print('30 < RSI <= 45, weak market')
        result = -0.5
        
    elif 45 < rsiT1 < 55 :
        print('45 < RSI < 55, normal market')
        result = 0
        
    elif 55 <= rsiT1 < 70 :
        print('55 <= RSI < 70, strong market')
        result = 0.5
        
    elif 70 <= rsiT1 < 80 :
        print('rsi >= 70, maybe overbought')
        result = -0.7
        if rsiT1 > rsiT0 :
            print('and still going up')
            result = -0.85
            
    elif rsiT1 >= 80 :
        print('rsi >= 80, overbought')
        result = -1
    
    return result
    
def analyseStochastic(df):
    '''
    Si D < 20 : zone de survente (la valeur est considérée comme survendue).  
    Toutefois, il sera nécessaire d’attendre le franchissement à la hausse de ce même niveau pour confirmer le signal d’achat. 
    Si la valeur de D augmente, on peut acheter.
    
    Si D> 80 : La valeur devient surachetée. 
    Le signal de vente se déclenche une fois ce même niveau est franchi à la baisse. 
    Si la valeur de D diminue, on peut vendre.

    Stochastique rapide
    La stochastique rapide K est calculée sur une période de 14 jours.
    A l’instant t – 14,    K< D
    A l’instant t, K> D
    On achète lorsque le stochastique K coupe à la hausse sa ligne de signal D.
    '''
    result = 0
    
    k = df['k slow']
    d = df['d slow']
    j = df['j slow']
    
    k1 = k[len(df.index) - 1]
    d1 = d[len(df.index) - 1]
    j1 = j[len(df.index) - 1]
    d_5 = d[len(df.index) - 6]
    
    # j is the most important
    if j1 > 100 :
        print('j > 100, really overbought')
        result = -1
    elif j1 < 0 :
        print('j < 0, really oversold')
        result = 1
    
    if d_5 > 80 and d1 < 80 :   # if d passed 80% and go back now
        print('d was > 80, d < 80 now, overbought')
        result -= 0.9
    elif d_5 < 20 and d1 > 20 : # if d passed 20% and go back now
        print('d was < 20, d > 20 now, oversold')
        result += 0.9
    elif d1 > 80 :              # if d passed 80%
        print('d > 80, overbought')
        result -= 0.6
    elif d1 < 20 :              # if d passed 20%
        print('d < 20, oversold')
        result += 0.6
    
    crossed = False
    if k1 > d1 :
        for i in range(1, 15) :
            if k[len(df.index) - i] < d[len(df.index) - i] :    # if k crossed above d for last 14 days
                if not crossed :
                    print('k crossed above d for last 14 days')
                crossed = True
        if crossed :
            result += 0.8
    
    if result >= 1 :
        return 1
    elif result <= -1 :
        return -1
    else :
        return result
    
    
    

def analyseFinanceData(df):
    import readFromFile as rff
    bna, per, returnRate, dividend, turnOver = rff.readFinanceData()
    
    
    
    
    
    
    
    
    
    
    