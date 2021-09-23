from bin import chrt,save,pd
from bin import constant as c

def run():
    print('Iniciando conversion de Imagenes')
    
    wallet_free_assets = pd.read_csv(c.INFOWALLETFREE,index_col=0)
    movimientos_comisiones = pd.read_csv(c.INFOMOVIMIENTOSCOMISIONES,index_col=0)
    info = pd.read_csv(c.INFO,index_col=0)
    porcentajeInversionistas = pd.read_csv(c.INFOPORCENTAJEINVERSIONISTAS)

    charts = chrt.visualesCharts(c.ESTILOMATPLOIT,c.HEXCOLOR)
    
    chartPercent_Assets_CRYPTO = charts.chartPercent_Assets_CRYPTO(wallet_free_assets,movimientos_comisiones,info['Total_spot'][0],info['Porcentaje'][0])
    save(c.ESTILOMATPLOIT,c.HEXCOLOR).saveImage(chartPercent_Assets_CRYPTO,'chartPercent_Assets_CRYPTO')

    chartPercentInversores = charts.chartPercentInversores(porcentajeInversionistas)
    save(c.ESTILOMATPLOIT,c.HEXCOLOR).saveImage(chartPercentInversores,'chartPercentInversores')
    

    chartMonedasTradeadas = charts.chartMonedasTradeadas(movimientos_comisiones)
    save(c.ESTILOMATPLOIT,c.HEXCOLOR).saveImage(chartMonedasTradeadas,'chartMonedasTradeadas')
    
    chartBalanceUSDT = charts.chartBalanceUSDT(movimientos_comisiones)
    save(c.ESTILOMATPLOIT,c.HEXCOLOR).saveImage(chartBalanceUSDT,'chartBalanceUSDT')
    
    
    #plt.show()