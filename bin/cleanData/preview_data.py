import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import json
from dateutil.relativedelta import relativedelta

class preview_data:
    def __init__(self,dataIN,month):        
        self.dataIN = dataIN
        self.range = month #rango en meses
        self.fecha_rango = None
        self.pasado = None
        self.df = None

    def read_data(self):
        #Esto esta seteado para la data de coingecko 
        self.df = self.dataIN
        self.df = self.df.set_index(['FECHA'])
        today = date.today()
        today = today.strftime("%Y.%m.%d")
        
        if  self.pasado  == None:
            current_date = date.today()
            past_date = current_date - relativedelta(months= self.range)
            past_date  = past_date.strftime("%Y.%m.%d") 
            #self.df = self.df.loc[(self.df.index >= '2021.05.13')& (self.df.index <'2021.06.13')]
        else:
            past_date=  self.pasado 
            #print(today)

  
        data = self.df
        _data_ = data.loc[(data.index >= past_date)& (data.index <today)] 
        df = _data_
        
        return df




