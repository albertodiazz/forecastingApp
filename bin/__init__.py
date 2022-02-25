from typing import Text
from matplotlib import colors
from pandas.io.parsers import read_csv
from pandas.core.dtypes.missing import notnull
from pandas.core.reshape.concat import concat

import PySimpleGUI as sg
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from os import path, read

import matplotlib.pyplot as plt
import pandas as pd

from numpy import info

from datetime import date
import json
from dateutil.relativedelta import relativedelta
import datetime as datetime
import time 
from pandas.io.pytables import performance_doc
from pandas.core.frame import DataFrame


from pandas.core.algorithms import mode
import requests
import asyncio

#BINANCE
from binance.client import Client
import win32api

#COINGECKO
from pycoingecko import CoinGeckoAPI

#SUPER IMPORTANTE AQUI IMPORTAMOS LAS CREDENCIALES DE BINNACE
#APIKEY = 'APIKEY'
#SECRETKEY = 'SECRETKEY'
import bin.keyApiBinnace

#MODULOS PROPIOS
from bin.ui.convertChartsImage import chartsVisuales  as chrt
from bin.ui.convertChartsImage import conversionCharts as save
import bin.ui.uiChartInforme as uiInforme

import bin.informeGeneral.clean_reporte as clsR
import bin.informeGeneral.data_json_workflow as jsw
import bin.informeGeneral.informe_general as informe_general


from bin.cleanData import trade_history as tdh
from bin.cleanData import preview_data as pwd
from bin.cleanData import trade_buy_sell as type_sell_buy

#LIBRERIAS PARA DESCARGAR DATA
from bin.downloadData.binace_api import downloadTradeHistory
from bin.downloadData.binace_api import downloadKlines
from bin.downloadData.coingecko_download import startDownload as startDownloadCoingecko

#LIBRERIA PARA CORRER CONVERSION DE IMAGEN
from bin.ui.runConvert import run as convertUi