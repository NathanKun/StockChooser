'''
Created on 2017 2 17 

@author: Junyang HE
'''
import ssl
  
def readFinanceData():
    import pandas as pd
    financeData = pd.ExcelFile('../data/finance data.xlsx')
    bna = financeData.parse('BNA')
    per = financeData.parse('PER')
    returnRate = financeData.parse('rendement')
    dividend = financeData.parse('dividende')
    turnOver = financeData.parse('CA')
    return bna, per, returnRate, dividend, turnOver

def readScoreFile(stock):
    import pandas as pd
    airbusNote = pd.ExcelFile('../data/airbus.xlsx')
    # other files...
    return airbusNote
    
def analyseScoreFile(df):
    sheetsName = df.sheet_names
    import scoreStructure as ss
    ssList = []
    for name in sheetsName:
        daySheet = df.parse(name)
        temp = ss.Score(name)
        temp.time = daySheet.iat[1, 6]
        temp.critere = daySheet.iloc[0:4, 0:4]
        temp.graphic = daySheet.iloc[9:14, 0:5]
        temp.finance = daySheet.iloc[18:23, 0:5]
        temp.finalScore = daySheet.iat[0, 6]
        temp.graphic.columns = daySheet.iloc[8:9, 0:5].as_matrix()[0]
        temp.finance.columns = daySheet.iloc[17:18, 0:5].as_matrix()[0]
        ssList.append(temp)
    return ssList
    
ssList = analyseScoreFile(readScoreFile('airbus'))
ss = ssList[1]
print(ss.date[:2])
    
    
    
    
    
    
    
    
    
    