from bin import pd
from bin import constant as c

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
        df.to_csv(c.INFOREPORTE)
        return

