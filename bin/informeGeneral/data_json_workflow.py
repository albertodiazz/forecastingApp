from bin import clsR,relativedelta,date,pd,json

class json_workflow:
    def __init__(self):
        self.path = None
        self.pasado = None
        self.sinNormalizar = []
        return

    def get_trades_historial(self,_data_,_meses_):
        #obtenemos nuestros trades por mes o en un rango de tiempo que establescamos
        _data_ = _data_.set_index(['Date(UTC)'])
        _data_index = _data_.index.str.split(" ",n=1,expand=True)
        fecha,hora = [],[]
        for i in range(len(_data_index)):
           hora.append(_data_index[i][1])
           fecha.append(_data_index[i][0])   
        _data_['Hora'] = hora
        _data_.set_index([fecha],inplace=True)
        _data_.index.name = 'Date(UTC)'

        today = date.today()
        today = today.strftime("%Y-%m-%d")
   
        if self.pasado == None:
            current_date = date.today()
            past_date = current_date - relativedelta(months=_meses_)
            past_date  = past_date.strftime("%Y-%m-%d")
        else:
            past_date = self.pasado
        _data_ = _data_.loc[(_data_.index >= past_date)& (_data_.index <today)] 
        df = _data_ #_data_.sort_index()
        #df.to_csv('data/informe_general/reporte.csv')
        clsR.cleanReporte(df)
        return df
    
    def clear_repeat_words(self,_data__):
        _data_ = _data__
        lista = []
        for index in range(len(_data_)):
            lista.append(_data_['Market'].iloc[index])
        res = []
        for i in lista:
            if i not in res:
                res.append(i)       
        return res
    
    def get_names_all(self,data_):
        return data_

    def getll_all_graficas(self,clean_data,mercado_historial,_MESES_):        
        l,names = [],[]
        equal_len = 0 
        for value in clean_data:
            for i in value.split('USDT'):
                if i not in '':
                    dataIN_Array = pd.read_csv('data/save_price/'+ i.lower() +'.csv',index_col=0)
                    mercado_Array = mercado_historial(dataIN_Array,_MESES_)
                    self.sinNormalizar.append(dataIN_Array['PRECIO'].iloc[-1])
                    for column in mercado_Array.index:
                        mercado_Array['PRECIO'] = (mercado_Array['PRECIO'] -mercado_Array['PRECIO'].mean() ) / mercado_Array['PRECIO'].std()
                    #l.append(i.lower()) 
                    if equal_len == 0:
                        len_size = len(mercado_Array['PRECIO'])
                        equal_len = 1
                    if len(mercado_Array['PRECIO']) > len_size:
                        mercado_Array.drop(index=mercado_Array.index[0], 
                                            axis=0, 
                                            inplace=True)
                        l.append(mercado_Array['PRECIO'] )
                        #print('FIXED LEN')
                    else:
                        l.append(mercado_Array['PRECIO'])
                    names.append(i.upper())
                    #resultado[i.lower()] = l
                    #print(i, ' : ', len(mercado_Array['PRECIO']))
        return l,names