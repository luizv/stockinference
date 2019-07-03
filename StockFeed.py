import time
from iexfinance.stocks import Stock
# from iexfinance.stocks import get_historical_data
import os
import requests

# SET API PERMISSIONS
os.environ["IEX_API_VERSION"] = "iexcloud-sandbox"
os.environ["IEX_TOKEN"] = "Tpk_d9cc24d84d83489d88e9faeaf93dbaf8"

aapl = Stock("AAPL")

URL = "http://localhost:5000/risk/facts"

headers = {'content-type': 'application/json'}

while True:
    fechamento = aapl.get_price()
    volume = aapl.get_volume()
    data = '{"values": [' + str(fechamento) + ',' + str(volume) + ']}'
    response = requests.post(URL, headers=headers, data=data)
    time.sleep(1)
