import pandas as pd
from datetime import datetime
from SIConfig import SIConfig

import json

## FOR STOCK DATA
from iexfinance.stocks import get_historical_intraday

## SET API PERMISSIONS
import os
os.environ["IEX_API_VERSION"]="iexcloud-sandbox"
os.environ["IEX_TOKEN"]="Tpk_d9cc24d84d83489d88e9faeaf93dbaf8"

class SIStockStorage:

    @staticmethod
    def csv_path(stock):
        return SIConfig.storage_directory_name +'/' + stock + '.csv'

    @staticmethod
    def check_directory_created():
        if not(os.path.exists('./' + SIConfig.storage_directory_name)):
            os.mkdir(SIConfig.storage_directory_name)

    @staticmethod
    def get_stock_archive(stock):
        path = SIStockStorage.csv_path(stock)
        if not(os.path.exists(path)):
            return
        else:
            return pd.read_csv(path)

    @staticmethod
    def stock_archive_exists(stock):
        path = SIStockStorage.csv_path(stock)
        if not (os.path.exists(path)):
            return
        else:
            return pd.read_csv(path)

    @staticmethod
    def savestocks():
        print("save")


#API
    @staticmethod
    def update_data(stock):
        '''
        Get or update data store
        :param stock:
        :return:
        '''
        from_date = SIConfig.initial_date
        stock_data = SIStockStorage.get_stock_archive(stock)

        if stock_data is not None:
            print("update date")
            # from_date = last_updated_data_for_stock
        else:
            stock_data = pd.DataFrame.empty


        start = from_date
        end = datetime.now()

        new_data = get_historical_intraday(stock, start=start, end=end, output_format='pandas')

        updated_data = pd.concat(stock_data, new_data)
        updated_data = updated_data.reset_index(drop=True)

        SIStockStorage.check_directory_created()
        csv_name = SIStockStorage.csv_path(stock)

        updated_data.to_csv(csv_name)




### TO GET STOCK LIST
    # def get_stock_list(self, name):
    #     categories = ["Electronic Technology", "Distribution Services", "Health Technology",
    #      "Commercial Services",  "Industrial Services", "Finance",
    #      "Process Industries", "Transportation", "Technology Services",
    #      "Producer Manufacturing", "Retail Trade", "Consumer Services",
    #      "Non-Energy Minerals", "Utilities", "Miscellaneous", "Health Services",
    #      "Consumer Durables", "Consumer Non-Durables", "Communications",
    #      "Energy Minerals", "Government"]


### GET SYMBOLS (NEED REAL TOKEN)
#from iexfinance.refdata import get_symbols

# symbols = get_symbols(format='csv')
# symbols_list = pd.DataFrame.from_dict(symbols)
# SIStockStorage.check_directory_created()
# symbols_list.to_csv(SIStockStorage.csv_path("symbols_list"))

