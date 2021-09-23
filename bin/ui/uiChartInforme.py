from typing import Text
from matplotlib import colors
from pandas.io.parsers import read_csv
import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

from PIL import Image, ImageTk
import io

from bin import chrt
from bin import constant as c

plt.style.use(c.ESTILOMATPLOIT)

def get_img_data(f, first=False):
    img = Image.open(f)
    img = img.resize((int(629/1.09),int(469/1.09)), Image.ANTIALIAS)
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

class uiChartInforme:
    def __init__(self):
        sg.theme('black')
        self._Window_ = None
        self.AppFont_ = 'Any 16'
        self._layout_ =  None
        self.color = c.HEXCOLOR
        self.TotalWallet_USDT = None
        self.percentPerdidaGanancia = None
        self.movimientosComisiones = None
        self.headersTable = None
        return

    def _layout_main(self):
        self._layout_ = [
            [
                sg.Button('Download',key='--Download--',enable_events=True),
                sg.Button('Normal',key='--Normal--',enable_events=True),
                sg.Button('Informe',key='--Informe--',enable_events=True)
            ]
        ]
        return self._layout_

    def _layout_informe(self):

        hexGreen = '#007f00'
        hexRed = '#cc2900'
        colorPerdidaGanancia,simbolo = None,None
        if round(float(ui.percentPerdidaGanancia),2) > 0:
            colorPerdidaGanancia =  hexGreen
            simbolo = '+'
        else: 
            colorPerdidaGanancia =  hexRed
            simbolo = '-'
        resultadoPorcentaje = simbolo + str(round(float(ui.percentPerdidaGanancia),2)) + '%'
        resultadoTotalUSDT = 'USDT: $'+ str(round(float(self.TotalWallet_USDT),2))

        self._layout_ = [
                [   
                    [
                        sg.Text(text=resultadoPorcentaje+'      ',pad=((0,500),(0,0)),justification='rigth',text_color=colorPerdidaGanancia,font=('Arial', 35),background_color=c.HEXCOLOR),
                        sg.Text(text=resultadoTotalUSDT,justification='rigth',text_color=colorPerdidaGanancia,font=('Arial', 30),background_color=c.HEXCOLOR),
                    ],
                     [                    
                        sg.Image(data=get_img_data('data/UI/informes/chartPercentInversores.png',first=True)),
                        sg.Image(data=get_img_data('data/UI/informes/chartPercent_Assets_CRYPTO.png',first=True)),
                        #sg.Text(text=resultadoTotalUSDT + ' ' + resultadoPorcentaje,size=(len(resultadoTotalUSDT),2),justification='center',text_color=colorPerdidaGanancia,font=('Arial', 35),background_color=setup.setupVariables().hexColor)
                    ],
                    [
                        sg.Image(data=get_img_data('data/UI/informes/chartMonedasTradeadas.png',first=True)),
                        sg.Image(data=get_img_data('data/UI/informes/chartBalanceUSDT.png',first=True))
                    ],

                   
                    [
                        sg.Table(values=self.movimientosComisiones,text_color='black',auto_size_columns=False,def_col_width=16,background_color=c.HEXCOLOR,num_rows=15),
                        #sg.Text(text=resultadoTotalUSDT + ' ' + resultadoPorcentaje,size=(len(resultadoTotalUSDT),2),justification='center',text_color=colorPerdidaGanancia,font=('Arial', 35),background_color=setup.setupVariables().hexColor),
                        #sg.Button('Exit',font=self.AppFont_)
                    ]
                ]
            
            ]
        return self._layout_

    def _window_setup(self,layout):
        self._Window_ = sg.Window('Such Window',
                                                layout,
                                                finalize=True,
                                                resizable=True,
                                                element_justification="center",
                                                background_color=self.color,
                                                location=(sg.Window.get_screen_size()[1]/2,0))
        return self._Window_   

    def draw_figure(self,canvas,plotFigure):
        figure_canvas_agg = FigureCanvasTkAgg(plotFigure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)    
        return figure_canvas_agg

#Esoty casi seguro que el estilo de programacion que estoy usando de aqui para abajo esta todo mal
#en un futuro corrigelo
ui = uiChartInforme()

def draw():
    wallet_free_assets = pd.read_csv(c.INFOWALLETFREE,index_col=0)
    movimientos_comisiones = pd.read_csv(c.INFOMOVIMIENTOSCOMISIONES,index_col=0, engine='python',header=None)
    info = pd.read_csv(c.INFO,index_col=0)

    ui.TotalWallet_USDT = info['Total_spot'][0]
    ui.percentPerdidaGanancia = info['Porcentaje'][0]

    ui.movimientosComisiones = movimientos_comisiones.values.tolist()

    chartsVisuales = chrt.visualesCharts(c.ESTILOMATPLOIT,c.HEXCOLOR)
    

    _WINDOWS = ui._window_setup(ui._layout_main())

    while True:
        event, values = _WINDOWS.read()
        if event == '--Normal--':
            print('Main UI')

        if event == '--Informe--':
            print('Informe UI')
            _WINDOWS = ui._window_setup(ui._layout_informe())

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    _WINDOWS.close()
