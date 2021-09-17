import matplotlib.pyplot as plt
from numpy import info
import pandas as pd

class visualesCharts:
    def __init__(self,matploitstyle,hexcolor):
        self.esilomatploit = matploitstyle
        self.hexcolor = hexcolor
        plt.style.use(self.esilomatploit)
        return

    def chartPercent_Assets_CRYPTO(self,wallet_free_assets,movimientos_comisiones,TotalWallet_USDT,percentPerdidaGanancia):
        #print(df)
        dp = movimientos_comisiones.loc[movimientos_comisiones['spot wallet USDT'] > 0.1]
        dp = dp.iloc[:-1 , :]
        dp['moneda'] = dp['moneda'].str.split("USDT",n=1,expand=True)
        self.chartPercent_Crypto = pd.DataFrame({'Asset': dp['moneda'],
                                            'Cantidad': dp['spot wallet USDT']
        })
        self.chartPercent_Crypto.loc[len(self.chartPercent_Crypto)] = ['USDT',wallet_free_assets['Conversion_USDT'].iloc[-1]]
        
        self.chartPercent_Crypto = self.chartPercent_Crypto.set_index('Asset')
        self.chartPercent_Crypto['Porcentaje'] = self.chartPercent_Crypto['Cantidad']/self.chartPercent_Crypto['Cantidad'].sum() * 100
        #self.chartPercent_Crypto['Porcentaje'] = self.chartPercent_Crypto['Porcentaje'].astype(int)
        self.chartPercent_Crypto['Porcentaje'] = self.chartPercent_Crypto['Porcentaje'].round(2)
        
        plt.pie(self.chartPercent_Crypto['Cantidad'],startangle=90,autopct='%1.1f%%')
        circle = plt.Circle(xy=(0,0), radius=0.75, facecolor=self.hexcolor)
        plt.gca().add_artist(circle)
        plt.legend(labels=self.chartPercent_Crypto.index)
        plt.axis('equal')
        plt.tight_layout()
        return plt
    
    def chartPercentInversores(self,_info_):
        plt.pie(_info_['Porcentaje'],startangle=90,autopct='%1.1f%%')
        circle = plt.Circle(xy=(0,0), radius=0.75, facecolor=self.hexcolor)
        plt.gca().add_artist(circle)
        plt.legend(labels=_info_['Name'].astype(str))
        plt.axis('equal')
        plt.tight_layout()
        return plt

    def chartMonedasTradeadas(self,_info_):
        df = pd.DataFrame({
            'moneda':_info_['moneda'],
            'trades':_info_['trades']
        })
        df = df.sort_values(by=['trades'])
        df.set_index('moneda',inplace=True)
        df = df.drop(df[df.trades == 0].index)
        plt.bar(df.index,df['trades'])
        plt.xticks(rotation='45')
        plt.tight_layout()
        return plt

    def chartBalanceUSDT(self,_info_):
        df = pd.DataFrame({
            'moneda':_info_['moneda'],
            'trades':_info_['balance']
        })
        df = df.sort_values(by=['trades'])
        df.set_index('moneda',inplace=True)
        df = df.drop(df[df.index == 'Total'].index)
        plt.bar(df.index,df['trades'])
        plt.xticks(rotation='45')
        plt.tight_layout()
        return plt

