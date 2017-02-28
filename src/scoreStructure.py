'''
Created on 2017 2 17

@author: Junyang HE
'''

class Score :
    
    date = None
    time = None
    criterion = []
    graphic = []
    finance = []
    finalScore = []
    
    def __init__(self, date):
        self.date = date
        self.time = None
        self.criterion = []
        self.graphic = []
        self.finance = []
        self.finalScore = []