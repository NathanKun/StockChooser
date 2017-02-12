'''
Created on 2017 2 9 

@author: Junyang HE
'''
'''
 pip install numpy
 pip install python-dateutil
 pip install pytz
 pip install pandas
 pip install pandas-datareader
 pip install jinja2
 pip install virtualenv
 pip install matplotlib
 pip install mpld3
 pip install Flask
 
 
 pip3 install numpy
 pip3 install python-dateutil
 pip3 install pytz
 pip3 install pandas
 pip3 install pandas-datareader
 pip3 install jinja2
 pip3 install virtualenv
 pip3 install matplotlib
 pip3 install mpld3
 pip3 install Flask
'''

             
from pandas_datareader import data      # for importing data
import matplotlib.pyplot as plt, mpld3  # 2D plotting library
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
    gi.plotIndicator(airbus, 'Adj close')
    
    #sopra.loc[cd.startShowing : cd.end, ['Close']].plot()
    
    
    #print(mpld3.fig_to_html(plt.gcf()))
    #import sys
    #print(sys.path)
    
    
    #plt.show()
    
    
    import analyser
    analyser.analyseRS(sopra)
    
    print("End!")