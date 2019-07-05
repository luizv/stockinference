from SIAnalysisType import SIAnalysisType
from SITradeType import SITradeType
from SITimeSeriesType import SITimeSeriesType
from datetime import datetime

# SIConfig
class SIConfig:
    trade_type    = SITradeType.daytrade
    analysis_type = SIAnalysisType.realtime
    data_type     = SITimeSeriesType.intradaily
    initial_date  = datetime(2017, 1, 1)
    intradaily_interval = 3

    storage_directory_name = "exports"
    symbols_directory_name = "symbol_lists"

#    symbols_list_name = "communications" #600 stocks
#    symbols_list_name = "techs"  #<10 stocks
    symbols_list_name = "aapl"  #<10 stocks

# Other variables
    #balance = 100000
