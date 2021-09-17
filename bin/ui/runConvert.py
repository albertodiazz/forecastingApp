from ui.convertChartsImage import chartsVisuales  as chrt
from ui.convertChartsImage import conversionCharts as save
import pandas as pd
from ui import constant as c

def run():
    print('Iniciando conversion de Imagenes')
    
    wallet_free_assets = pd.read_csv(c.WALLETFREE,index_col=0)
    movimientos_comisiones = pd.read_csv(c.MOVIMIENTOSCOMISIONES,index_col=0)
    info = pd.read_csv(c.INFO,index_col=0)
    porcentajeInversionistas = pd.read_csv(c.PORCENTAJEINVERSIONISTAS)

    charts = chrt.visualesCharts()
    
    chartPercent_Assets_CRYPTO = charts.chartPercent_Assets_CRYPTO(wallet_free_assets,movimientos_comisiones,info['Total_spot'][0],info['Porcentaje'][0])
    save(c.ESTILOMATPLOIT,c.HEXCOLOR).saveImage(chartPercent_Assets_CRYPTO,'chartPercent_Assets_CRYPTO')

    chartPercentInversores = charts.chartPercentInversores(porcentajeInversionistas)
    save(c.ESTILOMATPLOIT,c.HEXCOLOR).saveImage(chartPercentInversores,'chartPercentInversores')
    

    chartMonedasTradeadas = charts.chartMonedasTradeadas(movimientos_comisiones)
    save(c.ESTILOMATPLOIT,c.HEXCOLOR).saveImage(chartMonedasTradeadas,'chartMonedasTradeadas')
    
    chartBalanceUSDT = charts.chartBalanceUSDT(movimientos_comisiones)
    save(c.ESTILOMATPLOIT,c.HEXCOLOR).saveImage(chartBalanceUSDT,'chartBalanceUSDT')
    
    
    #plt.show()