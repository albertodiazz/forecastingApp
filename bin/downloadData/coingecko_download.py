'''
Lo que hace este script es bajar la data de https://www.coingecko.com por medio de su API con ayuda del
data.JSON, el cual funge como una lista de las crypto que acutlamente tradeo, esa lista es actualizada
manualmente. En cuanto a los precios, no baja margenes de precio de entrada y cierre solo es data para una previzualisacion general
de las graficas
'''
from bin import pd,np,time,json,CoinGeckoAPI
from bin import constant as c

path =  c.PATHCOINGECKO
#esto no lo borre por que no me afecta
save_file = open(path + '/cardano.txt','w')
#aqui esta la lista de monedas que tradeo
lista_cryptos = c.PATHJSON

def get_lista_json(_path_):
    _lista_ = open(_path_,"r")
    _data_ = json.load(_lista_)
    api_call_crypto_name, save_name_file = [],[]
    for i in _data_['crypto_trade'][0]:
        save_name_file.append(i.lower())
        api_call_crypto_name.append(_data_['crypto_trade'][0][i])
    df = pd.DataFrame(columns=["name_file","crypto_api_name"])
    df['name_file'] = save_name_file
    df['crypto_api_name'] = api_call_crypto_name
    return df

def api_gecko(path_,output_file_,_id_,name_save_file):
    cg = CoinGeckoAPI()
    sb = cg.ping()
    status_gecko = False
    
    status_gecko = True
    resultado = cg.get_coin_market_chart_by_id(id=str(_id_),vs_currency='usd',days='365')
    fecha = []
    tiempo = []
    precios = []
    for i  in range(len(resultado['prices'])):
        fecha.append(time.strftime('%Y.%m.%d',time.localtime((resultado['prices'][i][0])/1000)))
        tiempo.append(time.strftime('%H:%M:%S',time.localtime((resultado['prices'][i][0])/1000)))
        precios.append(resultado['prices'][i][1])

    data_f = np.array(fecha)
    data_t = np.array(tiempo)
    data_p = np.array(precios)
    data_ = {'FECHA':data_f,'HORA':data_t,'PRECIO':data_p}
    df = pd.DataFrame(data=data_)
    

    df.to_csv(path_ + '/' + str(name_save_file) + '.csv')
    return status_gecko


def startDownload():
    data = get_lista_json(lista_cryptos)

    try:
        for index in range(len(data)):
            name_file = data['name_file'].iloc[index]
            id = data['crypto_api_name'].iloc[index]
            print(str(id),str(name_file))
            api_gecko(path,save_file,_id_=str(id),name_save_file=str(name_file))
            print('<<<<<<< ' + str(id) + ' >>>>>>>>>')
    except Exception as error:
        print(error)

#status_gecko = api_gecko(path,save_file)

