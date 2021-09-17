from os import path, read
import pandas  as pd
from datetime import date
from dateutil.relativedelta import relativedelta

#Cuando compro me cobran el FEE en la moneda cripto
#Al vender me los cobran en USDT
class trade_history:
    def __init__(self,path):
        self.read = path
        self.today = None
        self.market = None
        self.pasado = None
        
    def acomodo_resultado(self,market):
        self.market = market + 'USDT'
        self.read = self.read.loc[self.read['Market']==self.market.upper()]
    
    def get_venta_compra(self,tipo):
        if tipo.upper() != 'ALL':
            self.read = self.read.loc[self.read['Type']==tipo.upper()]
            return self.read
        else:
            return self.read

    def rango_tiempo(self,rango):
        #Esto esta seteado para la data de coingecko 
        try:
            self.read = self.read.set_index(['Date(UTC)'])
        except:
            self.read = self.read
        
        #self.read = self.read.loc[(self.read.index >= '2021.05.13')& (self.read.index <'2021.06.13')]
        today_ = date.today()
        today_ = today_.strftime("%Y-%m-%d")

        _data_index = self.read.index.str.split(" ",n=1,expand=True)
        fecha,hora = [],[]
        for i in range(len(_data_index)):
           hora.append(_data_index[i][1])
           fecha.append(_data_index[i][0]) 
        self.read['Hora'] = hora  
        data = self.read.set_index([fecha])
        data.index.name = 'Date(UTC)'

        if self.pasado == None:
            current_date = date.today()
            past_date = current_date - relativedelta(months=rango)
            past_date  = past_date.strftime("%Y-%m-%d")
        else:
            past_date = self.pasado
        _data_ = data.loc[(data.index >= past_date)& (data.index <today_)] 
        df = _data_ #_data_.sort_index()
        
        return df