# Libraries
import time
from iexfinance.stocks import get_historical_intraday
from iexfinance.stocks import Stock
import os
import requests
from datetime import datetime

# SET API PERMISSIONS
os.environ["IEX_API_VERSION"] = "iexcloud-sandbox"
os.environ["IEX_TOKEN"] = "Tpk_d9cc24d84d83489d88e9faeaf93dbaf8"

# Set data interval
date = datetime(2019, 5, 23)



# Request settings
URL = "http://localhost:5000/stock/facts"
headers = {'content-type': 'application/json'}

# Send a request to each according
index = 0
while True:
    # Get historical data minute by minute
    # data = get_historical_intraday('AAPL', date, output_format='pandas')
    data = Stock('AAPL').get_quote()

    # Data
    openData = data['open']
    closeData = data['close']
    highData = data['high']
    lowData = data['low']
    volumeData = data['latestVolume']

    # Separate the data
    openValue = openData
    closeValue = closeData
    highValue = highData
    lowValue = lowData

    # Print the data as it will be sent

    # Encoding JSON data
    data = '{"close":' + "{0:0.2f}".format(closeValue) + ', "open":' + "{0:0.2f}".format(openValue) + ', "high":' + "{0:0.2f}".format(highValue) + ', "low":' + "{0:0.2f}".format(lowValue) + '}'
    print(data)

    # Send request
    response = requests.post(URL, headers=headers, data=data)

    # Wait 1 second
    time.sleep(1)

    # Increment index control
    index += 1
