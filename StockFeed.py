# Libraries
import time
from iexfinance.stocks import get_historical_intraday
import os
import requests
from datetime import datetime

# SET API PERMISSIONS
os.environ["IEX_API_VERSION"] = "iexcloud-sandbox"
os.environ["IEX_TOKEN"] = "Tpk_d9cc24d84d83489d88e9faeaf93dbaf8"

# Set data interval
date = datetime(2019, 5, 23)

# Get historical data minute by minute
data = get_historical_intraday('AAPL', date, output_format='pandas')

# Data
openData = data[['open']]
closeData = data[['close']]
highData = data[['high']]
lowData = data[['low']]
volumeData = data[['volume']]

# Request settings
URL = "http://localhost:5000/stock/facts"
headers = {'content-type': 'application/json'}

# Send a request to each according
index = 0
while index < len(closeData):
    # Separate the data
    openValue = openData.values[index]
    closeValue = closeData.values[index]
    highValue = highData.values[index]
    lowValue = lowData.values[index]

    # Print the data as it will be sent
    print(str(openValue) + str(closeValue) + str(highValue) + str(lowValue))

    # Encoding JSON data
    data = r'{"close":' + str(closeValue) + ', "open":' + str(openValue) + ', "high":' + str(highValue) + ', "low":' + str(lowValue) + '}'

    # Send request
    response = requests.post(URL, headers=headers, data=data)

    # Wait 1 second
    time.sleep(1)

    # Increment index control
    index += 1
