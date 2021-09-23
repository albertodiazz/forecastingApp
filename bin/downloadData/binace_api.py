import json,win32api,time,datetime
from bin import Client,pd
from bin import keyApiBinnace as key
from bin import constant as c
'''
    WebSocket connections have a limit of 5 incoming messages per second. A message is considered:
        A PING frame
        A PONG frame
        A JSON controlled message (e.g. subscribe, unsubscribe)
    A connection that goes beyond the limit will be disconnected; IPs that are repeatedly disconnected may be banned.
    A single connection can listen to a maximum of 1024 streams.
    
    Symbols
    https://api.binance.com/api/v1/ticker/allPrices
'''
class binance_data:
    def __init__(self):
        ApiKey = key.APIKEY
        SecretKey = key.SECRETKEY
        self.cliente = Client(ApiKey, SecretKey)
    
    def get_lista_json(self, _path_,_symbol_):
        _lista_ = open(_path_,"r")
        _data_ = json.load(_lista_)
        api_call_crypto_name, save_name_file = [],[]
        for i in _data_['crypto_trade'][0]:
            save_name_file.append(str(i)+_symbol_)
            api_call_crypto_name.append(_data_['crypto_trade'][0][i])
        df = pd.DataFrame(columns=["name_file","crypto_api_name"])
        df['name_file'] = save_name_file
        df['crypto_api_name'] = api_call_crypto_name
        return df

    def get_status(self):
        r = self.cliente.get_system_status()
        print('Respone: ', type(r), r)

    def server_time(self):
        r = self.cliente.get_server_time()
        print('Server Time: ', r['serverTime'] )
        tt=time.gmtime(int((r["serverTime"])/1000))
        win32api.SetSystemTime(tt[0],tt[1],0,tt[2],tt[3],tt[4],tt[5],0)   
    
    def get_klines(self,_symbol_,_path_,_intervals_='1d',_limit_=1000):
        # valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        #limit (int) – Default 500; max 1000
        try:
            timestamp = self.cliente._get_earliest_valid_timestamp(_symbol_,_intervals_)
            r = self.cliente.get_historical_klines(_symbol_, _intervals_, timestamp, limit=_limit_)
            with open(_path_+'/' +_symbol_+'.csv', 'w') as d:
                for line in r:
                    d.write(f'{line[0]}, {line[1]}, {line[2]}, {line[3]}, {line[4]}, {line[5]}, {line[6]}\n')
        except:
            print('Algo salio Mal en get_Klines en binance_api.py')
        return r

    def get_open_positions(self,_symbol_):
        #Aqui vemos cuales son las posiciones abiertas
        #Esto no refleja las cryptos en nuetra cartera
        r = self.cliente.get_open_orders(symbol=_symbol_)
        return r
    
    def get_all_trades(self, _symbol_):
        #Aqui vemos cuales son los trades realizados
        #Recuerda que el tiempo se mide en UNIX https://currentmillis.com/
        r = self.cliente.get_my_trades(symbol=_symbol_)
        return r

    def get_crytpos_cartera(self,_asset_):
        #Justo a la base de datos le falta la conversion a USDT
        for clean in _asset_.split('USDT'):
            if clean not in '':
                #print(clean.upper())
                r = self.cliente.get_asset_balance(asset=clean.upper())        
        return r

    def get_USDT_cartera(self,_asset_):
        r = self.cliente.get_asset_balance(asset=_asset_)   
        return r

    def get_time_snap(self,date):
        if date == 'now':
            dt = datetime.now()
            milliseconds = int(round(dt.timestamp() * 1000))
            return milliseconds
        else:
            r = date.split('-')
            ano = int(r[2])
            mes = int(r[1])
            dia = int(r[0])
            dt = datetime(ano,mes,dia)
            milliseconds = int(round(dt.timestamp() * 1000))
            return milliseconds 

    def save_csv(self,_path_,_data_):
        df = pd.DataFrame(_data_)
        df.to_csv(_path_)
        print(df)

def update_data_historialTrade():
    path_old = c.HISTORIALTRADE
    df = pd.read_csv(path_old,index_col=0)

    path_update = c.HISTORIALTRADEUPDATE
    df2 = pd.read_csv(path_update)
   
    dfNew = pd.concat([df,df2]).drop_duplicates()
    dfNew = dfNew[~dfNew.index.duplicated(keep='first')]

    df_save = pd.DataFrame(dfNew)
    dfNew.to_csv(path_old)
    print('UPDATE HISTORIAL TRADE!')
    return 

def downloadKlines():
    print('Download Klines')
    cliente = binance_data()
    status = cliente.get_status()
    cliente.get_klines('BTCUSDT',c.PATHKLINESDATA)
    return 'Download Finish'


def downloadTradeHistory():
    print('Download Trade History')
    path =  c.PATHJSON
    cliente = binance_data()
    status = cliente.get_status()
    #ARREGLAR PEDOS DE SINCRONIZACION CON EL CLIENTE
    #time_res = cliente.server_time()

    lista_cryptos = cliente.get_lista_json(path,'USDT')
    historial_trade = pd.DataFrame([])
    open_position = pd.DataFrame([])
    cartera_assets = pd.DataFrame([])

    for index in range(len(lista_cryptos)):
        print(lista_cryptos['name_file'].iloc[index])
        
        data = cliente.get_all_trades(lista_cryptos['name_file'].iloc[index])
        historial_trade = historial_trade.append(data)

        data_open_position = cliente.get_open_positions(lista_cryptos['name_file'].iloc[index])
        open_position = open_position.append(data_open_position)
        
        data_cartera = cliente.get_crytpos_cartera(lista_cryptos['name_file'].iloc[index])
        cartera_assets = cartera_assets.append(data_cartera,ignore_index=True)
        
    data_usdt_balance = cliente.get_USDT_cartera('USDT')
    cartera_assets = cartera_assets.append(data_usdt_balance,ignore_index=True)

    #historial_trade = append_avoid_dupllicados_historialTrade(historial_trade,'data/trade_history/historial_trade.csv')

    #Esto si lo tenemos que actualizar ya que es nuestro historial de trade y la plataforma de 
    #Binnace solo guarda un historial maximo de 3 meses (eso creo)
    cliente.save_csv(c.HISTORIALTRADEUPDATE,historial_trade)
    update_data_historialTrade()

    #OPEN POSITION Y CARTERA NO NESECITAN UN UPDATE O APPEND DE FECHAS
    cliente.save_csv(c.OPENPOSITION,open_position)
    cliente.save_csv(c.CARTERAASSETS,cartera_assets)

    return 'Download Finish'

