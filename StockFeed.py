# Libraries
import time
from iexfinance.stocks import get_historical_intraday
from iexfinance.stocks import Stock
import os
import requests
from SIConfig import SIConfig
from SITimeSeriesType import SITimeSeriesType
from SIStockStorage import SIStockStorage
from SIDatetimeFormatter import SIDatetimeFormatter
import pandas as pd
from datetime import datetime
import json

# SET API PERMISSIONS
os.environ["IEX_API_VERSION"] = "iexcloud-sandbox"
os.environ["IEX_TOKEN"] = "Tpk_d9cc24d84d83489d88e9faeaf93dbaf8"


# Request settings
URL = "http://localhost:5000/stock/facts"
headers = {'content-type': 'application/json'}


# Get data
data_dict = dict()

if SIConfig.data_type == SITimeSeriesType.daily:
    SIStockStorage.update_data_for_symbol_list()
    #data_dict = get_data_dictionary for daily...
elif SIConfig.data_type == SITimeSeriesType.intradaily:
    data_dict = SIStockStorage.get_intraday_data()



# while True:
#     # Get historical data minute by minute
#     # data = get_historical_intraday('AAPL', date, output_format='pandas')
#     data = Stock('AAPL').get_quote()
#     # Data
#     openValue = data['open']
#     closeValue = data['close']
#     highValue = data['high'] if data['high'] is not None else max(openValue, closeValue)
#     lowValue = data['low'] if data['low'] is not None else min(openValue, closeValue)
#     volumeData = data['latestVolume']
#
#
#     # Print the data as it will be sent
#     # Encoding JSON data
#     data = '{"close":' + "{0:0.2f}".format(closeValue) + ', "open":' + "{0:0.2f}".format(openValue) + ', "high":' + "{0:0.2f}".format(highValue) + ', "low":' + "{0:0.2f}".format(lowValue) + '}'
#     print(data)
#
#     # Send request
#     response = requests.post(URL, headers=headers, data=data)
#
#     # Wait 1 second
#     time.sleep(1)



## NOVO CICLO
while True:

    #por enquanto só tem a APPL nessa lista, mas é só trocar a lista pra mandar pra todos.
    for symbol in SIStockStorage.get_symbol_list():


        ## PEGANDO NOVOS DADOS, JUNTANDO COM OS HISTORICAL INTRADAY E NORMALIZANDO
        new_data = pd.DataFrame.from_records([Stock(symbol).get_quote()])
        print(new_data.columns)
        print(data_dict[symbol].columns)
        new_data = new_data[['close','open','low', 'high', 'latestTime', 'latestVolume', 'latestUpdate']]
        new_data.rename(columns={'latestUpdate':'datetime','latestVolume': 'volume', 'latestTime': 'date'}, inplace=True)


        # PROXIMA LINHA APENAS COM DADOS REAIS, SENÃO O TIMESTAMP VEM DOIDO
        # new_data['datetime'] = SIDatetimeFormatter.timestampToString(new_data['datetime'].item()/1000)

        new_data['datetime'] = datetime.now()
        new_data['date'] = new_data['datetime']
        new_data['high'] = new_data['high'].item() if new_data['high'].item() is not None else max(new_data['open'].item(), new_data['close'].item())
        new_data['low'] = new_data['low'].item() if new_data['low'].item() is not None else min(new_data['open'].item(), new_data['close'].item())

        new_data.set_index('datetime', inplace= True)


        data_dict[symbol] = pd.concat([data_dict[symbol], new_data])


        symbol_df = data_dict[symbol]
        symbol_df['datetime'] = symbol_df.index
        #symbol_df = symbol_df.transpose()
        #PARA VISUALIZAR SE TA ATUALIZANDO CERTO O DF
        #print(symbol_df.tail(10))


        # DUAS FORMAS DE ORGANIZAR O JSON PARA ENVIO
        #json = symbol_df.to_json(orient='split') # FORMA 1
        #json = symbol_dict.to_json(orient='split') # FORMA 2


        volume = list(symbol_df.volume.values)
        volume = [ int(x) for x in volume]
        low = list(symbol_df.low.values)
        high = list(symbol_df.high.values)
        close = list(symbol_df.close.values)
        open = list(symbol_df.open.values)
        date = list(symbol_df.datetime.values)
        date = [ int(x) for x in date]

        json2 = '{"date":' + json.dumps(date) + ',"low":' + json.dumps(low) + ',"high":' + json.dumps(high) +  ',"close":' + json.dumps(close) + ',"open":' + json.dumps(open) +  ',"volume":' + json.dumps(volume) + ',"type":' + str(SIConfig.data_type) + '}'
        print(json2)

        # Send request
        response = requests.post(URL, headers=headers, data=json2)


    # FORA DO FOR PORQUE SERAO VARIOS PAPÉIS:
    # Wait 1 second //TODO: pode ser um minuto (60)?
    time.sleep(1)
