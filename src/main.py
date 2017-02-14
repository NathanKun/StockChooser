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

             
import matplotlib.pyplot as plt, mpld3  # 2D plotting library
import genIndicator as gi
import constDaytime as cd



if __name__ == '__main__':
    #import sys
    #print(sys.path)
    
    print("start!")
    #plt.rcParams['figure.figsize'] = (15, 9)   # Change the size of plots


    # get 5 stocks data
    print("Getting data!")
    airbus = gi.getAndGen('airbus')
    biomerieux = gi.getAndGen('biomerieux')
    sopra = gi.getAndGen('sopra')
    total = gi.getAndGen('total')
    oreal = gi.getAndGen('oreal')

    import analyser
    #analyser.analyseRS(airbus)
    #analyser.analyseRSI(airbus)
    #analyser.analyseStochastic(airbus)
    print(analyser.analyseRS(biomerieux))
    
    gi.plotIndicator(airbus, 'MACD')
    #sopra.loc[cd.startShowing : cd.end, ['Close']].plot()
    
    gi.plotIndicator(biomerieux, 'RS')
    plt.show()
    
    
    
    print("End!")