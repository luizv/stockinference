import pandas as pd
from datetime import datetime
from SIConfig import SIConfig
from SITimeSeriesType import SITimeSeriesType
from SIDatetimeFormatter import SIDatetimeFormatter
from datetime import timedelta

import json

## FOR STOCK DATA
from iexfinance.stocks import get_historical_intraday
from iexfinance.stocks import get_historical_data

## SET API PERMISSIONS
import os
os.environ["IEX_API_VERSION"]="iexcloud-sandbox"
os.environ["IEX_TOKEN"]="Tpk_d9cc24d84d83489d88e9faeaf93dbaf8"

class SIStockStorage:

    @staticmethod
    def csv_path(stock, directory=SIConfig.storage_directory_name):
        return directory +'/' + stock + '.csv'


    @staticmethod
    def check_directory_created():
        if not(os.path.exists(SIConfig.storage_directory_name)):
            os.mkdir(SIConfig.storage_directory_name)

        if not (os.path.exists(SIConfig.symbols_directory_name)):
            os.mkdir(SIConfig.symbols_directory_name)


    @staticmethod
    def get_stock_archive(stock) -> (pd.DataFrame):
        path = SIStockStorage.csv_path(stock)
        if not(os.path.exists(path)):
            return
        else:
            return pd.read_csv(path)



    @staticmethod
    def get_symbol_archive(listname=SIConfig.symbols_list_name):
        path = SIStockStorage.csv_path(listname, directory=SIConfig.symbols_directory_name)
        if not (os.path.exists(path)):
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
    def update_data(stock): #, type=SITimeSeriesType.daily):
        '''
        Get or update data store
        :param stock:
        :return:
        '''

        from_date = SIConfig.initial_date
        stock_data = SIStockStorage.get_stock_archive(stock)

        # if type == SITimeSeriesType.intradaily:
        #     from_date = SIConfig.initial_date
        #    stock_data = SIStockStorage.get_stock_archive(stock)



        if stock_data is not None:
           # stock_data = pd.DataFrame()
            from_date = stock_data.last_valid_index
        else:
            stock_data = pd.DataFrame()


        start = from_date
        end = datetime.now()

        new_data = get_historical_data(stock, start=start, end=end, output_format='pandas')

        updated_data = pd.concat([stock_data, new_data])
        #updated_data = updated_data.reset_index(drop=True)

        SIStockStorage.check_directory_created()
        csv_name = SIStockStorage.csv_path(stock)

        updated_data.to_csv(csv_name)


    @staticmethod
    def get_symbol_list(listname=SIConfig.symbols_list_name):
        df = SIStockStorage.get_symbol_archive(listname=listname)

        if df is not None:
            return list(df.symbol)
        else:
            return list()

    @staticmethod
    def update_data_for_symbol_list(listname=SIConfig.symbols_list_name):
        list = SIStockStorage.get_symbol_list(listname=listname)

        for symbol in list:
            SIStockStorage.update_data(stock=symbol)
            print(symbol)


    @staticmethod
    def get_intraday_data(listname=SIConfig.symbols_list_name):
        intraday_dict = dict()

        list=SIStockStorage.get_symbol_list(listname)

        for stock in list:
            df = pd.DataFrame()
            today = datetime.today()
            days = SIConfig.intradaily_interval
            count = 0

            while days > count:
                print("- DOWNLOAD INTRADAY [" + stock + "]: D-" + str(count))
                reference_day = today - timedelta(days=count)
                new_data = get_historical_intraday(stock, date=reference_day, output_format='pandas')
                df = pd.concat([df,new_data])
                count = count + 1

            df.index = pd.to_datetime(df.index)

            intraday_dict[stock] = df

        return intraday_dict


#SIStockStorage.update_data_for_symbol_list()

# ## TO GET STOCK LIST
#    from iexfinance.stocks import get_collections
#
#     @staticmethod
#     def get_stock_list():
#         categories = ["Electronic Technology", "Distribution Services", "Health Technology",
#                       "Commercial Services", "Industrial Services", "Finance",
#                       "Process Industries", "Transportation", "Technology Services",
#                       "Producer Manufacturing", "Retail Trade", "Consumer Services",
#                       "Non-Energy Minerals", "Utilities", "Miscellaneous", "Health Services",
#                       "Consumer Durables", "Consumer Non-Durables", "Communications",
#                       "Energy Minerals", "Government"]
#
#         for c in categories:
#             symbols = get_collections(c)
#             symbols_list = pd.DataFrame.from_dict(symbols)
#             SIStockStorage.check_directory_created()
#             symbols_list.to_csv(SIStockStorage.csv_path(c))
#
#
# SIStockStorage.get_stock_list()
#
# ## GET SYMBOLS (NEED REAL TOKEN)
# from iexfinance.refdata import get_symbols
#
# symbols = get_symbols(format='csv')
# symbols_list = pd.DataFrame.from_dict(symbols)
# SIStockStorage.check_directory_created()
# symbols_list.to_csv(SIStockStorage.csv_path("symbols_list"))

