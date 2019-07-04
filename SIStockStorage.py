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

    def csv_path(self,stock):
        return SIConfig.storage_directory_name + stock + '.csv'


    def check_directory_created(stock):
        if not(os.path.exists('./' + SIConfig.storage_directory_name)):
            os.mkdir(SIConfig.storage_directory_name)


    def get_stock_archive(self, stock):
        path = self.csv_path(stock)
        if not(os.path.exists(path)):
            return
        else:
            return pd.read_csv(path)


    def stock_archive_exists(self, stock):
        path = self.csv_path(stock)
        if not (os.path.exists(path)):
            return
        else:
            return pd.read_csv(path)


    def savestocks(_):
        print("save")


#API
    def update_data(self, stock):
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

        self.check_directory_created()
        csv_name = self.csv_path(stock)

        updated_data.to_csv(csv_name)





