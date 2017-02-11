'''
Created on 2017年2月9日

@author: Junyang HE
'''
from array import array
from matplotlib.pyplot import subplot

'''
 pip install pandas
 pip install pandas-datareader
 pip install matplotlib
'''


#import pandas as pd                     
from pandas_datareader import data      # for importing data
import matplotlib.pyplot as plt         # 2D plotting library
import genIndicator as gi
import constDaytime as cd


if __name__ == '__main__':
    print("cd.start!")
    
    #plt.rcParams['figure.figsize'] = (15, 9)   # Change the size of plots
    
        


    # get 5 stocks data
    print("Getting data!")
    airbus = data.DataReader("AIR.PA", "yahoo", cd.start, cd.end) # get data from yahoo api
    sopra = data.DataReader("SOP.PA", "yahoo", cd.start, cd.end)
    #total = data.DataReader("FP.PA", "yahoo", cd.start, cd.end)
    #oreal = data.DataReader("OR.PA", "yahoo", cd.start, cd.end)
    #biome = data.DataReader("BIM.PA", "yahoo", cd.start, cd.end)
    

        
    # DataFrame as parameter will be modified, so no need to return
    gi.genLines(sopra)
    gi.genMA(sopra, [15,30,100])
    gi.genBollinger(sopra)
    gi.genRS(sopra)
    gi.genMACD(sopra)
    gi.genRSI(sopra)
    gi.genStochastic(sopra)
    
    gi.genAll(airbus)
    
    gi.plotIndicator(sopra, 'MA', [15,30,100])
    gi.plotIndicator(airbus, 'MACD')

    
    plt.show()
    
    print("cd.end!")