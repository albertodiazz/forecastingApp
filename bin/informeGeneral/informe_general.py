from bin import performance_doc,DataFrame,json,pd
from bin import constant as c

class info:
    def __init__(self) -> None:
        self.openPosition = None
        self.carteraSpot = None
        self.mercado = None
        self.path_historial = None
        self.data_pieChart = None
        self.porcentaje = None
        self.totalUSDT_SPOT = None
        pass
    def get_asset_alocation(self):
        print('')

    def info_depositos_pocentaje(self):
        path = c.DEPOSITOS
        read = pd.read_csv(path)
        read.set_index(['Date'],inplace=True)

        read['Monto MXN'] = read.groupby(['Name'])['Monto MXN'].transform('sum')
        sin_duplicados_totales = read.drop_duplicates(subset=['Name'])

        id = []
        for i in range(len(sin_duplicados_totales)):
            id.append(i)

        porcentaje = pd.DataFrame([])
        porcentaje['Name'] = sin_duplicados_totales['Name']
        porcentaje['Monto MXN'] = sin_duplicados_totales['Monto MXN']
        porcentaje['Porcentaje'] = sin_duplicados_totales['Monto MXN']/sin_duplicados_totales['Monto MXN'].sum() * 100
        porcentaje.set_index([id],inplace=True)
        #print(porcentaje)
        self.porcentaje =porcentaje
        #Name,Monto,Porcentaje
        return porcentaje

    def info_dinero_inversionistas(self):
        #OJO TAN SOLO AGREGANDO INVERSIONISTAS AL CSV NO GENERARA UN PORCENTAJE COHERENTE
        #EJEMPLO SI CREAS UNA PERSONA CON 500 PESOS EL PORCENTAJE NO REFLEJARA SUS 500 PESOS
        #YA QUE EL DEPOSITO AUN NO HA CAIDO EN BINANCE
        df = self.porcentaje
        df['USDT'] = (self.porcentaje['Porcentaje'] * self.totalUSDT_SPOT) / 100
        print('\n')
        df.to_csv(c.INFOPORCENTAJEINVERSIONISTAS)
        print(df)
        return

    def get_ganancias_perdias_comision(self,_buy_,_sell_,crypto_list=None):
        #OJO tienes que tener cuidad con las posiciones abiertas ya que te las contara como perdidas
        #la ventaja de este sistema es que en teoria te da el total de lo que si puedes retirar y de ahi
        
        f = open(c.PATHJSON)
        data_jason = json.load(f)
        n,p = [],[]
        for _crypto_ in data_jason['crypto_trade'][0]:
            data = pd.read_csv('data/save_price/'+str(_crypto_).lower() + '.csv')
            #print(_crypto_,data['PRECIO'].iloc[-1])
            n.append(_crypto_)
            p.append(data['PRECIO'].iloc[-1])
        last_price = pd.DataFrame({'Last_Price': p},index=n)

        #OPEN POSITION
        #Si no reviso esto me causa un bug en caso de estar vacio el documento de open_position
        isempty = self.openPosition.empty
        if isempty != True:
            self.openPosition['symbol']  = (self.openPosition['symbol'].str.split("USDT",n=1,expand=True))
            self.openPosition = self.openPosition.set_index(['symbol'])
            open_name,open_precio,open_crypto,open_usdt=[],[],[],[]
            for i in range(len(last_price)):
                name = last_price.index[i]
                precio = last_price['Last_Price'][i]
                for d in range(len(self.openPosition)):
                    if self.openPosition.index[d] == name:
                        open_name.append(name)
                        open_precio.append(precio)
                        open_crypto.append(self.openPosition['origQty'][d])
                        open_usdt.append((self.openPosition['origQty'][d]*precio))
            open_position_data = pd.DataFrame({'Moneda':open_name,
                                                'Precio_Ultimo': open_precio,
                                                'Crypto' : open_crypto,
                                                'Conversion_USDT': open_usdt
            })
            print('\n OPEN POSITION \n',open_position_data)
            open_position_data.to_csv(c.OPENPOSITION)            
            print('TOTAL', open_position_data['Conversion_USDT'].sum())
        else:
            print("OPEN POSITION IS EMPTY",isempty)
        #EN WALLET FREE
        seguro_wallet_free = 0
        wallet_free_name,wallet_free_precio,wallet_free_crypto,wallet_free_usdt=[],[],[],[]
        for i in range(len(last_price)):
            name = last_price.index[i]
            precio = last_price['Last_Price'][i]
            for d in range(len(self.carteraSpot)):
                if self.carteraSpot['asset'][d] == name:
                    wallet_free_name.append(name)
                    wallet_free_precio.append(precio)
                    wallet_free_crypto.append(self.carteraSpot['free'][d])
                    wallet_free_usdt.append((self.carteraSpot['free'][d]) * precio)
        #Aqui agarramos el valor de USDT OJO que esto me puede causar un bug ya que siempre estamos agarrando el ultimo valor
        #si llega a cambiar de lugar eso nos supondra un problema
        wallet_free_name.append(self.carteraSpot['asset'].iloc[-1])
        wallet_free_precio.append(0)
        wallet_free_crypto.append(0)
        wallet_free_usdt.append(self.carteraSpot['free'].iloc[-1])

        wallet_free_assets = pd.DataFrame({'Moneda':wallet_free_name,
                                            'Precio_Ultimo': wallet_free_precio,
                                            'Crypto' : wallet_free_crypto,
                                            'Conversion_USDT': wallet_free_usdt
        })
        print('\n WALLET FREE \n',wallet_free_assets)
        wallet_free_assets.to_csv(c.INFOWALLETFREE)            
        print('TOTAL', wallet_free_assets['Conversion_USDT'].sum())

        #HISTORIAL TRADE
        precios_spot_wallet = []
        posecion_wallet_monedas_spot = []
        valor_en_USDT,seguro = [],0
        for i in range(len(self.mercado)):
            name = self.mercado['Moneda'][i]
            precio = self.mercado['PrecioUltimo'][i]
            for x in range(len(self.carteraSpot)):
                if self.carteraSpot['asset'][x] == name:
                    resultado = (self.carteraSpot['free'][x]+self.carteraSpot['locked'][x]) * precio
                    posecion_wallet = round((self.carteraSpot['free'][x]+self.carteraSpot['free'][x]),2)
                    #print('\n find', name,precio, resultado)
                    precios_spot_wallet.append(resultado)
                    posecion_wallet_monedas_spot.append(posecion_wallet)
                elif self.carteraSpot['asset'][x] == 'USDT' and seguro == 0:
                    seguro = 1
                    valor_en_USDT.append(self.carteraSpot['free'][x] + self.carteraSpot['locked'][x])

        posecion_wallet_monedas_spot.append(0)
 
        totalUSDT_SPOT = sum(precios_spot_wallet)+valor_en_USDT
    

        total_spot = sum(precios_spot_wallet)
        precios_spot_wallet.append(total_spot)
        
        #agregarle la conversion a usdt
        #hnt ganacia de 72
        cryto_list = []
        lista_sell,lista_buy = [],[]
        comision_buy_all,comision_sell_all = [],[]
        cantidad_trades = []
        perdida_ganancia = []

        if crypto_list != None:
            for i in range(len(crypto_list)):
                cryto_list.append(crypto_list[i])
                buy_all = _buy_.loc[_buy_['Market']==crypto_list[i]]            
                sell_all = _sell_.loc[_sell_['Market']==crypto_list[i]]
                lista_buy.append(buy_all['Total'].sum() - buy_all['Fee'].sum())
                comision_buy_all.append(buy_all['Fee'].sum())
                lista_sell.append(sell_all['Total'].sum() - sell_all['Fee'].sum())
                comision_sell_all.append(sell_all['Fee'].sum())
                cantidad_trades.append(len(buy_all['Total'])+len(sell_all['Total']))
            cantidad_trades.append(0)
            
            reporte_mensual = pd.DataFrame({'moneda':crypto_list,
                                            'buy':lista_buy,
                                            'sell':lista_sell,
                                            'comision_buy':comision_buy_all,
                                            'comision_sell':comision_sell_all
                                            })
            reporte_mensual.loc[len(reporte_mensual.index)] = ['Total',
                                                                reporte_mensual['buy'].sum(),
                                                                reporte_mensual['sell'].sum(),
                                                                reporte_mensual['comision_buy'].sum(),
                                                                reporte_mensual['comision_sell'].sum()
                                                                ]
            reporte_mensual['trades'] =  cantidad_trades                                          
            reporte_mensual['spot wallet USDT'] = precios_spot_wallet
            reporte_mensual['balance'] = (((reporte_mensual['buy'] -  reporte_mensual['comision_buy']) -  (reporte_mensual['sell'] -  reporte_mensual['comision_sell'])) -reporte_mensual['spot wallet USDT'])*-1

            resultado_inversion = ((reporte_mensual['buy'][int(len(reporte_mensual.index))-1] - reporte_mensual['comision_buy'][int(len(reporte_mensual.index))-1]) - (reporte_mensual['sell'][int(len(reporte_mensual.index))-1] - reporte_mensual['comision_sell'][int(len(reporte_mensual.index))-1]))
            print('\n MOVIMIENTOS Y COMISIONES DE TRADES')
            print(reporte_mensual)
            reporte_mensual.to_csv(c.INFOMOVIMIENTOSCOMISIONES)            
            #print('\n',reporte_mensual['balance']+reporte_mensual['spot wallet USDT'])
            resultado = resultado_inversion
            self.totalUSDT_SPOT = totalUSDT_SPOT[0]
            print('\n TOTAL EN USDT EN LA WALLET DE SPOT: ',totalUSDT_SPOT[0])
            #print('\n GANANCIA O PERDIDA DEL PERIODO USDT', resultado-totalUSDT_SPOT[0])
            reporte_mensual_ = reporte_mensual['balance'].iloc[-1]
            print('\n PERDIDA O GANANCIA', reporte_mensual_)
            porcentaje_ganacia_perdida = (reporte_mensual['balance'].iloc[-1]/(totalUSDT_SPOT[0]+reporte_mensual['balance'].iloc[-1].__abs__()))*100
            print('\n PORCENTAJE', porcentaje_ganacia_perdida)
            print('\nOJO TAL VEZ ESTO NO CASE CON LA DATA DE BINANCE YA QUE YO ESTOY SUMANDO TAMBIEN LAS GANANCIAS DE LOS TRADES')
            print('POR LO TANTO EL PORTAFOLIO VALE MAS Y LOS PORCENTAJES SON DIFERENTES')

            #INFO GENERAL
            info = pd.DataFrame({'Total_spot':totalUSDT_SPOT[0],
                                'Perdida_Ganancia':reporte_mensual_,
                                'Porcentaje':porcentaje_ganacia_perdida},index=[0])
            info.to_csv(c.INFO)
            
            #PIE DATA CHART
            dp = reporte_mensual.loc[reporte_mensual['spot wallet USDT'] > 0.1]
            dp = dp.iloc[:-1 , :]
            dp['moneda'] = dp['moneda'].str.split("USDT",n=1,expand=True)
            self.data_pieChart = pd.DataFrame({'Asset': dp['moneda'],
                                              'Cantidad': dp['spot wallet USDT']
            })
            self.data_pieChart.loc[len(self.data_pieChart)] = ['USDT',wallet_free_assets['Conversion_USDT'].iloc[-1]]
            
            self.data_pieChart = self.data_pieChart.set_index('Asset')
            self.data_pieChart['Porcentaje'] = self.data_pieChart['Cantidad']/self.data_pieChart['Cantidad'].sum() * 100
            #self.data_pieChart['Porcentaje'] = self.data_pieChart['Porcentaje'].astype(int)
            self.data_pieChart['Porcentaje'] = self.data_pieChart['Porcentaje'].round(2)
            #print('\n',self.data_pieChart)
                
        else:
            compras = _buy_['Total'] - _buy_['Fee']
            ventas = _sell_['Total'] - _sell_['Fee']
            resultado = (compras.sum() - ventas.sum()) *-1
            print('BUY: ',compras.sum(), 'Comision: ', _buy_['Fee'].sum())
            print('SELL: ',ventas.sum(), 'Comision: ', _sell_['Fee'].sum())
            print('GANANCIA/PERDIDA: ',resultado)
        return resultado