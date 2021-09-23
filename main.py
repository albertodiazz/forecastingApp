from os import error

from bin import np,pd,plt,notnull,concat
from bin import constant as c
from bin import uiInforme,type_sell_buy,pwd,jsw,informe_general


_DATE_INICIO_FONDO = c._DATE_INICIO_FONDO_

def mercado_historial(path,month):
    _data_ = pwd.preview_data(path,month)
    _data_.pasado = _DATE_INICIO_FONDO
    _data_ = _data_.read_data()
    return _data_


if __name__ == "__main__":
    #Las fechas estan atrasadas por un dia entonces no te puede aparecer el trade que hiciste ese mismo dia
    #Al iguial que tienes que estar al pendiente de actualizar la base de datos de las Candlestick 
    #y de coingecko
    _CRYPTO_ = c._CRYPTO_
    _MESES_ = c._MESES_
    #normal,informe
    _MODO_ = c._MODO_

    path_grafica = 'data/save_price/'+_CRYPTO_+'.csv'
    path_historial = 'data/trade_history/historial_trade.csv'

    info = informe_general.info()
    info.openPosition = pd.read_csv('data/trade_history/open_position.csv',index_col=0)
    info.carteraSpot =  pd.read_csv('data/trade_history/cartera_assets.csv',index_col=0)

    dataIN = pd.read_csv(path_grafica,index_col=0)
    mercado_ = mercado_historial(dataIN,_MESES_) 

    _type_ = type_sell_buy.sell_buy(path=path_historial,crypto=_CRYPTO_,month=_MESES_,mercado=mercado_)
    if _DATE_INICIO_FONDO != None:
        _type_.pasado = '-'.join(_DATE_INICIO_FONDO.split('.'))
    _data_  = _type_.convert_data_to()
    #<<<<<<<>>>>>>>>>
    #Mostramos todo
    crypto_all = jsw.json_workflow()
    if _DATE_INICIO_FONDO != None:
        crypto_all.pasado = '-'.join(_DATE_INICIO_FONDO.split('.'))
    _data_ALL = crypto_all.get_trades_historial(_data_,_MESES_)
    clean_data = crypto_all.clear_repeat_words(_data_ALL)
    mostras_todas_graficas,names_all = crypto_all.getll_all_graficas(clean_data,mercado_historial,_MESES_)        
    #<<<<<<<>>>>>>>>>
    #figure_, axis_ = plt.subplots(2,1,figsize=(12.2,4.5)) 

    try:
        modo = _MODO_.upper()
        if modo == 'NORMAL':
            plt.figure(figsize=(12.2,4.5))
            plt.xticks(rotation=90,fontsize=5)
            _buy_ = _type_.get_type(_data_,'buy')
            _sell_ = _type_.get_type(_data_,'sell')
            #<<<<<<<<<<>>>>>>>>>>>>
            #info.get_ganancias_perdias_comision(_buy_,_sell_)
            #<<<<<<<<<<<<<<<>>>>>>>>>>
            plt.scatter(_buy_.index,_buy_['Price'], color='green', 
                    label='Buy', 
                    marker = '^', 
                    alpha=1)

            plt.scatter(_sell_.index,_sell_['Price'], color='red', 
                    label='Sell', 
                    marker = '^', 
                    alpha=1)
            plt.plot(mercado_.index,mercado_['PRECIO'])
            
            plt.tight_layout()
            plt.show()

        elif modo == 'INFORME':      
            try:
                forInfo = pd.DataFrame([])
                forInfo['Moneda'] = names_all
                forInfo['PrecioUltimo'] = crypto_all.sinNormalizar
                info.mercado = forInfo
                info.path_historial = _data_ALL  

                _buy_ = _type_.get_type(_data_ALL,'buy')
                _sell_ = _type_.get_type(_data_ALL,'sell')
                info.get_ganancias_perdias_comision(_buy_,_sell_,clean_data)  

                info.info_depositos_pocentaje()
                info.info_dinero_inversionistas()
                #ESTO NO DEBERIA OCURRIR PERO SI OCURRE QUIERE DECIR QUE ESTOY TENIENDO PROBLEMA EN COMO 
                #ALMACENO LA DATA (BUNEO AL MENOS ESO CREO)
            except:
                pass
            uiInforme.draw()
            print('DIBUJAA PERRO!!')

    except Exception as e:
            #plt.plot(mercado_.index,mercado_['PRECIO'])
            print(e)
   