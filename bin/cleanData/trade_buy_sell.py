from bin.cleanData import trade_history as tdh
import pandas as pd
import datetime

class sell_buy:
    def __init__(self,path,crypto,month,mercado):
        self.path = path
        self.crypto = crypto
        self.rango  = month
        self.mercado = mercado
        self.pasado = None

    def convert_data_to(self):
            df  = pd.read_csv(self.path)
            df = df.rename(columns={'symbol':'Market',
                            'price':'Price',
                            'qty':'Amount',
                            'quoteQty':'Total',
                            'commission':'Fee',
                            'commissionAsset':'Fee Coin',
                            'isBuyer':'Type',
                            'time':'Date(UTC)'})
            df['Type']= df['Type'].map({True:'BUY',False:'SELL'})
            convert = lambda x: datetime.datetime.fromtimestamp(x / 1e3)
            df['Date(UTC)'] = df['Date(UTC)'].apply(convert)
            df['Date(UTC)'] = df['Date(UTC)'].astype(str)
            #df = df.set_index(['Date(UTC)'])
            #print(df.to_string())
            return df

    def get_type(self,_data,type_):
        #tan solo mando a llamar esto por el tema del rengo de fecha
        #arreglalo quitando la funcion del main para no hacer tanto desmadre
        try:
            _data_ = tdh.trade_history(_data)
            _data_.pasado = self.pasado
            _data_.acomodo_resultado(self.crypto)
            _data_tiempo =_data_.rango_tiempo(self.rango)
            _data_.read = _data_tiempo
            filter_historial_ = _data_.get_venta_compra(type_)
       
            _data_index_ = filter_historial_
            _data_index_ = _data_index_.index.str.split("-",n=2,expand=True)
            data_join = []
            for i in range(len(_data_index_)):
                data_join.append(_data_index_[i][0]+'.'+_data_index_[i][1]+'.'+_data_index_[i][2])
            filter_historial_.index = data_join
            filter_historial_.index.name = 'Date(UTC)'

            _data_ = pd.concat([self.mercado,filter_historial_])
        except:
            _data_ = _data.loc[_data['Type']==type_.upper()]
        return _data_

