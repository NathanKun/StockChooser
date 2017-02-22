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
    if stock == 'airbus':
        excelFIle = pd.ExcelFile('../data/Airbus.xlsx')
    elif stock == 'sopra':
        excelFIle = pd.ExcelFile('../data/Sopra.xlsx')
    elif stock == 'biomerieux':
        excelFIle = pd.ExcelFile('../data/Biomerieux.xlsx')
    elif stock == 'oreal':
        excelFIle = pd.ExcelFile('../data/Loreal.xlsx')
    elif stock == 'total':
        excelFIle = pd.ExcelFile('../data/Total.xlsx')
    
    return excelFIle
    
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
    
    
if __name__ == '__main__':
    ssList = analyseScoreFile(readScoreFile('oreal'))
    #ss = ssList[0]
    for ss in ssList:
        print(ss.date)
    
    
    
    
    
    
    
    
    
    