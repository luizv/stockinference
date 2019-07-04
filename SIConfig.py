from SIAnalysisType import SIAnalysisType
from SITradeType import SITradeType
from datetime import datetime

# SIConfig
class SIConfig:
    trade_type = SITradeType.daytrade
    analysis_type = SIAnalysisType.realtime
    initial_date = datetime(2017, 1, 1)


    storage_directory_name = "exports"

    symbols_list_name = "all_symbols"

    # Other variables
    #balance = 100000
