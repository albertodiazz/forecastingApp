from os import path
import pandas as pd

class cleanReporte:
    def __init__(self,_data_):
        self.path = _data_
        self.path = self.path.sort_values(by=['Date(UTC)'])
        df = pd.DataFrame({
            'Crypto': self.path['Market'],
            'Price': self.path['Price'],
            'Amount':self.path['Amount'],
            'Total': self.path['Total'],
            'Fee': self.path['Fee'],
            'Fee Coin': self.path['Fee Coin'],
            'Type': self.path['Type'],
            'isMaker': self.path['isMaker'],
            'Hora': self.path['Hora']
        })
        self.path = df
        df.to_csv('data/informe_general/reporte.csv')
        return

