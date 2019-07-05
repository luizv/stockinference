# Libraries
import time
from iexfinance.stocks import get_historical_intraday
from iexfinance.stocks import Stock
import os
import requests
from SIConfig import SIConfig
from SITimeSeriesType import SITimeSeriesType
from datetime import datetime

# SET API PERMISSIONS
os.environ["IEX_API_VERSION"] = "iexcloud-sandbox"
os.environ["IEX_TOKEN"] = "Tpk_d9cc24d84d83489d88e9faeaf93dbaf8"


# Request settings
URL = "http://localhost:5000/stock/facts"
headers = {'content-type': 'application/json'}

if SIConfig.data_type == SITimeSeriesType.daily: pass
    # update_daily_data
elif SIConfig.data_type == SITimeSeriesType.intradaily: pass
    # update_intradaily_data




while True:
    # Get historical data minute by minute
    # data = get_historical_intraday('AAPL', date, output_format='pandas')
    data = Stock('AAPL').get_quote()

    # Data
    openValue = data['open']
    closeValue = data['close']
    highValue = data['high'] if data['high'] is not None else max(openValue, closeValue)
    lowValue = data['low'] if data['low'] is not None else min(openValue, closeValue)
    volumeData = data['latestVolume']


    # Print the data as it will be sent
    # Encoding JSON data
    data = '{"close":' + "{0:0.2f}".format(closeValue) + ', "open":' + "{0:0.2f}".format(openValue) + ', "high":' + "{0:0.2f}".format(highValue) + ', "low":' + "{0:0.2f}".format(lowValue) + '}'
    print(data)

    # Send request
    response = requests.post(URL, headers=headers, data=data)

    # Wait 1 second
    time.sleep(1)

